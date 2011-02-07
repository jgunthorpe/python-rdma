import struct,rdma.binstruct;
class BinFormat(rdma.binstruct.BinStruct):
    '''Base class for all `*Format` type packet layouts.'''
    def _format_data(self,F,start_bits,end_bits,offset):
        attr = ATTR_TO_STRUCT.get((self.__class__,self.attributeID));
        if attr is None:
            return self.dump(F,start_bits,end_bits,'data',offset);
        attr(self,offset+start_bits/8).printer(F,offset+start_bits/8);
    def describe(self):
        '''Return a short description of the RPC described by this format.'''
        attr = ATTR_TO_STRUCT.get((self.__class__,self.attributeID));
        if attr is None:
            s = '??(%u)'%(self.attributeID);
        else:
            s = '%s(%u)'%(attr.__name__,self.attributeID);
        return '%s %s(%u.%u) %s'%(IBA.const_str('MAD_METHOD_',self.method,True),
                                  self.__class__.__name__,self.mgmtClass,
                                  self.classVersion,s);
        
class HdrLRH(rdma.binstruct.BinStruct):
    '''Local Route Header (section 7.7)'''
    __slots__ = ('VL','LVer','SL','reserved1','LNH','DLID','reserved2','pktLen','SLID');
    MAD_LENGTH = 8
    def zero(self):
        self.VL = 0;
        self.LVer = 0;
        self.SL = 0;
        self.reserved1 = 0;
        self.LNH = 0;
        self.DLID = 0;
        self.reserved2 = 0;
        self.pktLen = 0;
        self.SLID = 0;

    @property
    def _pack_0_32(self):
        return ((self.VL & 0xF) << 28) | ((self.LVer & 0xF) << 24) | ((self.SL & 0xF) << 20) | ((self.reserved1 & 0x3) << 18) | ((self.LNH & 0x3) << 16) | ((self.DLID & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.VL = (value >> 28) & 0xF;
        self.LVer = (value >> 24) & 0xF;
        self.SL = (value >> 20) & 0xF;
        self.reserved1 = (value >> 18) & 0x3;
        self.LNH = (value >> 16) & 0x3;
        self.DLID = (value >> 0) & 0xFFFF;

    @property
    def _pack_1_32(self):
        return ((self.reserved2 & 0x1F) << 27) | ((self.pktLen & 0x7FF) << 16) | ((self.SLID & 0xFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved2 = (value >> 27) & 0x1F;
        self.pktLen = (value >> 16) & 0x7FF;
        self.SLID = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LL',buffer,offset+0,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>LL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "VL=%r,LVer=%r,SL=%r,reserved1=%r,LNH=%r,DLID=%r"%(self.VL,self.LVer,self.SL,self.reserved1,self.LNH,self.DLID);
        self.dump(F,0,32,label,offset);
        label = "reserved2=%r,pktLen=%r,SLID=%r"%(self.reserved2,self.pktLen,self.SLID);
        self.dump(F,32,64,label,offset);

class HdrRWH(rdma.binstruct.BinStruct):
    '''Raw Header (section 5.3)'''
    __slots__ = ('reserved1','etherType');
    MAD_LENGTH = 4
    def zero(self):
        self.reserved1 = 0;
        self.etherType = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HH',buffer,offset+0,self.reserved1,self.etherType);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.etherType,) = struct.unpack_from('>HH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,etherType=%r"%(self.reserved1,self.etherType);
        self.dump(F,0,32,label,offset);

class HdrGRH(rdma.binstruct.BinStruct):
    '''Global Route Header (section 8.3)'''
    __slots__ = ('IPVer','TClass','flowLabel','payLen','nxtHdr','hopLmt','SGID','DGID');
    MAD_LENGTH = 40
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
        self._buf = buffer[offset:];
        self.SGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.DGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        (self._pack_0_32,self.payLen,self.nxtHdr,self.hopLmt,) = struct.unpack_from('>LHBB',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "IPVer=%r,TClass=%r,flowLabel=%r"%(self.IPVer,self.TClass,self.flowLabel);
        self.dump(F,0,32,label,offset);
        label = "payLen=%r,nxtHdr=%r,hopLmt=%r"%(self.payLen,self.nxtHdr,self.hopLmt);
        self.dump(F,32,64,label,offset);
        label = "SGID=%r"%(self.SGID);
        self.dump(F,64,192,label,offset);
        label = "DGID=%r"%(self.DGID);
        self.dump(F,192,320,label,offset);

class HdrBTH(rdma.binstruct.BinStruct):
    '''Base Transport Header (section 9.2)'''
    __slots__ = ('service','function','SE','migReq','padCnt','TVer','PKey','reserved1','destQP','ackReq','reserved2','PSN');
    MAD_LENGTH = 12
    def zero(self):
        self.service = 0;
        self.function = 0;
        self.SE = 0;
        self.migReq = 0;
        self.padCnt = 0;
        self.TVer = 0;
        self.PKey = 0;
        self.reserved1 = 0;
        self.destQP = 0;
        self.ackReq = 0;
        self.reserved2 = 0;
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
        return ((self.reserved1 & 0xFF) << 24) | ((self.destQP & 0xFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved1 = (value >> 24) & 0xFF;
        self.destQP = (value >> 0) & 0xFFFFFF;

    @property
    def _pack_2_32(self):
        return ((self.ackReq & 0x1) << 31) | ((self.reserved2 & 0x7F) << 24) | ((self.PSN & 0xFFFFFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.ackReq = (value >> 31) & 0x1;
        self.reserved2 = (value >> 24) & 0x7F;
        self.PSN = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LLL',buffer,offset+0,self._pack_0_32,self._pack_1_32,self._pack_2_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self._pack_0_32,self._pack_1_32,self._pack_2_32,) = struct.unpack_from('>LLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "service=%r,function=%r,SE=%r,migReq=%r,padCnt=%r,TVer=%r,PKey=%r"%(self.service,self.function,self.SE,self.migReq,self.padCnt,self.TVer,self.PKey);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r,destQP=%r"%(self.reserved1,self.destQP);
        self.dump(F,32,64,label,offset);
        label = "ackReq=%r,reserved2=%r,PSN=%r"%(self.ackReq,self.reserved2,self.PSN);
        self.dump(F,64,96,label,offset);

class HdrRDETH(rdma.binstruct.BinStruct):
    '''Reliable Datagram Extended Transport Header (section 9.3.1)'''
    __slots__ = ('reserved1','EEC');
    MAD_LENGTH = 4
    def zero(self):
        self.reserved1 = 0;
        self.EEC = 0;

    @property
    def _pack_0_32(self):
        return ((self.reserved1 & 0xFF) << 24) | ((self.EEC & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.reserved1 = (value >> 24) & 0xFF;
        self.EEC = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,EEC=%r"%(self.reserved1,self.EEC);
        self.dump(F,0,32,label,offset);

class HdrDETH(rdma.binstruct.BinStruct):
    '''Datagram Extended Transport Header (section 9.3.2)'''
    __slots__ = ('QKey','reserved1','srcQP');
    MAD_LENGTH = 8
    def zero(self):
        self.QKey = 0;
        self.reserved1 = 0;
        self.srcQP = 0;

    @property
    def _pack_0_32(self):
        return ((self.reserved1 & 0xFF) << 24) | ((self.srcQP & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.reserved1 = (value >> 24) & 0xFF;
        self.srcQP = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LL',buffer,offset+0,self.QKey,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.QKey,self._pack_0_32,) = struct.unpack_from('>LL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "QKey=%r"%(self.QKey);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r,srcQP=%r"%(self.reserved1,self.srcQP);
        self.dump(F,32,64,label,offset);

class HdrRETH(rdma.binstruct.BinStruct):
    '''RDMA Extended Transport Header (section 9.3.3)'''
    __slots__ = ('VA','RKey','DMALen');
    MAD_LENGTH = 16
    def zero(self):
        self.VA = 0;
        self.RKey = 0;
        self.DMALen = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QLL',buffer,offset+0,self.VA,self.RKey,self.DMALen);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.VA,self.RKey,self.DMALen,) = struct.unpack_from('>QLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "VA=%r"%(self.VA);
        self.dump(F,0,64,label,offset);
        label = "RKey=%r"%(self.RKey);
        self.dump(F,64,96,label,offset);
        label = "DMALen=%r"%(self.DMALen);
        self.dump(F,96,128,label,offset);

class HdrAtomicETH(rdma.binstruct.BinStruct):
    '''Atomic Extended Transport Header (section 9.3.4)'''
    __slots__ = ('VA','RKey','swapData','cmpData');
    MAD_LENGTH = 28
    def zero(self):
        self.VA = 0;
        self.RKey = 0;
        self.swapData = 0;
        self.cmpData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QLQQ',buffer,offset+0,self.VA,self.RKey,self.swapData,self.cmpData);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.VA,self.RKey,self.swapData,self.cmpData,) = struct.unpack_from('>QLQQ',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "VA=%r"%(self.VA);
        self.dump(F,0,64,label,offset);
        label = "RKey=%r"%(self.RKey);
        self.dump(F,64,96,label,offset);
        label = "swapData=%r"%(self.swapData);
        self.dump(F,96,160,label,offset);
        label = "cmpData=%r"%(self.cmpData);
        self.dump(F,160,224,label,offset);

class HdrAETH(rdma.binstruct.BinStruct):
    '''ACK Extended Transport Header (section 9.3.5)'''
    __slots__ = ('syndrome','MSN');
    MAD_LENGTH = 4
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
        self._buf = buffer[offset:];
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "syndrome=%r,MSN=%r"%(self.syndrome,self.MSN);
        self.dump(F,0,32,label,offset);

class HdrAtomicAckETH(rdma.binstruct.BinStruct):
    '''Atomic Acknowledge Extended Transport Header (section 9.5.3)'''
    __slots__ = ('origRData');
    MAD_LENGTH = 8
    def zero(self):
        self.origRData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>Q',buffer,offset+0,self.origRData);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.origRData,) = struct.unpack_from('>Q',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "origRData=%r"%(self.origRData);
        self.dump(F,0,64,label,offset);

class HdrImmDt(rdma.binstruct.BinStruct):
    '''Immediate Extended Transport Header (section 9.3.6)'''
    __slots__ = ('immediateData');
    MAD_LENGTH = 4
    def zero(self):
        self.immediateData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self.immediateData);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.immediateData,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "immediateData=%r"%(self.immediateData);
        self.dump(F,0,32,label,offset);

class HdrIETH(rdma.binstruct.BinStruct):
    '''Invalidate Extended Transport Header (section 9.3.7)'''
    __slots__ = ('RKey');
    MAD_LENGTH = 4
    def zero(self):
        self.RKey = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self.RKey);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.RKey,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "RKey=%r"%(self.RKey);
        self.dump(F,0,32,label,offset);

class HdrFlowControl(rdma.binstruct.BinStruct):
    '''Flow Control Packet (section 7.9.4)'''
    __slots__ = ('op','FCTBS','VL','FCCL');
    MAD_LENGTH = 4
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
        self._buf = buffer[offset:];
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "op=%r,FCTBS=%r,VL=%r,FCCL=%r"%(self.op,self.FCTBS,self.VL,self.FCCL);
        self.dump(F,0,32,label,offset);

class CMFormat(BinFormat):
    '''Request for Communication (section 16.7.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x7
    MAD_CLASS_VERSION = 0x2
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
        self.attributeModifier = 0;
        self.data = bytearray(232);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.data = buffer[offset + 24:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        self._format_data(F,192,2048,offset);

class CMPath(rdma.binstruct.BinStruct):
    '''Path Information (section 12.6)'''
    __slots__ = ('SLID','DLID','SGID','DGID','flowLabel','reserved1','reserved2','PD','TClass','hopLimit','SL','subnetLocal','reserved3','localACKTimeout','reserved4');
    MAD_LENGTH = 44
    def zero(self):
        self.SLID = 0;
        self.DLID = 0;
        self.SGID = IBA.GID();
        self.DGID = IBA.GID();
        self.flowLabel = 0;
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.PD = 0;
        self.TClass = 0;
        self.hopLimit = 0;
        self.SL = 0;
        self.subnetLocal = 0;
        self.reserved3 = 0;
        self.localACKTimeout = 0;
        self.reserved4 = 0;

    @property
    def _pack_0_32(self):
        return ((self.flowLabel & 0xFFFFF) << 12) | ((self.reserved1 & 0xF) << 8) | ((self.reserved2 & 0x3) << 6) | ((self.PD & 0x3F) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.flowLabel = (value >> 12) & 0xFFFFF;
        self.reserved1 = (value >> 8) & 0xF;
        self.reserved2 = (value >> 6) & 0x3;
        self.PD = (value >> 0) & 0x3F;

    @property
    def _pack_1_32(self):
        return ((self.TClass & 0xFF) << 24) | ((self.hopLimit & 0xFF) << 16) | ((self.SL & 0xF) << 12) | ((self.subnetLocal & 0x1) << 11) | ((self.reserved3 & 0x7) << 8) | ((self.localACKTimeout & 0x1F) << 3) | ((self.reserved4 & 0x7) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.TClass = (value >> 24) & 0xFF;
        self.hopLimit = (value >> 16) & 0xFF;
        self.SL = (value >> 12) & 0xF;
        self.subnetLocal = (value >> 11) & 0x1;
        self.reserved3 = (value >> 8) & 0x7;
        self.localACKTimeout = (value >> 3) & 0x1F;
        self.reserved4 = (value >> 0) & 0x7;

    def pack_into(self,buffer,offset=0):
        self.SGID.pack_into(buffer,offset + 4);
        self.DGID.pack_into(buffer,offset + 20);
        struct.pack_into('>HH',buffer,offset+0,self.SLID,self.DLID);
        struct.pack_into('>LL',buffer,offset+36,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.SGID = IBA.GID(buffer[offset + 4:offset + 20],raw=True);
        self.DGID = IBA.GID(buffer[offset + 20:offset + 36],raw=True);
        (self.SLID,self.DLID,) = struct.unpack_from('>HH',buffer,offset+0);
        (self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>LL',buffer,offset+36);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "SLID=%r,DLID=%r"%(self.SLID,self.DLID);
        self.dump(F,0,32,label,offset);
        label = "SGID=%r"%(self.SGID);
        self.dump(F,32,160,label,offset);
        label = "DGID=%r"%(self.DGID);
        self.dump(F,160,288,label,offset);
        label = "flowLabel=%r,reserved1=%r,reserved2=%r,PD=%r"%(self.flowLabel,self.reserved1,self.reserved2,self.PD);
        self.dump(F,288,320,label,offset);
        label = "TClass=%r,hopLimit=%r,SL=%r,subnetLocal=%r,reserved3=%r,localACKTimeout=%r,reserved4=%r"%(self.TClass,self.hopLimit,self.SL,self.subnetLocal,self.reserved3,self.localACKTimeout,self.reserved4);
        self.dump(F,320,352,label,offset);

class CMREQ(rdma.binstruct.BinStruct):
    '''Request for Communication (section 12.6.5)'''
    __slots__ = ('LCID','reserved1','serviceID','LGUID','localCMQKey','localQKey','localQPN','responderResources','localEECN','initiatorDepth','remoteEECN','remoteResponseTimeout','transportService','flowControl','startingPSN','localResponseTimeout','retryCount','PKey','pathPacketMTU','RDCExists','RNRRetryCount','maxCMRetries','reserved2','primaryPath','alternatePath','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x10
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def __init__(self,*args):
        self.primaryPath = CMPath();
        self.alternatePath = CMPath();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LCID = 0;
        self.reserved1 = 0;
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
        self.reserved2 = 0;
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
        return ((self.PKey & 0xFFFF) << 16) | ((self.pathPacketMTU & 0xF) << 12) | ((self.RDCExists & 0x1) << 11) | ((self.RNRRetryCount & 0x7) << 8) | ((self.maxCMRetries & 0xF) << 4) | ((self.reserved2 & 0xF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.PKey = (value >> 16) & 0xFFFF;
        self.pathPacketMTU = (value >> 12) & 0xF;
        self.RDCExists = (value >> 11) & 0x1;
        self.RNRRetryCount = (value >> 8) & 0x7;
        self.maxCMRetries = (value >> 4) & 0xF;
        self.reserved2 = (value >> 0) & 0xF;

    def pack_into(self,buffer,offset=0):
        self.LGUID.pack_into(buffer,offset + 16);
        self.primaryPath.pack_into(buffer,offset + 52);
        self.alternatePath.pack_into(buffer,offset + 96);
        buffer[offset + 140:offset + 232] = self.privateData
        struct.pack_into('>LLQ',buffer,offset+0,self.LCID,self.reserved1,self.serviceID);
        struct.pack_into('>LLLLLLL',buffer,offset+24,self.localCMQKey,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.LGUID = IBA.GUID(buffer[offset + 16:offset + 24],raw=True);
        self.primaryPath.unpack_from(buffer,offset + 52);
        self.alternatePath.unpack_from(buffer,offset + 96);
        self.privateData = buffer[offset + 140:offset + 232]
        (self.LCID,self.reserved1,self.serviceID,) = struct.unpack_from('>LLQ',buffer,offset+0);
        (self.localCMQKey,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32,) = struct.unpack_from('>LLLLLLL',buffer,offset+24);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "serviceID=%r"%(self.serviceID);
        self.dump(F,64,128,label,offset);
        label = "LGUID=%r"%(self.LGUID);
        self.dump(F,128,192,label,offset);
        label = "localCMQKey=%r"%(self.localCMQKey);
        self.dump(F,192,224,label,offset);
        label = "localQKey=%r"%(self.localQKey);
        self.dump(F,224,256,label,offset);
        label = "localQPN=%r,responderResources=%r"%(self.localQPN,self.responderResources);
        self.dump(F,256,288,label,offset);
        label = "localEECN=%r,initiatorDepth=%r"%(self.localEECN,self.initiatorDepth);
        self.dump(F,288,320,label,offset);
        label = "remoteEECN=%r,remoteResponseTimeout=%r,transportService=%r,flowControl=%r"%(self.remoteEECN,self.remoteResponseTimeout,self.transportService,self.flowControl);
        self.dump(F,320,352,label,offset);
        label = "startingPSN=%r,localResponseTimeout=%r,retryCount=%r"%(self.startingPSN,self.localResponseTimeout,self.retryCount);
        self.dump(F,352,384,label,offset);
        label = "PKey=%r,pathPacketMTU=%r,RDCExists=%r,RNRRetryCount=%r,maxCMRetries=%r,reserved2=%r"%(self.PKey,self.pathPacketMTU,self.RDCExists,self.RNRRetryCount,self.maxCMRetries,self.reserved2);
        self.dump(F,384,416,label,offset);
        label = "primaryPath=%r"%(self.primaryPath);
        self.dump(F,416,768,label,offset);
        label = "alternatePath=%r"%(self.alternatePath);
        self.dump(F,768,1120,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,1120,1856,label,offset);

class CMMRA(rdma.binstruct.BinStruct):
    '''Message Receipt Acknowledgement (section 12.6.6)'''
    __slots__ = ('LCID','RCID','messageMRAed','reserved1','serviceTimeout','reserved2','reserved3','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x11
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.messageMRAed = 0;
        self.reserved1 = 0;
        self.serviceTimeout = 0;
        self.reserved2 = 0;
        self.reserved3 = 0;
        self.privateData = bytearray(220);

    @property
    def _pack_0_32(self):
        return ((self.messageMRAed & 0x3) << 30) | ((self.reserved1 & 0x3F) << 24) | ((self.serviceTimeout & 0x1F) << 19) | ((self.reserved2 & 0x7) << 16) | ((self.reserved3 & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.messageMRAed = (value >> 30) & 0x3;
        self.reserved1 = (value >> 24) & 0x3F;
        self.serviceTimeout = (value >> 19) & 0x1F;
        self.reserved2 = (value >> 16) & 0x7;
        self.reserved3 = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 232] = self.privateData
        struct.pack_into('>LLL',buffer,offset+0,self.LCID,self.RCID,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.privateData = buffer[offset + 12:offset + 232]
        (self.LCID,self.RCID,self._pack_0_32,) = struct.unpack_from('>LLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "messageMRAed=%r,reserved1=%r,serviceTimeout=%r,reserved2=%r,reserved3=%r"%(self.messageMRAed,self.reserved1,self.serviceTimeout,self.reserved2,self.reserved3);
        self.dump(F,64,96,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,96,1856,label,offset);

class CMREJ(rdma.binstruct.BinStruct):
    '''Reject (section 12.6.7)'''
    __slots__ = ('LCID','RCID','messageRejected','reserved1','rejectInfoLength','reserved2','reason','ARI','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x12
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.messageRejected = 0;
        self.reserved1 = 0;
        self.rejectInfoLength = 0;
        self.reserved2 = 0;
        self.reason = 0;
        self.ARI = bytearray(72);
        self.privateData = bytearray(148);

    @property
    def _pack_0_32(self):
        return ((self.messageRejected & 0x3) << 30) | ((self.reserved1 & 0x3F) << 24) | ((self.rejectInfoLength & 0x7F) << 17) | ((self.reserved2 & 0x1) << 16) | ((self.reason & 0xFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.messageRejected = (value >> 30) & 0x3;
        self.reserved1 = (value >> 24) & 0x3F;
        self.rejectInfoLength = (value >> 17) & 0x7F;
        self.reserved2 = (value >> 16) & 0x1;
        self.reason = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 84] = self.ARI
        buffer[offset + 84:offset + 232] = self.privateData
        struct.pack_into('>LLL',buffer,offset+0,self.LCID,self.RCID,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.ARI = buffer[offset + 12:offset + 84]
        self.privateData = buffer[offset + 84:offset + 232]
        (self.LCID,self.RCID,self._pack_0_32,) = struct.unpack_from('>LLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "messageRejected=%r,reserved1=%r,rejectInfoLength=%r,reserved2=%r,reason=%r"%(self.messageRejected,self.reserved1,self.rejectInfoLength,self.reserved2,self.reason);
        self.dump(F,64,96,label,offset);
        label = "ARI=%r"%(self.ARI);
        self.dump(F,96,672,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,672,1856,label,offset);

class CMREP(rdma.binstruct.BinStruct):
    '''Reply To Request For Communication (section 12.6.8)'''
    __slots__ = ('LCID','RCID','localQKey','localQPN','reserved1','localEEContext','reserved2','startingPSN','reserved3','responderResources','initiatorDepth','targetACKDelay','failoverAccepted','flowControl','RNRRetryCount','reserved4','LGUID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x13
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.localQKey = 0;
        self.localQPN = 0;
        self.reserved1 = 0;
        self.localEEContext = 0;
        self.reserved2 = 0;
        self.startingPSN = 0;
        self.reserved3 = 0;
        self.responderResources = 0;
        self.initiatorDepth = 0;
        self.targetACKDelay = 0;
        self.failoverAccepted = 0;
        self.flowControl = 0;
        self.RNRRetryCount = 0;
        self.reserved4 = 0;
        self.LGUID = IBA.GUID();
        self.privateData = bytearray(196);

    @property
    def _pack_0_32(self):
        return ((self.localQPN & 0xFFFFFF) << 8) | ((self.reserved1 & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.localQPN = (value >> 8) & 0xFFFFFF;
        self.reserved1 = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.localEEContext & 0xFFFFFF) << 8) | ((self.reserved2 & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.localEEContext = (value >> 8) & 0xFFFFFF;
        self.reserved2 = (value >> 0) & 0xFF;

    @property
    def _pack_2_32(self):
        return ((self.startingPSN & 0xFFFFFF) << 8) | ((self.reserved3 & 0xFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.startingPSN = (value >> 8) & 0xFFFFFF;
        self.reserved3 = (value >> 0) & 0xFF;

    @property
    def _pack_3_32(self):
        return ((self.responderResources & 0xFF) << 24) | ((self.initiatorDepth & 0xFF) << 16) | ((self.targetACKDelay & 0x1F) << 11) | ((self.failoverAccepted & 0x3) << 9) | ((self.flowControl & 0x1) << 8) | ((self.RNRRetryCount & 0x7) << 5) | ((self.reserved4 & 0x1F) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.responderResources = (value >> 24) & 0xFF;
        self.initiatorDepth = (value >> 16) & 0xFF;
        self.targetACKDelay = (value >> 11) & 0x1F;
        self.failoverAccepted = (value >> 9) & 0x3;
        self.flowControl = (value >> 8) & 0x1;
        self.RNRRetryCount = (value >> 5) & 0x7;
        self.reserved4 = (value >> 0) & 0x1F;

    def pack_into(self,buffer,offset=0):
        self.LGUID.pack_into(buffer,offset + 28);
        buffer[offset + 36:offset + 232] = self.privateData
        struct.pack_into('>LLLLLLL',buffer,offset+0,self.LCID,self.RCID,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.LGUID = IBA.GUID(buffer[offset + 28:offset + 36],raw=True);
        self.privateData = buffer[offset + 36:offset + 232]
        (self.LCID,self.RCID,self.localQKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,) = struct.unpack_from('>LLLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "localQKey=%r"%(self.localQKey);
        self.dump(F,64,96,label,offset);
        label = "localQPN=%r,reserved1=%r"%(self.localQPN,self.reserved1);
        self.dump(F,96,128,label,offset);
        label = "localEEContext=%r,reserved2=%r"%(self.localEEContext,self.reserved2);
        self.dump(F,128,160,label,offset);
        label = "startingPSN=%r,reserved3=%r"%(self.startingPSN,self.reserved3);
        self.dump(F,160,192,label,offset);
        label = "responderResources=%r,initiatorDepth=%r,targetACKDelay=%r,failoverAccepted=%r,flowControl=%r,RNRRetryCount=%r,reserved4=%r"%(self.responderResources,self.initiatorDepth,self.targetACKDelay,self.failoverAccepted,self.flowControl,self.RNRRetryCount,self.reserved4);
        self.dump(F,192,224,label,offset);
        label = "LGUID=%r"%(self.LGUID);
        self.dump(F,224,288,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,288,1856,label,offset);

class CMRTU(rdma.binstruct.BinStruct):
    '''Ready To Use (section 12.6.9)'''
    __slots__ = ('LCID','RCID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x14
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.privateData = bytearray(224);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 8:offset + 232] = self.privateData
        struct.pack_into('>LL',buffer,offset+0,self.LCID,self.RCID);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.privateData = buffer[offset + 8:offset + 232]
        (self.LCID,self.RCID,) = struct.unpack_from('>LL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,64,1856,label,offset);

class CMDREQ(rdma.binstruct.BinStruct):
    '''Request For Communication Release (Disconnection Request) (section 12.6.10)'''
    __slots__ = ('LCID','RCID','remoteQPN','reserved1','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x15
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.remoteQPN = 0;
        self.reserved1 = 0;
        self.privateData = bytearray(220);

    @property
    def _pack_0_32(self):
        return ((self.remoteQPN & 0xFFFFFF) << 8) | ((self.reserved1 & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.remoteQPN = (value >> 8) & 0xFFFFFF;
        self.reserved1 = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 232] = self.privateData
        struct.pack_into('>LLL',buffer,offset+0,self.LCID,self.RCID,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.privateData = buffer[offset + 12:offset + 232]
        (self.LCID,self.RCID,self._pack_0_32,) = struct.unpack_from('>LLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "remoteQPN=%r,reserved1=%r"%(self.remoteQPN,self.reserved1);
        self.dump(F,64,96,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,96,1856,label,offset);

class CMDREP(rdma.binstruct.BinStruct):
    '''Reply To Request For Communication Release (section 12.6.11)'''
    __slots__ = ('LCID','RCID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x16
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.privateData = bytearray(224);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 8:offset + 232] = self.privateData
        struct.pack_into('>LL',buffer,offset+0,self.LCID,self.RCID);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.privateData = buffer[offset + 8:offset + 232]
        (self.LCID,self.RCID,) = struct.unpack_from('>LL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,64,1856,label,offset);

class CMLAP(rdma.binstruct.BinStruct):
    '''Load Alternate Path (section 12.8.1)'''
    __slots__ = ('LCID','RCID','QKey','RQPN','RCMTimeout','reserved1','reserved2','altSLID','altDLID','altSGID','altDGID','altFlowLabel','reserved3','altTClass','altHopLimit','reserved4','altIPD','altSL','altSubnetLocal','reserved5','altLocalACKTimeout','reserved6','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x19
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.QKey = 0;
        self.RQPN = 0;
        self.RCMTimeout = 0;
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.altSLID = 0;
        self.altDLID = 0;
        self.altSGID = IBA.GID();
        self.altDGID = IBA.GID();
        self.altFlowLabel = 0;
        self.reserved3 = 0;
        self.altTClass = 0;
        self.altHopLimit = 0;
        self.reserved4 = 0;
        self.altIPD = 0;
        self.altSL = 0;
        self.altSubnetLocal = 0;
        self.reserved5 = 0;
        self.altLocalACKTimeout = 0;
        self.reserved6 = 0;
        self.privateData = bytearray(168);

    @property
    def _pack_0_32(self):
        return ((self.RQPN & 0xFFFFFF) << 8) | ((self.RCMTimeout & 0x1F) << 3) | ((self.reserved1 & 0x7) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.RQPN = (value >> 8) & 0xFFFFFF;
        self.RCMTimeout = (value >> 3) & 0x1F;
        self.reserved1 = (value >> 0) & 0x7;

    @property
    def _pack_1_32(self):
        return ((self.altFlowLabel & 0xFFFFF) << 12) | ((self.reserved3 & 0xF) << 8) | ((self.altTClass & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.altFlowLabel = (value >> 12) & 0xFFFFF;
        self.reserved3 = (value >> 8) & 0xF;
        self.altTClass = (value >> 0) & 0xFF;

    @property
    def _pack_2_32(self):
        return ((self.altHopLimit & 0xFF) << 24) | ((self.reserved4 & 0x3) << 22) | ((self.altIPD & 0x3F) << 16) | ((self.altSL & 0xF) << 12) | ((self.altSubnetLocal & 0x1) << 11) | ((self.reserved5 & 0x7) << 8) | ((self.altLocalACKTimeout & 0x1F) << 3) | ((self.reserved6 & 0x7) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.altHopLimit = (value >> 24) & 0xFF;
        self.reserved4 = (value >> 22) & 0x3;
        self.altIPD = (value >> 16) & 0x3F;
        self.altSL = (value >> 12) & 0xF;
        self.altSubnetLocal = (value >> 11) & 0x1;
        self.reserved5 = (value >> 8) & 0x7;
        self.altLocalACKTimeout = (value >> 3) & 0x1F;
        self.reserved6 = (value >> 0) & 0x7;

    def pack_into(self,buffer,offset=0):
        self.altSGID.pack_into(buffer,offset + 24);
        self.altDGID.pack_into(buffer,offset + 40);
        buffer[offset + 64:offset + 232] = self.privateData
        struct.pack_into('>LLLLLHH',buffer,offset+0,self.LCID,self.RCID,self.QKey,self._pack_0_32,self.reserved2,self.altSLID,self.altDLID);
        struct.pack_into('>LL',buffer,offset+56,self._pack_1_32,self._pack_2_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.altSGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        self.altDGID = IBA.GID(buffer[offset + 40:offset + 56],raw=True);
        self.privateData = buffer[offset + 64:offset + 232]
        (self.LCID,self.RCID,self.QKey,self._pack_0_32,self.reserved2,self.altSLID,self.altDLID,) = struct.unpack_from('>LLLLLHH',buffer,offset+0);
        (self._pack_1_32,self._pack_2_32,) = struct.unpack_from('>LL',buffer,offset+56);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "QKey=%r"%(self.QKey);
        self.dump(F,64,96,label,offset);
        label = "RQPN=%r,RCMTimeout=%r,reserved1=%r"%(self.RQPN,self.RCMTimeout,self.reserved1);
        self.dump(F,96,128,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,128,160,label,offset);
        label = "altSLID=%r,altDLID=%r"%(self.altSLID,self.altDLID);
        self.dump(F,160,192,label,offset);
        label = "altSGID=%r"%(self.altSGID);
        self.dump(F,192,320,label,offset);
        label = "altDGID=%r"%(self.altDGID);
        self.dump(F,320,448,label,offset);
        label = "altFlowLabel=%r,reserved3=%r,altTClass=%r"%(self.altFlowLabel,self.reserved3,self.altTClass);
        self.dump(F,448,480,label,offset);
        label = "altHopLimit=%r,reserved4=%r,altIPD=%r,altSL=%r,altSubnetLocal=%r,reserved5=%r,altLocalACKTimeout=%r,reserved6=%r"%(self.altHopLimit,self.reserved4,self.altIPD,self.altSL,self.altSubnetLocal,self.reserved5,self.altLocalACKTimeout,self.reserved6);
        self.dump(F,480,512,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,512,1856,label,offset);

class CMAPR(rdma.binstruct.BinStruct):
    '''Alternate Path Response (section 12.8.2)'''
    __slots__ = ('LCID','RCID','additionalInfoLength','APstatus','reserved1','additionalInfo','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x1a
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.LCID = 0;
        self.RCID = 0;
        self.additionalInfoLength = 0;
        self.APstatus = 0;
        self.reserved1 = 0;
        self.additionalInfo = bytearray(72);
        self.privateData = bytearray(148);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 12:offset + 84] = self.additionalInfo
        buffer[offset + 84:offset + 232] = self.privateData
        struct.pack_into('>LLBBH',buffer,offset+0,self.LCID,self.RCID,self.additionalInfoLength,self.APstatus,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.additionalInfo = buffer[offset + 12:offset + 84]
        self.privateData = buffer[offset + 84:offset + 232]
        (self.LCID,self.RCID,self.additionalInfoLength,self.APstatus,self.reserved1,) = struct.unpack_from('>LLBBH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LCID=%r"%(self.LCID);
        self.dump(F,0,32,label,offset);
        label = "RCID=%r"%(self.RCID);
        self.dump(F,32,64,label,offset);
        label = "additionalInfoLength=%r,APstatus=%r,reserved1=%r"%(self.additionalInfoLength,self.APstatus,self.reserved1);
        self.dump(F,64,96,label,offset);
        label = "additionalInfo=%r"%(self.additionalInfo);
        self.dump(F,96,672,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,672,1856,label,offset);

class CMSIDR_REQ(rdma.binstruct.BinStruct):
    '''Service ID Resolution Request (section 12.11.1)'''
    __slots__ = ('requestID','reserved1','serviceID','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x17
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.requestID = 0;
        self.reserved1 = 0;
        self.serviceID = 0;
        self.privateData = bytearray(216);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 16:offset + 232] = self.privateData
        struct.pack_into('>LLQ',buffer,offset+0,self.requestID,self.reserved1,self.serviceID);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.privateData = buffer[offset + 16:offset + 232]
        (self.requestID,self.reserved1,self.serviceID,) = struct.unpack_from('>LLQ',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "requestID=%r"%(self.requestID);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "serviceID=%r"%(self.serviceID);
        self.dump(F,64,128,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,128,1856,label,offset);

class CMSIDR_REP(rdma.binstruct.BinStruct):
    '''Service ID Resolution Response (section 12.11.2)'''
    __slots__ = ('requestID','QPN','status','serviceID','QKey','classPortinfo','privateData');
    MAD_LENGTH = 232
    MAD_ATTRIBUTE_ID = 0x18
    MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
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
        self._buf = buffer[offset:];
        self.classPortinfo.unpack_from(buffer,offset + 20);
        self.privateData = buffer[offset + 92:offset + 232]
        (self.requestID,self._pack_0_32,self.serviceID,self.QKey,) = struct.unpack_from('>LLQL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "requestID=%r"%(self.requestID);
        self.dump(F,0,32,label,offset);
        label = "QPN=%r,status=%r"%(self.QPN,self.status);
        self.dump(F,32,64,label,offset);
        label = "serviceID=%r"%(self.serviceID);
        self.dump(F,64,128,label,offset);
        label = "QKey=%r"%(self.QKey);
        self.dump(F,128,160,label,offset);
        label = "classPortinfo=%r"%(self.classPortinfo);
        self.dump(F,160,736,label,offset);
        label = "privateData=%r"%(self.privateData);
        self.dump(F,736,1856,label,offset);

class MADHeader(rdma.binstruct.BinStruct):
    '''MAD Base Header (section 13.4.3)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier');
    MAD_LENGTH = 24
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
        self.attributeModifier = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);

class MADHeaderDirected(rdma.binstruct.BinStruct):
    '''MAD Base Header Directed (section 13.4.3)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','D','status','hopPointer','hopCount','transactionID','attributeID','reserved1','attributeModifier');
    MAD_LENGTH = 24
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
        self.reserved1 = 0;
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
        struct.pack_into('>BBBBLQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,) = struct.unpack_from('>BBBBLQHHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "D=%r,status=%r,hopPointer=%r,hopCount=%r"%(self.D,self.status,self.hopPointer,self.hopCount);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);

class MADClassPortInfo(rdma.binstruct.BinStruct):
    '''Class Port Info (section 13.4.8.1)'''
    __slots__ = ('baseVersion','classVersion','capabilityMask','reserved1','respTimeValue','redirectGID','redirectTC','redirectSL','redirectFL','redirectLID','redirectPKey','reserved2','redirectQP','redirectQKey','trapGID','trapTC','trapSL','trapFL','trapLID','trapPKey','trapHL','trapQP','trapQKey');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x1
    MAD_COMMMGTGET = 0x1 # MAD_METHOD_GET
    MAD_COMMMGTSET = 0x2 # MAD_METHOD_SET
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_BMGET = 0x1 # MAD_METHOD_GET
    MAD_BMSET = 0x2 # MAD_METHOD_SET
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    MAD_SNMPGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    COMPONENT_MASK = {'baseVersion':0, 'classVersion':1, 'capabilityMask':2, 'reserved1':3, 'respTimeValue':4, 'redirectGID':5, 'redirectTC':6, 'redirectSL':7, 'redirectFL':8, 'redirectLID':9, 'redirectPKey':10, 'reserved2':11, 'redirectQP':12, 'redirectQKey':13, 'trapGID':14, 'trapTC':15, 'trapSL':16, 'trapFL':17, 'trapLID':18, 'trapPKey':19, 'trapHL':20, 'trapQP':21, 'trapQKey':22}
    def zero(self):
        self.baseVersion = 0;
        self.classVersion = 0;
        self.capabilityMask = 0;
        self.reserved1 = 0;
        self.respTimeValue = 0;
        self.redirectGID = IBA.GID();
        self.redirectTC = 0;
        self.redirectSL = 0;
        self.redirectFL = 0;
        self.redirectLID = 0;
        self.redirectPKey = 0;
        self.reserved2 = 0;
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
        return ((self.reserved1 & 0x7FFFFFF) << 5) | ((self.respTimeValue & 0x1F) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.reserved1 = (value >> 5) & 0x7FFFFFF;
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
        return ((self.reserved2 & 0xFF) << 24) | ((self.redirectQP & 0xFFFFFF) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved2 = (value >> 24) & 0xFF;
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
        self._buf = buffer[offset:];
        self.redirectGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.trapGID = IBA.GID(buffer[offset + 40:offset + 56],raw=True);
        (self.baseVersion,self.classVersion,self.capabilityMask,self._pack_0_32,) = struct.unpack_from('>BBHL',buffer,offset+0);
        (self._pack_1_32,self.redirectLID,self.redirectPKey,self._pack_2_32,self.redirectQKey,) = struct.unpack_from('>LHHLL',buffer,offset+24);
        (self._pack_3_32,self.trapLID,self.trapPKey,self._pack_4_32,self.trapQKey,) = struct.unpack_from('>LHHLL',buffer,offset+56);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,classVersion=%r,capabilityMask=%r"%(self.baseVersion,self.classVersion,self.capabilityMask);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r,respTimeValue=%r"%(self.reserved1,self.respTimeValue);
        self.dump(F,32,64,label,offset);
        label = "redirectGID=%r"%(self.redirectGID);
        self.dump(F,64,192,label,offset);
        label = "redirectTC=%r,redirectSL=%r,redirectFL=%r"%(self.redirectTC,self.redirectSL,self.redirectFL);
        self.dump(F,192,224,label,offset);
        label = "redirectLID=%r,redirectPKey=%r"%(self.redirectLID,self.redirectPKey);
        self.dump(F,224,256,label,offset);
        label = "reserved2=%r,redirectQP=%r"%(self.reserved2,self.redirectQP);
        self.dump(F,256,288,label,offset);
        label = "redirectQKey=%r"%(self.redirectQKey);
        self.dump(F,288,320,label,offset);
        label = "trapGID=%r"%(self.trapGID);
        self.dump(F,320,448,label,offset);
        label = "trapTC=%r,trapSL=%r,trapFL=%r"%(self.trapTC,self.trapSL,self.trapFL);
        self.dump(F,448,480,label,offset);
        label = "trapLID=%r,trapPKey=%r"%(self.trapLID,self.trapPKey);
        self.dump(F,480,512,label,offset);
        label = "trapHL=%r,trapQP=%r"%(self.trapHL,self.trapQP);
        self.dump(F,512,544,label,offset);
        label = "trapQKey=%r"%(self.trapQKey);
        self.dump(F,544,576,label,offset);

class MADInformInfo(rdma.binstruct.BinStruct):
    '''InformInfo (section 13.4.8.3)'''
    __slots__ = ('GID','LIDRangeBegin','LIDRangeEnd','reserved1','isGeneric','subscribe','type','trapNumber','QPN','reserved2','respTimeValue','reserved3','producerType');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x3
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    COMPONENT_MASK = {'GID':0, 'LIDRangeBegin':1, 'LIDRangeEnd':2, 'reserved1':3, 'isGeneric':4, 'subscribe':5, 'type':6, 'trapNumber':7, 'QPN':8, 'reserved2':9, 'respTimeValue':10, 'reserved3':11, 'producerType':12}
    def zero(self):
        self.GID = IBA.GID();
        self.LIDRangeBegin = 0;
        self.LIDRangeEnd = 0;
        self.reserved1 = 0;
        self.isGeneric = 0;
        self.subscribe = 0;
        self.type = 0;
        self.trapNumber = 0;
        self.QPN = 0;
        self.reserved2 = 0;
        self.respTimeValue = 0;
        self.reserved3 = 0;
        self.producerType = 0;

    @property
    def _pack_0_32(self):
        return ((self.QPN & 0xFFFFFF) << 8) | ((self.reserved2 & 0x7) << 5) | ((self.respTimeValue & 0x1F) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.QPN = (value >> 8) & 0xFFFFFF;
        self.reserved2 = (value >> 5) & 0x7;
        self.respTimeValue = (value >> 0) & 0x1F;

    @property
    def _pack_1_32(self):
        return ((self.reserved3 & 0xFF) << 24) | ((self.producerType & 0xFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved3 = (value >> 24) & 0xFF;
        self.producerType = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.GID.pack_into(buffer,offset + 0);
        struct.pack_into('>HHHBBHHLL',buffer,offset+16,self.LIDRangeBegin,self.LIDRangeEnd,self.reserved1,self.isGeneric,self.subscribe,self.type,self.trapNumber,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.GID = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        (self.LIDRangeBegin,self.LIDRangeEnd,self.reserved1,self.isGeneric,self.subscribe,self.type,self.trapNumber,self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>HHHBBHHLL',buffer,offset+16);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "GID=%r"%(self.GID);
        self.dump(F,0,128,label,offset);
        label = "LIDRangeBegin=%r,LIDRangeEnd=%r"%(self.LIDRangeBegin,self.LIDRangeEnd);
        self.dump(F,128,160,label,offset);
        label = "reserved1=%r,isGeneric=%r,subscribe=%r"%(self.reserved1,self.isGeneric,self.subscribe);
        self.dump(F,160,192,label,offset);
        label = "type=%r,trapNumber=%r"%(self.type,self.trapNumber);
        self.dump(F,192,224,label,offset);
        label = "QPN=%r,reserved2=%r,respTimeValue=%r"%(self.QPN,self.reserved2,self.respTimeValue);
        self.dump(F,224,256,label,offset);
        label = "reserved3=%r,producerType=%r"%(self.reserved3,self.producerType);
        self.dump(F,256,288,label,offset);

class RMPPHeader(rdma.binstruct.BinStruct):
    '''RMPP Header Fields (section 13.6.2.1)'''
    __slots__ = ('MADHeader','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus','data1','data2');
    MAD_LENGTH = 36
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
        self._buf = buffer[offset:];
        self.MADHeader.unpack_from(buffer,offset + 0);
        (self._pack_0_32,self.data1,self.data2,) = struct.unpack_from('>LLL',buffer,offset+24);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "MADHeader=%r"%(self.MADHeader);
        self.dump(F,0,192,label,offset);
        label = "RMPPVersion=%r,RMPPType=%r,RRespTime=%r,RMPPFlags=%r,RMPPStatus=%r"%(self.RMPPVersion,self.RMPPType,self.RRespTime,self.RMPPFlags,self.RMPPStatus);
        self.dump(F,192,224,label,offset);
        label = "data1=%r"%(self.data1);
        self.dump(F,224,256,label,offset);
        label = "data2=%r"%(self.data2);
        self.dump(F,256,288,label,offset);

class RMPPShortHeader(rdma.binstruct.BinStruct):
    '''RMPP Header Fields (section 13.6.2.1)'''
    __slots__ = ('MADHeader','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus');
    MAD_LENGTH = 28
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
        self._buf = buffer[offset:];
        self.MADHeader.unpack_from(buffer,offset + 0);
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+24);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "MADHeader=%r"%(self.MADHeader);
        self.dump(F,0,192,label,offset);
        label = "RMPPVersion=%r,RMPPType=%r,RRespTime=%r,RMPPFlags=%r,RMPPStatus=%r"%(self.RMPPVersion,self.RMPPType,self.RRespTime,self.RMPPFlags,self.RMPPStatus);
        self.dump(F,192,224,label,offset);

class RMPPData(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','segmentNumber','payLoadLength','data');
    MAD_LENGTH = 256
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
        self._buf = buffer[offset:];
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.data = buffer[offset + 36:offset + 256]
        (self.segmentNumber,self.payLoadLength,) = struct.unpack_from('>LL',buffer,offset+28);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "RMPPHeader=%r"%(self.RMPPHeader);
        self.dump(F,0,224,label,offset);
        label = "segmentNumber=%r"%(self.segmentNumber);
        self.dump(F,224,256,label,offset);
        label = "payLoadLength=%r"%(self.payLoadLength);
        self.dump(F,256,288,label,offset);
        label = "data=%r"%(self.data);
        self.dump(F,288,2048,label,offset);

class RMPPAck(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','segmentNumber','newWindowLast','reserved1');
    MAD_LENGTH = 256
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.segmentNumber = 0;
        self.newWindowLast = 0;
        self.reserved1 = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.reserved1
        struct.pack_into('>LL',buffer,offset+28,self.segmentNumber,self.newWindowLast);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.reserved1 = buffer[offset + 36:offset + 256]
        (self.segmentNumber,self.newWindowLast,) = struct.unpack_from('>LL',buffer,offset+28);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "RMPPHeader=%r"%(self.RMPPHeader);
        self.dump(F,0,224,label,offset);
        label = "segmentNumber=%r"%(self.segmentNumber);
        self.dump(F,224,256,label,offset);
        label = "newWindowLast=%r"%(self.newWindowLast);
        self.dump(F,256,288,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,288,2048,label,offset);

class RMPPAbort(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','reserved1','reserved2','errorData');
    MAD_LENGTH = 256
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.errorData = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.errorData
        struct.pack_into('>LL',buffer,offset+28,self.reserved1,self.reserved2);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.errorData = buffer[offset + 36:offset + 256]
        (self.reserved1,self.reserved2,) = struct.unpack_from('>LL',buffer,offset+28);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "RMPPHeader=%r"%(self.RMPPHeader);
        self.dump(F,0,224,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,224,256,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,256,288,label,offset);
        label = "errorData=%r"%(self.errorData);
        self.dump(F,288,2048,label,offset);

class RMPPStop(rdma.binstruct.BinStruct):
    '''RMPP Data Packet (section 13.6.2.3)'''
    __slots__ = ('RMPPHeader','reserved1','reserved2','errorData');
    MAD_LENGTH = 256
    def __init__(self,*args):
        self.RMPPHeader = RMPPShortHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPShortHeader();
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.errorData = bytearray(220);

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        buffer[offset + 36:offset + 256] = self.errorData
        struct.pack_into('>LL',buffer,offset+28,self.reserved1,self.reserved2);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        self.errorData = buffer[offset + 36:offset + 256]
        (self.reserved1,self.reserved2,) = struct.unpack_from('>LL',buffer,offset+28);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "RMPPHeader=%r"%(self.RMPPHeader);
        self.dump(F,0,224,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,224,256,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,256,288,label,offset);
        label = "errorData=%r"%(self.errorData);
        self.dump(F,288,2048,label,offset);

class SMPLIDPortBlock(rdma.binstruct.BinStruct):
    '''LID/Port Block Element (section 14.2.5.11)'''
    __slots__ = ('LID','valid','LMC','reserved1','port');
    MAD_LENGTH = 4
    def zero(self):
        self.LID = 0;
        self.valid = 0;
        self.LMC = 0;
        self.reserved1 = 0;
        self.port = 0;

    @property
    def _pack_0_32(self):
        return ((self.LID & 0xFFFF) << 16) | ((self.valid & 0x1) << 15) | ((self.LMC & 0x7) << 12) | ((self.reserved1 & 0xF) << 8) | ((self.port & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.LID = (value >> 16) & 0xFFFF;
        self.valid = (value >> 15) & 0x1;
        self.LMC = (value >> 12) & 0x7;
        self.reserved1 = (value >> 8) & 0xF;
        self.port = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,valid=%r,LMC=%r,reserved1=%r,port=%r"%(self.LID,self.valid,self.LMC,self.reserved1,self.port);
        self.dump(F,0,32,label,offset);

class SMPFormat(BinFormat):
    '''SMP Format - LID Routed (section 14.2.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier','MKey','reserved2','data','reserved3');
    MAD_LENGTH = 256
    MAD_CLASS = 0x1
    MAD_CLASS_VERSION = 0x1
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
        self.attributeModifier = 0;
        self.MKey = 0;
        self.reserved2 = bytearray(32);
        self.data = bytearray(64);
        self.reserved3 = bytearray(128);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 32:offset + 64] = self.reserved2
        buffer[offset + 64:offset + 128] = self.data
        buffer[offset + 128:offset + 256] = self.reserved3
        struct.pack_into('>BBBBHHQHHLQ',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,self.MKey);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.reserved2 = buffer[offset + 32:offset + 64]
        self.data = buffer[offset + 64:offset + 128]
        self.reserved3 = buffer[offset + 128:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,self.MKey,) = struct.unpack_from('>BBBBHHQHHLQ',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        label = "MKey=%r"%(self.MKey);
        self.dump(F,192,256,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,256,512,label,offset);
        self._format_data(F,512,1024,offset);
        label = "reserved3=%r"%(self.reserved3);
        self.dump(F,1024,2048,label,offset);

class SMPFormatDirected(BinFormat):
    '''SMP Format - Direct Routed (section 14.2.1.2)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','D','status','hopPointer','hopCount','transactionID','attributeID','reserved1','attributeModifier','MKey','drSLID','drDLID','reserved2','data','initialPath','returnPath');
    MAD_LENGTH = 256
    MAD_CLASS = 0x81
    MAD_CLASS_VERSION = 0x1
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
        self.reserved1 = 0;
        self.attributeModifier = 0;
        self.MKey = 0;
        self.drSLID = 0;
        self.drDLID = 0;
        self.reserved2 = bytearray(28);
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
        buffer[offset + 36:offset + 64] = self.reserved2
        buffer[offset + 64:offset + 128] = self.data
        buffer[offset + 128:offset + 192] = self.initialPath
        buffer[offset + 192:offset + 256] = self.returnPath
        struct.pack_into('>BBBBLQHHLQHH',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,self.MKey,self.drSLID,self.drDLID);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.reserved2 = buffer[offset + 36:offset + 64]
        self.data = buffer[offset + 64:offset + 128]
        self.initialPath = buffer[offset + 128:offset + 192]
        self.returnPath = buffer[offset + 192:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self._pack_0_32,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,self.MKey,self.drSLID,self.drDLID,) = struct.unpack_from('>BBBBLQHHLQHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "D=%r,status=%r,hopPointer=%r,hopCount=%r"%(self.D,self.status,self.hopPointer,self.hopCount);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        label = "MKey=%r"%(self.MKey);
        self.dump(F,192,256,label,offset);
        label = "drSLID=%r,drDLID=%r"%(self.drSLID,self.drDLID);
        self.dump(F,256,288,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,288,512,label,offset);
        self._format_data(F,512,1024,offset);
        label = "initialPath=%r"%(self.initialPath);
        self.dump(F,1024,1536,label,offset);
        label = "returnPath=%r"%(self.returnPath);
        self.dump(F,1536,2048,label,offset);

class SMPNodeDescription(rdma.binstruct.BinStruct):
    '''Node Description String (section 14.2.5.2)'''
    __slots__ = ('nodeString');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x10
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    def __init__(self,*args):
        self.nodeString = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.nodeString = bytearray(64);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 64] = self.nodeString

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.nodeString = buffer[offset + 0:offset + 64]

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "nodeString=%r"%(self.nodeString);
        self.dump(F,0,512,label,offset);

class SMPNodeInfo(rdma.binstruct.BinStruct):
    '''Generic Node Data (section 14.2.5.3)'''
    __slots__ = ('baseVersion','classVersion','nodeType','numPorts','systemImageGUID','nodeGUID','portGUID','partitionCap','deviceID','revision','localPortNum','vendorID');
    MAD_LENGTH = 40
    MAD_ATTRIBUTE_ID = 0x11
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
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
        self._buf = buffer[offset:];
        self.systemImageGUID = IBA.GUID(buffer[offset + 4:offset + 12],raw=True);
        self.nodeGUID = IBA.GUID(buffer[offset + 12:offset + 20],raw=True);
        self.portGUID = IBA.GUID(buffer[offset + 20:offset + 28],raw=True);
        (self.baseVersion,self.classVersion,self.nodeType,self.numPorts,) = struct.unpack_from('>BBBB',buffer,offset+0);
        (self.partitionCap,self.deviceID,self.revision,self._pack_0_32,) = struct.unpack_from('>HHLL',buffer,offset+28);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,classVersion=%r,nodeType=%r,numPorts=%r"%(self.baseVersion,self.classVersion,self.nodeType,self.numPorts);
        self.dump(F,0,32,label,offset);
        label = "systemImageGUID=%r"%(self.systemImageGUID);
        self.dump(F,32,96,label,offset);
        label = "nodeGUID=%r"%(self.nodeGUID);
        self.dump(F,96,160,label,offset);
        label = "portGUID=%r"%(self.portGUID);
        self.dump(F,160,224,label,offset);
        label = "partitionCap=%r,deviceID=%r"%(self.partitionCap,self.deviceID);
        self.dump(F,224,256,label,offset);
        label = "revision=%r"%(self.revision);
        self.dump(F,256,288,label,offset);
        label = "localPortNum=%r,vendorID=%r"%(self.localPortNum,self.vendorID);
        self.dump(F,288,320,label,offset);

class SMPSwitchInfo(rdma.binstruct.BinStruct):
    '''Switch Information (section 14.2.5.4)'''
    __slots__ = ('linearFDBCap','randomFDBCap','multicastFDBCap','linearFDBTop','defaultPort','defaultMulticastPrimaryPort','defaultMulticastNotPrimaryPort','lifeTimeValue','portStateChange','reserved1','optimizedSLtoVLMappingProgramming','LIDsPerPort','partitionEnforcementCap','inboundEnforcementCap','outboundEnforcementCap','filterRawInboundCap','filterRawOutboundCap','enhancedPort0','reserved2','reserved3');
    MAD_LENGTH = 20
    MAD_ATTRIBUTE_ID = 0x12
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
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
        self.reserved1 = 0;
        self.optimizedSLtoVLMappingProgramming = 0;
        self.LIDsPerPort = 0;
        self.partitionEnforcementCap = 0;
        self.inboundEnforcementCap = 0;
        self.outboundEnforcementCap = 0;
        self.filterRawInboundCap = 0;
        self.filterRawOutboundCap = 0;
        self.enhancedPort0 = 0;
        self.reserved2 = 0;
        self.reserved3 = 0;

    @property
    def _pack_0_32(self):
        return ((self.defaultPort & 0xFF) << 24) | ((self.defaultMulticastPrimaryPort & 0xFF) << 16) | ((self.defaultMulticastNotPrimaryPort & 0xFF) << 8) | ((self.lifeTimeValue & 0x1F) << 3) | ((self.portStateChange & 0x1) << 2) | ((self.reserved1 & 0x1) << 1) | ((self.optimizedSLtoVLMappingProgramming & 0x1) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.defaultPort = (value >> 24) & 0xFF;
        self.defaultMulticastPrimaryPort = (value >> 16) & 0xFF;
        self.defaultMulticastNotPrimaryPort = (value >> 8) & 0xFF;
        self.lifeTimeValue = (value >> 3) & 0x1F;
        self.portStateChange = (value >> 2) & 0x1;
        self.reserved1 = (value >> 1) & 0x1;
        self.optimizedSLtoVLMappingProgramming = (value >> 0) & 0x1;

    @property
    def _pack_1_32(self):
        return ((self.inboundEnforcementCap & 0x1) << 31) | ((self.outboundEnforcementCap & 0x1) << 30) | ((self.filterRawInboundCap & 0x1) << 29) | ((self.filterRawOutboundCap & 0x1) << 28) | ((self.enhancedPort0 & 0x1) << 27) | ((self.reserved2 & 0x7) << 24) | ((self.reserved3 & 0xFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.inboundEnforcementCap = (value >> 31) & 0x1;
        self.outboundEnforcementCap = (value >> 30) & 0x1;
        self.filterRawInboundCap = (value >> 29) & 0x1;
        self.filterRawOutboundCap = (value >> 28) & 0x1;
        self.enhancedPort0 = (value >> 27) & 0x1;
        self.reserved2 = (value >> 24) & 0x7;
        self.reserved3 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHLHHL',buffer,offset+0,self.linearFDBCap,self.randomFDBCap,self.multicastFDBCap,self.linearFDBTop,self._pack_0_32,self.LIDsPerPort,self.partitionEnforcementCap,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.linearFDBCap,self.randomFDBCap,self.multicastFDBCap,self.linearFDBTop,self._pack_0_32,self.LIDsPerPort,self.partitionEnforcementCap,self._pack_1_32,) = struct.unpack_from('>HHHHLHHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "linearFDBCap=%r,randomFDBCap=%r"%(self.linearFDBCap,self.randomFDBCap);
        self.dump(F,0,32,label,offset);
        label = "multicastFDBCap=%r,linearFDBTop=%r"%(self.multicastFDBCap,self.linearFDBTop);
        self.dump(F,32,64,label,offset);
        label = "defaultPort=%r,defaultMulticastPrimaryPort=%r,defaultMulticastNotPrimaryPort=%r,lifeTimeValue=%r,portStateChange=%r,reserved1=%r,optimizedSLtoVLMappingProgramming=%r"%(self.defaultPort,self.defaultMulticastPrimaryPort,self.defaultMulticastNotPrimaryPort,self.lifeTimeValue,self.portStateChange,self.reserved1,self.optimizedSLtoVLMappingProgramming);
        self.dump(F,64,96,label,offset);
        label = "LIDsPerPort=%r,partitionEnforcementCap=%r"%(self.LIDsPerPort,self.partitionEnforcementCap);
        self.dump(F,96,128,label,offset);
        label = "inboundEnforcementCap=%r,outboundEnforcementCap=%r,filterRawInboundCap=%r,filterRawOutboundCap=%r,enhancedPort0=%r,reserved2=%r,reserved3=%r"%(self.inboundEnforcementCap,self.outboundEnforcementCap,self.filterRawInboundCap,self.filterRawOutboundCap,self.enhancedPort0,self.reserved2,self.reserved3);
        self.dump(F,128,160,label,offset);

class SMPGUIDInfo(rdma.binstruct.BinStruct):
    '''Assigned GUIDs (section 14.2.5.5)'''
    __slots__ = ('GUIDBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x14
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.GUIDBlock = [IBA.GUID()]*8;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.GUIDBlock = [IBA.GUID()]*8;

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
        self._buf = buffer[offset:];
        self.GUIDBlock[0] = IBA.GUID(buffer[offset + 0:offset + 8],raw=True);
        self.GUIDBlock[1] = IBA.GUID(buffer[offset + 8:offset + 16],raw=True);
        self.GUIDBlock[2] = IBA.GUID(buffer[offset + 16:offset + 24],raw=True);
        self.GUIDBlock[3] = IBA.GUID(buffer[offset + 24:offset + 32],raw=True);
        self.GUIDBlock[4] = IBA.GUID(buffer[offset + 32:offset + 40],raw=True);
        self.GUIDBlock[5] = IBA.GUID(buffer[offset + 40:offset + 48],raw=True);
        self.GUIDBlock[6] = IBA.GUID(buffer[offset + 48:offset + 56],raw=True);
        self.GUIDBlock[7] = IBA.GUID(buffer[offset + 56:offset + 64],raw=True);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "GUIDBlock=%r"%(self.GUIDBlock);
        self.dump(F,0,512,label,offset);

class SMPPortInfo(rdma.binstruct.BinStruct):
    '''Port Information (section 14.2.5.6)'''
    __slots__ = ('MKey','GIDPrefix','LID','masterSMLID','capabilityMask','diagCode','MKeyLeasePeriod','localPortNum','linkWidthEnabled','linkWidthSupported','linkWidthActive','linkSpeedSupported','portState','portPhysicalState','linkDownDefaultState','MKeyProtectBits','reserved1','LMC','linkSpeedActive','linkSpeedEnabled','neighborMTU','masterSMSL','VLCap','initType','VLHighLimit','VLArbitrationHighCap','VLArbitrationLowCap','initTypeReply','MTUCap','VLStallCount','HOQLife','operationalVLs','partitionEnforcementInbound','partitionEnforcementOutbound','filterRawInbound','filterRawOutbound','MKeyViolations','PKeyViolations','QKeyViolations','GUIDCap','clientReregister','reserved2','subnetTimeOut','reserved3','respTimeValue','localPhyErrors','overrunErrors','reserved4');
    MAD_LENGTH = 56
    MAD_ATTRIBUTE_ID = 0x15
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
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
        self.reserved1 = 0;
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
        self.reserved2 = 0;
        self.subnetTimeOut = 0;
        self.reserved3 = 0;
        self.respTimeValue = 0;
        self.localPhyErrors = 0;
        self.overrunErrors = 0;
        self.reserved4 = 0;

    @property
    def _pack_0_32(self):
        return ((self.linkSpeedSupported & 0xF) << 28) | ((self.portState & 0xF) << 24) | ((self.portPhysicalState & 0xF) << 20) | ((self.linkDownDefaultState & 0xF) << 16) | ((self.MKeyProtectBits & 0x3) << 14) | ((self.reserved1 & 0x7) << 11) | ((self.LMC & 0x7) << 8) | ((self.linkSpeedActive & 0xF) << 4) | ((self.linkSpeedEnabled & 0xF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.linkSpeedSupported = (value >> 28) & 0xF;
        self.portState = (value >> 24) & 0xF;
        self.portPhysicalState = (value >> 20) & 0xF;
        self.linkDownDefaultState = (value >> 16) & 0xF;
        self.MKeyProtectBits = (value >> 14) & 0x3;
        self.reserved1 = (value >> 11) & 0x7;
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
        return ((self.QKeyViolations & 0xFFFF) << 16) | ((self.GUIDCap & 0xFF) << 8) | ((self.clientReregister & 0x1) << 7) | ((self.reserved2 & 0x3) << 5) | ((self.subnetTimeOut & 0x1F) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.QKeyViolations = (value >> 16) & 0xFFFF;
        self.GUIDCap = (value >> 8) & 0xFF;
        self.clientReregister = (value >> 7) & 0x1;
        self.reserved2 = (value >> 5) & 0x3;
        self.subnetTimeOut = (value >> 0) & 0x1F;

    @property
    def _pack_4_32(self):
        return ((self.reserved3 & 0x7) << 29) | ((self.respTimeValue & 0x1F) << 24) | ((self.localPhyErrors & 0xF) << 20) | ((self.overrunErrors & 0xF) << 16) | ((self.reserved4 & 0xFFFF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.reserved3 = (value >> 29) & 0x7;
        self.respTimeValue = (value >> 24) & 0x1F;
        self.localPhyErrors = (value >> 20) & 0xF;
        self.overrunErrors = (value >> 16) & 0xF;
        self.reserved4 = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QQHHLHHBBBBLLLHHLL',buffer,offset+0,self.MKey,self.GIDPrefix,self.LID,self.masterSMLID,self.capabilityMask,self.diagCode,self.MKeyLeasePeriod,self.localPortNum,self.linkWidthEnabled,self.linkWidthSupported,self.linkWidthActive,self._pack_0_32,self._pack_1_32,self._pack_2_32,self.MKeyViolations,self.PKeyViolations,self._pack_3_32,self._pack_4_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.MKey,self.GIDPrefix,self.LID,self.masterSMLID,self.capabilityMask,self.diagCode,self.MKeyLeasePeriod,self.localPortNum,self.linkWidthEnabled,self.linkWidthSupported,self.linkWidthActive,self._pack_0_32,self._pack_1_32,self._pack_2_32,self.MKeyViolations,self.PKeyViolations,self._pack_3_32,self._pack_4_32,) = struct.unpack_from('>QQHHLHHBBBBLLLHHLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "MKey=%r"%(self.MKey);
        self.dump(F,0,64,label,offset);
        label = "GIDPrefix=%r"%(self.GIDPrefix);
        self.dump(F,64,128,label,offset);
        label = "LID=%r,masterSMLID=%r"%(self.LID,self.masterSMLID);
        self.dump(F,128,160,label,offset);
        label = "capabilityMask=%r"%(self.capabilityMask);
        self.dump(F,160,192,label,offset);
        label = "diagCode=%r,MKeyLeasePeriod=%r"%(self.diagCode,self.MKeyLeasePeriod);
        self.dump(F,192,224,label,offset);
        label = "localPortNum=%r,linkWidthEnabled=%r,linkWidthSupported=%r,linkWidthActive=%r"%(self.localPortNum,self.linkWidthEnabled,self.linkWidthSupported,self.linkWidthActive);
        self.dump(F,224,256,label,offset);
        label = "linkSpeedSupported=%r,portState=%r,portPhysicalState=%r,linkDownDefaultState=%r,MKeyProtectBits=%r,reserved1=%r,LMC=%r,linkSpeedActive=%r,linkSpeedEnabled=%r"%(self.linkSpeedSupported,self.portState,self.portPhysicalState,self.linkDownDefaultState,self.MKeyProtectBits,self.reserved1,self.LMC,self.linkSpeedActive,self.linkSpeedEnabled);
        self.dump(F,256,288,label,offset);
        label = "neighborMTU=%r,masterSMSL=%r,VLCap=%r,initType=%r,VLHighLimit=%r,VLArbitrationHighCap=%r"%(self.neighborMTU,self.masterSMSL,self.VLCap,self.initType,self.VLHighLimit,self.VLArbitrationHighCap);
        self.dump(F,288,320,label,offset);
        label = "VLArbitrationLowCap=%r,initTypeReply=%r,MTUCap=%r,VLStallCount=%r,HOQLife=%r,operationalVLs=%r,partitionEnforcementInbound=%r,partitionEnforcementOutbound=%r,filterRawInbound=%r,filterRawOutbound=%r"%(self.VLArbitrationLowCap,self.initTypeReply,self.MTUCap,self.VLStallCount,self.HOQLife,self.operationalVLs,self.partitionEnforcementInbound,self.partitionEnforcementOutbound,self.filterRawInbound,self.filterRawOutbound);
        self.dump(F,320,352,label,offset);
        label = "MKeyViolations=%r,PKeyViolations=%r"%(self.MKeyViolations,self.PKeyViolations);
        self.dump(F,352,384,label,offset);
        label = "QKeyViolations=%r,GUIDCap=%r,clientReregister=%r,reserved2=%r,subnetTimeOut=%r"%(self.QKeyViolations,self.GUIDCap,self.clientReregister,self.reserved2,self.subnetTimeOut);
        self.dump(F,384,416,label,offset);
        label = "reserved3=%r,respTimeValue=%r,localPhyErrors=%r,overrunErrors=%r,reserved4=%r"%(self.reserved3,self.respTimeValue,self.localPhyErrors,self.overrunErrors,self.reserved4);
        self.dump(F,416,448,label,offset);

class SMPPKeyTable(rdma.binstruct.BinStruct):
    '''Partition Table (section 14.2.5.7)'''
    __slots__ = ('PKeyBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x16
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.PKeyBlock = [0]*32;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.PKeyBlock = [0]*32;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self.PKeyBlock[0],self.PKeyBlock[1],self.PKeyBlock[2],self.PKeyBlock[3],self.PKeyBlock[4],self.PKeyBlock[5],self.PKeyBlock[6],self.PKeyBlock[7],self.PKeyBlock[8],self.PKeyBlock[9],self.PKeyBlock[10],self.PKeyBlock[11],self.PKeyBlock[12],self.PKeyBlock[13],self.PKeyBlock[14],self.PKeyBlock[15],self.PKeyBlock[16],self.PKeyBlock[17],self.PKeyBlock[18],self.PKeyBlock[19],self.PKeyBlock[20],self.PKeyBlock[21],self.PKeyBlock[22],self.PKeyBlock[23],self.PKeyBlock[24],self.PKeyBlock[25],self.PKeyBlock[26],self.PKeyBlock[27],self.PKeyBlock[28],self.PKeyBlock[29],self.PKeyBlock[30],self.PKeyBlock[31]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.PKeyBlock[0],self.PKeyBlock[1],self.PKeyBlock[2],self.PKeyBlock[3],self.PKeyBlock[4],self.PKeyBlock[5],self.PKeyBlock[6],self.PKeyBlock[7],self.PKeyBlock[8],self.PKeyBlock[9],self.PKeyBlock[10],self.PKeyBlock[11],self.PKeyBlock[12],self.PKeyBlock[13],self.PKeyBlock[14],self.PKeyBlock[15],self.PKeyBlock[16],self.PKeyBlock[17],self.PKeyBlock[18],self.PKeyBlock[19],self.PKeyBlock[20],self.PKeyBlock[21],self.PKeyBlock[22],self.PKeyBlock[23],self.PKeyBlock[24],self.PKeyBlock[25],self.PKeyBlock[26],self.PKeyBlock[27],self.PKeyBlock[28],self.PKeyBlock[29],self.PKeyBlock[30],self.PKeyBlock[31],) = struct.unpack_from('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "PKeyBlock=%r"%(self.PKeyBlock);
        self.dump(F,0,512,label,offset);

class SMPSLToVLMappingTable(rdma.binstruct.BinStruct):
    '''Service Level to Virtual Lane mapping Information (section 14.2.5.8)'''
    __slots__ = ('SLtoVL');
    MAD_LENGTH = 8
    MAD_ATTRIBUTE_ID = 0x17
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.SLtoVL = bytearray(16);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.SLtoVL = bytearray(16);

    def pack_into(self,buffer,offset=0):
        rdma.binstruct.pack_array8(buffer,0,4,16,self.SLtoVL);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        rdma.binstruct.unpack_array8(buffer,0,4,16,self.SLtoVL);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "SLtoVL=%r"%(self.SLtoVL);
        self.dump(F,0,64,label,offset);

class SMPVLArbitrationTable(rdma.binstruct.BinStruct):
    '''List of Weights (section 14.2.5.9)'''
    __slots__ = ('VLWeightBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x18
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.VLWeightBlock = [0]*32;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.VLWeightBlock = [0]*32;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self.VLWeightBlock[0],self.VLWeightBlock[1],self.VLWeightBlock[2],self.VLWeightBlock[3],self.VLWeightBlock[4],self.VLWeightBlock[5],self.VLWeightBlock[6],self.VLWeightBlock[7],self.VLWeightBlock[8],self.VLWeightBlock[9],self.VLWeightBlock[10],self.VLWeightBlock[11],self.VLWeightBlock[12],self.VLWeightBlock[13],self.VLWeightBlock[14],self.VLWeightBlock[15],self.VLWeightBlock[16],self.VLWeightBlock[17],self.VLWeightBlock[18],self.VLWeightBlock[19],self.VLWeightBlock[20],self.VLWeightBlock[21],self.VLWeightBlock[22],self.VLWeightBlock[23],self.VLWeightBlock[24],self.VLWeightBlock[25],self.VLWeightBlock[26],self.VLWeightBlock[27],self.VLWeightBlock[28],self.VLWeightBlock[29],self.VLWeightBlock[30],self.VLWeightBlock[31]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.VLWeightBlock[0],self.VLWeightBlock[1],self.VLWeightBlock[2],self.VLWeightBlock[3],self.VLWeightBlock[4],self.VLWeightBlock[5],self.VLWeightBlock[6],self.VLWeightBlock[7],self.VLWeightBlock[8],self.VLWeightBlock[9],self.VLWeightBlock[10],self.VLWeightBlock[11],self.VLWeightBlock[12],self.VLWeightBlock[13],self.VLWeightBlock[14],self.VLWeightBlock[15],self.VLWeightBlock[16],self.VLWeightBlock[17],self.VLWeightBlock[18],self.VLWeightBlock[19],self.VLWeightBlock[20],self.VLWeightBlock[21],self.VLWeightBlock[22],self.VLWeightBlock[23],self.VLWeightBlock[24],self.VLWeightBlock[25],self.VLWeightBlock[26],self.VLWeightBlock[27],self.VLWeightBlock[28],self.VLWeightBlock[29],self.VLWeightBlock[30],self.VLWeightBlock[31],) = struct.unpack_from('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "VLWeightBlock=%r"%(self.VLWeightBlock);
        self.dump(F,0,512,label,offset);

class SMPLinearForwardingTable(rdma.binstruct.BinStruct):
    '''Linear Forwarding Table Information (section 14.2.5.10)'''
    __slots__ = ('portBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x19
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.portBlock = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.portBlock = bytearray(64);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 64] = self.portBlock

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.portBlock = buffer[offset + 0:offset + 64]

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "portBlock=%r"%(self.portBlock);
        self.dump(F,0,512,label,offset);

class SMPRandomForwardingTable(rdma.binstruct.BinStruct):
    '''Random Forwarding Table Information (section 14.2.5.11)'''
    __slots__ = ('LIDPortBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x1a
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.LIDPortBlock = [SMPLIDPortBlock()]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LIDPortBlock = [SMPLIDPortBlock()]*16;

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
        self._buf = buffer[offset:];
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

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LIDPortBlock=%r"%(self.LIDPortBlock);
        self.dump(F,0,512,label,offset);

class SMPMulticastForwardingTable(rdma.binstruct.BinStruct):
    '''Multicast Forwarding Table Information (section 14.2.5.12)'''
    __slots__ = ('portMaskBlock');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x1b
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.portMaskBlock = [0]*32;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.portMaskBlock = [0]*32;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0,self.portMaskBlock[0],self.portMaskBlock[1],self.portMaskBlock[2],self.portMaskBlock[3],self.portMaskBlock[4],self.portMaskBlock[5],self.portMaskBlock[6],self.portMaskBlock[7],self.portMaskBlock[8],self.portMaskBlock[9],self.portMaskBlock[10],self.portMaskBlock[11],self.portMaskBlock[12],self.portMaskBlock[13],self.portMaskBlock[14],self.portMaskBlock[15],self.portMaskBlock[16],self.portMaskBlock[17],self.portMaskBlock[18],self.portMaskBlock[19],self.portMaskBlock[20],self.portMaskBlock[21],self.portMaskBlock[22],self.portMaskBlock[23],self.portMaskBlock[24],self.portMaskBlock[25],self.portMaskBlock[26],self.portMaskBlock[27],self.portMaskBlock[28],self.portMaskBlock[29],self.portMaskBlock[30],self.portMaskBlock[31]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.portMaskBlock[0],self.portMaskBlock[1],self.portMaskBlock[2],self.portMaskBlock[3],self.portMaskBlock[4],self.portMaskBlock[5],self.portMaskBlock[6],self.portMaskBlock[7],self.portMaskBlock[8],self.portMaskBlock[9],self.portMaskBlock[10],self.portMaskBlock[11],self.portMaskBlock[12],self.portMaskBlock[13],self.portMaskBlock[14],self.portMaskBlock[15],self.portMaskBlock[16],self.portMaskBlock[17],self.portMaskBlock[18],self.portMaskBlock[19],self.portMaskBlock[20],self.portMaskBlock[21],self.portMaskBlock[22],self.portMaskBlock[23],self.portMaskBlock[24],self.portMaskBlock[25],self.portMaskBlock[26],self.portMaskBlock[27],self.portMaskBlock[28],self.portMaskBlock[29],self.portMaskBlock[30],self.portMaskBlock[31],) = struct.unpack_from('>HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "portMaskBlock=%r"%(self.portMaskBlock);
        self.dump(F,0,512,label,offset);

class SMPSMInfo(rdma.binstruct.BinStruct):
    '''Subnet Management Information (section 14.2.5.13)'''
    __slots__ = ('GUID','SMKey','actCount','priority','SMState','reserved1');
    MAD_LENGTH = 24
    MAD_ATTRIBUTE_ID = 0x20
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.GUID = IBA.GUID();
        self.SMKey = 0;
        self.actCount = 0;
        self.priority = 0;
        self.SMState = 0;
        self.reserved1 = 0;

    @property
    def _pack_0_32(self):
        return ((self.priority & 0xF) << 28) | ((self.SMState & 0xF) << 24) | ((self.reserved1 & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.priority = (value >> 28) & 0xF;
        self.SMState = (value >> 24) & 0xF;
        self.reserved1 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.GUID.pack_into(buffer,offset + 0);
        struct.pack_into('>QLL',buffer,offset+8,self.SMKey,self.actCount,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.GUID = IBA.GUID(buffer[offset + 0:offset + 8],raw=True);
        (self.SMKey,self.actCount,self._pack_0_32,) = struct.unpack_from('>QLL',buffer,offset+8);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "GUID=%r"%(self.GUID);
        self.dump(F,0,64,label,offset);
        label = "SMKey=%r"%(self.SMKey);
        self.dump(F,64,128,label,offset);
        label = "actCount=%r"%(self.actCount);
        self.dump(F,128,160,label,offset);
        label = "priority=%r,SMState=%r,reserved1=%r"%(self.priority,self.SMState,self.reserved1);
        self.dump(F,160,192,label,offset);

class SMPVendorDiag(rdma.binstruct.BinStruct):
    '''Vendor Specific Diagnostic (section 14.2.5.14)'''
    __slots__ = ('nextIndex','reserved1','diagData');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x30
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    def zero(self):
        self.nextIndex = 0;
        self.reserved1 = 0;
        self.diagData = bytearray(60);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 4:offset + 64] = self.diagData
        struct.pack_into('>HH',buffer,offset+0,self.nextIndex,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.diagData = buffer[offset + 4:offset + 64]
        (self.nextIndex,self.reserved1,) = struct.unpack_from('>HH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "nextIndex=%r,reserved1=%r"%(self.nextIndex,self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "diagData=%r"%(self.diagData);
        self.dump(F,32,512,label,offset);

class SMPLedInfo(rdma.binstruct.BinStruct):
    '''Turn on/off LED (section 14.2.5.15)'''
    __slots__ = ('ledMask','reserved1');
    MAD_LENGTH = 4
    MAD_ATTRIBUTE_ID = 0x31
    MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.ledMask = 0;
        self.reserved1 = 0;

    @property
    def _pack_0_32(self):
        return ((self.ledMask & 0x1) << 31) | ((self.reserved1 & 0x7FFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.ledMask = (value >> 31) & 0x1;
        self.reserved1 = (value >> 0) & 0x7FFFFFFF;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "ledMask=%r,reserved1=%r"%(self.ledMask,self.reserved1);
        self.dump(F,0,32,label,offset);

class SAHeader(rdma.binstruct.BinStruct):
    '''SA Header (section 15.2.1.1)'''
    __slots__ = ('RMPPHeader','SMKey','attributeOffset','reserved1','componentMask');
    MAD_LENGTH = 56
    MAD_CLASS = 0x3
    MAD_CLASS_VERSION = 0x2
    def __init__(self,*args):
        self.RMPPHeader = RMPPHeader();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.RMPPHeader = RMPPHeader();
        self.SMKey = 0;
        self.attributeOffset = 0;
        self.reserved1 = 0;
        self.componentMask = 0;

    def pack_into(self,buffer,offset=0):
        self.RMPPHeader.pack_into(buffer,offset + 0);
        struct.pack_into('>QHHQ',buffer,offset+36,self.SMKey,self.attributeOffset,self.reserved1,self.componentMask);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.RMPPHeader.unpack_from(buffer,offset + 0);
        (self.SMKey,self.attributeOffset,self.reserved1,self.componentMask,) = struct.unpack_from('>QHHQ',buffer,offset+36);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "RMPPHeader=%r"%(self.RMPPHeader);
        self.dump(F,0,288,label,offset);
        label = "SMKey=%r"%(self.SMKey);
        self.dump(F,288,352,label,offset);
        label = "attributeOffset=%r,reserved1=%r"%(self.attributeOffset,self.reserved1);
        self.dump(F,352,384,label,offset);
        label = "componentMask=%r"%(self.componentMask);
        self.dump(F,384,448,label,offset);

class SAFormat(BinFormat):
    '''SA Format (section 15.2.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier','RMPPVersion','RMPPType','RRespTime','RMPPFlags','RMPPStatus','data1','data2','SMKey','attributeOffset','reserved2','componentMask','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x3
    MAD_CLASS_VERSION = 0x2
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
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
        self.reserved2 = 0;
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
        struct.pack_into('>BBBBHHQHHLLLLQHHQ',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self.SMKey,self.attributeOffset,self.reserved2,self.componentMask);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.data = buffer[offset + 56:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,self._pack_0_32,self.data1,self.data2,self.SMKey,self.attributeOffset,self.reserved2,self.componentMask,) = struct.unpack_from('>BBBBHHQHHLLLLQHHQ',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        label = "RMPPVersion=%r,RMPPType=%r,RRespTime=%r,RMPPFlags=%r,RMPPStatus=%r"%(self.RMPPVersion,self.RMPPType,self.RRespTime,self.RMPPFlags,self.RMPPStatus);
        self.dump(F,192,224,label,offset);
        label = "data1=%r"%(self.data1);
        self.dump(F,224,256,label,offset);
        label = "data2=%r"%(self.data2);
        self.dump(F,256,288,label,offset);
        label = "SMKey=%r"%(self.SMKey);
        self.dump(F,288,352,label,offset);
        label = "attributeOffset=%r,reserved2=%r"%(self.attributeOffset,self.reserved2);
        self.dump(F,352,384,label,offset);
        label = "componentMask=%r"%(self.componentMask);
        self.dump(F,384,448,label,offset);
        self._format_data(F,448,2048,offset);

class SANodeRecord(rdma.binstruct.BinStruct):
    '''Container for NodeInfo (section 15.2.5.2)'''
    __slots__ = ('LID','reserved1','nodeInfo','nodeDescription');
    MAD_LENGTH = 108
    MAD_ATTRIBUTE_ID = 0x11
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved1':1, 'nodeInfo.baseVersion':2, 'nodeInfo.classVersion':3, 'nodeInfo.nodeType':4, 'nodeInfo.numPorts':5, 'nodeInfo.systemImageGUID':6, 'nodeInfo.nodeGUID':7, 'nodeInfo.portGUID':8, 'nodeInfo.partitionCap':9, 'nodeInfo.deviceID':10, 'nodeInfo.revision':11, 'nodeInfo.localPortNum':12, 'nodeInfo.vendorID':13, 'nodeDescription.nodeString':14}
    def __init__(self,*args):
        self.nodeInfo = SMPNodeInfo();
        self.nodeDescription = SMPNodeDescription();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved1 = 0;
        self.nodeInfo = SMPNodeInfo();
        self.nodeDescription = SMPNodeDescription();

    def pack_into(self,buffer,offset=0):
        self.nodeInfo.pack_into(buffer,offset + 4);
        self.nodeDescription.pack_into(buffer,offset + 44);
        struct.pack_into('>HH',buffer,offset+0,self.LID,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.nodeInfo.unpack_from(buffer,offset + 4);
        self.nodeDescription.unpack_from(buffer,offset + 44);
        (self.LID,self.reserved1,) = struct.unpack_from('>HH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,reserved1=%r"%(self.LID,self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "nodeInfo=%r"%(self.nodeInfo);
        self.dump(F,32,352,label,offset);
        label = "nodeDescription=%r"%(self.nodeDescription);
        self.dump(F,352,864,label,offset);

class SAPortInfoRecord(rdma.binstruct.BinStruct):
    '''Container for PortInfo (section 15.2.5.3)'''
    __slots__ = ('endportLID','portNum','reserved1','portInfo');
    MAD_LENGTH = 60
    MAD_ATTRIBUTE_ID = 0x12
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'endportLID':0, 'portNum':1, 'reserved1':2, 'portInfo.MKey':3, 'portInfo.GIDPrefix':4, 'portInfo.LID':5, 'portInfo.masterSMLID':6, 'portInfo.capabilityMask':7, 'portInfo.diagCode':8, 'portInfo.MKeyLeasePeriod':9, 'portInfo.localPortNum':10, 'portInfo.linkWidthEnabled':11, 'portInfo.linkWidthSupported':12, 'portInfo.linkWidthActive':13, 'portInfo.linkSpeedSupported':14, 'portInfo.portState':15, 'portInfo.portPhysicalState':16, 'portInfo.linkDownDefaultState':17, 'portInfo.MKeyProtectBits':18, 'portInfo.reserved1':19, 'portInfo.LMC':20, 'portInfo.linkSpeedActive':21, 'portInfo.linkSpeedEnabled':22, 'portInfo.neighborMTU':23, 'portInfo.masterSMSL':24, 'portInfo.VLCap':25, 'portInfo.initType':26, 'portInfo.VLHighLimit':27, 'portInfo.VLArbitrationHighCap':28, 'portInfo.VLArbitrationLowCap':29, 'portInfo.initTypeReply':30, 'portInfo.MTUCap':31, 'portInfo.VLStallCount':32, 'portInfo.HOQLife':33, 'portInfo.operationalVLs':34, 'portInfo.partitionEnforcementInbound':35, 'portInfo.partitionEnforcementOutbound':36, 'portInfo.filterRawInbound':37, 'portInfo.filterRawOutbound':38, 'portInfo.MKeyViolations':39, 'portInfo.PKeyViolations':40, 'portInfo.QKeyViolations':41, 'portInfo.GUIDCap':42, 'portInfo.clientReregister':43, 'portInfo.reserved2':44, 'portInfo.subnetTimeOut':45, 'portInfo.reserved3':46, 'portInfo.respTimeValue':47, 'portInfo.localPhyErrors':48, 'portInfo.overrunErrors':49, 'portInfo.reserved4':50}
    def __init__(self,*args):
        self.portInfo = SMPPortInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.endportLID = 0;
        self.portNum = 0;
        self.reserved1 = 0;
        self.portInfo = SMPPortInfo();

    def pack_into(self,buffer,offset=0):
        self.portInfo.pack_into(buffer,offset + 4);
        struct.pack_into('>HBB',buffer,offset+0,self.endportLID,self.portNum,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.portInfo.unpack_from(buffer,offset + 4);
        (self.endportLID,self.portNum,self.reserved1,) = struct.unpack_from('>HBB',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "endportLID=%r,portNum=%r,reserved1=%r"%(self.endportLID,self.portNum,self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "portInfo=%r"%(self.portInfo);
        self.dump(F,32,480,label,offset);

class SASLToVLMappingTableRecord(rdma.binstruct.BinStruct):
    '''Container for SLtoVLMappingTable entry (section 15.2.5.4)'''
    __slots__ = ('LID','inputPortNum','outputPortNum','reserved1','SLToVLMappingTable');
    MAD_LENGTH = 16
    MAD_ATTRIBUTE_ID = 0x13
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'inputPortNum':1, 'outputPortNum':2, 'reserved1':3, 'SLToVLMappingTable.SLtoVL':4}
    def __init__(self,*args):
        self.SLToVLMappingTable = SMPSLToVLMappingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.inputPortNum = 0;
        self.outputPortNum = 0;
        self.reserved1 = 0;
        self.SLToVLMappingTable = SMPSLToVLMappingTable();

    def pack_into(self,buffer,offset=0):
        self.SLToVLMappingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HBBL',buffer,offset+0,self.LID,self.inputPortNum,self.outputPortNum,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.SLToVLMappingTable.unpack_from(buffer,offset + 8);
        (self.LID,self.inputPortNum,self.outputPortNum,self.reserved1,) = struct.unpack_from('>HBBL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,inputPortNum=%r,outputPortNum=%r"%(self.LID,self.inputPortNum,self.outputPortNum);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "SLToVLMappingTable=%r"%(self.SLToVLMappingTable);
        self.dump(F,64,128,label,offset);

class SASwitchInfoRecord(rdma.binstruct.BinStruct):
    '''Container for SwitchInfo (section 15.2.5.5)'''
    __slots__ = ('LID','reserved1','switchInfo');
    MAD_LENGTH = 24
    MAD_ATTRIBUTE_ID = 0x14
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved1':1, 'switchInfo.linearFDBCap':2, 'switchInfo.randomFDBCap':3, 'switchInfo.multicastFDBCap':4, 'switchInfo.linearFDBTop':5, 'switchInfo.defaultPort':6, 'switchInfo.defaultMulticastPrimaryPort':7, 'switchInfo.defaultMulticastNotPrimaryPort':8, 'switchInfo.lifeTimeValue':9, 'switchInfo.portStateChange':10, 'switchInfo.reserved1':11, 'switchInfo.optimizedSLtoVLMappingProgramming':12, 'switchInfo.LIDsPerPort':13, 'switchInfo.partitionEnforcementCap':14, 'switchInfo.inboundEnforcementCap':15, 'switchInfo.outboundEnforcementCap':16, 'switchInfo.filterRawInboundCap':17, 'switchInfo.filterRawOutboundCap':18, 'switchInfo.enhancedPort0':19, 'switchInfo.reserved2':20, 'switchInfo.reserved3':21}
    def __init__(self,*args):
        self.switchInfo = SMPSwitchInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved1 = 0;
        self.switchInfo = SMPSwitchInfo();

    def pack_into(self,buffer,offset=0):
        self.switchInfo.pack_into(buffer,offset + 4);
        struct.pack_into('>HH',buffer,offset+0,self.LID,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.switchInfo.unpack_from(buffer,offset + 4);
        (self.LID,self.reserved1,) = struct.unpack_from('>HH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,reserved1=%r"%(self.LID,self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "switchInfo=%r"%(self.switchInfo);
        self.dump(F,32,192,label,offset);

class SALinearForwardingTableRecord(rdma.binstruct.BinStruct):
    '''Container for LinearForwardingTable entry (section 15.2.5.6)'''
    __slots__ = ('LID','blockNum','reserved1','linearForwardingTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x15
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved1':2, 'linearForwardingTable.portBlock':3}
    def __init__(self,*args):
        self.linearForwardingTable = SMPLinearForwardingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.reserved1 = 0;
        self.linearForwardingTable = SMPLinearForwardingTable();

    def pack_into(self,buffer,offset=0):
        self.linearForwardingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HHL',buffer,offset+0,self.LID,self.blockNum,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.linearForwardingTable.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self.reserved1,) = struct.unpack_from('>HHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,blockNum=%r"%(self.LID,self.blockNum);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "linearForwardingTable=%r"%(self.linearForwardingTable);
        self.dump(F,64,576,label,offset);

class SARandomForwardingTableRecord(rdma.binstruct.BinStruct):
    '''Container for RandomForwardingTable entry (section 15.2.5.7)'''
    __slots__ = ('LID','blockNum','reserved1','randomForwardingTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x16
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved1':2, 'randomForwardingTable.LIDPortBlock':3}
    def __init__(self,*args):
        self.randomForwardingTable = SMPRandomForwardingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.reserved1 = 0;
        self.randomForwardingTable = SMPRandomForwardingTable();

    def pack_into(self,buffer,offset=0):
        self.randomForwardingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HHL',buffer,offset+0,self.LID,self.blockNum,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.randomForwardingTable.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self.reserved1,) = struct.unpack_from('>HHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,blockNum=%r"%(self.LID,self.blockNum);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "randomForwardingTable=%r"%(self.randomForwardingTable);
        self.dump(F,64,576,label,offset);

class SAMulticastForwardingTableRecord(rdma.binstruct.BinStruct):
    '''Container for MulticastForwardingTable entry (section 15.2.5.8)'''
    __slots__ = ('LID','reserved1','position','blockNum','reserved2','multicastForwardingTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x17
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved1':1, 'position':2, 'blockNum':3, 'reserved2':4, 'multicastForwardingTable.portMaskBlock':5}
    def __init__(self,*args):
        self.multicastForwardingTable = SMPMulticastForwardingTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved1 = 0;
        self.position = 0;
        self.blockNum = 0;
        self.reserved2 = 0;
        self.multicastForwardingTable = SMPMulticastForwardingTable();

    @property
    def _pack_0_32(self):
        return ((self.LID & 0xFFFF) << 16) | ((self.reserved1 & 0x3) << 14) | ((self.position & 0xF) << 10) | ((self.blockNum & 0x3FF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.LID = (value >> 16) & 0xFFFF;
        self.reserved1 = (value >> 14) & 0x3;
        self.position = (value >> 10) & 0xF;
        self.blockNum = (value >> 0) & 0x3FF;

    def pack_into(self,buffer,offset=0):
        self.multicastForwardingTable.pack_into(buffer,offset + 8);
        struct.pack_into('>LL',buffer,offset+0,self._pack_0_32,self.reserved2);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.multicastForwardingTable.unpack_from(buffer,offset + 8);
        (self._pack_0_32,self.reserved2,) = struct.unpack_from('>LL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,reserved1=%r,position=%r,blockNum=%r"%(self.LID,self.reserved1,self.position,self.blockNum);
        self.dump(F,0,32,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,32,64,label,offset);
        label = "multicastForwardingTable=%r"%(self.multicastForwardingTable);
        self.dump(F,64,576,label,offset);

class SAVLArbitrationTableRecord(rdma.binstruct.BinStruct):
    '''Container for VLArbitrationTable entry (section 15.2.5.9)'''
    __slots__ = ('LID','outputPortNum','blockNum','reserved1','VLArbitrationTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x36
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'outputPortNum':1, 'blockNum':2, 'reserved1':3, 'VLArbitrationTable.VLWeightBlock':4}
    def __init__(self,*args):
        self.VLArbitrationTable = SMPVLArbitrationTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.outputPortNum = 0;
        self.blockNum = 0;
        self.reserved1 = 0;
        self.VLArbitrationTable = SMPVLArbitrationTable();

    def pack_into(self,buffer,offset=0):
        self.VLArbitrationTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HBBL',buffer,offset+0,self.LID,self.outputPortNum,self.blockNum,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.VLArbitrationTable.unpack_from(buffer,offset + 8);
        (self.LID,self.outputPortNum,self.blockNum,self.reserved1,) = struct.unpack_from('>HBBL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,outputPortNum=%r,blockNum=%r"%(self.LID,self.outputPortNum,self.blockNum);
        self.dump(F,0,32,label,offset);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "VLArbitrationTable=%r"%(self.VLArbitrationTable);
        self.dump(F,64,576,label,offset);

class SASMInfoRecord(rdma.binstruct.BinStruct):
    '''Container for SMInfo (section 15.2.5.10)'''
    __slots__ = ('LID','reserved1','SMInfo');
    MAD_LENGTH = 28
    MAD_ATTRIBUTE_ID = 0x18
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'reserved1':1, 'SMInfo.GUID':2, 'SMInfo.SMKey':3, 'SMInfo.actCount':4, 'SMInfo.priority':5, 'SMInfo.SMState':6, 'SMInfo.reserved1':7}
    def __init__(self,*args):
        self.SMInfo = SMPSMInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.reserved1 = 0;
        self.SMInfo = SMPSMInfo();

    def pack_into(self,buffer,offset=0):
        self.SMInfo.pack_into(buffer,offset + 4);
        struct.pack_into('>HH',buffer,offset+0,self.LID,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.SMInfo.unpack_from(buffer,offset + 4);
        (self.LID,self.reserved1,) = struct.unpack_from('>HH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,reserved1=%r"%(self.LID,self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "SMInfo=%r"%(self.SMInfo);
        self.dump(F,32,224,label,offset);

class SAInformInfoRecord(rdma.binstruct.BinStruct):
    '''Container for InformInfo (section 15.2.5.12)'''
    __slots__ = ('subscriberGID','enumeration','reserved1','reserved2','informInfo','reserved3');
    MAD_LENGTH = 80
    MAD_ATTRIBUTE_ID = 0xf3
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'subscriberGID':0, 'enumeration':1, 'reserved1':2, 'reserved2':3, 'informInfo.GID':4, 'informInfo.LIDRangeBegin':5, 'informInfo.LIDRangeEnd':6, 'informInfo.reserved1':7, 'informInfo.isGeneric':8, 'informInfo.subscribe':9, 'informInfo.type':10, 'informInfo.trapNumber':11, 'informInfo.QPN':12, 'informInfo.reserved2':13, 'informInfo.respTimeValue':14, 'informInfo.reserved3':15, 'informInfo.producerType':16, 'reserved3':17}
    def __init__(self,*args):
        self.informInfo = MADInformInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.subscriberGID = IBA.GID();
        self.enumeration = 0;
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.informInfo = MADInformInfo();
        self.reserved3 = bytearray(20);

    def pack_into(self,buffer,offset=0):
        self.subscriberGID.pack_into(buffer,offset + 0);
        self.informInfo.pack_into(buffer,offset + 24);
        buffer[offset + 60:offset + 80] = self.reserved3
        struct.pack_into('>HHL',buffer,offset+16,self.enumeration,self.reserved1,self.reserved2);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.subscriberGID = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        self.informInfo.unpack_from(buffer,offset + 24);
        self.reserved3 = buffer[offset + 60:offset + 80]
        (self.enumeration,self.reserved1,self.reserved2,) = struct.unpack_from('>HHL',buffer,offset+16);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "subscriberGID=%r"%(self.subscriberGID);
        self.dump(F,0,128,label,offset);
        label = "enumeration=%r,reserved1=%r"%(self.enumeration,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,160,192,label,offset);
        label = "informInfo=%r"%(self.informInfo);
        self.dump(F,192,480,label,offset);
        label = "reserved3=%r"%(self.reserved3);
        self.dump(F,480,640,label,offset);

class SALinkRecord(rdma.binstruct.BinStruct):
    '''Inter-node linkage information (section 15.2.5.13)'''
    __slots__ = ('fromLID','fromPort','toPort','toLID','reserved1');
    MAD_LENGTH = 8
    MAD_ATTRIBUTE_ID = 0x20
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'fromLID':0, 'fromPort':1, 'toPort':2, 'toLID':3, 'reserved1':4}
    def zero(self):
        self.fromLID = 0;
        self.fromPort = 0;
        self.toPort = 0;
        self.toLID = 0;
        self.reserved1 = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HBBHH',buffer,offset+0,self.fromLID,self.fromPort,self.toPort,self.toLID,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.fromLID,self.fromPort,self.toPort,self.toLID,self.reserved1,) = struct.unpack_from('>HBBHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "fromLID=%r,fromPort=%r,toPort=%r"%(self.fromLID,self.fromPort,self.toPort);
        self.dump(F,0,32,label,offset);
        label = "toLID=%r,reserved1=%r"%(self.toLID,self.reserved1);
        self.dump(F,32,64,label,offset);

class SAGUIDInfoRecord(rdma.binstruct.BinStruct):
    '''Container for port GUIDInfo (section 15.2.5.18)'''
    __slots__ = ('LID','blockNum','reserved1','reserved2','GUIDInfo');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x30
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved1':2, 'reserved2':3, 'GUIDInfo.GUIDBlock':4}
    def __init__(self,*args):
        self.GUIDInfo = SMPGUIDInfo();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.GUIDInfo = SMPGUIDInfo();

    def pack_into(self,buffer,offset=0):
        self.GUIDInfo.pack_into(buffer,offset + 8);
        struct.pack_into('>HBBL',buffer,offset+0,self.LID,self.blockNum,self.reserved1,self.reserved2);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.GUIDInfo.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self.reserved1,self.reserved2,) = struct.unpack_from('>HBBL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,blockNum=%r,reserved1=%r"%(self.LID,self.blockNum,self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,32,64,label,offset);
        label = "GUIDInfo=%r"%(self.GUIDInfo);
        self.dump(F,64,576,label,offset);

class SAServiceRecord(rdma.binstruct.BinStruct):
    '''Information on advertised services (section 15.2.5.14)'''
    __slots__ = ('serviceID','serviceGID','servicePKey','reserved1','serviceLease','serviceKey','serviceName','serviceData8','serviceData16','serviceData32','serviceData64');
    MAD_LENGTH = 176
    MAD_ATTRIBUTE_ID = 0x31
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    COMPONENT_MASK = {'serviceID':0, 'serviceGID':1, 'servicePKey':2, 'reserved1':3, 'serviceLease':4, 'serviceKey':5, 'serviceName':6, 'serviceData8':7, 'serviceData16':8, 'serviceData32':9, 'serviceData64':10}
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
        self.reserved1 = 0;
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
        rdma.binstruct.pack_array8(buffer,160,64,2,self.serviceData64);
        struct.pack_into('>Q',buffer,offset+0,self.serviceID);
        struct.pack_into('>HHL',buffer,offset+24,self.servicePKey,self.reserved1,self.serviceLease);
        struct.pack_into('>HHHHHHHHLLLL',buffer,offset+128,self.serviceData16[0],self.serviceData16[1],self.serviceData16[2],self.serviceData16[3],self.serviceData16[4],self.serviceData16[5],self.serviceData16[6],self.serviceData16[7],self.serviceData32[0],self.serviceData32[1],self.serviceData32[2],self.serviceData32[3]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.serviceGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.serviceKey = IBA.GID(buffer[offset + 32:offset + 48],raw=True);
        self.serviceName = buffer[offset + 48:offset + 112]
        self.serviceData8 = buffer[offset + 112:offset + 128]
        rdma.binstruct.unpack_array8(buffer,160,64,2,self.serviceData64);
        (self.serviceID,) = struct.unpack_from('>Q',buffer,offset+0);
        (self.servicePKey,self.reserved1,self.serviceLease,) = struct.unpack_from('>HHL',buffer,offset+24);
        (self.serviceData16[0],self.serviceData16[1],self.serviceData16[2],self.serviceData16[3],self.serviceData16[4],self.serviceData16[5],self.serviceData16[6],self.serviceData16[7],self.serviceData32[0],self.serviceData32[1],self.serviceData32[2],self.serviceData32[3],) = struct.unpack_from('>HHHHHHHHLLLL',buffer,offset+128);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "serviceID=%r"%(self.serviceID);
        self.dump(F,0,64,label,offset);
        label = "serviceGID=%r"%(self.serviceGID);
        self.dump(F,64,192,label,offset);
        label = "servicePKey=%r,reserved1=%r"%(self.servicePKey,self.reserved1);
        self.dump(F,192,224,label,offset);
        label = "serviceLease=%r"%(self.serviceLease);
        self.dump(F,224,256,label,offset);
        label = "serviceKey=%r"%(self.serviceKey);
        self.dump(F,256,384,label,offset);
        label = "serviceName=%r"%(self.serviceName);
        self.dump(F,384,896,label,offset);
        label = "serviceData8=%r"%(self.serviceData8);
        self.dump(F,896,1024,label,offset);
        label = "serviceData16=%r"%(self.serviceData16);
        self.dump(F,1024,1152,label,offset);
        label = "serviceData32=%r"%(self.serviceData32);
        self.dump(F,1152,1280,label,offset);
        label = "serviceData64=%r"%(self.serviceData64);
        self.dump(F,1280,1408,label,offset);

class SAPKeyTableRecord(rdma.binstruct.BinStruct):
    '''Container for P_Key Table (section 15.2.5.11)'''
    __slots__ = ('LID','blockNum','portNum','reserved1','PKeyTable');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x33
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'LID':0, 'blockNum':1, 'portNum':2, 'reserved1':3, 'PKeyTable.PKeyBlock':4}
    def __init__(self,*args):
        self.PKeyTable = SMPPKeyTable();
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.LID = 0;
        self.blockNum = 0;
        self.portNum = 0;
        self.reserved1 = 0;
        self.PKeyTable = SMPPKeyTable();

    @property
    def _pack_0_32(self):
        return ((self.portNum & 0xFF) << 24) | ((self.reserved1 & 0xFFFFFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.portNum = (value >> 24) & 0xFF;
        self.reserved1 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.PKeyTable.pack_into(buffer,offset + 8);
        struct.pack_into('>HHL',buffer,offset+0,self.LID,self.blockNum,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.PKeyTable.unpack_from(buffer,offset + 8);
        (self.LID,self.blockNum,self._pack_0_32,) = struct.unpack_from('>HHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "LID=%r,blockNum=%r"%(self.LID,self.blockNum);
        self.dump(F,0,32,label,offset);
        label = "portNum=%r,reserved1=%r"%(self.portNum,self.reserved1);
        self.dump(F,32,64,label,offset);
        label = "PKeyTable=%r"%(self.PKeyTable);
        self.dump(F,64,576,label,offset);

class SAPathRecord(rdma.binstruct.BinStruct):
    '''Information on paths through the subnet (section 15.2.5.16)'''
    __slots__ = ('reserved1','reserved2','DGID','SGID','DLID','SLID','rawTraffic','reserved3','flowLabel','hopLimit','TClass','reversible','numbPath','PKey','reserved4','SL','MTUSelector','MTU','rateSelector','rate','packetLifeTimeSelector','packetLifeTime','preference','reserved5','reserved6');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x35
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'reserved1':0, 'reserved2':1, 'DGID':2, 'SGID':3, 'DLID':4, 'SLID':5, 'rawTraffic':6, 'reserved3':7, 'flowLabel':8, 'hopLimit':9, 'TClass':10, 'reversible':11, 'numbPath':12, 'PKey':13, 'reserved4':14, 'SL':15, 'MTUSelector':16, 'MTU':17, 'rateSelector':18, 'rate':19, 'packetLifeTimeSelector':20, 'packetLifeTime':21, 'preference':22, 'reserved5':23, 'reserved6':24}
    def zero(self):
        self.reserved1 = 0;
        self.reserved2 = 0;
        self.DGID = IBA.GID();
        self.SGID = IBA.GID();
        self.DLID = 0;
        self.SLID = 0;
        self.rawTraffic = 0;
        self.reserved3 = 0;
        self.flowLabel = 0;
        self.hopLimit = 0;
        self.TClass = 0;
        self.reversible = 0;
        self.numbPath = 0;
        self.PKey = 0;
        self.reserved4 = 0;
        self.SL = 0;
        self.MTUSelector = 0;
        self.MTU = 0;
        self.rateSelector = 0;
        self.rate = 0;
        self.packetLifeTimeSelector = 0;
        self.packetLifeTime = 0;
        self.preference = 0;
        self.reserved5 = 0;
        self.reserved6 = 0;

    @property
    def _pack_0_32(self):
        return ((self.rawTraffic & 0x1) << 31) | ((self.reserved3 & 0x7) << 28) | ((self.flowLabel & 0xFFFFF) << 8) | ((self.hopLimit & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.rawTraffic = (value >> 31) & 0x1;
        self.reserved3 = (value >> 28) & 0x7;
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
        return ((self.reserved4 & 0xFFF) << 20) | ((self.SL & 0xF) << 16) | ((self.MTUSelector & 0x3) << 14) | ((self.MTU & 0x3F) << 8) | ((self.rateSelector & 0x3) << 6) | ((self.rate & 0x3F) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved4 = (value >> 20) & 0xFFF;
        self.SL = (value >> 16) & 0xF;
        self.MTUSelector = (value >> 14) & 0x3;
        self.MTU = (value >> 8) & 0x3F;
        self.rateSelector = (value >> 6) & 0x3;
        self.rate = (value >> 0) & 0x3F;

    @property
    def _pack_3_32(self):
        return ((self.packetLifeTimeSelector & 0x3) << 30) | ((self.packetLifeTime & 0x3F) << 24) | ((self.preference & 0xFF) << 16) | ((self.reserved5 & 0xFFFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.packetLifeTimeSelector = (value >> 30) & 0x3;
        self.packetLifeTime = (value >> 24) & 0x3F;
        self.preference = (value >> 16) & 0xFF;
        self.reserved5 = (value >> 0) & 0xFFFF;

    def pack_into(self,buffer,offset=0):
        self.DGID.pack_into(buffer,offset + 8);
        self.SGID.pack_into(buffer,offset + 24);
        struct.pack_into('>LL',buffer,offset+0,self.reserved1,self.reserved2);
        struct.pack_into('>HHLLLLL',buffer,offset+40,self.DLID,self.SLID,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self.reserved6);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.DGID = IBA.GID(buffer[offset + 8:offset + 24],raw=True);
        self.SGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        (self.reserved1,self.reserved2,) = struct.unpack_from('>LL',buffer,offset+0);
        (self.DLID,self.SLID,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self.reserved6,) = struct.unpack_from('>HHLLLLL',buffer,offset+40);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r"%(self.reserved1);
        self.dump(F,0,32,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,32,64,label,offset);
        label = "DGID=%r"%(self.DGID);
        self.dump(F,64,192,label,offset);
        label = "SGID=%r"%(self.SGID);
        self.dump(F,192,320,label,offset);
        label = "DLID=%r,SLID=%r"%(self.DLID,self.SLID);
        self.dump(F,320,352,label,offset);
        label = "rawTraffic=%r,reserved3=%r,flowLabel=%r,hopLimit=%r"%(self.rawTraffic,self.reserved3,self.flowLabel,self.hopLimit);
        self.dump(F,352,384,label,offset);
        label = "TClass=%r,reversible=%r,numbPath=%r,PKey=%r"%(self.TClass,self.reversible,self.numbPath,self.PKey);
        self.dump(F,384,416,label,offset);
        label = "reserved4=%r,SL=%r,MTUSelector=%r,MTU=%r,rateSelector=%r,rate=%r"%(self.reserved4,self.SL,self.MTUSelector,self.MTU,self.rateSelector,self.rate);
        self.dump(F,416,448,label,offset);
        label = "packetLifeTimeSelector=%r,packetLifeTime=%r,preference=%r,reserved5=%r"%(self.packetLifeTimeSelector,self.packetLifeTime,self.preference,self.reserved5);
        self.dump(F,448,480,label,offset);
        label = "reserved6=%r"%(self.reserved6);
        self.dump(F,480,512,label,offset);

class SAMCMemberRecord(rdma.binstruct.BinStruct):
    '''Multicast member attribute (section 15.2.5.17)'''
    __slots__ = ('MGID','portGID','requesterGID','QKey','MLID','MTUSelector','MTU','TClass','PKey','rateSelector','rate','packetLifeTimeSelector','packetLifeTime','SL','flowLabel','hopLimit','scope','joinState','reserved1');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x38
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    COMPONENT_MASK = {'MGID':0, 'portGID':1, 'requesterGID':2, 'QKey':3, 'MLID':4, 'MTUSelector':5, 'MTU':6, 'TClass':7, 'PKey':8, 'rateSelector':9, 'rate':10, 'packetLifeTimeSelector':11, 'packetLifeTime':12, 'SL':13, 'flowLabel':14, 'hopLimit':15, 'scope':16, 'joinState':17, 'reserved1':18}
    def zero(self):
        self.MGID = IBA.GID();
        self.portGID = IBA.GID();
        self.requesterGID = IBA.GID();
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
        self.reserved1 = 0;

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
        return ((self.scope & 0xF) << 28) | ((self.joinState & 0xF) << 24) | ((self.reserved1 & 0xFFFFFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.scope = (value >> 28) & 0xF;
        self.joinState = (value >> 24) & 0xF;
        self.reserved1 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.MGID.pack_into(buffer,offset + 0);
        self.portGID.pack_into(buffer,offset + 16);
        self.requesterGID.pack_into(buffer,offset + 32);
        struct.pack_into('>LLLLL',buffer,offset+48,self.QKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.MGID = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        self.portGID = IBA.GID(buffer[offset + 16:offset + 32],raw=True);
        self.requesterGID = IBA.GID(buffer[offset + 32:offset + 48],raw=True);
        (self.QKey,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,) = struct.unpack_from('>LLLLL',buffer,offset+48);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "MGID=%r"%(self.MGID);
        self.dump(F,0,128,label,offset);
        label = "portGID=%r"%(self.portGID);
        self.dump(F,128,256,label,offset);
        label = "requesterGID=%r"%(self.requesterGID);
        self.dump(F,256,384,label,offset);
        label = "QKey=%r"%(self.QKey);
        self.dump(F,384,416,label,offset);
        label = "MLID=%r,MTUSelector=%r,MTU=%r,TClass=%r"%(self.MLID,self.MTUSelector,self.MTU,self.TClass);
        self.dump(F,416,448,label,offset);
        label = "PKey=%r,rateSelector=%r,rate=%r,packetLifeTimeSelector=%r,packetLifeTime=%r"%(self.PKey,self.rateSelector,self.rate,self.packetLifeTimeSelector,self.packetLifeTime);
        self.dump(F,448,480,label,offset);
        label = "SL=%r,flowLabel=%r,hopLimit=%r"%(self.SL,self.flowLabel,self.hopLimit);
        self.dump(F,480,512,label,offset);
        label = "scope=%r,joinState=%r,reserved1=%r"%(self.scope,self.joinState,self.reserved1);
        self.dump(F,512,544,label,offset);

class SATraceRecord(rdma.binstruct.BinStruct):
    '''Path trace information (section 15.2.5.19)'''
    __slots__ = ('GIDPrefix','IDGeneration','reserved1','nodeType','nodeID','chassisID','entryPortID','exitPortID','entryPort','exitPort','reserved2');
    MAD_LENGTH = 48
    MAD_ATTRIBUTE_ID = 0x39
    MAD_SUBNADMGETTRACETABLE = 0x13 # MAD_METHOD_GET_TRACE_TABLE
    COMPONENT_MASK = {'GIDPrefix':0, 'IDGeneration':1, 'reserved1':2, 'nodeType':3, 'nodeID':4, 'chassisID':5, 'entryPortID':6, 'exitPortID':7, 'entryPort':8, 'exitPort':9, 'reserved2':10}
    def zero(self):
        self.GIDPrefix = 0;
        self.IDGeneration = 0;
        self.reserved1 = 0;
        self.nodeType = 0;
        self.nodeID = 0;
        self.chassisID = 0;
        self.entryPortID = 0;
        self.exitPortID = 0;
        self.entryPort = 0;
        self.exitPort = 0;
        self.reserved2 = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>QHBBQQQQBBH',buffer,offset+0,self.GIDPrefix,self.IDGeneration,self.reserved1,self.nodeType,self.nodeID,self.chassisID,self.entryPortID,self.exitPortID,self.entryPort,self.exitPort,self.reserved2);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.GIDPrefix,self.IDGeneration,self.reserved1,self.nodeType,self.nodeID,self.chassisID,self.entryPortID,self.exitPortID,self.entryPort,self.exitPort,self.reserved2,) = struct.unpack_from('>QHBBQQQQBBH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "GIDPrefix=%r"%(self.GIDPrefix);
        self.dump(F,0,64,label,offset);
        label = "IDGeneration=%r,reserved1=%r,nodeType=%r"%(self.IDGeneration,self.reserved1,self.nodeType);
        self.dump(F,64,96,label,offset);
        label = "nodeID=%r"%(self.nodeID);
        self.dump(F,96,160,label,offset);
        label = "chassisID=%r"%(self.chassisID);
        self.dump(F,160,224,label,offset);
        label = "entryPortID=%r"%(self.entryPortID);
        self.dump(F,224,288,label,offset);
        label = "exitPortID=%r"%(self.exitPortID);
        self.dump(F,288,352,label,offset);
        label = "entryPort=%r,exitPort=%r,reserved2=%r"%(self.entryPort,self.exitPort,self.reserved2);
        self.dump(F,352,384,label,offset);

class SAMultiPathRecord(rdma.binstruct.BinStruct):
    '''Request for multiple paths (section 15.2.5.20)'''
    __slots__ = ('rawTraffic','reserved1','flowLabel','hopLimit','TClass','reversible','numbPath','PKey','reserved2','SL','MTUSelector','MTU','rateSelector','rate','packetLifeTimeSelector','packetLifeTime','reserved3','independenceSelector','reserved4','SGIDCount','DGIDCount','reserved5','reserved6','SDGID');
    MAD_LENGTH = 40
    MAD_ATTRIBUTE_ID = 0x3a
    MAD_SUBNADMGETMULTI = 0x14 # MAD_METHOD_GET_MULTI
    COMPONENT_MASK = {'rawTraffic':0, 'reserved1':1, 'flowLabel':2, 'hopLimit':3, 'TClass':4, 'reversible':5, 'numbPath':6, 'PKey':7, 'reserved2':8, 'SL':9, 'MTUSelector':10, 'MTU':11, 'rateSelector':12, 'rate':13, 'packetLifeTimeSelector':14, 'packetLifeTime':15, 'reserved3':16, 'independenceSelector':17, 'reserved4':18, 'SGIDCount':19, 'DGIDCount':20, 'reserved5':21, 'reserved6':22, 'SDGID':23}
    def zero(self):
        self.rawTraffic = 0;
        self.reserved1 = 0;
        self.flowLabel = 0;
        self.hopLimit = 0;
        self.TClass = 0;
        self.reversible = 0;
        self.numbPath = 0;
        self.PKey = 0;
        self.reserved2 = 0;
        self.SL = 0;
        self.MTUSelector = 0;
        self.MTU = 0;
        self.rateSelector = 0;
        self.rate = 0;
        self.packetLifeTimeSelector = 0;
        self.packetLifeTime = 0;
        self.reserved3 = 0;
        self.independenceSelector = 0;
        self.reserved4 = 0;
        self.SGIDCount = 0;
        self.DGIDCount = 0;
        self.reserved5 = 0;
        self.reserved6 = 0;
        self.SDGID = IBA.GID();

    @property
    def _pack_0_32(self):
        return ((self.rawTraffic & 0x1) << 31) | ((self.reserved1 & 0x7) << 28) | ((self.flowLabel & 0xFFFFF) << 8) | ((self.hopLimit & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.rawTraffic = (value >> 31) & 0x1;
        self.reserved1 = (value >> 28) & 0x7;
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
        return ((self.reserved2 & 0xFFF) << 20) | ((self.SL & 0xF) << 16) | ((self.MTUSelector & 0x3) << 14) | ((self.MTU & 0x3F) << 8) | ((self.rateSelector & 0x3) << 6) | ((self.rate & 0x3F) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved2 = (value >> 20) & 0xFFF;
        self.SL = (value >> 16) & 0xF;
        self.MTUSelector = (value >> 14) & 0x3;
        self.MTU = (value >> 8) & 0x3F;
        self.rateSelector = (value >> 6) & 0x3;
        self.rate = (value >> 0) & 0x3F;

    @property
    def _pack_3_32(self):
        return ((self.packetLifeTimeSelector & 0x3) << 30) | ((self.packetLifeTime & 0x3F) << 24) | ((self.reserved3 & 0xFF) << 16) | ((self.independenceSelector & 0x3) << 14) | ((self.reserved4 & 0x3F) << 8) | ((self.SGIDCount & 0xFF) << 0)

    @_pack_3_32.setter
    def _pack_3_32(self,value):
        self.packetLifeTimeSelector = (value >> 30) & 0x3;
        self.packetLifeTime = (value >> 24) & 0x3F;
        self.reserved3 = (value >> 16) & 0xFF;
        self.independenceSelector = (value >> 14) & 0x3;
        self.reserved4 = (value >> 8) & 0x3F;
        self.SGIDCount = (value >> 0) & 0xFF;

    @property
    def _pack_4_32(self):
        return ((self.DGIDCount & 0xFF) << 24) | ((self.reserved5 & 0xFFFFFF) << 0)

    @_pack_4_32.setter
    def _pack_4_32(self,value):
        self.DGIDCount = (value >> 24) & 0xFF;
        self.reserved5 = (value >> 0) & 0xFFFFFF;

    def pack_into(self,buffer,offset=0):
        self.SDGID.pack_into(buffer,offset + 24);
        struct.pack_into('>LLLLLL',buffer,offset+0,self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32,self.reserved6);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.SDGID = IBA.GID(buffer[offset + 24:offset + 40],raw=True);
        (self._pack_0_32,self._pack_1_32,self._pack_2_32,self._pack_3_32,self._pack_4_32,self.reserved6,) = struct.unpack_from('>LLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "rawTraffic=%r,reserved1=%r,flowLabel=%r,hopLimit=%r"%(self.rawTraffic,self.reserved1,self.flowLabel,self.hopLimit);
        self.dump(F,0,32,label,offset);
        label = "TClass=%r,reversible=%r,numbPath=%r,PKey=%r"%(self.TClass,self.reversible,self.numbPath,self.PKey);
        self.dump(F,32,64,label,offset);
        label = "reserved2=%r,SL=%r,MTUSelector=%r,MTU=%r,rateSelector=%r,rate=%r"%(self.reserved2,self.SL,self.MTUSelector,self.MTU,self.rateSelector,self.rate);
        self.dump(F,64,96,label,offset);
        label = "packetLifeTimeSelector=%r,packetLifeTime=%r,reserved3=%r,independenceSelector=%r,reserved4=%r,SGIDCount=%r"%(self.packetLifeTimeSelector,self.packetLifeTime,self.reserved3,self.independenceSelector,self.reserved4,self.SGIDCount);
        self.dump(F,96,128,label,offset);
        label = "DGIDCount=%r,reserved5=%r"%(self.DGIDCount,self.reserved5);
        self.dump(F,128,160,label,offset);
        label = "reserved6=%r"%(self.reserved6);
        self.dump(F,160,192,label,offset);
        label = "SDGID=%r"%(self.SDGID);
        self.dump(F,192,320,label,offset);

class SAServiceAssociationRecord(rdma.binstruct.BinStruct):
    '''ServiceRecord ServiceName/ServiceKey association (section 15.2.5.15)'''
    __slots__ = ('serviceKey','serviceName');
    MAD_LENGTH = 80
    MAD_ATTRIBUTE_ID = 0x3b
    MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    COMPONENT_MASK = {'serviceKey':0, 'serviceName':1}
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
        self._buf = buffer[offset:];
        self.serviceKey = IBA.GID(buffer[offset + 0:offset + 16],raw=True);
        self.serviceName = buffer[offset + 16:offset + 80]

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "serviceKey=%r"%(self.serviceKey);
        self.dump(F,0,128,label,offset);
        label = "serviceName=%r"%(self.serviceName);
        self.dump(F,128,640,label,offset);

class PMFormat(BinFormat):
    '''Performance Management MAD Format (section 16.1.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier','reserved2','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x4
    MAD_CLASS_VERSION = 0x1
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
        self.attributeModifier = 0;
        self.reserved2 = bytearray(40);
        self.data = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 64] = self.reserved2
        buffer[offset + 64:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.reserved2 = buffer[offset + 24:offset + 64]
        self.data = buffer[offset + 64:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,192,512,label,offset);
        self._format_data(F,512,2048,offset);

class PMPortSamplesCtl(rdma.binstruct.BinStruct):
    '''Port Performance Data Sampling Control (section 16.1.3.2)'''
    __slots__ = ('opCode','portSelect','tick','reserved1','counterWidth','reserved2','counterMask0','counterMask1','counterMask2','counterMask3','counterMask4','counterMask5','counterMask6','counterMask7','counterMask8','counterMask9','reserved3','counterMask10','counterMask11','counterMask12','counterMask13','counterMask14','sampleMechanisms','reserved4','sampleStatus','optionMask','vendorMask','sampleStart','sampleInterval','tag','counterSelect0','counterSelect1','counterSelect2','counterSelect3','counterSelect4','counterSelect5','counterSelect6','counterSelect7','counterSelect8','counterSelect9','counterSelect10','counterSelect11','counterSelect12','counterSelect13','counterSelect14','reserved5','samplesOnlyOptionMask','reserved6');
    MAD_LENGTH = 192
    MAD_ATTRIBUTE_ID = 0x10
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.opCode = 0;
        self.portSelect = 0;
        self.tick = 0;
        self.reserved1 = 0;
        self.counterWidth = 0;
        self.reserved2 = 0;
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
        self.reserved3 = 0;
        self.counterMask10 = 0;
        self.counterMask11 = 0;
        self.counterMask12 = 0;
        self.counterMask13 = 0;
        self.counterMask14 = 0;
        self.sampleMechanisms = 0;
        self.reserved4 = 0;
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
        self.reserved5 = 0;
        self.samplesOnlyOptionMask = 0;
        self.reserved6 = bytearray(112);

    @property
    def _pack_0_32(self):
        return ((self.opCode & 0xFF) << 24) | ((self.portSelect & 0xFF) << 16) | ((self.tick & 0xFF) << 8) | ((self.reserved1 & 0x1F) << 3) | ((self.counterWidth & 0x7) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.opCode = (value >> 24) & 0xFF;
        self.portSelect = (value >> 16) & 0xFF;
        self.tick = (value >> 8) & 0xFF;
        self.reserved1 = (value >> 3) & 0x1F;
        self.counterWidth = (value >> 0) & 0x7;

    @property
    def _pack_1_32(self):
        return ((self.reserved2 & 0x3) << 30) | ((self.counterMask0 & 0x7) << 27) | ((self.counterMask1 & 0x7) << 24) | ((self.counterMask2 & 0x7) << 21) | ((self.counterMask3 & 0x7) << 18) | ((self.counterMask4 & 0x7) << 15) | ((self.counterMask5 & 0x7) << 12) | ((self.counterMask6 & 0x7) << 9) | ((self.counterMask7 & 0x7) << 6) | ((self.counterMask8 & 0x7) << 3) | ((self.counterMask9 & 0x7) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.reserved2 = (value >> 30) & 0x3;
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
        return ((self.reserved3 & 0x1) << 31) | ((self.counterMask10 & 0x7) << 28) | ((self.counterMask11 & 0x7) << 25) | ((self.counterMask12 & 0x7) << 22) | ((self.counterMask13 & 0x7) << 19) | ((self.counterMask14 & 0x7) << 16) | ((self.sampleMechanisms & 0xFF) << 8) | ((self.reserved4 & 0x3F) << 2) | ((self.sampleStatus & 0x3) << 0)

    @_pack_2_32.setter
    def _pack_2_32(self,value):
        self.reserved3 = (value >> 31) & 0x1;
        self.counterMask10 = (value >> 28) & 0x7;
        self.counterMask11 = (value >> 25) & 0x7;
        self.counterMask12 = (value >> 22) & 0x7;
        self.counterMask13 = (value >> 19) & 0x7;
        self.counterMask14 = (value >> 16) & 0x7;
        self.sampleMechanisms = (value >> 8) & 0xFF;
        self.reserved4 = (value >> 2) & 0x3F;
        self.sampleStatus = (value >> 0) & 0x3;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 80:offset + 192] = self.reserved6
        struct.pack_into('>LLLQQLLHHHHHHHHHHHHHHHHLQ',buffer,offset+0,self._pack_0_32,self._pack_1_32,self._pack_2_32,self.optionMask,self.vendorMask,self.sampleStart,self.sampleInterval,self.tag,self.counterSelect0,self.counterSelect1,self.counterSelect2,self.counterSelect3,self.counterSelect4,self.counterSelect5,self.counterSelect6,self.counterSelect7,self.counterSelect8,self.counterSelect9,self.counterSelect10,self.counterSelect11,self.counterSelect12,self.counterSelect13,self.counterSelect14,self.reserved5,self.samplesOnlyOptionMask);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.reserved6 = buffer[offset + 80:offset + 192]
        (self._pack_0_32,self._pack_1_32,self._pack_2_32,self.optionMask,self.vendorMask,self.sampleStart,self.sampleInterval,self.tag,self.counterSelect0,self.counterSelect1,self.counterSelect2,self.counterSelect3,self.counterSelect4,self.counterSelect5,self.counterSelect6,self.counterSelect7,self.counterSelect8,self.counterSelect9,self.counterSelect10,self.counterSelect11,self.counterSelect12,self.counterSelect13,self.counterSelect14,self.reserved5,self.samplesOnlyOptionMask,) = struct.unpack_from('>LLLQQLLHHHHHHHHHHHHHHHHLQ',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "opCode=%r,portSelect=%r,tick=%r,reserved1=%r,counterWidth=%r"%(self.opCode,self.portSelect,self.tick,self.reserved1,self.counterWidth);
        self.dump(F,0,32,label,offset);
        label = "reserved2=%r,counterMask0=%r,counterMask1=%r,counterMask2=%r,counterMask3=%r,counterMask4=%r,counterMask5=%r,counterMask6=%r,counterMask7=%r,counterMask8=%r,counterMask9=%r"%(self.reserved2,self.counterMask0,self.counterMask1,self.counterMask2,self.counterMask3,self.counterMask4,self.counterMask5,self.counterMask6,self.counterMask7,self.counterMask8,self.counterMask9);
        self.dump(F,32,64,label,offset);
        label = "reserved3=%r,counterMask10=%r,counterMask11=%r,counterMask12=%r,counterMask13=%r,counterMask14=%r,sampleMechanisms=%r,reserved4=%r,sampleStatus=%r"%(self.reserved3,self.counterMask10,self.counterMask11,self.counterMask12,self.counterMask13,self.counterMask14,self.sampleMechanisms,self.reserved4,self.sampleStatus);
        self.dump(F,64,96,label,offset);
        label = "optionMask=%r"%(self.optionMask);
        self.dump(F,96,160,label,offset);
        label = "vendorMask=%r"%(self.vendorMask);
        self.dump(F,160,224,label,offset);
        label = "sampleStart=%r"%(self.sampleStart);
        self.dump(F,224,256,label,offset);
        label = "sampleInterval=%r"%(self.sampleInterval);
        self.dump(F,256,288,label,offset);
        label = "tag=%r,counterSelect0=%r"%(self.tag,self.counterSelect0);
        self.dump(F,288,320,label,offset);
        label = "counterSelect1=%r,counterSelect2=%r"%(self.counterSelect1,self.counterSelect2);
        self.dump(F,320,352,label,offset);
        label = "counterSelect3=%r,counterSelect4=%r"%(self.counterSelect3,self.counterSelect4);
        self.dump(F,352,384,label,offset);
        label = "counterSelect5=%r,counterSelect6=%r"%(self.counterSelect5,self.counterSelect6);
        self.dump(F,384,416,label,offset);
        label = "counterSelect7=%r,counterSelect8=%r"%(self.counterSelect7,self.counterSelect8);
        self.dump(F,416,448,label,offset);
        label = "counterSelect9=%r,counterSelect10=%r"%(self.counterSelect9,self.counterSelect10);
        self.dump(F,448,480,label,offset);
        label = "counterSelect11=%r,counterSelect12=%r"%(self.counterSelect11,self.counterSelect12);
        self.dump(F,480,512,label,offset);
        label = "counterSelect13=%r,counterSelect14=%r"%(self.counterSelect13,self.counterSelect14);
        self.dump(F,512,544,label,offset);
        label = "reserved5=%r"%(self.reserved5);
        self.dump(F,544,576,label,offset);
        label = "samplesOnlyOptionMask=%r"%(self.samplesOnlyOptionMask);
        self.dump(F,576,640,label,offset);
        label = "reserved6=%r"%(self.reserved6);
        self.dump(F,640,1536,label,offset);

class PMPortSamplesRes(rdma.binstruct.BinStruct):
    '''Port Performance Data Sampling Results (section 16.1.3.4)'''
    __slots__ = ('tag','reserved1','sampleStatus','counter');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x11
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    def __init__(self,*args):
        self.counter = [0]*15;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.tag = 0;
        self.reserved1 = 0;
        self.sampleStatus = 0;
        self.counter = [0]*15;

    @property
    def _pack_0_32(self):
        return ((self.tag & 0xFFFF) << 16) | ((self.reserved1 & 0x3FFF) << 2) | ((self.sampleStatus & 0x3) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.tag = (value >> 16) & 0xFFFF;
        self.reserved1 = (value >> 2) & 0x3FFF;
        self.sampleStatus = (value >> 0) & 0x3;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>LLLLLLLLLLLLLLLL',buffer,offset+0,self._pack_0_32,self.counter[0],self.counter[1],self.counter[2],self.counter[3],self.counter[4],self.counter[5],self.counter[6],self.counter[7],self.counter[8],self.counter[9],self.counter[10],self.counter[11],self.counter[12],self.counter[13],self.counter[14]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self._pack_0_32,self.counter[0],self.counter[1],self.counter[2],self.counter[3],self.counter[4],self.counter[5],self.counter[6],self.counter[7],self.counter[8],self.counter[9],self.counter[10],self.counter[11],self.counter[12],self.counter[13],self.counter[14],) = struct.unpack_from('>LLLLLLLLLLLLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "tag=%r,reserved1=%r,sampleStatus=%r"%(self.tag,self.reserved1,self.sampleStatus);
        self.dump(F,0,32,label,offset);
        label = "counter=%r"%(self.counter);
        self.dump(F,32,512,label,offset);

class PMPortCounters(rdma.binstruct.BinStruct):
    '''Port Basic Performance and Error Counters (section 16.1.3.5)'''
    __slots__ = ('reserved1','portSelect','counterSelect','symbolErrorCounter','linkErrorRecoveryCounter','linkDownedCounter','portRcvErrors','portRcvRemotePhysicalErrors','portRcvSwitchRelayErrors','portXmitDiscards','portXmitConstraintErrors','portRcvConstraintErrors','counterSelect2','localLinkIntegrityErrors','excessiveBufferOverrunErrors','reserved2','VL15Dropped','portXmitData','portRcvData','portXmitPkts','portRcvPkts','portXmitWait');
    MAD_LENGTH = 44
    MAD_ATTRIBUTE_ID = 0x12
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.reserved1 = 0;
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
        self.reserved2 = 0;
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
        struct.pack_into('>BBHHBBHHHHLHHLLLLL',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.symbolErrorCounter,self.linkErrorRecoveryCounter,self.linkDownedCounter,self.portRcvErrors,self.portRcvRemotePhysicalErrors,self.portRcvSwitchRelayErrors,self.portXmitDiscards,self._pack_0_32,self.reserved2,self.VL15Dropped,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portXmitWait);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.symbolErrorCounter,self.linkErrorRecoveryCounter,self.linkDownedCounter,self.portRcvErrors,self.portRcvRemotePhysicalErrors,self.portRcvSwitchRelayErrors,self.portXmitDiscards,self._pack_0_32,self.reserved2,self.VL15Dropped,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portXmitWait,) = struct.unpack_from('>BBHHBBHHHHLHHLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "symbolErrorCounter=%r,linkErrorRecoveryCounter=%r,linkDownedCounter=%r"%(self.symbolErrorCounter,self.linkErrorRecoveryCounter,self.linkDownedCounter);
        self.dump(F,32,64,label,offset);
        label = "portRcvErrors=%r,portRcvRemotePhysicalErrors=%r"%(self.portRcvErrors,self.portRcvRemotePhysicalErrors);
        self.dump(F,64,96,label,offset);
        label = "portRcvSwitchRelayErrors=%r,portXmitDiscards=%r"%(self.portRcvSwitchRelayErrors,self.portXmitDiscards);
        self.dump(F,96,128,label,offset);
        label = "portXmitConstraintErrors=%r,portRcvConstraintErrors=%r,counterSelect2=%r,localLinkIntegrityErrors=%r,excessiveBufferOverrunErrors=%r"%(self.portXmitConstraintErrors,self.portRcvConstraintErrors,self.counterSelect2,self.localLinkIntegrityErrors,self.excessiveBufferOverrunErrors);
        self.dump(F,128,160,label,offset);
        label = "reserved2=%r,VL15Dropped=%r"%(self.reserved2,self.VL15Dropped);
        self.dump(F,160,192,label,offset);
        label = "portXmitData=%r"%(self.portXmitData);
        self.dump(F,192,224,label,offset);
        label = "portRcvData=%r"%(self.portRcvData);
        self.dump(F,224,256,label,offset);
        label = "portXmitPkts=%r"%(self.portXmitPkts);
        self.dump(F,256,288,label,offset);
        label = "portRcvPkts=%r"%(self.portRcvPkts);
        self.dump(F,288,320,label,offset);
        label = "portXmitWait=%r"%(self.portXmitWait);
        self.dump(F,320,352,label,offset);

class PMPortRcvErrorDetails(rdma.binstruct.BinStruct):
    '''Port Detailed Error Counters (section 16.1.4.1)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portLocalPhysicalErrors','portMalformedPacketErrors','portBufferOverrunErrors','portDLIDMappingErrors','portVLMappingErrors','portLoopingErrors');
    MAD_LENGTH = 16
    MAD_ATTRIBUTE_ID = 0x15
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portLocalPhysicalErrors = 0;
        self.portMalformedPacketErrors = 0;
        self.portBufferOverrunErrors = 0;
        self.portDLIDMappingErrors = 0;
        self.portVLMappingErrors = 0;
        self.portLoopingErrors = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHH',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.portLocalPhysicalErrors,self.portMalformedPacketErrors,self.portBufferOverrunErrors,self.portDLIDMappingErrors,self.portVLMappingErrors,self.portLoopingErrors);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.portLocalPhysicalErrors,self.portMalformedPacketErrors,self.portBufferOverrunErrors,self.portDLIDMappingErrors,self.portVLMappingErrors,self.portLoopingErrors,) = struct.unpack_from('>BBHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portLocalPhysicalErrors=%r,portMalformedPacketErrors=%r"%(self.portLocalPhysicalErrors,self.portMalformedPacketErrors);
        self.dump(F,32,64,label,offset);
        label = "portBufferOverrunErrors=%r,portDLIDMappingErrors=%r"%(self.portBufferOverrunErrors,self.portDLIDMappingErrors);
        self.dump(F,64,96,label,offset);
        label = "portVLMappingErrors=%r,portLoopingErrors=%r"%(self.portVLMappingErrors,self.portLoopingErrors);
        self.dump(F,96,128,label,offset);

class PMPortXmitDiscardDetails(rdma.binstruct.BinStruct):
    '''Port Transmit Discard Counters (section 16.1.4.2)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portInactiveDiscards','portNeighborMTUDiscards','portSwLifetimeLimitDiscards','portSwHOQLimitDiscards');
    MAD_LENGTH = 12
    MAD_ATTRIBUTE_ID = 0x16
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portInactiveDiscards = 0;
        self.portNeighborMTUDiscards = 0;
        self.portSwLifetimeLimitDiscards = 0;
        self.portSwHOQLimitDiscards = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHH',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.portInactiveDiscards,self.portNeighborMTUDiscards,self.portSwLifetimeLimitDiscards,self.portSwHOQLimitDiscards);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.portInactiveDiscards,self.portNeighborMTUDiscards,self.portSwLifetimeLimitDiscards,self.portSwHOQLimitDiscards,) = struct.unpack_from('>BBHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portInactiveDiscards=%r,portNeighborMTUDiscards=%r"%(self.portInactiveDiscards,self.portNeighborMTUDiscards);
        self.dump(F,32,64,label,offset);
        label = "portSwLifetimeLimitDiscards=%r,portSwHOQLimitDiscards=%r"%(self.portSwLifetimeLimitDiscards,self.portSwHOQLimitDiscards);
        self.dump(F,64,96,label,offset);

class PMPortOpRcvCounters(rdma.binstruct.BinStruct):
    '''Port Receive Counters per Op Code (section 16.1.4.3)'''
    __slots__ = ('opCode','portSelect','counterSelect','portOpRcvPkts','portOpRcvData');
    MAD_LENGTH = 12
    MAD_ATTRIBUTE_ID = 0x17
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.opCode = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portOpRcvPkts = 0;
        self.portOpRcvData = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLL',buffer,offset+0,self.opCode,self.portSelect,self.counterSelect,self.portOpRcvPkts,self.portOpRcvData);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.opCode,self.portSelect,self.counterSelect,self.portOpRcvPkts,self.portOpRcvData,) = struct.unpack_from('>BBHLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "opCode=%r,portSelect=%r,counterSelect=%r"%(self.opCode,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portOpRcvPkts=%r"%(self.portOpRcvPkts);
        self.dump(F,32,64,label,offset);
        label = "portOpRcvData=%r"%(self.portOpRcvData);
        self.dump(F,64,96,label,offset);

class PMPortFlowCtlCounters(rdma.binstruct.BinStruct):
    '''Port Flow Control Counters (section 16.1.4.4)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portXmitFlowPkts','portRcvFlowPkts');
    MAD_LENGTH = 12
    MAD_ATTRIBUTE_ID = 0x18
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portXmitFlowPkts = 0;
        self.portRcvFlowPkts = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLL',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.portXmitFlowPkts,self.portRcvFlowPkts);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.portXmitFlowPkts,self.portRcvFlowPkts,) = struct.unpack_from('>BBHLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portXmitFlowPkts=%r"%(self.portXmitFlowPkts);
        self.dump(F,32,64,label,offset);
        label = "portRcvFlowPkts=%r"%(self.portRcvFlowPkts);
        self.dump(F,64,96,label,offset);

class PMPortVLOpPackets(rdma.binstruct.BinStruct):
    '''Port Packets Received per Op Code per VL (section 16.1.4.5)'''
    __slots__ = ('opCode','portSelect','counterSelect','portVLOpPackets');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x19
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
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
        self._buf = buffer[offset:];
        (self.opCode,self.portSelect,self.counterSelect,self.portVLOpPackets[0],self.portVLOpPackets[1],self.portVLOpPackets[2],self.portVLOpPackets[3],self.portVLOpPackets[4],self.portVLOpPackets[5],self.portVLOpPackets[6],self.portVLOpPackets[7],self.portVLOpPackets[8],self.portVLOpPackets[9],self.portVLOpPackets[10],self.portVLOpPackets[11],self.portVLOpPackets[12],self.portVLOpPackets[13],self.portVLOpPackets[14],self.portVLOpPackets[15],) = struct.unpack_from('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "opCode=%r,portSelect=%r,counterSelect=%r"%(self.opCode,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portVLOpPackets=%r"%(self.portVLOpPackets);
        self.dump(F,32,288,label,offset);

class PMPortVLOpData(rdma.binstruct.BinStruct):
    '''Port Kilobytes Received per Op Code per VL (section 16.1.4.6)'''
    __slots__ = ('opCode','portSelect','counterSelect','portVLOpData');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x1a
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
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
        self._buf = buffer[offset:];
        (self.opCode,self.portSelect,self.counterSelect,self.portVLOpData[0],self.portVLOpData[1],self.portVLOpData[2],self.portVLOpData[3],self.portVLOpData[4],self.portVLOpData[5],self.portVLOpData[6],self.portVLOpData[7],self.portVLOpData[8],self.portVLOpData[9],self.portVLOpData[10],self.portVLOpData[11],self.portVLOpData[12],self.portVLOpData[13],self.portVLOpData[14],self.portVLOpData[15],) = struct.unpack_from('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "opCode=%r,portSelect=%r,counterSelect=%r"%(self.opCode,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portVLOpData=%r"%(self.portVLOpData);
        self.dump(F,32,544,label,offset);

class PMPortVLXmitFlowCtlUpdateErrors(rdma.binstruct.BinStruct):
    '''Port Flow Control update errors per VL (section 16.1.4.7)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portVLXmitFlowCtlUpdateErrors');
    MAD_LENGTH = 8
    MAD_ATTRIBUTE_ID = 0x1b
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.portVLXmitFlowCtlUpdateErrors = bytearray(16);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portVLXmitFlowCtlUpdateErrors = bytearray(16);

    def pack_into(self,buffer,offset=0):
        rdma.binstruct.pack_array8(buffer,4,2,16,self.portVLXmitFlowCtlUpdateErrors);
        struct.pack_into('>BBH',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        rdma.binstruct.unpack_array8(buffer,4,2,16,self.portVLXmitFlowCtlUpdateErrors);
        (self.reserved1,self.portSelect,self.counterSelect,) = struct.unpack_from('>BBH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portVLXmitFlowCtlUpdateErrors=%r"%(self.portVLXmitFlowCtlUpdateErrors);
        self.dump(F,32,64,label,offset);

class PMPortVLXmitWaitCounters(rdma.binstruct.BinStruct):
    '''Port Ticks Waiting to Transmit Counters per VL (section 16.1.4.8)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portVLXmitWait');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x1c
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.portVLXmitWait = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portVLXmitWait = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.portVLXmitWait[0],self.portVLXmitWait[1],self.portVLXmitWait[2],self.portVLXmitWait[3],self.portVLXmitWait[4],self.portVLXmitWait[5],self.portVLXmitWait[6],self.portVLXmitWait[7],self.portVLXmitWait[8],self.portVLXmitWait[9],self.portVLXmitWait[10],self.portVLXmitWait[11],self.portVLXmitWait[12],self.portVLXmitWait[13],self.portVLXmitWait[14],self.portVLXmitWait[15]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.portVLXmitWait[0],self.portVLXmitWait[1],self.portVLXmitWait[2],self.portVLXmitWait[3],self.portVLXmitWait[4],self.portVLXmitWait[5],self.portVLXmitWait[6],self.portVLXmitWait[7],self.portVLXmitWait[8],self.portVLXmitWait[9],self.portVLXmitWait[10],self.portVLXmitWait[11],self.portVLXmitWait[12],self.portVLXmitWait[13],self.portVLXmitWait[14],self.portVLXmitWait[15],) = struct.unpack_from('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portVLXmitWait=%r"%(self.portVLXmitWait);
        self.dump(F,32,288,label,offset);

class PMSwPortVLCongestion(rdma.binstruct.BinStruct):
    '''Switch Port Congestion per VL (section 16.1.4.9)'''
    __slots__ = ('reserved1','portSelect','counterSelect','swPortVLCongestion');
    MAD_LENGTH = 36
    MAD_ATTRIBUTE_ID = 0x30
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.swPortVLCongestion = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.swPortVLCongestion = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.swPortVLCongestion[0],self.swPortVLCongestion[1],self.swPortVLCongestion[2],self.swPortVLCongestion[3],self.swPortVLCongestion[4],self.swPortVLCongestion[5],self.swPortVLCongestion[6],self.swPortVLCongestion[7],self.swPortVLCongestion[8],self.swPortVLCongestion[9],self.swPortVLCongestion[10],self.swPortVLCongestion[11],self.swPortVLCongestion[12],self.swPortVLCongestion[13],self.swPortVLCongestion[14],self.swPortVLCongestion[15]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.swPortVLCongestion[0],self.swPortVLCongestion[1],self.swPortVLCongestion[2],self.swPortVLCongestion[3],self.swPortVLCongestion[4],self.swPortVLCongestion[5],self.swPortVLCongestion[6],self.swPortVLCongestion[7],self.swPortVLCongestion[8],self.swPortVLCongestion[9],self.swPortVLCongestion[10],self.swPortVLCongestion[11],self.swPortVLCongestion[12],self.swPortVLCongestion[13],self.swPortVLCongestion[14],self.swPortVLCongestion[15],) = struct.unpack_from('>BBHHHHHHHHHHHHHHHHH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "swPortVLCongestion=%r"%(self.swPortVLCongestion);
        self.dump(F,32,288,label,offset);

class PMPortSamplesResExt(rdma.binstruct.BinStruct):
    '''Extended Port Samples Result (section 16.1.4.10)'''
    __slots__ = ('tag','reserved1','sampleStatus','extendedWidth','reserved2','counter');
    MAD_LENGTH = 128
    MAD_ATTRIBUTE_ID = 0x1e
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.counter = [0]*15;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.tag = 0;
        self.reserved1 = 0;
        self.sampleStatus = 0;
        self.extendedWidth = 0;
        self.reserved2 = 0;
        self.counter = [0]*15;

    @property
    def _pack_0_32(self):
        return ((self.tag & 0xFFFF) << 16) | ((self.reserved1 & 0x3FFF) << 2) | ((self.sampleStatus & 0x3) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.tag = (value >> 16) & 0xFFFF;
        self.reserved1 = (value >> 2) & 0x3FFF;
        self.sampleStatus = (value >> 0) & 0x3;

    @property
    def _pack_1_32(self):
        return ((self.extendedWidth & 0x3) << 30) | ((self.reserved2 & 0x3FFFFFFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.extendedWidth = (value >> 30) & 0x3;
        self.reserved2 = (value >> 0) & 0x3FFFFFFF;

    def pack_into(self,buffer,offset=0):
        rdma.binstruct.pack_array8(buffer,8,64,15,self.counter);
        struct.pack_into('>LL',buffer,offset+0,self._pack_0_32,self._pack_1_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        rdma.binstruct.unpack_array8(buffer,8,64,15,self.counter);
        (self._pack_0_32,self._pack_1_32,) = struct.unpack_from('>LL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "tag=%r,reserved1=%r,sampleStatus=%r"%(self.tag,self.reserved1,self.sampleStatus);
        self.dump(F,0,32,label,offset);
        label = "extendedWidth=%r,reserved2=%r"%(self.extendedWidth,self.reserved2);
        self.dump(F,32,64,label,offset);
        label = "counter=%r"%(self.counter);
        self.dump(F,64,1024,label,offset);

class PMPortCountersExt(rdma.binstruct.BinStruct):
    '''Extended Port Counters (section 16.1.4.11)'''
    __slots__ = ('reserved1','portSelect','counterSelect','reserved2','portXmitData','portRcvData','portXmitPkts','portRcvPkts','portUnicastXmitPkts','portUnicastRcvPkts','portMulticastXmitPkts','portMulticastRcvPkts');
    MAD_LENGTH = 72
    MAD_ATTRIBUTE_ID = 0x1d
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.reserved2 = 0;
        self.portXmitData = 0;
        self.portRcvData = 0;
        self.portXmitPkts = 0;
        self.portRcvPkts = 0;
        self.portUnicastXmitPkts = 0;
        self.portUnicastRcvPkts = 0;
        self.portMulticastXmitPkts = 0;
        self.portMulticastRcvPkts = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLQQQQQQQQ',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.reserved2,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portUnicastXmitPkts,self.portUnicastRcvPkts,self.portMulticastXmitPkts,self.portMulticastRcvPkts);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.reserved2,self.portXmitData,self.portRcvData,self.portXmitPkts,self.portRcvPkts,self.portUnicastXmitPkts,self.portUnicastRcvPkts,self.portMulticastXmitPkts,self.portMulticastRcvPkts,) = struct.unpack_from('>BBHLQQQQQQQQ',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,32,64,label,offset);
        label = "portXmitData=%r"%(self.portXmitData);
        self.dump(F,64,128,label,offset);
        label = "portRcvData=%r"%(self.portRcvData);
        self.dump(F,128,192,label,offset);
        label = "portXmitPkts=%r"%(self.portXmitPkts);
        self.dump(F,192,256,label,offset);
        label = "portRcvPkts=%r"%(self.portRcvPkts);
        self.dump(F,256,320,label,offset);
        label = "portUnicastXmitPkts=%r"%(self.portUnicastXmitPkts);
        self.dump(F,320,384,label,offset);
        label = "portUnicastRcvPkts=%r"%(self.portUnicastRcvPkts);
        self.dump(F,384,448,label,offset);
        label = "portMulticastXmitPkts=%r"%(self.portMulticastXmitPkts);
        self.dump(F,448,512,label,offset);
        label = "portMulticastRcvPkts=%r"%(self.portMulticastRcvPkts);
        self.dump(F,512,576,label,offset);

class PMPortXmitDataSL(rdma.binstruct.BinStruct):
    '''Transmit SL Port Counters (section A13.6.5)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portXmitDataSL');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x36
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.portXmitDataSL = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portXmitDataSL = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.portXmitDataSL[0],self.portXmitDataSL[1],self.portXmitDataSL[2],self.portXmitDataSL[3],self.portXmitDataSL[4],self.portXmitDataSL[5],self.portXmitDataSL[6],self.portXmitDataSL[7],self.portXmitDataSL[8],self.portXmitDataSL[9],self.portXmitDataSL[10],self.portXmitDataSL[11],self.portXmitDataSL[12],self.portXmitDataSL[13],self.portXmitDataSL[14],self.portXmitDataSL[15]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.portXmitDataSL[0],self.portXmitDataSL[1],self.portXmitDataSL[2],self.portXmitDataSL[3],self.portXmitDataSL[4],self.portXmitDataSL[5],self.portXmitDataSL[6],self.portXmitDataSL[7],self.portXmitDataSL[8],self.portXmitDataSL[9],self.portXmitDataSL[10],self.portXmitDataSL[11],self.portXmitDataSL[12],self.portXmitDataSL[13],self.portXmitDataSL[14],self.portXmitDataSL[15],) = struct.unpack_from('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portXmitDataSL=%r"%(self.portXmitDataSL);
        self.dump(F,32,544,label,offset);

class PMPortRcvDataSL(rdma.binstruct.BinStruct):
    '''Receive SL Port Counters (section A13.6.5)'''
    __slots__ = ('reserved1','portSelect','counterSelect','portRcvDataSL');
    MAD_LENGTH = 68
    MAD_ATTRIBUTE_ID = 0x37
    MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    def __init__(self,*args):
        self.portRcvDataSL = [0]*16;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.reserved1 = 0;
        self.portSelect = 0;
        self.counterSelect = 0;
        self.portRcvDataSL = [0]*16;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0,self.reserved1,self.portSelect,self.counterSelect,self.portRcvDataSL[0],self.portRcvDataSL[1],self.portRcvDataSL[2],self.portRcvDataSL[3],self.portRcvDataSL[4],self.portRcvDataSL[5],self.portRcvDataSL[6],self.portRcvDataSL[7],self.portRcvDataSL[8],self.portRcvDataSL[9],self.portRcvDataSL[10],self.portRcvDataSL[11],self.portRcvDataSL[12],self.portRcvDataSL[13],self.portRcvDataSL[14],self.portRcvDataSL[15]);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.reserved1,self.portSelect,self.counterSelect,self.portRcvDataSL[0],self.portRcvDataSL[1],self.portRcvDataSL[2],self.portRcvDataSL[3],self.portRcvDataSL[4],self.portRcvDataSL[5],self.portRcvDataSL[6],self.portRcvDataSL[7],self.portRcvDataSL[8],self.portRcvDataSL[9],self.portRcvDataSL[10],self.portRcvDataSL[11],self.portRcvDataSL[12],self.portRcvDataSL[13],self.portRcvDataSL[14],self.portRcvDataSL[15],) = struct.unpack_from('>BBHLLLLLLLLLLLLLLLL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "reserved1=%r,portSelect=%r,counterSelect=%r"%(self.reserved1,self.portSelect,self.counterSelect);
        self.dump(F,0,32,label,offset);
        label = "portRcvDataSL=%r"%(self.portRcvDataSL);
        self.dump(F,32,544,label,offset);

class DMFormat(BinFormat):
    '''Device Management MAD Format (section 16.3.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier','reserved2','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x6
    MAD_CLASS_VERSION = 0x1
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
        self.attributeModifier = 0;
        self.reserved2 = bytearray(40);
        self.data = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 64] = self.reserved2
        buffer[offset + 64:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.reserved2 = buffer[offset + 24:offset + 64]
        self.data = buffer[offset + 64:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,192,512,label,offset);
        self._format_data(F,512,2048,offset);

class DMServiceEntry(rdma.binstruct.BinStruct):
    '''Service Entry (section 16.3.3)'''
    __slots__ = ('serviceName','serviceID');
    MAD_LENGTH = 48
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
        self._buf = buffer[offset:];
        self.serviceName = buffer[offset + 0:offset + 40]
        (self.serviceID,) = struct.unpack_from('>Q',buffer,offset+40);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "serviceName=%r"%(self.serviceName);
        self.dump(F,0,320,label,offset);
        label = "serviceID=%r"%(self.serviceID);
        self.dump(F,320,384,label,offset);

class DMIOUnitInfo(rdma.binstruct.BinStruct):
    '''List of all I/O Controllers in a I/O Unit (section 16.3.3.3)'''
    __slots__ = ('changeID','maxControllers','reserved1','diagDeviceID','optionROM','controllerList');
    MAD_LENGTH = 132
    MAD_ATTRIBUTE_ID = 0x10
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    def zero(self):
        self.changeID = 0;
        self.maxControllers = 0;
        self.reserved1 = 0;
        self.diagDeviceID = 0;
        self.optionROM = 0;
        self.controllerList = bytearray(128);

    @property
    def _pack_0_32(self):
        return ((self.changeID & 0xFFFF) << 16) | ((self.maxControllers & 0xFF) << 8) | ((self.reserved1 & 0x3F) << 2) | ((self.diagDeviceID & 0x1) << 1) | ((self.optionROM & 0x1) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.changeID = (value >> 16) & 0xFFFF;
        self.maxControllers = (value >> 8) & 0xFF;
        self.reserved1 = (value >> 2) & 0x3F;
        self.diagDeviceID = (value >> 1) & 0x1;
        self.optionROM = (value >> 0) & 0x1;

    def pack_into(self,buffer,offset=0):
        buffer[offset + 4:offset + 132] = self.controllerList
        struct.pack_into('>L',buffer,offset+0,self._pack_0_32);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.controllerList = buffer[offset + 4:offset + 132]
        (self._pack_0_32,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "changeID=%r,maxControllers=%r,reserved1=%r,diagDeviceID=%r,optionROM=%r"%(self.changeID,self.maxControllers,self.reserved1,self.diagDeviceID,self.optionROM);
        self.dump(F,0,32,label,offset);
        label = "controllerList=%r"%(self.controllerList);
        self.dump(F,32,1056,label,offset);

class DMIOControllerProfile(rdma.binstruct.BinStruct):
    '''I/O Controller Profile Information (section 16.3.3.4)'''
    __slots__ = ('GUID','vendorID','reserved1','deviceID','deviceVersion','reserved2','subsystemVendorID','reserved3','subsystemID','IOClass','IOSubclass','protocol','protocolVersion','reserved4','reserved5','sendMessageDepth','reserved6','RDMAReadDepth','sendMessageSize','RDMATransferSize','controllerOperationsMask','reserved7','serviceEntries','reserved8','reserved9','IDString');
    MAD_LENGTH = 128
    MAD_ATTRIBUTE_ID = 0x11
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    def __init__(self,*args):
        self.IDString = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.GUID = IBA.GUID();
        self.vendorID = 0;
        self.reserved1 = 0;
        self.deviceID = 0;
        self.deviceVersion = 0;
        self.reserved2 = 0;
        self.subsystemVendorID = 0;
        self.reserved3 = 0;
        self.subsystemID = 0;
        self.IOClass = 0;
        self.IOSubclass = 0;
        self.protocol = 0;
        self.protocolVersion = 0;
        self.reserved4 = 0;
        self.reserved5 = 0;
        self.sendMessageDepth = 0;
        self.reserved6 = 0;
        self.RDMAReadDepth = 0;
        self.sendMessageSize = 0;
        self.RDMATransferSize = 0;
        self.controllerOperationsMask = 0;
        self.reserved7 = 0;
        self.serviceEntries = 0;
        self.reserved8 = 0;
        self.reserved9 = 0;
        self.IDString = bytearray(64);

    @property
    def _pack_0_32(self):
        return ((self.vendorID & 0xFFFFFF) << 8) | ((self.reserved1 & 0xFF) << 0)

    @_pack_0_32.setter
    def _pack_0_32(self,value):
        self.vendorID = (value >> 8) & 0xFFFFFF;
        self.reserved1 = (value >> 0) & 0xFF;

    @property
    def _pack_1_32(self):
        return ((self.subsystemVendorID & 0xFFFFFF) << 8) | ((self.reserved3 & 0xFF) << 0)

    @_pack_1_32.setter
    def _pack_1_32(self,value):
        self.subsystemVendorID = (value >> 8) & 0xFFFFFF;
        self.reserved3 = (value >> 0) & 0xFF;

    def pack_into(self,buffer,offset=0):
        self.GUID.pack_into(buffer,offset + 0);
        buffer[offset + 64:offset + 128] = self.IDString
        struct.pack_into('>LLHHLLHHHHHHHBBLLBBBBQ',buffer,offset+8,self._pack_0_32,self.deviceID,self.deviceVersion,self.reserved2,self._pack_1_32,self.subsystemID,self.IOClass,self.IOSubclass,self.protocol,self.protocolVersion,self.reserved4,self.reserved5,self.sendMessageDepth,self.reserved6,self.RDMAReadDepth,self.sendMessageSize,self.RDMATransferSize,self.controllerOperationsMask,self.reserved7,self.serviceEntries,self.reserved8,self.reserved9);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.GUID = IBA.GUID(buffer[offset + 0:offset + 8],raw=True);
        self.IDString = buffer[offset + 64:offset + 128]
        (self._pack_0_32,self.deviceID,self.deviceVersion,self.reserved2,self._pack_1_32,self.subsystemID,self.IOClass,self.IOSubclass,self.protocol,self.protocolVersion,self.reserved4,self.reserved5,self.sendMessageDepth,self.reserved6,self.RDMAReadDepth,self.sendMessageSize,self.RDMATransferSize,self.controllerOperationsMask,self.reserved7,self.serviceEntries,self.reserved8,self.reserved9,) = struct.unpack_from('>LLHHLLHHHHHHHBBLLBBBBQ',buffer,offset+8);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "GUID=%r"%(self.GUID);
        self.dump(F,0,64,label,offset);
        label = "vendorID=%r,reserved1=%r"%(self.vendorID,self.reserved1);
        self.dump(F,64,96,label,offset);
        label = "deviceID=%r"%(self.deviceID);
        self.dump(F,96,128,label,offset);
        label = "deviceVersion=%r,reserved2=%r"%(self.deviceVersion,self.reserved2);
        self.dump(F,128,160,label,offset);
        label = "subsystemVendorID=%r,reserved3=%r"%(self.subsystemVendorID,self.reserved3);
        self.dump(F,160,192,label,offset);
        label = "subsystemID=%r"%(self.subsystemID);
        self.dump(F,192,224,label,offset);
        label = "IOClass=%r,IOSubclass=%r"%(self.IOClass,self.IOSubclass);
        self.dump(F,224,256,label,offset);
        label = "protocol=%r,protocolVersion=%r"%(self.protocol,self.protocolVersion);
        self.dump(F,256,288,label,offset);
        label = "reserved4=%r,reserved5=%r"%(self.reserved4,self.reserved5);
        self.dump(F,288,320,label,offset);
        label = "sendMessageDepth=%r,reserved6=%r,RDMAReadDepth=%r"%(self.sendMessageDepth,self.reserved6,self.RDMAReadDepth);
        self.dump(F,320,352,label,offset);
        label = "sendMessageSize=%r"%(self.sendMessageSize);
        self.dump(F,352,384,label,offset);
        label = "RDMATransferSize=%r"%(self.RDMATransferSize);
        self.dump(F,384,416,label,offset);
        label = "controllerOperationsMask=%r,reserved7=%r,serviceEntries=%r,reserved8=%r"%(self.controllerOperationsMask,self.reserved7,self.serviceEntries,self.reserved8);
        self.dump(F,416,448,label,offset);
        label = "reserved9=%r"%(self.reserved9);
        self.dump(F,448,512,label,offset);
        label = "IDString=%r"%(self.IDString);
        self.dump(F,512,1024,label,offset);

class DMServiceEntries(rdma.binstruct.BinStruct):
    '''List of Supported Services and Their Associated Service IDs (section 16.3.3.5)'''
    __slots__ = ('serviceEntry');
    MAD_LENGTH = 192
    MAD_ATTRIBUTE_ID = 0x12
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    def __init__(self,*args):
        self.serviceEntry = [DMServiceEntry()]*4;
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.serviceEntry = [DMServiceEntry()]*4;

    def pack_into(self,buffer,offset=0):
        self.serviceEntry[0].pack_into(buffer,offset + 0);
        self.serviceEntry[1].pack_into(buffer,offset + 48);
        self.serviceEntry[2].pack_into(buffer,offset + 96);
        self.serviceEntry[3].pack_into(buffer,offset + 144);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.serviceEntry[0].unpack_from(buffer,offset + 0);
        self.serviceEntry[1].unpack_from(buffer,offset + 48);
        self.serviceEntry[2].unpack_from(buffer,offset + 96);
        self.serviceEntry[3].unpack_from(buffer,offset + 144);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "serviceEntry=%r"%(self.serviceEntry);
        self.dump(F,0,1536,label,offset);

class DMDiagnosticTimeout(rdma.binstruct.BinStruct):
    '''Get the Maximum Time for Completion of a Diagnostic Test (section 16.3.3.6)'''
    __slots__ = ('maxDiagTime');
    MAD_LENGTH = 4
    MAD_ATTRIBUTE_ID = 0x20
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    def zero(self):
        self.maxDiagTime = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>L',buffer,offset+0,self.maxDiagTime);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.maxDiagTime,) = struct.unpack_from('>L',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "maxDiagTime=%r"%(self.maxDiagTime);
        self.dump(F,0,32,label,offset);

class DMPrepareToTest(rdma.binstruct.BinStruct):
    '''Prepare Device for Test (section 16.3.3.7)'''
    __slots__ = ();
    MAD_LENGTH = 0
    MAD_ATTRIBUTE_ID = 0x21
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    def pack_into(self,buffer,offset=0):
        return None;

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        return;

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);

class DMTestDeviceOnce(rdma.binstruct.BinStruct):
    '''Test Device Once (section 16.3.3.8)'''
    __slots__ = ();
    MAD_LENGTH = 0
    MAD_ATTRIBUTE_ID = 0x22
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    def pack_into(self,buffer,offset=0):
        return None;

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        return;

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);

class DMTestDeviceLoop(rdma.binstruct.BinStruct):
    '''Test Device Continuously (section 16.3.3.9)'''
    __slots__ = ();
    MAD_LENGTH = 0
    MAD_ATTRIBUTE_ID = 0x23
    MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    def pack_into(self,buffer,offset=0):
        return None;

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        return;

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);

class DMDiagCode(rdma.binstruct.BinStruct):
    '''Vendor-Specific Device Diagnostic Information (section 16.3.3.10)'''
    __slots__ = ('diagCode','reserved1');
    MAD_LENGTH = 4
    MAD_ATTRIBUTE_ID = 0x24
    MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    def zero(self):
        self.diagCode = 0;
        self.reserved1 = 0;

    def pack_into(self,buffer,offset=0):
        struct.pack_into('>HH',buffer,offset+0,self.diagCode,self.reserved1);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        (self.diagCode,self.reserved1,) = struct.unpack_from('>HH',buffer,offset+0);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "diagCode=%r,reserved1=%r"%(self.diagCode,self.reserved1);
        self.dump(F,0,32,label,offset);

class SNMPFormat(BinFormat):
    '''SNMP Tunneling MAD Format (section 16.4.1)'''
    __slots__ = ('baseVersion','mgmtClass','classVersion','method','status','classSpecific','transactionID','attributeID','reserved1','attributeModifier','reserved2','RAddress','payloadLength','segmentNumber','sourceLID','data');
    MAD_LENGTH = 256
    MAD_CLASS = 0x8
    MAD_CLASS_VERSION = 0x1
    def zero(self):
        self.baseVersion = 0;
        self.mgmtClass = 0;
        self.classVersion = 0;
        self.method = 0;
        self.status = 0;
        self.classSpecific = 0;
        self.transactionID = 0;
        self.attributeID = 0;
        self.reserved1 = 0;
        self.attributeModifier = 0;
        self.reserved2 = bytearray(32);
        self.RAddress = 0;
        self.payloadLength = 0;
        self.segmentNumber = 0;
        self.sourceLID = 0;
        self.data = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 24:offset + 56] = self.reserved2
        buffer[offset + 64:offset + 256] = self.data
        struct.pack_into('>BBBBHHQHHL',buffer,offset+0,self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier);
        struct.pack_into('>LBBH',buffer,offset+56,self.RAddress,self.payloadLength,self.segmentNumber,self.sourceLID);

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.reserved2 = buffer[offset + 24:offset + 56]
        self.data = buffer[offset + 64:offset + 256]
        (self.baseVersion,self.mgmtClass,self.classVersion,self.method,self.status,self.classSpecific,self.transactionID,self.attributeID,self.reserved1,self.attributeModifier,) = struct.unpack_from('>BBBBHHQHHL',buffer,offset+0);
        (self.RAddress,self.payloadLength,self.segmentNumber,self.sourceLID,) = struct.unpack_from('>LBBH',buffer,offset+56);

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "baseVersion=%r,mgmtClass=%r,classVersion=%r,method=%r"%(self.baseVersion,self.mgmtClass,self.classVersion,self.method);
        self.dump(F,0,32,label,offset);
        label = "status=%r,classSpecific=%r"%(self.status,self.classSpecific);
        self.dump(F,32,64,label,offset);
        label = "transactionID=%r"%(self.transactionID);
        self.dump(F,64,128,label,offset);
        label = "attributeID=%r,reserved1=%r"%(self.attributeID,self.reserved1);
        self.dump(F,128,160,label,offset);
        label = "attributeModifier=%r"%(self.attributeModifier);
        self.dump(F,160,192,label,offset);
        label = "reserved2=%r"%(self.reserved2);
        self.dump(F,192,448,label,offset);
        label = "RAddress=%r"%(self.RAddress);
        self.dump(F,448,480,label,offset);
        label = "payloadLength=%r,segmentNumber=%r,sourceLID=%r"%(self.payloadLength,self.segmentNumber,self.sourceLID);
        self.dump(F,480,512,label,offset);
        self._format_data(F,512,2048,offset);

class SNMPCommunityInfo(rdma.binstruct.BinStruct):
    '''Community Name Data Store (section 16.4.3.2)'''
    __slots__ = ('communityName');
    MAD_LENGTH = 64
    MAD_ATTRIBUTE_ID = 0x10
    MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND
    def __init__(self,*args):
        self.communityName = bytearray(64);
        rdma.binstruct.BinStruct.__init__(self,*args);

    def zero(self):
        self.communityName = bytearray(64);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 64] = self.communityName

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.communityName = buffer[offset + 0:offset + 64]

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "communityName=%r"%(self.communityName);
        self.dump(F,0,512,label,offset);

class SNMPPDUInfo(rdma.binstruct.BinStruct):
    '''Data Segment (section 16.4.3.3)'''
    __slots__ = ('PDUData');
    MAD_LENGTH = 192
    MAD_ATTRIBUTE_ID = 0x11
    MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND
    def zero(self):
        self.PDUData = bytearray(192);

    def pack_into(self,buffer,offset=0):
        buffer[offset + 0:offset + 192] = self.PDUData

    def unpack_from(self,buffer,offset=0):
        self._buf = buffer[offset:];
        self.PDUData = buffer[offset + 0:offset + 192]

    def printer(self,F,offset=0,header=True):
        rdma.binstruct.BinStruct.printer(self,F,offset,header);
        label = "PDUData=%r"%(self.PDUData);
        self.dump(F,0,1536,label,offset);

CLASS_TO_STRUCT = {(7,2):CMFormat,
	(1,1):SMPFormat,
	(129,1):SMPFormatDirected,
	(3,2):SAFormat,
	(4,1):PMFormat,
	(6,1):DMFormat,
	(8,1):SNMPFormat};
ATTR_TO_STRUCT = {(CMFormat,16):CMREQ,
	(CMFormat,17):CMMRA,
	(CMFormat,18):CMREJ,
	(CMFormat,19):CMREP,
	(CMFormat,20):CMRTU,
	(CMFormat,21):CMDREQ,
	(CMFormat,22):CMDREP,
	(CMFormat,25):CMLAP,
	(CMFormat,26):CMAPR,
	(CMFormat,23):CMSIDR_REQ,
	(CMFormat,24):CMSIDR_REP,
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
	(SAFormat,17):SANodeRecord,
	(SAFormat,18):SAPortInfoRecord,
	(SAFormat,19):SASLToVLMappingTableRecord,
	(SAFormat,20):SASwitchInfoRecord,
	(SAFormat,21):SALinearForwardingTableRecord,
	(SAFormat,22):SARandomForwardingTableRecord,
	(SAFormat,23):SAMulticastForwardingTableRecord,
	(SAFormat,54):SAVLArbitrationTableRecord,
	(SAFormat,24):SASMInfoRecord,
	(SAFormat,243):SAInformInfoRecord,
	(SAFormat,32):SALinkRecord,
	(SAFormat,48):SAGUIDInfoRecord,
	(SAFormat,49):SAServiceRecord,
	(SAFormat,51):SAPKeyTableRecord,
	(SAFormat,53):SAPathRecord,
	(SAFormat,56):SAMCMemberRecord,
	(SAFormat,57):SATraceRecord,
	(SAFormat,58):SAMultiPathRecord,
	(SAFormat,59):SAServiceAssociationRecord,
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
	(PMFormat,48):PMSwPortVLCongestion,
	(PMFormat,30):PMPortSamplesResExt,
	(PMFormat,29):PMPortCountersExt,
	(PMFormat,54):PMPortXmitDataSL,
	(PMFormat,55):PMPortRcvDataSL,
	(DMFormat,16):DMIOUnitInfo,
	(DMFormat,17):DMIOControllerProfile,
	(DMFormat,18):DMServiceEntries,
	(DMFormat,32):DMDiagnosticTimeout,
	(DMFormat,33):DMPrepareToTest,
	(DMFormat,34):DMTestDeviceOnce,
	(DMFormat,35):DMTestDeviceLoop,
	(DMFormat,36):DMDiagCode,
	(SNMPFormat,16):SNMPCommunityInfo,
	(SNMPFormat,17):SNMPPDUInfo};
