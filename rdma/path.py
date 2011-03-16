# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import os;
import sys;
import rdma;
import rdma.IBA as IBA;

class Path(object):
    """Describe an RDMA path. This also serves to cache the path for cases
    that need it in an AH or other format. Paths should be considered final,
    once construction is finished their content must never change. This is to
    prevent cached data in the path from becoming stale.

    The :func:`repr` format will produce a string that is valid Python and is also
    compatible with :func:`from_spec_string`."""

    #: Number of times a MAD will be resent, or the value of retry_cnt for a
    #: RC QP.
    retries = 0;
    #: End Port this path is associated with
    end_port = None;

    def __init__(self,end_port,**kwargs):
        """*end_port* is the :class:`rdma.devices.EndPort` this path is
        associated with. *kwargs* is applied to set attributes of the
        instance during initialization."""
        if isinstance(end_port,str) or isinstance(end_port,unicode):
            end_port = rdma.get_end_port(end_port);
        self.end_port = end_port;
        for k,v in kwargs.iteritems():
            setattr(self,k,v);

    def copy(self,**kwargs):
        """Return a new path object that is a copy of this one. This takes
        care of the internal caching mechanism.  *kwargs* is applied to set
        attributes of the instance after copying."""
        # Note: The copy module uses the __reduce__ call, so we may as
        # well just use it directly.
        tp = self.__reduce__();
        tp[2].update(kwargs);
        return tp[0](self.end_port,**tp[2]);

    def drop_cache(self):
        """Release any cached information."""
        for I in self.__dict__.keys():
            if I.startswith("_cached"):
                self.__delattr__(I);

    def __repr__(self):
        cls = self.__class__;
        keys = ("%s=%s"%(k,getattr(cls,"_format_%s"%(k),lambda x:repr(x))(v))
                for k,v in sorted(self.__dict__.iteritems())
                if k[0] != "_" and k != "end_port" and getattr(cls,k,None) != v);
        if self.end_port is None:
            ep = None;
        else:
            ep = str(self.end_port)
        return "%s(end_port=%r, %s)"%(cls.__name__,ep,", ".join(keys));

    def __reduce__(self):
        """When we pickle :class:`~rdma.path.IBPath` objects the *end_port*
        attribute is thrown away and not restored."""
        cls = self.__class__;
        d = dict((k,v) for k,v in self.__dict__.iteritems()
                 if k[0] != "_" and k != "end_port" and getattr(cls,k,None) != v);
        return (cls,(None,),d);

