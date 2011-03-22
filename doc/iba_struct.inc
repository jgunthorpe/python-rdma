Communication Management (12)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.CMAPR

    Alternate Path Response (section 12.8.2)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('additionalInfoLength',8,1), ('APstatus',8,1), ('reserved_80',16,1), ('additionalInfo',576,1), ('privateData',1184,1)]

    ============================ ============= ========================
    Member                       Position      Type                    
    ============================ ============= ========================
    :attr:`LCID`                 0:4 (32)      :class:`int`            
    :attr:`RCID`                 4:8 (32)      :class:`int`            
    :attr:`additionalInfoLength` 8:9 (8)       :class:`int`            
    :attr:`APstatus`             9:10 (8)      :class:`int`            
    :attr:`reserved_80`          10:12 (16)    :class:`int`            
    :attr:`additionalInfo`       12:84 (576)   :class:`bytearray` (72) 
    :attr:`privateData`          84:232 (1184) :class:`bytearray` (148)
    ============================ ============= ========================

.. class:: rdma.IBA.CMDREP

    Reply To Request For Communication Release (section 12.6.11)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('privateData',1792,1)]

    =================== ============ ========================
    Member              Position     Type                    
    =================== ============ ========================
    :attr:`LCID`        0:4 (32)     :class:`int`            
    :attr:`RCID`        4:8 (32)     :class:`int`            
    :attr:`privateData` 8:232 (1792) :class:`bytearray` (224)
    =================== ============ ========================

.. class:: rdma.IBA.CMDREQ

    Request For Communication Release (Disconnection Request) (section 12.6.10)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('remoteQPN',24,1), ('reserved_88',8,1), ('privateData',1760,1)]

    =================== ============= ========================
    Member              Position      Type                    
    =================== ============= ========================
    :attr:`LCID`        0:4 (32)      :class:`int`            
    :attr:`RCID`        4:8 (32)      :class:`int`            
    :attr:`remoteQPN`   8:11 (24)     :class:`int`            
    :attr:`reserved_88` 11:12 (8)     :class:`int`            
    :attr:`privateData` 12:232 (1760) :class:`bytearray` (220)
    =================== ============= ========================

.. class:: rdma.IBA.CMLAP

    Load Alternate Path (section 12.8.1)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('QKey',32,1), ('RQPN',24,1), ('RCMTimeout',5,1), ('reserved_125',3,1), ('reserved_128',32,1), ('altSLID',16,1), ('altDLID',16,1), ('altSGID',128,1), ('altDGID',128,1), ('altFlowLabel',20,1), ('reserved_468',4,1), ('altTClass',8,1), ('altHopLimit',8,1), ('reserved_488',2,1), ('altIPD',6,1), ('altSL',4,1), ('altSubnetLocal',1,1), ('reserved_501',3,1), ('altLocalACKTimeout',5,1), ('reserved_509',3,1), ('privateData',1344,1)]

    ========================== =============== ========================
    Member                     Position        Type                    
    ========================== =============== ========================
    :attr:`LCID`               0:4 (32)        :class:`int`            
    :attr:`RCID`               4:8 (32)        :class:`int`            
    :attr:`QKey`               8:12 (32)       :class:`int`            
    :attr:`RQPN`               12:15 (24)      :class:`int`            
    :attr:`RCMTimeout`         15:15[5] (5)    :class:`int`            
    :attr:`reserved_125`       15[5]:16 (3)    :class:`int`            
    :attr:`reserved_128`       16:20 (32)      :class:`int`            
    :attr:`altSLID`            20:22 (16)      :class:`int`            
    :attr:`altDLID`            22:24 (16)      :class:`int`            
    :attr:`altSGID`            24:40 (128)     :class:`~rdma.IBA.GID`  
    :attr:`altDGID`            40:56 (128)     :class:`~rdma.IBA.GID`  
    :attr:`altFlowLabel`       56:58[4] (20)   :class:`int`            
    :attr:`reserved_468`       58[4]:59 (4)    :class:`int`            
    :attr:`altTClass`          59:60 (8)       :class:`int`            
    :attr:`altHopLimit`        60:61 (8)       :class:`int`            
    :attr:`reserved_488`       61:61[2] (2)    :class:`int`            
    :attr:`altIPD`             61[2]:62 (6)    :class:`int`            
    :attr:`altSL`              62:62[4] (4)    :class:`int`            
    :attr:`altSubnetLocal`     62[4]:62[5] (1) :class:`int`            
    :attr:`reserved_501`       62[5]:63 (3)    :class:`int`            
    :attr:`altLocalACKTimeout` 63:63[5] (5)    :class:`int`            
    :attr:`reserved_509`       63[5]:64 (3)    :class:`int`            
    :attr:`privateData`        64:232 (1344)   :class:`bytearray` (168)
    ========================== =============== ========================

.. class:: rdma.IBA.CMMRA

    Message Receipt Acknowledgement (section 12.6.6)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('messageMRAed',2,1), ('reserved_66',6,1), ('serviceTimeout',5,1), ('reserved_77',3,1), ('reserved_80',16,1), ('privateData',1760,1)]

    ====================== ============= ========================
    Member                 Position      Type                    
    ====================== ============= ========================
    :attr:`LCID`           0:4 (32)      :class:`int`            
    :attr:`RCID`           4:8 (32)      :class:`int`            
    :attr:`messageMRAed`   8:8[2] (2)    :class:`int`            
    :attr:`reserved_66`    8[2]:9 (6)    :class:`int`            
    :attr:`serviceTimeout` 9:9[5] (5)    :class:`int`            
    :attr:`reserved_77`    9[5]:10 (3)   :class:`int`            
    :attr:`reserved_80`    10:12 (16)    :class:`int`            
    :attr:`privateData`    12:232 (1760) :class:`bytearray` (220)
    ====================== ============= ========================

.. class:: rdma.IBA.CMPath

    Path Information (section 12.6)

    .. attribute:: MAD_LENGTH = 44
    .. attribute:: MEMBERS = [('SLID',16,1), ('DLID',16,1), ('SGID',128,1), ('DGID',128,1), ('flowLabel',20,1), ('reserved_308',4,1), ('reserved_312',2,1), ('PD',6,1), ('TClass',8,1), ('hopLimit',8,1), ('SL',4,1), ('subnetLocal',1,1), ('reserved_341',3,1), ('localACKTimeout',5,1), ('reserved_349',3,1)]

    ======================= =============== ======================
    Member                  Position        Type                  
    ======================= =============== ======================
    :attr:`SLID`            0:2 (16)        :class:`int`          
    :attr:`DLID`            2:4 (16)        :class:`int`          
    :attr:`SGID`            4:20 (128)      :class:`~rdma.IBA.GID`
    :attr:`DGID`            20:36 (128)     :class:`~rdma.IBA.GID`
    :attr:`flowLabel`       36:38[4] (20)   :class:`int`          
    :attr:`reserved_308`    38[4]:39 (4)    :class:`int`          
    :attr:`reserved_312`    39:39[2] (2)    :class:`int`          
    :attr:`PD`              39[2]:40 (6)    :class:`int`          
    :attr:`TClass`          40:41 (8)       :class:`int`          
    :attr:`hopLimit`        41:42 (8)       :class:`int`          
    :attr:`SL`              42:42[4] (4)    :class:`int`          
    :attr:`subnetLocal`     42[4]:42[5] (1) :class:`int`          
    :attr:`reserved_341`    42[5]:43 (3)    :class:`int`          
    :attr:`localACKTimeout` 43:43[5] (5)    :class:`int`          
    :attr:`reserved_349`    43[5]:44 (3)    :class:`int`          
    ======================= =============== ======================

.. class:: rdma.IBA.CMREJ

    Reject (section 12.6.7)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('messageRejected',2,1), ('reserved_66',6,1), ('rejectInfoLength',7,1), ('reserved_79',1,1), ('reason',16,1), ('ARI',576,1), ('privateData',1184,1)]

    ======================== ============= ========================
    Member                   Position      Type                    
    ======================== ============= ========================
    :attr:`LCID`             0:4 (32)      :class:`int`            
    :attr:`RCID`             4:8 (32)      :class:`int`            
    :attr:`messageRejected`  8:8[2] (2)    :class:`int`            
    :attr:`reserved_66`      8[2]:9 (6)    :class:`int`            
    :attr:`rejectInfoLength` 9:9[7] (7)    :class:`int`            
    :attr:`reserved_79`      9[7]:10 (1)   :class:`int`            
    :attr:`reason`           10:12 (16)    :class:`int`            
    :attr:`ARI`              12:84 (576)   :class:`bytearray` (72) 
    :attr:`privateData`      84:232 (1184) :class:`bytearray` (148)
    ======================== ============= ========================

.. class:: rdma.IBA.CMREP

    Reply To Request For Communication (section 12.6.8)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x13
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('localQKey',32,1), ('localQPN',24,1), ('reserved_120',8,1), ('localEEContext',24,1), ('reserved_152',8,1), ('startingPSN',24,1), ('reserved_184',8,1), ('responderResources',8,1), ('initiatorDepth',8,1), ('targetACKDelay',5,1), ('failoverAccepted',2,1), ('flowControl',1,1), ('RNRRetryCount',3,1), ('reserved_219',5,1), ('LGUID',64,1), ('privateData',1568,1)]

    ========================== =============== ========================
    Member                     Position        Type                    
    ========================== =============== ========================
    :attr:`LCID`               0:4 (32)        :class:`int`            
    :attr:`RCID`               4:8 (32)        :class:`int`            
    :attr:`localQKey`          8:12 (32)       :class:`int`            
    :attr:`localQPN`           12:15 (24)      :class:`int`            
    :attr:`reserved_120`       15:16 (8)       :class:`int`            
    :attr:`localEEContext`     16:19 (24)      :class:`int`            
    :attr:`reserved_152`       19:20 (8)       :class:`int`            
    :attr:`startingPSN`        20:23 (24)      :class:`int`            
    :attr:`reserved_184`       23:24 (8)       :class:`int`            
    :attr:`responderResources` 24:25 (8)       :class:`int`            
    :attr:`initiatorDepth`     25:26 (8)       :class:`int`            
    :attr:`targetACKDelay`     26:26[5] (5)    :class:`int`            
    :attr:`failoverAccepted`   26[5]:26[7] (2) :class:`int`            
    :attr:`flowControl`        26[7]:27 (1)    :class:`int`            
    :attr:`RNRRetryCount`      27:27[3] (3)    :class:`int`            
    :attr:`reserved_219`       27[3]:28 (5)    :class:`int`            
    :attr:`LGUID`              28:36 (64)      :class:`~rdma.IBA.GUID` 
    :attr:`privateData`        36:232 (1568)   :class:`bytearray` (196)
    ========================== =============== ========================

.. class:: rdma.IBA.CMREQ

    Request for Communication (section 12.6.5)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('reserved_32',32,1), ('serviceID',64,1), ('LGUID',64,1), ('localCMQKey',32,1), ('localQKey',32,1), ('localQPN',24,1), ('responderResources',8,1), ('localEECN',24,1), ('initiatorDepth',8,1), ('remoteEECN',24,1), ('remoteResponseTimeout',5,1), ('transportService',2,1), ('flowControl',1,1), ('startingPSN',24,1), ('localResponseTimeout',5,1), ('retryCount',3,1), ('PKey',16,1), ('pathPacketMTU',4,1), ('RDCExists',1,1), ('RNRRetryCount',3,1), ('maxCMRetries',4,1), ('reserved_412',4,1), ('primaryPath',352,1), ('alternatePath',352,1), ('privateData',736,1)]

    ============================= =============== =========================
    Member                        Position        Type                     
    ============================= =============== =========================
    :attr:`LCID`                  0:4 (32)        :class:`int`             
    :attr:`reserved_32`           4:8 (32)        :class:`int`             
    :attr:`serviceID`             8:16 (64)       :class:`int`             
    :attr:`LGUID`                 16:24 (64)      :class:`~rdma.IBA.GUID`  
    :attr:`localCMQKey`           24:28 (32)      :class:`int`             
    :attr:`localQKey`             28:32 (32)      :class:`int`             
    :attr:`localQPN`              32:35 (24)      :class:`int`             
    :attr:`responderResources`    35:36 (8)       :class:`int`             
    :attr:`localEECN`             36:39 (24)      :class:`int`             
    :attr:`initiatorDepth`        39:40 (8)       :class:`int`             
    :attr:`remoteEECN`            40:43 (24)      :class:`int`             
    :attr:`remoteResponseTimeout` 43:43[5] (5)    :class:`int`             
    :attr:`transportService`      43[5]:43[7] (2) :class:`int`             
    :attr:`flowControl`           43[7]:44 (1)    :class:`int`             
    :attr:`startingPSN`           44:47 (24)      :class:`int`             
    :attr:`localResponseTimeout`  47:47[5] (5)    :class:`int`             
    :attr:`retryCount`            47[5]:48 (3)    :class:`int`             
    :attr:`PKey`                  48:50 (16)      :class:`int`             
    :attr:`pathPacketMTU`         50:50[4] (4)    :class:`int`             
    :attr:`RDCExists`             50[4]:50[5] (1) :class:`int`             
    :attr:`RNRRetryCount`         50[5]:51 (3)    :class:`int`             
    :attr:`maxCMRetries`          51:51[4] (4)    :class:`int`             
    :attr:`reserved_412`          51[4]:52 (4)    :class:`int`             
    :attr:`primaryPath`           52:96 (352)     :class:`~rdma.IBA.CMPath`
    :attr:`alternatePath`         96:140 (352)    :class:`~rdma.IBA.CMPath`
    :attr:`privateData`           140:232 (736)   :class:`bytearray` (92)  
    ============================= =============== =========================

.. class:: rdma.IBA.CMRTU

    Ready To Use (section 12.6.9)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('LCID',32,1), ('RCID',32,1), ('privateData',1792,1)]

    =================== ============ ========================
    Member              Position     Type                    
    =================== ============ ========================
    :attr:`LCID`        0:4 (32)     :class:`int`            
    :attr:`RCID`        4:8 (32)     :class:`int`            
    :attr:`privateData` 8:232 (1792) :class:`bytearray` (224)
    =================== ============ ========================

.. class:: rdma.IBA.CMSIDR_REP

    Service ID Resolution Response (section 12.11.2)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('requestID',32,1), ('QPN',24,1), ('status',8,1), ('serviceID',64,1), ('QKey',32,1), ('classPortinfo',576,1), ('privateData',1120,1)]

    ===================== ============= ===================================
    Member                Position      Type                               
    ===================== ============= ===================================
    :attr:`requestID`     0:4 (32)      :class:`int`                       
    :attr:`QPN`           4:7 (24)      :class:`int`                       
    :attr:`status`        7:8 (8)       :class:`int`                       
    :attr:`serviceID`     8:16 (64)     :class:`int`                       
    :attr:`QKey`          16:20 (32)    :class:`int`                       
    :attr:`classPortinfo` 20:92 (576)   :class:`~rdma.IBA.MADClassPortInfo`
    :attr:`privateData`   92:232 (1120) :class:`bytearray` (140)           
    ===================== ============= ===================================

