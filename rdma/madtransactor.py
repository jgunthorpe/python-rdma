# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import rdma,rdma.path,sys;
import rdma.IBA as IBA;

TRACE_SEND = 0;
TRACE_COMPLETE = 1;
TRACE_UNEXPECTED = 2;
TRACE_RECEIVE = 3;
TRACE_REPLY = 4;

class _MADFormat(rdma.binstruct.BinFormat,IBA.MADHeader):
    """Support clase to let us trace error MADs."""
    def __init__(self,buf):
        IBA.MADHeader.__init__(self,buf);
        self.match = MADTransactor.get_request_match_key(buf);
    def describe(self):
        '''Return a short description of the RPC described by this format.'''
        kind = IBA.get_fmt_payload(*self.match);
        return '%s %s(%u.%u) %s(%u)'%(IBA.const_str('MAD_METHOD_',self.method,True),
                                      '??' if kind[0] is None else kind[0].__name__,
                                      self.mgmtClass,self.classVersion,
                                      '??' if kind[1] is None else kind[1].__name__,
                                      self.attributeID);

def simple_tracer(mt,kind,fmt=None,path=None,ret=None):
    """Simply logs summaries of what is happening to :data:`sys.stdout`.
    Assign to :attr:`rdma.madtransactor.MADTransactor.trace_func`."""
    if kind == TRACE_COMPLETE:
        desc = fmt.describe();

        if ret is None:
            print "D: RPC %s TIMED OUT to '%s'."%(desc,path);
            return;
        else:
            print "D: RPC %s completed to '%s' len %u."%(desc,path,len(ret[0]));
    if kind == TRACE_RECEIVE:
        print "D: RPC %s received from '%s' len %u."%(fmt.describe(),
                                                          path,len(ret[0]));
    if kind == TRACE_REPLY:
        print "D: RPC %s reply to '%s'"%(fmt.describe(),path);
    if kind == TRACE_UNEXPECTED:
        print "D: Got unexpected MAD from '%s'."%(ret[1]);