class IBPath(Path):
    """Describe a path in an IB network with a LRH and GRH and BTH

    Our convention is that a path describes the LRH/GRH/BTH header fields on
    the wire. So a packet being sent from here should have a path with
    :attr:`SGID` == self and the path for a received packet should have
    :attr:`DGID` == self.  Ditto for *[ds]qpn* and *[DS]LID*. Paths for packets
    received will thus have reversed semantics, :attr:`SGID` == remote.

    This includes all relevant addressing information as well as any
    method specific information (ie a UMAD agent_id) required to use
    it with the method in question. Since this includes the BTH information
    it must also include the DQPN if that is required (eg for unconnected
    communication)"""

    #: Holds :attr:`rdma.IBA.HdrLRH.DLID`
    DLID = 0;
    #: Holds :attr:`rdma.IBA.HdrLRH.SLID`
    SLID = 0;
    #: Holds :attr:`rdma.IBA.HdrLRH.SL`
    SL = 0;
    #: Holds :attr:`rdma.IBA.HdrBTH.PKey`
    pkey = IBA.PKEY_DEFAULT;
    #: True if a :class:`rdma.IBA.HdrGRH` is present
    has_grh = False;

    # These are only present if the path is going got be used for
    # something connectionless
    #: Holds :attr:`rdma.IBA.HdrBTH.destQP`
    dqpn = None;
    #: Holds :attr:`rdma.IBA.HdrDETH.srcQP`
    sqpn = None;
    #: Holds :attr:`rdma.IBA.HdrDETH.QKey`
    qkey = None;

    #: Maximum MTU to use on this path
    MTU = IBA.MTU_256;
    #: Maximum injection rate for this path
    rate = IBA.PR_RATE_2Gb5;

    # These are only present if has_grh is True
    #: Holds :attr:`rdma.IBA.HdrGRH.SGID`
    SGID = None;
    #: Holds :attr:`rdma.IBA.HdrGRH.DGID`
    DGID = None;
    #: Holds :attr:`rdma.IBA.HdrGRH.hopLmt`
    hop_limit = 0;
    #: Holds :attr:`rdma.IBA.HdrGRH.TClass`
    traffic_class = 0;
    #: Holds :attr:`rdma.IBA.HdrGRH.flowLabel`
    flow_label = 0;

    # MAD specific things
    #: Method specific - override the *agent_id* for :class:`rdma.umad.UMAD`
    umad_agent_id = None;
    #: Used to compute :attr:`mad_timeout`
    resp_time = 20; # See C13-13.1.1

    # QP specific things
    #: Minimum value for `rdma.IBA.HdrAETH.syndrome` for
    #: RNR NAK. (FIXME: Where does this come from??)
    min_rnr_timer = 0;
    #: Destination ack response time. Used to compute :attr:`qp_timeout`
    dack_resp_time = 20;
    #: Source RC ack response time. Value is from :meth:`rdma.ibverbs.Context.query_device`.
    sack_resp_time = 20;
    #: Destination queue PSN, holds the initial value for the remote :attr:`sqpsn`.
    dqpsn = 0;
    #: Source queue PSN, holds the initial value for :attr:`rdma.IBA.HdrBTH.PSN`
    sqpsn = 0;
    #: Destination issuable RD atomic
    drdatomic = 255;
    #: Source issuable RD atomic
    srdatomic = 255;

    def reverse(self,for_reply=True):
        """Reverse this path in-place according to IBA 13.5.4. If *for_reply*
        is `True` then the reversed path will be usable as a MAD reply,
        otherwise it is simply reversed (the only difference is that reply paths
        have the hop_limit set to 255). Returns `self`"""
        self.DLID,self.SLID = self.SLID,self.DLID;
        self.dqpn ,self.sqpn = self.sqpn,self.dqpn;
        self.DGID,self.SGID = self.SGID,self.DGID;
        if self.has_grh and for_reply:
            self.hop_limit = 0xff;
        self.dack_resp_time,self.sack_resp_time = self.sack_resp_time,self.dack_resp_time;
        self.dqpsn,self.sqpsn = self.sqpsn,self.dqpsn;
        self.drdatomic,self.srdatomic = self.srdatomic,self.drdatomic
        self.drop_cache();
        return self

    @property
    def SGID_index(self):
        """Cache and return the index of the SGID for the associated
        :class:`~rdma.devices.EndPort`. Assignment updates the :attr:`SGID`
        value."""
        try:
            return self._cached_SGID_index;
        except AttributeError:
            pass
        try:
            self._cached_SGID_index = self.end_port.gids.index(self.SGID);
            return self._cached_SGID_index;
        except ValueError:
            raise rdma.RDMAError("GID %s not available on %s"%(self.SGID,self.end_port));
    @SGID_index.setter
    def SGID_index(self,value):
        self.SGID = self.end_port.gids[value];
        self._cached_SGID_index = value;

    @property
    def pkey_index(self):
        """Cache and return the index of the PKey for the associated
        :class:`~rdma.devices.EndPort`. Assignment updates the :attr:`pkey`
        value."""
        try:
            return self._cached_pkey_index;
        except AttributeError:
            pass
        try:
            self._cached_pkey_index = self.end_port.pkeys.index(self.pkey);
            return self._cached_pkey_index;
        except ValueError:
            raise rdma.RDMAError("PKey 0x%x not available on %s"%(self.pkey,self.end_port));
    @pkey_index.setter
    def pkey_index(self,value):
        self.pkey = self.end_port.pkeys[value];
        self._cached_pkey_index = value;

    @property
    def SLID_bits(self):
        """Cache and return the LMC portion of the
        :attr:`SLID`. Assignment updates the :attr:`SLID` using the value from
        :attr:`rdma.devices.EndPort.lid`."""
        # FIXME: Don't think more than this is actually necessary, the mask in
        # done in the kernel, drivers and HW as well. Kept as a placeholder.
        return self.SLID & 0xFF;
    @SLID_bits.setter
    def SLID_bits(self,value):
        self.SLID = value | self.end_port.lid;

    @property
    def DLID_bits(self):
        """Cache and return the LMC portion of the
        :attr:`DLID`. Assignment updates the :attr:`DLID` using the value from
        :attr:`rdma.devices.EndPort.lid`."""
        # FIXME: Don't think more than this is actually necessary, the mask in
        # done in the kernel, drivers and HW as well. Kept as a placeholder.
        return self.DLID & 0xFF;
    @DLID_bits.setter
    def DLID_bits(self,value):
        self.DLID = value | self.end_port.lid;

    @property
    def packet_life_time(self):
        """The packet lifetime value for this path. The lifetime value for the
        path is the expected uni-directional transit time.  If a value has not
        been provided then the port's
        :attr:`rdma.devices.EndPort.subnet_timeout` is used. To convert
        to seconds use 4.096 uS * 2**(packet_life_time)"""
        return self.__dict__.get("packet_life_time",self.end_port.subnet_timeout);
    @packet_life_time.setter
    def packet_life_time(self,value):
        self.__dict__["packet_life_time"] = value;

    @property
    def mad_timeout(self):
        """The timeout to use for MADs on this path. Expressed
        as float seconds."""
        try:
            return self._cached_mad_timeout;
        except AttributeError:
            self._cached_mad_timeout = 4.096E-6*(2**(self.packet_life_time+1) +
                                                 2**self.resp_time);
            return self._cached_mad_timeout;

    @property
    def qp_timeout(self):
        """The timeout to use for RC/RD connections. This is 2 *
        packet_life_time + target_ack_delay. Expressed as float seconds."""
        try:
            return self._cached_qp_timeout;
        except AttributeError:
            self._cached_qp_timeout = 4.096E-6*(2**(self.packet_life_time+1) +
                                                2**self.dack_resp_time);
            return self._cached_qp_timeout;

    @classmethod
    def _format_pkey(cls,v):
        return "0x%x"%(v);
    _format_qkey = _format_pkey
    @classmethod
    def _format_DLID(cls,v):
        if v >= IBA.LID_MULTICAST:
            return "0x%x"%(v);
        return str(v);
    _format_SLID = _format_DLID

    def __str__(self):
        if self.has_grh:
            res = "%s %r -> %s %u TC=%r FL=%r HL=%r"%(
                self.SGID,self.SLID,self.DGID,self.DLID,self.traffic_class,
                self.flow_label,self.hop_limit);
        else:
            res = "%r -> %r"%(self.SLID,self.DLID);
        return "Path %s SL=%r PKey=0x%x DQPN=%r"%(
            res,self.SL,self.pkey,self.dqpn);