.. class:: rdma.IBA.CMSIDR_REQ

    Service ID Resolution Request (section 12.11.1)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('requestID',32,1), ('reserved_32',32,1), ('serviceID',64,1), ('privateData',1728,1)]

    =================== ============= ========================
    Member              Position      Type                    
    =================== ============= ========================
    :attr:`requestID`   0:4 (32)      :class:`int`            
    :attr:`reserved_32` 4:8 (32)      :class:`int`            
    :attr:`serviceID`   8:16 (64)     :class:`int`            
    :attr:`privateData` 16:232 (1728) :class:`bytearray` (216)
    =================== ============= ========================

Generic MAD (13.4)
^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.MADClassPortInfo

    Class Port Info (section 13.4.8.1)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1
    .. attribute:: MAD_BMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_BMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_COMMMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_COMMMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SNMPGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: COMPONENT_MASK = {'baseVersion':0, 'classVersion':1, 'capabilityMask':2, 'capabilityMask2':3, 'respTimeValue':4, 'redirectGID':5, 'redirectTC':6, 'redirectSL':7, 'redirectFL':8, 'redirectLID':9, 'redirectPKey':10, 'reserved_256':11, 'redirectQP':12, 'redirectQKey':13, 'trapGID':14, 'trapTC':15, 'trapSL':16, 'trapFL':17, 'trapLID':18, 'trapPKey':19, 'trapHL':20, 'trapQP':21, 'trapQKey':22}
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('classVersion',8,1), ('capabilityMask',16,1), ('capabilityMask2',27,1), ('respTimeValue',5,1), ('redirectGID',128,1), ('redirectTC',8,1), ('redirectSL',4,1), ('redirectFL',20,1), ('redirectLID',16,1), ('redirectPKey',16,1), ('reserved_256',8,1), ('redirectQP',24,1), ('redirectQKey',32,1), ('trapGID',128,1), ('trapTC',8,1), ('trapSL',4,1), ('trapFL',20,1), ('trapLID',16,1), ('trapPKey',16,1), ('trapHL',8,1), ('trapQP',24,1), ('trapQKey',32,1)]

    ======================= ============= ======================
    Member                  Position      Type                  
    ======================= ============= ======================
    :attr:`baseVersion`     0:1 (8)       :class:`int`          
    :attr:`classVersion`    1:2 (8)       :class:`int`          
    :attr:`capabilityMask`  2:4 (16)      :class:`int`          
    :attr:`capabilityMask2` 4:7[3] (27)   :class:`int`          
    :attr:`respTimeValue`   7[3]:8 (5)    :class:`int`          
    :attr:`redirectGID`     8:24 (128)    :class:`~rdma.IBA.GID`
    :attr:`redirectTC`      24:25 (8)     :class:`int`          
    :attr:`redirectSL`      25:25[4] (4)  :class:`int`          
    :attr:`redirectFL`      25[4]:28 (20) :class:`int`          
    :attr:`redirectLID`     28:30 (16)    :class:`int`          
    :attr:`redirectPKey`    30:32 (16)    :class:`int`          
    :attr:`reserved_256`    32:33 (8)     :class:`int`          
    :attr:`redirectQP`      33:36 (24)    :class:`int`          
    :attr:`redirectQKey`    36:40 (32)    :class:`int`          
    :attr:`trapGID`         40:56 (128)   :class:`~rdma.IBA.GID`
    :attr:`trapTC`          56:57 (8)     :class:`int`          
    :attr:`trapSL`          57:57[4] (4)  :class:`int`          
    :attr:`trapFL`          57[4]:60 (20) :class:`int`          
    :attr:`trapLID`         60:62 (16)    :class:`int`          
    :attr:`trapPKey`        62:64 (16)    :class:`int`          
    :attr:`trapHL`          64:65 (8)     :class:`int`          
    :attr:`trapQP`          65:68 (24)    :class:`int`          
    :attr:`trapQKey`        68:72 (32)    :class:`int`          
    ======================= ============= ======================

.. class:: rdma.IBA.MADHeader

    MAD Base Header (section 13.4.3)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1)]

    ========================= ========== ============
    Member                    Position   Type        
    ========================= ========== ============
    :attr:`baseVersion`       0:1 (8)    :class:`int`
    :attr:`mgmtClass`         1:2 (8)    :class:`int`
    :attr:`classVersion`      2:3 (8)    :class:`int`
    :attr:`method`            3:4 (8)    :class:`int`
    :attr:`status`            4:6 (16)   :class:`int`
    :attr:`classSpecific`     6:8 (16)   :class:`int`
    :attr:`transactionID`     8:16 (64)  :class:`int`
    :attr:`attributeID`       16:18 (16) :class:`int`
    :attr:`reserved_144`      18:20 (16) :class:`int`
    :attr:`attributeModifier` 20:24 (32) :class:`int`
    ========================= ========== ============

.. class:: rdma.IBA.MADHeaderDirected

    MAD Base Header Directed (section 13.4.3)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('D',1,1), ('status',15,1), ('hopPointer',8,1), ('hopCount',8,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1)]

    ========================= =========== ============
    Member                    Position    Type        
    ========================= =========== ============
    :attr:`baseVersion`       0:1 (8)     :class:`int`
    :attr:`mgmtClass`         1:2 (8)     :class:`int`
    :attr:`classVersion`      2:3 (8)     :class:`int`
    :attr:`method`            3:4 (8)     :class:`int`
    :attr:`D`                 4:4[1] (1)  :class:`int`
    :attr:`status`            4[1]:6 (15) :class:`int`
    :attr:`hopPointer`        6:7 (8)     :class:`int`
    :attr:`hopCount`          7:8 (8)     :class:`int`
    :attr:`transactionID`     8:16 (64)   :class:`int`
    :attr:`attributeID`       16:18 (16)  :class:`int`
    :attr:`reserved_144`      18:20 (16)  :class:`int`
    :attr:`attributeModifier` 20:24 (32)  :class:`int`
    ========================= =========== ============

.. class:: rdma.IBA.MADInformInfo

    InformInfo (section 13.4.8.3)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: COMPONENT_MASK = {'GID':0, 'LIDRangeBegin':1, 'LIDRangeEnd':2, 'reserved_160':3, 'isGeneric':4, 'subscribe':5, 'type':6, 'trapNumber':7, 'QPN':8, 'reserved_248':9, 'respTimeValue':10, 'reserved_256':11, 'producerType':12}
    .. attribute:: MEMBERS = [('GID',128,1), ('LIDRangeBegin',16,1), ('LIDRangeEnd',16,1), ('reserved_160',16,1), ('isGeneric',8,1), ('subscribe',8,1), ('type',16,1), ('trapNumber',16,1), ('QPN',24,1), ('reserved_248',3,1), ('respTimeValue',5,1), ('reserved_256',8,1), ('producerType',24,1)]

    ===================== ============ ======================
    Member                Position     Type                  
    ===================== ============ ======================
    :attr:`GID`           0:16 (128)   :class:`~rdma.IBA.GID`
    :attr:`LIDRangeBegin` 16:18 (16)   :class:`int`          
    :attr:`LIDRangeEnd`   18:20 (16)   :class:`int`          
    :attr:`reserved_160`  20:22 (16)   :class:`int`          
    :attr:`isGeneric`     22:23 (8)    :class:`int`          
    :attr:`subscribe`     23:24 (8)    :class:`int`          
    :attr:`type`          24:26 (16)   :class:`int`          
    :attr:`trapNumber`    26:28 (16)   :class:`int`          
    :attr:`QPN`           28:31 (24)   :class:`int`          
    :attr:`reserved_248`  31:31[3] (3) :class:`int`          
    :attr:`respTimeValue` 31[3]:32 (5) :class:`int`          
    :attr:`reserved_256`  32:33 (8)    :class:`int`          
    :attr:`producerType`  33:36 (24)   :class:`int`          
    ===================== ============ ======================

RMPP (13.6)
^^^^^^^^^^^

.. class:: rdma.IBA.RMPPAbort

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MEMBERS = [('RMPPHeader',224,1), ('reserved_224',32,1), ('reserved_256',32,1), ('errorData',1760,1)]

    ==================== ============= ==================================
    Member               Position      Type                              
    ==================== ============= ==================================
    :attr:`RMPPHeader`   0:28 (224)    :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`reserved_224` 28:32 (32)    :class:`int`                      
    :attr:`reserved_256` 32:36 (32)    :class:`int`                      
    :attr:`errorData`    36:256 (1760) :class:`bytearray` (220)          
    ==================== ============= ==================================

.. class:: rdma.IBA.RMPPAck

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MEMBERS = [('RMPPHeader',224,1), ('segmentNumber',32,1), ('newWindowLast',32,1), ('reserved_288',1760,1)]

    ===================== ============= ==================================
    Member                Position      Type                              
    ===================== ============= ==================================
    :attr:`RMPPHeader`    0:28 (224)    :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`segmentNumber` 28:32 (32)    :class:`int`                      
    :attr:`newWindowLast` 32:36 (32)    :class:`int`                      
    :attr:`reserved_288`  36:256 (1760) :class:`bytearray` (220)          
    ===================== ============= ==================================

.. class:: rdma.IBA.RMPPData

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MEMBERS = [('RMPPHeader',224,1), ('segmentNumber',32,1), ('payLoadLength',32,1), ('data',1760,1)]

    ===================== ============= ==================================
    Member                Position      Type                              
    ===================== ============= ==================================
    :attr:`RMPPHeader`    0:28 (224)    :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`segmentNumber` 28:32 (32)    :class:`int`                      
    :attr:`payLoadLength` 32:36 (32)    :class:`int`                      
    :attr:`data`          36:256 (1760) :class:`bytearray` (220)          
    ===================== ============= ==================================

.. class:: rdma.IBA.RMPPHeader

    RMPP Header Fields (section 13.6.2.1)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MEMBERS = [('MADHeader',192,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1)]

    =================== ============ ============================
    Member              Position     Type                        
    =================== ============ ============================
    :attr:`MADHeader`   0:24 (192)   :class:`~rdma.IBA.MADHeader`
    :attr:`RMPPVersion` 24:25 (8)    :class:`int`                
    :attr:`RMPPType`    25:26 (8)    :class:`int`                
    :attr:`RRespTime`   26:26[5] (5) :class:`int`                
    :attr:`RMPPFlags`   26[5]:27 (3) :class:`int`                
    :attr:`RMPPStatus`  27:28 (8)    :class:`int`                
    :attr:`data1`       28:32 (32)   :class:`int`                
    :attr:`data2`       32:36 (32)   :class:`int`                
    =================== ============ ============================

.. class:: rdma.IBA.RMPPShortHeader

    RMPP Header Fields (section 13.6.2.1)

    .. attribute:: MAD_LENGTH = 28
    .. attribute:: MEMBERS = [('MADHeader',192,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1)]

    =================== ============ ============================
    Member              Position     Type                        
    =================== ============ ============================
    :attr:`MADHeader`   0:24 (192)   :class:`~rdma.IBA.MADHeader`
    :attr:`RMPPVersion` 24:25 (8)    :class:`int`                
    :attr:`RMPPType`    25:26 (8)    :class:`int`                
    :attr:`RRespTime`   26:26[5] (5) :class:`int`                
    :attr:`RMPPFlags`   26[5]:27 (3) :class:`int`                
    :attr:`RMPPStatus`  27:28 (8)    :class:`int`                
    =================== ============ ============================

.. class:: rdma.IBA.RMPPStop

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MEMBERS = [('RMPPHeader',224,1), ('reserved_224',32,1), ('reserved_256',32,1), ('errorData',1760,1)]

    ==================== ============= ==================================
    Member               Position      Type                              
    ==================== ============= ==================================
    :attr:`RMPPHeader`   0:28 (224)    :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`reserved_224` 28:32 (32)    :class:`int`                      
    :attr:`reserved_256` 32:36 (32)    :class:`int`                      
    :attr:`errorData`    36:256 (1760) :class:`bytearray` (220)          
    ==================== ============= ==================================

Subnet Management (14)
^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.SMPFormat

    An *aggregation* of: MADHeader

    SMP Format - LID Routed (section 14.2.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x1
    .. attribute:: MAD_CLASS_VERSION = 0x1
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('MKey',64,1), ('reserved_256',256,1), ('data',512,1), ('reserved_1024',1024,1)]

    ========================= ============== ========================
    Member                    Position       Type                    
    ========================= ============== ========================
    :attr:`baseVersion`       0:1 (8)        :class:`int`            
    :attr:`mgmtClass`         1:2 (8)        :class:`int`            
    :attr:`classVersion`      2:3 (8)        :class:`int`            
    :attr:`method`            3:4 (8)        :class:`int`            
    :attr:`status`            4:6 (16)       :class:`int`            
    :attr:`classSpecific`     6:8 (16)       :class:`int`            
    :attr:`transactionID`     8:16 (64)      :class:`int`            
    :attr:`attributeID`       16:18 (16)     :class:`int`            
    :attr:`reserved_144`      18:20 (16)     :class:`int`            
    :attr:`attributeModifier` 20:24 (32)     :class:`int`            
    :attr:`MKey`              24:32 (64)     :class:`int`            
    :attr:`reserved_256`      32:64 (256)    :class:`bytearray` (32) 
    :attr:`data`              64:128 (512)   :class:`bytearray` (64) 
    :attr:`reserved_1024`     128:256 (1024) :class:`bytearray` (128)
    ========================= ============== ========================

.. class:: rdma.IBA.SMPFormatDirected

    An *aggregation* of: MADHeaderDirected

    SMP Format - Direct Routed (section 14.2.1.2)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x81
    .. attribute:: MAD_CLASS_VERSION = 0x1
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('D',1,1), ('status',15,1), ('hopPointer',8,1), ('hopCount',8,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('MKey',64,1), ('drSLID',16,1), ('drDLID',16,1), ('reserved_288',224,1), ('data',512,1), ('initialPath',8,64), ('returnPath',8,64)]

    ========================= ============ ============================
    Member                    Position     Type                        
    ========================= ============ ============================
    :attr:`baseVersion`       0:1 (8)      :class:`int`                
    :attr:`mgmtClass`         1:2 (8)      :class:`int`                
    :attr:`classVersion`      2:3 (8)      :class:`int`                
    :attr:`method`            3:4 (8)      :class:`int`                
    :attr:`D`                 4:4[1] (1)   :class:`int`                
    :attr:`status`            4[1]:6 (15)  :class:`int`                
    :attr:`hopPointer`        6:7 (8)      :class:`int`                
    :attr:`hopCount`          7:8 (8)      :class:`int`                
    :attr:`transactionID`     8:16 (64)    :class:`int`                
    :attr:`attributeID`       16:18 (16)   :class:`int`                
    :attr:`reserved_144`      18:20 (16)   :class:`int`                
    :attr:`attributeModifier` 20:24 (32)   :class:`int`                
    :attr:`MKey`              24:32 (64)   :class:`int`                
    :attr:`drSLID`            32:34 (16)   :class:`int`                
    :attr:`drDLID`            34:36 (16)   :class:`int`                
    :attr:`reserved_288`      36:64 (224)  :class:`bytearray` (28)     
    :attr:`data`              64:128 (512) :class:`bytearray` (64)     
    :attr:`initialPath`       128:192 (8)  [:class:`bytearray` (64)]*64
    :attr:`returnPath`        192:256 (8)  [:class:`bytearray` (64)]*64
    ========================= ============ ============================

