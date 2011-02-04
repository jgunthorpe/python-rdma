#!/usr/bin/python
import rdma,rdma.path,sys;
import rdma.IBA as IBA;

TRACE_SEND = 0;
TRACE_COMPLETE = 1;

def simple_tracer(mt,kind,fmt=None,path=None,ret=None):
    """Simply logs summaries of what is happening to :data:`sys.stdout`.
    Assign to :attr:`rdma.madtransactor.MADTransactor.trace_func`."""
    if kind != TRACE_COMPLETE:
        return;
    desc = fmt.describe();

    if ret is None:
        print "debug: RPC %s TIMED OUT to '%s'."%(desc,path);
        return;
    else:
        print "debug: RPC %s completed to '%s'."%(desc,path);

def dumper_tracer(mt,kind,fmt=None,path=None,ret=None):
    """Logs full decoded packet dumps of what is happening to
    :data:`sys.stdout`.  Assign to
    :attr:`rdma.madtransactor.MADTransactor.trace_func`."""
    if kind != TRACE_COMPLETE:
        return;

    simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
    print "debug: Request",fmt.describe();
    fmt.printer(sys.stdout,header=False);
    if ret is not None:
        res = fmt.__class__(bytes(ret[0]));
        print "debug: Reply",res.describe()
        res.printer(sys.stdout,header=False);

