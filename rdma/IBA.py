#!/usr/bin/python

# NOTE: The docstrings for this module are specially processed in the
# documentation take some care when editing.

import socket,sys;

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
LID_RESERVED = 0; # for uninitialised ports
LID_MULTICAST = 0xC000; # first multicast LID
LID_PERMISSIVE = 0xFFFF;
LID_COUNT_UNICAST = 0xC000;
LID_COUNT_MULTICAST = 0xFFFE - 0xC000;

#: Partition Key Constants
PKEY_DEFAULT = 0xFFFF;
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

#: Internal MAD Status Constants
MAD_XSTATUS_INVALID_REP_SIZE = 1<<16;

def mad_status_to_str(status):
    """Decode a MAD status into a string."""
    if status == MAD_XSTATUS_INVALID_REP_SIZE:
        return "Invalid reply size";
    res = "";
    if status & MAD_STATUS_BUSY:
        res = res + "BUSY ";
    if status & MAD_STATUS_REDIRECT:
        res = res + "REDIECT ";
    code = (status >> 2) & 7;
    if code == 0:
        return res + "Ok";
    if code == 1:
        return res + "Bad version";
    if code == 2:
        return res + "Unsupported method";
    if code == 3:
        return res + "Unsupported method+attr";
    if code == 7:
        return res + "Invalid attr or modifier";
    return res + "??";

#: MAD Class Constants
MAD_SUBNET = 0x01;
MAD_SUBNET_DIRECTED = 0x81;
MAD_SUBNET_ADMIN = 0x3;
MAD_COMMUNICATIONS = 0x7;
MAD_PERFORMANCE = 0x4;
MAD_DEVICE = 0x6;
MAD_SNMP = 0x8;

#: ClassPortInfo capabilityMask Constants
generatesTraps = 1<<0;
implementsNotice = 1<<1;
allPortSelect = 1<<8; # Performance Management

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
            return bytes.__new__(self,bytes.__str__(s));
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
            return bytes.__new__(self,bytes.__str__(s));
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
ZERO_GID = bytes('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00');

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