.. class:: rdma.IBA.SMPGUIDInfo

    Assigned GUIDs (section 14.2.5.5)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('GUIDBlock',64,8)]

    ================= ========= ===========================
    Member            Position  Type                       
    ================= ========= ===========================
    :attr:`GUIDBlock` 0:64 (64) [:class:`~rdma.IBA.GUID`]*8
    ================= ========= ===========================

.. class:: rdma.IBA.SMPLIDPortBlock

    LID/Port Block Element (section 14.2.5.11)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('LID',16,1), ('valid',1,1), ('LMC',3,1), ('reserved_20',4,1), ('port',8,1)]

    =================== ============= ============
    Member              Position      Type        
    =================== ============= ============
    :attr:`LID`         0:2 (16)      :class:`int`
    :attr:`valid`       2:2[1] (1)    :class:`int`
    :attr:`LMC`         2[1]:2[4] (3) :class:`int`
    :attr:`reserved_20` 2[4]:3 (4)    :class:`int`
    :attr:`port`        3:4 (8)       :class:`int`
    =================== ============= ============

.. class:: rdma.IBA.SMPLedInfo

    Turn on/off LED (section 14.2.5.15)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x31
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('ledMask',1,1), ('reserved_1',31,1)]

    ================== =========== ============
    Member             Position    Type        
    ================== =========== ============
    :attr:`ledMask`    0:0[1] (1)  :class:`int`
    :attr:`reserved_1` 0[1]:4 (31) :class:`int`
    ================== =========== ============

.. class:: rdma.IBA.SMPLinearForwardingTable

    Linear Forwarding Table Information (section 14.2.5.10)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('portBlock',8,64)]

    ================= ======== ============================
    Member            Position Type                        
    ================= ======== ============================
    :attr:`portBlock` 0:64 (8) [:class:`bytearray` (64)]*64
    ================= ======== ============================

.. class:: rdma.IBA.SMPMulticastForwardingTable

    Multicast Forwarding Table Information (section 14.2.5.12)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1b
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('portMaskBlock',16,32)]

    ===================== ========= =================
    Member                Position  Type             
    ===================== ========= =================
    :attr:`portMaskBlock` 0:64 (16) [:class:`int`]*32
    ===================== ========= =================

.. class:: rdma.IBA.SMPNodeDescription

    Node Description String (section 14.2.5.2)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('nodeString',8,64)]

    ================== ======== ============================
    Member             Position Type                        
    ================== ======== ============================
    :attr:`nodeString` 0:64 (8) [:class:`bytearray` (64)]*64
    ================== ======== ============================

.. class:: rdma.IBA.SMPNodeInfo

    Generic Node Data (section 14.2.5.3)

    .. attribute:: MAD_LENGTH = 40
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('classVersion',8,1), ('nodeType',8,1), ('numPorts',8,1), ('systemImageGUID',64,1), ('nodeGUID',64,1), ('portGUID',64,1), ('partitionCap',16,1), ('deviceID',16,1), ('revision',32,1), ('localPortNum',8,1), ('vendorID',24,1)]

    ======================= ========== =======================
    Member                  Position   Type                   
    ======================= ========== =======================
    :attr:`baseVersion`     0:1 (8)    :class:`int`           
    :attr:`classVersion`    1:2 (8)    :class:`int`           
    :attr:`nodeType`        2:3 (8)    :class:`int`           
    :attr:`numPorts`        3:4 (8)    :class:`int`           
    :attr:`systemImageGUID` 4:12 (64)  :class:`~rdma.IBA.GUID`
    :attr:`nodeGUID`        12:20 (64) :class:`~rdma.IBA.GUID`
    :attr:`portGUID`        20:28 (64) :class:`~rdma.IBA.GUID`
    :attr:`partitionCap`    28:30 (16) :class:`int`           
    :attr:`deviceID`        30:32 (16) :class:`int`           
    :attr:`revision`        32:36 (32) :class:`int`           
    :attr:`localPortNum`    36:37 (8)  :class:`int`           
    :attr:`vendorID`        37:40 (24) :class:`int`           
    ======================= ========== =======================

.. class:: rdma.IBA.SMPPKeyTable

    Partition Table (section 14.2.5.7)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('PKeyBlock',16,32)]

    ================= ========= =================
    Member            Position  Type             
    ================= ========= =================
    :attr:`PKeyBlock` 0:64 (16) [:class:`int`]*32
    ================= ========= =================

.. class:: rdma.IBA.SMPPortInfo

    Port Information (section 14.2.5.6)

    .. attribute:: MAD_LENGTH = 60
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('MKey',64,1), ('GIDPrefix',64,1), ('LID',16,1), ('masterSMLID',16,1), ('capabilityMask',32,1), ('diagCode',16,1), ('MKeyLeasePeriod',16,1), ('localPortNum',8,1), ('linkWidthEnabled',8,1), ('linkWidthSupported',8,1), ('linkWidthActive',8,1), ('linkSpeedSupported',4,1), ('portState',4,1), ('portPhysicalState',4,1), ('linkDownDefaultState',4,1), ('MKeyProtectBits',2,1), ('reserved_274',3,1), ('LMC',3,1), ('linkSpeedActive',4,1), ('linkSpeedEnabled',4,1), ('neighborMTU',4,1), ('masterSMSL',4,1), ('VLCap',4,1), ('initType',4,1), ('VLHighLimit',8,1), ('VLArbitrationHighCap',8,1), ('VLArbitrationLowCap',8,1), ('initTypeReply',4,1), ('MTUCap',4,1), ('VLStallCount',3,1), ('HOQLife',5,1), ('operationalVLs',4,1), ('partitionEnforcementInbound',1,1), ('partitionEnforcementOutbound',1,1), ('filterRawInbound',1,1), ('filterRawOutbound',1,1), ('MKeyViolations',16,1), ('PKeyViolations',16,1), ('QKeyViolations',16,1), ('GUIDCap',8,1), ('clientReregister',1,1), ('reserved_409',2,1), ('subnetTimeOut',5,1), ('reserved_416',3,1), ('respTimeValue',5,1), ('localPhyErrors',4,1), ('overrunErrors',4,1), ('maxCreditHint',16,1), ('reserved_448',8,1), ('linkRoundTripLatency',24,1)]

    ==================================== =============== ============
    Member                               Position        Type        
    ==================================== =============== ============
    :attr:`MKey`                         0:8 (64)        :class:`int`
    :attr:`GIDPrefix`                    8:16 (64)       :class:`int`
    :attr:`LID`                          16:18 (16)      :class:`int`
    :attr:`masterSMLID`                  18:20 (16)      :class:`int`
    :attr:`capabilityMask`               20:24 (32)      :class:`int`
    :attr:`diagCode`                     24:26 (16)      :class:`int`
    :attr:`MKeyLeasePeriod`              26:28 (16)      :class:`int`
    :attr:`localPortNum`                 28:29 (8)       :class:`int`
    :attr:`linkWidthEnabled`             29:30 (8)       :class:`int`
    :attr:`linkWidthSupported`           30:31 (8)       :class:`int`
    :attr:`linkWidthActive`              31:32 (8)       :class:`int`
    :attr:`linkSpeedSupported`           32:32[4] (4)    :class:`int`
    :attr:`portState`                    32[4]:33 (4)    :class:`int`
    :attr:`portPhysicalState`            33:33[4] (4)    :class:`int`
    :attr:`linkDownDefaultState`         33[4]:34 (4)    :class:`int`
    :attr:`MKeyProtectBits`              34:34[2] (2)    :class:`int`
    :attr:`reserved_274`                 34[2]:34[5] (3) :class:`int`
    :attr:`LMC`                          34[5]:35 (3)    :class:`int`
    :attr:`linkSpeedActive`              35:35[4] (4)    :class:`int`
    :attr:`linkSpeedEnabled`             35[4]:36 (4)    :class:`int`
    :attr:`neighborMTU`                  36:36[4] (4)    :class:`int`
    :attr:`masterSMSL`                   36[4]:37 (4)    :class:`int`
    :attr:`VLCap`                        37:37[4] (4)    :class:`int`
    :attr:`initType`                     37[4]:38 (4)    :class:`int`
    :attr:`VLHighLimit`                  38:39 (8)       :class:`int`
    :attr:`VLArbitrationHighCap`         39:40 (8)       :class:`int`
    :attr:`VLArbitrationLowCap`          40:41 (8)       :class:`int`
    :attr:`initTypeReply`                41:41[4] (4)    :class:`int`
    :attr:`MTUCap`                       41[4]:42 (4)    :class:`int`
    :attr:`VLStallCount`                 42:42[3] (3)    :class:`int`
    :attr:`HOQLife`                      42[3]:43 (5)    :class:`int`
    :attr:`operationalVLs`               43:43[4] (4)    :class:`int`
    :attr:`partitionEnforcementInbound`  43[4]:43[5] (1) :class:`int`
    :attr:`partitionEnforcementOutbound` 43[5]:43[6] (1) :class:`int`
    :attr:`filterRawInbound`             43[6]:43[7] (1) :class:`int`
    :attr:`filterRawOutbound`            43[7]:44 (1)    :class:`int`
    :attr:`MKeyViolations`               44:46 (16)      :class:`int`
    :attr:`PKeyViolations`               46:48 (16)      :class:`int`
    :attr:`QKeyViolations`               48:50 (16)      :class:`int`
    :attr:`GUIDCap`                      50:51 (8)       :class:`int`
    :attr:`clientReregister`             51:51[1] (1)    :class:`int`
    :attr:`reserved_409`                 51[1]:51[3] (2) :class:`int`
    :attr:`subnetTimeOut`                51[3]:52 (5)    :class:`int`
    :attr:`reserved_416`                 52:52[3] (3)    :class:`int`
    :attr:`respTimeValue`                52[3]:53 (5)    :class:`int`
    :attr:`localPhyErrors`               53:53[4] (4)    :class:`int`
    :attr:`overrunErrors`                53[4]:54 (4)    :class:`int`
    :attr:`maxCreditHint`                54:56 (16)      :class:`int`
    :attr:`reserved_448`                 56:57 (8)       :class:`int`
    :attr:`linkRoundTripLatency`         57:60 (24)      :class:`int`
    ==================================== =============== ============

.. class:: rdma.IBA.SMPRandomForwardingTable

    Random Forwarding Table Information (section 14.2.5.11)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('LIDPortBlock',32,16)]

    ==================== ========= =======================================
    Member               Position  Type                                   
    ==================== ========= =======================================
    :attr:`LIDPortBlock` 0:64 (32) [:class:`~rdma.IBA.SMPLIDPortBlock`]*16
    ==================== ========= =======================================

.. class:: rdma.IBA.SMPSLToVLMappingTable

    Service Level to Virtual Lane mapping Information (section 14.2.5.8)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('SLtoVL',4,16)]

    ============== ======== =================
    Member         Position Type             
    ============== ======== =================
    :attr:`SLtoVL` 0:8 (4)  [:class:`int`]*16
    ============== ======== =================

.. class:: rdma.IBA.SMPSMInfo

    Subnet Management Information (section 14.2.5.13)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('GUID',64,1), ('SMKey',64,1), ('actCount',32,1), ('priority',4,1), ('SMState',4,1), ('reserved_168',24,1)]

    ==================== ============ =======================
    Member               Position     Type                   
    ==================== ============ =======================
    :attr:`GUID`         0:8 (64)     :class:`~rdma.IBA.GUID`
    :attr:`SMKey`        8:16 (64)    :class:`int`           
    :attr:`actCount`     16:20 (32)   :class:`int`           
    :attr:`priority`     20:20[4] (4) :class:`int`           
    :attr:`SMState`      20[4]:21 (4) :class:`int`           
    :attr:`reserved_168` 21:24 (24)   :class:`int`           
    ==================== ============ =======================

.. class:: rdma.IBA.SMPSwitchInfo

    Switch Information (section 14.2.5.4)

    .. attribute:: MAD_LENGTH = 20
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('linearFDBCap',16,1), ('randomFDBCap',16,1), ('multicastFDBCap',16,1), ('linearFDBTop',16,1), ('defaultPort',8,1), ('defaultMulticastPrimaryPort',8,1), ('defaultMulticastNotPrimaryPort',8,1), ('lifeTimeValue',5,1), ('portStateChange',1,1), ('optimizedSLtoVLMappingProgramming',2,1), ('LIDsPerPort',16,1), ('partitionEnforcementCap',16,1), ('inboundEnforcementCap',1,1), ('outboundEnforcementCap',1,1), ('filterRawInboundCap',1,1), ('filterRawOutboundCap',1,1), ('enhancedPort0',1,1), ('reserved_133',3,1), ('reserved_136',24,1)]

    ========================================= =============== ============
    Member                                    Position        Type        
    ========================================= =============== ============
    :attr:`linearFDBCap`                      0:2 (16)        :class:`int`
    :attr:`randomFDBCap`                      2:4 (16)        :class:`int`
    :attr:`multicastFDBCap`                   4:6 (16)        :class:`int`
    :attr:`linearFDBTop`                      6:8 (16)        :class:`int`
    :attr:`defaultPort`                       8:9 (8)         :class:`int`
    :attr:`defaultMulticastPrimaryPort`       9:10 (8)        :class:`int`
    :attr:`defaultMulticastNotPrimaryPort`    10:11 (8)       :class:`int`
    :attr:`lifeTimeValue`                     11:11[5] (5)    :class:`int`
    :attr:`portStateChange`                   11[5]:11[6] (1) :class:`int`
    :attr:`optimizedSLtoVLMappingProgramming` 11[6]:12 (2)    :class:`int`
    :attr:`LIDsPerPort`                       12:14 (16)      :class:`int`
    :attr:`partitionEnforcementCap`           14:16 (16)      :class:`int`
    :attr:`inboundEnforcementCap`             16:16[1] (1)    :class:`int`
    :attr:`outboundEnforcementCap`            16[1]:16[2] (1) :class:`int`
    :attr:`filterRawInboundCap`               16[2]:16[3] (1) :class:`int`
    :attr:`filterRawOutboundCap`              16[3]:16[4] (1) :class:`int`
    :attr:`enhancedPort0`                     16[4]:16[5] (1) :class:`int`
    :attr:`reserved_133`                      16[5]:17 (3)    :class:`int`
    :attr:`reserved_136`                      17:20 (24)      :class:`int`
    ========================================= =============== ============