class IBDRPath(IBPath):
    """Describe a directed route path in an IB network using a VL15 QP0 packet,
    a LRH and :class:`rdma.IBA.SMPFormatDirected` MADs."""
    #: Holds :attr:`rdma.IBA.SMPFormatDirected.drSLID`. Should be the same as SLID.
    drSLID = 0xFFFF;
    #: Holds :attr:`rdma.IBA.SMPFormatDirected.drDLID`
    drDLID = 0xFFFF;
    #: Holds :attr:`rdma.IBA.SMPFormatDirected.drPath`. len(:attr:`drPath`) is used to set *hopCount*.
    drPath = None;

    def __init__(self,end_port,**kwargs):
        """*end_port* is the :class:`rdma.devices.EndPort` this path is
        associated with. *kwargs* is applied to set attributes of the
        instance during initialization.

        By default this class construct a DR path to the local port."""
        self.DLID = IBA.LID_PERMISSIVE;
        self.SLID = IBA.LID_PERMISSIVE;
        self.drPath = bytes(chr(0));
        self.dqpn = 0;
        self.sqpn = 0;
        self.qkey = IBA.IB_DEFAULT_QP0_QKEY;
        IBPath.__init__(self,end_port,**kwargs);

    @property
    def SGID_index(self):
        """raises :exc:`AttributeError`, GID addressing is not possible for DR paths."""
        raise AttributeError();

    @property
    def has_grh(self):
        """Returns False, GID addressing is not possible for DR paths."""
        return False;

    @classmethod
    def _format_drPath(cls,v):
        return ":".join("%u"%(ord(I)) for I in v) + ":";

    def __str__(self):
        # No LID components
        drPath = tuple(ord(I) for I in self.drPath);
        if self.drDLID == IBA.LID_PERMISSIVE and self.drSLID == IBA.LID_PERMISSIVE:
            return "DR Path %r"%(drPath,);
        # LID route at the start
        if self.drDLID == IBA.LID_PERMISSIVE and self.drSLID != IBA.LID_PERMISSIVE:
            return "DR Path %u -> %r"%(self.DLID,drPath);
        # LID route at the end
        if self.drDLID != IBA.LID_PERMISSIVE and self.drSLID == IBA.LID_PERMISSIVE:
            return "DR Path %r -> %u"%(drPath,self.drDLID);
        # Double ended
        return "DR Path %u -> %r -> %u"%(self.DLID,drPath,self.drDLID);

