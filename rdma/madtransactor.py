#!/usr/bin/python
import rdma,rdma.path,sys;
import rdma.IBA as IBA;

TRACE_SEND = 0;
TRACE_COMPLETE = 1;
TRACE_UNEXPECTED = 2;

def simple_tracer(mt,kind,fmt=None,path=None,ret=None):
    """Simply logs summaries of what is happening to :data:`sys.stdout`.
    Assign to :attr:`rdma.madtransactor.MADTransactor.trace_func`."""
    if kind == TRACE_COMPLETE:
        desc = fmt.describe();

        if ret is None:
            print "debug: RPC %s TIMED OUT to '%s'."%(desc,path);
            return;
        else:
            print "debug: RPC %s completed to '%s'."%(desc,path);
    if kind == TRACE_UNEXPECTED:
        print "debug: Got unexpected MAD from '%s'."%(ret[1]);

def dumper_tracer(mt,kind,fmt=None,path=None,ret=None):
    """Logs full decoded packet dumps of what is happening to
    :data:`sys.stdout`.  Assign to
    :attr:`rdma.madtransactor.MADTransactor.trace_func`."""
    if kind == TRACE_COMPLETE:
        simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
        print "debug: Request",fmt.describe();
        fmt.printer(sys.stdout,header=False);
        if ret is not None:
            res = fmt.__class__(bytes(ret[0]));
            print "debug: Reply",res.describe()
            res.printer(sys.stdout,header=False);
    if kind == TRACE_UNEXPECTED:
        simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
        IBA.MADHeader(bytes(ret[0])).printer(sys.stdout);

class MADTransactor(object):
    """This class is a mixin for everything that implements a MAD RPC
    transaction interface. Derived classes must provide the :meth:`_execute`
    method which sends the MAD and gets the reply.

    By design instances of this interface cannot be multi-threaded. For
    multi-threaded applications each thread must have a separate
    :class:`MADTransactor` instance.  Simple MAD request/reply transactors
    return payload, other attributes for the last processed reply are
    available via instance attributes.

    Paths used with this object can have a MKey (for SMPs) and SMKey (for
    SA GMPs) attribute."""

    #: The path for the last reply packet processed
    reply_path = None;
    #: The MADFormat for the last reply packet processed
    reply_fmt = None;
    #: A function to call for tracing.
    trace_func = None;
    #: The end_port this is associated with
    end_port = None;

    def _execute(self,buf,path):
        """Send the fully formed MAD in buf to path and copy the reply
        into buf. Return path of the reply"""
        pass

    def _get_new_TID(self):
        """Override in derived classes."""
        pass;

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
        # Hmmm, I wonder if this should live someplace else?
        if x[1] == IBA.MAD_METHOD_SET:
            return (x[0],IBA.MAD_METHOD_GET_RESP,x[2]);
        else:
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

        rmpp = False;
        nfmt = fmt.__class__;
        if getattr(fmt,"RMPPVersion",None) is not None:
            # Quick check if RMPP was used
            if (rbuf[26] & IBA.RMPP_ACTIVE):
                nfmt = IBA.SAHeader; # FIXME, should be class specific
                rmpp = True;

        if ((not rmpp and len(rbuf) != fmt.MAD_LENGTH) or
            (rmpp and len(rbuf) < nfmt.MAD_LENGTH)):
            raise rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                msg="Invalid reply size. Got %u, expected %u"%(len(rbuf),
                                                                               fmt.MAD_LENGTH));
        # The try wrappers the unpack incase the MAD is busted somehow.
        try:
            self.reply_fmt = nfmt(rbuf);
        except:
            e = rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                exc_info=sys.exc_info());
            raise rdma.MADError,e,e.exc_info[2]

        # Note that everything in get_reply_match_key has already been
        # checked

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
            if rmpp:
                # For this path the entire RMPP protocol must have been done
                # and we expect a single MAD that contains a SAHeader plus
                # all the data.
                if self.reply_fmt.attributeOffset == 0:
                    rpayload = [];
                else:
                    step = 8*self.reply_fmt.attributeOffset;
                    if step < newer.MAD_LENGTH:
                        raise rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                            status=self.reply_fmt.status,
                                            msg="RMPP attribute is too small. Got %u, expected %u"%(
                                                step,newer.MAD_LENGTH));

                    start = self.reply_fmt.MAD_LENGTH;
                    count = (len(rbuf) - start)//(step);
                    #self.reply_fmt.printer(sys.stdout);
                    #print start,step,len(rpayload),len(rbuf);
                    #print repr(rbuf[start+step*len(rpayload):]);
                    # I wonder why the data2 element makes no sense?
                    if start + step*count > len(rbuf):
                        raise rdma.MADError(req=fmt,rep_buf=rbuf,path=path,
                                            status=self.reply_fmt.status,
                                            msg="RMPP complete packet was too short.");
                    rpayload = [newer(rbuf[start + step*I:start + step*(I+1)])
                                for I in range(count)];
            else:
                rpayload = newer(self.reply_fmt.data);
        except rdma.MADError:
            raise
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
        fmt.MKey = getattr(path,"MKey",0);
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
        fmt.SMKey = getattr(path,"SMKey",0);
        return self._doMAD(fmt,payload,path,attributeModifier,method);

    def SubnAdmGet(self,payload,path,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                           payload.MAD_SUBNADMGET);
    def SubnAdmGetTable(self,payload,path,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                                 payload.MAD_SUBNADMGETTABLE);
    def SubnAdmSet(self,payload,path,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                           payload.MAD_SUBNADMSET);

    # TODO ['BMGet', 'BMSet', 'CommMgtGet', 'CommMgtSend', 'CommMgtSet',
    # 'DevMgtGet', 'DevMgtSet', 'SNMPGet',
    # 'SNMPSend', 'SubnAdmDelete', 'SubnAdmGet', 'SubnAdmGetMulti',
    # 'SubnAdmGetTable', 'SubnAdmGetTraceTable', 'SubnAdmSet']