.. class:: rdma.IBA.SMPVLArbitrationTable

    List of Weights (section 14.2.5.9)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('VLWeightBlock',16,32)]

    ===================== ========= =================
    Member                Position  Type             
    ===================== ========= =================
    :attr:`VLWeightBlock` 0:64 (16) [:class:`int`]*32
    ===================== ========= =================

.. class:: rdma.IBA.SMPVendorDiag

    Vendor Specific Diagnostic (section 14.2.5.14)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('nextIndex',16,1), ('reserved_16',16,1), ('diagData',480,1)]

    =================== ========== =======================
    Member              Position   Type                   
    =================== ========== =======================
    :attr:`nextIndex`   0:2 (16)   :class:`int`           
    :attr:`reserved_16` 2:4 (16)   :class:`int`           
    :attr:`diagData`    4:64 (480) :class:`bytearray` (60)
    =================== ========== =======================

Subnet Administration (15)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.SAFormat

    An *aggregation* of: SAHeader

    SA Format (section 15.2.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x3
    .. attribute:: MAD_CLASS_VERSION = 0x2
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1), ('SMKey',64,1), ('attributeOffset',16,1), ('reserved_368',16,1), ('componentMask',64,1), ('data',1600,1)]

    ========================= ============= ========================
    Member                    Position      Type                    
    ========================= ============= ========================
    :attr:`baseVersion`       0:1 (8)       :class:`int`            
    :attr:`mgmtClass`         1:2 (8)       :class:`int`            
    :attr:`classVersion`      2:3 (8)       :class:`int`            
    :attr:`method`            3:4 (8)       :class:`int`            
    :attr:`status`            4:6 (16)      :class:`int`            
    :attr:`classSpecific`     6:8 (16)      :class:`int`            
    :attr:`transactionID`     8:16 (64)     :class:`int`            
    :attr:`attributeID`       16:18 (16)    :class:`int`            
    :attr:`reserved_144`      18:20 (16)    :class:`int`            
    :attr:`attributeModifier` 20:24 (32)    :class:`int`            
    :attr:`RMPPVersion`       24:25 (8)     :class:`int`            
    :attr:`RMPPType`          25:26 (8)     :class:`int`            
    :attr:`RRespTime`         26:26[5] (5)  :class:`int`            
    :attr:`RMPPFlags`         26[5]:27 (3)  :class:`int`            
    :attr:`RMPPStatus`        27:28 (8)     :class:`int`            
    :attr:`data1`             28:32 (32)    :class:`int`            
    :attr:`data2`             32:36 (32)    :class:`int`            
    :attr:`SMKey`             36:44 (64)    :class:`int`            
    :attr:`attributeOffset`   44:46 (16)    :class:`int`            
    :attr:`reserved_368`      46:48 (16)    :class:`int`            
    :attr:`componentMask`     48:56 (64)    :class:`int`            
    :attr:`data`              56:256 (1600) :class:`bytearray` (200)
    ========================= ============= ========================

.. class:: rdma.IBA.SAGUIDInfoRecord

    Container for port GUIDInfo (section 15.2.5.18)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved_24':2, 'reserved_32':3, 'GUIDInfo.GUIDBlock':4}
    .. attribute:: MEMBERS = [('LID',16,1), ('blockNum',8,1), ('reserved_24',8,1), ('reserved_32',32,1), ('GUIDInfo',512,1)]

    =================== ========== ==============================
    Member              Position   Type                          
    =================== ========== ==============================
    :attr:`LID`         0:2 (16)   :class:`int`                  
    :attr:`blockNum`    2:3 (8)    :class:`int`                  
    :attr:`reserved_24` 3:4 (8)    :class:`int`                  
    :attr:`reserved_32` 4:8 (32)   :class:`int`                  
    :attr:`GUIDInfo`    8:72 (512) :class:`~rdma.IBA.SMPGUIDInfo`
    =================== ========== ==============================

.. class:: rdma.IBA.SAHeader

    An *aggregation* of: MADHeader, RMPPHeader

    SA Header (section 15.2.1.1)

    .. attribute:: MAD_LENGTH = 56
    .. attribute:: MAD_CLASS = 0x3
    .. attribute:: MAD_CLASS_VERSION = 0x2
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('RMPPVersion',8,1), ('RMPPType',8,1), ('RRespTime',5,1), ('RMPPFlags',3,1), ('RMPPStatus',8,1), ('data1',32,1), ('data2',32,1), ('SMKey',64,1), ('attributeOffset',16,1), ('reserved_368',16,1), ('componentMask',64,1)]

    ========================= ============ ============
    Member                    Position     Type        
    ========================= ============ ============
    :attr:`baseVersion`       0:1 (8)      :class:`int`
    :attr:`mgmtClass`         1:2 (8)      :class:`int`
    :attr:`classVersion`      2:3 (8)      :class:`int`
    :attr:`method`            3:4 (8)      :class:`int`
    :attr:`status`            4:6 (16)     :class:`int`
    :attr:`classSpecific`     6:8 (16)     :class:`int`
    :attr:`transactionID`     8:16 (64)    :class:`int`
    :attr:`attributeID`       16:18 (16)   :class:`int`
    :attr:`reserved_144`      18:20 (16)   :class:`int`
    :attr:`attributeModifier` 20:24 (32)   :class:`int`
    :attr:`RMPPVersion`       24:25 (8)    :class:`int`
    :attr:`RMPPType`          25:26 (8)    :class:`int`
    :attr:`RRespTime`         26:26[5] (5) :class:`int`
    :attr:`RMPPFlags`         26[5]:27 (3) :class:`int`
    :attr:`RMPPStatus`        27:28 (8)    :class:`int`
    :attr:`data1`             28:32 (32)   :class:`int`
    :attr:`data2`             32:36 (32)   :class:`int`
    :attr:`SMKey`             36:44 (64)   :class:`int`
    :attr:`attributeOffset`   44:46 (16)   :class:`int`
    :attr:`reserved_368`      46:48 (16)   :class:`int`
    :attr:`componentMask`     48:56 (64)   :class:`int`
    ========================= ============ ============

.. class:: rdma.IBA.SAInformInfoRecord

    Container for InformInfo (section 15.2.5.12)

    .. attribute:: MAD_LENGTH = 80
    .. attribute:: MAD_ATTRIBUTE_ID = 0xf3
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'subscriberGID':0, 'enumeration':1, 'reserved_144':2, 'reserved_160':3, 'informInfo.GID':4, 'informInfo.LIDRangeBegin':5, 'informInfo.LIDRangeEnd':6, 'informInfo.reserved_160':7, 'informInfo.isGeneric':8, 'informInfo.subscribe':9, 'informInfo.type':10, 'informInfo.trapNumber':11, 'informInfo.QPN':12, 'informInfo.reserved_248':13, 'informInfo.respTimeValue':14, 'informInfo.reserved_256':15, 'informInfo.producerType':16, 'reserved_480':17}
    .. attribute:: MEMBERS = [('subscriberGID',128,1), ('enumeration',16,1), ('reserved_144',16,1), ('reserved_160',32,1), ('informInfo',288,1), ('reserved_480',160,1)]

    ===================== =========== ================================
    Member                Position    Type                            
    ===================== =========== ================================
    :attr:`subscriberGID` 0:16 (128)  :class:`~rdma.IBA.GID`          
    :attr:`enumeration`   16:18 (16)  :class:`int`                    
    :attr:`reserved_144`  18:20 (16)  :class:`int`                    
    :attr:`reserved_160`  20:24 (32)  :class:`int`                    
    :attr:`informInfo`    24:60 (288) :class:`~rdma.IBA.MADInformInfo`
    :attr:`reserved_480`  60:80 (160) :class:`bytearray` (20)         
    ===================== =========== ================================

.. class:: rdma.IBA.SALinearForwardingTableRecord

    Container for LinearForwardingTable entry (section 15.2.5.6)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved_32':2, 'linearForwardingTable.portBlock':3}
    .. attribute:: MEMBERS = [('LID',16,1), ('blockNum',16,1), ('reserved_32',32,1), ('linearForwardingTable',512,1)]

    ============================= ========== ===========================================
    Member                        Position   Type                                       
    ============================= ========== ===========================================
    :attr:`LID`                   0:2 (16)   :class:`int`                               
    :attr:`blockNum`              2:4 (16)   :class:`int`                               
    :attr:`reserved_32`           4:8 (32)   :class:`int`                               
    :attr:`linearForwardingTable` 8:72 (512) :class:`~rdma.IBA.SMPLinearForwardingTable`
    ============================= ========== ===========================================

.. class:: rdma.IBA.SALinkRecord

    Inter-node linkage information (section 15.2.5.13)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'fromLID':0, 'fromPort':1, 'toPort':2, 'toLID':3, 'reserved_48':4}
    .. attribute:: MEMBERS = [('fromLID',16,1), ('fromPort',8,1), ('toPort',8,1), ('toLID',16,1), ('reserved_48',16,1)]

    =================== ======== ============
    Member              Position Type        
    =================== ======== ============
    :attr:`fromLID`     0:2 (16) :class:`int`
    :attr:`fromPort`    2:3 (8)  :class:`int`
    :attr:`toPort`      3:4 (8)  :class:`int`
    :attr:`toLID`       4:6 (16) :class:`int`
    :attr:`reserved_48` 6:8 (16) :class:`int`
    =================== ======== ============

.. class:: rdma.IBA.SAMCMemberRecord

    Multicast member attribute (section 15.2.5.17)

    .. attribute:: MAD_LENGTH = 52
    .. attribute:: MAD_ATTRIBUTE_ID = 0x38
    .. attribute:: MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: COMPONENT_MASK = {'MGID':0, 'portGID':1, 'QKey':2, 'MLID':3, 'MTUSelector':4, 'MTU':5, 'TClass':6, 'PKey':7, 'rateSelector':8, 'rate':9, 'packetLifeTimeSelector':10, 'packetLifeTime':11, 'SL':12, 'flowLabel':13, 'hopLimit':14, 'scope':15, 'joinState':16, 'proxyJoin':17, 'reserved_393':18}
    .. attribute:: MEMBERS = [('MGID',128,1), ('portGID',128,1), ('QKey',32,1), ('MLID',16,1), ('MTUSelector',2,1), ('MTU',6,1), ('TClass',8,1), ('PKey',16,1), ('rateSelector',2,1), ('rate',6,1), ('packetLifeTimeSelector',2,1), ('packetLifeTime',6,1), ('SL',4,1), ('flowLabel',20,1), ('hopLimit',8,1), ('scope',4,1), ('joinState',4,1), ('proxyJoin',1,1), ('reserved_393',23,1)]

    ============================== ============= ======================
    Member                         Position      Type                  
    ============================== ============= ======================
    :attr:`MGID`                   0:16 (128)    :class:`~rdma.IBA.GID`
    :attr:`portGID`                16:32 (128)   :class:`~rdma.IBA.GID`
    :attr:`QKey`                   32:36 (32)    :class:`int`          
    :attr:`MLID`                   36:38 (16)    :class:`int`          
    :attr:`MTUSelector`            38:38[2] (2)  :class:`int`          
    :attr:`MTU`                    38[2]:39 (6)  :class:`int`          
    :attr:`TClass`                 39:40 (8)     :class:`int`          
    :attr:`PKey`                   40:42 (16)    :class:`int`          
    :attr:`rateSelector`           42:42[2] (2)  :class:`int`          
    :attr:`rate`                   42[2]:43 (6)  :class:`int`          
    :attr:`packetLifeTimeSelector` 43:43[2] (2)  :class:`int`          
    :attr:`packetLifeTime`         43[2]:44 (6)  :class:`int`          
    :attr:`SL`                     44:44[4] (4)  :class:`int`          
    :attr:`flowLabel`              44[4]:47 (20) :class:`int`          
    :attr:`hopLimit`               47:48 (8)     :class:`int`          
    :attr:`scope`                  48:48[4] (4)  :class:`int`          
    :attr:`joinState`              48[4]:49 (4)  :class:`int`          
    :attr:`proxyJoin`              49:49[1] (1)  :class:`int`          
    :attr:`reserved_393`           49[1]:52 (23) :class:`int`          
    ============================== ============= ======================

.. class:: rdma.IBA.SAMultiPathRecord

    Request for multiple paths (section 15.2.5.20)

    .. attribute:: MAD_LENGTH = 40
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3a
    .. attribute:: MAD_SUBNADMGETMULTI = 0x14 # MAD_METHOD_GET_MULTI
    .. attribute:: COMPONENT_MASK = {'rawTraffic':0, 'reserved_1':1, 'flowLabel':2, 'hopLimit':3, 'TClass':4, 'reversible':5, 'numbPath':6, 'PKey':7, 'reserved_64':8, 'SL':9, 'MTUSelector':10, 'MTU':11, 'rateSelector':12, 'rate':13, 'packetLifeTimeSelector':14, 'packetLifeTime':15, 'reserved_104':16, 'independenceSelector':17, 'reserved_114':18, 'SGIDCount':19, 'DGIDCount':20, 'reserved_136':21, 'reserved_160':22, 'SDGID':23}
    .. attribute:: MEMBERS = [('rawTraffic',1,1), ('reserved_1',3,1), ('flowLabel',20,1), ('hopLimit',8,1), ('TClass',8,1), ('reversible',1,1), ('numbPath',7,1), ('PKey',16,1), ('reserved_64',12,1), ('SL',4,1), ('MTUSelector',2,1), ('MTU',6,1), ('rateSelector',2,1), ('rate',6,1), ('packetLifeTimeSelector',2,1), ('packetLifeTime',6,1), ('reserved_104',8,1), ('independenceSelector',2,1), ('reserved_114',6,1), ('SGIDCount',8,1), ('DGIDCount',8,1), ('reserved_136',24,1), ('reserved_160',32,1), ('SDGID',128,1)]

    ============================== ============= ======================
    Member                         Position      Type                  
    ============================== ============= ======================
    :attr:`rawTraffic`             0:0[1] (1)    :class:`int`          
    :attr:`reserved_1`             0[1]:0[4] (3) :class:`int`          
    :attr:`flowLabel`              0[4]:3 (20)   :class:`int`          
    :attr:`hopLimit`               3:4 (8)       :class:`int`          
    :attr:`TClass`                 4:5 (8)       :class:`int`          
    :attr:`reversible`             5:5[1] (1)    :class:`int`          
    :attr:`numbPath`               5[1]:6 (7)    :class:`int`          
    :attr:`PKey`                   6:8 (16)      :class:`int`          
    :attr:`reserved_64`            8:9[4] (12)   :class:`int`          
    :attr:`SL`                     9[4]:10 (4)   :class:`int`          
    :attr:`MTUSelector`            10:10[2] (2)  :class:`int`          
    :attr:`MTU`                    10[2]:11 (6)  :class:`int`          
    :attr:`rateSelector`           11:11[2] (2)  :class:`int`          
    :attr:`rate`                   11[2]:12 (6)  :class:`int`          
    :attr:`packetLifeTimeSelector` 12:12[2] (2)  :class:`int`          
    :attr:`packetLifeTime`         12[2]:13 (6)  :class:`int`          
    :attr:`reserved_104`           13:14 (8)     :class:`int`          
    :attr:`independenceSelector`   14:14[2] (2)  :class:`int`          
    :attr:`reserved_114`           14[2]:15 (6)  :class:`int`          
    :attr:`SGIDCount`              15:16 (8)     :class:`int`          
    :attr:`DGIDCount`              16:17 (8)     :class:`int`          
    :attr:`reserved_136`           17:20 (24)    :class:`int`          
    :attr:`reserved_160`           20:24 (32)    :class:`int`          
    :attr:`SDGID`                  24:40 (128)   :class:`~rdma.IBA.GID`
    ============================== ============= ======================