class SAPathNotFoundError(rdma.MADClassError):
    """Thrown when a path record query fails with a no records error
    from the SM."""
    def __init__(self,fmt,err=None):
        rdma.MADClassError._copy_init(self,err);
        self.message(fmt);

class LazyIBPath(IBPath):
    """Similar to :class:`rdma.path.IBPath` but the unpack of the actual data
    deferred until necessary since most of the time we do not care."""
    def __getattribute__(self,name):
        if name[0] != '_':
            # I wonder if this is evil? We switch out class to the
            # parent the first time someone requests an attribute.
            cls = self.__class__
            object.__setattr__(self,"__class__",rdma.path.IBPath);
            cls._unpack_rcv(self);
        return object.__getattribute__(self,name);

    def __repr__(self):
        cls = self.__class__
        object.__setattr__(self,"__class__",rdma.path.IBPath);
        cls._unpack_rcv(self);
        return rdma.path.IBPath.__repr__(self);
    def __str__(self):
        cls = self.__class__
        object.__setattr__(self,"__class__",rdma.path.IBPath);
        cls._unpack_rcv(self);
        return rdma.path.IBPath.__repr__(self);

def get_mad_path(mad,ep_addr,**kwargs):
    """Query the SA and return a path for *ep_addr*.

    This is a simplified query function to return MAD paths from the end port
    associated with *mad* to the destination *ep_addr*.  If *ep_addr* is a
    string then :func:`from_string` is called automatically, otherwise
    :func:`rdma.IBA.conv_ep_addr` is used. Thus this will accept a destination
    address string, an integer (DLID), :class:`~rdma.IBA.GID` (DGID) and
    :class:`~rdma.IBA.GUID` (DGID).

    This returns a single reversible path.

    :raises ValueError: If dest is not appropriate.
    :raises rdma.path.SAPathNotFoundError: If *ep_addr* was not found at the SA.
    :raises rdma.MADError: If the RPC failed in some way."""
    ty = type(ep_addr);
    if ty == str or ty == unicode:
        path = from_string(ep_addr,require_ep=mad.end_port);
        for k,v in kwargs.iteritems():
            setattr(path,k,v);
    else:
        ep_addr = IBA.conv_ep_addr(ep_addr);
        if isinstance(ep_addr,IBA.GID):
            path = IBPath(mad.end_port,DGID=ep_addr,**kwargs);
        else:
            path = IBPath(mad.end_port,DLID=ep_addr,**kwargs);

    return resolve_path(mad,path,True);

def resolve_path(mad,path,reversible=False,properties=None):
    """Resolve *path* to a full path for use with a QP. *path* must have at
    least a DGID or DLID set.

    *properties* is a dictionary of additional PR fields to set in the query.

    FUTURE: This routine may populate path with up to 3 full path records, one
    for GMPs, one for the forward direction and one for the return direction.
    If the path is being used for UD then it should probably set the
    *reversible* argument to True.

    :raises rdma.path.SAPathNotFoundError: If *ep_addr* was not found at the SA.
    :raises rdma.MADError: If the RPC failed in some way."""

    if path.end_port is None:
        path.end_port = mad.end_port;

    q = IBA.ComponentMask(IBA.SAPathRecord());
    if reversible:
        q.reversible = True;
    # FIXME: want to remove this line ...
    q.reversible = True;
    if path.SGID is not None:
        q.SGID = path.SGID;
    else:
        q.SGID = mad.end_port.default_gid;

    if path.DGID is not None:
        q.DGID = path.DGID;
    else:
        q.DLID = path.DLID;

    if properties:
        for k,v in properties.iteritems():
            setattr(q,k,v);

    try:
        rep = mad.SubnAdmGet(q);
    except rdma.MADClassError as err:
        if err.code == IBA.MAD_STATUS_SA_NO_RECORDS:
            raise SAPathNotFoundError("Failed getting path record for path %r."%(path),
                                      err);
        err.message("Failed getting path record for path %r."%(path));
        raise
    except rdma.MADError as err:
        err.message("Failed getting path record for path %r."%(path));
        raise

    path.DGID = rep.DGID;
    path.SGID = rep.SGID;
    path.DLID = rep.DLID;
    path.SLID = rep.SLID;
    path.flow_label = rep.flowLabel;
    path.hop_limit = rep.hopLimit;
    path.traffic_class = rep.TClass;
    path.pkey = rep.PKey;
    path.SL = rep.SL;
    path.MTU = rep.MTU;
    path.rate = rep.rate;
    path.has_grh = rep.hopLimit != 0;
    path.packet_life_time = rep.packetLifeTime;
    return path;

