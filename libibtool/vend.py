import libibtool.vendstruct,rdma.binstruct,struct
class MlxGeneralInfo(rdma.binstruct.BinStruct):
    '''None (section None)'''
    __slots__ = ('reserved_0','hw_revision','device_id','reserved_96','uptime','reserved_320','fw_major','fw_minor','fw_sub_minor','fw_build_id','fw_month','fw_day','fw_year','reserved_416','fw_hour','fw_psid','fw_init_file_version','reserved_608','hw_major','hw_minor','hw_sub_minor','reserved_640');
    MAD_LENGTH = 108
    FORMAT = libibtool.vendstruct.MlxFormat
    MAD_ATTRIBUTE_ID = 0x17
    MAD_VENDGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('reserved_0',64,1), ('hw_revision',16,1), ('device_id',16,1), ('reserved_96',192,1), ('uptime',32,1), ('reserved_320',8,1), ('fw_major',8,1), ('fw_minor',8,1), ('fw_sub_minor',8,1), ('fw_build_id',32,1), ('fw_month',8,1), ('fw_day',8,1), ('fw_year',16,1), ('reserved_416',16,1), ('fw_hour',16,1), ('fw_psid',128,1), ('fw_init_file_version',32,1), ('reserved_608',8,1), ('hw_major',8,1), ('hw_minor',8,1), ('hw_sub_minor',8,1), ('reserved_640',224,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.hw_revision = 0;
        self.device_id = 0;
        self.reserved_96 = bytearray(24);
        self.uptime = 0;
        self.reserved_320 = 0;
        self.fw_major = 0;
        self.fw_minor = 0;
        self.fw_sub_minor = 0;
        self.fw_build_id = 0;
        self.fw_month = 0;
        self.fw_day = 0;
        self.fw_year = 0;
        self.reserved_416 = 0;
        self.fw_hour = 0;
        self.fw_psid = bytearray(16);
        self.fw_init_file_version = 0;
        self.reserved_608 = 0;
        self.hw_major = 0;
        self.hw_minor = 0;
        self.hw_sub_minor = 0;
        self.reserved_640 = bytearray(28);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 36] = self.reserved_96
        buffer[offset + 56:offset + 72] = self.fw_psid
        buffer[offset + 80:offset + 108] = self.reserved_640
        struct.pack_into('>QHH',buffer,offset+0,self.reserved_0,self.hw_revision,self.device_id);
        struct.pack_into('>LBBBBLBBHHH',buffer,offset+36,self.uptime,self.reserved_320,self.fw_major,self.fw_minor,self.fw_sub_minor,self.fw_build_id,self.fw_month,self.fw_day,self.fw_year,self.reserved_416,self.fw_hour);
        struct.pack_into('>LBBBB',buffer,offset+72,self.fw_init_file_version,self.reserved_608,self.hw_major,self.hw_minor,self.hw_sub_minor);

    def unpack_from(self,buffer,offset=0):
        self.reserved_96 = bytearray(buffer[offset + 12:offset + 36])
        self.fw_psid = bytearray(buffer[offset + 56:offset + 72])
        self.reserved_640 = bytearray(buffer[offset + 80:offset + 108])
        (self.reserved_0,self.hw_revision,self.device_id,) = struct.unpack_from('>QHH',buffer,offset+0);
        (self.uptime,self.reserved_320,self.fw_major,self.fw_minor,self.fw_sub_minor,self.fw_build_id,self.fw_month,self.fw_day,self.fw_year,self.reserved_416,self.fw_hour,) = struct.unpack_from('>LBBBBLBBHHH',buffer,offset+36);
        (self.fw_init_file_version,self.reserved_608,self.hw_major,self.hw_minor,self.hw_sub_minor,) = struct.unpack_from('>LBBBB',buffer,offset+72);

class OFASysStatPing(rdma.binstruct.BinStruct):
    '''None (section None)'''
    __slots__ = ('cookie');
    MAD_LENGTH = 64
    FORMAT = libibtool.vendstruct.OFASysStatFormat
    MAD_ATTRIBUTE_ID = 0x10
    MAD_VENDGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('cookie',64,1)]
    def zero(self):
        self.cookie = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>Q',buffer,offset+0,self.cookie);

    def unpack_from(self,buffer,offset=0):
        (self.cookie,) = struct.unpack_from('>Q',buffer,offset+0);

class OFASysStatHostInfo(rdma.binstruct.BinStruct):
    '''None (section None)'''
    __slots__ = ('data_str');
    MAD_LENGTH = 216
    FORMAT = libibtool.vendstruct.OFASysStatFormat
    MAD_ATTRIBUTE_ID = 0x11
    MAD_VENDGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('data_str',8,216)]
    def __init__(self,*args):
        self.data_str = bytearray(216);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.data_str = bytearray(216);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 216] = self.data_str

    def unpack_from(self,buffer,offset=0):
        self.data_str = bytearray(buffer[offset + 0:offset + 216])

class OFASysStatCPUInfo(rdma.binstruct.BinStruct):
    '''None (section None)'''
    __slots__ = ('data_str');
    MAD_LENGTH = 216
    FORMAT = libibtool.vendstruct.OFASysStatFormat
    MAD_ATTRIBUTE_ID = 0x112
    MAD_VENDGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('data_str',8,216)]
    def __init__(self,*args):
        self.data_str = bytearray(216);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.data_str = bytearray(216);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 216] = self.data_str

    def unpack_from(self,buffer,offset=0):
        self.data_str = bytearray(buffer[offset + 0:offset + 216])

MEMBER_FORMATS = {'data_str': 'str'};
CLASS_TO_STRUCT = {};
ATTR_TO_STRUCT = {(libibtool.vendstruct.MlxFormat,23):MlxGeneralInfo,
	(libibtool.vendstruct.OFASysStatFormat,16):OFASysStatPing,
	(libibtool.vendstruct.OFASysStatFormat,17):OFASysStatHostInfo,
	(libibtool.vendstruct.OFASysStatFormat,274):OFASysStatCPUInfo};
