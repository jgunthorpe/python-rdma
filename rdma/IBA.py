# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

# NOTE: The docstrings for this module are specially processed in the
# documentation take some care when editing.

import socket,sys;
import rdma.binstruct;

#: Node Type Constants
# see NodeInfo.nodeType
NODE_CA = 1;
NODE_SWITCH = 2;
NODE_ROUTER = 3;

#: General Constants
MAX_PORTS = 254; # maximum number of physical ports on a device
INVALID_PORT = 255;
MAX_PKEYS = 65536;
MAX_GUIDS = 256;
MAX_PKT_WORDS = 4222/4;

#: LID Constants
LID_RESERVED = 0; # for uninitialized ports
LID_MULTICAST = 0xC000; # first multicast LID
LID_PERMISSIVE = 0xFFFF;
LID_COUNT_UNICAST = 0xC000;
LID_COUNT_MULTICAST = (0xFFFE - 0xC000) + 1;

#: Partition Key Constants
PKEY_DEFAULT = 0xFFFF;
PKEY_PARTIAL_DEFAULT = 0x7FFF;
PKEY_MEMBERSHIP_BIT = (1<<15);
PKEY_INVALID = 0;

#: Well known QKEY Constants
IB_DEFAULT_QP0_QKEY = 0
IB_DEFAULT_QP1_QKEY = 0x80010000

#: LRH LNH Header bits
LNH_GRH = 1<<0;
LNH_IBA = 1<<1;

#: GID Constants
GID_DEFAULT_PREFIX = 0xFE80 << 48;

#: PortInfo MTU Constants
MTU_256 = 1;
MTU_512 = 2;
MTU_1024 = 3;
MTU_2048 = 4;
MTU_4096 = 5;

#: PortInfo Link Width Constants
LINK_WIDTH_1x = 0x1;
LINK_WIDTH_4x = 0x2;
LINK_WIDTH_8x = 0x4;
LINK_WIDTH_12x = 0x8;

#: PortInfo Link Speed Constants
LINK_SPEED_2Gb5 = 0x1;
LINK_SPEED_5Gb0 = 0x2;
LINK_SPEED_10Gb0 = 0x4;

#: PortInfo Link Speed Extended Constants
LINK_SPEED_EXT_14Gb0 = 0x1;
LINK_SPEED_EXT_25Gb7 = 0x2;

#: PathRecord rate constants
PR_RATE_2Gb5 = 2;
PR_RATE_10Gb0 = 3;
PR_RATE_30Gb0 = 4;
PR_RATE_5Gb0 = 5;
PR_RATE_20Gb0 = 6;
PR_RATE_40Gb0 = 7;
PR_RATE_60Gb0 = 8;
PR_RATE_80Gb0 = 9;
PR_RATE_120Gb0 = 10;
PR_RATE_14Gb0 = 11;
PR_RATE_56Gb0 = 12;
PR_RATE_112Gb0 = 13;
PR_RATE_168Gb0 = 14;
PR_RATE_25Gb0 = 15;
PR_RATE_100Gb0 = 16;
PR_RATE_200Gb0 = 17;
PR_RATE_300Gb0 = 18;

#: PortInfo Port State Constants
PORT_STATE_DOWN = 1;
PORT_STATE_INIT = 2;
PORT_STATE_ARMED = 3;
PORT_STATE_ACTIVE = 4;

#: PortInfo Physical Port State Constants
PHYS_PORT_STATE_SLEEP = 1;
PHYS_PORT_STATE_POLLING = 2;
PHYS_PORT_STATE_DISABLED = 3;
PHYS_PORT_STATE_CFG_TRAIN = 4;
PHYS_PORT_STATE_LINK_UP = 5;
PHYS_PORT_STATE_LINK_ERR_RECOVERY = 6;
PHYS_PORT_STATE_PHY_TEST = 7;

#: MAD RPC Constants
MAD_METHOD_GET = 0x01;
MAD_METHOD_SET = 0x02;
MAD_METHOD_SEND = 0x03;
MAD_METHOD_GET_RESP = 0x81;
MAD_METHOD_TRAP = 0x05;
MAD_METHOD_TRAP_REPRESS = 0x07;
MAD_METHOD_GET_TABLE = 0x12;
MAD_METHOD_GET_TRACE_TABLE = 0x13;
MAD_METHOD_GET_MULTI = 0x14;
MAD_METHOD_DELETE = 0x15;
MAD_METHOD_RESPONSE = 0x80;

MAD_BASE_VERSION = 1;

MAD_NOTICE_FATAL = 0;
MAD_NOTICE_URGENT = 1;
MAD_NOTICE_SECURITY = 2;
MAD_NOTICE_SM = 3;
MAD_NOTICE_INFO = 4;