def fill_path(qp,path,max_rd_atomic=255):
    """Fill in fields in path assuming *path* will be used with a QP. The
    filled fields are used to establish the QP parameters.

    If *max_rd_atomic* is set then that at most that many responder resources
    for RDMA READ and ATOMICs will be provisioned.  Since HCAs have limited
    responder resources this value should always be limited if possible. If
    RDMA READ and ATOMICs will not be used then it should be set to 0. Otherwise
    at least set to the sendq depth."""
    path.sqpn = qp.qp_num;
    devinfo = qp.ctx.query_device();
    path.sack_resp_time = devinfo.local_ca_ack_delay;

    # Maximum number of RD atomics the local HCA can issue
    path.srdatomic = min(path.srdatomic,devinfo.max_qp_init_rd_atom,max_rd_atomic);
    # Maximum number of RD atomics responder resources the HCA can allocate
    path.drdatomic = min(path.drdatomic,devinfo.max_qp_rd_atom,max_rd_atomic);
    if path.sqpsn == 0:
        path.sqpsn = int(os.urandom(3).encode("hex"),16);
    if path.dqpsn == 0:
        path.dqpsn = int(os.urandom(3).encode("hex"),16);

def from_spec_string(s):
    """Construct a *Path* (or derived) instance from it's `repr` string.

    This parser is safe to use with untrusted data.

    :raises ValueError: If the string can not be parsed."""
    import re,itertools;
    m = re.match("^(.+?)\(\s*?(.*?)\s*?\)$",s);
    if m is None:
        raise ValueError("Invalid path specification %r"%(s,));
    m = m.groups();
    cls = getattr(sys.modules[__name__],m[0],None)
    if cls is None or not issubclass(cls,Path):
        raise ValueError("Invalid path specification %r, bad path type"%(s,));

    kwargs = dict((t[0].strip(), t[2].strip())
                  for t in (I.partition('=')
                            for I in m[1].split(',')));

    if len(kwargs) < 1:
        raise ValueError("Invalid path specification %r"%(s,));
    for k,v in kwargs.iteritems():
        if v == '':
            raise ValueError("Invalid path specification %r"%(s,));
        if not hasattr(cls,k):
            raise ValueError("Path attribute %r is not known"%(k,));

        if v.startswith("GID("):
            v = v[4:-1];
            if v[0] == '"' or v[0] == "'":
                v = v[1:-1];
            kwargs[k] = IBA.GID(v);
        elif k.find("GID") != -1:
            kwargs[k] = IBA.GID(v);
        elif k == "drPath":
            # Using : because I am too lazy to fix the splitter to respect quotes.
            dr = v.split(":");
            if len(dr) == 1:
                raise ValueError("Invalid DR path specification %r"%(v,));
            if dr[-1] == '':
                dr = [int(I) for I in dr[:-1]];
            else:
                dr = [int(I) for I in dr];
            for I in dr:
                if I >= 255:
                    raise ValueError("Invalid DR path specification %r"%(v,));
                if len(dr) == 0:
                    raise ValueError("Invalid DR path specification %r"%(s,));
                if dr[0] != 0:
                    raise ValueError("Invalid DR path specification %r"%(s,));
            kwargs[k] = bytes("").join("%c"%(I) for I in dr);
        elif k == "end_port":
            if v[0] == '"' or v[0] == "'":
                v = v[1:-1];
            try:
                if v == "None":
                    kwargs[k] = None;
                else:
                    kwargs[k] = rdma.get_end_port(v);
            except rdma.RDMAError, e:
                raise ValueError("Could not find %r: %s"%(v,e));
        else:
            try:
                kwargs[k] = int(v,0);
            except ValueError:
                raise ValueError("%r=%r is not a valid integer"%(k,v));
    if "end_port" not in kwargs:
        kwargs["end_port"] = None;
    return cls(**kwargs);

