#!/usr/bin/python
import copy;
import rdma;
import rdma.IBA as IBA;

class Path(object):
    """Describe an RDMA path. This also serves to cache the path for cases
    that need it in an AH or other format. Paths should be considered final,
    once construction is finished their content must never change. This is to
    prevent cached data in the path from becoming stale."""

    #: Number of times a MAD will be resent, or the value of retry_cnt for a RC QP.
    retries = 0;

    def __init__(self,end_port,**kwargs):
        """*end_port* is the :class:`rdma.devices.EndPort` this path is
        associated with. *kwargs* is applied to set attributes of the
        instance during initialization."""
        self.end_port = end_port;
        for k,v in kwargs.iteritems():
            setattr(self,k,v);

    def copy(self,**kwargs):
        """Return a new path object that is a copy of this one. This takes
        care of the internal caching mechanism.  *kwargs* is applied to set
        attributes of the instance after copying."""
        ret = copy.copy(self);
        ret.drop_cache();
        for k,v in kwargs.iteritems():
            setattr(ret,k,v);
        return ret;

    def drop_cache(self):
        """Release any cached information."""
        for I in self.__dict__.keys():
            if I.startswith("_cached"):
                self.__delattr__(I);

    def __repr__(self):
        cls = self.__class__;
        keys = ("%s=%r"%(k,v) for k,v in self.__dict__.iteritems()
                if k[0] != "_" and k != "end_port" and getattr(cls,k,None) != v);
        return "%s(end_port=%r, %s)"%(cls.__name__,str(self.end_port),
                                      ", ".join(keys));

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
    #: Used to compute :attr:`packet_lifetime`
    resp_time = 20; # See C13-13.1.1

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

    #: Method specific - override the *agent_id* for :class:`rdma.umad.UMAD`
    umad_agent_id = None;

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

    def reverse(self):
        """Reverse this path in-place according to IBA 13.5.4."""
        self.DLID,self.SLID = self.SLID,self.DLID;
        self.dqpn ,self.sqpn = self.sqpn,self.dqpn;
        self.DGID,self.SGID = self.SGID,self.DGID;
        if self.has_grh:
            self.hop_limit = 0xff;
        self.drop_cache();

    @property
    def SGID_index(self):
        """Cache and return the index of the SGID for the associated
        :class:`~rdma.devices.EndPort`. Assignment updates the :attr:`SGID`
        value."""
        try:
            return self._cached_SGID_index;
        except AttributeError:
            self._cached_SGID_index = self.end_port.gids.index(self.SGID);
            return self._cached_SGID_index;
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
            self._cached_pkey_index = self.end_port.pkeys.index(self.pkey);
            return self._cached_pkey_index;
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
    def packet_life_time(self):
        """The packet lifetime value for this path. The lifetime value for the
        path is the expected uni-directional transit time.  If a value has not
        been provided then the port's
        :attr:`rdma.devices.EndPort.subnet_timeout` is used."""
        try:
            return Path.__getattr__(self,"packet_life_time");
        except AttributeError:
            return self.end_port.subnet_timeout;
    @packet_life_time.setter
    def packet_life_time(self,value):
        self.__dict__["packet_life_time"] = value;
        return value;

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

    def __str__(self):
        if self.has_grh:
            res = "%s %r -> %s %u TC=%r FL=%r HL=%r"%(
                self.SGID,self.SLID,self.DGID,self.DLID,self.traffic_class,
                self.flow_label,self.hop_limit);
        else:
            res = "%r -> %r"%(self.SLID,self.DLID);
        return "Path %s SL=%r PKey=%r DQPN=%r"%(
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

def get_mad_path(mad,ep_addr):
    """Query the SA and return a path for *ep_addr* (:func:rdma.IBA.conv_ep_addr is
    called automatically).

    This is a simplified query function to return MAD paths from the end port
    associated with *mad* to the destination *ep_addr*.

    This returns a single reversible path.

    :raises ValueError: If dest is not appropriate.
    :raises rdma.path.SAPathNotFoundError: If *ep_addr* was not found at the SA.
    :raises rdma.MADError: If the RPC failed in some way."""
    ep_addr = IBA.conv_ep_addr(ep_addr);

    q = IBA.ComponentMask(IBA.SAPathRecord());
    q.reversible = True;
    q.SGID = mad.end_port.gids[0];
    if isinstance(ep_addr,IBA.GID):
        q.DGID = ep_addr;
    else:
        q.DLID = ep_addr;

    try:
        rep = mad.SubnAdmGet(q);
    except rdma.MADClassError as err:
        if err.code == IBA.MAD_STATUS_SA_NO_RECORDS:
            raise SAPathNotFoundError("Failed getting MAD path record for end port %r."%(ep_addr),
                                      err);
        err.message("Failed getting MAD path record for end port %r."%(ep_addr));
        raise
    except rdma.MADError as err:
        err.message("Failed getting MAD path record for end port %r."%(ep_addr));
        raise

    return IBPath(mad.end_port,
                  DGID=rep.DGID,
                  SGID=rep.SGID,
                  DLID=rep.DLID,
                  SLID=rep.SLID,
                  flow_label=rep.flowLabel,
                  hop_limit=rep.hopLimit,
                  traffic_class=rep.TClass,
                  pkey=rep.PKey,
                  SL=rep.SL,
                  MTU=rep.MTU,
                  rate=rep.rate,
                  has_grh=rep.hopLimit != 0,
                  packet_life_time=rep.packetLifeTime);