.. class:: rdma.IBA.SAMulticastForwardingTableRecord

    Container for MulticastForwardingTable entry (section 15.2.5.8)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'position':2, 'blockNum':3, 'reserved_32':4, 'multicastForwardingTable.portMaskBlock':5}
    .. attribute:: MEMBERS = [('LID',16,1), ('reserved_16',2,1), ('position',4,1), ('blockNum',10,1), ('reserved_32',32,1), ('multicastForwardingTable',512,1)]

    ================================ ============= ==============================================
    Member                           Position      Type                                          
    ================================ ============= ==============================================
    :attr:`LID`                      0:2 (16)      :class:`int`                                  
    :attr:`reserved_16`              2:2[2] (2)    :class:`int`                                  
    :attr:`position`                 2[2]:2[6] (4) :class:`int`                                  
    :attr:`blockNum`                 2[6]:4 (10)   :class:`int`                                  
    :attr:`reserved_32`              4:8 (32)      :class:`int`                                  
    :attr:`multicastForwardingTable` 8:72 (512)    :class:`~rdma.IBA.SMPMulticastForwardingTable`
    ================================ ============= ==============================================

.. class:: rdma.IBA.SANodeRecord

    Container for NodeInfo (section 15.2.5.2)

    .. attribute:: MAD_LENGTH = 108
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'nodeInfo.baseVersion':2, 'nodeInfo.classVersion':3, 'nodeInfo.nodeType':4, 'nodeInfo.numPorts':5, 'nodeInfo.systemImageGUID':6, 'nodeInfo.nodeGUID':7, 'nodeInfo.portGUID':8, 'nodeInfo.partitionCap':9, 'nodeInfo.deviceID':10, 'nodeInfo.revision':11, 'nodeInfo.localPortNum':12, 'nodeInfo.vendorID':13, 'nodeDescription.nodeString':14}
    .. attribute:: MEMBERS = [('LID',16,1), ('reserved_16',16,1), ('nodeInfo',320,1), ('nodeDescription',512,1)]

    ======================= ============ =====================================
    Member                  Position     Type                                 
    ======================= ============ =====================================
    :attr:`LID`             0:2 (16)     :class:`int`                         
    :attr:`reserved_16`     2:4 (16)     :class:`int`                         
    :attr:`nodeInfo`        4:44 (320)   :class:`~rdma.IBA.SMPNodeInfo`       
    :attr:`nodeDescription` 44:108 (512) :class:`~rdma.IBA.SMPNodeDescription`
    ======================= ============ =====================================

.. class:: rdma.IBA.SAPKeyTableRecord

    Container for P_Key Table (section 15.2.5.11)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x33
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'portNum':2, 'reserved_40':3, 'PKeyTable.PKeyBlock':4}
    .. attribute:: MEMBERS = [('LID',16,1), ('blockNum',16,1), ('portNum',8,1), ('reserved_40',24,1), ('PKeyTable',512,1)]

    =================== ========== ===============================
    Member              Position   Type                           
    =================== ========== ===============================
    :attr:`LID`         0:2 (16)   :class:`int`                   
    :attr:`blockNum`    2:4 (16)   :class:`int`                   
    :attr:`portNum`     4:5 (8)    :class:`int`                   
    :attr:`reserved_40` 5:8 (24)   :class:`int`                   
    :attr:`PKeyTable`   8:72 (512) :class:`~rdma.IBA.SMPPKeyTable`
    =================== ========== ===============================

.. class:: rdma.IBA.SAPathRecord

    Information on paths through the subnet (section 15.2.5.16)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x35
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'serviceID':0, 'serviceID56LSB':1, 'DGID':2, 'SGID':3, 'DLID':4, 'SLID':5, 'rawTraffic':6, 'reserved_353':7, 'flowLabel':8, 'hopLimit':9, 'TClass':10, 'reversible':11, 'numbPath':12, 'PKey':13, 'QOSClass':14, 'SL':15, 'MTUSelector':16, 'MTU':17, 'rateSelector':18, 'rate':19, 'packetLifeTimeSelector':20, 'packetLifeTime':21, 'preference':22, 'reserved_464':23, 'reserved_480':24}
    .. attribute:: MEMBERS = [('serviceID',64,1), ('DGID',128,1), ('SGID',128,1), ('DLID',16,1), ('SLID',16,1), ('rawTraffic',1,1), ('reserved_353',3,1), ('flowLabel',20,1), ('hopLimit',8,1), ('TClass',8,1), ('reversible',1,1), ('numbPath',7,1), ('PKey',16,1), ('QOSClass',12,1), ('SL',4,1), ('MTUSelector',2,1), ('MTU',6,1), ('rateSelector',2,1), ('rate',6,1), ('packetLifeTimeSelector',2,1), ('packetLifeTime',6,1), ('preference',8,1), ('reserved_464',16,1), ('reserved_480',32,1)]

    ============================== =============== ======================
    Member                         Position        Type                  
    ============================== =============== ======================
    :attr:`serviceID`              0:8 (64)        :class:`int`          
    :attr:`serviceID56LSB`         8:8 (0)         :class:`int`          
    :attr:`DGID`                   8:24 (128)      :class:`~rdma.IBA.GID`
    :attr:`SGID`                   24:40 (128)     :class:`~rdma.IBA.GID`
    :attr:`DLID`                   40:42 (16)      :class:`int`          
    :attr:`SLID`                   42:44 (16)      :class:`int`          
    :attr:`rawTraffic`             44:44[1] (1)    :class:`int`          
    :attr:`reserved_353`           44[1]:44[4] (3) :class:`int`          
    :attr:`flowLabel`              44[4]:47 (20)   :class:`int`          
    :attr:`hopLimit`               47:48 (8)       :class:`int`          
    :attr:`TClass`                 48:49 (8)       :class:`int`          
    :attr:`reversible`             49:49[1] (1)    :class:`int`          
    :attr:`numbPath`               49[1]:50 (7)    :class:`int`          
    :attr:`PKey`                   50:52 (16)      :class:`int`          
    :attr:`QOSClass`               52:53[4] (12)   :class:`int`          
    :attr:`SL`                     53[4]:54 (4)    :class:`int`          
    :attr:`MTUSelector`            54:54[2] (2)    :class:`int`          
    :attr:`MTU`                    54[2]:55 (6)    :class:`int`          
    :attr:`rateSelector`           55:55[2] (2)    :class:`int`          
    :attr:`rate`                   55[2]:56 (6)    :class:`int`          
    :attr:`packetLifeTimeSelector` 56:56[2] (2)    :class:`int`          
    :attr:`packetLifeTime`         56[2]:57 (6)    :class:`int`          
    :attr:`preference`             57:58 (8)       :class:`int`          
    :attr:`reserved_464`           58:60 (16)      :class:`int`          
    :attr:`reserved_480`           60:64 (32)      :class:`int`          
    ============================== =============== ======================

.. class:: rdma.IBA.SAPortInfoRecord

    Container for PortInfo (section 15.2.5.3)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'endportLID':0, 'portNum':1, 'reserved_24':2, 'portInfo.MKey':3, 'portInfo.GIDPrefix':4, 'portInfo.LID':5, 'portInfo.masterSMLID':6, 'portInfo.capabilityMask':7, 'portInfo.diagCode':8, 'portInfo.MKeyLeasePeriod':9, 'portInfo.localPortNum':10, 'portInfo.linkWidthEnabled':11, 'portInfo.linkWidthSupported':12, 'portInfo.linkWidthActive':13, 'portInfo.linkSpeedSupported':14, 'portInfo.portState':15, 'portInfo.portPhysicalState':16, 'portInfo.linkDownDefaultState':17, 'portInfo.MKeyProtectBits':18, 'portInfo.reserved_274':19, 'portInfo.LMC':20, 'portInfo.linkSpeedActive':21, 'portInfo.linkSpeedEnabled':22, 'portInfo.neighborMTU':23, 'portInfo.masterSMSL':24, 'portInfo.VLCap':25, 'portInfo.initType':26, 'portInfo.VLHighLimit':27, 'portInfo.VLArbitrationHighCap':28, 'portInfo.VLArbitrationLowCap':29, 'portInfo.initTypeReply':30, 'portInfo.MTUCap':31, 'portInfo.VLStallCount':32, 'portInfo.HOQLife':33, 'portInfo.operationalVLs':34, 'portInfo.partitionEnforcementInbound':35, 'portInfo.partitionEnforcementOutbound':36, 'portInfo.filterRawInbound':37, 'portInfo.filterRawOutbound':38, 'portInfo.MKeyViolations':39, 'portInfo.PKeyViolations':40, 'portInfo.QKeyViolations':41, 'portInfo.GUIDCap':42, 'portInfo.clientReregister':43, 'portInfo.reserved_409':44, 'portInfo.subnetTimeOut':45, 'portInfo.reserved_416':46, 'portInfo.respTimeValue':47, 'portInfo.localPhyErrors':48, 'portInfo.overrunErrors':49, 'portInfo.maxCreditHint':50, 'portInfo.reserved_448':51, 'portInfo.linkRoundTripLatency':52}
    .. attribute:: MEMBERS = [('endportLID',16,1), ('portNum',8,1), ('reserved_24',8,1), ('portInfo',480,1)]

    =================== ========== ==============================
    Member              Position   Type                          
    =================== ========== ==============================
    :attr:`endportLID`  0:2 (16)   :class:`int`                  
    :attr:`portNum`     2:3 (8)    :class:`int`                  
    :attr:`reserved_24` 3:4 (8)    :class:`int`                  
    :attr:`portInfo`    4:64 (480) :class:`~rdma.IBA.SMPPortInfo`
    =================== ========== ==============================

.. class:: rdma.IBA.SARandomForwardingTableRecord

    Container for RandomForwardingTable entry (section 15.2.5.7)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved_32':2, 'randomForwardingTable.LIDPortBlock':3}
    .. attribute:: MEMBERS = [('LID',16,1), ('blockNum',16,1), ('reserved_32',32,1), ('randomForwardingTable',512,1)]

    ============================= ========== ===========================================
    Member                        Position   Type                                       
    ============================= ========== ===========================================
    :attr:`LID`                   0:2 (16)   :class:`int`                               
    :attr:`blockNum`              2:4 (16)   :class:`int`                               
    :attr:`reserved_32`           4:8 (32)   :class:`int`                               
    :attr:`randomForwardingTable` 8:72 (512) :class:`~rdma.IBA.SMPRandomForwardingTable`
    ============================= ========== ===========================================

.. class:: rdma.IBA.SASLToVLMappingTableRecord

    Container for SLtoVLMappingTable entry (section 15.2.5.4)

    .. attribute:: MAD_LENGTH = 16
    .. attribute:: MAD_ATTRIBUTE_ID = 0x13
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'inputPortNum':1, 'outputPortNum':2, 'reserved_32':3, 'SLToVLMappingTable.SLtoVL':4}
    .. attribute:: MEMBERS = [('LID',16,1), ('inputPortNum',8,1), ('outputPortNum',8,1), ('reserved_32',32,1), ('SLToVLMappingTable',64,1)]

    ========================== ========= ========================================
    Member                     Position  Type                                    
    ========================== ========= ========================================
    :attr:`LID`                0:2 (16)  :class:`int`                            
    :attr:`inputPortNum`       2:3 (8)   :class:`int`                            
    :attr:`outputPortNum`      3:4 (8)   :class:`int`                            
    :attr:`reserved_32`        4:8 (32)  :class:`int`                            
    :attr:`SLToVLMappingTable` 8:16 (64) :class:`~rdma.IBA.SMPSLToVLMappingTable`
    ========================== ========= ========================================

.. class:: rdma.IBA.SASMInfoRecord

    Container for SMInfo (section 15.2.5.10)

    .. attribute:: MAD_LENGTH = 28
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'SMInfo.GUID':2, 'SMInfo.SMKey':3, 'SMInfo.actCount':4, 'SMInfo.priority':5, 'SMInfo.SMState':6, 'SMInfo.reserved_168':7}
    .. attribute:: MEMBERS = [('LID',16,1), ('reserved_16',16,1), ('SMInfo',192,1)]

    =================== ========== ============================
    Member              Position   Type                        
    =================== ========== ============================
    :attr:`LID`         0:2 (16)   :class:`int`                
    :attr:`reserved_16` 2:4 (16)   :class:`int`                
    :attr:`SMInfo`      4:28 (192) :class:`~rdma.IBA.SMPSMInfo`
    =================== ========== ============================

.. class:: rdma.IBA.SAServiceAssociationRecord

    ServiceRecord ServiceName/ServiceKey association (section 15.2.5.15)

    .. attribute:: MAD_LENGTH = 80
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3b
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'serviceKey':0, 'serviceName':1}
    .. attribute:: MEMBERS = [('serviceKey',128,1), ('serviceName',8,64)]

    =================== ========== ============================
    Member              Position   Type                        
    =================== ========== ============================
    :attr:`serviceKey`  0:16 (128) :class:`~rdma.IBA.GID`      
    :attr:`serviceName` 16:80 (8)  [:class:`bytearray` (64)]*64
    =================== ========== ============================

.. class:: rdma.IBA.SAServiceRecord

    Information on advertised services (section 15.2.5.14)

    .. attribute:: MAD_LENGTH = 176
    .. attribute:: MAD_ATTRIBUTE_ID = 0x31
    .. attribute:: MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: COMPONENT_MASK = {'serviceID':0, 'serviceGID':1, 'servicePKey':2, 'reserved_208':3, 'serviceLease':4, 'serviceKey':5, 'serviceName':6, 'serviceData8':7, 'serviceData16':8, 'serviceData32':9, 'serviceData64':10}
    .. attribute:: MEMBERS = [('serviceID',64,1), ('serviceGID',128,1), ('servicePKey',16,1), ('reserved_208',16,1), ('serviceLease',32,1), ('serviceKey',128,1), ('serviceName',8,64), ('serviceData8',8,16), ('serviceData16',16,8), ('serviceData32',32,4), ('serviceData64',64,2)]

    ===================== ============ ============================
    Member                Position     Type                        
    ===================== ============ ============================
    :attr:`serviceID`     0:8 (64)     :class:`int`                
    :attr:`serviceGID`    8:24 (128)   :class:`~rdma.IBA.GID`      
    :attr:`servicePKey`   24:26 (16)   :class:`int`                
    :attr:`reserved_208`  26:28 (16)   :class:`int`                
    :attr:`serviceLease`  28:32 (32)   :class:`int`                
    :attr:`serviceKey`    32:48 (128)  :class:`~rdma.IBA.GID`      
    :attr:`serviceName`   48:112 (8)   [:class:`bytearray` (64)]*64
    :attr:`serviceData8`  112:128 (8)  [:class:`bytearray` (16)]*16
    :attr:`serviceData16` 128:144 (16) [:class:`int`]*8            
    :attr:`serviceData32` 144:160 (32) [:class:`int`]*4            
    :attr:`serviceData64` 160:176 (64) [:class:`int`]*2            
    ===================== ============ ============================