#: MAD Response Status Constants
MAD_STATUS_BUSY = 1<<0;
MAD_STATUS_REDIRECT = 1<<1;
MAD_STATUS_BAD_VERSION = 1<<2;
MAD_STATUS_UNSUP_METHOD = 2<<2;
MAD_STATUS_UNSUP_METHOD_ATTR_COMBO = 3<<2;
MAD_STATUS_INVALID_ATTR_OR_MODIFIER = 7<<2;
MAD_STATUS_DIRECTED_RESPONSE = 1<<15;

#: SUBNET_ADMIN Class Specific Status Codes
MAD_STATUS_SA_NO_RESOURCE = 1;
MAD_STATUS_SA_REQ_INVALID = 2;
MAD_STATUS_SA_NO_RECORDS = 3;
MAD_STATUS_SA_TOO_MANY_RECORDS = 4;
MAD_STATUS_SA_INVALID_GID = 5;
MAD_STATUS_SA_INSUFFICIENT_COMPONENTS = 6;
MAD_STATUS_SA_DENIED = 7;

MAD_STATUS_CLASS_SHIFT = 8;
MAD_STATUS_CLASS_MASK = 0x7F;

#: MAD Class Constants
MAD_SUBNET = 0x01;
MAD_SUBNET_DIRECTED = 0x81;
MAD_SUBNET_ADMIN = 0x3;
MAD_COMMUNICATIONS = 0x7;
MAD_PERFORMANCE = 0x4;
MAD_DEVICE = 0x6;
MAD_SNMP = 0x8;

#: RMPP Constants
RMPP_ACTIVE = (1<<0);
RMPP_FIRST = (1<<1);
RMPP_LAST = (1<<2);

#: ClassPortInfo capabilityMask Constants
generatesTraps = 1<<0;
implementsNotice = 1<<1;

#: PMA ClassPortInfo capabilityMask Constants
allPortSelect = 1<<8;
portCountersXmitWaitSupported = 1<<12;

#: PortInfo capabilityMask Constants
isSM = 1<<1;
isNoticeSupported = 1<<2;
isTrapSupported = 1<<3;
# isOptionalIPDSupported (IBA assumes capability when applicable)
isAutomaticMigrationSupported = 1<<5;
isSLMappingSupported = 1<<6;
isMKeyNVRAM = 1<<7;
isPKeyNVRAM = 1<<8;
isLEDInfoSupported = 1<<9;
isSMdisabled = 1<<10;
isSystemImageGUIDSupported = 1<<11;
isPKeySwitchExternalPortTrapSupported = 1<<12;
isExtendedSpeedsSupported = 1<<14;
isCommunicationManagementSupported = 1<<16;
isSNMPTunnelingSupported = 1<<17;
isReinitSupported = 1<<18;
isDeviceManagementSupported = 1<<19;
isVendorClassSupported = 1<<20;
isDRNoticeSupported = 1<<21;
isCapabilityMaskNoticeSupported = 1<<22;
isBootManagementSupported = 1<<23;
isLinkRoundTripLatencySupported = 1<<24;
isClientReregistrationSupported = 1<<25;
isOtherLocalChangesNoticeSupported = 1<<26;
isLinkSpeedWidthPairsTableSupported = 1<<27;

def conv_lid(s,multicast=False):
    """Converts the string *s* into an integer assuming it is a LID.
    If *multicast* is `False` then the LID must be a valid unicast LID.
    If *multicast* is `True` then the LID must be a valid multicast LID.
    If *multicast* is `None` then any 16 bit value is accepted.

    :raises ValueError: If the string can not be parsed."""
    lid = int(s,0);
    if multicast is None:
        return lid;
    if multicast == True:
        if lid < LID_MULTICAST or lid == LID_PERMISSIVE:
            raise ValueError("%r is not a multicast LID"%(s));
    else:
        if lid >= LID_MULTICAST or lid == LID_RESERVED:
            raise ValueError("%r is not a unicast LID"%(s));
    return lid;

def lid_lmc_range(lid,lmc):
    """Return all the LIDs described by *lid* and *lmc*. Similar to `range`"""
    lmc = 1 << lmc;
    lid = lid & (~(lmc-1))
    return range(lid,lid + lmc);

def to_timer(sec):
    """Take a timeout value in float seconds and convert it into the IBA format
    that satisfies `sec <= 4.096 us * 2**ret`"""
    import math;
    v = sec/4.096E-6;
    return math.ceil(math.log(v,2));

