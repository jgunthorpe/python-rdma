import rdma.binstruct,struct
class HdrLRH(rdma.binstruct.BinStruct):
    '''Local Route Header (section 7.7)'''
    __slots__ = ('VL','LVer','SL','reserved_12','LNH','DLID','reserved_32','pktLen','SLID');
    MAD_LENGTH = 8
    MEMBERS = [('VL',4,1), ('LVer',4,1), ('SL',4,1), ('reserved_12',2,1), ('LNH',2,1), ('DLID',16,1), ('reserved_32',5,1), ('pktLen',11,1), ('SLID',16,1)]
    def zero(self):
        self.VL = 0;
        self.LVer = 0;
        self.SL = 0;
        self.reserved_12 = 0;
        self.LNH = 0;
        self.DLID = 0;
        self.reserved_32 = 0;
        self.pktLen = 0;
        self.SLID = 0;

    @property
    def _pack_0_32(self):
        return ((self.VL & 0xF) << 28) | ((self.LVer & 0xF) << 24) | ((self.SL & 0xF) << 20) | ((self.reserved_12 & 0x3) << 18) | ((self.LNH & 0x3) << 16) | ((self.DLID & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.VL = (value >> 28) & 0xF;
        self.LVer = (value >> 24) & 0xF;
        self.SL = (value >> 20) & 0xF;
        self.reserved_12 = (value >> 18) & 0x3;
        self.LNH = (value >> 16) & 0x3;
        self.DLID = (value >> 0) & 0xFFFF;

    @property
    def _pack_1_32(self):
        return ((self.reserved_32 & 0x1F) << 27) | ((self.pktLen & 0x7FF) << 16) | ((self.SLID & 0xFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved_32 = (value >> 27) & 0x1F;
        self.pktLen = (value >> 16) & 0x7FF;
        self.SLID = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LL',buffer,offset+0,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>LL',buffer,offset+0);

class HdrRWH(rdma.binstruct.BinStruct):
    '''Raw Header (section 5.3)'''
    __slots__ = ('reserved_0','etherType');
    MAD_LENGTH = 4
    MEMBERS = [('reserved_0',16,1), ('etherType',16,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.etherType = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HH',buffer,offset+0,self.reserved_0,self.etherType);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.etherType,) = struct.unpack_from('>HH',buffer,offset+0);

class HdrGRH(rdma.binstruct.BinStruct):
    '''Global Route Header (section 8.3)'''
    __slots__ = ('IPVer','TClass','flowLabel','payLen','nxtHdr','hopLmt','SGID','DGID');
    MAD_LENGTH = 40
    MEMBERS = [('IPVer',4,1), ('TClass',8,1), ('flowLabel',20,1), ('payLen',16,1), ('nxtHdr',8,1), ('hopLmt',8,1), ('SGID',128,1), ('DGID',128,1)]
    def zero(self):
        self.IPVer = 0;
        self.TClass = 0;
        self.flowLabel = 0;
        self.payLen = 0;
        self.nxtHdr = 0;
        self.hopLmt = 0;
        self.SGID = IBA.GID();
        self.DGID = IBA.GID();

    @property
    def _pack_0_32(self):
        return ((self.IPVer & 0xF) << 28) | ((self.TClass & 0xFF) << 20) | ((self.flowLabel & 0xFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.IPVer = (value >> 28) & 0xF;
        self.TClass = (value >> 20) & 0xFF;
        self.flowLabel = (value >> 0) & 0xFFFFF;

    def pack_into(self,buffer,offset=0):
        self.SGID.pack_into(buffer,offset + 8);
        self.DGID.pack_into(buffer,offset + 24);
        struct.pack_into('>LHBB',buffer,offset+0,self._pack_0_32,self.payLen,self.nxtHdr,self.hopLmt);

    def unpack_from(self,buffer,offset=0):
        self.SGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.DGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        (self._pack_0_32,self.payLen,self.nxtHdr,self.hopLmt,) = struct.unpack_from('>LHBB',buffer,offset+0);

class HdrBTH(rdma.binstruct.BinStruct):
    '''Base Transport Header (section 9.2)'''
    __slots__ = ('service','function','SE','migReq','padCnt','TVer','PKey','reserved_32','destQP','ackReq','reserved_65','PSN');
    MAD_LENGTH = 12
    MEMBERS = [('service',3,1), ('function',5,1), ('SE',1,1), ('migReq',1,1), ('padCnt',2,1), ('TVer',4,1), ('PKey',16,1), ('reserved_32',8,1), ('destQP',24,1), ('ackReq',1,1), ('reserved_65',7,1), ('PSN',24,1)]
    def zero(self):
        self.service = 0;
        self.function = 0;
        self.SE = 0;
        self.migReq = 0;
        self.padCnt = 0;
        self.TVer = 0;
        self.PKey = 0;
        self.reserved_32 = 0;
        self.destQP = 0;
        self.ackReq = 0;
        self.reserved_65 = 0;
        self.PSN = 0;

    @property
    def _pack_0_32(self):
        return ((self.service & 0x7) << 29) | ((self.function & 0x1F) << 24) | ((self.SE & 0x1) << 23) | ((self.migReq & 0x1) << 22) | ((self.padCnt & 0x3) << 20) | ((self.TVer & 0xF) << 16) | ((self.PKey & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.service = (value >> 29) & 0x7;
        self.function = (value >> 24) & 0x1F;
        self.SE = (value >> 23) & 0x1;
        self.migReq = (value >> 22) & 0x1;
        self.padCnt = (value >> 20) & 0x3;
        self.TVer = (value >> 16) & 0xF;
        self.PKey = (value >> 0) & 0xFFFF;

    @property
    def _pack_1_32(self):
        return ((self.reserved_32 & 0xFF) << 24) | ((self.destQP & 0xFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved_32 = (value >> 24) & 0xFF;
        self.destQP = (value >> 0) & 0xFFFFFF;

    @property
    def _pack_2_32(self):
        return ((self.ackReq & 0x1) << 31) | ((self.reserved_65 & 0x7F) << 24) | ((self.PSN & 0xFFFFFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.ackReq = (value >> 31) & 0x1;
        self.reserved_65 = (value >> 24) & 0x7F;
        self.PSN = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LLL',buffer,offset+0,self._pack_0_32,self._pack_1_32,self._pack_2_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,self._pack_1_32,self._pack_2_32,) = struct.unpack_from('>LLL',buffer,offset+0);

class HdrRDETH(rdma.binstruct.BinStruct):
    '''Reliable Datagram Extended Transport Header (section 9.3.1)'''
    __slots__ = ('reserved_0','EEC');
    MAD_LENGTH = 4
    MEMBERS = [('reserved_0',8,1), ('EEC',24,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.EEC = 0;

    @property
    def _pack_0_32(self):
        return ((self.reserved_0 & 0xFF) << 24) | ((self.EEC & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.reserved_0 = (value >> 24) & 0xFF;
        self.EEC = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

class HdrDETH(rdma.binstruct.BinStruct):
    '''Datagram Extended Transport Header (section 9.3.2)'''
    __slots__ = ('QKey','reserved_32','srcQP');
    MAD_LENGTH = 8
    MEMBERS = [('QKey',32,1), ('reserved_32',8,1), ('srcQP',24,1)]
    def zero(self):
        self.QKey = 0;
        self.reserved_32 = 0;
        self.srcQP = 0;

    @property
    def _pack_0_32(self):
        return ((self.reserved_32 & 0xFF) << 24) | ((self.srcQP & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.reserved_32 = (value >> 24) & 0xFF;
        self.srcQP = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LL',buffer,offset+0,self.QKey,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        (self.QKey,self._pack_0_32,) = struct.unpack_from('>LL',buffer,offset+0);

class HdrRETH(rdma.binstruct.BinStruct):
    '''RDMA Extended Transport Header (section 9.3.3)'''
    __slots__ = ('VA','RKey','DMALen');
    MAD_LENGTH = 16
    MEMBERS = [('VA',64,1), ('RKey',32,1), ('DMALen',32,1)]
    def zero(self):
        self.VA = 0;
        self.RKey = 0;
        self.DMALen = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QLL',buffer,offset+0,self.VA,self.RKey,self.DMALen);

    def unpack_from(self,buffer,offset=0):
        (self.VA,self.RKey,self.DMALen,) = struct.unpack_from('>QLL',buffer,offset+0);

class HdrAtomicETH(rdma.binstruct.BinStruct):
    '''Atomic Extended Transport Header (section 9.3.4)'''
    __slots__ = ('VA','RKey','swapData','cmpData');
    MAD_LENGTH = 28
    MEMBERS = [('VA',64,1), ('RKey',32,1), ('swapData',64,1), ('cmpData',64,1)]
    def zero(self):
        self.VA = 0;
        self.RKey = 0;
        self.swapData = 0;
        self.cmpData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QLQQ',buffer,offset+0,self.VA,self.RKey,self.swapData,self.cmpData);

    def unpack_from(self,buffer,offset=0):
        (self.VA,self.RKey,self.swapData,self.cmpData,) = struct.unpack_from('>QLQQ',buffer,offset+0);

class HdrAETH(rdma.binstruct.BinStruct):
    '''ACK Extended Transport Header (section 9.3.5)'''
    __slots__ = ('syndrome','MSN');
    MAD_LENGTH = 4
    MEMBERS = [('syndrome',8,1), ('MSN',24,1)]
    def zero(self):
        self.syndrome = 0;
        self.MSN = 0;

    @property
    def _pack_0_32(self):
        return ((self.syndrome & 0xFF) << 24) | ((self.MSN & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.syndrome = (value >> 24) & 0xFF;
        self.MSN = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

class HdrAtomicAckETH(rdma.binstruct.BinStruct):
    '''Atomic Acknowledge Extended Transport Header (section 9.5.3)'''
    __slots__ = ('origRData');
    MAD_LENGTH = 8
    MEMBERS = [('origRData',64,1)]
    def zero(self):
        self.origRData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>Q',buffer,offset+0,self.origRData);

    def unpack_from(self,buffer,offset=0):
        (self.origRData,) = struct.unpack_from('>Q',buffer,offset+0);

class HdrImmDt(rdma.binstruct.BinStruct):
    '''Immediate Extended Transport Header (section 9.3.6)'''
    __slots__ = ('immediateData');
    MAD_LENGTH = 4
    MEMBERS = [('immediateData',32,1)]
    def zero(self):
        self.immediateData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self.immediateData);

    def unpack_from(self,buffer,offset=0):
        (self.immediateData,) = struct.unpack_from('>L',buffer,offset+0);

class HdrIETH(rdma.binstruct.BinStruct):
    '''Invalidate Extended Transport Header (section 9.3.7)'''
    __slots__ = ('RKey');
    MAD_LENGTH = 4
    MEMBERS = [('RKey',32,1)]
    def zero(self):
        self.RKey = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self.RKey);

    def unpack_from(self,buffer,offset=0):
        (self.RKey,) = struct.unpack_from('>L',buffer,offset+0);

class HdrFlowControl(rdma.binstruct.BinStruct):
    '''Flow Control Packet (section 7.9.4)'''
    __slots__ = ('op','FCTBS','VL','FCCL');
    MAD_LENGTH = 4
    MEMBERS = [('op',4,1), ('FCTBS',12,1), ('VL',4,1), ('FCCL',12,1)]
    def zero(self):
        self.op = 0;
        self.FCTBS = 0;
        self.VL = 0;
        self.FCCL = 0;

    @property
    def _pack_0_32(self):
        return ((self.op & 0xF) << 28) | ((self.FCTBS & 0xFFF) << 16) | ((self.VL & 0xF) << 12) | ((self.FCCL & 0xFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.op = (value >> 28) & 0xF;
        self.FCTBS = (value >> 16) & 0xFFF;
        self.VL = (value >> 12) & 0xF;
        self.FCCL = (value >> 0) & 0xFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

class CMFormat(rdma.binstruct.BinFormat):
    '''Request for Communication (section 16.7.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x7
    MAD_CLASS_VERSION = 0x2
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('data',1856,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.data = bytearray(232);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self.data = bytearray(buffer[offset + 24:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

class CMPath(rdma.binstruct.BinStruct):
    '''Path Information (section 12.6)'''
    __slots__ = ('SLID','DLID','SGID','DGID','flowLabel','reserved_308','reserved_312','PD','TClass','hopLimit','SL','subnetLocal','reserved_341','localACKTimeout','reserved_349');
    MAD_LENGTH = 44
    MEMBERS = [('SLID',16,1), ('DLID',16,1), ('SGID',128,1), ('DGID',128,1), ('flowLabel',20,1), ('reserved_308',4,1), ('reserved_312',2,1), ('PD',6,1), ('TClass',8,1), ('hopLimit',8,1), ('SL',4,1), ('subnetLocal',1,1), ('reserved_341',3,1), ('localACKTimeout',5,1), ('reserved_349',3,1)]
    def zero(self):
        self.SLID = 0;
        self.DLID = 0;
        self.SGID = IBA.GID();
        self.DGID = IBA.GID();
        self.flowLabel = 0;
        self.reserved_308 = 0;
        self.reserved_312 = 0;
        self.PD = 0;
        self.TClass = 0;
        self.hopLimit = 0;
        self.SL = 0;
        self.subnetLocal = 0;
        self.reserved_341 = 0;
        self.localACKTimeout = 0;
        self.reserved_349 = 0;

    @property
    def _pack_0_32(self):
        return ((self.flowLabel & 0xFFFFF) << 12) | ((self.reserved_308 & 0xF) << 8) | ((self.reserved_312 & 0x3) << 6) | ((self.PD & 0x3F) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.flowLabel = (value >> 12) & 0xFFFFF;
        self.reserved_308 = (value >> 8) & 0xF;
        self.reserved_312 = (value >> 6) & 0x3;
        self.PD = (value >> 0) & 0x3F;

    @property
    def _pack_1_32(self):
        return ((self.TClass & 0xFF) << 24) | ((self.hopLimit & 0xFF) << 16) | ((self.SL & 0xF) << 12) | ((self.subnetLocal & 0x1) << 11) | ((self.reserved_341 & 0x7) << 8) | ((self.localACKTimeout & 0x1F) << 3) | ((self.reserved_349 & 0x7) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.TClass = (value >> 24) & 0xFF;
        self.hopLimit = (value >> 16) & 0xFF;
        self.SL = (value >> 12) & 0xF;
        self.subnetLocal = (value >> 11) & 0x1;
        self.reserved_341 = (value >> 8) & 0x7;
        self.localACKTimeout = (value >> 3) & 0x1F;
        self.reserved_349 = (value >> 0) & 0x7;

    def pack_into(self,buffer,offset=0):
        self.SGID.pack_into(buffer,offset + 4);
        self.DGID.pack_into(buffer,offset + 20);
        struct.pack_into('>HH',buffer,offset+0,self.SLID,self.DLID);
        struct.pack_into('>LL',buffer,offset+36,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self.SGID = IBA.GID(buffer[offset + 4:offset + 20],raw=True);
        self.DGID = IBA.GID(buffer[offset + 20:offset + 36],raw=True);
        (self.SLID,self.DLID,) = struct.unpack_from('>HH',buffer,offset+0);
        (self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>LL',buffer,offset+36);

class CMREQ(rdma.binstruct.BinStruct):
    '''Request for Communication (section 12.6.5)'''
    __slots__ = ('LCID','reserved_32','serviceID','LGUID','localCMQKey','localQKey','localQPN','responderResources','localEECN','initiatorDepth','remoteEECN','remoteResponseTimeout','transportService','flowControl','startingPSN','localResponseTimeout','retryCount','PKey','pathPacketMTU','RDCExists','RNRRetryCount','maxCMRetries','reserved_412','primaryPath','alternatePath','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x10
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('reserved_32',32,1), ('serviceID',64,1), ('LGUID',64,1), ('localCMQKey',32,1), ('localQKey',32,1), ('localQPN',24,1), ('responderResources',8,1), ('localEECN',24,1), ('initiatorDepth',8,1), ('remoteEECN',24,1), ('remoteResponseTimeout',5,1), ('transportService',2,1), ('flowControl',1,1), ('startingPSN',24,1), ('localResponseTimeout',5,1), ('retryCount',3,1), ('PKey',16,1), ('pathPacketMTU',4,1), ('RDCExists',1,1), ('RNRRetryCount',3,1), ('maxCMRetries',4,1), ('reserved_412',4,1), ('primaryPath',352,1), ('alternatePath',352,1), ('privateData',736,1)]
    def __init__(self,*args):
        self.primaryPath = CMPath();
        self.alternatePath = CMPath();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LCID = 0;
        self.reserved_32 = 0;
        self.serviceID = 0;
        self.LGUID = IBA.GUID();
        self.localCMQKey = 0;
        self.localQKey = 0;
        self.localQPN = 0;
        self.responderResources = 0;
        self.localEECN = 0;
        self.initiatorDepth = 0;
        self.remoteEECN = 0;
        self.remoteResponseTimeout = 0;
        self.transportService = 0;
        self.flowControl = 0;
        self.startingPSN = 0;
        self.localResponseTimeout = 0;
        self.retryCount = 0;
        self.PKey = 0;
        self.pathPacketMTU = 0;
        self.RDCExists = 0;
        self.RNRRetryCount = 0;
        self.maxCMRetries = 0;
        self.reserved_412 = 0;
        self.primaryPath = CMPath();
        self.alternatePath = CMPath();
        self.privateData = bytearray(92);

    @property
    def _pack_0_32(self):
        return ((self.localQPN & 0xFFFFFF) << 8) | ((self.responderResources & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.localQPN = (value >> 8) & 0xFFFFFF;
        self.responderResources = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.localEECN & 0xFFFFFF) << 8) | ((self.initiatorDepth & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.localEECN = (value >> 8) & 0xFFFFFF;
        self.initiatorDepth = (value >> 0) & 0xFF;

    @property
    def _pack_2_32(self):
        return ((self.remoteEECN & 0xFFFFFF) << 8) | ((self.remoteResponseTimeout & 0x1F) << 3) | ((self.transportService & 0x3) << 1) | ((self.flowControl & 0x1) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.remoteEECN = (value >> 8) & 0xFFFFFF;
        self.remoteResponseTimeout = (value >> 3) & 0x1F;
        self.transportService = (value >> 1) & 0x3;
        self.flowControl = (value >> 0) & 0x1;

    @property
    def _pack_3_32(self):
        return ((self.startingPSN & 0xFFFFFF) << 8) | ((self.localResponseTimeout & 0x1F) << 3) | ((self.retryCount & 0x7) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.startingPSN = (value >> 8) & 0xFFFFFF;
        self.localResponseTimeout = (value >> 3) & 0x1F;
        self.retryCount = (value >> 0) & 0x7;

    @property
    def _pack_4_32(self):
        return ((self.PKey & 0xFFFF) << 16) | ((self.pathPacketMTU & 0xF) << 12) | ((self.RDCExists & 0x1) << 11) | ((self.RNRRetryCount & 0x7) << 8) | ((self.maxCMRetries & 0xF) << 4) | ((self.reserved_412 & 0xF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.PKey = (value >> 16) & 0xFFFF;
        self.pathPacketMTU = (value >> 12) & 0xF;
        self.RDCExists = (value >> 11) & 0x1;
        self.RNRRetryCount = (value >> 8) & 0x7;
        self.maxCMRetries = (value >> 4) & 0xF;
        self.reserved_412 = (value >> 0) & 0xF;

    def pack_into(self,buffer,offset=0):
        self.LGUID.pack_into(buffer,offset + 16);
        self.primaryPath.pack_into(buffer,offset + 52);
        self.alternatePath.pack_into(buffer,offset + 96);
        buffer[offset + 140:offset + 232] = self.privateData
        struct.pack_into('>LLQ',buffer,offset+0,self.LCID,self.reserved_32,self.serviceID);
        struct.pack_into('>LLLLLLL',buffer,offset+24,self.localCMQKey,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32);

    def unpack_from(self,buffer,offset=0):
        self.LGUID = IBA.GUID(buffer[offset + 16:offset + 24],raw=True);
        self.primaryPath.unpack_from(buffer,offset + 52);
        self.alternatePath.unpack_from(buffer,offset + 96);
        self.privateData = bytearray(buffer[offset + 140:offset + 232])
        (self.LCID,self.reserved_32,self.serviceID,) = struct.unpack_from('>LLQ',buffer,offset+0);
        (self.localCMQKey,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32,) = struct.unpack_from('>LLLLLLL',buffer,offset+24);

class CMMRA(rdma.binstruct.BinStruct):
    '''Message Receipt Acknowledgement (section 12.6.6)'''
    __slots__ = ('LCID','RCID','messageMRAed','reserved_66','serviceTimeout','reserved_77','reserved_80','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x11
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('messageMRAed',2,1), ('reserved_66',6,1), ('serviceTimeout',5,1), ('reserved_77',3,1), ('reserved_80',16,1), ('privateData',1760,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.messageMRAed = 0;
        self.reserved_66 = 0;
        self.serviceTimeout = 0;
        self.reserved_77 = 0;
        self.reserved_80 = 0;
        self.privateData = bytearray(220);

    @property
    def _pack_0_32(self):
        return ((self.messageMRAed & 0x3) << 30) | ((self.reserved_66 & 0x3F) << 24) | ((self.serviceTimeout & 0x1F) << 19) | ((self.reserved_77 & 0x7) << 16) | ((self.reserved_80 & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.messageMRAed = (value >> 30) & 0x3;
        self.reserved_66 = (value >> 24) & 0x3F;
        self.serviceTimeout = (value >> 19) & 0x1F;
        self.reserved_77 = (value >> 16) & 0x7;
        self.reserved_80 = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 232] = self.privateData
        struct.pack_into('>LLL',buffer,offset+0,self.LCID,self.RCID,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.privateData = bytearray(buffer[offset + 12:offset + 232])
        (self.LCID,self.RCID,self._pack_0_32,) = struct.unpack_from('>LLL',buffer,offset+0);

class CMREJ(rdma.binstruct.BinStruct):
    '''Reject (section 12.6.7)'''
    __slots__ = ('LCID','RCID','messageRejected','reserved_66','rejectInfoLength','reserved_79','reason','ARI','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x12
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('messageRejected',2,1), ('reserved_66',6,1), ('rejectInfoLength',7,1), ('reserved_79',1,1), ('reason',16,1), ('ARI',576,1), ('privateData',1184,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.messageRejected = 0;
        self.reserved_66 = 0;
        self.rejectInfoLength = 0;
        self.reserved_79 = 0;
        self.reason = 0;
        self.ARI = bytearray(72);
        self.privateData = bytearray(148);

    @property
    def _pack_0_32(self):
        return ((self.messageRejected & 0x3) << 30) | ((self.reserved_66 & 0x3F) << 24) | ((self.rejectInfoLength & 0x7F) << 17) | ((self.reserved_79 & 0x1) << 16) | ((self.reason & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.messageRejected = (value >> 30) & 0x3;
        self.reserved_66 = (value >> 24) & 0x3F;
        self.rejectInfoLength = (value >> 17) & 0x7F;
        self.reserved_79 = (value >> 16) & 0x1;
        self.reason = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 84] = self.ARI
        buffer[offset + 84:offset + 232] = self.privateData
        struct.pack_into('>LLL',buffer,offset+0,self.LCID,self.RCID,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.ARI = bytearray(buffer[offset + 12:offset + 84])
        self.privateData = bytearray(buffer[offset + 84:offset + 232])
        (self.LCID,self.RCID,self._pack_0_32,) = struct.unpack_from('>LLL',buffer,offset+0);

class CMREP(rdma.binstruct.BinStruct):
    '''Reply To Request For Communication (section 12.6.8)'''
    __slots__ = ('LCID','RCID','localQKey','localQPN','reserved_120','localEEContext','reserved_152','startingPSN','reserved_184','responderResources','initiatorDepth','targetACKDelay','failoverAccepted','flowControl','RNRRetryCount','reserved_219','LGUID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x13
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('localQKey',32,1), ('localQPN',24,1), ('reserved_120',8,1), ('localEEContext',24,1), ('reserved_152',8,1), ('startingPSN',24,1), ('reserved_184',8,1), ('responderResources',8,1), ('initiatorDepth',8,1), ('targetACKDelay',5,1), ('failoverAccepted',2,1), ('flowControl',1,1), ('RNRRetryCount',3,1), ('reserved_219',5,1), ('LGUID',64,1), ('privateData',1568,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.localQKey = 0;
        self.localQPN = 0;
        self.reserved_120 = 0;
        self.localEEContext = 0;
        self.reserved_152 = 0;
        self.startingPSN = 0;
        self.reserved_184 = 0;
        self.responderResources = 0;
        self.initiatorDepth = 0;
        self.targetACKDelay = 0;
        self.failoverAccepted = 0;
        self.flowControl = 0;
        self.RNRRetryCount = 0;
        self.reserved_219 = 0;
        self.LGUID = IBA.GUID();
        self.privateData = bytearray(196);

    @property
    def _pack_0_32(self):
        return ((self.localQPN & 0xFFFFFF) << 8) | ((self.reserved_120 & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.localQPN = (value >> 8) & 0xFFFFFF;
        self.reserved_120 = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.localEEContext & 0xFFFFFF) << 8) | ((self.reserved_152 & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.localEEContext = (value >> 8) & 0xFFFFFF;
        self.reserved_152 = (value >> 0) & 0xFF;

    @property
    def _pack_2_32(self):
        return ((self.startingPSN & 0xFFFFFF) << 8) | ((self.reserved_184 & 0xFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.startingPSN = (value >> 8) & 0xFFFFFF;
        self.reserved_184 = (value >> 0) & 0xFF;

    @property
    def _pack_3_32(self):
        return ((self.responderResources & 0xFF) << 24) | ((self.initiatorDepth & 0xFF) << 16) | ((self.targetACKDelay & 0x1F) << 11) | ((self.failoverAccepted & 0x3) << 9) | ((self.flowControl & 0x1) << 8) | ((self.RNRRetryCount & 0x7) << 5) | ((self.reserved_219 & 0x1F) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.responderResources = (value >> 24) & 0xFF;
        self.initiatorDepth = (value >> 16) & 0xFF;
        self.targetACKDelay = (value >> 11) & 0x1F;
        self.failoverAccepted = (value >> 9) & 0x3;
        self.flowControl = (value >> 8) & 0x1;
        self.RNRRetryCount = (value >> 5) & 0x7;
        self.reserved_219 = (value >> 0) & 0x1F;

    def pack_into(self,buffer,offset=0):
        self.LGUID.pack_into(buffer,offset + 28);
        buffer[offset + 36:offset + 232] = self.privateData
        struct.pack_into('>LLLLLLL',buffer,offset+0,self.LCID,self.RCID,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32);

    def unpack_from(self,buffer,offset=0):
        self.LGUID = IBA.GUID(buffer[offset + 28:offset + 36],raw=True);
        self.privateData = bytearray(buffer[offset + 36:offset + 232])
        (self.LCID,self.RCID,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,) = struct.unpack_from('>LLLLLLL',buffer,offset+0);

class CMRTU(rdma.binstruct.BinStruct):
    '''Ready To Use (section 12.6.9)'''
    __slots__ = ('LCID','RCID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x14
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('privateData',1792,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.privateData = bytearray(224);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 8:offset + 232] = self.privateData
        struct.pack_into('>LL',buffer,offset+0,self.LCID,self.RCID);

    def unpack_from(self,buffer,offset=0):
        self.privateData = bytearray(buffer[offset + 8:offset + 232])
        (self.LCID,self.RCID,) = struct.unpack_from('>LL',buffer,offset+0);

class CMDREQ(rdma.binstruct.BinStruct):
    '''Request For Communication Release (Disconnection Request) (section 12.6.10)'''
    __slots__ = ('LCID','RCID','remoteQPN','reserved_88','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x15
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('remoteQPN',24,1), ('reserved_88',8,1), ('privateData',1760,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.remoteQPN = 0;
        self.reserved_88 = 0;
        self.privateData = bytearray(220);

    @property
    def _pack_0_32(self):
        return ((self.remoteQPN & 0xFFFFFF) << 8) | ((self.reserved_88 & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.remoteQPN = (value >> 8) & 0xFFFFFF;
        self.reserved_88 = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 232] = self.privateData
        struct.pack_into('>LLL',buffer,offset+0,self.LCID,self.RCID,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.privateData = bytearray(buffer[offset + 12:offset + 232])
        (self.LCID,self.RCID,self._pack_0_32,) = struct.unpack_from('>LLL',buffer,offset+0);

class CMDREP(rdma.binstruct.BinStruct):
    '''Reply To Request For Communication Release (section 12.6.11)'''
    __slots__ = ('LCID','RCID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x16
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('privateData',1792,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.privateData = bytearray(224);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 8:offset + 232] = self.privateData
        struct.pack_into('>LL',buffer,offset+0,self.LCID,self.RCID);

    def unpack_from(self,buffer,offset=0):
        self.privateData = bytearray(buffer[offset + 8:offset + 232])
        (self.LCID,self.RCID,) = struct.unpack_from('>LL',buffer,offset+0);

class CMLAP(rdma.binstruct.BinStruct):
    '''Load Alternate Path (section 12.8.1)'''
    __slots__ = ('LCID','RCID','QKey','RQPN','RCMTimeout','reserved_125','reserved_128','altSLID','altDLID','altSGID','altDGID','altFlowLabel','reserved_468','altTClass','altHopLimit','reserved_488','altIPD','altSL','altSubnetLocal','reserved_501','altLocalACKTimeout','reserved_509','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x19
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('QKey',32,1), ('RQPN',24,1), ('RCMTimeout',5,1), ('reserved_125',3,1), ('reserved_128',32,1), ('altSLID',16,1), ('altDLID',16,1), ('altSGID',128,1), ('altDGID',128,1), ('altFlowLabel',20,1), ('reserved_468',4,1), ('altTClass',8,1), ('altHopLimit',8,1), ('reserved_488',2,1), ('altIPD',6,1), ('altSL',4,1), ('altSubnetLocal',1,1), ('reserved_501',3,1), ('altLocalACKTimeout',5,1), ('reserved_509',3,1), ('privateData',1344,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.QKey = 0;
        self.RQPN = 0;
        self.RCMTimeout = 0;
        self.reserved_125 = 0;
        self.reserved_128 = 0;
        self.altSLID = 0;
        self.altDLID = 0;
        self.altSGID = IBA.GID();
        self.altDGID = IBA.GID();
        self.altFlowLabel = 0;
        self.reserved_468 = 0;
        self.altTClass = 0;
        self.altHopLimit = 0;
        self.reserved_488 = 0;
        self.altIPD = 0;
        self.altSL = 0;
        self.altSubnetLocal = 0;
        self.reserved_501 = 0;
        self.altLocalACKTimeout = 0;
        self.reserved_509 = 0;
        self.privateData = bytearray(168);

    @property
    def _pack_0_32(self):
        return ((self.RQPN & 0xFFFFFF) << 8) | ((self.RCMTimeout & 0x1F) << 3) | ((self.reserved_125 & 0x7) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RQPN = (value >> 8) & 0xFFFFFF;
        self.RCMTimeout = (value >> 3) & 0x1F;
        self.reserved_125 = (value >> 0) & 0x7;

    @property
    def _pack_1_32(self):
        return ((self.altFlowLabel & 0xFFFFF) << 12) | ((self.reserved_468 & 0xF) << 8) | ((self.altTClass & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.altFlowLabel = (value >> 12) & 0xFFFFF;
        self.reserved_468 = (value >> 8) & 0xF;
        self.altTClass = (value >> 0) & 0xFF;

    @property
    def _pack_2_32(self):
        return ((self.altHopLimit & 0xFF) << 24) | ((self.reserved_488 & 0x3) << 22) | ((self.altIPD & 0x3F) << 16) | ((self.altSL & 0xF) << 12) | ((self.altSubnetLocal & 0x1) << 11) | ((self.reserved_501 & 0x7) << 8) | ((self.altLocalACKTimeout & 0x1F) << 3) | ((self.reserved_509 & 0x7) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.altHopLimit = (value >> 24) & 0xFF;
        self.reserved_488 = (value >> 22) & 0x3;
        self.altIPD = (value >> 16) & 0x3F;
        self.altSL = (value >> 12) & 0xF;
        self.altSubnetLocal = (value >> 11) & 0x1;
        self.reserved_501 = (value >> 8) & 0x7;
        self.altLocalACKTimeout = (value >> 3) & 0x1F;
        self.reserved_509 = (value >> 0) & 0x7;

    def pack_into(self,buffer,offset=0):
        self.altSGID.pack_into(buffer,offset + 24);
        self.altDGID.pack_into(buffer,offset + 40);
        buffer[offset + 64:offset + 232] = self.privateData
        struct.pack_into('>LLLLLHH',buffer,offset+0,self.LCID,self.RCID,self.QKey,self._pack_0_32,self.reserved_128,self.altSLID,self.altDLID);
        struct.pack_into('>LL',buffer,offset+56,self._pack_1_32,self._pack_2_32);

    def unpack_from(self,buffer,offset=0):
        self.altSGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        self.altDGID = IBA.GID(buffer[offset + 40:offset + 56],raw=True);
        self.privateData = bytearray(buffer[offset + 64:offset + 232])
        (self.LCID,self.RCID,self.QKey,self._pack_0_32,self.reserved_128,self.altSLID,self.altDLID,) = struct.unpack_from('>LLLLLHH',buffer,offset+0);
        (self._pack_1_32,self._pack_2_32,) = struct.unpack_from('>LL',buffer,offset+56);

class CMAPR(rdma.binstruct.BinStruct):
    '''Alternate Path Response (section 12.8.2)'''
    __slots__ = ('LCID','RCID','additionalInfoLength','APstatus','reserved_80','additionalInfo','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x1a
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('LCID',32,1), ('RCID',32,1), ('additionalInfoLength',8,1), ('APstatus',8,1), ('reserved_80',16,1), ('additionalInfo',576,1), ('privateData',1184,1)]
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.additionalInfoLength = 0;
        self.APstatus = 0;
        self.reserved_80 = 0;
        self.additionalInfo = bytearray(72);
        self.privateData = bytearray(148);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 84] = self.additionalInfo
        buffer[offset + 84:offset + 232] = self.privateData
        struct.pack_into('>LLBBH',buffer,offset+0,self.LCID,self.RCID,self.additionalInfoLength,self.APstatus,self.reserved_80);

    def unpack_from(self,buffer,offset=0):
        self.additionalInfo = bytearray(buffer[offset + 12:offset + 84])
        self.privateData = bytearray(buffer[offset + 84:offset + 232])
        (self.LCID,self.RCID,self.additionalInfoLength,self.APstatus,self.reserved_80,) = struct.unpack_from('>LLBBH',buffer,offset+0);

class CMSIDR_REQ(rdma.binstruct.BinStruct):
    '''Service ID Resolution Request (section 12.11.1)'''
    __slots__ = ('requestID','reserved_32','serviceID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x17
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('requestID',32,1), ('reserved_32',32,1), ('serviceID',64,1), ('privateData',1728,1)]
    def zero(self):
        self.requestID = 0;
        self.reserved_32 = 0;
        self.serviceID = 0;
        self.privateData = bytearray(216);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 16:offset + 232] = self.privateData
        struct.pack_into('>LLQ',buffer,offset+0,self.requestID,self.reserved_32,self.serviceID);

    def unpack_from(self,buffer,offset=0):
        self.privateData = bytearray(buffer[offset + 16:offset + 232])
        (self.requestID,self.reserved_32,self.serviceID,) = struct.unpack_from('>LLQ',buffer,offset+0);

class CMSIDR_REP(rdma.binstruct.BinStruct):
    '''Service ID Resolution Response (section 12.11.2)'''
    __slots__ = ('requestID','QPN','status','serviceID','QKey','classPortinfo','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x18
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('requestID',32,1), ('QPN',24,1), ('status',8,1), ('serviceID',64,1), ('QKey',32,1), ('classPortinfo',576,1), ('privateData',1120,1)]
    def __init__(self,*args):
        self.classPortinfo = MADClassPortInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.requestID = 0;
        self.QPN = 0;
        self.status = 0;
        self.serviceID = 0;
        self.QKey = 0;
        self.classPortinfo = MADClassPortInfo();
        self.privateData = bytearray(140);

    @property
    def _pack_0_32(self):
        return ((self.QPN & 0xFFFFFF) << 8) | ((self.status & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.QPN = (value >> 8) & 0xFFFFFF;
        self.status = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        self.classPortinfo.pack_into(buffer,offset + 20);
        buffer[offset + 92:offset + 232] = self.privateData
        struct.pack_into('>LLQL',buffer,offset+0,self.requestID,self._pack_0_32,self.serviceID,self.QKey);

    def unpack_from(self,buffer,offset=0):
        self.classPortinfo.unpack_from(buffer,offset + 20);
        self.privateData = bytearray(buffer[offset + 92:offset + 232])
        (self.requestID,self._pack_0_32,self.serviceID,self.QKey,) = struct.unpack_from('>LLQL',buffer,offset+0);

class MADHeader(rdma.binstruct.BinStruct):
    '''MAD Base Header (section 13.4.3)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier');
    MAD_LENGTH = 24
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

class MADHeaderDirected(rdma.binstruct.BinStruct):
    '''MAD Base Header Directed (section 13.4.3)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','D','status','hopPointer','hopCount','transactionID','attributeID','reserved_144','attributeModifier');
    MAD_LENGTH = 24
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('D',1,1), ('status',15,1), ('hopPointer',8,1), ('hopCount',8,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.D = 0;
        self.status = 0;
        self.hopPointer = 0;
        self.hopCount = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;

    @property
    def _pack_0_32(self):
        return ((self.D & 0x1) << 31) | ((self.status & 0x7FFF) << 16) | ((self.hopPointer & 0xFF) << 8) | ((self.hopCount & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.D = (value >> 31) & 0x1;
        self.status = (value >> 16) & 0x7FFF;
        self.hopPointer = (value >> 8) & 0xFF;
        self.hopCount = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBBBLQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBLQHHL',buffer,offset+0);

class MADClassPortInfo(rdma.binstruct.BinStruct):
    '''Class Port Info (section 13.4.8.1)'''
    __slots__ = ('baseVersion','classVersion','capabilityMask','capabilityMask2','respTimeValue','redirectGID','redirectTC','redirectSL','redirectFL','redirectLID','redirectPKey','reserved_256','redirectQP','redirectQKey','trapGID','trapTC','trapSL','trapFL','trapLID','trapPKey','trapHL','trapQP','trapQKey');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x1
    MAD_BMGET = 0x1 # MAD_METHOD_GET
    MAD_BMSET = 0x2 # MAD_METHOD_SET
    MAD_COMMMGTGET = 0x1 # MAD_METHOD_GET
    MAD_COMMMGTSET = 0x2 # MAD_METHOD_SET
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_SNMPGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    COMPONENT_MASK = {'baseVersion':0, 'classVersion':1, 'capabilityMask':2, 'capabilityMask2':3, 'respTimeValue':4, 'redirectGID':5, 'redirectTC':6, 'redirectSL':7, 'redirectFL':8, 'redirectLID':9, 'redirectPKey':10, 'reserved_256':11, 'redirectQP':12, 'redirectQKey':13, 'trapGID':14, 'trapTC':15, 'trapSL':16, 'trapFL':17, 'trapLID':18, 'trapPKey':19, 'trapHL':20, 'trapQP':21, 'trapQKey':22}
    MEMBERS = [('baseVersion',8,1), ('classVersion',8,1), ('capabilityMask',16,1), ('capabilityMask2',27,1), ('respTimeValue',5,1), ('redirectGID',128,1), ('redirectTC',8,1), ('redirectSL',4,1), ('redirectFL',20,1), ('redirectLID',16,1), ('redirectPKey',16,1), ('reserved_256',8,1), ('redirectQP',24,1), ('redirectQKey',32,1), ('trapGID',128,1), ('trapTC',8,1), ('trapSL',4,1), ('trapFL',20,1), ('trapLID',16,1), ('trapPKey',16,1), ('trapHL',8,1), ('trapQP',24,1), ('trapQKey',32,1)]
    def zero(self):
        self.baseVersion = 0;
        self.classVersion = 0;
        self.capabilityMask = 0;
        self.capabilityMask2 = 0;
        self.respTimeValue = 0;
        self.redirectGID = IBA.GID();
        self.redirectTC = 0;
        self.redirectSL = 0;
        self.redirectFL = 0;
        self.redirectLID = 0;
        self.redirectPKey = 0;
        self.reserved_256 = 0;
        self.redirectQP = 0;
        self.redirectQKey = 0;
        self.trapGID = IBA.GID();
        self.trapTC = 0;
        self.trapSL = 0;
        self.trapFL = 0;
        self.trapLID = 0;
        self.trapPKey = 0;
        self.trapHL = 0;
        self.trapQP = 0;
        self.trapQKey = 0;

    @property
    def _pack_0_32(self):
        return ((self.capabilityMask2 & 0x7FFFFFF) << 5) | ((self.respTimeValue & 0x1F) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.capabilityMask2 = (value >> 5) & 0x7FFFFFF;
        self.respTimeValue = (value >> 0) & 0x1F;

    @property
    def _pack_1_32(self):
        return ((self.redirectTC & 0xFF) << 24) | ((self.redirectSL & 0xF) << 20) | ((self.redirectFL & 0xFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.redirectTC = (value >> 24) & 0xFF;
        self.redirectSL = (value >> 20) & 0xF;
        self.redirectFL = (value >> 0) & 0xFFFFF;

    @property
    def _pack_2_32(self):
        return ((self.reserved_256 & 0xFF) << 24) | ((self.redirectQP & 0xFFFFFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved_256 = (value >> 24) & 0xFF;
        self.redirectQP = (value >> 0) & 0xFFFFFF;

    @property
    def _pack_3_32(self):
        return ((self.trapTC & 0xFF) << 24) | ((self.trapSL & 0xF) << 20) | ((self.trapFL & 0xFFFFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.trapTC = (value >> 24) & 0xFF;
        self.trapSL = (value >> 20) & 0xF;
        self.trapFL = (value >> 0) & 0xFFFFF;

    @property
    def _pack_4_32(self):
        return ((self.trapHL & 0xFF) << 24) | ((self.trapQP & 0xFFFFFF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.trapHL = (value >> 24) & 0xFF;
        self.trapQP = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.redirectGID.pack_into(buffer,offset + 8);
        self.trapGID.pack_into(buffer,offset + 40);
        struct.pack_into('>BBHL',buffer,offset+0,self.baseVersion,self.classVersion,self.capabilityMask,self._pack_0_32);
        struct.pack_into('>LHHLL',buffer,offset+24,self._pack_1_32,self.redirectLID,self.redirectPKey,self._pack_2_32,self.redirectQKey);
        struct.pack_into('>LHHLL',buffer,offset+56,self._pack_3_32,self.trapLID,self.trapPKey,self._pack_4_32,self.trapQKey);

    def unpack_from(self,buffer,offset=0):
        self.redirectGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.trapGID = IBA.GID(buffer[offset + 40:offset + 56],raw=True);
        (self.baseVersion,self.classVersion,self.capabilityMask,self._pack_0_32,) = struct.unpack_from('>BBHL',buffer,offset+0);
        (self._pack_1_32,self.redirectLID,self.redirectPKey,self._pack_2_32,self.redirectQKey,) = struct.unpack_from('>LHHLL',buffer,offset+24);
        (self._pack_3_32,self.trapLID,self.trapPKey,self._pack_4_32,self.trapQKey,) = struct.unpack_from('>LHHLL',buffer,offset+56);

class MADInformInfo(rdma.binstruct.BinStruct):
    '''InformInfo (section 13.4.8.3)'''
    __slots__ = ('GID','LIDRangeBegin','LIDRangeEnd','reserved_160','isGeneric','subscribe','type','trapNumber','QPN','reserved_248','respTimeValue','reserved_256','producerType');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x3
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    COMPONENT_MASK = {'GID':0, 'LIDRangeBegin':1, 'LIDRangeEnd':2, 'reserved_160':3, 'isGeneric':4, 'subscribe':5, 'type':6, 'trapNumber':7, 'QPN':8, 'reserved_248':9, 'respTimeValue':10, 'reserved_256':11, 'producerType':12}
    MEMBERS = [('GID',128,1), ('LIDRangeBegin',16,1), ('LIDRangeEnd',16,1), ('reserved_160',16,1), ('isGeneric',8,1), ('subscribe',8,1), ('type',16,1), ('trapNumber',16,1), ('QPN',24,1), ('reserved_248',3,1), ('respTimeValue',5,1), ('reserved_256',8,1), ('producerType',24,1)]
    def zero(self):
        self.GID = IBA.GID();
        self.LIDRangeBegin = 0;
        self.LIDRangeEnd = 0;
        self.reserved_160 = 0;
        self.isGeneric = 0;
        self.subscribe = 0;
        self.type = 0;
        self.trapNumber = 0;
        self.QPN = 0;
        self.reserved_248 = 0;
        self.respTimeValue = 0;
        self.reserved_256 = 0;
        self.producerType = 0;

    @property
    def _pack_0_32(self):
        return ((self.QPN & 0xFFFFFF) << 8) | ((self.reserved_248 & 0x7) << 5) | ((self.respTimeValue & 0x1F) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.QPN = (value >> 8) & 0xFFFFFF;
        self.reserved_248 = (value >> 5) & 0x7;
        self.respTimeValue = (value >> 0) & 0x1F;

    @property
    def _pack_1_32(self):
        return ((self.reserved_256 & 0xFF) << 24) | ((self.producerType & 0xFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved_256 = (value >> 24) & 0xFF;
        self.producerType = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.GID.pack_into(buffer,offset + 0);
        struct.pack_into('>HHHBBHHLL',buffer,offset+16,self.LIDRangeBegin,self.LIDRangeEnd,self.reserved_160,self.isGeneric,self.subscribe,self.type,self.trapNumber,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self.GID = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        (self.LIDRangeBegin,self.LIDRangeEnd,self.reserved_160,self.isGeneric,self.subscribe,self.type,self.trapNumber,self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>HHHBBHHLL',buffer,offset+16);

class RMPPHeader(rdma.binstruct.BinStruct):
    '''RMPP Header Fields (section 13.6.2.1)'''
    __slots__ = ('MADHeader','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus','data1','data2');
    MAD_LENGTH = 36
    MEMBERS = [('MADHeader',192,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1)]
    def __init__(self,*args):
        self.MADHeader = MADHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.MADHeader = MADHeader();
        self.RMPPVersion = 0;
        self.RMPPType = 0;
        self.RRespTime = 0;
        self.RMPPFlags = 0;
        self.RMPPStatus = 0;
        self.data1 = 0;
        self.data2 = 0;

    @property
    def _pack_0_32(self):
        return ((self.RMPPVersion & 0xFF) << 24) | ((self.RMPPType & 0xFF) << 16) | ((self.RRespTime & 0x1F) << 11) | ((self.RMPPFlags & 0x7) << 8) | ((self.RMPPStatus & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RMPPVersion = (value >> 24) & 0xFF;
        self.RMPPType = (value >> 16) & 0xFF;
        self.RRespTime = (value >> 11) & 0x1F;
        self.RMPPFlags = (value >> 8) & 0x7;
        self.RMPPStatus = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        self.MADHeader.pack_into(buffer,offset + 0);
        struct.pack_into('>LLL',buffer,offset+24,self._pack_0_32,self.data1,self.data2);

    def unpack_from(self,buffer,offset=0):
        self.MADHeader.unpack_from(buffer,offset + 0);
        (self._pack_0_32,self.data1,self.data2,) = struct.unpack_from('>LLL',buffer,offset+24);

class RMPPShortHeader(rdma.binstruct.BinStruct):
    '''RMPP Header Fields (section 13.6.2.1)'''
    __slots__ = ('MADHeader','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus');
    MAD_LENGTH = 28
    MEMBERS = [('MADHeader',192,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1)]
    def __init__(self,*args):
        self.MADHeader = MADHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.MADHeader = MADHeader();
        self.RMPPVersion = 0;
        self.RMPPType = 0;
        self.RRespTime = 0;
        self.RMPPFlags = 0;
        self.RMPPStatus = 0;

    @property
    def _pack_0_32(self):
        return ((self.RMPPVersion & 0xFF) << 24) | ((self.RMPPType & 0xFF) << 16) | ((self.RRespTime & 0x1F) << 11) | ((self.RMPPFlags & 0x7) << 8) | ((self.RMPPStatus & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RMPPVersion = (value >> 24) & 0xFF;
        self.RMPPType = (value >> 16) & 0xFF;
        self.RRespTime = (value >> 11) & 0x1F;
        self.RMPPFlags = (value >> 8) & 0x7;
        self.RMPPStatus = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        self.MADHeader.pack_into(buffer,offset + 0);
        struct.pack_into('>L',buffer,offset+24,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.MADHeader.unpack_from(buffer,offset + 0);
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+24);

class RMPPData(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','segmentNumber','payLoadLength','data');
    MAD_LENGTH = 256
    MEMBERS = [('RMPPHeader',224,1), ('segmentNumber',32,1), ('payLoadLength',32,1), ('data',1760,1)]
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.segmentNumber = 0;
        self.payLoadLength = 0;
        self.data = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.data
        struct.pack_into('>LL',buffer,offset+28,self.segmentNumber,self.payLoadLength);

    def unpack_from(self,buffer,offset=0):
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.data = bytearray(buffer[offset + 36:offset + 256])
        (self.segmentNumber,self.payLoadLength,) = struct.unpack_from('>LL',buffer,offset+28);

class RMPPAck(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','segmentNumber','newWindowLast','reserved_288');
    MAD_LENGTH = 256
    MEMBERS = [('RMPPHeader',224,1), ('segmentNumber',32,1), ('newWindowLast',32,1), ('reserved_288',1760,1)]
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.segmentNumber = 0;
        self.newWindowLast = 0;
        self.reserved_288 = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.reserved_288
        struct.pack_into('>LL',buffer,offset+28,self.segmentNumber,self.newWindowLast);

    def unpack_from(self,buffer,offset=0):
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.reserved_288 = bytearray(buffer[offset + 36:offset + 256])
        (self.segmentNumber,self.newWindowLast,) = struct.unpack_from('>LL',buffer,offset+28);

class RMPPAbort(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','reserved_224','reserved_256','errorData');
    MAD_LENGTH = 256
    MEMBERS = [('RMPPHeader',224,1), ('reserved_224',32,1), ('reserved_256',32,1), ('errorData',1760,1)]
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.reserved_224 = 0;
        self.reserved_256 = 0;
        self.errorData = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.errorData
        struct.pack_into('>LL',buffer,offset+28,self.reserved_224,self.reserved_256);

    def unpack_from(self,buffer,offset=0):
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.errorData = bytearray(buffer[offset + 36:offset + 256])
        (self.reserved_224,self.reserved_256,) = struct.unpack_from('>LL',buffer,offset+28);

class RMPPStop(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','reserved_224','reserved_256','errorData');
    MAD_LENGTH = 256
    MEMBERS = [('RMPPHeader',224,1), ('reserved_224',32,1), ('reserved_256',32,1), ('errorData',1760,1)]
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.reserved_224 = 0;
        self.reserved_256 = 0;
        self.errorData = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.errorData
        struct.pack_into('>LL',buffer,offset+28,self.reserved_224,self.reserved_256);

    def unpack_from(self,buffer,offset=0):
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.errorData = bytearray(buffer[offset + 36:offset + 256])
        (self.reserved_224,self.reserved_256,) = struct.unpack_from('>LL',buffer,offset+28);

class SMPLIDPortBlock(rdma.binstruct.BinStruct):
    '''LID/Port Block Element (section 14.2.5.11)'''
    __slots__ = ('LID','valid','LMC','reserved_20','port');
    MAD_LENGTH = 4
    MEMBERS = [('LID',16,1), ('valid',1,1), ('LMC',3,1), ('reserved_20',4,1), ('port',8,1)]
    def zero(self):
        self.LID = 0;
        self.valid = 0;
        self.LMC = 0;
        self.reserved_20 = 0;
        self.port = 0;

    @property
    def _pack_0_32(self):
        return ((self.LID & 0xFFFF) << 16) | ((self.valid & 0x1) << 15) | ((self.LMC & 0x7) << 12) | ((self.reserved_20 & 0xF) << 8) | ((self.port & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.LID = (value >> 16) & 0xFFFF;
        self.valid = (value >> 15) & 0x1;
        self.LMC = (value >> 12) & 0x7;
        self.reserved_20 = (value >> 8) & 0xF;
        self.port = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

class SMPFormat(rdma.binstruct.BinFormat):
    '''SMP Format - LID Routed (section 14.2.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','MKey','reserved_256','data','reserved_1024');
    MAD_LENGTH = 256
    MAD_CLASS = 0x1
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('MKey',64,1), ('reserved_256',256,1), ('data',512,1), ('reserved_1024',1024,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.MKey = 0;
        self.reserved_256 = bytearray(32);
        self.data = bytearray(64);
        self.reserved_1024 = bytearray(128);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 32:offset + 64] = self.reserved_256
        buffer[offset + 64:offset + 128] = self.data
        buffer[offset + 128:offset + 256] = self.reserved_1024
        struct.pack_into('>BBBBHHQHHLQ',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self.MKey);

    def unpack_from(self,buffer,offset=0):
        self.reserved_256 = bytearray(buffer[offset + 32:offset + 64])
        self.data = bytearray(buffer[offset + 64:offset + 128])
        self.reserved_1024 = bytearray(buffer[offset + 128:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self.MKey,) = struct.unpack_from('>BBBBHHQHHLQ',buffer,offset+0);

class SMPFormatDirected(rdma.binstruct.BinFormat):
    '''SMP Format - Direct Routed (section 14.2.1.2)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','D','status','hopPointer','hopCount','transactionID','attributeID','reserved_144','attributeModifier','MKey','drSLID','drDLID','reserved_288','data','initialPath','returnPath');
    MAD_LENGTH = 256
    MAD_CLASS = 0x81
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('D',1,1), ('status',15,1), ('hopPointer',8,1), ('hopCount',8,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('MKey',64,1), ('drSLID',16,1), ('drDLID',16,1), ('reserved_288',224,1), ('data',512,1), ('initialPath',8,64), ('returnPath',8,64)]
    def __init__(self,*args):
        self.initialPath = bytearray(64);
        self.returnPath = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.D = 0;
        self.status = 0;
        self.hopPointer = 0;
        self.hopCount = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.MKey = 0;
        self.drSLID = 0;
        self.drDLID = 0;
        self.reserved_288 = bytearray(28);
        self.data = bytearray(64);
        self.initialPath = bytearray(64);
        self.returnPath = bytearray(64);

    @property
    def _pack_0_32(self):
        return ((self.D & 0x1) << 31) | ((self.status & 0x7FFF) << 16) | ((self.hopPointer & 0xFF) << 8) | ((self.hopCount & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.D = (value >> 31) & 0x1;
        self.status = (value >> 16) & 0x7FFF;
        self.hopPointer = (value >> 8) & 0xFF;
        self.hopCount = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 36:offset + 64] = self.reserved_288
        buffer[offset + 64:offset + 128] = self.data
        buffer[offset + 128:offset + 192] = self.initialPath
        buffer[offset + 192:offset + 256] = self.returnPath
        struct.pack_into('>BBBBLQHHLQHH',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self.MKey,self.drSLID,self.drDLID);

    def unpack_from(self,buffer,offset=0):
        self.reserved_288 = bytearray(buffer[offset + 36:offset + 64])
        self.data = bytearray(buffer[offset + 64:offset + 128])
        self.initialPath = bytearray(buffer[offset + 128:offset + 192])
        self.returnPath = bytearray(buffer[offset + 192:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self.MKey,self.drSLID,self.drDLID,) = struct.unpack_from('>BBBBLQHHLQHH',buffer,offset+0);

class SMPNodeDescription(rdma.binstruct.BinStruct):
    '''Node Description String (section 14.2.5.2)'''
    __slots__ = ('nodeString');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x10
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('nodeString',8,64)]
    def __init__(self,*args):
        self.nodeString = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.nodeString = bytearray(64);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 64] = self.nodeString

    def unpack_from(self,buffer,offset=0):
        self.nodeString = bytearray(buffer[offset + 0:offset + 64])

class SMPNodeInfo(rdma.binstruct.BinStruct):
    '''Generic Node Data (section 14.2.5.3)'''
    __slots__ = ('baseVersion','classVersion','nodeType','numPorts','systemImageGUID','nodeGUID','portGUID','partitionCap','deviceID','revision','localPortNum','vendorID');
    MAD_LENGTH = 40
    MAD_ATTRIBUTE_ID = 0x11
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('baseVersion',8,1), ('classVersion',8,1), ('nodeType',8,1), ('numPorts',8,1), ('systemImageGUID',64,1), ('nodeGUID',64,1), ('portGUID',64,1), ('partitionCap',16,1), ('deviceID',16,1), ('revision',32,1), ('localPortNum',8,1), ('vendorID',24,1)]
    def zero(self):
        self.baseVersion = 0;
        self.classVersion = 0;
        self.nodeType = 0;
        self.numPorts = 0;
        self.systemImageGUID = IBA.GUID();
        self.nodeGUID = IBA.GUID();
        self.portGUID = IBA.GUID();
        self.partitionCap = 0;
        self.deviceID = 0;
        self.revision = 0;
        self.localPortNum = 0;
        self.vendorID = 0;

    @property
    def _pack_0_32(self):
        return ((self.localPortNum & 0xFF) << 24) | ((self.vendorID & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.localPortNum = (value >> 24) & 0xFF;
        self.vendorID = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.systemImageGUID.pack_into(buffer,offset + 4);
        self.nodeGUID.pack_into(buffer,offset + 12);
        self.portGUID.pack_into(buffer,offset + 20);
        struct.pack_into('>BBBB',buffer,offset+0,self.baseVersion,self.classVersion,self.nodeType,self.numPorts);
        struct.pack_into('>HHLL',buffer,offset+28,self.partitionCap,self.deviceID,self.revision,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.systemImageGUID = IBA.GUID(buffer[offset + 4:offset + 12],raw=True);
        self.nodeGUID = IBA.GUID(buffer[offset + 12:offset + 20],raw=True);
        self.portGUID = IBA.GUID(buffer[offset + 20:offset + 28],raw=True);
        (self.baseVersion,self.classVersion,self.nodeType,self.numPorts,) = struct.unpack_from('>BBBB',buffer,offset+0);
        (self.partitionCap,self.deviceID,self.revision,self._pack_0_32,) = struct.unpack_from('>HHLL',buffer,offset+28);

class SMPSwitchInfo(rdma.binstruct.BinStruct):
    '''Switch Information (section 14.2.5.4)'''
    __slots__ = ('linearFDBCap','randomFDBCap','multicastFDBCap','linearFDBTop','defaultPort','defaultMulticastPrimaryPort','defaultMulticastNotPrimaryPort','lifeTimeValue','portStateChange','optimizedSLtoVLMappingProgramming','LIDsPerPort','partitionEnforcementCap','inboundEnforcementCap','outboundEnforcementCap','filterRawInboundCap','filterRawOutboundCap','enhancedPort0','reserved_133','reserved_136','multicastFDBTop');
    MAD_LENGTH = 20
    MAD_ATTRIBUTE_ID = 0x12
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('linearFDBCap',16,1), ('randomFDBCap',16,1), ('multicastFDBCap',16,1), ('linearFDBTop',16,1), ('defaultPort',8,1), ('defaultMulticastPrimaryPort',8,1), ('defaultMulticastNotPrimaryPort',8,1), ('lifeTimeValue',5,1), ('portStateChange',1,1), ('optimizedSLtoVLMappingProgramming',2,1), ('LIDsPerPort',16,1), ('partitionEnforcementCap',16,1), ('inboundEnforcementCap',1,1), ('outboundEnforcementCap',1,1), ('filterRawInboundCap',1,1), ('filterRawOutboundCap',1,1), ('enhancedPort0',1,1), ('reserved_133',3,1), ('reserved_136',8,1), ('multicastFDBTop',16,1)]
    def zero(self):
        self.linearFDBCap = 0;
        self.randomFDBCap = 0;
        self.multicastFDBCap = 0;
        self.linearFDBTop = 0;
        self.defaultPort = 0;
        self.defaultMulticastPrimaryPort = 0;
        self.defaultMulticastNotPrimaryPort = 0;
        self.lifeTimeValue = 0;
        self.portStateChange = 0;
        self.optimizedSLtoVLMappingProgramming = 0;
        self.LIDsPerPort = 0;
        self.partitionEnforcementCap = 0;
        self.inboundEnforcementCap = 0;
        self.outboundEnforcementCap = 0;
        self.filterRawInboundCap = 0;
        self.filterRawOutboundCap = 0;
        self.enhancedPort0 = 0;
        self.reserved_133 = 0;
        self.reserved_136 = 0;
        self.multicastFDBTop = 0;

    @property
    def _pack_0_32(self):
        return ((self.defaultPort & 0xFF) << 24) | ((self.defaultMulticastPrimaryPort & 0xFF) << 16) | ((self.defaultMulticastNotPrimaryPort & 0xFF) << 8) | ((self.lifeTimeValue & 0x1F) << 3) | ((self.portStateChange & 0x1) << 2) | ((self.optimizedSLtoVLMappingProgramming & 0x3) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.defaultPort = (value >> 24) & 0xFF;
        self.defaultMulticastPrimaryPort = (value >> 16) & 0xFF;
        self.defaultMulticastNotPrimaryPort = (value >> 8) & 0xFF;
        self.lifeTimeValue = (value >> 3) & 0x1F;
        self.portStateChange = (value >> 2) & 0x1;
        self.optimizedSLtoVLMappingProgramming = (value >> 0) & 0x3;

    @property
    def _pack_1_32(self):
        return ((self.inboundEnforcementCap & 0x1) << 31) | ((self.outboundEnforcementCap & 0x1) << 30) | ((self.filterRawInboundCap & 0x1) << 29) | ((self.filterRawOutboundCap & 0x1) << 28) | ((self.enhancedPort0 & 0x1) << 27) | ((self.reserved_133 & 0x7) << 24) | ((self.reserved_136 & 0xFF) << 16) | ((self.multicastFDBTop & 0xFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.inboundEnforcementCap = (value >> 31) & 0x1;
        self.outboundEnforcementCap = (value >> 30) & 0x1;
        self.filterRawInboundCap = (value >> 29) & 0x1;
        self.filterRawOutboundCap = (value >> 28) & 0x1;
        self.enhancedPort0 = (value >> 27) & 0x1;
        self.reserved_133 = (value >> 24) & 0x7;
        self.reserved_136 = (value >> 16) & 0xFF;
        self.multicastFDBTop = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHLHHL',buffer,offset+0,self.linearFDBCap,self.randomFDBCap,self.multicastFDBCap,self.linearFDBTop,self._pack_0_32,self.LIDsPerPort,self.partitionEnforcementCap,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        (self.linearFDBCap,self.randomFDBCap,self.multicastFDBCap,self.linearFDBTop,self._pack_0_32,self.LIDsPerPort,self.partitionEnforcementCap,self._pack_1_32,) = struct.unpack_from('>HHHHLHHL',buffer,offset+0);

class SMPGUIDInfo(rdma.binstruct.BinStruct):
    '''Assigned GUIDs (section 14.2.5.5)'''
    __slots__ = ('GUIDBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x14
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('GUIDBlock',64,8)]
    def __init__(self,*args):
        self.GUIDBlock = [IBA.GUID() for I in range(8)];
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.GUIDBlock = [IBA.GUID() for I in range(8)];

    def pack_into(self,buffer,offset=0):
        self.GUIDBlock[0].pack_into(buffer,offset + 0);
        self.GUIDBlock[1].pack_into(buffer,offset + 8);
        self.GUIDBlock[2].pack_into(buffer,offset + 16);
        self.GUIDBlock[3].pack_into(buffer,offset + 24);
        self.GUIDBlock[4].pack_into(buffer,offset + 32);
        self.GUIDBlock[5].pack_into(buffer,offset + 40);
        self.GUIDBlock[6].pack_into(buffer,offset + 48);
        self.GUIDBlock[7].pack_into(buffer,offset + 56);

    def unpack_from(self,buffer,offset=0):
        self.GUIDBlock[0] = IBA.GUID(buffer[offset + 0:offset + 8],raw=True);
        self.GUIDBlock[1] = IBA.GUID(buffer[offset + 8:offset + 16],raw=True);
        self.GUIDBlock[2] = IBA.GUID(buffer[offset + 16:offset + 24],raw=True);
        self.GUIDBlock[3] = IBA.GUID(buffer[offset + 24:offset + 32],raw=True);
        self.GUIDBlock[4] = IBA.GUID(buffer[offset + 32:offset + 40],raw=True);
        self.GUIDBlock[5] = IBA.GUID(buffer[offset + 40:offset + 48],raw=True);
        self.GUIDBlock[6] = IBA.GUID(buffer[offset + 48:offset + 56],raw=True);
        self.GUIDBlock[7] = IBA.GUID(buffer[offset + 56:offset + 64],raw=True);

class SMPPortInfo(rdma.binstruct.BinStruct):
    '''Port Information (section 14.2.5.6)'''
    __slots__ = ('MKey','GIDPrefix','LID','masterSMLID','capabilityMask','diagCode','MKeyLeasePeriod','localPortNum','linkWidthEnabled','linkWidthSupported','linkWidthActive','linkSpeedSupported','portState','portPhysicalState','linkDownDefaultState','MKeyProtectBits','reserved_274','LMC','linkSpeedActive','linkSpeedEnabled','neighborMTU','masterSMSL','VLCap','initType','VLHighLimit','VLArbitrationHighCap','VLArbitrationLowCap','initTypeReply','MTUCap','VLStallCount','HOQLife','operationalVLs','partitionEnforcementInbound','partitionEnforcementOutbound','filterRawInbound','filterRawOutbound','MKeyViolations','PKeyViolations','QKeyViolations','GUIDCap','clientReregister','multicastPKeyTrapSuppressionEnabled','subnetTimeOut','reserved_416','respTimeValue','localPhyErrors','overrunErrors','maxCreditHint','reserved_448','linkRoundTripLatency','capabilityMask2','linkSpeedExtActive','linkSpeedExtSupported','reserved_504','linkSpeedExtEnabled');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x15
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('MKey',64,1), ('GIDPrefix',64,1), ('LID',16,1), ('masterSMLID',16,1), ('capabilityMask',32,1), ('diagCode',16,1), ('MKeyLeasePeriod',16,1), ('localPortNum',8,1), ('linkWidthEnabled',8,1), ('linkWidthSupported',8,1), ('linkWidthActive',8,1), ('linkSpeedSupported',4,1), ('portState',4,1), ('portPhysicalState',4,1), ('linkDownDefaultState',4,1), ('MKeyProtectBits',2,1), ('reserved_274',3,1), ('LMC',3,1), ('linkSpeedActive',4,1), ('linkSpeedEnabled',4,1), ('neighborMTU',4,1), ('masterSMSL',4,1), ('VLCap',4,1), ('initType',4,1), ('VLHighLimit',8,1), ('VLArbitrationHighCap',8,1), ('VLArbitrationLowCap',8,1), ('initTypeReply',4,1), ('MTUCap',4,1), ('VLStallCount',3,1), ('HOQLife',5,1), ('operationalVLs',4,1), ('partitionEnforcementInbound',1,1), ('partitionEnforcementOutbound',1,1), ('filterRawInbound',1,1), ('filterRawOutbound',1,1), ('MKeyViolations',16,1), ('PKeyViolations',16,1), ('QKeyViolations',16,1), ('GUIDCap',8,1), ('clientReregister',1,1), ('multicastPKeyTrapSuppressionEnabled',2,1), ('subnetTimeOut',5,1), ('reserved_416',3,1), ('respTimeValue',5,1), ('localPhyErrors',4,1), ('overrunErrors',4,1), ('maxCreditHint',16,1), ('reserved_448',8,1), ('linkRoundTripLatency',24,1), ('capabilityMask2',16,1), ('linkSpeedExtActive',4,1), ('linkSpeedExtSupported',4,1), ('reserved_504',3,1), ('linkSpeedExtEnabled',5,1)]
    def zero(self):
        self.MKey = 0;
        self.GIDPrefix = 0;
        self.LID = 0;
        self.masterSMLID = 0;
        self.capabilityMask = 0;
        self.diagCode = 0;
        self.MKeyLeasePeriod = 0;
        self.localPortNum = 0;
        self.linkWidthEnabled = 0;
        self.linkWidthSupported = 0;
        self.linkWidthActive = 0;
        self.linkSpeedSupported = 0;
        self.portState = 0;
        self.portPhysicalState = 0;
        self.linkDownDefaultState = 0;
        self.MKeyProtectBits = 0;
        self.reserved_274 = 0;
        self.LMC = 0;
        self.linkSpeedActive = 0;
        self.linkSpeedEnabled = 0;
        self.neighborMTU = 0;
        self.masterSMSL = 0;
        self.VLCap = 0;
        self.initType = 0;
        self.VLHighLimit = 0;
        self.VLArbitrationHighCap = 0;
        self.VLArbitrationLowCap = 0;
        self.initTypeReply = 0;
        self.MTUCap = 0;
        self.VLStallCount = 0;
        self.HOQLife = 0;
        self.operationalVLs = 0;
        self.partitionEnforcementInbound = 0;
        self.partitionEnforcementOutbound = 0;
        self.filterRawInbound = 0;
        self.filterRawOutbound = 0;
        self.MKeyViolations = 0;
        self.PKeyViolations = 0;
        self.QKeyViolations = 0;
        self.GUIDCap = 0;
        self.clientReregister = 0;
        self.multicastPKeyTrapSuppressionEnabled = 0;
        self.subnetTimeOut = 0;
        self.reserved_416 = 0;
        self.respTimeValue = 0;
        self.localPhyErrors = 0;
        self.overrunErrors = 0;
        self.maxCreditHint = 0;
        self.reserved_448 = 0;
        self.linkRoundTripLatency = 0;
        self.capabilityMask2 = 0;
        self.linkSpeedExtActive = 0;
        self.linkSpeedExtSupported = 0;
        self.reserved_504 = 0;
        self.linkSpeedExtEnabled = 0;

    @property
    def _pack_0_32(self):
        return ((self.linkSpeedSupported & 0xF) << 28) | ((self.portState & 0xF) << 24) | ((self.portPhysicalState & 0xF) << 20) | ((self.linkDownDefaultState & 0xF) << 16) | ((self.MKeyProtectBits & 0x3) << 14) | ((self.reserved_274 & 0x7) << 11) | ((self.LMC & 0x7) << 8) | ((self.linkSpeedActive & 0xF) << 4) | ((self.linkSpeedEnabled & 0xF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.linkSpeedSupported = (value >> 28) & 0xF;
        self.portState = (value >> 24) & 0xF;
        self.portPhysicalState = (value >> 20) & 0xF;
        self.linkDownDefaultState = (value >> 16) & 0xF;
        self.MKeyProtectBits = (value >> 14) & 0x3;
        self.reserved_274 = (value >> 11) & 0x7;
        self.LMC = (value >> 8) & 0x7;
        self.linkSpeedActive = (value >> 4) & 0xF;
        self.linkSpeedEnabled = (value >> 0) & 0xF;

    @property
    def _pack_1_32(self):
        return ((self.neighborMTU & 0xF) << 28) | ((self.masterSMSL & 0xF) << 24) | ((self.VLCap & 0xF) << 20) | ((self.initType & 0xF) << 16) | ((self.VLHighLimit & 0xFF) << 8) | ((self.VLArbitrationHighCap & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.neighborMTU = (value >> 28) & 0xF;
        self.masterSMSL = (value >> 24) & 0xF;
        self.VLCap = (value >> 20) & 0xF;
        self.initType = (value >> 16) & 0xF;
        self.VLHighLimit = (value >> 8) & 0xFF;
        self.VLArbitrationHighCap = (value >> 0) & 0xFF;

    @property
    def _pack_2_32(self):
        return ((self.VLArbitrationLowCap & 0xFF) << 24) | ((self.initTypeReply & 0xF) << 20) | ((self.MTUCap & 0xF) << 16) | ((self.VLStallCount & 0x7) << 13) | ((self.HOQLife & 0x1F) << 8) | ((self.operationalVLs & 0xF) << 4) | ((self.partitionEnforcementInbound & 0x1) << 3) | ((self.partitionEnforcementOutbound & 0x1) << 2) | ((self.filterRawInbound & 0x1) << 1) | ((self.filterRawOutbound & 0x1) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.VLArbitrationLowCap = (value >> 24) & 0xFF;
        self.initTypeReply = (value >> 20) & 0xF;
        self.MTUCap = (value >> 16) & 0xF;
        self.VLStallCount = (value >> 13) & 0x7;
        self.HOQLife = (value >> 8) & 0x1F;
        self.operationalVLs = (value >> 4) & 0xF;
        self.partitionEnforcementInbound = (value >> 3) & 0x1;
        self.partitionEnforcementOutbound = (value >> 2) & 0x1;
        self.filterRawInbound = (value >> 1) & 0x1;
        self.filterRawOutbound = (value >> 0) & 0x1;

    @property
    def _pack_3_32(self):
        return ((self.QKeyViolations & 0xFFFF) << 16) | ((self.GUIDCap & 0xFF) << 8) | ((self.clientReregister & 0x1) << 7) | ((self.multicastPKeyTrapSuppressionEnabled & 0x3) << 5) | ((self.subnetTimeOut & 0x1F) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.QKeyViolations = (value >> 16) & 0xFFFF;
        self.GUIDCap = (value >> 8) & 0xFF;
        self.clientReregister = (value >> 7) & 0x1;
        self.multicastPKeyTrapSuppressionEnabled = (value >> 5) & 0x3;
        self.subnetTimeOut = (value >> 0) & 0x1F;

    @property
    def _pack_4_32(self):
        return ((self.reserved_416 & 0x7) << 29) | ((self.respTimeValue & 0x1F) << 24) | ((self.localPhyErrors & 0xF) << 20) | ((self.overrunErrors & 0xF) << 16) | ((self.maxCreditHint & 0xFFFF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.reserved_416 = (value >> 29) & 0x7;
        self.respTimeValue = (value >> 24) & 0x1F;
        self.localPhyErrors = (value >> 20) & 0xF;
        self.overrunErrors = (value >> 16) & 0xF;
        self.maxCreditHint = (value >> 0) & 0xFFFF;

    @property
    def _pack_5_32(self):
        return ((self.reserved_448 & 0xFF) << 24) | ((self.linkRoundTripLatency & 0xFFFFFF) << 0)

    @_pack_5_32.setter
    def _pack_5_32(self,value):
        self.reserved_448 = (value >> 24) & 0xFF;
        self.linkRoundTripLatency = (value >> 0) & 0xFFFFFF;

    @property
    def _pack_6_32(self):
        return ((self.capabilityMask2 & 0xFFFF) << 16) | ((self.linkSpeedExtActive & 0xF) << 12) | ((self.linkSpeedExtSupported & 0xF) << 8) | ((self.reserved_504 & 0x7) << 5) | ((self.linkSpeedExtEnabled & 0x1F) << 0)

    @_pack_6_32.setter
    def _pack_6_32(self,value):
        self.capabilityMask2 = (value >> 16) & 0xFFFF;
        self.linkSpeedExtActive = (value >> 12) & 0xF;
        self.linkSpeedExtSupported = (value >> 8) & 0xF;
        self.reserved_504 = (value >> 5) & 0x7;
        self.linkSpeedExtEnabled = (value >> 0) & 0x1F;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QQHHLHHBBBBLLLHHLLLL',buffer,offset+0,self.MKey,self.GIDPrefix,self.LID,self.masterSMLID,self.capabilityMask,self.diagCode,self.MKeyLeasePeriod,self.localPortNum,self.linkWidthEnabled,self.linkWidthSupported,self.linkWidthActive,self._pack_0_32,self._pack_1_32,self._pack_2_32,self.MKeyViolations,self.PKeyViolations,self._pack_3_32,self._pack_4_32,self._pack_5_32,self._pack_6_32);

    def unpack_from(self,buffer,offset=0):
        (self.MKey,self.GIDPrefix,self.LID,self.masterSMLID,self.capabilityMask,self.diagCode,self.MKeyLeasePeriod,self.localPortNum,self.linkWidthEnabled,self.linkWidthSupported,self.linkWidthActive,self._pack_0_32,self._pack_1_32,self._pack_2_32,self.MKeyViolations,self.PKeyViolations,self._pack_3_32,self._pack_4_32,self._pack_5_32,self._pack_6_32,) = struct.unpack_from('>QQHHLHHBBBBLLLHHLLLL',buffer,offset+0);

class SMPPKeyTable(rdma.binstruct.BinStruct):
    '''Partition Table (section 14.2.5.7)'''
    __slots__ = ('PKeyBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x16
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('PKeyBlock',16,32)]
    def __init__(self,*args):
        self.PKeyBlock = [0]*32;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.PKeyBlock = [0]*32;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self.PKeyBlock[0],self.PKeyBlock[1],self.PKeyBlock[2],self.PKeyBlock[3],self.PKeyBlock[4],self.PKeyBlock[5],self.PKeyBlock[6],self.PKeyBlock[7],self.PKeyBlock[8],self.PKeyBlock[9],self.PKeyBlock[10],self.PKeyBlock[11],self.PKeyBlock[12],self.PKeyBlock[13],self.PKeyBlock[14],self.PKeyBlock[15],self.PKeyBlock[16],self.PKeyBlock[17],self.PKeyBlock[18],self.PKeyBlock[19],self.PKeyBlock[20],self.PKeyBlock[21],self.PKeyBlock[22],self.PKeyBlock[23],self.PKeyBlock[24],self.PKeyBlock[25],self.PKeyBlock[26],self.PKeyBlock[27],self.PKeyBlock[28],self.PKeyBlock[29],self.PKeyBlock[30],self.PKeyBlock[31]);

    def unpack_from(self,buffer,offset=0):
        (self.PKeyBlock[0],self.PKeyBlock[1],self.PKeyBlock[2],self.PKeyBlock[3],self.PKeyBlock[4],self.PKeyBlock[5],self.PKeyBlock[6],self.PKeyBlock[7],self.PKeyBlock[8],self.PKeyBlock[9],self.PKeyBlock[10],self.PKeyBlock[11],self.PKeyBlock[12],self.PKeyBlock[13],self.PKeyBlock[14],self.PKeyBlock[15],self.PKeyBlock[16],self.PKeyBlock[17],self.PKeyBlock[18],self.PKeyBlock[19],self.PKeyBlock[20],self.PKeyBlock[21],self.PKeyBlock[22],self.PKeyBlock[23],self.PKeyBlock[24],self.PKeyBlock[25],self.PKeyBlock[26],self.PKeyBlock[27],self.PKeyBlock[28],self.PKeyBlock[29],self.PKeyBlock[30],self.PKeyBlock[31],) = struct.unpack_from('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

class SMPSLToVLMappingTable(rdma.binstruct.BinStruct):
    '''Service Level to Virtual Lane mapping Information (section 14.2.5.8)'''
    __slots__ = ('SLtoVL');
    MAD_LENGTH = 8
    MAD_ATTRIBUTE_ID = 0x17
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('SLtoVL',4,16)]
    def __init__(self,*args):
        self.SLtoVL = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.SLtoVL = [0]*16;

    def pack_into(self,buffer,offset=0):
        rdma.binstruct.pack_array8(buffer,offset+0,4,16,self.SLtoVL);

    def unpack_from(self,buffer,offset=0):
        rdma.binstruct.unpack_array8(buffer,offset+0,4,16,self.SLtoVL);

class SMPVLArbitrationTable(rdma.binstruct.BinStruct):
    '''List of Weights (section 14.2.5.9)'''
    __slots__ = ('VLWeightBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x18
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('VLWeightBlock',16,32)]
    def __init__(self,*args):
        self.VLWeightBlock = [0]*32;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.VLWeightBlock = [0]*32;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self.VLWeightBlock[0],self.VLWeightBlock[1],self.VLWeightBlock[2],self.VLWeightBlock[3],self.VLWeightBlock[4],self.VLWeightBlock[5],self.VLWeightBlock[6],self.VLWeightBlock[7],self.VLWeightBlock[8],self.VLWeightBlock[9],self.VLWeightBlock[10],self.VLWeightBlock[11],self.VLWeightBlock[12],self.VLWeightBlock[13],self.VLWeightBlock[14],self.VLWeightBlock[15],self.VLWeightBlock[16],self.VLWeightBlock[17],self.VLWeightBlock[18],self.VLWeightBlock[19],self.VLWeightBlock[20],self.VLWeightBlock[21],self.VLWeightBlock[22],self.VLWeightBlock[23],self.VLWeightBlock[24],self.VLWeightBlock[25],self.VLWeightBlock[26],self.VLWeightBlock[27],self.VLWeightBlock[28],self.VLWeightBlock[29],self.VLWeightBlock[30],self.VLWeightBlock[31]);

    def unpack_from(self,buffer,offset=0):
        (self.VLWeightBlock[0],self.VLWeightBlock[1],self.VLWeightBlock[2],self.VLWeightBlock[3],self.VLWeightBlock[4],self.VLWeightBlock[5],self.VLWeightBlock[6],self.VLWeightBlock[7],self.VLWeightBlock[8],self.VLWeightBlock[9],self.VLWeightBlock[10],self.VLWeightBlock[11],self.VLWeightBlock[12],self.VLWeightBlock[13],self.VLWeightBlock[14],self.VLWeightBlock[15],self.VLWeightBlock[16],self.VLWeightBlock[17],self.VLWeightBlock[18],self.VLWeightBlock[19],self.VLWeightBlock[20],self.VLWeightBlock[21],self.VLWeightBlock[22],self.VLWeightBlock[23],self.VLWeightBlock[24],self.VLWeightBlock[25],self.VLWeightBlock[26],self.VLWeightBlock[27],self.VLWeightBlock[28],self.VLWeightBlock[29],self.VLWeightBlock[30],self.VLWeightBlock[31],) = struct.unpack_from('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

class SMPLinearForwardingTable(rdma.binstruct.BinStruct):
    '''Linear Forwarding Table Information (section 14.2.5.10)'''
    __slots__ = ('portBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x19
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('portBlock',8,64)]
    def __init__(self,*args):
        self.portBlock = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.portBlock = bytearray(64);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 64] = self.portBlock

    def unpack_from(self,buffer,offset=0):
        self.portBlock = bytearray(buffer[offset + 0:offset + 64])

class SMPRandomForwardingTable(rdma.binstruct.BinStruct):
    '''Random Forwarding Table Information (section 14.2.5.11)'''
    __slots__ = ('LIDPortBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x1a
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('LIDPortBlock',32,16)]
    def __init__(self,*args):
        self.LIDPortBlock = [SMPLIDPortBlock() for I in range(16)];
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LIDPortBlock = [SMPLIDPortBlock() for I in range(16)];

    def pack_into(self,buffer,offset=0):
        self.LIDPortBlock[0].pack_into(buffer,offset + 0);
        self.LIDPortBlock[1].pack_into(buffer,offset + 4);
        self.LIDPortBlock[2].pack_into(buffer,offset + 8);
        self.LIDPortBlock[3].pack_into(buffer,offset + 12);
        self.LIDPortBlock[4].pack_into(buffer,offset + 16);
        self.LIDPortBlock[5].pack_into(buffer,offset + 20);
        self.LIDPortBlock[6].pack_into(buffer,offset + 24);
        self.LIDPortBlock[7].pack_into(buffer,offset + 28);
        self.LIDPortBlock[8].pack_into(buffer,offset + 32);
        self.LIDPortBlock[9].pack_into(buffer,offset + 36);
        self.LIDPortBlock[10].pack_into(buffer,offset + 40);
        self.LIDPortBlock[11].pack_into(buffer,offset + 44);
        self.LIDPortBlock[12].pack_into(buffer,offset + 48);
        self.LIDPortBlock[13].pack_into(buffer,offset + 52);
        self.LIDPortBlock[14].pack_into(buffer,offset + 56);
        self.LIDPortBlock[15].pack_into(buffer,offset + 60);

    def unpack_from(self,buffer,offset=0):
        self.LIDPortBlock[0].unpack_from(buffer,offset + 0);
        self.LIDPortBlock[1].unpack_from(buffer,offset + 4);
        self.LIDPortBlock[2].unpack_from(buffer,offset + 8);
        self.LIDPortBlock[3].unpack_from(buffer,offset + 12);
        self.LIDPortBlock[4].unpack_from(buffer,offset + 16);
        self.LIDPortBlock[5].unpack_from(buffer,offset + 20);
        self.LIDPortBlock[6].unpack_from(buffer,offset + 24);
        self.LIDPortBlock[7].unpack_from(buffer,offset + 28);
        self.LIDPortBlock[8].unpack_from(buffer,offset + 32);
        self.LIDPortBlock[9].unpack_from(buffer,offset + 36);
        self.LIDPortBlock[10].unpack_from(buffer,offset + 40);
        self.LIDPortBlock[11].unpack_from(buffer,offset + 44);
        self.LIDPortBlock[12].unpack_from(buffer,offset + 48);
        self.LIDPortBlock[13].unpack_from(buffer,offset + 52);
        self.LIDPortBlock[14].unpack_from(buffer,offset + 56);
        self.LIDPortBlock[15].unpack_from(buffer,offset + 60);

class SMPMulticastForwardingTable(rdma.binstruct.BinStruct):
    '''Multicast Forwarding Table Information (section 14.2.5.12)'''
    __slots__ = ('portMaskBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x1b
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('portMaskBlock',16,32)]
    def __init__(self,*args):
        self.portMaskBlock = [0]*32;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.portMaskBlock = [0]*32;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self.portMaskBlock[0],self.portMaskBlock[1],self.portMaskBlock[2],self.portMaskBlock[3],self.portMaskBlock[4],self.portMaskBlock[5],self.portMaskBlock[6],self.portMaskBlock[7],self.portMaskBlock[8],self.portMaskBlock[9],self.portMaskBlock[10],self.portMaskBlock[11],self.portMaskBlock[12],self.portMaskBlock[13],self.portMaskBlock[14],self.portMaskBlock[15],self.portMaskBlock[16],self.portMaskBlock[17],self.portMaskBlock[18],self.portMaskBlock[19],self.portMaskBlock[20],self.portMaskBlock[21],self.portMaskBlock[22],self.portMaskBlock[23],self.portMaskBlock[24],self.portMaskBlock[25],self.portMaskBlock[26],self.portMaskBlock[27],self.portMaskBlock[28],self.portMaskBlock[29],self.portMaskBlock[30],self.portMaskBlock[31]);

    def unpack_from(self,buffer,offset=0):
        (self.portMaskBlock[0],self.portMaskBlock[1],self.portMaskBlock[2],self.portMaskBlock[3],self.portMaskBlock[4],self.portMaskBlock[5],self.portMaskBlock[6],self.portMaskBlock[7],self.portMaskBlock[8],self.portMaskBlock[9],self.portMaskBlock[10],self.portMaskBlock[11],self.portMaskBlock[12],self.portMaskBlock[13],self.portMaskBlock[14],self.portMaskBlock[15],self.portMaskBlock[16],self.portMaskBlock[17],self.portMaskBlock[18],self.portMaskBlock[19],self.portMaskBlock[20],self.portMaskBlock[21],self.portMaskBlock[22],self.portMaskBlock[23],self.portMaskBlock[24],self.portMaskBlock[25],self.portMaskBlock[26],self.portMaskBlock[27],self.portMaskBlock[28],self.portMaskBlock[29],self.portMaskBlock[30],self.portMaskBlock[31],) = struct.unpack_from('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

class SMPSMInfo(rdma.binstruct.BinStruct):
    '''Subnet Management Information (section 14.2.5.13)'''
    __slots__ = ('GUID','SMKey','actCount','priority','SMState','reserved_168');
    MAD_LENGTH = 24
    MAD_ATTRIBUTE_ID = 0x20
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('GUID',64,1), ('SMKey',64,1), ('actCount',32,1), ('priority',4,1), ('SMState',4,1), ('reserved_168',24,1)]
    def zero(self):
        self.GUID = IBA.GUID();
        self.SMKey = 0;
        self.actCount = 0;
        self.priority = 0;
        self.SMState = 0;
        self.reserved_168 = 0;

    @property
    def _pack_0_32(self):
        return ((self.priority & 0xF) << 28) | ((self.SMState & 0xF) << 24) | ((self.reserved_168 & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.priority = (value >> 28) & 0xF;
        self.SMState = (value >> 24) & 0xF;
        self.reserved_168 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.GUID.pack_into(buffer,offset + 0);
        struct.pack_into('>QLL',buffer,offset+8,self.SMKey,self.actCount,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.GUID = IBA.GUID(buffer[offset + 0:offset + 8],raw=True);
        (self.SMKey,self.actCount,self._pack_0_32,) = struct.unpack_from('>QLL',buffer,offset+8);

class SMPVendorDiag(rdma.binstruct.BinStruct):
    '''Vendor Specific Diagnostic (section 14.2.5.14)'''
    __slots__ = ('nextIndex','reserved_16','diagData');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x30
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('nextIndex',16,1), ('reserved_16',16,1), ('diagData',480,1)]
    def zero(self):
        self.nextIndex = 0;
        self.reserved_16 = 0;
        self.diagData = bytearray(60);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 4:offset + 64] = self.diagData
        struct.pack_into('>HH',buffer,offset+0,self.nextIndex,self.reserved_16);

    def unpack_from(self,buffer,offset=0):
        self.diagData = bytearray(buffer[offset + 4:offset + 64])
        (self.nextIndex,self.reserved_16,) = struct.unpack_from('>HH',buffer,offset+0);

class SMPLedInfo(rdma.binstruct.BinStruct):
    '''Turn on/off LED (section 14.2.5.15)'''
    __slots__ = ('ledMask','reserved_1');
    MAD_LENGTH = 4
    MAD_ATTRIBUTE_ID = 0x31
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('ledMask',1,1), ('reserved_1',31,1)]
    def zero(self):
        self.ledMask = 0;
        self.reserved_1 = 0;

    @property
    def _pack_0_32(self):
        return ((self.ledMask & 0x1) << 31) | ((self.reserved_1 & 0x7FFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.ledMask = (value >> 31) & 0x1;
        self.reserved_1 = (value >> 0) & 0x7FFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

class SMPNoticeTrap(rdma.binstruct.BinStruct):
    '''Notice (section 13.4.8.2)'''
    __slots__ = ('isGeneric','noticeType','nodeType','trapNumber','issuerLID','noticeToggle','noticeCount','dataDetails','dataDetails2');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x2
    MAD_SUBNTRAP = 0x5 # MAD_METHOD_TRAP
    MAD_SUBNTRAPREPRESS = 0x7 # MAD_METHOD_TRAP_REPRESS
    MEMBERS = [('isGeneric',1,1), ('noticeType',7,1), ('nodeType',24,1), ('trapNumber',16,1), ('issuerLID',16,1), ('noticeToggle',1,1), ('noticeCount',15,1), ('dataDetails',16,1), ('dataDetails2',16,26)]
    def __init__(self,*args):
        self.dataDetails2 = [0]*26;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.isGeneric = 0;
        self.noticeType = 0;
        self.nodeType = 0;
        self.trapNumber = 0;
        self.issuerLID = 0;
        self.noticeToggle = 0;
        self.noticeCount = 0;
        self.dataDetails = 0;
        self.dataDetails2 = [0]*26;

    @property
    def _pack_0_32(self):
        return ((self.isGeneric & 0x1) << 31) | ((self.noticeType & 0x7F) << 24) | ((self.nodeType & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.isGeneric = (value >> 31) & 0x1;
        self.noticeType = (value >> 24) & 0x7F;
        self.nodeType = (value >> 0) & 0xFFFFFF;

    @property
    def _pack_1_32(self):
        return ((self.noticeToggle & 0x1) << 31) | ((self.noticeCount & 0x7FFF) << 16) | ((self.dataDetails & 0xFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.noticeToggle = (value >> 31) & 0x1;
        self.noticeCount = (value >> 16) & 0x7FFF;
        self.dataDetails = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LHHLHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self._pack_0_32,self.trapNumber,self.issuerLID,self._pack_1_32,self.dataDetails2[0],self.dataDetails2[1],self.dataDetails2[2],self.dataDetails2[3],self.dataDetails2[4],self.dataDetails2[5],self.dataDetails2[6],self.dataDetails2[7],self.dataDetails2[8],self.dataDetails2[9],self.dataDetails2[10],self.dataDetails2[11],self.dataDetails2[12],self.dataDetails2[13],self.dataDetails2[14],self.dataDetails2[15],self.dataDetails2[16],self.dataDetails2[17],self.dataDetails2[18],self.dataDetails2[19],self.dataDetails2[20],self.dataDetails2[21],self.dataDetails2[22],self.dataDetails2[23],self.dataDetails2[24],self.dataDetails2[25]);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,self.trapNumber,self.issuerLID,self._pack_1_32,self.dataDetails2[0],self.dataDetails2[1],self.dataDetails2[2],self.dataDetails2[3],self.dataDetails2[4],self.dataDetails2[5],self.dataDetails2[6],self.dataDetails2[7],self.dataDetails2[8],self.dataDetails2[9],self.dataDetails2[10],self.dataDetails2[11],self.dataDetails2[12],self.dataDetails2[13],self.dataDetails2[14],self.dataDetails2[15],self.dataDetails2[16],self.dataDetails2[17],self.dataDetails2[18],self.dataDetails2[19],self.dataDetails2[20],self.dataDetails2[21],self.dataDetails2[22],self.dataDetails2[23],self.dataDetails2[24],self.dataDetails2[25],) = struct.unpack_from('>LHHLHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

class SAHeader(rdma.binstruct.BinStruct):
    '''SA Header (section 15.2.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus','data1','data2','SMKey','attributeOffset','reserved_368','componentMask');
    MAD_LENGTH = 56
    MAD_CLASS = 0x3
    MAD_CLASS_VERSION = 0x2
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1), ('SMKey',64,1), ('attributeOffset',16,1), ('reserved_368',16,1), ('componentMask',64,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.RMPPVersion = 0;
        self.RMPPType = 0;
        self.RRespTime = 0;
        self.RMPPFlags = 0;
        self.RMPPStatus = 0;
        self.data1 = 0;
        self.data2 = 0;
        self.SMKey = 0;
        self.attributeOffset = 0;
        self.reserved_368 = 0;
        self.componentMask = 0;

    @property
    def _pack_0_32(self):
        return ((self.RMPPVersion & 0xFF) << 24) | ((self.RMPPType & 0xFF) << 16) | ((self.RRespTime & 0x1F) << 11) | ((self.RMPPFlags & 0x7) << 8) | ((self.RMPPStatus & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RMPPVersion = (value >> 24) & 0xFF;
        self.RMPPType = (value >> 16) & 0xFF;
        self.RRespTime = (value >> 11) & 0x1F;
        self.RMPPFlags = (value >> 8) & 0x7;
        self.RMPPStatus = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBBBHHQHHLLLLQHHQ',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self.SMKey,self.attributeOffset,self.reserved_368,self.componentMask);

    def unpack_from(self,buffer,offset=0):
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self.SMKey,self.attributeOffset,self.reserved_368,self.componentMask,) = struct.unpack_from('>BBBBHHQHHLLLLQHHQ',buffer,offset+0);

class SAFormat(rdma.binstruct.BinFormat):
    '''SA Format (section 15.2.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus','data1','data2','SMKey','attributeOffset','reserved_368','componentMask','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x3
    MAD_CLASS_VERSION = 0x2
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1), ('SMKey',64,1), ('attributeOffset',16,1), ('reserved_368',16,1), ('componentMask',64,1), ('data',1600,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.RMPPVersion = 0;
        self.RMPPType = 0;
        self.RRespTime = 0;
        self.RMPPFlags = 0;
        self.RMPPStatus = 0;
        self.data1 = 0;
        self.data2 = 0;
        self.SMKey = 0;
        self.attributeOffset = 0;
        self.reserved_368 = 0;
        self.componentMask = 0;
        self.data = bytearray(200);

    @property
    def _pack_0_32(self):
        return ((self.RMPPVersion & 0xFF) << 24) | ((self.RMPPType & 0xFF) << 16) | ((self.RRespTime & 0x1F) << 11) | ((self.RMPPFlags & 0x7) << 8) | ((self.RMPPStatus & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RMPPVersion = (value >> 24) & 0xFF;
        self.RMPPType = (value >> 16) & 0xFF;
        self.RRespTime = (value >> 11) & 0x1F;
        self.RMPPFlags = (value >> 8) & 0x7;
        self.RMPPStatus = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 56:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHLLLLQHHQ',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self.SMKey,self.attributeOffset,self.reserved_368,self.componentMask);

    def unpack_from(self,buffer,offset=0):
        self.data = bytearray(buffer[offset + 56:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self.SMKey,self.attributeOffset,self.reserved_368,self.componentMask,) = struct.unpack_from('>BBBBHHQHHLLLLQHHQ',buffer,offset+0);

class SANodeRecord(rdma.binstruct.BinStruct):
    '''Container for NodeInfo (section 15.2.5.2)'''
    __slots__ = ('LID','reserved_16','nodeInfo','nodeDescription');
    MAD_LENGTH = 108
    MAD_ATTRIBUTE_ID = 0x11
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'nodeInfo.baseVersion':2, 'nodeInfo.classVersion':3, 'nodeInfo.nodeType':4, 'nodeInfo.numPorts':5, 'nodeInfo.systemImageGUID':6, 'nodeInfo.nodeGUID':7, 'nodeInfo.portGUID':8, 'nodeInfo.partitionCap':9, 'nodeInfo.deviceID':10, 'nodeInfo.revision':11, 'nodeInfo.localPortNum':12, 'nodeInfo.vendorID':13, 'nodeDescription.nodeString':14}
    MEMBERS = [('LID',16,1), ('reserved_16',16,1), ('nodeInfo',320,1), ('nodeDescription',512,1)]
    def __init__(self,*args):
        self.nodeInfo = SMPNodeInfo();
        self.nodeDescription = SMPNodeDescription();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved_16 = 0;
        self.nodeInfo = SMPNodeInfo();
        self.nodeDescription = SMPNodeDescription();

    def pack_into(self,buffer,offset=0):
        self.nodeInfo.pack_into(buffer,offset + 4);
        self.nodeDescription.pack_into(buffer,offset + 44);
        struct.pack_into('>HH',buffer,offset+0,self.LID,self.reserved_16);

    def unpack_from(self,buffer,offset=0):
        self.nodeInfo.unpack_from(buffer,offset + 4);
        self.nodeDescription.unpack_from(buffer,offset + 44);
        (self.LID,self.reserved_16,) = struct.unpack_from('>HH',buffer,offset+0);

class SAPortInfoRecord(rdma.binstruct.BinStruct):
    '''Container for PortInfo (section 15.2.5.3)'''
    __slots__ = ('endportLID','portNum','reserved_24','portInfo');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x12
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'endportLID':0, 'portNum':1, 'reserved_24':2, 'portInfo.MKey':3, 'portInfo.GIDPrefix':4, 'portInfo.LID':5, 'portInfo.masterSMLID':6, 'portInfo.capabilityMask':7, 'portInfo.diagCode':8, 'portInfo.MKeyLeasePeriod':9, 'portInfo.localPortNum':10, 'portInfo.linkWidthEnabled':11, 'portInfo.linkWidthSupported':12, 'portInfo.linkWidthActive':13, 'portInfo.linkSpeedSupported':14, 'portInfo.portState':15, 'portInfo.portPhysicalState':16, 'portInfo.linkDownDefaultState':17, 'portInfo.MKeyProtectBits':18, 'portInfo.reserved_274':19, 'portInfo.LMC':20, 'portInfo.linkSpeedActive':21, 'portInfo.linkSpeedEnabled':22, 'portInfo.neighborMTU':23, 'portInfo.masterSMSL':24, 'portInfo.VLCap':25, 'portInfo.initType':26, 'portInfo.VLHighLimit':27, 'portInfo.VLArbitrationHighCap':28, 'portInfo.VLArbitrationLowCap':29, 'portInfo.initTypeReply':30, 'portInfo.MTUCap':31, 'portInfo.VLStallCount':32, 'portInfo.HOQLife':33, 'portInfo.operationalVLs':34, 'portInfo.partitionEnforcementInbound':35, 'portInfo.partitionEnforcementOutbound':36, 'portInfo.filterRawInbound':37, 'portInfo.filterRawOutbound':38, 'portInfo.MKeyViolations':39, 'portInfo.PKeyViolations':40, 'portInfo.QKeyViolations':41, 'portInfo.GUIDCap':42, 'portInfo.clientReregister':43, 'portInfo.multicastPKeyTrapSuppressionEnabled':44, 'portInfo.subnetTimeOut':45, 'portInfo.reserved_416':46, 'portInfo.respTimeValue':47, 'portInfo.localPhyErrors':48, 'portInfo.overrunErrors':49, 'portInfo.maxCreditHint':50, 'portInfo.reserved_448':51, 'portInfo.linkRoundTripLatency':52, 'portInfo.capabilityMask2':53, 'portInfo.linkSpeedExtActive':54, 'portInfo.linkSpeedExtSupported':55, 'portInfo.reserved_504':56, 'portInfo.linkSpeedExtEnabled':57}
    MEMBERS = [('endportLID',16,1), ('portNum',8,1), ('reserved_24',8,1), ('portInfo',512,1)]
    def __init__(self,*args):
        self.portInfo = SMPPortInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.endportLID = 0;
        self.portNum = 0;
        self.reserved_24 = 0;
        self.portInfo = SMPPortInfo();

    def pack_into(self,buffer,offset=0):
        self.portInfo.pack_into(buffer,offset + 4);
        struct.pack_into('>HBB',buffer,offset+0,self.endportLID,self.portNum,self.reserved_24);

    def unpack_from(self,buffer,offset=0):
        self.portInfo.unpack_from(buffer,offset + 4);
        (self.endportLID,self.portNum,self.reserved_24,) = struct.unpack_from('>HBB',buffer,offset+0);

class SASLToVLMappingTableRecord(rdma.binstruct.BinStruct):
    '''Container for SLtoVLMappingTable entry (section 15.2.5.4)'''
    __slots__ = ('LID','inputPortNum','outputPortNum','reserved_32','SLToVLMappingTable');
    MAD_LENGTH = 16
    MAD_ATTRIBUTE_ID = 0x13
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'inputPortNum':1, 'outputPortNum':2, 'reserved_32':3, 'SLToVLMappingTable.SLtoVL':4}
    MEMBERS = [('LID',16,1), ('inputPortNum',8,1), ('outputPortNum',8,1), ('reserved_32',32,1), ('SLToVLMappingTable',64,1)]
    def __init__(self,*args):
        self.SLToVLMappingTable = SMPSLToVLMappingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.inputPortNum = 0;
        self.outputPortNum = 0;
        self.reserved_32 = 0;
        self.SLToVLMappingTable = SMPSLToVLMappingTable();

    def pack_into(self,buffer,offset=0):
        self.SLToVLMappingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HBBL',buffer,offset+0,self.LID,self.inputPortNum,self.outputPortNum,self.reserved_32);

    def unpack_from(self,buffer,offset=0):
        self.SLToVLMappingTable.unpack_from(buffer,offset + 8);
        (self.LID,self.inputPortNum,self.outputPortNum,self.reserved_32,) = struct.unpack_from('>HBBL',buffer,offset+0);

class SASwitchInfoRecord(rdma.binstruct.BinStruct):
    '''Container for SwitchInfo (section 15.2.5.5)'''
    __slots__ = ('LID','reserved_16','switchInfo');
    MAD_LENGTH = 24
    MAD_ATTRIBUTE_ID = 0x14
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'switchInfo.linearFDBCap':2, 'switchInfo.randomFDBCap':3, 'switchInfo.multicastFDBCap':4, 'switchInfo.linearFDBTop':5, 'switchInfo.defaultPort':6, 'switchInfo.defaultMulticastPrimaryPort':7, 'switchInfo.defaultMulticastNotPrimaryPort':8, 'switchInfo.lifeTimeValue':9, 'switchInfo.portStateChange':10, 'switchInfo.optimizedSLtoVLMappingProgramming':11, 'switchInfo.LIDsPerPort':12, 'switchInfo.partitionEnforcementCap':13, 'switchInfo.inboundEnforcementCap':14, 'switchInfo.outboundEnforcementCap':15, 'switchInfo.filterRawInboundCap':16, 'switchInfo.filterRawOutboundCap':17, 'switchInfo.enhancedPort0':18, 'switchInfo.reserved_133':19, 'switchInfo.reserved_136':20, 'switchInfo.multicastFDBTop':21}
    MEMBERS = [('LID',16,1), ('reserved_16',16,1), ('switchInfo',160,1)]
    def __init__(self,*args):
        self.switchInfo = SMPSwitchInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved_16 = 0;
        self.switchInfo = SMPSwitchInfo();

    def pack_into(self,buffer,offset=0):
        self.switchInfo.pack_into(buffer,offset + 4);
        struct.pack_into('>HH',buffer,offset+0,self.LID,self.reserved_16);

    def unpack_from(self,buffer,offset=0):
        self.switchInfo.unpack_from(buffer,offset + 4);
        (self.LID,self.reserved_16,) = struct.unpack_from('>HH',buffer,offset+0);

class SALinearForwardingTableRecord(rdma.binstruct.BinStruct):
    '''Container for LinearForwardingTable entry (section 15.2.5.6)'''
    __slots__ = ('LID','blockNum','reserved_32','linearForwardingTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x15
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved_32':2, 'linearForwardingTable.portBlock':3}
    MEMBERS = [('LID',16,1), ('blockNum',16,1), ('reserved_32',32,1), ('linearForwardingTable',512,1)]
    def __init__(self,*args):
        self.linearForwardingTable = SMPLinearForwardingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.reserved_32 = 0;
        self.linearForwardingTable = SMPLinearForwardingTable();

    def pack_into(self,buffer,offset=0):
        self.linearForwardingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HHL',buffer,offset+0,self.LID,self.blockNum,self.reserved_32);

    def unpack_from(self,buffer,offset=0):
        self.linearForwardingTable.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self.reserved_32,) = struct.unpack_from('>HHL',buffer,offset+0);

class SARandomForwardingTableRecord(rdma.binstruct.BinStruct):
    '''Container for RandomForwardingTable entry (section 15.2.5.7)'''
    __slots__ = ('LID','blockNum','reserved_32','randomForwardingTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x16
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved_32':2, 'randomForwardingTable.LIDPortBlock':3}
    MEMBERS = [('LID',16,1), ('blockNum',16,1), ('reserved_32',32,1), ('randomForwardingTable',512,1)]
    def __init__(self,*args):
        self.randomForwardingTable = SMPRandomForwardingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.reserved_32 = 0;
        self.randomForwardingTable = SMPRandomForwardingTable();

    def pack_into(self,buffer,offset=0):
        self.randomForwardingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HHL',buffer,offset+0,self.LID,self.blockNum,self.reserved_32);

    def unpack_from(self,buffer,offset=0):
        self.randomForwardingTable.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self.reserved_32,) = struct.unpack_from('>HHL',buffer,offset+0);

class SAMulticastForwardingTableRecord(rdma.binstruct.BinStruct):
    '''Container for MulticastForwardingTable entry (section 15.2.5.8)'''
    __slots__ = ('LID','reserved_16','position','blockNum','reserved_32','multicastForwardingTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x17
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'position':2, 'blockNum':3, 'reserved_32':4, 'multicastForwardingTable.portMaskBlock':5}
    MEMBERS = [('LID',16,1), ('reserved_16',2,1), ('position',4,1), ('blockNum',10,1), ('reserved_32',32,1), ('multicastForwardingTable',512,1)]
    def __init__(self,*args):
        self.multicastForwardingTable = SMPMulticastForwardingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved_16 = 0;
        self.position = 0;
        self.blockNum = 0;
        self.reserved_32 = 0;
        self.multicastForwardingTable = SMPMulticastForwardingTable();

    @property
    def _pack_0_32(self):
        return ((self.LID & 0xFFFF) << 16) | ((self.reserved_16 & 0x3) << 14) | ((self.position & 0xF) << 10) | ((self.blockNum & 0x3FF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.LID = (value >> 16) & 0xFFFF;
        self.reserved_16 = (value >> 14) & 0x3;
        self.position = (value >> 10) & 0xF;
        self.blockNum = (value >> 0) & 0x3FF;

    def pack_into(self,buffer,offset=0):
        self.multicastForwardingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>LL',buffer,offset+0,self._pack_0_32,self.reserved_32);

    def unpack_from(self,buffer,offset=0):
        self.multicastForwardingTable.unpack_from(buffer,offset + 8);
        (self._pack_0_32,self.reserved_32,) = struct.unpack_from('>LL',buffer,offset+0);

class SAVLArbitrationTableRecord(rdma.binstruct.BinStruct):
    '''Container for VLArbitrationTable entry (section 15.2.5.9)'''
    __slots__ = ('LID','outputPortNum','blockNum','reserved_32','VLArbitrationTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x36
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'outputPortNum':1, 'blockNum':2, 'reserved_32':3, 'VLArbitrationTable.VLWeightBlock':4}
    MEMBERS = [('LID',16,1), ('outputPortNum',8,1), ('blockNum',8,1), ('reserved_32',32,1), ('VLArbitrationTable',512,1)]
    def __init__(self,*args):
        self.VLArbitrationTable = SMPVLArbitrationTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.outputPortNum = 0;
        self.blockNum = 0;
        self.reserved_32 = 0;
        self.VLArbitrationTable = SMPVLArbitrationTable();

    def pack_into(self,buffer,offset=0):
        self.VLArbitrationTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HBBL',buffer,offset+0,self.LID,self.outputPortNum,self.blockNum,self.reserved_32);

    def unpack_from(self,buffer,offset=0):
        self.VLArbitrationTable.unpack_from(buffer,offset + 8);
        (self.LID,self.outputPortNum,self.blockNum,self.reserved_32,) = struct.unpack_from('>HBBL',buffer,offset+0);

class SASMInfoRecord(rdma.binstruct.BinStruct):
    '''Container for SMInfo (section 15.2.5.10)'''
    __slots__ = ('LID','reserved_16','SMInfo');
    MAD_LENGTH = 28
    MAD_ATTRIBUTE_ID = 0x18
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'SMInfo.GUID':2, 'SMInfo.SMKey':3, 'SMInfo.actCount':4, 'SMInfo.priority':5, 'SMInfo.SMState':6, 'SMInfo.reserved_168':7}
    MEMBERS = [('LID',16,1), ('reserved_16',16,1), ('SMInfo',192,1)]
    def __init__(self,*args):
        self.SMInfo = SMPSMInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved_16 = 0;
        self.SMInfo = SMPSMInfo();

    def pack_into(self,buffer,offset=0):
        self.SMInfo.pack_into(buffer,offset + 4);
        struct.pack_into('>HH',buffer,offset+0,self.LID,self.reserved_16);

    def unpack_from(self,buffer,offset=0):
        self.SMInfo.unpack_from(buffer,offset + 4);
        (self.LID,self.reserved_16,) = struct.unpack_from('>HH',buffer,offset+0);

class SAInformInfoRecord(rdma.binstruct.BinStruct):
    '''Container for InformInfo (section 15.2.5.12)'''
    __slots__ = ('subscriberGID','enumeration','reserved_144','reserved_160','informInfo','reserved_480');
    MAD_LENGTH = 80
    MAD_ATTRIBUTE_ID = 0xf3
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'subscriberGID':0, 'enumeration':1, 'reserved_144':2, 'informInfo.GID':3, 'informInfo.LIDRangeBegin':4, 'informInfo.LIDRangeEnd':5, 'informInfo.reserved_160':6, 'informInfo.isGeneric':7, 'informInfo.subscribe':8, 'informInfo.type':9, 'informInfo.trapNumber':10, 'informInfo.QPN':11, 'informInfo.reserved_248':12, 'informInfo.respTimeValue':13, 'informInfo.reserved_256':14, 'informInfo.producerType':15, 'reserved_480':16}
    MEMBERS = [('subscriberGID',128,1), ('enumeration',16,1), ('reserved_144',16,1), ('reserved_160',32,1), ('informInfo',288,1), ('reserved_480',160,1)]
    def __init__(self,*args):
        self.informInfo = MADInformInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.subscriberGID = IBA.GID();
        self.enumeration = 0;
        self.reserved_144 = 0;
        self.reserved_160 = 0;
        self.informInfo = MADInformInfo();
        self.reserved_480 = bytearray(20);

    def pack_into(self,buffer,offset=0):
        self.subscriberGID.pack_into(buffer,offset + 0);
        self.informInfo.pack_into(buffer,offset + 24);
        buffer[offset + 60:offset + 80] = self.reserved_480
        struct.pack_into('>HHL',buffer,offset+16,self.enumeration,self.reserved_144,self.reserved_160);

    def unpack_from(self,buffer,offset=0):
        self.subscriberGID = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        self.informInfo.unpack_from(buffer,offset + 24);
        self.reserved_480 = bytearray(buffer[offset + 60:offset + 80])
        (self.enumeration,self.reserved_144,self.reserved_160,) = struct.unpack_from('>HHL',buffer,offset+16);

class SALinkRecord(rdma.binstruct.BinStruct):
    '''Inter-node linkage information (section 15.2.5.13)'''
    __slots__ = ('fromLID','fromPort','toPort','toLID','reserved_48');
    MAD_LENGTH = 8
    MAD_ATTRIBUTE_ID = 0x20
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'fromLID':0, 'fromPort':1, 'toPort':2, 'toLID':3, 'reserved_48':4}
    MEMBERS = [('fromLID',16,1), ('fromPort',8,1), ('toPort',8,1), ('toLID',16,1), ('reserved_48',16,1)]
    def zero(self):
        self.fromLID = 0;
        self.fromPort = 0;
        self.toPort = 0;
        self.toLID = 0;
        self.reserved_48 = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HBBHH',buffer,offset+0,self.fromLID,self.fromPort,self.toPort,self.toLID,self.reserved_48);

    def unpack_from(self,buffer,offset=0):
        (self.fromLID,self.fromPort,self.toPort,self.toLID,self.reserved_48,) = struct.unpack_from('>HBBHH',buffer,offset+0);

class SAGUIDInfoRecord(rdma.binstruct.BinStruct):
    '''Container for port GUIDInfo (section 15.2.5.18)'''
    __slots__ = ('LID','blockNum','reserved_24','reserved_32','GUIDInfo');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x30
    MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved_24':2, 'reserved_32':3, 'GUIDInfo.GUIDBlock':4}
    MEMBERS = [('LID',16,1), ('blockNum',8,1), ('reserved_24',8,1), ('reserved_32',32,1), ('GUIDInfo',512,1)]
    def __init__(self,*args):
        self.GUIDInfo = SMPGUIDInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.reserved_24 = 0;
        self.reserved_32 = 0;
        self.GUIDInfo = SMPGUIDInfo();

    def pack_into(self,buffer,offset=0):
        self.GUIDInfo.pack_into(buffer,offset + 8);
        struct.pack_into('>HBBL',buffer,offset+0,self.LID,self.blockNum,self.reserved_24,self.reserved_32);

    def unpack_from(self,buffer,offset=0):
        self.GUIDInfo.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self.reserved_24,self.reserved_32,) = struct.unpack_from('>HBBL',buffer,offset+0);

class SAServiceRecord(rdma.binstruct.BinStruct):
    '''Information on advertised services (section 15.2.5.14)'''
    __slots__ = ('serviceID','serviceGID','servicePKey','reserved_208','serviceLease','serviceKey','serviceName','serviceData8','serviceData16','serviceData32','serviceData64');
    MAD_LENGTH = 176
    MAD_ATTRIBUTE_ID = 0x31
    MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    COMPONENT_MASK = {'serviceID':0, 'serviceGID':1, 'servicePKey':2, 'reserved_208':3, 'serviceLease':4, 'serviceKey':5, 'serviceName':6, 'serviceData8_0':7, 'serviceData8_1':8, 'serviceData8_2':9, 'serviceData8_3':10, 'serviceData8_4':11, 'serviceData8_5':12, 'serviceData8_6':13, 'serviceData8_7':14, 'serviceData8_8':15, 'serviceData8_9':16, 'serviceData8_10':17, 'serviceData8_11':18, 'serviceData8_12':19, 'serviceData8_13':20, 'serviceData8_14':21, 'serviceData8_15':22, 'serviceData16_0':23, 'serviceData16_1':24, 'serviceData16_2':25, 'serviceData16_3':26, 'serviceData16_4':27, 'serviceData16_5':28, 'serviceData16_6':29, 'serviceData16_7':30, 'serviceData32_0':31, 'serviceData32_1':32, 'serviceData32_2':33, 'serviceData32_3':34, 'serviceData64_0':35, 'serviceData64_1':36}
    MEMBERS = [('serviceID',64,1), ('serviceGID',128,1), ('servicePKey',16,1), ('reserved_208',16,1), ('serviceLease',32,1), ('serviceKey',128,1), ('serviceName',8,64), ('serviceData8',8,16), ('serviceData16',16,8), ('serviceData32',32,4), ('serviceData64',64,2)]
    def __init__(self,*args):
        self.serviceName = bytearray(64);
        self.serviceData8 = bytearray(16);
        self.serviceData16 = [0]*8;
        self.serviceData32 = [0]*4;
        self.serviceData64 = [0]*2;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.serviceID = 0;
        self.serviceGID = IBA.GID();
        self.servicePKey = 0;
        self.reserved_208 = 0;
        self.serviceLease = 0;
        self.serviceKey = IBA.GID();
        self.serviceName = bytearray(64);
        self.serviceData8 = bytearray(16);
        self.serviceData16 = [0]*8;
        self.serviceData32 = [0]*4;
        self.serviceData64 = [0]*2;

    def pack_into(self,buffer,offset=0):
        self.serviceGID.pack_into(buffer,offset + 8);
        self.serviceKey.pack_into(buffer,offset + 32);
        buffer[offset + 48:offset + 112] = self.serviceName
        buffer[offset + 112:offset + 128] = self.serviceData8
        rdma.binstruct.pack_array8(buffer,offset+160,64,2,self.serviceData64);
        struct.pack_into('>Q',buffer,offset+0,self.serviceID);
        struct.pack_into('>HHL',buffer,offset+24,self.servicePKey,self.reserved_208,self.serviceLease);
        struct.pack_into('>HHHHHHHHLLLL',buffer,offset+128,self.serviceData16[0],self.serviceData16[1],self.serviceData16[2],self.serviceData16[3],self.serviceData16[4],self.serviceData16[5],self.serviceData16[6],self.serviceData16[7],self.serviceData32[0],self.serviceData32[1],self.serviceData32[2],self.serviceData32[3]);

    def unpack_from(self,buffer,offset=0):
        self.serviceGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.serviceKey = IBA.GID(buffer[offset + 32:offset + 48],raw=True);
        self.serviceName = bytearray(buffer[offset + 48:offset + 112])
        self.serviceData8 = bytearray(buffer[offset + 112:offset + 128])
        rdma.binstruct.unpack_array8(buffer,offset+160,64,2,self.serviceData64);
        (self.serviceID,) = struct.unpack_from('>Q',buffer,offset+0);
        (self.servicePKey,self.reserved_208,self.serviceLease,) = struct.unpack_from('>HHL',buffer,offset+24);
        (self.serviceData16[0],self.serviceData16[1],self.serviceData16[2],self.serviceData16[3],self.serviceData16[4],self.serviceData16[5],self.serviceData16[6],self.serviceData16[7],self.serviceData32[0],self.serviceData32[1],self.serviceData32[2],self.serviceData32[3],) = struct.unpack_from('>HHHHHHHHLLLL',buffer,offset+128);

class SAPKeyTableRecord(rdma.binstruct.BinStruct):
    '''Container for P_Key Table (section 15.2.5.11)'''
    __slots__ = ('LID','blockNum','portNum','reserved_40','PKeyTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x33
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'portNum':2, 'reserved_40':3, 'PKeyTable.PKeyBlock':4}
    MEMBERS = [('LID',16,1), ('blockNum',16,1), ('portNum',8,1), ('reserved_40',24,1), ('PKeyTable',512,1)]
    def __init__(self,*args):
        self.PKeyTable = SMPPKeyTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.portNum = 0;
        self.reserved_40 = 0;
        self.PKeyTable = SMPPKeyTable();

    @property
    def _pack_0_32(self):
        return ((self.portNum & 0xFF) << 24) | ((self.reserved_40 & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.portNum = (value >> 24) & 0xFF;
        self.reserved_40 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.PKeyTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HHL',buffer,offset+0,self.LID,self.blockNum,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.PKeyTable.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self._pack_0_32,) = struct.unpack_from('>HHL',buffer,offset+0);

class SAPathRecord(rdma.binstruct.BinStruct):
    '''Information on paths through the subnet (section 15.2.5.16)'''
    __slots__ = ('serviceID','DGID','SGID','DLID','SLID','rawTraffic','reserved_353','flowLabel','hopLimit','TClass','reversible','numbPath','PKey','QOSClass','SL','MTUSelector','MTU','rateSelector','rate','packetLifeTimeSelector','packetLifeTime','preference','reversePathPKeyMemberBit','reserved_466','reserved_480');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x35
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'serviceID':0, 'serviceID56LSB':1, 'DGID':2, 'SGID':3, 'DLID':4, 'SLID':5, 'rawTraffic':6, 'reserved_353':7, 'flowLabel':8, 'hopLimit':9, 'TClass':10, 'reversible':11, 'numbPath':12, 'PKey':13, 'QOSClass':14, 'SL':15, 'MTUSelector':16, 'MTU':17, 'rateSelector':18, 'rate':19, 'packetLifeTimeSelector':20, 'packetLifeTime':21, 'preference':22, 'reversePathPKeyMemberBit':23, 'reserved_466':24, 'reserved_480':25}
    MEMBERS = [('serviceID',64,1), ('DGID',128,1), ('SGID',128,1), ('DLID',16,1), ('SLID',16,1), ('rawTraffic',1,1), ('reserved_353',3,1), ('flowLabel',20,1), ('hopLimit',8,1), ('TClass',8,1), ('reversible',1,1), ('numbPath',7,1), ('PKey',16,1), ('QOSClass',12,1), ('SL',4,1), ('MTUSelector',2,1), ('MTU',6,1), ('rateSelector',2,1), ('rate',6,1), ('packetLifeTimeSelector',2,1), ('packetLifeTime',6,1), ('preference',8,1), ('reversePathPKeyMemberBit',2,1), ('reserved_466',14,1), ('reserved_480',32,1)]
    def zero(self):
        self.serviceID = 0;
        self.DGID = IBA.GID();
        self.SGID = IBA.GID();
        self.DLID = 0;
        self.SLID = 0;
        self.rawTraffic = 0;
        self.reserved_353 = 0;
        self.flowLabel = 0;
        self.hopLimit = 0;
        self.TClass = 0;
        self.reversible = 0;
        self.numbPath = 0;
        self.PKey = 0;
        self.QOSClass = 0;
        self.SL = 0;
        self.MTUSelector = 0;
        self.MTU = 0;
        self.rateSelector = 0;
        self.rate = 0;
        self.packetLifeTimeSelector = 0;
        self.packetLifeTime = 0;
        self.preference = 0;
        self.reversePathPKeyMemberBit = 0;
        self.reserved_466 = 0;
        self.reserved_480 = 0;

    @property
    def _pack_0_32(self):
        return ((self.rawTraffic & 0x1) << 31) | ((self.reserved_353 & 0x7) << 28) | ((self.flowLabel & 0xFFFFF) << 8) | ((self.hopLimit & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.rawTraffic = (value >> 31) & 0x1;
        self.reserved_353 = (value >> 28) & 0x7;
        self.flowLabel = (value >> 8) & 0xFFFFF;
        self.hopLimit = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.TClass & 0xFF) << 24) | ((self.reversible & 0x1) << 23) | ((self.numbPath & 0x7F) << 16) | ((self.PKey & 0xFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.TClass = (value >> 24) & 0xFF;
        self.reversible = (value >> 23) & 0x1;
        self.numbPath = (value >> 16) & 0x7F;
        self.PKey = (value >> 0) & 0xFFFF;

    @property
    def _pack_2_32(self):
        return ((self.QOSClass & 0xFFF) << 20) | ((self.SL & 0xF) << 16) | ((self.MTUSelector & 0x3) << 14) | ((self.MTU & 0x3F) << 8) | ((self.rateSelector & 0x3) << 6) | ((self.rate & 0x3F) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.QOSClass = (value >> 20) & 0xFFF;
        self.SL = (value >> 16) & 0xF;
        self.MTUSelector = (value >> 14) & 0x3;
        self.MTU = (value >> 8) & 0x3F;
        self.rateSelector = (value >> 6) & 0x3;
        self.rate = (value >> 0) & 0x3F;

    @property
    def _pack_3_32(self):
        return ((self.packetLifeTimeSelector & 0x3) << 30) | ((self.packetLifeTime & 0x3F) << 24) | ((self.preference & 0xFF) << 16) | ((self.reversePathPKeyMemberBit & 0x3) << 14) | ((self.reserved_466 & 0x3FFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.packetLifeTimeSelector = (value >> 30) & 0x3;
        self.packetLifeTime = (value >> 24) & 0x3F;
        self.preference = (value >> 16) & 0xFF;
        self.reversePathPKeyMemberBit = (value >> 14) & 0x3;
        self.reserved_466 = (value >> 0) & 0x3FFF;

    def pack_into(self,buffer,offset=0):
        self.DGID.pack_into(buffer,offset + 8);
        self.SGID.pack_into(buffer,offset + 24);
        struct.pack_into('>Q',buffer,offset+0,self.serviceID);
        struct.pack_into('>HHLLLLL',buffer,offset+40,self.DLID,self.SLID,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self.reserved_480);

    def unpack_from(self,buffer,offset=0):
        self.DGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.SGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        (self.serviceID,) = struct.unpack_from('>Q',buffer,offset+0);
        (self.DLID,self.SLID,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self.reserved_480,) = struct.unpack_from('>HHLLLLL',buffer,offset+40);

class SAMCMemberRecord(rdma.binstruct.BinStruct):
    '''Multicast member attribute (section 15.2.5.17)'''
    __slots__ = ('MGID','portGID','QKey','MLID','MTUSelector','MTU','TClass','PKey','rateSelector','rate','packetLifeTimeSelector','packetLifeTime','SL','flowLabel','hopLimit','scope','joinState','proxyJoin','reserved_393');
    MAD_LENGTH = 52
    MAD_ATTRIBUTE_ID = 0x38
    MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    COMPONENT_MASK = {'MGID':0, 'portGID':1, 'QKey':2, 'MLID':3, 'MTUSelector':4, 'MTU':5, 'TClass':6, 'PKey':7, 'rateSelector':8, 'rate':9, 'packetLifeTimeSelector':10, 'packetLifeTime':11, 'SL':12, 'flowLabel':13, 'hopLimit':14, 'scope':15, 'joinState':16, 'proxyJoin':17, 'reserved_393':18}
    MEMBERS = [('MGID',128,1), ('portGID',128,1), ('QKey',32,1), ('MLID',16,1), ('MTUSelector',2,1), ('MTU',6,1), ('TClass',8,1), ('PKey',16,1), ('rateSelector',2,1), ('rate',6,1), ('packetLifeTimeSelector',2,1), ('packetLifeTime',6,1), ('SL',4,1), ('flowLabel',20,1), ('hopLimit',8,1), ('scope',4,1), ('joinState',4,1), ('proxyJoin',1,1), ('reserved_393',23,1)]
    def zero(self):
        self.MGID = IBA.GID();
        self.portGID = IBA.GID();
        self.QKey = 0;
        self.MLID = 0;
        self.MTUSelector = 0;
        self.MTU = 0;
        self.TClass = 0;
        self.PKey = 0;
        self.rateSelector = 0;
        self.rate = 0;
        self.packetLifeTimeSelector = 0;
        self.packetLifeTime = 0;
        self.SL = 0;
        self.flowLabel = 0;
        self.hopLimit = 0;
        self.scope = 0;
        self.joinState = 0;
        self.proxyJoin = 0;
        self.reserved_393 = 0;

    @property
    def _pack_0_32(self):
        return ((self.MLID & 0xFFFF) << 16) | ((self.MTUSelector & 0x3) << 14) | ((self.MTU & 0x3F) << 8) | ((self.TClass & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.MLID = (value >> 16) & 0xFFFF;
        self.MTUSelector = (value >> 14) & 0x3;
        self.MTU = (value >> 8) & 0x3F;
        self.TClass = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.PKey & 0xFFFF) << 16) | ((self.rateSelector & 0x3) << 14) | ((self.rate & 0x3F) << 8) | ((self.packetLifeTimeSelector & 0x3) << 6) | ((self.packetLifeTime & 0x3F) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.PKey = (value >> 16) & 0xFFFF;
        self.rateSelector = (value >> 14) & 0x3;
        self.rate = (value >> 8) & 0x3F;
        self.packetLifeTimeSelector = (value >> 6) & 0x3;
        self.packetLifeTime = (value >> 0) & 0x3F;

    @property
    def _pack_2_32(self):
        return ((self.SL & 0xF) << 28) | ((self.flowLabel & 0xFFFFF) << 8) | ((self.hopLimit & 0xFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.SL = (value >> 28) & 0xF;
        self.flowLabel = (value >> 8) & 0xFFFFF;
        self.hopLimit = (value >> 0) & 0xFF;

    @property
    def _pack_3_32(self):
        return ((self.scope & 0xF) << 28) | ((self.joinState & 0xF) << 24) | ((self.proxyJoin & 0x1) << 23) | ((self.reserved_393 & 0x7FFFFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.scope = (value >> 28) & 0xF;
        self.joinState = (value >> 24) & 0xF;
        self.proxyJoin = (value >> 23) & 0x1;
        self.reserved_393 = (value >> 0) & 0x7FFFFF;

    def pack_into(self,buffer,offset=0):
        self.MGID.pack_into(buffer,offset + 0);
        self.portGID.pack_into(buffer,offset + 16);
        struct.pack_into('>LLLLL',buffer,offset+32,self.QKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32);

    def unpack_from(self,buffer,offset=0):
        self.MGID = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        self.portGID = IBA.GID(buffer[offset + 16:offset + 32],raw=True);
        (self.QKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,) = struct.unpack_from('>LLLLL',buffer,offset+32);

class SATraceRecord(rdma.binstruct.BinStruct):
    '''Path trace information (section 15.2.5.19)'''
    __slots__ = ('GIDPrefix','IDGeneration','reserved_80','nodeType','nodeID','chassisID','entryPortID','exitPortID','entryPort','exitPort','reserved_368');
    MAD_LENGTH = 48
    MAD_ATTRIBUTE_ID = 0x39
    MAD_SUBNADMGETTRACETABLE = 0x13 # MAD_METHOD_GET_TRACE_TABLE
    COMPONENT_MASK = {'GIDPrefix':0, 'IDGeneration':1, 'reserved_80':2, 'nodeType':3, 'nodeID':4, 'chassisID':5, 'entryPortID':6, 'exitPortID':7, 'entryPort':8, 'exitPort':9, 'reserved_368':10}
    MEMBERS = [('GIDPrefix',64,1), ('IDGeneration',16,1), ('reserved_80',8,1), ('nodeType',8,1), ('nodeID',64,1), ('chassisID',64,1), ('entryPortID',64,1), ('exitPortID',64,1), ('entryPort',8,1), ('exitPort',8,1), ('reserved_368',16,1)]
    def zero(self):
        self.GIDPrefix = 0;
        self.IDGeneration = 0;
        self.reserved_80 = 0;
        self.nodeType = 0;
        self.nodeID = 0;
        self.chassisID = 0;
        self.entryPortID = 0;
        self.exitPortID = 0;
        self.entryPort = 0;
        self.exitPort = 0;
        self.reserved_368 = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QHBBQQQQBBH',buffer,offset+0,self.GIDPrefix,self.IDGeneration,self.reserved_80,self.nodeType,self.nodeID,self.chassisID,self.entryPortID,self.exitPortID,self.entryPort,self.exitPort,self.reserved_368);

    def unpack_from(self,buffer,offset=0):
        (self.GIDPrefix,self.IDGeneration,self.reserved_80,self.nodeType,self.nodeID,self.chassisID,self.entryPortID,self.exitPortID,self.entryPort,self.exitPort,self.reserved_368,) = struct.unpack_from('>QHBBQQQQBBH',buffer,offset+0);

class SAMultiPathRecord(rdma.binstruct.BinStruct):
    '''Request for multiple paths (section 15.2.5.20)'''
    __slots__ = ('rawTraffic','reserved_1','flowLabel','hopLimit','TClass','reversible','numbPath','PKey','reserved_64','SL','MTUSelector','MTU','rateSelector','rate','packetLifeTimeSelector','packetLifeTime','reserved_104','independenceSelector','reserved_114','SGIDCount','DGIDCount','reserved_136','reserved_160','SDGID');
    MAD_LENGTH = 40
    MAD_ATTRIBUTE_ID = 0x3a
    MAD_SUBNADMGETMULTI = 0x14 # MAD_METHOD_GET_MULTI
    COMPONENT_MASK = {'rawTraffic':0, 'reserved_1':1, 'flowLabel':2, 'hopLimit':3, 'TClass':4, 'reversible':5, 'numbPath':6, 'PKey':7, 'reserved_64':8, 'SL':9, 'MTUSelector':10, 'MTU':11, 'rateSelector':12, 'rate':13, 'packetLifeTimeSelector':14, 'packetLifeTime':15, 'reserved_104':16, 'independenceSelector':17, 'reserved_114':18, 'SGIDCount':19, 'DGIDCount':20, 'reserved_136':21, 'reserved_160':22, 'SDGID':23}
    MEMBERS = [('rawTraffic',1,1), ('reserved_1',3,1), ('flowLabel',20,1), ('hopLimit',8,1), ('TClass',8,1), ('reversible',1,1), ('numbPath',7,1), ('PKey',16,1), ('reserved_64',12,1), ('SL',4,1), ('MTUSelector',2,1), ('MTU',6,1), ('rateSelector',2,1), ('rate',6,1), ('packetLifeTimeSelector',2,1), ('packetLifeTime',6,1), ('reserved_104',8,1), ('independenceSelector',2,1), ('reserved_114',6,1), ('SGIDCount',8,1), ('DGIDCount',8,1), ('reserved_136',24,1), ('reserved_160',32,1), ('SDGID',128,1)]
    def zero(self):
        self.rawTraffic = 0;
        self.reserved_1 = 0;
        self.flowLabel = 0;
        self.hopLimit = 0;
        self.TClass = 0;
        self.reversible = 0;
        self.numbPath = 0;
        self.PKey = 0;
        self.reserved_64 = 0;
        self.SL = 0;
        self.MTUSelector = 0;
        self.MTU = 0;
        self.rateSelector = 0;
        self.rate = 0;
        self.packetLifeTimeSelector = 0;
        self.packetLifeTime = 0;
        self.reserved_104 = 0;
        self.independenceSelector = 0;
        self.reserved_114 = 0;
        self.SGIDCount = 0;
        self.DGIDCount = 0;
        self.reserved_136 = 0;
        self.reserved_160 = 0;
        self.SDGID = IBA.GID();

    @property
    def _pack_0_32(self):
        return ((self.rawTraffic & 0x1) << 31) | ((self.reserved_1 & 0x7) << 28) | ((self.flowLabel & 0xFFFFF) << 8) | ((self.hopLimit & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.rawTraffic = (value >> 31) & 0x1;
        self.reserved_1 = (value >> 28) & 0x7;
        self.flowLabel = (value >> 8) & 0xFFFFF;
        self.hopLimit = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.TClass & 0xFF) << 24) | ((self.reversible & 0x1) << 23) | ((self.numbPath & 0x7F) << 16) | ((self.PKey & 0xFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.TClass = (value >> 24) & 0xFF;
        self.reversible = (value >> 23) & 0x1;
        self.numbPath = (value >> 16) & 0x7F;
        self.PKey = (value >> 0) & 0xFFFF;

    @property
    def _pack_2_32(self):
        return ((self.reserved_64 & 0xFFF) << 20) | ((self.SL & 0xF) << 16) | ((self.MTUSelector & 0x3) << 14) | ((self.MTU & 0x3F) << 8) | ((self.rateSelector & 0x3) << 6) | ((self.rate & 0x3F) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved_64 = (value >> 20) & 0xFFF;
        self.SL = (value >> 16) & 0xF;
        self.MTUSelector = (value >> 14) & 0x3;
        self.MTU = (value >> 8) & 0x3F;
        self.rateSelector = (value >> 6) & 0x3;
        self.rate = (value >> 0) & 0x3F;

    @property
    def _pack_3_32(self):
        return ((self.packetLifeTimeSelector & 0x3) << 30) | ((self.packetLifeTime & 0x3F) << 24) | ((self.reserved_104 & 0xFF) << 16) | ((self.independenceSelector & 0x3) << 14) | ((self.reserved_114 & 0x3F) << 8) | ((self.SGIDCount & 0xFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.packetLifeTimeSelector = (value >> 30) & 0x3;
        self.packetLifeTime = (value >> 24) & 0x3F;
        self.reserved_104 = (value >> 16) & 0xFF;
        self.independenceSelector = (value >> 14) & 0x3;
        self.reserved_114 = (value >> 8) & 0x3F;
        self.SGIDCount = (value >> 0) & 0xFF;

    @property
    def _pack_4_32(self):
        return ((self.DGIDCount & 0xFF) << 24) | ((self.reserved_136 & 0xFFFFFF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.DGIDCount = (value >> 24) & 0xFF;
        self.reserved_136 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.SDGID.pack_into(buffer,offset + 24);
        struct.pack_into('>LLLLLL',buffer,offset+0,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32,self.reserved_160);

    def unpack_from(self,buffer,offset=0):
        self.SDGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        (self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32,self.reserved_160,) = struct.unpack_from('>LLLLLL',buffer,offset+0);

class SAServiceAssociationRecord(rdma.binstruct.BinStruct):
    '''ServiceRecord ServiceName/ServiceKey association (section 15.2.5.15)'''
    __slots__ = ('serviceKey','serviceName');
    MAD_LENGTH = 80
    MAD_ATTRIBUTE_ID = 0x3b
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'serviceKey':0, 'serviceName':1}
    MEMBERS = [('serviceKey',128,1), ('serviceName',8,64)]
    def __init__(self,*args):
        self.serviceName = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.serviceKey = IBA.GID();
        self.serviceName = bytearray(64);

    def pack_into(self,buffer,offset=0):
        self.serviceKey.pack_into(buffer,offset + 0);
        buffer[offset + 16:offset + 80] = self.serviceName

    def unpack_from(self,buffer,offset=0):
        self.serviceKey = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        self.serviceName = bytearray(buffer[offset + 16:offset + 80])

class PMFormat(rdma.binstruct.BinFormat):
    '''Performance Management MAD Format (section 16.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','reserved_192','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x4
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('reserved_192',320,1), ('data',1536,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.reserved_192 = bytearray(40);
        self.data = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 64] = self.reserved_192
        buffer[offset + 64:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self.reserved_192 = bytearray(buffer[offset + 24:offset + 64])
        self.data = bytearray(buffer[offset + 64:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

class PMPortSamplesCtl(rdma.binstruct.BinStruct):
    '''Port Performance Data Sampling Control (section 16.1.3.2)'''
    __slots__ = ('opCode','portSelect','tick','reserved_24','counterWidth','reserved_32','counterMask0','counterMask1','counterMask2','counterMask3','counterMask4','counterMask5','counterMask6','counterMask7','counterMask8','counterMask9','reserved_64','counterMask10','counterMask11','counterMask12','counterMask13','counterMask14','sampleMechanisms','reserved_88','sampleStatus','optionMask','vendorMask','sampleStart','sampleInterval','tag','counterSelect0','counterSelect1','counterSelect2','counterSelect3','counterSelect4','counterSelect5','counterSelect6','counterSelect7','counterSelect8','counterSelect9','counterSelect10','counterSelect11','counterSelect12','counterSelect13','counterSelect14','reserved_544','samplesOnlyOptionMask','reserved_640');
    MAD_LENGTH = 192
    MAD_ATTRIBUTE_ID = 0x10
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('tick',8,1), ('reserved_24',5,1), ('counterWidth',3,1), ('reserved_32',2,1), ('counterMask0',3,1), ('counterMask1',3,1), ('counterMask2',3,1), ('counterMask3',3,1), ('counterMask4',3,1), ('counterMask5',3,1), ('counterMask6',3,1), ('counterMask7',3,1), ('counterMask8',3,1), ('counterMask9',3,1), ('reserved_64',1,1), ('counterMask10',3,1), ('counterMask11',3,1), ('counterMask12',3,1), ('counterMask13',3,1), ('counterMask14',3,1), ('sampleMechanisms',8,1), ('reserved_88',6,1), ('sampleStatus',2,1), ('optionMask',64,1), ('vendorMask',64,1), ('sampleStart',32,1), ('sampleInterval',32,1), ('tag',16,1), ('counterSelect0',16,1), ('counterSelect1',16,1), ('counterSelect2',16,1), ('counterSelect3',16,1), ('counterSelect4',16,1), ('counterSelect5',16,1), ('counterSelect6',16,1), ('counterSelect7',16,1), ('counterSelect8',16,1), ('counterSelect9',16,1), ('counterSelect10',16,1), ('counterSelect11',16,1), ('counterSelect12',16,1), ('counterSelect13',16,1), ('counterSelect14',16,1), ('reserved_544',32,1), ('samplesOnlyOptionMask',64,1), ('reserved_640',896,1)]
    def zero(self):
        self.opCode = 0;
        self.portSelect = 0;
        self.tick = 0;
        self.reserved_24 = 0;
        self.counterWidth = 0;
        self.reserved_32 = 0;
        self.counterMask0 = 0;
        self.counterMask1 = 0;
        self.counterMask2 = 0;
        self.counterMask3 = 0;
        self.counterMask4 = 0;
        self.counterMask5 = 0;
        self.counterMask6 = 0;
        self.counterMask7 = 0;
        self.counterMask8 = 0;
        self.counterMask9 = 0;
        self.reserved_64 = 0;
        self.counterMask10 = 0;
        self.counterMask11 = 0;
        self.counterMask12 = 0;
        self.counterMask13 = 0;
        self.counterMask14 = 0;
        self.sampleMechanisms = 0;
        self.reserved_88 = 0;
        self.sampleStatus = 0;
        self.optionMask = 0;
        self.vendorMask = 0;
        self.sampleStart = 0;
        self.sampleInterval = 0;
        self.tag = 0;
        self.counterSelect0 = 0;
        self.counterSelect1 = 0;
        self.counterSelect2 = 0;
        self.counterSelect3 = 0;
        self.counterSelect4 = 0;
        self.counterSelect5 = 0;
        self.counterSelect6 = 0;
        self.counterSelect7 = 0;
        self.counterSelect8 = 0;
        self.counterSelect9 = 0;
        self.counterSelect10 = 0;
        self.counterSelect11 = 0;
        self.counterSelect12 = 0;
        self.counterSelect13 = 0;
        self.counterSelect14 = 0;
        self.reserved_544 = 0;
        self.samplesOnlyOptionMask = 0;
        self.reserved_640 = bytearray(112);

    @property
    def _pack_0_32(self):
        return ((self.opCode & 0xFF) << 24) | ((self.portSelect & 0xFF) << 16) | ((self.tick & 0xFF) << 8) | ((self.reserved_24 & 0x1F) << 3) | ((self.counterWidth & 0x7) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.opCode = (value >> 24) & 0xFF;
        self.portSelect = (value >> 16) & 0xFF;
        self.tick = (value >> 8) & 0xFF;
        self.reserved_24 = (value >> 3) & 0x1F;
        self.counterWidth = (value >> 0) & 0x7;

    @property
    def _pack_1_32(self):
        return ((self.reserved_32 & 0x3) << 30) | ((self.counterMask0 & 0x7) << 27) | ((self.counterMask1 & 0x7) << 24) | ((self.counterMask2 & 0x7) << 21) | ((self.counterMask3 & 0x7) << 18) | ((self.counterMask4 & 0x7) << 15) | ((self.counterMask5 & 0x7) << 12) | ((self.counterMask6 & 0x7) << 9) | ((self.counterMask7 & 0x7) << 6) | ((self.counterMask8 & 0x7) << 3) | ((self.counterMask9 & 0x7) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved_32 = (value >> 30) & 0x3;
        self.counterMask0 = (value >> 27) & 0x7;
        self.counterMask1 = (value >> 24) & 0x7;
        self.counterMask2 = (value >> 21) & 0x7;
        self.counterMask3 = (value >> 18) & 0x7;
        self.counterMask4 = (value >> 15) & 0x7;
        self.counterMask5 = (value >> 12) & 0x7;
        self.counterMask6 = (value >> 9) & 0x7;
        self.counterMask7 = (value >> 6) & 0x7;
        self.counterMask8 = (value >> 3) & 0x7;
        self.counterMask9 = (value >> 0) & 0x7;

    @property
    def _pack_2_32(self):
        return ((self.reserved_64 & 0x1) << 31) | ((self.counterMask10 & 0x7) << 28) | ((self.counterMask11 & 0x7) << 25) | ((self.counterMask12 & 0x7) << 22) | ((self.counterMask13 & 0x7) << 19) | ((self.counterMask14 & 0x7) << 16) | ((self.sampleMechanisms & 0xFF) << 8) | ((self.reserved_88 & 0x3F) << 2) | ((self.sampleStatus & 0x3) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved_64 = (value >> 31) & 0x1;
        self.counterMask10 = (value >> 28) & 0x7;
        self.counterMask11 = (value >> 25) & 0x7;
        self.counterMask12 = (value >> 22) & 0x7;
        self.counterMask13 = (value >> 19) & 0x7;
        self.counterMask14 = (value >> 16) & 0x7;
        self.sampleMechanisms = (value >> 8) & 0xFF;
        self.reserved_88 = (value >> 2) & 0x3F;
        self.sampleStatus = (value >> 0) & 0x3;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 80:offset + 192] = self.reserved_640
        struct.pack_into('>LLLQQLLHHHHHHHHHHHHHHHHLQ',buffer,offset+0,self._pack_0_32,self._pack_1_32,self._pack_2_32,self.optionMask,self.vendorMask,self.sampleStart,self.sampleInterval,self.tag,self.counterSelect0,self.counterSelect1,self.counterSelect2,self.counterSelect3,self.counterSelect4,self.counterSelect5,self.counterSelect6,self.counterSelect7,self.counterSelect8,self.counterSelect9,self.counterSelect10,self.counterSelect11,self.counterSelect12,self.counterSelect13,self.counterSelect14,self.reserved_544,self.samplesOnlyOptionMask);

    def unpack_from(self,buffer,offset=0):
        self.reserved_640 = bytearray(buffer[offset + 80:offset + 192])
        (self._pack_0_32,self._pack_1_32,self._pack_2_32,self.optionMask,self.vendorMask,self.sampleStart,self.sampleInterval,self.tag,self.counterSelect0,self.counterSelect1,self.counterSelect2,self.counterSelect3,self.counterSelect4,self.counterSelect5,self.counterSelect6,self.counterSelect7,self.counterSelect8,self.counterSelect9,self.counterSelect10,self.counterSelect11,self.counterSelect12,self.counterSelect13,self.counterSelect14,self.reserved_544,self.samplesOnlyOptionMask,) = struct.unpack_from('>LLLQQLLHHHHHHHHHHHHHHHHLQ',buffer,offset+0);

class PMPortSamplesRes(rdma.binstruct.BinStruct):
    '''Port Performance Data Sampling Results (section 16.1.3.4)'''
    __slots__ = ('tag','reserved_16','sampleStatus','counter');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x11
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('tag',16,1), ('reserved_16',14,1), ('sampleStatus',2,1), ('counter',32,15)]
    def __init__(self,*args):
        self.counter = [0]*15;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.tag = 0;
        self.reserved_16 = 0;
        self.sampleStatus = 0;
        self.counter = [0]*15;

    @property
    def _pack_0_32(self):
        return ((self.tag & 0xFFFF) << 16) | ((self.reserved_16 & 0x3FFF) << 2) | ((self.sampleStatus & 0x3) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.tag = (value >> 16) & 0xFFFF;
        self.reserved_16 = (value >> 2) & 0x3FFF;
        self.sampleStatus = (value >> 0) & 0x3;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LLLLLLLLLLLLLLLL',buffer,offset+0,self._pack_0_32,self.counter[0],self.counter[1],self.counter[2],self.counter[3],self.counter[4],self.counter[5],self.counter[6],self.counter[7],self.counter[8],self.counter[9],self.counter[10],self.counter[11],self.counter[12],self.counter[13],self.counter[14]);

    def unpack_from(self,buffer,offset=0):
        (self._pack_0_32,self.counter[0],self.counter[1],self.counter[2],self.counter[3],self.counter[4],self.counter[5],self.counter[6],self.counter[7],self.counter[8],self.counter[9],self.counter[10],self.counter[11],self.counter[12],self.counter[13],self.counter[14],) = struct.unpack_from('>LLLLLLLLLLLLLLLL',buffer,offset+0);

class PMPortCounters(rdma.binstruct.BinStruct):
    '''Port Basic Performance and Error Counters (section 16.1.3.5)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','symbolErrorCounter','linkErrorRecoveryCounter','linkDownedCounter','portRcvErrors','portRcvRemotePhysicalErrors','portRcvSwitchRelayErrors','portXmitDiscards','portXmitConstraintErrors','portRcvConstraintErrors','counterSelect2','localLinkIntegrityErrors','excessiveBufferOverrunErrors','reserved_160','VL15Dropped','portXmitData','portRcvData','portXmitPkts','portRcvPkts','portXmitWait');
    MAD_LENGTH = 44
    MAD_ATTRIBUTE_ID = 0x12
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('symbolErrorCounter',16,1), ('linkErrorRecoveryCounter',8,1), ('linkDownedCounter',8,1), ('portRcvErrors',16,1), ('portRcvRemotePhysicalErrors',16,1), ('portRcvSwitchRelayErrors',16,1), ('portXmitDiscards',16,1), ('portXmitConstraintErrors',8,1), ('portRcvConstraintErrors',8,1), ('counterSelect2',8,1), ('localLinkIntegrityErrors',4,1), ('excessiveBufferOverrunErrors',4,1), ('reserved_160',16,1), ('VL15Dropped',16,1), ('portXmitData',32,1), ('portRcvData',32,1), ('portXmitPkts',32,1), ('portRcvPkts',32,1), ('portXmitWait',32,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.symbolErrorCounter = 0;
        self.linkErrorRecoveryCounter = 0;
        self.linkDownedCounter = 0;
        self.portRcvErrors = 0;
        self.portRcvRemotePhysicalErrors = 0;
        self.portRcvSwitchRelayErrors = 0;
        self.portXmitDiscards = 0;
        self.portXmitConstraintErrors = 0;
        self.portRcvConstraintErrors = 0;
        self.counterSelect2 = 0;
        self.localLinkIntegrityErrors = 0;
        self.excessiveBufferOverrunErrors = 0;
        self.reserved_160 = 0;
        self.VL15Dropped = 0;
        self.portXmitData = 0;
        self.portRcvData = 0;
        self.portXmitPkts = 0;
        self.portRcvPkts = 0;
        self.portXmitWait = 0;

    @property
    def _pack_0_32(self):
        return ((self.portXmitConstraintErrors & 0xFF) << 24) | ((self.portRcvConstraintErrors & 0xFF) << 16) | ((self.counterSelect2 & 0xFF) << 8) | ((self.localLinkIntegrityErrors & 0xF) << 4) | ((self.excessiveBufferOverrunErrors & 0xF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.portXmitConstraintErrors = (value >> 24) & 0xFF;
        self.portRcvConstraintErrors = (value >> 16) & 0xFF;
        self.counterSelect2 = (value >> 8) & 0xFF;
        self.localLinkIntegrityErrors = (value >> 4) & 0xF;
        self.excessiveBufferOverrunErrors = (value >> 0) & 0xF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHBBHHHHLHHLLLLL',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.symbolErrorCounter,self.linkErrorRecoveryCounter,self.linkDownedCounter,self.portRcvErrors,self.portRcvRemotePhysicalErrors,self.portRcvSwitchRelayErrors,self.portXmitDiscards,self._pack_0_32,self.reserved_160,self.VL15Dropped,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portXmitWait);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.symbolErrorCounter,self.linkErrorRecoveryCounter,self.linkDownedCounter,self.portRcvErrors,self.portRcvRemotePhysicalErrors,self.portRcvSwitchRelayErrors,self.portXmitDiscards,self._pack_0_32,self.reserved_160,self.VL15Dropped,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portXmitWait,) = struct.unpack_from('>BBHHBBHHHHLHHLLLLL',buffer,offset+0);

class PMPortRcvErrorDetails(rdma.binstruct.BinStruct):
    '''Port Detailed Error Counters (section 16.1.4.1)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portLocalPhysicalErrors','portMalformedPacketErrors','portBufferOverrunErrors','portDLIDMappingErrors','portVLMappingErrors','portLoopingErrors');
    MAD_LENGTH = 16
    MAD_ATTRIBUTE_ID = 0x15
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portLocalPhysicalErrors',16,1), ('portMalformedPacketErrors',16,1), ('portBufferOverrunErrors',16,1), ('portDLIDMappingErrors',16,1), ('portVLMappingErrors',16,1), ('portLoopingErrors',16,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portLocalPhysicalErrors = 0;
        self.portMalformedPacketErrors = 0;
        self.portBufferOverrunErrors = 0;
        self.portDLIDMappingErrors = 0;
        self.portVLMappingErrors = 0;
        self.portLoopingErrors = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHH',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.portLocalPhysicalErrors,self.portMalformedPacketErrors,self.portBufferOverrunErrors,self.portDLIDMappingErrors,self.portVLMappingErrors,self.portLoopingErrors);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.portLocalPhysicalErrors,self.portMalformedPacketErrors,self.portBufferOverrunErrors,self.portDLIDMappingErrors,self.portVLMappingErrors,self.portLoopingErrors,) = struct.unpack_from('>BBHHHHHHH',buffer,offset+0);

class PMPortXmitDiscardDetails(rdma.binstruct.BinStruct):
    '''Port Transmit Discard Counters (section 16.1.4.2)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portInactiveDiscards','portNeighborMTUDiscards','portSwLifetimeLimitDiscards','portSwHOQLimitDiscards');
    MAD_LENGTH = 12
    MAD_ATTRIBUTE_ID = 0x16
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portInactiveDiscards',16,1), ('portNeighborMTUDiscards',16,1), ('portSwLifetimeLimitDiscards',16,1), ('portSwHOQLimitDiscards',16,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portInactiveDiscards = 0;
        self.portNeighborMTUDiscards = 0;
        self.portSwLifetimeLimitDiscards = 0;
        self.portSwHOQLimitDiscards = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHH',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.portInactiveDiscards,self.portNeighborMTUDiscards,self.portSwLifetimeLimitDiscards,self.portSwHOQLimitDiscards);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.portInactiveDiscards,self.portNeighborMTUDiscards,self.portSwLifetimeLimitDiscards,self.portSwHOQLimitDiscards,) = struct.unpack_from('>BBHHHHH',buffer,offset+0);

class PMPortOpRcvCounters(rdma.binstruct.BinStruct):
    '''Port Receive Counters per Op Code (section 16.1.4.3)'''
    __slots__ = ('opCode','portSelect','counterSelect','portOpRcvPkts','portOpRcvData');
    MAD_LENGTH = 12
    MAD_ATTRIBUTE_ID = 0x17
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portOpRcvPkts',32,1), ('portOpRcvData',32,1)]
    def zero(self):
        self.opCode = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portOpRcvPkts = 0;
        self.portOpRcvData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLL',buffer,offset+0,self.opCode,self.portSelect,self.counterSelect,self.portOpRcvPkts,self.portOpRcvData);

    def unpack_from(self,buffer,offset=0):
        (self.opCode,self.portSelect,self.counterSelect,self.portOpRcvPkts,self.portOpRcvData,) = struct.unpack_from('>BBHLL',buffer,offset+0);

class PMPortFlowCtlCounters(rdma.binstruct.BinStruct):
    '''Port Flow Control Counters (section 16.1.4.4)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portXmitFlowPkts','portRcvFlowPkts');
    MAD_LENGTH = 12
    MAD_ATTRIBUTE_ID = 0x18
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portXmitFlowPkts',32,1), ('portRcvFlowPkts',32,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portXmitFlowPkts = 0;
        self.portRcvFlowPkts = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLL',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.portXmitFlowPkts,self.portRcvFlowPkts);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.portXmitFlowPkts,self.portRcvFlowPkts,) = struct.unpack_from('>BBHLL',buffer,offset+0);

class PMPortVLOpPackets(rdma.binstruct.BinStruct):
    '''Port Packets Received per Op Code per VL (section 16.1.4.5)'''
    __slots__ = ('opCode','portSelect','counterSelect','portVLOpPackets');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x19
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLOpPackets',16,16)]
    def __init__(self,*args):
        self.portVLOpPackets = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.opCode = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portVLOpPackets = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0,self.opCode,self.portSelect,self.counterSelect,self.portVLOpPackets[0],self.portVLOpPackets[1],self.portVLOpPackets[2],self.portVLOpPackets[3],self.portVLOpPackets[4],self.portVLOpPackets[5],self.portVLOpPackets[6],self.portVLOpPackets[7],self.portVLOpPackets[8],self.portVLOpPackets[9],self.portVLOpPackets[10],self.portVLOpPackets[11],self.portVLOpPackets[12],self.portVLOpPackets[13],self.portVLOpPackets[14],self.portVLOpPackets[15]);

    def unpack_from(self,buffer,offset=0):
        (self.opCode,self.portSelect,self.counterSelect,self.portVLOpPackets[0],self.portVLOpPackets[1],self.portVLOpPackets[2],self.portVLOpPackets[3],self.portVLOpPackets[4],self.portVLOpPackets[5],self.portVLOpPackets[6],self.portVLOpPackets[7],self.portVLOpPackets[8],self.portVLOpPackets[9],self.portVLOpPackets[10],self.portVLOpPackets[11],self.portVLOpPackets[12],self.portVLOpPackets[13],self.portVLOpPackets[14],self.portVLOpPackets[15],) = struct.unpack_from('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0);

class PMPortVLOpData(rdma.binstruct.BinStruct):
    '''Port Kilobytes Received per Op Code per VL (section 16.1.4.6)'''
    __slots__ = ('opCode','portSelect','counterSelect','portVLOpData');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x1a
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLOpData',32,16)]
    def __init__(self,*args):
        self.portVLOpData = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.opCode = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portVLOpData = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0,self.opCode,self.portSelect,self.counterSelect,self.portVLOpData[0],self.portVLOpData[1],self.portVLOpData[2],self.portVLOpData[3],self.portVLOpData[4],self.portVLOpData[5],self.portVLOpData[6],self.portVLOpData[7],self.portVLOpData[8],self.portVLOpData[9],self.portVLOpData[10],self.portVLOpData[11],self.portVLOpData[12],self.portVLOpData[13],self.portVLOpData[14],self.portVLOpData[15]);

    def unpack_from(self,buffer,offset=0):
        (self.opCode,self.portSelect,self.counterSelect,self.portVLOpData[0],self.portVLOpData[1],self.portVLOpData[2],self.portVLOpData[3],self.portVLOpData[4],self.portVLOpData[5],self.portVLOpData[6],self.portVLOpData[7],self.portVLOpData[8],self.portVLOpData[9],self.portVLOpData[10],self.portVLOpData[11],self.portVLOpData[12],self.portVLOpData[13],self.portVLOpData[14],self.portVLOpData[15],) = struct.unpack_from('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0);

class PMPortVLXmitFlowCtlUpdateErrors(rdma.binstruct.BinStruct):
    '''Port Flow Control update errors per VL (section 16.1.4.7)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portVLXmitFlowCtlUpdateErrors');
    MAD_LENGTH = 8
    MAD_ATTRIBUTE_ID = 0x1b
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLXmitFlowCtlUpdateErrors',2,16)]
    def __init__(self,*args):
        self.portVLXmitFlowCtlUpdateErrors = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portVLXmitFlowCtlUpdateErrors = [0]*16;

    def pack_into(self,buffer,offset=0):
        rdma.binstruct.pack_array8(buffer,offset+4,2,16,self.portVLXmitFlowCtlUpdateErrors);
        struct.pack_into('>BBH',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect);

    def unpack_from(self,buffer,offset=0):
        rdma.binstruct.unpack_array8(buffer,offset+4,2,16,self.portVLXmitFlowCtlUpdateErrors);
        (self.reserved_0,self.portSelect,self.counterSelect,) = struct.unpack_from('>BBH',buffer,offset+0);

class PMPortVLXmitWaitCounters(rdma.binstruct.BinStruct):
    '''Port Ticks Waiting to Transmit Counters per VL (section 16.1.4.8)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portVLXmitWait');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x1c
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLXmitWait',16,16)]
    def __init__(self,*args):
        self.portVLXmitWait = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portVLXmitWait = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.portVLXmitWait[0],self.portVLXmitWait[1],self.portVLXmitWait[2],self.portVLXmitWait[3],self.portVLXmitWait[4],self.portVLXmitWait[5],self.portVLXmitWait[6],self.portVLXmitWait[7],self.portVLXmitWait[8],self.portVLXmitWait[9],self.portVLXmitWait[10],self.portVLXmitWait[11],self.portVLXmitWait[12],self.portVLXmitWait[13],self.portVLXmitWait[14],self.portVLXmitWait[15]);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.portVLXmitWait[0],self.portVLXmitWait[1],self.portVLXmitWait[2],self.portVLXmitWait[3],self.portVLXmitWait[4],self.portVLXmitWait[5],self.portVLXmitWait[6],self.portVLXmitWait[7],self.portVLXmitWait[8],self.portVLXmitWait[9],self.portVLXmitWait[10],self.portVLXmitWait[11],self.portVLXmitWait[12],self.portVLXmitWait[13],self.portVLXmitWait[14],self.portVLXmitWait[15],) = struct.unpack_from('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0);

class PMSwPortVLCongestion(rdma.binstruct.BinStruct):
    '''Switch Port Congestion per VL (section 16.1.4.9)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','swPortVLCongestion');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x30
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('swPortVLCongestion',16,16)]
    def __init__(self,*args):
        self.swPortVLCongestion = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.swPortVLCongestion = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.swPortVLCongestion[0],self.swPortVLCongestion[1],self.swPortVLCongestion[2],self.swPortVLCongestion[3],self.swPortVLCongestion[4],self.swPortVLCongestion[5],self.swPortVLCongestion[6],self.swPortVLCongestion[7],self.swPortVLCongestion[8],self.swPortVLCongestion[9],self.swPortVLCongestion[10],self.swPortVLCongestion[11],self.swPortVLCongestion[12],self.swPortVLCongestion[13],self.swPortVLCongestion[14],self.swPortVLCongestion[15]);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.swPortVLCongestion[0],self.swPortVLCongestion[1],self.swPortVLCongestion[2],self.swPortVLCongestion[3],self.swPortVLCongestion[4],self.swPortVLCongestion[5],self.swPortVLCongestion[6],self.swPortVLCongestion[7],self.swPortVLCongestion[8],self.swPortVLCongestion[9],self.swPortVLCongestion[10],self.swPortVLCongestion[11],self.swPortVLCongestion[12],self.swPortVLCongestion[13],self.swPortVLCongestion[14],self.swPortVLCongestion[15],) = struct.unpack_from('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0);

class PMPortSamplesResExt(rdma.binstruct.BinStruct):
    '''Extended Port Samples Result (section 16.1.4.10)'''
    __slots__ = ('tag','reserved_16','sampleStatus','extendedWidth','reserved_34','counter');
    MAD_LENGTH = 128
    MAD_ATTRIBUTE_ID = 0x1e
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('tag',16,1), ('reserved_16',14,1), ('sampleStatus',2,1), ('extendedWidth',2,1), ('reserved_34',30,1), ('counter',64,15)]
    def __init__(self,*args):
        self.counter = [0]*15;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.tag = 0;
        self.reserved_16 = 0;
        self.sampleStatus = 0;
        self.extendedWidth = 0;
        self.reserved_34 = 0;
        self.counter = [0]*15;

    @property
    def _pack_0_32(self):
        return ((self.tag & 0xFFFF) << 16) | ((self.reserved_16 & 0x3FFF) << 2) | ((self.sampleStatus & 0x3) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.tag = (value >> 16) & 0xFFFF;
        self.reserved_16 = (value >> 2) & 0x3FFF;
        self.sampleStatus = (value >> 0) & 0x3;

    @property
    def _pack_1_32(self):
        return ((self.extendedWidth & 0x3) << 30) | ((self.reserved_34 & 0x3FFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.extendedWidth = (value >> 30) & 0x3;
        self.reserved_34 = (value >> 0) & 0x3FFFFFFF;

    def pack_into(self,buffer,offset=0):
        rdma.binstruct.pack_array8(buffer,offset+8,64,15,self.counter);
        struct.pack_into('>LL',buffer,offset+0,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        rdma.binstruct.unpack_array8(buffer,offset+8,64,15,self.counter);
        (self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>LL',buffer,offset+0);

class PMPortCountersExt(rdma.binstruct.BinStruct):
    '''Extended Port Counters (section 16.1.4.11)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','reserved_32','portXmitData','portRcvData','portXmitPkts','portRcvPkts','portUnicastXmitPkts','portUnicastRcvPkts','portMulticastXmitPkts','portMulticastRcvPkts');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x1d
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('reserved_32',32,1), ('portXmitData',64,1), ('portRcvData',64,1), ('portXmitPkts',64,1), ('portRcvPkts',64,1), ('portUnicastXmitPkts',64,1), ('portUnicastRcvPkts',64,1), ('portMulticastXmitPkts',64,1), ('portMulticastRcvPkts',64,1)]
    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.reserved_32 = 0;
        self.portXmitData = 0;
        self.portRcvData = 0;
        self.portXmitPkts = 0;
        self.portRcvPkts = 0;
        self.portUnicastXmitPkts = 0;
        self.portUnicastRcvPkts = 0;
        self.portMulticastXmitPkts = 0;
        self.portMulticastRcvPkts = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLQQQQQQQQ',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.reserved_32,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portUnicastXmitPkts,self.portUnicastRcvPkts,self.portMulticastXmitPkts,self.portMulticastRcvPkts);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.reserved_32,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portUnicastXmitPkts,self.portUnicastRcvPkts,self.portMulticastXmitPkts,self.portMulticastRcvPkts,) = struct.unpack_from('>BBHLQQQQQQQQ',buffer,offset+0);

class PMPortXmitDataSL(rdma.binstruct.BinStruct):
    '''Transmit SL Port Counters (section A13.6.5)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portXmitDataSL');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x36
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portXmitDataSL',32,16)]
    def __init__(self,*args):
        self.portXmitDataSL = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portXmitDataSL = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.portXmitDataSL[0],self.portXmitDataSL[1],self.portXmitDataSL[2],self.portXmitDataSL[3],self.portXmitDataSL[4],self.portXmitDataSL[5],self.portXmitDataSL[6],self.portXmitDataSL[7],self.portXmitDataSL[8],self.portXmitDataSL[9],self.portXmitDataSL[10],self.portXmitDataSL[11],self.portXmitDataSL[12],self.portXmitDataSL[13],self.portXmitDataSL[14],self.portXmitDataSL[15]);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.portXmitDataSL[0],self.portXmitDataSL[1],self.portXmitDataSL[2],self.portXmitDataSL[3],self.portXmitDataSL[4],self.portXmitDataSL[5],self.portXmitDataSL[6],self.portXmitDataSL[7],self.portXmitDataSL[8],self.portXmitDataSL[9],self.portXmitDataSL[10],self.portXmitDataSL[11],self.portXmitDataSL[12],self.portXmitDataSL[13],self.portXmitDataSL[14],self.portXmitDataSL[15],) = struct.unpack_from('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0);

class PMPortRcvDataSL(rdma.binstruct.BinStruct):
    '''Receive SL Port Counters (section A13.6.5)'''
    __slots__ = ('reserved_0','portSelect','counterSelect','portRcvDataSL');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x37
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portRcvDataSL',32,16)]
    def __init__(self,*args):
        self.portRcvDataSL = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved_0 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portRcvDataSL = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0,self.reserved_0,self.portSelect,self.counterSelect,self.portRcvDataSL[0],self.portRcvDataSL[1],self.portRcvDataSL[2],self.portRcvDataSL[3],self.portRcvDataSL[4],self.portRcvDataSL[5],self.portRcvDataSL[6],self.portRcvDataSL[7],self.portRcvDataSL[8],self.portRcvDataSL[9],self.portRcvDataSL[10],self.portRcvDataSL[11],self.portRcvDataSL[12],self.portRcvDataSL[13],self.portRcvDataSL[14],self.portRcvDataSL[15]);

    def unpack_from(self,buffer,offset=0):
        (self.reserved_0,self.portSelect,self.counterSelect,self.portRcvDataSL[0],self.portRcvDataSL[1],self.portRcvDataSL[2],self.portRcvDataSL[3],self.portRcvDataSL[4],self.portRcvDataSL[5],self.portRcvDataSL[6],self.portRcvDataSL[7],self.portRcvDataSL[8],self.portRcvDataSL[9],self.portRcvDataSL[10],self.portRcvDataSL[11],self.portRcvDataSL[12],self.portRcvDataSL[13],self.portRcvDataSL[14],self.portRcvDataSL[15],) = struct.unpack_from('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0);

class DMFormat(rdma.binstruct.BinFormat):
    '''Device Management MAD Format (section 16.3.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','reserved_192','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x6
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('reserved_192',320,1), ('data',1536,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.reserved_192 = bytearray(40);
        self.data = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 64] = self.reserved_192
        buffer[offset + 64:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self.reserved_192 = bytearray(buffer[offset + 24:offset + 64])
        self.data = bytearray(buffer[offset + 64:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

class DMServiceEntry(rdma.binstruct.BinStruct):
    '''Service Entry (section 16.3.3)'''
    __slots__ = ('serviceName','serviceID');
    MAD_LENGTH = 48
    MEMBERS = [('serviceName',8,40), ('serviceID',64,1)]
    def __init__(self,*args):
        self.serviceName = bytearray(40);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.serviceName = bytearray(40);
        self.serviceID = 0;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 40] = self.serviceName
        struct.pack_into('>Q',buffer,offset+40,self.serviceID);

    def unpack_from(self,buffer,offset=0):
        self.serviceName = bytearray(buffer[offset + 0:offset + 40])
        (self.serviceID,) = struct.unpack_from('>Q',buffer,offset+40);

class DMIOUnitInfo(rdma.binstruct.BinStruct):
    '''List of all I/O Controllers in a I/O Unit (section 16.3.3.3)'''
    __slots__ = ('changeID','maxControllers','reserved_24','diagDeviceID','optionROM','controllerList');
    MAD_LENGTH = 132
    MAD_ATTRIBUTE_ID = 0x10
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('changeID',16,1), ('maxControllers',8,1), ('reserved_24',6,1), ('diagDeviceID',1,1), ('optionROM',1,1), ('controllerList',1024,1)]
    def zero(self):
        self.changeID = 0;
        self.maxControllers = 0;
        self.reserved_24 = 0;
        self.diagDeviceID = 0;
        self.optionROM = 0;
        self.controllerList = bytearray(128);

    @property
    def _pack_0_32(self):
        return ((self.changeID & 0xFFFF) << 16) | ((self.maxControllers & 0xFF) << 8) | ((self.reserved_24 & 0x3F) << 2) | ((self.diagDeviceID & 0x1) << 1) | ((self.optionROM & 0x1) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.changeID = (value >> 16) & 0xFFFF;
        self.maxControllers = (value >> 8) & 0xFF;
        self.reserved_24 = (value >> 2) & 0x3F;
        self.diagDeviceID = (value >> 1) & 0x1;
        self.optionROM = (value >> 0) & 0x1;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 4:offset + 132] = self.controllerList
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self.controllerList = bytearray(buffer[offset + 4:offset + 132])
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

class DMIOControllerProfile(rdma.binstruct.BinStruct):
    '''I/O Controller Profile Information (section 16.3.3.4)'''
    __slots__ = ('GUID','vendorID','reserved_88','deviceID','deviceVersion','reserved_144','subsystemVendorID','reserved_184','subsystemID','IOClass','IOSubclass','protocol','protocolVersion','reserved_288','reserved_304','sendMessageDepth','reserved_336','RDMAReadDepth','sendMessageSize','RDMATransferSize','controllerOperationsMask','reserved_424','serviceEntries','reserved_440','reserved_448','IDString');
    MAD_LENGTH = 128
    MAD_ATTRIBUTE_ID = 0x11
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('GUID',64,1), ('vendorID',24,1), ('reserved_88',8,1), ('deviceID',32,1), ('deviceVersion',16,1), ('reserved_144',16,1), ('subsystemVendorID',24,1), ('reserved_184',8,1), ('subsystemID',32,1), ('IOClass',16,1), ('IOSubclass',16,1), ('protocol',16,1), ('protocolVersion',16,1), ('reserved_288',16,1), ('reserved_304',16,1), ('sendMessageDepth',16,1), ('reserved_336',8,1), ('RDMAReadDepth',8,1), ('sendMessageSize',32,1), ('RDMATransferSize',32,1), ('controllerOperationsMask',8,1), ('reserved_424',8,1), ('serviceEntries',8,1), ('reserved_440',8,1), ('reserved_448',64,1), ('IDString',8,64)]
    def __init__(self,*args):
        self.IDString = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.GUID = IBA.GUID();
        self.vendorID = 0;
        self.reserved_88 = 0;
        self.deviceID = 0;
        self.deviceVersion = 0;
        self.reserved_144 = 0;
        self.subsystemVendorID = 0;
        self.reserved_184 = 0;
        self.subsystemID = 0;
        self.IOClass = 0;
        self.IOSubclass = 0;
        self.protocol = 0;
        self.protocolVersion = 0;
        self.reserved_288 = 0;
        self.reserved_304 = 0;
        self.sendMessageDepth = 0;
        self.reserved_336 = 0;
        self.RDMAReadDepth = 0;
        self.sendMessageSize = 0;
        self.RDMATransferSize = 0;
        self.controllerOperationsMask = 0;
        self.reserved_424 = 0;
        self.serviceEntries = 0;
        self.reserved_440 = 0;
        self.reserved_448 = 0;
        self.IDString = bytearray(64);

    @property
    def _pack_0_32(self):
        return ((self.vendorID & 0xFFFFFF) << 8) | ((self.reserved_88 & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.vendorID = (value >> 8) & 0xFFFFFF;
        self.reserved_88 = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.subsystemVendorID & 0xFFFFFF) << 8) | ((self.reserved_184 & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.subsystemVendorID = (value >> 8) & 0xFFFFFF;
        self.reserved_184 = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        self.GUID.pack_into(buffer,offset + 0);
        buffer[offset + 64:offset + 128] = self.IDString
        struct.pack_into('>LLHHLLHHHHHHHBBLLBBBBQ',buffer,offset+8,self._pack_0_32,self.deviceID,self.deviceVersion,self.reserved_144,self._pack_1_32,self.subsystemID,self.IOClass,self.IOSubclass,self.protocol,self.protocolVersion,self.reserved_288,self.reserved_304,self.sendMessageDepth,self.reserved_336,self.RDMAReadDepth,self.sendMessageSize,self.RDMATransferSize,self.controllerOperationsMask,self.reserved_424,self.serviceEntries,self.reserved_440,self.reserved_448);

    def unpack_from(self,buffer,offset=0):
        self.GUID = IBA.GUID(buffer[offset + 0:offset + 8],raw=True);
        self.IDString = bytearray(buffer[offset + 64:offset + 128])
        (self._pack_0_32,self.deviceID,self.deviceVersion,self.reserved_144,self._pack_1_32,self.subsystemID,self.IOClass,self.IOSubclass,self.protocol,self.protocolVersion,self.reserved_288,self.reserved_304,self.sendMessageDepth,self.reserved_336,self.RDMAReadDepth,self.sendMessageSize,self.RDMATransferSize,self.controllerOperationsMask,self.reserved_424,self.serviceEntries,self.reserved_440,self.reserved_448,) = struct.unpack_from('>LLHHLLHHHHHHHBBLLBBBBQ',buffer,offset+8);

class DMServiceEntries(rdma.binstruct.BinStruct):
    '''List of Supported Services and Their Associated Service IDs (section 16.3.3.5)'''
    __slots__ = ('serviceEntry');
    MAD_LENGTH = 192
    MAD_ATTRIBUTE_ID = 0x12
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('serviceEntry',384,4)]
    def __init__(self,*args):
        self.serviceEntry = [DMServiceEntry() for I in range(4)];
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.serviceEntry = [DMServiceEntry() for I in range(4)];

    def pack_into(self,buffer,offset=0):
        self.serviceEntry[0].pack_into(buffer,offset + 0);
        self.serviceEntry[1].pack_into(buffer,offset + 48);
        self.serviceEntry[2].pack_into(buffer,offset + 96);
        self.serviceEntry[3].pack_into(buffer,offset + 144);

    def unpack_from(self,buffer,offset=0):
        self.serviceEntry[0].unpack_from(buffer,offset + 0);
        self.serviceEntry[1].unpack_from(buffer,offset + 48);
        self.serviceEntry[2].unpack_from(buffer,offset + 96);
        self.serviceEntry[3].unpack_from(buffer,offset + 144);

class DMDiagnosticTimeout(rdma.binstruct.BinStruct):
    '''Get the Maximum Time for Completion of a Diagnostic Test (section 16.3.3.6)'''
    __slots__ = ('maxDiagTime');
    MAD_LENGTH = 4
    MAD_ATTRIBUTE_ID = 0x20
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('maxDiagTime',32,1)]
    def zero(self):
        self.maxDiagTime = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self.maxDiagTime);

    def unpack_from(self,buffer,offset=0):
        (self.maxDiagTime,) = struct.unpack_from('>L',buffer,offset+0);

class DMPrepareToTest(rdma.binstruct.BinStruct):
    '''Prepare Device for Test (section 16.3.3.7)'''
    __slots__ = ();
    MAD_LENGTH = 0
    MAD_ATTRIBUTE_ID = 0x21
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    MEMBERS = []
    def pack_into(self,buffer,offset=0):
        return None;

    def unpack_from(self,buffer,offset=0):
        return;

class DMTestDeviceOnce(rdma.binstruct.BinStruct):
    '''Test Device Once (section 16.3.3.8)'''
    __slots__ = ();
    MAD_LENGTH = 0
    MAD_ATTRIBUTE_ID = 0x22
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    MEMBERS = []
    def pack_into(self,buffer,offset=0):
        return None;

    def unpack_from(self,buffer,offset=0):
        return;

class DMTestDeviceLoop(rdma.binstruct.BinStruct):
    '''Test Device Continuously (section 16.3.3.9)'''
    __slots__ = ();
    MAD_LENGTH = 0
    MAD_ATTRIBUTE_ID = 0x23
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    MEMBERS = []
    def pack_into(self,buffer,offset=0):
        return None;

    def unpack_from(self,buffer,offset=0):
        return;

class DMDiagCode(rdma.binstruct.BinStruct):
    '''Vendor-Specific Device Diagnostic Information (section 16.3.3.10)'''
    __slots__ = ('diagCode','reserved_16');
    MAD_LENGTH = 4
    MAD_ATTRIBUTE_ID = 0x24
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MEMBERS = [('diagCode',16,1), ('reserved_16',16,1)]
    def zero(self):
        self.diagCode = 0;
        self.reserved_16 = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HH',buffer,offset+0,self.diagCode,self.reserved_16);

    def unpack_from(self,buffer,offset=0):
        (self.diagCode,self.reserved_16,) = struct.unpack_from('>HH',buffer,offset+0);

class SNMPFormat(rdma.binstruct.BinFormat):
    '''SNMP Tunneling MAD Format (section 16.4.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','reserved_192','RAddress','payloadLength','segmentNumber','sourceLID','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x8
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('reserved_192',256,1), ('RAddress',32,1), ('payloadLength',8,1), ('segmentNumber',8,1), ('sourceLID',16,1), ('data',1536,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.reserved_192 = bytearray(32);
        self.RAddress = 0;
        self.payloadLength = 0;
        self.segmentNumber = 0;
        self.sourceLID = 0;
        self.data = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 56] = self.reserved_192
        buffer[offset + 64:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);
        struct.pack_into('>LBBH',buffer,offset+56,self.RAddress,self.payloadLength,self.segmentNumber,self.sourceLID);

    def unpack_from(self,buffer,offset=0):
        self.reserved_192 = bytearray(buffer[offset + 24:offset + 56])
        self.data = bytearray(buffer[offset + 64:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);
        (self.RAddress,self.payloadLength,self.segmentNumber,self.sourceLID,) = struct.unpack_from('>LBBH',buffer,offset+56);

class SNMPCommunityInfo(rdma.binstruct.BinStruct):
    '''Community Name Data Store (section 16.4.3.2)'''
    __slots__ = ('communityName');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x10
    MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('communityName',8,64)]
    def __init__(self,*args):
        self.communityName = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.communityName = bytearray(64);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 64] = self.communityName

    def unpack_from(self,buffer,offset=0):
        self.communityName = bytearray(buffer[offset + 0:offset + 64])

class SNMPPDUInfo(rdma.binstruct.BinStruct):
    '''Data Segment (section 16.4.3.3)'''
    __slots__ = ('PDUData');
    MAD_LENGTH = 192
    MAD_ATTRIBUTE_ID = 0x11
    MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND
    MEMBERS = [('PDUData',1536,1)]
    def zero(self):
        self.PDUData = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 192] = self.PDUData

    def unpack_from(self,buffer,offset=0):
        self.PDUData = bytearray(buffer[offset + 0:offset + 192])

class VendFormat(rdma.binstruct.BinFormat):
    '''Vendor Specific Management MAD Format (section 16.5.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x9
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('data',1856,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.data = bytearray(232);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self.data = bytearray(buffer[offset + 24:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

class VendOUIFormat(rdma.binstruct.BinFormat):
    '''Vendor Specific Management MAD Format with OUI (section 16.5.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved_144','attributeModifier','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus','data1','data2','reserved_288','OUI','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x30
    MAD_CLASS_VERSION = 0x1
    MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1), ('reserved_288',8,1), ('OUI',24,1), ('data',1728,1)]
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved_144 = 0;
        self.attributeModifier = 0;
        self.RMPPVersion = 0;
        self.RMPPType = 0;
        self.RRespTime = 0;
        self.RMPPFlags = 0;
        self.RMPPStatus = 0;
        self.data1 = 0;
        self.data2 = 0;
        self.reserved_288 = 0;
        self.OUI = 0;
        self.data = bytearray(216);

    @property
    def _pack_0_32(self):
        return ((self.RMPPVersion & 0xFF) << 24) | ((self.RMPPType & 0xFF) << 16) | ((self.RRespTime & 0x1F) << 11) | ((self.RMPPFlags & 0x7) << 8) | ((self.RMPPStatus & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RMPPVersion = (value >> 24) & 0xFF;
        self.RMPPType = (value >> 16) & 0xFF;
        self.RRespTime = (value >> 11) & 0x1F;
        self.RMPPFlags = (value >> 8) & 0x7;
        self.RMPPStatus = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.reserved_288 & 0xFF) << 24) | ((self.OUI & 0xFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved_288 = (value >> 24) & 0xFF;
        self.OUI = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 40:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHLLLLL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self.data = bytearray(buffer[offset + 40:offset + 256])
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved_144,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self._pack_1_32,) = struct.unpack_from('>BBBBHHQHHLLLLL',buffer,offset+0);

MEMBER_FORMATS = {'counterSelect2': 'hex', 'counterSelect3': 'hex', 'counterSelect0': 'hex', 'counterSelect1': 'hex', 'counterSelect6': 'hex', 'nodeString': 'str', 'counterSelect4': 'hex', 'redirectPKey': 'hex', 'diagCode': 'hex', 'servicePKey': 'hex', 'QOSClass': 'hex', 'initType': 'hex', 'trapQP': 'hex', 'counterSelect10': 'hex', 'altTClass': 'hex', 'MLID': 'hex', 'counterSelect': 'hex', 'QKey': 'hex', 'counterSelect12': 'hex', 'counterSelect7': 'hex', 'vendorID': 'hex', 'capabilityMask': 'hex', 'initTypeReply': 'hex', 'counterSelect14': 'hex', 'redirectQKey': 'hex', 'counterSelect5': 'hex', 'serviceName': 'str', 'IDString': 'str', 'PKeyBlock': 'hex', 'communityName': 'str', 'counterSelect8': 'hex', 'revision': 'hex', 'PKey': 'hex', 'capabilityMask2': 'hex', 'counterSelect9': 'hex', 'redirectTC': 'hex', 'trapPKey': 'hex', 'counterSelect11': 'hex', 'transactionID': 'hex', 'counterSelect13': 'hex', 'SMKey': 'hex', 'MKey': 'hex', 'localCMQKey': 'hex', 'redirectQP': 'hex', 'GIDPrefix': 'gid_prefix', 'localQKey': 'hex', 'serviceID': 'hex', 'deviceID': 'hex', 'trapQKey': 'hex', 'TClass': 'hex'};
CLASS_TO_STRUCT = {(7,258):CMFormat,
	(1,257):SMPFormat,
	(129,257):SMPFormatDirected,
	(3,258):SAFormat,
	(4,257):PMFormat,
	(6,257):DMFormat,
	(8,257):SNMPFormat,
	(9,257):VendFormat,
	(48,257):VendOUIFormat};
ATTR_TO_STRUCT = {(CMFormat,16):CMREQ,
	(CMFormat,17):CMMRA,
	(CMFormat,18):CMREJ,
	(CMFormat,19):CMREP,
	(CMFormat,20):CMRTU,
	(CMFormat,21):CMDREQ,
	(CMFormat,22):CMDREP,
	(CMFormat,23):CMSIDR_REQ,
	(CMFormat,24):CMSIDR_REP,
	(CMFormat,25):CMLAP,
	(CMFormat,26):CMAPR,
	(DMFormat,1):MADClassPortInfo,
	(DMFormat,16):DMIOUnitInfo,
	(DMFormat,17):DMIOControllerProfile,
	(DMFormat,18):DMServiceEntries,
	(DMFormat,32):DMDiagnosticTimeout,
	(DMFormat,33):DMPrepareToTest,
	(DMFormat,34):DMTestDeviceOnce,
	(DMFormat,35):DMTestDeviceLoop,
	(DMFormat,36):DMDiagCode,
	(PMFormat,1):MADClassPortInfo,
	(PMFormat,16):PMPortSamplesCtl,
	(PMFormat,17):PMPortSamplesRes,
	(PMFormat,18):PMPortCounters,
	(PMFormat,21):PMPortRcvErrorDetails,
	(PMFormat,22):PMPortXmitDiscardDetails,
	(PMFormat,23):PMPortOpRcvCounters,
	(PMFormat,24):PMPortFlowCtlCounters,
	(PMFormat,25):PMPortVLOpPackets,
	(PMFormat,26):PMPortVLOpData,
	(PMFormat,27):PMPortVLXmitFlowCtlUpdateErrors,
	(PMFormat,28):PMPortVLXmitWaitCounters,
	(PMFormat,29):PMPortCountersExt,
	(PMFormat,30):PMPortSamplesResExt,
	(PMFormat,48):PMSwPortVLCongestion,
	(PMFormat,54):PMPortXmitDataSL,
	(PMFormat,55):PMPortRcvDataSL,
	(SAFormat,1):MADClassPortInfo,
	(SAFormat,3):MADInformInfo,
	(SAFormat,17):SANodeRecord,
	(SAFormat,18):SAPortInfoRecord,
	(SAFormat,19):SASLToVLMappingTableRecord,
	(SAFormat,20):SASwitchInfoRecord,
	(SAFormat,21):SALinearForwardingTableRecord,
	(SAFormat,22):SARandomForwardingTableRecord,
	(SAFormat,23):SAMulticastForwardingTableRecord,
	(SAFormat,24):SASMInfoRecord,
	(SAFormat,32):SALinkRecord,
	(SAFormat,48):SAGUIDInfoRecord,
	(SAFormat,49):SAServiceRecord,
	(SAFormat,51):SAPKeyTableRecord,
	(SAFormat,53):SAPathRecord,
	(SAFormat,54):SAVLArbitrationTableRecord,
	(SAFormat,56):SAMCMemberRecord,
	(SAFormat,57):SATraceRecord,
	(SAFormat,58):SAMultiPathRecord,
	(SAFormat,59):SAServiceAssociationRecord,
	(SAFormat,243):SAInformInfoRecord,
	(SMPFormat,2):SMPNoticeTrap,
	(SMPFormat,16):SMPNodeDescription,
	(SMPFormat,17):SMPNodeInfo,
	(SMPFormat,18):SMPSwitchInfo,
	(SMPFormat,20):SMPGUIDInfo,
	(SMPFormat,21):SMPPortInfo,
	(SMPFormat,22):SMPPKeyTable,
	(SMPFormat,23):SMPSLToVLMappingTable,
	(SMPFormat,24):SMPVLArbitrationTable,
	(SMPFormat,25):SMPLinearForwardingTable,
	(SMPFormat,26):SMPRandomForwardingTable,
	(SMPFormat,27):SMPMulticastForwardingTable,
	(SMPFormat,32):SMPSMInfo,
	(SMPFormat,48):SMPVendorDiag,
	(SMPFormat,49):SMPLedInfo,
	(SMPFormatDirected,2):SMPNoticeTrap,
	(SMPFormatDirected,16):SMPNodeDescription,
	(SMPFormatDirected,17):SMPNodeInfo,
	(SMPFormatDirected,18):SMPSwitchInfo,
	(SMPFormatDirected,20):SMPGUIDInfo,
	(SMPFormatDirected,21):SMPPortInfo,
	(SMPFormatDirected,22):SMPPKeyTable,
	(SMPFormatDirected,23):SMPSLToVLMappingTable,
	(SMPFormatDirected,24):SMPVLArbitrationTable,
	(SMPFormatDirected,25):SMPLinearForwardingTable,
	(SMPFormatDirected,26):SMPRandomForwardingTable,
	(SMPFormatDirected,27):SMPMulticastForwardingTable,
	(SMPFormatDirected,32):SMPSMInfo,
	(SMPFormatDirected,48):SMPVendorDiag,
	(SMPFormatDirected,49):SMPLedInfo,
	(SNMPFormat,16):SNMPCommunityInfo,
	(SNMPFormat,17):SNMPPDUInfo};