def _check_ep(ep,require_dev=None,require_ep=None):
    if require_dev is not None and ep.parent != require_dev:
        raise ValueError("Path requires device %s, got %s"%(require_dev,ep))
    if require_ep is not None and ep != require_ep:
        raise ValueError("Path requires end port %s, got %s"%(require_ep,ep))

def from_string(s,default_end_port=None,require_dev=None,require_ep=None):
    """Convert the string *s* into an instance of :class:`Path` or
    derived.

    Supported formats for *s* are:
      =========== ============================ ========================
      Format      Example                      Creates
      =========== ============================ ========================
      Port GID    fe80::2:c903:0:1491          IBPath.DGID = s
      Scope'd GID fe80::2:c903:0:1491%mlx4_0/1 IBPath.DGID = s
      Port GUID   0002:c903:0000:1491          IBPath.DGID = fe80:: + s
      LID         12                           IBPath.DLID = 12
      Hex LID     0xc                          IBPath.DLID = 12
      DR Path     0,1,                         IBDRPath.drPath = '\\\\0\\\\1'
      Path Spec   IBPath(DLID=2,SL=2)          IBPath.{DLID=2,SL=2}
      =========== ============================ ========================

    If the format unambiguously specifies an end port, eg due to a provided
    scope or by specifying the subnet prefix then the result will have `end_port`
    set appropriately. Otherwise `end_port` is set to `default_end_port`.

    *require_dev* and *require_ep* will restrict the lookup to returning
    a path for those conditions. If a scoped address is given that doesn't
    match then :exc:`ValueError` is raised. These options should be used when
    a path is being parsed for use with an existing bound resource (eg
    a :class:`rdma.ibverbs.Context` or :class:`rdma.ibverbs.`)

    FUTURE: This may return paths other than IB for other technologies.

    :raises ValueError: If the string can not be parsed."""
    if require_ep is not None:
        default_end_port = require_ep;

    if s.find("(") != -1:
        ret = from_spec_string(s);
        if ret.end_port is None:
            ret.end_port = default_end_port;
        else:
            _check_ep(ret.end_port,require_dev,require_ep);
        return ret;

    dr = s.split(",");
    if len(dr) != 1:
        if dr[-1] == '':
            dr = [int(I) for I in dr[:-1]];
        else:
            dr = [int(I) for I in dr];
        for I in dr:
            if I >= 255:
                raise ValueError("Invalid DR path specification %r"%(s,));
        if len(dr) == 0:
            raise ValueError("Invalid DR path specification %r"%(s,));
        if dr[0] != 0:
            raise ValueError("Invalid DR path specification %r"%(s,));
        drPath = bytes("").join("%c"%(I) for I in dr);
        return IBDRPath(default_end_port,drPath=drPath);

    a = s.split('%');
    if len(a) == 2:
        DGID = IBA.GID(a[0])
        try:
            end_port = rdma.get_end_port(a[1]);
            _check_ep(end_port,require_dev,require_ep);
        except rdma.RDMAError, e:
            raise ValueError("Could not find %r: %s"%(a[1],e));
        return IBPath(end_port,DGID=DGID);

    res = rdma.IBA.conv_ep_addr(s);
    if isinstance(res,IBA.GID):
        # Search all the GIDs for one that matches the prefix, someday we
        # should have a host routing table for this lookup...
        prefix = int(res) >> 64;
        if prefix != IBA.GID_DEFAULT_PREFIX and require_ep is None:
            for I in rdma.get_devices():
                if I != require_dev and require_dev is not None:
                    continue;
                for J in I.end_ports:
                    for G in J.gids:
                        if int(G) >> 64 == prefix:
                            _check_ep(J,require_dev,require_ep);
                            return IBPath(J,DGID=res);
        return IBPath(default_end_port,DGID=res);
    if isinstance(res,int) or isinstance(res,long):
        return IBPath(default_end_port,DLID=res);
    raise ValueError("Invalid destination %r"%(s,))