class GUID(bytes):
    """Stores a GUID in internal format. In string format a GUID is formatted
    as ``0002:c903:0000:1491``. Externally the class looks like a string
    that formats to the GUID. :meth:`pack_into` is used to store the GUID in
    network format. Instances are immutable and can be hashed."""
    def __init__(self,s=None,raw=False):
        """Convert from a string to our GUID representation. *s* is the input
        string and if *raw* is True then *s* must be a length 8 :class:`bytes`.

        If *s* is `None` then the :attr:`~rdma.IBA.ZERO_GUID` is
        instantiated. *s* can also be an integer.

        :raises ValueError: If the string can not be parsed."""
        pass
    def __new__(self,s=None,raw=False):
        if s is None:
            return ZERO_GUID;
        if isinstance(s,GUID):
            return s;
        if isinstance(s,int) or isinstance(s,long):
            s = ("%016x"%(s)).decode("hex");
            raw = True;
        if raw:
            assert(len(s) == 8);
            return bytes.__new__(self,s);

        v = ''.join(I.zfill(4) for I in s.strip().split(':'));
        if len(v) != 16:
            raise ValueError("%r is not a valid GUID"%(s));
        try:
            return bytes.__new__(self,v.decode("hex"));
        except TypeError:
            raise ValueError("%r is not a valid GUID"%(s));

    def pack_into(self,buf,offset=0):
        """Pack the value into a byte array.""";
        buf[offset:offset+8] = bytes.__str__(self);

    def __str__(self):
        """Return a printable string of the GUID."""
        tmp = self.encode("hex");
        return "%s:%s:%s:%s"%(tmp[0:4],tmp[4:8],tmp[8:12],tmp[12:16]);
    def __repr__(self):
        return "GUID('%s')"%(self.__str__());
    def __int__(self):
        return int(bytes.__str__(self).encode("hex"),16);

    def __reduce__(self):
        return (GUID,(bytes.__str__(self),True));

#: All zeros GUID value.
ZERO_GUID = GUID('\x00\x00\x00\x00\x00\x00\x00\x00',raw=True);

class GID(bytes):
    """Stores a GID in internal format. In string format a GID is formatted
    like an IPv6 addres eg ``fe80::2:c903:0:1491``. Externally the class looks
    like a string that formats to the GID. :meth:`pack_into` is used to store
    the GID in network format. Instances are immutable and can be hashed."""
    def __init__(self,s=None,raw=False,prefix=None,guid=None):
        """Convert from a string to our GID representation. *s* is the input
        string and if *raw* is `True` then *s* must be a length 16 :class:`bytes`.

        If *s* is `None` then the :attr:`~rdma.IBA.ZERO_GID` is
        instantiated. Invoking as ``GID(prefix=PREFIX,guid=GUID)`` will
        construct a GID by concatenating the *PREFIX* to *GUID*. *GUID* should
        be a :class:`rdma.IBA.GUID` while *PREFIX* can be 8 bytes, an integer
        or a :class:`rdma.IBA.GID`.

        :raises ValueError: If the string can not be parsed."""
        pass
    def __new__(self,s=None,raw=False,prefix=None,guid=None):
        if s is None:
            if prefix is None:
                return ZERO_GID;
            if isinstance(prefix,GID):
                prefix = bytes.__str__(prefix)[:8];
            elif isinstance(prefix,GUID):
                prefix = bytes.__str__(prefix);
            elif isinstance(prefix,int) or isinstance(prefix,long):
                prefix = ("%016x"%(prefix)).decode("hex");
            return bytes.__new__(self,prefix + bytes.__str__(guid))

        if isinstance(s,GID):
            return s;
        if raw:
            assert(len(s) == 16);
            return bytes.__new__(self,s);
        try:
            return bytes.__new__(self,socket.inet_pton(socket.AF_INET6,s.strip()));
        except:
            raise ValueError("%r is not a valid GID"%(s));

    def pack_into(self,buf,offset=0):
        """Pack the value into a byte array.""";
        buf[offset:offset+16] = bytes.__str__(self);

    def __str__(self):
        """Return a printable string of the GID."""
        return socket.inet_ntop(socket.AF_INET6,bytes.__str__(self));
    def __repr__(self):
        return "GID('%s')"%(self.__str__());
    def guid(self):
        """Return the GUID portion of the GID."""
        return GUID(bytes.__getslice__(self,8,16),raw=True);
    def prefix(self):
        """Return the prefix portion of the GID."""
        return GUID(bytes.__getslice__(self,0,8),raw=True);
    def __int__(self):
        return int(bytes.__str__(self).encode("hex"),16);

    def __reduce__(self):
        return (GID,(bytes.__str__(self),True));


#: All zeros GID value.
ZERO_GID = GID('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',raw=True);