class MADTransactor(object):
    """This class is a mixin for everything that implements a MAD RPC
    transaction interface. Derived classes must provide the :meth:`_execute`
    method which sends the MAD and gets the reply.

    By design instances of this interface cannot be multi-threaded. For
    multi-threaded applications each thread must have a separate
    :class:`MADTransactor` instance.  Simple MAD request/reply transactors
    return payload, other attributes for the last processed reply are
    available via instance attributes."""

    #: The path for the last reply packet processed
    reply_path = None;
    #: The MADFormat for the last reply packet processed
    reply_fmt = None;
    #: A function to call for tracing.
    trace_func = None;

    def __init__(self):
        self._tid = 0;

    def _execute(self,buf,path):
        """Send the fully formed MAD in buf to path and copy the reply
        into buf. Return path of the reply"""
        pass

    def _get_new_TID(self):
        self._tid = (self._tid + 1) % (1 << 32);
        return self._tid;

    @staticmethod
    def _get_match_key(buf):
        """Return a tuple that represents the 'key' for MAD buf.
        If two keys match then they are the same transaction."""
        # baseVersion,mgmtClass,classVersion method transactionID[31:0],attributeID
        if isinstance(buf,bytearray):
            return (bytes(buf[0:2]),buf[3],bytes(buf[12:18]));
        return (buf[0:2],ord(buf[3]),buf[12:18]);

    @staticmethod
    def _get_reply_match_key(buf):
        """Return a tuple that represents the 'key' for response to MAD buf.
        If two keys match then they are the same transaction."""
        # baseVersion,mgmtClass,classVersion method transactionID[31:0],attributeID
        x = MADTransactor._get_match_key(buf)
        return (x[0],x[1] | IBA.MAD_METHOD_RESPONSE,x[2]);

    def _prepareMAD(self,fmt,payload,attributeModifier,method,path):
        fmt.baseVersion = IBA.MAD_BASE_VERSION;
        fmt.mgmtClass = fmt.MAD_CLASS;
        fmt.classVersion = fmt.MAD_CLASS_VERSION;
        fmt.method = method;
        fmt.transactionID = self._get_new_TID();
        fmt.attributeID = payload.MAD_ATTRIBUTE_ID;
        fmt.attributeModifier = attributeModifier;

        # You can pass in the class object for payload and this means
        # send all zeros for it. Used for GET operations with no additional
        # inputs.
        if not isinstance(payload,type):
            payload.pack_into(fmt.data);
        fmt._buf = bytearray(fmt.MAD_LENGTH);
        fmt.pack_into(fmt._buf);

        if self.trace_func is not None:
            self.trace_func(self,TRACE_SEND,fmt=fmt,path=path);

    def _completeMAD(self,ret,fmt,path,newer,completer):
        if self.trace_func is not None:
            self.trace_func(self,TRACE_COMPLETE,ret=ret,fmt=fmt,path=path);

        if ret is None:
            raise rdma.MADTimeoutError(req=fmt,path=path);
        rbuf,self.reply_path = ret;

        # The try wrappers the unpack incase the MAD is busted somehow.
        if len(rbuf) != fmt.MAD_LENGTH:
            raise rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                msg="Invalid reply size. Got %u, expected %u"%(len(rbuf),
                                                                               fmt.MAD_LENGTH));
        try:
            self.reply_fmt = fmt.__class__(rbuf);
        except:
            e = rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                exc_info=sys.exc_info());
            raise rdma.MADError,e,e.exc_info[2]

        if (fmt.baseVersion != self.reply_fmt.baseVersion or
            fmt.mgmtClass != self.reply_fmt.mgmtClass or
            fmt.classVersion != self.reply_fmt.classVersion or
            fmt.attributeID != self.reply_fmt.attributeID or
            (fmt.method | IBA.MAD_METHOD_RESPONSE) != self.reply_fmt.method):
            raise rdma.MADError(req=fmt,rep=self.reply_fmt,path=path,
                                msg="Reply header does not match what is expected.");

        # FIXME: Handle BUSY
        # FIXME: Handle redirect
        status = self.reply_fmt.status;
        if status & 0x1F != 0:
            raise rdma.MADError(req=fmt,rep=self.reply_fmt,path=path,
                                status=self.reply_fmt.status);

        # Throw a class specific code..
        class_code = (status >> IBA.MAD_STATUS_CLASS_SHIFT) & IBA.MAD_STATUS_CLASS_MASK;
        if class_code != 0:
            raise rdma.MADClassError(req=fmt,rep=self.reply_fmt,path=path,
                                     status=self.reply_fmt.status,
                                     code=class_code);

        try:
            rpayload = newer(self.reply_fmt.data);
        except:
            e = rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                exc_info=sys.exc_info());
            raise rdma.MADError,e,e.exc_info[2]

        if completer:
            return completer(rpayload);
        return rpayload;

    def _doMAD(self,fmt,payload,path,attributeModifier,method,completer=None):
        """To support the asynchronous MADTransactor models the RPC wrapper
        caller must always return _doMAD(). If for some reason there is some
        post-processing work to do then a completer function must be specified
        to do it."""
        self._prepareMAD(fmt,payload,attributeModifier,method,path);
        ret = self._execute(fmt._buf,path);
        newer = payload if isinstance(payload,type) else payload.__class__;
        return self._completeMAD(ret,fmt,path,newer,completer);

    def _subn_do(self,payload,path,attributeModifier,method):
        if isinstance(path,rdma.path.IBDRPath):
            fmt = IBA.SMPFormatDirected();
            fmt.drSLID = path.drSLID;
            fmt.drDLID = path.drDLID;
            fmt.initialPath[:len(path.drPath)] = path.drPath;
            fmt.hopCount = len(path.drPath)-1;
        else:
            fmt = IBA.SMPFormat();
        return self._doMAD(fmt,payload,path,attributeModifier,method);

    def SubnGet(self,payload,path,attributeModifier=0):
        return self._subn_do(payload,path,attributeModifier,
                           payload.MAD_SUBNGET);
    def SubnSet(self,payload,path,attributeModifier=0):
        return self._subn_do(payload,path,attributeModifier,
                           payload.MAD_SUBNSET);

    def PerformanceGet(self,payload,path,attributeModifier=0):
        return self._doMAD(IBA.PMFormat(),payload,path,attributeModifier,
                           payload.MAD_PERFORMANCEGET);
    def PerformanceSet(self,payload,path,attributeModifier=0):
        return self._doMAD(IBA.PMFormat(),payload,path,attributeModifier,
                           payload.MAD_PERFORMANCESET);

    def _subn_adm_do(self,payload,path,attributeModifier,method):
        fmt = IBA.SAFormat();
        if isinstance(payload,IBA.ComponentMask):
            fmt.componentMask = payload.component_mask;
            payload = payload.payload;
        # fmt.SMKey = path.SMKey;
        return self._doMAD(fmt,payload,path,attributeModifier,method);

    def SubnAdmGet(self,payload,path,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                           payload.MAD_SUBNADMGET);
    def SubnAdmSet(self,payload,path,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                           payload.MAD_SUBNADMSET);

    # TODO ['BMGet', 'BMSet', 'CommMgtGet', 'CommMgtSend', 'CommMgtSet',
    # 'DevMgtGet', 'DevMgtSet', 'SNMPGet',
    # 'SNMPSend', 'SubnAdmDelete', 'SubnAdmGet', 'SubnAdmGetMulti',
    # 'SubnAdmGetTable', 'SubnAdmGetTraceTable', 'SubnAdmSet']