def dumper_tracer(mt,kind,fmt=None,path=None,ret=None):
    """Logs full decoded packet dumps of what is happening to
    :data:`sys.stdout`.  Assign to
    :attr:`rdma.madtransactor.MADTransactor.trace_func`."""
    if kind == TRACE_COMPLETE:
        simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
        print "D: Request",fmt.describe();
        fmt.printer(sys.stdout,header=False);
        if ret is not None:
            res = fmt.__class__(bytes(ret[0]));
            print "D: Reply",res.describe()
            res.printer(sys.stdout,header=False);
    if kind == TRACE_UNEXPECTED:
        simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
        IBA.MADHeader(bytes(ret[0])).printer(sys.stdout);
    if kind == TRACE_RECEIVE:
        simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
        if fmt is not None:
            print "D: Incoming request",fmt.describe();
            fmt.printer(sys.stdout,header=False);
    if kind == TRACE_REPLY:
        simple_tracer(mt,kind,fmt=fmt,path=path,ret=ret);
        if fmt is not None:
            print "D: Outgoing reply",fmt.describe();
            fmt.printer(sys.stdout,header=False);

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

    # Used when emulating an async interface in do_async
    result = None;

    @property
    def is_async(self):
        """True if this is an async MADTransactor interface."""
        return False;

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

    @staticmethod
    def get_request_match_key(buf):
        """Return a :class:`tuple` for matching a request MAD buf. The :class:`tuple`
        is `((oui << 8) | mgmtClass,(baseVersion << 8) | classVersion,attributeID)`. Where *oui* is 0
        if this is not a vendor OUI MAD."""
        if isinstance(buf,bytearray):
            mgmtClass = buf[1];
            classVersion = (buf[0] << 8) | buf[2];
            attr = (buf[16] << 8) | buf[17];
            if mgmtClass >= 0x30 and mgmtClass <= 0x4F:
                oui = (buf[37] << 16) | (buf[38] << 8) | buf[39];
            else:
                oui = 0;
        else:
            mgmtClass = ord(buf[1]);
            classVersion = (ord(buf[0]) << 8) | ord(buf[2]);
            attr = (ord(buf[16]) << 8) | ord(buf[17]);
            if mgmtClass >= 0x30 and mgmtClass <= 0x4F:
                oui = (ord(buf[37]) << 16) | (ord(buf[38]) << 8) | ord(buf[39]);
            else:
                oui = 0;
        return ((oui << 8) | mgmtClass,classVersion,attr);

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
        buf = bytearray(fmt.MAD_LENGTH);
        fmt.pack_into(buf);

        if self.trace_func is not None:
            self.trace_func(self,TRACE_SEND,fmt=fmt,path=path);
        return buf

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
                                rep_buf=rbuf,status=self.reply_fmt.status);

        # Throw a class specific code..
        class_code = (status >> IBA.MAD_STATUS_CLASS_SHIFT) & IBA.MAD_STATUS_CLASS_MASK;
        if class_code != 0:
            if isinstance(completer,tuple):
                self.req_fmt = fmt;
                self.req_path = path;
                ret = completer[1](self.reply_fmt,class_code);
                if ret is not None:
                    ret = completer[0](ret);
                self.req_fmt = None;
                self.req_path = None;
                if ret is not None:
                    return ret;
            raise rdma.MADClassError(req=fmt,rep=self.reply_fmt,path=path,
                                     status=self.reply_fmt.status,
                                     rep_buf=rbuf,code=class_code);

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
                        raise rdma.MADError(req=fmt,rep=self.reply_fmt,path=path,
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
                        raise rdma.MADError(req=fmt,rep=self.reply_fmt,path=path,
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
            self.req_fmt = fmt;
            self.req_path = path;
            if isinstance(completer,tuple):
                ret = completer[0](rpayload);
            else:
                ret = completer(rpayload);
            self.req_fmt = None;
            self.req_path = None;
            return ret;
        return rpayload;

    def _doMAD(self,fmt,payload,path,attributeModifier,method,completer=None):
        """To support the asynchronous MADTransactor models the RPC wrapper
        caller must always return _doMAD(). If for some reason there is some
        post-processing work to do then a completer function must be specified
        to do it."""
        buf = self._prepareMAD(fmt,payload,attributeModifier,method,path);
        ret = self._execute(buf,path);
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

    def _subn_adm_do(self,payload,path,attributeModifier,method,completer=None):
        if path is None:
            path = self.end_port.sa_path;
        fmt = IBA.SAFormat();
        if isinstance(payload,IBA.ComponentMask):
            fmt.componentMask = payload.component_mask;
            payload = payload.payload;
        fmt.SMKey = getattr(path,"SMKey",0);
        return self._doMAD(fmt,payload,path,attributeModifier,method,completer);

    def SubnAdmGet(self,payload,path=None,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                           payload.MAD_SUBNADMGET);
    def SubnAdmGetTable(self,payload,path=None,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                                 payload.MAD_SUBNADMGETTABLE);
    def SubnAdmSet(self,payload,path=None,attributeModifier=0):
        return self._subn_adm_do(payload,path,attributeModifier,
                           payload.MAD_SUBNADMSET);

    def _vend_do(self,payload,path,attributeModifier,method):
        fmt = payload.FORMAT();
        return self._doMAD(fmt,payload,path,attributeModifier,method);

    def VendGet(self,payload,path,attributeModifier=0):
        return self._vend_do(payload,path,attributeModifier,
                             payload.MAD_VENDGET);
    def VendSet(self,payload,path,attributeModifier=0):
        return self._vend_do(payload,path,attributeModifier,
                             payload.MAD_VENDSET);

    def parse_request(self,rbuf,path):
        """Parse a request packet into a format and data.

        :raises rdma.MADError: If the packet could not be parsed."""
        l = len(rbuf);
        if l <= IBA.MADHeader.MAD_LENGTH:
            raise rdma.MADError(req_buf=rbuf,path=path,
                                reply_status=0,
                                msg="Invalid request size.Got %u, expected at least %u"%(
                                    l,IBA.MADHeader.MAD_LENGTH));
        match = self.get_request_match_key(rbuf);
        if match[1] >> 8 != IBA.MAD_BASE_VERSION:
            raise rdma.MADError(req_buf=rbuf,path=path,
                                reply_status=IBA.MAD_STATUS_BAD_VERSION,
                                msg="Invalid base version, got key %r"%(match));
        kind = IBA.get_fmt_payload(*match);
        if kind[0] is None:
            for clsid,ver in IBA.CLASS_TO_STRUCT.iterkeys():
                if clsid == kind[0]:
                    raise rdma.MADError(req_buf=rbuf,path=path,
                                        reply_status=IBA.MAD_STATUS_BAD_VERSION,
                                        msg="Invalid class version, got key %r"%(match));
            raise rdma.MADError(req_buf=rbuf,path=path,
                                reply_status=IBA.MAD_STATUS_UNSUP_METHOD,
                                msg="Unsupported class ID, got key %r"%(match));
        if l != kind[0].MAD_LENGTH:
            raise rdma.MADError(req_buf=rbuf,path=path,
                                reply_status=0,
                                msg="Invalid request size.Got %u, expected %u"%(
                                    l,kind[0].MAD_LENGTH));

        # The try wrappers the unpack incase the MAD is busted somehow.
        try:
            fmt = kind[0](rbuf);
            if self.trace_func is not None:
                self.trace_func(self,TRACE_RECEIVE,fmt=fmt,path=path,
                                ret=(rbuf,path));
            if kind[1] is None:
                raise rdma.MADError(req=fmt,req_buf=rbuf,path=path,
                                    reply_status=IBA.MAD_STATUS_UNSUP_METHOD_ATTR_COMBO,
                                    msg="Unsupported attribute ID for %s, got key %r"%(
                                        fmt.describe(),match));
            return fmt,kind[1](fmt.data);
        except rdma.MADError:
            raise
        except:
            e = rdma.MADError(req_buf=rbuf,path=path,
                              reply_status=IBA.MAD_STATUS_INVALID_ATTR_OR_MODIFIER,
                              exc_info=sys.exc_info());
            raise rdma.MADError,e,e.exc_info[2]

    def send_error_exc(self,exc):
        """Call :meth:`send_error_reply` with the arguments derived from
        the :exc:`rdma.MADError` exception passed in."""
        status = getattr(exc,"reply_status",IBA.MAD_STATUS_UNSUP_METHOD);
        if status == 0:
            return
        self.send_error_reply(exc.req_buf,exc.path,status);

    def send_error_reply(self,buf,path,status,class_code=0):
        """Generate an error reply for a MAD. *buf* is the full original
        packet. This entire packet is returned with an appropriate error code
        set. *status* and *class_code* should be set to the appropriate result
        code."""
        hdr = _MADFormat(buf);
        hdr.status = (status & 0x1F) | ((class_code & IBA.MAD_STATUS_CLASS_MASK) <<  IBA.MAD_STATUS_CLASS_SHIFT)
        if hdr.method == IBA.MAD_METHOD_SET:
            hdr.method = IBA.MAD_METHOD_GET_RESP
        else:
            hdr.method = hdr.method | IBA.MAD_METHOD_RESPONSE;
        buf = bytearray(buf);
        hdr.pack_into(buf);

        path.reverse();
        if self.trace_func is not None:
            self.trace_func(self,TRACE_REPLY,fmt=hdr,path=path);
        self.sendto(buf,path);

    def send_reply(self,ofmt,payload,path,attributeModifier=0,
                   status=0,class_code=0):
        """Generate a reply packet. *ofmt* should be the request format."""
        fmt = ofmt.__class__();
        fmt.baseVersion = IBA.MAD_BASE_VERSION;
        fmt.mgmtClass = fmt.MAD_CLASS;
        fmt.classVersion = fmt.MAD_CLASS_VERSION;
        fmt.status = (status & 0x1F) | ((class_code & IBA.MAD_STATUS_CLASS_MASK) <<  IBA.MAD_STATUS_CLASS_SHIFT)
        if ofmt.method == IBA.MAD_METHOD_SET:
            fmt.method = IBA.MAD_METHOD_GET_RESP
        else:
            fmt.method = ofmt.method | IBA.MAD_METHOD_RESPONSE;
        fmt.transactionID = ofmt.transactionID;
        fmt.attributeID = ofmt.attributeID;
        fmt.attributeModifier = attributeModifier;

        if not isinstance(payload,type):
            payload.pack_into(fmt.data);
        buf = bytearray(fmt.MAD_LENGTH);
        fmt.pack_into(buf);

        path.reverse();
        if self.trace_func is not None:
            self.trace_func(self,TRACE_REPLY,fmt=fmt,path=path);
        self.sendto(buf,path);

    def do_async(self,op):
        """This runs a simple async work coroutine against a synchronous
        instance. In this case the coroutine yields its own next result."""
        assert(self.is_async == False);
        if op is None:
            return self.result;
        result = None;
        self.result = None;
        while True:
            try:
                if result is None:
                    result = op.next();
                else:
                    result = op.send(result);
                    if result is None:
                        result = True;
            except StopIteration:
                return self.result;

    # TODO ['BMGet', 'BMSet', 'CommMgtGet', 'CommMgtSend', 'CommMgtSet',
    # 'DevMgtGet', 'DevMgtSet', 'SNMPGet',
    # 'SNMPSend', 'SubnAdmDelete', 'SubnAdmGetMulti',
    # 'SubnAdmGetTraceTable', 'SubnAdmSet']