.. class:: rdma.IBA.SASwitchInfoRecord

    Container for SwitchInfo (section 15.2.5.5)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved_16':1, 'switchInfo.linearFDBCap':2, 'switchInfo.randomFDBCap':3, 'switchInfo.multicastFDBCap':4, 'switchInfo.linearFDBTop':5, 'switchInfo.defaultPort':6, 'switchInfo.defaultMulticastPrimaryPort':7, 'switchInfo.defaultMulticastNotPrimaryPort':8, 'switchInfo.lifeTimeValue':9, 'switchInfo.portStateChange':10, 'switchInfo.optimizedSLtoVLMappingProgramming':11, 'switchInfo.LIDsPerPort':12, 'switchInfo.partitionEnforcementCap':13, 'switchInfo.inboundEnforcementCap':14, 'switchInfo.outboundEnforcementCap':15, 'switchInfo.filterRawInboundCap':16, 'switchInfo.filterRawOutboundCap':17, 'switchInfo.enhancedPort0':18, 'switchInfo.reserved_133':19, 'switchInfo.reserved_136':20}
    .. attribute:: MEMBERS = [('LID',16,1), ('reserved_16',16,1), ('switchInfo',160,1)]

    =================== ========== ================================
    Member              Position   Type                            
    =================== ========== ================================
    :attr:`LID`         0:2 (16)   :class:`int`                    
    :attr:`reserved_16` 2:4 (16)   :class:`int`                    
    :attr:`switchInfo`  4:24 (160) :class:`~rdma.IBA.SMPSwitchInfo`
    =================== ========== ================================

.. class:: rdma.IBA.SATraceRecord

    Path trace information (section 15.2.5.19)

    .. attribute:: MAD_LENGTH = 48
    .. attribute:: MAD_ATTRIBUTE_ID = 0x39
    .. attribute:: MAD_SUBNADMGETTRACETABLE = 0x13 # MAD_METHOD_GET_TRACE_TABLE
    .. attribute:: COMPONENT_MASK = {'GIDPrefix':0, 'IDGeneration':1, 'reserved_80':2, 'nodeType':3, 'nodeID':4, 'chassisID':5, 'entryPortID':6, 'exitPortID':7, 'entryPort':8, 'exitPort':9, 'reserved_368':10}
    .. attribute:: MEMBERS = [('GIDPrefix',64,1), ('IDGeneration',16,1), ('reserved_80',8,1), ('nodeType',8,1), ('nodeID',64,1), ('chassisID',64,1), ('entryPortID',64,1), ('exitPortID',64,1), ('entryPort',8,1), ('exitPort',8,1), ('reserved_368',16,1)]

    ==================== ========== ============
    Member               Position   Type        
    ==================== ========== ============
    :attr:`GIDPrefix`    0:8 (64)   :class:`int`
    :attr:`IDGeneration` 8:10 (16)  :class:`int`
    :attr:`reserved_80`  10:11 (8)  :class:`int`
    :attr:`nodeType`     11:12 (8)  :class:`int`
    :attr:`nodeID`       12:20 (64) :class:`int`
    :attr:`chassisID`    20:28 (64) :class:`int`
    :attr:`entryPortID`  28:36 (64) :class:`int`
    :attr:`exitPortID`   36:44 (64) :class:`int`
    :attr:`entryPort`    44:45 (8)  :class:`int`
    :attr:`exitPort`     45:46 (8)  :class:`int`
    :attr:`reserved_368` 46:48 (16) :class:`int`
    ==================== ========== ============

.. class:: rdma.IBA.SAVLArbitrationTableRecord

    Container for VLArbitrationTable entry (section 15.2.5.9)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x36
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'outputPortNum':1, 'blockNum':2, 'reserved_32':3, 'VLArbitrationTable.VLWeightBlock':4}
    .. attribute:: MEMBERS = [('LID',16,1), ('outputPortNum',8,1), ('blockNum',8,1), ('reserved_32',32,1), ('VLArbitrationTable',512,1)]

    ========================== ========== ========================================
    Member                     Position   Type                                    
    ========================== ========== ========================================
    :attr:`LID`                0:2 (16)   :class:`int`                            
    :attr:`outputPortNum`      2:3 (8)    :class:`int`                            
    :attr:`blockNum`           3:4 (8)    :class:`int`                            
    :attr:`reserved_32`        4:8 (32)   :class:`int`                            
    :attr:`VLArbitrationTable` 8:72 (512) :class:`~rdma.IBA.SMPVLArbitrationTable`
    ========================== ========== ========================================

Performance Management (16.1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.PMFormat

    An *aggregation* of: MADHeader

    Performance Management MAD Format (section 16.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x4
    .. attribute:: MAD_CLASS_VERSION = 0x1
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('reserved_192',320,1), ('data',1536,1)]

    ========================= ============= ========================
    Member                    Position      Type                    
    ========================= ============= ========================
    :attr:`baseVersion`       0:1 (8)       :class:`int`            
    :attr:`mgmtClass`         1:2 (8)       :class:`int`            
    :attr:`classVersion`      2:3 (8)       :class:`int`            
    :attr:`method`            3:4 (8)       :class:`int`            
    :attr:`status`            4:6 (16)      :class:`int`            
    :attr:`classSpecific`     6:8 (16)      :class:`int`            
    :attr:`transactionID`     8:16 (64)     :class:`int`            
    :attr:`attributeID`       16:18 (16)    :class:`int`            
    :attr:`reserved_144`      18:20 (16)    :class:`int`            
    :attr:`attributeModifier` 20:24 (32)    :class:`int`            
    :attr:`reserved_192`      24:64 (320)   :class:`bytearray` (40) 
    :attr:`data`              64:256 (1536) :class:`bytearray` (192)
    ========================= ============= ========================

.. class:: rdma.IBA.PMPortCounters

    Port Basic Performance and Error Counters (section 16.1.3.5)

    .. attribute:: MAD_LENGTH = 44
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('symbolErrorCounter',16,1), ('linkErrorRecoveryCounter',8,1), ('linkDownedCounter',8,1), ('portRcvErrors',16,1), ('portRcvRemotePhysicalErrors',16,1), ('portRcvSwitchRelayErrors',16,1), ('portXmitDiscards',16,1), ('portXmitConstraintErrors',8,1), ('portRcvConstraintErrors',8,1), ('counterSelect2',8,1), ('localLinkIntegrityErrors',4,1), ('excessiveBufferOverrunErrors',4,1), ('reserved_160',16,1), ('VL15Dropped',16,1), ('portXmitData',32,1), ('portRcvData',32,1), ('portXmitPkts',32,1), ('portRcvPkts',32,1), ('portXmitWait',32,1)]

    ==================================== ============ ============
    Member                               Position     Type        
    ==================================== ============ ============
    :attr:`reserved_0`                   0:1 (8)      :class:`int`
    :attr:`portSelect`                   1:2 (8)      :class:`int`
    :attr:`counterSelect`                2:4 (16)     :class:`int`
    :attr:`symbolErrorCounter`           4:6 (16)     :class:`int`
    :attr:`linkErrorRecoveryCounter`     6:7 (8)      :class:`int`
    :attr:`linkDownedCounter`            7:8 (8)      :class:`int`
    :attr:`portRcvErrors`                8:10 (16)    :class:`int`
    :attr:`portRcvRemotePhysicalErrors`  10:12 (16)   :class:`int`
    :attr:`portRcvSwitchRelayErrors`     12:14 (16)   :class:`int`
    :attr:`portXmitDiscards`             14:16 (16)   :class:`int`
    :attr:`portXmitConstraintErrors`     16:17 (8)    :class:`int`
    :attr:`portRcvConstraintErrors`      17:18 (8)    :class:`int`
    :attr:`counterSelect2`               18:19 (8)    :class:`int`
    :attr:`localLinkIntegrityErrors`     19:19[4] (4) :class:`int`
    :attr:`excessiveBufferOverrunErrors` 19[4]:20 (4) :class:`int`
    :attr:`reserved_160`                 20:22 (16)   :class:`int`
    :attr:`VL15Dropped`                  22:24 (16)   :class:`int`
    :attr:`portXmitData`                 24:28 (32)   :class:`int`
    :attr:`portRcvData`                  28:32 (32)   :class:`int`
    :attr:`portXmitPkts`                 32:36 (32)   :class:`int`
    :attr:`portRcvPkts`                  36:40 (32)   :class:`int`
    :attr:`portXmitWait`                 40:44 (32)   :class:`int`
    ==================================== ============ ============

.. class:: rdma.IBA.PMPortCountersExt

    Extended Port Counters (section 16.1.4.11)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1d
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('reserved_32',32,1), ('portXmitData',64,1), ('portRcvData',64,1), ('portXmitPkts',64,1), ('portRcvPkts',64,1), ('portUnicastXmitPkts',64,1), ('portUnicastRcvPkts',64,1), ('portMulticastXmitPkts',64,1), ('portMulticastRcvPkts',64,1)]

    ============================= ========== ============
    Member                        Position   Type        
    ============================= ========== ============
    :attr:`reserved_0`            0:1 (8)    :class:`int`
    :attr:`portSelect`            1:2 (8)    :class:`int`
    :attr:`counterSelect`         2:4 (16)   :class:`int`
    :attr:`reserved_32`           4:8 (32)   :class:`int`
    :attr:`portXmitData`          8:16 (64)  :class:`int`
    :attr:`portRcvData`           16:24 (64) :class:`int`
    :attr:`portXmitPkts`          24:32 (64) :class:`int`
    :attr:`portRcvPkts`           32:40 (64) :class:`int`
    :attr:`portUnicastXmitPkts`   40:48 (64) :class:`int`
    :attr:`portUnicastRcvPkts`    48:56 (64) :class:`int`
    :attr:`portMulticastXmitPkts` 56:64 (64) :class:`int`
    :attr:`portMulticastRcvPkts`  64:72 (64) :class:`int`
    ============================= ========== ============

.. class:: rdma.IBA.PMPortFlowCtlCounters

    Port Flow Control Counters (section 16.1.4.4)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portXmitFlowPkts',32,1), ('portRcvFlowPkts',32,1)]

    ======================== ========= ============
    Member                   Position  Type        
    ======================== ========= ============
    :attr:`reserved_0`       0:1 (8)   :class:`int`
    :attr:`portSelect`       1:2 (8)   :class:`int`
    :attr:`counterSelect`    2:4 (16)  :class:`int`
    :attr:`portXmitFlowPkts` 4:8 (32)  :class:`int`
    :attr:`portRcvFlowPkts`  8:12 (32) :class:`int`
    ======================== ========= ============

.. class:: rdma.IBA.PMPortOpRcvCounters

    Port Receive Counters per Op Code (section 16.1.4.3)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portOpRcvPkts',32,1), ('portOpRcvData',32,1)]

    ===================== ========= ============
    Member                Position  Type        
    ===================== ========= ============
    :attr:`opCode`        0:1 (8)   :class:`int`
    :attr:`portSelect`    1:2 (8)   :class:`int`
    :attr:`counterSelect` 2:4 (16)  :class:`int`
    :attr:`portOpRcvPkts` 4:8 (32)  :class:`int`
    :attr:`portOpRcvData` 8:12 (32) :class:`int`
    ===================== ========= ============

.. class:: rdma.IBA.PMPortRcvErrorDetails

    Port Detailed Error Counters (section 16.1.4.1)

    .. attribute:: MAD_LENGTH = 16
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portLocalPhysicalErrors',16,1), ('portMalformedPacketErrors',16,1), ('portBufferOverrunErrors',16,1), ('portDLIDMappingErrors',16,1), ('portVLMappingErrors',16,1), ('portLoopingErrors',16,1)]

    ================================= ========== ============
    Member                            Position   Type        
    ================================= ========== ============
    :attr:`reserved_0`                0:1 (8)    :class:`int`
    :attr:`portSelect`                1:2 (8)    :class:`int`
    :attr:`counterSelect`             2:4 (16)   :class:`int`
    :attr:`portLocalPhysicalErrors`   4:6 (16)   :class:`int`
    :attr:`portMalformedPacketErrors` 6:8 (16)   :class:`int`
    :attr:`portBufferOverrunErrors`   8:10 (16)  :class:`int`
    :attr:`portDLIDMappingErrors`     10:12 (16) :class:`int`
    :attr:`portVLMappingErrors`       12:14 (16) :class:`int`
    :attr:`portLoopingErrors`         14:16 (16) :class:`int`
    ================================= ========== ============