def conv_ep_addr(s):
    """Convert the string *s* into a end port address. *s* can be a
    GID, port GUID or LID. The result of this function is a
    :class:`GID` or :class:`int`.

    :raises ValueError: If the string can not be parsed."""
    # Called on our own output.
    if isinstance(s,GID) or isinstance(s,int) or isinstance(s,long):
        return s;

    try:
        return GID(s);
    except ValueError:
        pass;
    try:
        guid = GUID(s);
        return GID(prefix=GID_DEFAULT_PREFIX,guid=guid);
    except ValueError:
        pass;
    try:
        return conv_lid(s);
    except ValueError:
        pass;
    raise ValueError("%r is not a valid end port address (GID, port GUID or LID)"%(s))

class ComponentMask(object):
    """This is a wrapper class for managing IBA structures with a component
    mask. Attribute access is overridden and tracked by mapping the attribute
    name to the component mask bit index to build up a component mask value as
    the class is used."""

    #: The computed component_mask
    component_mask = 0

    def __init__(self,obj,mask=0):
        """*obj* is wrappered"""
        object.__setattr__(self,"component_mask",mask);
        object.__setattr__(self,"_obj",obj);

    @property
    def payload(self):
        """The original object that is wrappered."""
        return self._obj;

    def touch(self,name):
        """Include the component mask value *name* in the calculation.
        Normally this happens automatically as attributes are accessed.

        :raises ValueError: If *name* is not a valid component name"""
        bit = self._obj.COMPONENT_MASK[name];
        object.__setattr__(self,"component_mask",
                           self.component_mask | (1<<bit));

    def unmask(self,name):
        """Exclude the component mask value *name* in the calculation.

        :raises ValueError: If *name* is not a valid component name"""
        bit = self._obj.COMPONENT_MASK[name];
        object.__setattr__(self,"component_mask",
                           self.component_mask & (0xFFFFFFFFFFFFFFFF ^ (1<<bit)));

    def _touch(self,name):
        bit = self._obj.COMPONENT_MASK.get(name);
        if bit is not None:
            object.__setattr__(self,"component_mask",
                               self.component_mask | (1<<bit));

    def __getattr__(self,name):
        res = getattr(self._obj,name);
        if isinstance(res,rdma.binstruct.BinStruct):
            return ComponentMask._Proxy(self,name,res);
        if isinstance(res,bytearray) or isinstance(res,list):
            # It is an array of some sort, just reading from those
            # flips the bit because I am lazy.
            self._touch(name);
        return res;

    def __setattr__(self,name,value):
        if name == 'component_mask':
            return object.__setattr__(self,name,value);
        self._touch(name);
        return setattr(self._obj,name,value);

    class _Proxy(object):
        def __init__(self,parent,name,obj):
            object.__setattr__(self,"_parent",parent);
            object.__setattr__(self,"_name",name);
            object.__setattr__(self,"_obj",obj);

        def __getattr__(self,name):
            res = getattr(self._obj,name);
            if isinstance(res,rdma.binstruct.BinStruct):
                return _Proxy(self._parent,"%s.%s"%(self._name,name),res);
            if isinstance(res,bytearray) or isinstance(res,list):
                # It is an array of some sort, just reading from those
                # flips the bit because I am lazy.
                self._parent._touch("%s.%s"%(self._name,name));
            return res;

        def __setattr__(self,name,value):
            self._parent._touch("%s.%s"%(self._name,name));
            return setattr(self._obj,name,value);

def const_str(prefix,value,with_int=False,me=sys.modules[__name__]):
    """Generalized constant integer to string that uses introspection
    to figure it out."""
    for k,v in me.__dict__.iteritems():
        if k.startswith(prefix):
            try:
                if value == v:
                    if with_int:
                        return "%s(%u)"%(k,value);
                    else:
                        return k;
            except rdma.RDMAError:
                pass;
    if with_int:
        return "%s??(%u)"%(prefix,value)
    return "%s?%u"%(prefix,value)

def get_fmt_payload(class_id,class_version,attribute_id):
    """Find the MAD format and MAD payload classes for class_id and
    attribute_id. *class_version* is `(base_version << 8) | class_version`.
    See :meth:`rdma.madtransactor.MADTransactor.get_request_match_key`."""
    cls = CLASS_TO_STRUCT.get((class_id,class_version));
    if cls is None:
        return (None,None);
    attr = ATTR_TO_STRUCT.get((cls,attribute_id));
    if attr is None:
        return (cls,None);
    return (cls,attr);

from rdma.IBA_struct import *;
def _make_IBA_link():
    """We have a bit of a circular dependency here, make a IBA
    name inside the IBA_struct module so that it can see the
    stuff in this module when its code runs. Fugly, but I
    don't think you can do #include in python, which is what
    I really want.."""
    me = sys.modules[__name__];
    struct = sys.modules["rdma.IBA_struct"];
    setattr(struct,"IBA",me)
_make_IBA_link();
