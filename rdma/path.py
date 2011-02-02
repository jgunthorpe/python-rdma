#!/usr/bin/python
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

    def drop_cache(self):
        """Release any cached information."""
        for I in self.__dict__.keys():
            if I.startswith("_cached"):
                self.__delattr__(I);

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

    #: Method specific - override the *agent_id* for :class:`rdma.umad.UMAD`
    umad_agent_id = None;

    # These are only present if has_grh is True
    #: Holds :attr:`rdma.IBA.HdrGRH.SGID`
    SGID = None;
    #: Holds :attr:`rdma.IBA.HdrGRH.DGID`
    DGID = None;
    #: Holds :attr:`rdma.IBA.HdrGRH.hopLmt`
    hop_limit = 255;
    #: Holds :attr:`rdma.IBA.HdrGRH.TClass`
    traffic_class = 0;
    #: Holds :attr:`rdma.IBA.HdrGRH.flowLabel`
    flow_label = 0;

    def reverse(self):
        """Reverse this path in-place according to IBA 13.5.4."""
        self.DLID,self.SLID = self.SLID,self.DLID;
        self.dqpn ,self.sqpn = self.sqpn,self.dqpn;
        if self.has_grh:
            self.DGID,self.SGID = self.SGID,self.DGID;
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
        been provided the the port's
        :attr:`rdma.devices.EndPort.subnet_timeout` is used."""
        try:
            return self._packet_life_time;
        except AttributeError:
            return self.end_port.subnet_timeout;
    @packet_life_time.setter
    def packet_life_time(self,value):
        self._packet_life_time = value;
        return self._packet_life_time;

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

class IBDRPath(IBPath):
    """Describe a directed route path in an IB network using a VL15 QP0 packet,
    a LRH and :class:`rdma.IBA.SMPFormatDirected` MADs."""
    #: Holds :attr:`rdma.IBA.SMPFormatDirected.drSLID`
    drSLID = 0xFFFF;
    #: Holds :attr:`rdma.IBA.SMPFormatDirected.drDLID`
    drDLID = 0xFFFF;
    #: Holds :attr:`rdma.IBA.SMPFormatDirected.drPath`. len(:attr:`drPath`) is used to set *hopCount*.
    drPath = None;

    def __init__(self,end_port,**kwargs):
        """*end_port* is the :class:`rdma.devices.EndPort` this path is
        associated with. *kwargs* is applied to set attributes of the
        instance during initialization."""
        self.DLID = 0xFFFF;
        self.SLID = 0; # FIXME
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