.. class:: rdma.IBA.PMPortSamplesCtl

    Port Performance Data Sampling Control (section 16.1.3.2)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('tick',8,1), ('reserved_24',5,1), ('counterWidth',3,1), ('reserved_32',2,1), ('counterMask0',3,1), ('counterMask1',3,1), ('counterMask2',3,1), ('counterMask3',3,1), ('counterMask4',3,1), ('counterMask5',3,1), ('counterMask6',3,1), ('counterMask7',3,1), ('counterMask8',3,1), ('counterMask9',3,1), ('reserved_64',1,1), ('counterMask10',3,1), ('counterMask11',3,1), ('counterMask12',3,1), ('counterMask13',3,1), ('counterMask14',3,1), ('sampleMechanisms',8,1), ('reserved_88',6,1), ('sampleStatus',2,1), ('optionMask',64,1), ('vendorMask',64,1), ('sampleStart',32,1), ('sampleInterval',32,1), ('tag',16,1), ('counterSelect0',16,1), ('counterSelect1',16,1), ('counterSelect2',16,1), ('counterSelect3',16,1), ('counterSelect4',16,1), ('counterSelect5',16,1), ('counterSelect6',16,1), ('counterSelect7',16,1), ('counterSelect8',16,1), ('counterSelect9',16,1), ('counterSelect10',16,1), ('counterSelect11',16,1), ('counterSelect12',16,1), ('counterSelect13',16,1), ('counterSelect14',16,1), ('reserved_544',32,1), ('samplesOnlyOptionMask',64,1), ('reserved_640',896,1)]

    ============================= ============= ========================
    Member                        Position      Type                    
    ============================= ============= ========================
    :attr:`opCode`                0:1 (8)       :class:`int`            
    :attr:`portSelect`            1:2 (8)       :class:`int`            
    :attr:`tick`                  2:3 (8)       :class:`int`            
    :attr:`reserved_24`           3:3[5] (5)    :class:`int`            
    :attr:`counterWidth`          3[5]:4 (3)    :class:`int`            
    :attr:`reserved_32`           4:4[2] (2)    :class:`int`            
    :attr:`counterMask0`          4[2]:4[5] (3) :class:`int`            
    :attr:`counterMask1`          4[5]:5 (3)    :class:`int`            
    :attr:`counterMask2`          5:5[3] (3)    :class:`int`            
    :attr:`counterMask3`          5[3]:5[6] (3) :class:`int`            
    :attr:`counterMask4`          5[6]:6[1] (3) :class:`int`            
    :attr:`counterMask5`          6[1]:6[4] (3) :class:`int`            
    :attr:`counterMask6`          6[4]:6[7] (3) :class:`int`            
    :attr:`counterMask7`          6[7]:7[2] (3) :class:`int`            
    :attr:`counterMask8`          7[2]:7[5] (3) :class:`int`            
    :attr:`counterMask9`          7[5]:8 (3)    :class:`int`            
    :attr:`reserved_64`           8:8[1] (1)    :class:`int`            
    :attr:`counterMask10`         8[1]:8[4] (3) :class:`int`            
    :attr:`counterMask11`         8[4]:8[7] (3) :class:`int`            
    :attr:`counterMask12`         8[7]:9[2] (3) :class:`int`            
    :attr:`counterMask13`         9[2]:9[5] (3) :class:`int`            
    :attr:`counterMask14`         9[5]:10 (3)   :class:`int`            
    :attr:`sampleMechanisms`      10:11 (8)     :class:`int`            
    :attr:`reserved_88`           11:11[6] (6)  :class:`int`            
    :attr:`sampleStatus`          11[6]:12 (2)  :class:`int`            
    :attr:`optionMask`            12:20 (64)    :class:`int`            
    :attr:`vendorMask`            20:28 (64)    :class:`int`            
    :attr:`sampleStart`           28:32 (32)    :class:`int`            
    :attr:`sampleInterval`        32:36 (32)    :class:`int`            
    :attr:`tag`                   36:38 (16)    :class:`int`            
    :attr:`counterSelect0`        38:40 (16)    :class:`int`            
    :attr:`counterSelect1`        40:42 (16)    :class:`int`            
    :attr:`counterSelect2`        42:44 (16)    :class:`int`            
    :attr:`counterSelect3`        44:46 (16)    :class:`int`            
    :attr:`counterSelect4`        46:48 (16)    :class:`int`            
    :attr:`counterSelect5`        48:50 (16)    :class:`int`            
    :attr:`counterSelect6`        50:52 (16)    :class:`int`            
    :attr:`counterSelect7`        52:54 (16)    :class:`int`            
    :attr:`counterSelect8`        54:56 (16)    :class:`int`            
    :attr:`counterSelect9`        56:58 (16)    :class:`int`            
    :attr:`counterSelect10`       58:60 (16)    :class:`int`            
    :attr:`counterSelect11`       60:62 (16)    :class:`int`            
    :attr:`counterSelect12`       62:64 (16)    :class:`int`            
    :attr:`counterSelect13`       64:66 (16)    :class:`int`            
    :attr:`counterSelect14`       66:68 (16)    :class:`int`            
    :attr:`reserved_544`          68:72 (32)    :class:`int`            
    :attr:`samplesOnlyOptionMask` 72:80 (64)    :class:`int`            
    :attr:`reserved_640`          80:192 (896)  :class:`bytearray` (112)
    ============================= ============= ========================

.. class:: rdma.IBA.PMPortSamplesRes

    Port Performance Data Sampling Results (section 16.1.3.4)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('tag',16,1), ('reserved_16',14,1), ('sampleStatus',2,1), ('counter',32,15)]

    ==================== =========== =================
    Member               Position    Type             
    ==================== =========== =================
    :attr:`tag`          0:2 (16)    :class:`int`     
    :attr:`reserved_16`  2:3[6] (14) :class:`int`     
    :attr:`sampleStatus` 3[6]:4 (2)  :class:`int`     
    :attr:`counter`      4:64 (32)   [:class:`int`]*15
    ==================== =========== =================

.. class:: rdma.IBA.PMPortSamplesResExt

    Extended Port Samples Result (section 16.1.4.10)

    .. attribute:: MAD_LENGTH = 128
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1e
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('tag',16,1), ('reserved_16',14,1), ('sampleStatus',2,1), ('extendedWidth',2,1), ('reserved_34',30,1), ('counter',64,15)]

    ===================== =========== =================
    Member                Position    Type             
    ===================== =========== =================
    :attr:`tag`           0:2 (16)    :class:`int`     
    :attr:`reserved_16`   2:3[6] (14) :class:`int`     
    :attr:`sampleStatus`  3[6]:4 (2)  :class:`int`     
    :attr:`extendedWidth` 4:4[2] (2)  :class:`int`     
    :attr:`reserved_34`   4[2]:8 (30) :class:`int`     
    :attr:`counter`       8:128 (64)  [:class:`int`]*15
    ===================== =========== =================

.. class:: rdma.IBA.PMPortVLOpData

    Port Kilobytes Received per Op Code per VL (section 16.1.4.6)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLOpData',32,16)]

    ===================== ========= =================
    Member                Position  Type             
    ===================== ========= =================
    :attr:`opCode`        0:1 (8)   :class:`int`     
    :attr:`portSelect`    1:2 (8)   :class:`int`     
    :attr:`counterSelect` 2:4 (16)  :class:`int`     
    :attr:`portVLOpData`  4:68 (32) [:class:`int`]*16
    ===================== ========= =================

.. class:: rdma.IBA.PMPortVLOpPackets

    Port Packets Received per Op Code per VL (section 16.1.4.5)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('opCode',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLOpPackets',16,16)]

    ======================= ========= =================
    Member                  Position  Type             
    ======================= ========= =================
    :attr:`opCode`          0:1 (8)   :class:`int`     
    :attr:`portSelect`      1:2 (8)   :class:`int`     
    :attr:`counterSelect`   2:4 (16)  :class:`int`     
    :attr:`portVLOpPackets` 4:36 (16) [:class:`int`]*16
    ======================= ========= =================

.. class:: rdma.IBA.PMPortVLXmitFlowCtlUpdateErrors

    Port Flow Control update errors per VL (section 16.1.4.7)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1b
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLXmitFlowCtlUpdateErrors',2,16)]

    ===================================== ======== =================
    Member                                Position Type             
    ===================================== ======== =================
    :attr:`reserved_0`                    0:1 (8)  :class:`int`     
    :attr:`portSelect`                    1:2 (8)  :class:`int`     
    :attr:`counterSelect`                 2:4 (16) :class:`int`     
    :attr:`portVLXmitFlowCtlUpdateErrors` 4:8 (2)  [:class:`int`]*16
    ===================================== ======== =================

.. class:: rdma.IBA.PMPortVLXmitWaitCounters

    Port Ticks Waiting to Transmit Counters per VL (section 16.1.4.8)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1c
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portVLXmitWait',16,16)]

    ====================== ========= =================
    Member                 Position  Type             
    ====================== ========= =================
    :attr:`reserved_0`     0:1 (8)   :class:`int`     
    :attr:`portSelect`     1:2 (8)   :class:`int`     
    :attr:`counterSelect`  2:4 (16)  :class:`int`     
    :attr:`portVLXmitWait` 4:36 (16) [:class:`int`]*16
    ====================== ========= =================

.. class:: rdma.IBA.PMPortXmitDiscardDetails

    Port Transmit Discard Counters (section 16.1.4.2)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portInactiveDiscards',16,1), ('portNeighborMTUDiscards',16,1), ('portSwLifetimeLimitDiscards',16,1), ('portSwHOQLimitDiscards',16,1)]

    =================================== ========== ============
    Member                              Position   Type        
    =================================== ========== ============
    :attr:`reserved_0`                  0:1 (8)    :class:`int`
    :attr:`portSelect`                  1:2 (8)    :class:`int`
    :attr:`counterSelect`               2:4 (16)   :class:`int`
    :attr:`portInactiveDiscards`        4:6 (16)   :class:`int`
    :attr:`portNeighborMTUDiscards`     6:8 (16)   :class:`int`
    :attr:`portSwLifetimeLimitDiscards` 8:10 (16)  :class:`int`
    :attr:`portSwHOQLimitDiscards`      10:12 (16) :class:`int`
    =================================== ========== ============

.. class:: rdma.IBA.PMSwPortVLCongestion

    Switch Port Congestion per VL (section 16.1.4.9)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('swPortVLCongestion',16,16)]

    ========================== ========= =================
    Member                     Position  Type             
    ========================== ========= =================
    :attr:`reserved_0`         0:1 (8)   :class:`int`     
    :attr:`portSelect`         1:2 (8)   :class:`int`     
    :attr:`counterSelect`      2:4 (16)  :class:`int`     
    :attr:`swPortVLCongestion` 4:36 (16) [:class:`int`]*16
    ========================== ========= =================

.. class:: rdma.IBA.PMPortRcvDataSL

    Receive SL Port Counters (section A13.6.5)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x37
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portRcvDataSL',32,16)]

    ===================== ========= =================
    Member                Position  Type             
    ===================== ========= =================
    :attr:`reserved_0`    0:1 (8)   :class:`int`     
    :attr:`portSelect`    1:2 (8)   :class:`int`     
    :attr:`counterSelect` 2:4 (16)  :class:`int`     
    :attr:`portRcvDataSL` 4:68 (32) [:class:`int`]*16
    ===================== ========= =================

.. class:: rdma.IBA.PMPortXmitDataSL

    Transmit SL Port Counters (section A13.6.5)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x36
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('portSelect',8,1), ('counterSelect',16,1), ('portXmitDataSL',32,16)]

    ====================== ========= =================
    Member                 Position  Type             
    ====================== ========= =================
    :attr:`reserved_0`     0:1 (8)   :class:`int`     
    :attr:`portSelect`     1:2 (8)   :class:`int`     
    :attr:`counterSelect`  2:4 (16)  :class:`int`     
    :attr:`portXmitDataSL` 4:68 (32) [:class:`int`]*16
    ====================== ========= =================

Device Management (16.3)
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.DMDiagCode

    Vendor-Specific Device Diagnostic Information (section 16.3.3.10)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x24
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('diagCode',16,1), ('reserved_16',16,1)]

    =================== ======== ============
    Member              Position Type        
    =================== ======== ============
    :attr:`diagCode`    0:2 (16) :class:`int`
    :attr:`reserved_16` 2:4 (16) :class:`int`
    =================== ======== ============

.. class:: rdma.IBA.DMDiagnosticTimeout

    Get the Maximum Time for Completion of a Diagnostic Test (section 16.3.3.6)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('maxDiagTime',32,1)]

    =================== ======== ============
    Member              Position Type        
    =================== ======== ============
    :attr:`maxDiagTime` 0:4 (32) :class:`int`
    =================== ======== ============

.. class:: rdma.IBA.DMFormat

    An *aggregation* of: MADHeader

    Device Management MAD Format (section 16.3.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x6
    .. attribute:: MAD_CLASS_VERSION = 0x1
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('reserved_192',320,1), ('data',1536,1)]

    ========================= ============= ========================
    Member                    Position      Type                    
    ========================= ============= ========================
    :attr:`baseVersion`       0:1 (8)       :class:`int`            
    :attr:`mgmtClass`         1:2 (8)       :class:`int`            
    :attr:`classVersion`      2:3 (8)       :class:`int`            
    :attr:`method`            3:4 (8)       :class:`int`            
    :attr:`status`            4:6 (16)      :class:`int`            
    :attr:`classSpecific`     6:8 (16)      :class:`int`            
    :attr:`transactionID`     8:16 (64)     :class:`int`            
    :attr:`attributeID`       16:18 (16)    :class:`int`            
    :attr:`reserved_144`      18:20 (16)    :class:`int`            
    :attr:`attributeModifier` 20:24 (32)    :class:`int`            
    :attr:`reserved_192`      24:64 (320)   :class:`bytearray` (40) 
    :attr:`data`              64:256 (1536) :class:`bytearray` (192)
    ========================= ============= ========================

.. class:: rdma.IBA.DMIOControllerProfile

    I/O Controller Profile Information (section 16.3.3.4)

    .. attribute:: MAD_LENGTH = 128
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('GUID',64,1), ('vendorID',24,1), ('reserved_88',8,1), ('deviceID',32,1), ('deviceVersion',16,1), ('reserved_144',16,1), ('subsystemVendorID',24,1), ('reserved_184',8,1), ('subsystemID',32,1), ('IOClass',16,1), ('IOSubclass',16,1), ('protocol',16,1), ('protocolVersion',16,1), ('reserved_288',16,1), ('reserved_304',16,1), ('sendMessageDepth',16,1), ('reserved_336',8,1), ('RDMAReadDepth',8,1), ('sendMessageSize',32,1), ('RDMATransferSize',32,1), ('controllerOperationsMask',8,1), ('reserved_424',8,1), ('serviceEntries',8,1), ('reserved_440',8,1), ('reserved_448',64,1), ('IDString',8,64)]

    ================================ ========== ============================
    Member                           Position   Type                        
    ================================ ========== ============================
    :attr:`GUID`                     0:8 (64)   :class:`~rdma.IBA.GUID`     
    :attr:`vendorID`                 8:11 (24)  :class:`int`                
    :attr:`reserved_88`              11:12 (8)  :class:`int`                
    :attr:`deviceID`                 12:16 (32) :class:`int`                
    :attr:`deviceVersion`            16:18 (16) :class:`int`                
    :attr:`reserved_144`             18:20 (16) :class:`int`                
    :attr:`subsystemVendorID`        20:23 (24) :class:`int`                
    :attr:`reserved_184`             23:24 (8)  :class:`int`                
    :attr:`subsystemID`              24:28 (32) :class:`int`                
    :attr:`IOClass`                  28:30 (16) :class:`int`                
    :attr:`IOSubclass`               30:32 (16) :class:`int`                
    :attr:`protocol`                 32:34 (16) :class:`int`                
    :attr:`protocolVersion`          34:36 (16) :class:`int`                
    :attr:`reserved_288`             36:38 (16) :class:`int`                
    :attr:`reserved_304`             38:40 (16) :class:`int`                
    :attr:`sendMessageDepth`         40:42 (16) :class:`int`                
    :attr:`reserved_336`             42:43 (8)  :class:`int`                
    :attr:`RDMAReadDepth`            43:44 (8)  :class:`int`                
    :attr:`sendMessageSize`          44:48 (32) :class:`int`                
    :attr:`RDMATransferSize`         48:52 (32) :class:`int`                
    :attr:`controllerOperationsMask` 52:53 (8)  :class:`int`                
    :attr:`reserved_424`             53:54 (8)  :class:`int`                
    :attr:`serviceEntries`           54:55 (8)  :class:`int`                
    :attr:`reserved_440`             55:56 (8)  :class:`int`                
    :attr:`reserved_448`             56:64 (64) :class:`int`                
    :attr:`IDString`                 64:128 (8) [:class:`bytearray` (64)]*64
    ================================ ========== ============================

