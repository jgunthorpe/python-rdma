#!/usr/bin/python
'''Constants from the InfiniBand Architecture'''

from rdma.IBA_struct import *;

# see NodeInfo.nodeType
CA = 1;
SWITCH = 2;
ROUTER = 3;

MAX_PORTS = 254; # maximum number of physical ports on a device
INVALID_PORT = 255;
MAX_PKEYS = 65536;
MAX_GUIDS = 256;
MAX_PKT_WORDS = 4222/4;

MAD_BASE_VERSION = 1;

LID_RESERVED = 0; # for uninitialised ports
LID_MULTICAST = 0xC000; # first multicast LID
LID_PERMISSIVE = 0xFFFF;
LID_COUNT_UNICAST = 0xC000;
LID_COUNT_MULTICAST = 0xFFFE - 0xC000;

PKEY_DEFAULT = 0xFFFF;
PKEY_INVALID = 0;

LNH_GRH = 1<<0;
LNH_IBA = 1<<1;

GID_DEFAULT_PREFIX = 0xFE80 << 48;

MTU_256 = 1;
MTU_512 = 2;
MTU_1024 = 3;
MTU_2048 = 4;
MTU_4096 = 5;

LINK_WIDTH_1x = 0x1;
LINK_WIDTH_4x = 0x2;
LINK_WIDTH_8x = 0x4;
LINK_WIDTH_12x = 0x8;

LINK_SPEED_2Gb5 = 0x1;
LINK_SPEED_5Gb0 = 0x2;
LINK_SPEED_10Gb0 = 0x4;

PORT_STATE_DOWN = 1;
PORT_STATE_INIT = 2;
PORT_STATE_ARMED = 3;
PORT_STATE_ACTIVE = 4;

PHYS_PORT_STATE_SLEEP = 1;
PHYS_PORT_STATE_POLLING = 2;
PHYS_PORT_STATE_DISABLED = 3;
PHYS_PORT_STATE_CFG_TRAIN = 4;
PHYS_PORT_STATE_LINK_UP = 5;
PHYS_PORT_STATE_LINK_ERR_RECOVERY = 6;
PHYS_PORT_STATE_PHY_TEST = 7;

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

MAD_NOTICE_FATAL = 0;
MAD_NOTICE_URGENT = 1;
MAD_NOTICE_SECURITY = 2;
MAD_NOTICE_SM = 3;
MAD_NOTICE_INFO = 4;

MAD_STATUS_BUSY = 1<<0;
MAD_STATUS_REDIRECT = 1<<1;
MAD_STATUS_BAD_VERSION = 1<<2;
MAD_STATUS_UNSUP_METHOD = 2<<2;
MAD_STATUS_UNSUP_METHOD_ATTR_COMBO = 3<<2;
MAD_STATUS_INVALID_ATTR_OR_MODIFIER = 7<<2;
MAD_STATUS_DIRECTED_RESPONSE = 1<<15;

# MAD Classes. Try not to use, the structs have these embedded
MAD_SUBNET = 0x01;
MAD_SUBNET_DIRECTED = 0x81;
MAD_SUBNET_ADMIN = 0x3;
MAD_COMMUNICATIONS = 0x7;
MAD_PERFORMANCE = 0x4;
MAD_DEVICE = 0x6;
MAD_SNMP = 0x8;

IB_DEFAULT_QP0_QKEY = 0
IB_DEFAULT_QP1_QKEY = 0x80010000

# ClassPortInfo.capabilityMask
generatesTraps = 1<<0;
implementsNotice = 1<<1;
allPortSelect = 1<<8; # Performance Management

# PortInfo.capabilityMask
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