.. class:: rdma.IBA.DMIOUnitInfo

    List of all I/O Controllers in a I/O Unit (section 16.3.3.3)

    .. attribute:: MAD_LENGTH = 132
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('changeID',16,1), ('maxControllers',8,1), ('reserved_24',6,1), ('diagDeviceID',1,1), ('optionROM',1,1), ('controllerList',1024,1)]

    ====================== ============= ========================
    Member                 Position      Type                    
    ====================== ============= ========================
    :attr:`changeID`       0:2 (16)      :class:`int`            
    :attr:`maxControllers` 2:3 (8)       :class:`int`            
    :attr:`reserved_24`    3:3[6] (6)    :class:`int`            
    :attr:`diagDeviceID`   3[6]:3[7] (1) :class:`int`            
    :attr:`optionROM`      3[7]:4 (1)    :class:`int`            
    :attr:`controllerList` 4:132 (1024)  :class:`bytearray` (128)
    ====================== ============= ========================

.. class:: rdma.IBA.DMPrepareToTest

    Prepare Device for Test (section 16.3.3.7)

    .. attribute:: MAD_LENGTH = 0
    .. attribute:: MAD_ATTRIBUTE_ID = 0x21
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = []

    ====== ======== ====
    Member Position Type
    ====== ======== ====
    ====== ======== ====

.. class:: rdma.IBA.DMServiceEntries

    List of Supported Services and Their Associated Service IDs (section 16.3.3.5)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MEMBERS = [('serviceEntry',384,4)]

    ==================== =========== =====================================
    Member               Position    Type                                 
    ==================== =========== =====================================
    :attr:`serviceEntry` 0:192 (384) [:class:`~rdma.IBA.DMServiceEntry`]*4
    ==================== =========== =====================================

.. class:: rdma.IBA.DMServiceEntry

    Service Entry (section 16.3.3)

    .. attribute:: MAD_LENGTH = 48
    .. attribute:: MEMBERS = [('serviceName',8,40), ('serviceID',64,1)]

    =================== ========== ============================
    Member              Position   Type                        
    =================== ========== ============================
    :attr:`serviceName` 0:40 (8)   [:class:`bytearray` (40)]*40
    :attr:`serviceID`   40:48 (64) :class:`int`                
    =================== ========== ============================

.. class:: rdma.IBA.DMTestDeviceLoop

    Test Device Continuously (section 16.3.3.9)

    .. attribute:: MAD_LENGTH = 0
    .. attribute:: MAD_ATTRIBUTE_ID = 0x23
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = []

    ====== ======== ====
    Member Position Type
    ====== ======== ====
    ====== ======== ====

.. class:: rdma.IBA.DMTestDeviceOnce

    Test Device Once (section 16.3.3.8)

    .. attribute:: MAD_LENGTH = 0
    .. attribute:: MAD_ATTRIBUTE_ID = 0x22
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MEMBERS = []

    ====== ======== ====
    Member Position Type
    ====== ======== ====
    ====== ======== ====

SNMP Tunneling (16.4)
^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.SNMPCommunityInfo

    Community Name Data Store (section 16.4.3.2)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('communityName',8,64)]

    ===================== ======== ============================
    Member                Position Type                        
    ===================== ======== ============================
    :attr:`communityName` 0:64 (8) [:class:`bytearray` (64)]*64
    ===================== ======== ============================

.. class:: rdma.IBA.SNMPFormat

    An *aggregation* of: MADHeader

    SNMP Tunneling MAD Format (section 16.4.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x8
    .. attribute:: MAD_CLASS_VERSION = 0x1
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('reserved_192',256,1), ('RAddress',32,1), ('payloadLength',8,1), ('segmentNumber',8,1), ('sourceLID',16,1), ('data',1536,1)]

    ========================= ============= ========================
    Member                    Position      Type                    
    ========================= ============= ========================
    :attr:`baseVersion`       0:1 (8)       :class:`int`            
    :attr:`mgmtClass`         1:2 (8)       :class:`int`            
    :attr:`classVersion`      2:3 (8)       :class:`int`            
    :attr:`method`            3:4 (8)       :class:`int`            
    :attr:`status`            4:6 (16)      :class:`int`            
    :attr:`classSpecific`     6:8 (16)      :class:`int`            
    :attr:`transactionID`     8:16 (64)     :class:`int`            
    :attr:`attributeID`       16:18 (16)    :class:`int`            
    :attr:`reserved_144`      18:20 (16)    :class:`int`            
    :attr:`attributeModifier` 20:24 (32)    :class:`int`            
    :attr:`reserved_192`      24:56 (256)   :class:`bytearray` (32) 
    :attr:`RAddress`          56:60 (32)    :class:`int`            
    :attr:`payloadLength`     60:61 (8)     :class:`int`            
    :attr:`segmentNumber`     61:62 (8)     :class:`int`            
    :attr:`sourceLID`         62:64 (16)    :class:`int`            
    :attr:`data`              64:256 (1536) :class:`bytearray` (192)
    ========================= ============= ========================

.. class:: rdma.IBA.SNMPPDUInfo

    Data Segment (section 16.4.3.3)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND
    .. attribute:: MEMBERS = [('PDUData',1536,1)]

    =============== ============ ========================
    Member          Position     Type                    
    =============== ============ ========================
    :attr:`PDUData` 0:192 (1536) :class:`bytearray` (192)
    =============== ============ ========================

Miscellaneous IBA Structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.CMFormat

    An *aggregation* of: MADHeader

    Request for Communication (section 16.7.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x7
    .. attribute:: MAD_CLASS_VERSION = 0x2
    .. attribute:: MEMBERS = [('baseVersion',8,1), ('mgmtClass',8,1), ('classVersion',8,1), ('method',8,1), ('status',16,1), ('classSpecific',16,1), ('transactionID',64,1), ('attributeID',16,1), ('reserved_144',16,1), ('attributeModifier',32,1), ('data',1856,1)]

    ========================= ============= ========================
    Member                    Position      Type                    
    ========================= ============= ========================
    :attr:`baseVersion`       0:1 (8)       :class:`int`            
    :attr:`mgmtClass`         1:2 (8)       :class:`int`            
    :attr:`classVersion`      2:3 (8)       :class:`int`            
    :attr:`method`            3:4 (8)       :class:`int`            
    :attr:`status`            4:6 (16)      :class:`int`            
    :attr:`classSpecific`     6:8 (16)      :class:`int`            
    :attr:`transactionID`     8:16 (64)     :class:`int`            
    :attr:`attributeID`       16:18 (16)    :class:`int`            
    :attr:`reserved_144`      18:20 (16)    :class:`int`            
    :attr:`attributeModifier` 20:24 (32)    :class:`int`            
    :attr:`data`              24:256 (1856) :class:`bytearray` (232)
    ========================= ============= ========================

.. class:: rdma.IBA.HdrAETH

    ACK Extended Transport Header (section 9.3.5)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('syndrome',8,1), ('MSN',24,1)]

    ================ ======== ============
    Member           Position Type        
    ================ ======== ============
    :attr:`syndrome` 0:1 (8)  :class:`int`
    :attr:`MSN`      1:4 (24) :class:`int`
    ================ ======== ============

.. class:: rdma.IBA.HdrAtomicAckETH

    Atomic Acknowledge Extended Transport Header (section 9.5.3)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MEMBERS = [('origRData',64,1)]

    ================= ======== ============
    Member            Position Type        
    ================= ======== ============
    :attr:`origRData` 0:8 (64) :class:`int`
    ================= ======== ============

.. class:: rdma.IBA.HdrAtomicETH

    Atomic Extended Transport Header (section 9.3.4)

    .. attribute:: MAD_LENGTH = 28
    .. attribute:: MEMBERS = [('VA',64,1), ('RKey',32,1), ('swapData',64,1), ('cmpData',64,1)]

    ================ ========== ============
    Member           Position   Type        
    ================ ========== ============
    :attr:`VA`       0:8 (64)   :class:`int`
    :attr:`RKey`     8:12 (32)  :class:`int`
    :attr:`swapData` 12:20 (64) :class:`int`
    :attr:`cmpData`  20:28 (64) :class:`int`
    ================ ========== ============

.. class:: rdma.IBA.HdrBTH

    Base Transport Header (section 9.2)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MEMBERS = [('service',3,1), ('function',5,1), ('SE',1,1), ('migReq',1,1), ('padCnt',2,1), ('TVer',4,1), ('PKey',16,1), ('reserved_32',8,1), ('destQP',24,1), ('ackReq',1,1), ('reserved_65',7,1), ('PSN',24,1)]

    =================== ============= ============
    Member              Position      Type        
    =================== ============= ============
    :attr:`service`     0:0[3] (3)    :class:`int`
    :attr:`function`    0[3]:1 (5)    :class:`int`
    :attr:`SE`          1:1[1] (1)    :class:`int`
    :attr:`migReq`      1[1]:1[2] (1) :class:`int`
    :attr:`padCnt`      1[2]:1[4] (2) :class:`int`
    :attr:`TVer`        1[4]:2 (4)    :class:`int`
    :attr:`PKey`        2:4 (16)      :class:`int`
    :attr:`reserved_32` 4:5 (8)       :class:`int`
    :attr:`destQP`      5:8 (24)      :class:`int`
    :attr:`ackReq`      8:8[1] (1)    :class:`int`
    :attr:`reserved_65` 8[1]:9 (7)    :class:`int`
    :attr:`PSN`         9:12 (24)     :class:`int`
    =================== ============= ============

.. class:: rdma.IBA.HdrDETH

    Datagram Extended Transport Header (section 9.3.2)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MEMBERS = [('QKey',32,1), ('reserved_32',8,1), ('srcQP',24,1)]

    =================== ======== ============
    Member              Position Type        
    =================== ======== ============
    :attr:`QKey`        0:4 (32) :class:`int`
    :attr:`reserved_32` 4:5 (8)  :class:`int`
    :attr:`srcQP`       5:8 (24) :class:`int`
    =================== ======== ============

.. class:: rdma.IBA.HdrFlowControl

    Flow Control Packet (section 7.9.4)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('op',4,1), ('FCTBS',12,1), ('VL',4,1), ('FCCL',12,1)]

    ============= =========== ============
    Member        Position    Type        
    ============= =========== ============
    :attr:`op`    0:0[4] (4)  :class:`int`
    :attr:`FCTBS` 0[4]:2 (12) :class:`int`
    :attr:`VL`    2:2[4] (4)  :class:`int`
    :attr:`FCCL`  2[4]:4 (12) :class:`int`
    ============= =========== ============

.. class:: rdma.IBA.HdrGRH

    Global Route Header (section 8.3)

    .. attribute:: MAD_LENGTH = 40
    .. attribute:: MEMBERS = [('IPVer',4,1), ('TClass',8,1), ('flowLabel',20,1), ('payLen',16,1), ('nxtHdr',8,1), ('hopLmt',8,1), ('SGID',128,1), ('DGID',128,1)]

    ================= ============= ======================
    Member            Position      Type                  
    ================= ============= ======================
    :attr:`IPVer`     0:0[4] (4)    :class:`int`          
    :attr:`TClass`    0[4]:1[4] (8) :class:`int`          
    :attr:`flowLabel` 1[4]:4 (20)   :class:`int`          
    :attr:`payLen`    4:6 (16)      :class:`int`          
    :attr:`nxtHdr`    6:7 (8)       :class:`int`          
    :attr:`hopLmt`    7:8 (8)       :class:`int`          
    :attr:`SGID`      8:24 (128)    :class:`~rdma.IBA.GID`
    :attr:`DGID`      24:40 (128)   :class:`~rdma.IBA.GID`
    ================= ============= ======================

.. class:: rdma.IBA.HdrIETH

    Invalidate Extended Transport Header (section 9.3.7)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('RKey',32,1)]

    ============ ======== ============
    Member       Position Type        
    ============ ======== ============
    :attr:`RKey` 0:4 (32) :class:`int`
    ============ ======== ============

.. class:: rdma.IBA.HdrImmDt

    Immediate Extended Transport Header (section 9.3.6)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('immediateData',32,1)]

    ===================== ======== ============
    Member                Position Type        
    ===================== ======== ============
    :attr:`immediateData` 0:4 (32) :class:`int`
    ===================== ======== ============

.. class:: rdma.IBA.HdrLRH

    Local Route Header (section 7.7)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MEMBERS = [('VL',4,1), ('LVer',4,1), ('SL',4,1), ('reserved_12',2,1), ('LNH',2,1), ('DLID',16,1), ('reserved_32',5,1), ('pktLen',11,1), ('SLID',16,1)]

    =================== ============= ============
    Member              Position      Type        
    =================== ============= ============
    :attr:`VL`          0:0[4] (4)    :class:`int`
    :attr:`LVer`        0[4]:1 (4)    :class:`int`
    :attr:`SL`          1:1[4] (4)    :class:`int`
    :attr:`reserved_12` 1[4]:1[6] (2) :class:`int`
    :attr:`LNH`         1[6]:2 (2)    :class:`int`
    :attr:`DLID`        2:4 (16)      :class:`int`
    :attr:`reserved_32` 4:4[5] (5)    :class:`int`
    :attr:`pktLen`      4[5]:6 (11)   :class:`int`
    :attr:`SLID`        6:8 (16)      :class:`int`
    =================== ============= ============

.. class:: rdma.IBA.HdrRDETH

    Reliable Datagram Extended Transport Header (section 9.3.1)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('reserved_0',8,1), ('EEC',24,1)]

    ================== ======== ============
    Member             Position Type        
    ================== ======== ============
    :attr:`reserved_0` 0:1 (8)  :class:`int`
    :attr:`EEC`        1:4 (24) :class:`int`
    ================== ======== ============

.. class:: rdma.IBA.HdrRETH

    RDMA Extended Transport Header (section 9.3.3)

    .. attribute:: MAD_LENGTH = 16
    .. attribute:: MEMBERS = [('VA',64,1), ('RKey',32,1), ('DMALen',32,1)]

    ============== ========== ============
    Member         Position   Type        
    ============== ========== ============
    :attr:`VA`     0:8 (64)   :class:`int`
    :attr:`RKey`   8:12 (32)  :class:`int`
    :attr:`DMALen` 12:16 (32) :class:`int`
    ============== ========== ============

.. class:: rdma.IBA.HdrRWH

    Raw Header (section 5.3)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MEMBERS = [('reserved_0',16,1), ('etherType',16,1)]

    ================== ======== ============
    Member             Position Type        
    ================== ======== ============
    :attr:`reserved_0` 0:2 (16) :class:`int`
    :attr:`etherType`  2:4 (16) :class:`int`
    ================== ======== ============

