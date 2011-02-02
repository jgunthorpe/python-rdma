Communication Management (12)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.CMAPR

    Alternate Path Response (section 12.8.2)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ============================ =============== ========================
    Member                       Position        Type                    
    ============================ =============== ========================
    :attr:`LCID`                 0:32 (32)       :class:`int`            
    :attr:`RCID`                 32:64 (32)      :class:`int`            
    :attr:`additionalInfoLength` 64:72 (8)       :class:`int`            
    :attr:`APstatus`             72:80 (8)       :class:`int`            
    :attr:`reserved1`            80:96 (16)      :class:`int`            
    :attr:`additionalInfo`       96:672 (576)    :class:`bytearray` (72) 
    :attr:`privateData`          672:1856 (1184) :class:`bytearray` (148)
    ============================ =============== ========================

.. class:: rdma.IBA.CMDREP

    Reply To Request For Communication Release (section 12.6.11)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    =================== ============== ========================
    Member              Position       Type                    
    =================== ============== ========================
    :attr:`LCID`        0:32 (32)      :class:`int`            
    :attr:`RCID`        32:64 (32)     :class:`int`            
    :attr:`privateData` 64:1856 (1792) :class:`bytearray` (224)
    =================== ============== ========================

.. class:: rdma.IBA.CMDREQ

    Request For Communication Release (Disconnection Request) (section 12.6.10)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    =================== ============== ========================
    Member              Position       Type                    
    =================== ============== ========================
    :attr:`LCID`        0:32 (32)      :class:`int`            
    :attr:`RCID`        32:64 (32)     :class:`int`            
    :attr:`remoteQPN`   64:88 (24)     :class:`int`            
    :attr:`reserved1`   88:96 (8)      :class:`int`            
    :attr:`privateData` 96:1856 (1760) :class:`bytearray` (220)
    =================== ============== ========================

.. class:: rdma.IBA.CMLAP

    Load Alternate Path (section 12.8.1)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ========================== =============== ========================
    Member                     Position        Type                    
    ========================== =============== ========================
    :attr:`LCID`               0:32 (32)       :class:`int`            
    :attr:`RCID`               32:64 (32)      :class:`int`            
    :attr:`QKey`               64:96 (32)      :class:`int`            
    :attr:`RQPN`               96:120 (24)     :class:`int`            
    :attr:`RCMTimeout`         120:125 (5)     :class:`int`            
    :attr:`reserved1`          55:58 (3)       :class:`int`            
    :attr:`reserved2`          128:160 (32)    :class:`int`            
    :attr:`altSLID`            160:176 (16)    :class:`int`            
    :attr:`altDLID`            176:192 (16)    :class:`int`            
    :attr:`altSGID`            192:320 (128)   :class:`~rdma.IBA.GID`  
    :attr:`altDGID`            320:448 (128)   :class:`~rdma.IBA.GID`  
    :attr:`altFlowLabel`       448:468 (20)    :class:`int`            
    :attr:`reserved3`          90:94 (4)       :class:`int`            
    :attr:`altTClass`          472:480 (8)     :class:`int`            
    :attr:`altHopLimit`        480:488 (8)     :class:`int`            
    :attr:`reserved4`          488:490 (2)     :class:`int`            
    :attr:`altIPD`             77:83 (6)       :class:`int`            
    :attr:`altSL`              496:500 (4)     :class:`int`            
    :attr:`altSubnetLocal`     94:95 (1)       :class:`int`            
    :attr:`reserved5`          102:105 (3)     :class:`int`            
    :attr:`altLocalACKTimeout` 504:509 (5)     :class:`int`            
    :attr:`reserved6`          103:106 (3)     :class:`int`            
    :attr:`privateData`        512:1856 (1344) :class:`bytearray` (168)
    ========================== =============== ========================

.. class:: rdma.IBA.CMMRA

    Message Receipt Acknowledgement (section 12.6.6)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ====================== ============== ========================
    Member                 Position       Type                    
    ====================== ============== ========================
    :attr:`LCID`           0:32 (32)      :class:`int`            
    :attr:`RCID`           32:64 (32)     :class:`int`            
    :attr:`messageMRAed`   64:66 (2)      :class:`int`            
    :attr:`reserved1`      24:30 (6)      :class:`int`            
    :attr:`serviceTimeout` 72:77 (5)      :class:`int`            
    :attr:`reserved2`      49:52 (3)      :class:`int`            
    :attr:`reserved3`      80:96 (16)     :class:`int`            
    :attr:`privateData`    96:1856 (1760) :class:`bytearray` (220)
    ====================== ============== ========================

.. class:: rdma.IBA.CMPath

    Path Information (section 12.6)

    .. attribute:: MAD_LENGTH = 44

    ======================= ============= ======================
    Member                  Position      Type                  
    ======================= ============= ======================
    :attr:`SLID`            0:16 (16)     :class:`int`          
    :attr:`DLID`            16:32 (16)    :class:`int`          
    :attr:`SGID`            32:160 (128)  :class:`~rdma.IBA.GID`
    :attr:`DGID`            160:288 (128) :class:`~rdma.IBA.GID`
    :attr:`flowLabel`       288:308 (20)  :class:`int`          
    :attr:`reserved1`       70:74 (4)     :class:`int`          
    :attr:`reserved2`       312:314 (2)   :class:`int`          
    :attr:`PD`              55:61 (6)     :class:`int`          
    :attr:`TClass`          320:328 (8)   :class:`int`          
    :attr:`hopLimit`        328:336 (8)   :class:`int`          
    :attr:`SL`              336:340 (4)   :class:`int`          
    :attr:`subnetLocal`     74:75 (1)     :class:`int`          
    :attr:`reserved3`       82:85 (3)     :class:`int`          
    :attr:`localACKTimeout` 344:349 (5)   :class:`int`          
    :attr:`reserved4`       83:86 (3)     :class:`int`          
    ======================= ============= ======================

.. class:: rdma.IBA.CMREJ

    Reject (section 12.6.7)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ======================== =============== ========================
    Member                   Position        Type                    
    ======================== =============== ========================
    :attr:`LCID`             0:32 (32)       :class:`int`            
    :attr:`RCID`             32:64 (32)      :class:`int`            
    :attr:`messageRejected`  64:66 (2)       :class:`int`            
    :attr:`reserved1`        24:30 (6)       :class:`int`            
    :attr:`rejectInfoLength` 72:79 (7)       :class:`int`            
    :attr:`reserved2`        65:66 (1)       :class:`int`            
    :attr:`reason`           80:96 (16)      :class:`int`            
    :attr:`ARI`              96:672 (576)    :class:`bytearray` (72) 
    :attr:`privateData`      672:1856 (1184) :class:`bytearray` (148)
    ======================== =============== ========================

.. class:: rdma.IBA.CMREP

    Reply To Request For Communication (section 12.6.8)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x13
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ========================== =============== ========================
    Member                     Position        Type                    
    ========================== =============== ========================
    :attr:`LCID`               0:32 (32)       :class:`int`            
    :attr:`RCID`               32:64 (32)      :class:`int`            
    :attr:`localQKey`          64:96 (32)      :class:`int`            
    :attr:`localQPN`           96:120 (24)     :class:`int`            
    :attr:`reserved1`          120:128 (8)     :class:`int`            
    :attr:`localEEContext`     128:152 (24)    :class:`int`            
    :attr:`reserved2`          152:160 (8)     :class:`int`            
    :attr:`startingPSN`        160:184 (24)    :class:`int`            
    :attr:`reserved3`          184:192 (8)     :class:`int`            
    :attr:`responderResources` 192:200 (8)     :class:`int`            
    :attr:`initiatorDepth`     200:208 (8)     :class:`int`            
    :attr:`targetACKDelay`     208:213 (5)     :class:`int`            
    :attr:`failoverAccepted`   66:68 (2)       :class:`int`            
    :attr:`flowControl`        82:83 (1)       :class:`int`            
    :attr:`RNRRetryCount`      216:219 (3)     :class:`int`            
    :attr:`reserved4`          51:56 (5)       :class:`int`            
    :attr:`LGUID`              224:288 (64)    :class:`~rdma.IBA.GUID` 
    :attr:`privateData`        288:1856 (1568) :class:`bytearray` (196)
    ========================== =============== ========================

.. class:: rdma.IBA.CMREQ

    Request for Communication (section 12.6.5)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ============================= =============== =========================
    Member                        Position        Type                     
    ============================= =============== =========================
    :attr:`LCID`                  0:32 (32)       :class:`int`             
    :attr:`reserved1`             32:64 (32)      :class:`int`             
    :attr:`serviceID`             64:128 (64)     :class:`int`             
    :attr:`LGUID`                 128:192 (64)    :class:`~rdma.IBA.GUID`  
    :attr:`localCMQKey`           192:224 (32)    :class:`int`             
    :attr:`localQKey`             224:256 (32)    :class:`int`             
    :attr:`localQPN`              256:280 (24)    :class:`int`             
    :attr:`responderResources`    280:288 (8)     :class:`int`             
    :attr:`localEECN`             288:312 (24)    :class:`int`             
    :attr:`initiatorDepth`        312:320 (8)     :class:`int`             
    :attr:`remoteEECN`            320:344 (24)    :class:`int`             
    :attr:`remoteResponseTimeout` 344:349 (5)     :class:`int`             
    :attr:`transportService`      83:85 (2)       :class:`int`             
    :attr:`flowControl`           99:100 (1)      :class:`int`             
    :attr:`startingPSN`           352:376 (24)    :class:`int`             
    :attr:`localResponseTimeout`  376:381 (5)     :class:`int`             
    :attr:`retryCount`            87:90 (3)       :class:`int`             
    :attr:`PKey`                  384:400 (16)    :class:`int`             
    :attr:`pathPacketMTU`         400:404 (4)     :class:`int`             
    :attr:`RDCExists`             82:83 (1)       :class:`int`             
    :attr:`RNRRetryCount`         90:93 (3)       :class:`int`             
    :attr:`maxCMRetries`          408:412 (4)     :class:`int`             
    :attr:`reserved2`             83:87 (4)       :class:`int`             
    :attr:`primaryPath`           416:768 (352)   :class:`~rdma.IBA.CMPath`
    :attr:`alternatePath`         768:1120 (352)  :class:`~rdma.IBA.CMPath`
    :attr:`privateData`           1120:1856 (736) :class:`bytearray` (92)  
    ============================= =============== =========================

.. class:: rdma.IBA.CMRTU

    Ready To Use (section 12.6.9)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    =================== ============== ========================
    Member              Position       Type                    
    =================== ============== ========================
    :attr:`LCID`        0:32 (32)      :class:`int`            
    :attr:`RCID`        32:64 (32)     :class:`int`            
    :attr:`privateData` 64:1856 (1792) :class:`bytearray` (224)
    =================== ============== ========================

.. class:: rdma.IBA.CMSIDR_REP

    Service ID Resolution Response (section 12.11.2)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    ===================== =============== ===================================
    Member                Position        Type                               
    ===================== =============== ===================================
    :attr:`requestID`     0:32 (32)       :class:`int`                       
    :attr:`QPN`           32:56 (24)      :class:`int`                       
    :attr:`status`        56:64 (8)       :class:`int`                       
    :attr:`serviceID`     64:128 (64)     :class:`int`                       
    :attr:`QKey`          128:160 (32)    :class:`int`                       
    :attr:`classPortinfo` 160:736 (576)   :class:`~rdma.IBA.MADClassPortInfo`
    :attr:`privateData`   736:1856 (1120) :class:`bytearray` (140)           
    ===================== =============== ===================================

.. class:: rdma.IBA.CMSIDR_REQ

    Service ID Resolution Request (section 12.11.1)

    .. attribute:: MAD_LENGTH = 232
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_COMMMGTSEND = 0x3 # MAD_METHOD_SEND

    =================== =============== ========================
    Member              Position        Type                    
    =================== =============== ========================
    :attr:`requestID`   0:32 (32)       :class:`int`            
    :attr:`reserved1`   32:64 (32)      :class:`int`            
    :attr:`serviceID`   64:128 (64)     :class:`int`            
    :attr:`privateData` 128:1856 (1728) :class:`bytearray` (216)
    =================== =============== ========================

Generic MAD (13.4)
^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.MADClassPortInfo

    Class Port Info (section 13.4.8.1)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1
    .. attribute:: MAD_COMMMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_COMMMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_BMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_BMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_SNMPGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET

    ====================== =============== ======================
    Member                 Position        Type                  
    ====================== =============== ======================
    :attr:`baseVersion`    0:8 (8)         :class:`int`          
    :attr:`classVersion`   64:72 (8)       :class:`int`          
    :attr:`capabilityMask` 128:144 (16)    :class:`int`          
    :attr:`reserved1`      256:283 (27)    :class:`int`          
    :attr:`respTimeValue`  472:477 (5)     :class:`int`          
    :attr:`redirectGID`    512:640 (128)   :class:`~rdma.IBA.GID`
    :attr:`redirectTC`     1536:1544 (8)   :class:`int`          
    :attr:`redirectSL`     1600:1604 (4)   :class:`int`          
    :attr:`redirectFL`     1632:1652 (20)  :class:`int`          
    :attr:`redirectLID`    1792:1808 (16)  :class:`int`          
    :attr:`redirectPKey`   1920:1936 (16)  :class:`int`          
    :attr:`reserved2`      2048:2056 (8)   :class:`int`          
    :attr:`redirectQP`     2112:2136 (24)  :class:`int`          
    :attr:`redirectQKey`   2304:2336 (32)  :class:`int`          
    :attr:`trapGID`        2560:2688 (128) :class:`~rdma.IBA.GID`
    :attr:`trapTC`         3584:3592 (8)   :class:`int`          
    :attr:`trapSL`         3648:3652 (4)   :class:`int`          
    :attr:`trapFL`         3680:3700 (20)  :class:`int`          
    :attr:`trapLID`        3840:3856 (16)  :class:`int`          
    :attr:`trapPKey`       3968:3984 (16)  :class:`int`          
    :attr:`trapHL`         4096:4104 (8)   :class:`int`          
    :attr:`trapQP`         4160:4184 (24)  :class:`int`          
    :attr:`trapQKey`       4352:4384 (32)  :class:`int`          
    ====================== =============== ======================

.. class:: rdma.IBA.MADHeader

    MAD Base Header (section 13.4.3)

    .. attribute:: MAD_LENGTH = 24

    ========================= ============== ============
    Member                    Position       Type        
    ========================= ============== ============
    :attr:`baseVersion`       0:8 (8)        :class:`int`
    :attr:`mgmtClass`         64:72 (8)      :class:`int`
    :attr:`classVersion`      128:136 (8)    :class:`int`
    :attr:`method`            192:200 (8)    :class:`int`
    :attr:`status`            256:272 (16)   :class:`int`
    :attr:`classSpecific`     384:400 (16)   :class:`int`
    :attr:`transactionID`     512:576 (64)   :class:`int`
    :attr:`attributeID`       1024:1040 (16) :class:`int`
    :attr:`reserved1`         1152:1168 (16) :class:`int`
    :attr:`attributeModifier` 1280:1312 (32) :class:`int`
    ========================= ============== ============

.. class:: rdma.IBA.MADHeaderDirected

    MAD Base Header Directed (section 13.4.3)

    .. attribute:: MAD_LENGTH = 24

    ========================= ============== ============
    Member                    Position       Type        
    ========================= ============== ============
    :attr:`baseVersion`       0:8 (8)        :class:`int`
    :attr:`mgmtClass`         64:72 (8)      :class:`int`
    :attr:`classVersion`      128:136 (8)    :class:`int`
    :attr:`method`            192:200 (8)    :class:`int`
    :attr:`D`                 256:257 (1)    :class:`int`
    :attr:`status`            264:279 (15)   :class:`int`
    :attr:`hopPointer`        384:392 (8)    :class:`int`
    :attr:`hopCount`          448:456 (8)    :class:`int`
    :attr:`transactionID`     512:576 (64)   :class:`int`
    :attr:`attributeID`       1024:1040 (16) :class:`int`
    :attr:`reserved1`         1152:1168 (16) :class:`int`
    :attr:`attributeModifier` 1280:1312 (32) :class:`int`
    ========================= ============== ============

.. class:: rdma.IBA.MADInformInfo

    InformInfo (section 13.4.8.3)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET

    ===================== ============== ======================
    Member                Position       Type                  
    ===================== ============== ======================
    :attr:`GID`           0:128 (128)    :class:`~rdma.IBA.GID`
    :attr:`LIDRangeBegin` 1024:1040 (16) :class:`int`          
    :attr:`LIDRangeEnd`   1152:1168 (16) :class:`int`          
    :attr:`reserved1`     1280:1296 (16) :class:`int`          
    :attr:`isGeneric`     1408:1416 (8)  :class:`int`          
    :attr:`subscribe`     1472:1480 (8)  :class:`int`          
    :attr:`type`          1536:1552 (16) :class:`int`          
    :attr:`trapNumber`    1664:1680 (16) :class:`int`          
    :attr:`QPN`           1792:1816 (24) :class:`int`          
    :attr:`reserved2`     1984:1987 (3)  :class:`int`          
    :attr:`respTimeValue` 2008:2013 (5)  :class:`int`          
    :attr:`reserved3`     2048:2056 (8)  :class:`int`          
    :attr:`producerType`  2112:2136 (24) :class:`int`          
    ===================== ============== ======================

RMPP (13.6)
^^^^^^^^^^^

.. class:: rdma.IBA.RMPPAbort

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256

    ================== =============== ==================================
    Member             Position        Type                              
    ================== =============== ==================================
    :attr:`RMPPHeader` 0:224 (224)     :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`reserved1`  224:256 (32)    :class:`int`                      
    :attr:`reserved2`  256:288 (32)    :class:`int`                      
    :attr:`errorData`  288:2048 (1760) :class:`bytearray` (220)          
    ================== =============== ==================================

.. class:: rdma.IBA.RMPPAck

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256

    ===================== =============== ==================================
    Member                Position        Type                              
    ===================== =============== ==================================
    :attr:`RMPPHeader`    0:224 (224)     :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`segmentNumber` 224:256 (32)    :class:`int`                      
    :attr:`newWindowLast` 256:288 (32)    :class:`int`                      
    :attr:`reserved1`     288:2048 (1760) :class:`bytearray` (220)          
    ===================== =============== ==================================

.. class:: rdma.IBA.RMPPData

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256

    ===================== =============== ==================================
    Member                Position        Type                              
    ===================== =============== ==================================
    :attr:`RMPPHeader`    0:224 (224)     :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`segmentNumber` 224:256 (32)    :class:`int`                      
    :attr:`payLoadLength` 256:288 (32)    :class:`int`                      
    :attr:`data`          288:2048 (1760) :class:`bytearray` (220)          
    ===================== =============== ==================================

.. class:: rdma.IBA.RMPPHeader

    RMPP Header Fields (section 13.6.2.1)

    .. attribute:: MAD_LENGTH = 36

    =================== ============ ============================
    Member              Position     Type                        
    =================== ============ ============================
    :attr:`MADHeader`   0:192 (192)  :class:`~rdma.IBA.MADHeader`
    :attr:`RMPPVersion` 192:200 (8)  :class:`int`                
    :attr:`RMPPType`    200:208 (8)  :class:`int`                
    :attr:`RRespTime`   208:213 (5)  :class:`int`                
    :attr:`RMPPFlags`   66:69 (3)    :class:`int`                
    :attr:`RMPPStatus`  216:224 (8)  :class:`int`                
    :attr:`data1`       224:256 (32) :class:`int`                
    :attr:`data2`       256:288 (32) :class:`int`                
    =================== ============ ============================

.. class:: rdma.IBA.RMPPShortHeader

    RMPP Header Fields (section 13.6.2.1)

    .. attribute:: MAD_LENGTH = 28

    =================== =========== ============================
    Member              Position    Type                        
    =================== =========== ============================
    :attr:`MADHeader`   0:192 (192) :class:`~rdma.IBA.MADHeader`
    :attr:`RMPPVersion` 192:200 (8) :class:`int`                
    :attr:`RMPPType`    200:208 (8) :class:`int`                
    :attr:`RRespTime`   208:213 (5) :class:`int`                
    :attr:`RMPPFlags`   66:69 (3)   :class:`int`                
    :attr:`RMPPStatus`  216:224 (8) :class:`int`                
    =================== =========== ============================

.. class:: rdma.IBA.RMPPStop

    RMPP Data Packet (section 13.6.2.3)

    .. attribute:: MAD_LENGTH = 256

    ================== =============== ==================================
    Member             Position        Type                              
    ================== =============== ==================================
    :attr:`RMPPHeader` 0:224 (224)     :class:`~rdma.IBA.RMPPShortHeader`
    :attr:`reserved1`  224:256 (32)    :class:`int`                      
    :attr:`reserved2`  256:288 (32)    :class:`int`                      
    :attr:`errorData`  288:2048 (1760) :class:`bytearray` (220)          
    ================== =============== ==================================

Subnet Management (14)
^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.SMPFormat

    SMP Format - LID Routed (section 14.2.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x1
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ================= ================ ============================
    Member            Position         Type                        
    ================= ================ ============================
    :attr:`MADHeader` 0:192 (192)      :class:`~rdma.IBA.MADHeader`
    :attr:`MKey`      192:256 (64)     :class:`int`                
    :attr:`reserved1` 256:512 (256)    :class:`bytearray` (32)     
    :attr:`data`      512:1024 (512)   :class:`bytearray` (64)     
    :attr:`reserved2` 1024:2048 (1024) :class:`bytearray` (128)    
    ================= ================ ============================

.. class:: rdma.IBA.SMPFormatDirected

    SMP Format - Direct Routed (section 14.2.1.2)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x81
    .. attribute:: MAD_CLASS_VERSION = 0x1

    =================== ============== ====================================
    Member              Position       Type                                
    =================== ============== ====================================
    :attr:`MADHeader`   0:192 (192)    :class:`~rdma.IBA.MADHeaderDirected`
    :attr:`MKey`        192:256 (64)   :class:`int`                        
    :attr:`drSLID`      256:272 (16)   :class:`int`                        
    :attr:`drDLID`      272:288 (16)   :class:`int`                        
    :attr:`reserved1`   288:512 (224)  :class:`bytearray` (28)             
    :attr:`data`        512:1024 (512) :class:`bytearray` (64)             
    :attr:`initialPath` 1024:1536 (8)  [:class:`bytearray` (64)]*64        
    :attr:`returnPath`  1536:2048 (8)  [:class:`bytearray` (64)]*64        
    =================== ============== ====================================

.. class:: rdma.IBA.SMPGUIDInfo

    Assigned GUIDs (section 14.2.5.5)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ================= ========== ===========================
    Member            Position   Type                       
    ================= ========== ===========================
    :attr:`GUIDBlock` 0:512 (64) [:class:`~rdma.IBA.GUID`]*8
    ================= ========== ===========================

.. class:: rdma.IBA.SMPLIDPortBlock

    LID/Port Block Element (section 14.2.5.11)

    .. attribute:: MAD_LENGTH = 4

    ================= =========== ============
    Member            Position    Type        
    ================= =========== ============
    :attr:`LID`       0:16 (16)   :class:`int`
    :attr:`valid`     128:129 (1) :class:`int`
    :attr:`LMC`       136:139 (3) :class:`int`
    :attr:`reserved1` 160:164 (4) :class:`int`
    :attr:`port`      192:200 (8) :class:`int`
    ================= =========== ============

.. class:: rdma.IBA.SMPLedInfo

    Turn on/off LED (section 14.2.5.15)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x31
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ================= ========= ============
    Member            Position  Type        
    ================= ========= ============
    :attr:`ledMask`   0:1 (1)   :class:`int`
    :attr:`reserved1` 8:39 (31) :class:`int`
    ================= ========= ============

.. class:: rdma.IBA.SMPLinearForwardingTable

    Linear Forwarding Table Information (section 14.2.5.10)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ================= ========= ============================
    Member            Position  Type                        
    ================= ========= ============================
    :attr:`portBlock` 0:512 (8) [:class:`bytearray` (64)]*64
    ================= ========= ============================

.. class:: rdma.IBA.SMPMulticastForwardingTable

    Multicast Forwarding Table Information (section 14.2.5.12)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1b
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ===================== ========== =================
    Member                Position   Type             
    ===================== ========== =================
    :attr:`portMaskBlock` 0:512 (16) [:class:`int`]*32
    ===================== ========== =================

.. class:: rdma.IBA.SMPNodeDescription

    Node Description String (section 14.2.5.2)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET

    ================== ========= ============================
    Member             Position  Type                        
    ================== ========= ============================
    :attr:`nodeString` 0:512 (8) [:class:`bytearray` (64)]*64
    ================== ========= ============================

.. class:: rdma.IBA.SMPNodeInfo

    Generic Node Data (section 14.2.5.3)

    .. attribute:: MAD_LENGTH = 40
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET

    ======================= ============== =======================
    Member                  Position       Type                   
    ======================= ============== =======================
    :attr:`baseVersion`     0:8 (8)        :class:`int`           
    :attr:`classVersion`    64:72 (8)      :class:`int`           
    :attr:`nodeType`        128:136 (8)    :class:`int`           
    :attr:`numPorts`        192:200 (8)    :class:`int`           
    :attr:`systemImageGUID` 256:320 (64)   :class:`~rdma.IBA.GUID`
    :attr:`nodeGUID`        768:832 (64)   :class:`~rdma.IBA.GUID`
    :attr:`portGUID`        1280:1344 (64) :class:`~rdma.IBA.GUID`
    :attr:`partitionCap`    1792:1808 (16) :class:`int`           
    :attr:`deviceID`        1920:1936 (16) :class:`int`           
    :attr:`revision`        2048:2080 (32) :class:`int`           
    :attr:`localPortNum`    2304:2312 (8)  :class:`int`           
    :attr:`vendorID`        2368:2392 (24) :class:`int`           
    ======================= ============== =======================

.. class:: rdma.IBA.SMPPKeyTable

    Partition Table (section 14.2.5.7)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ================= ========== =================
    Member            Position   Type             
    ================= ========== =================
    :attr:`PKeyBlock` 0:512 (16) [:class:`int`]*32
    ================= ========== =================

.. class:: rdma.IBA.SMPPortInfo

    Port Information (section 14.2.5.6)

    .. attribute:: MAD_LENGTH = 56
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ==================================== ============== ============
    Member                               Position       Type        
    ==================================== ============== ============
    :attr:`MKey`                         0:64 (64)      :class:`int`
    :attr:`GIDPrefix`                    512:576 (64)   :class:`int`
    :attr:`LID`                          1024:1040 (16) :class:`int`
    :attr:`masterSMLID`                  1152:1168 (16) :class:`int`
    :attr:`capabilityMask`               1280:1312 (32) :class:`int`
    :attr:`diagCode`                     1536:1552 (16) :class:`int`
    :attr:`MKeyLeasePeriod`              1664:1680 (16) :class:`int`
    :attr:`localPortNum`                 1792:1800 (8)  :class:`int`
    :attr:`linkWidthEnabled`             1856:1864 (8)  :class:`int`
    :attr:`linkWidthSupported`           1920:1928 (8)  :class:`int`
    :attr:`linkWidthActive`              1984:1992 (8)  :class:`int`
    :attr:`linkSpeedSupported`           2048:2052 (4)  :class:`int`
    :attr:`portState`                    2080:2084 (4)  :class:`int`
    :attr:`portPhysicalState`            2112:2116 (4)  :class:`int`
    :attr:`linkDownDefaultState`         2144:2148 (4)  :class:`int`
    :attr:`MKeyProtectBits`              2176:2178 (2)  :class:`int`
    :attr:`reserved1`                    2192:2195 (3)  :class:`int`
    :attr:`LMC`                          2216:2219 (3)  :class:`int`
    :attr:`linkSpeedActive`              2240:2244 (4)  :class:`int`
    :attr:`linkSpeedEnabled`             2272:2276 (4)  :class:`int`
    :attr:`neighborMTU`                  2304:2308 (4)  :class:`int`
    :attr:`masterSMSL`                   2336:2340 (4)  :class:`int`
    :attr:`VLCap`                        2368:2372 (4)  :class:`int`
    :attr:`initType`                     2400:2404 (4)  :class:`int`
    :attr:`VLHighLimit`                  2432:2440 (8)  :class:`int`
    :attr:`VLArbitrationHighCap`         2496:2504 (8)  :class:`int`
    :attr:`VLArbitrationLowCap`          2560:2568 (8)  :class:`int`
    :attr:`initTypeReply`                2624:2628 (4)  :class:`int`
    :attr:`MTUCap`                       2656:2660 (4)  :class:`int`
    :attr:`VLStallCount`                 2688:2691 (3)  :class:`int`
    :attr:`HOQLife`                      2712:2717 (5)  :class:`int`
    :attr:`operationalVLs`               2752:2756 (4)  :class:`int`
    :attr:`partitionEnforcementInbound`  2784:2785 (1)  :class:`int`
    :attr:`partitionEnforcementOutbound` 2792:2793 (1)  :class:`int`
    :attr:`filterRawInbound`             2800:2801 (1)  :class:`int`
    :attr:`filterRawOutbound`            2808:2809 (1)  :class:`int`
    :attr:`MKeyViolations`               2816:2832 (16) :class:`int`
    :attr:`PKeyViolations`               2944:2960 (16) :class:`int`
    :attr:`QKeyViolations`               3072:3088 (16) :class:`int`
    :attr:`GUIDCap`                      3200:3208 (8)  :class:`int`
    :attr:`clientReregister`             3264:3265 (1)  :class:`int`
    :attr:`reserved2`                    3272:3274 (2)  :class:`int`
    :attr:`subnetTimeOut`                3288:3293 (5)  :class:`int`
    :attr:`reserved3`                    3328:3331 (3)  :class:`int`
    :attr:`respTimeValue`                3352:3357 (5)  :class:`int`
    :attr:`localPhyErrors`               3392:3396 (4)  :class:`int`
    :attr:`overrunErrors`                3424:3428 (4)  :class:`int`
    :attr:`reserved4`                    3456:3472 (16) :class:`int`
    ==================================== ============== ============

.. class:: rdma.IBA.SMPRandomForwardingTable

    Random Forwarding Table Information (section 14.2.5.11)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ==================== ========== =======================================
    Member               Position   Type                                   
    ==================== ========== =======================================
    :attr:`LIDPortBlock` 0:512 (32) [:class:`~rdma.IBA.SMPLIDPortBlock`]*16
    ==================== ========== =======================================

.. class:: rdma.IBA.SMPSLToVLMappingTable

    Service Level to Virtual Lane mapping Information (section 14.2.5.8)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ============== ======== ============================
    Member         Position Type                        
    ============== ======== ============================
    :attr:`SLtoVL` 0:64 (4) [:class:`bytearray` (16)]*16
    ============== ======== ============================

.. class:: rdma.IBA.SMPSMInfo

    Subnet Management Information (section 14.2.5.13)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ================= ============== =======================
    Member            Position       Type                   
    ================= ============== =======================
    :attr:`GUID`      0:64 (64)      :class:`~rdma.IBA.GUID`
    :attr:`SMKey`     512:576 (64)   :class:`int`           
    :attr:`actCount`  1024:1056 (32) :class:`int`           
    :attr:`priority`  1280:1284 (4)  :class:`int`           
    :attr:`SMState`   1312:1316 (4)  :class:`int`           
    :attr:`reserved1` 1344:1368 (24) :class:`int`           
    ================= ============== =======================

.. class:: rdma.IBA.SMPSwitchInfo

    Switch Information (section 14.2.5.4)

    .. attribute:: MAD_LENGTH = 20
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ========================================= ============== ============
    Member                                    Position       Type        
    ========================================= ============== ============
    :attr:`linearFDBCap`                      0:16 (16)      :class:`int`
    :attr:`randomFDBCap`                      128:144 (16)   :class:`int`
    :attr:`multicastFDBCap`                   256:272 (16)   :class:`int`
    :attr:`linearFDBTop`                      384:400 (16)   :class:`int`
    :attr:`defaultPort`                       512:520 (8)    :class:`int`
    :attr:`defaultMulticastPrimaryPort`       576:584 (8)    :class:`int`
    :attr:`defaultMulticastNotPrimaryPort`    640:648 (8)    :class:`int`
    :attr:`lifeTimeValue`                     704:709 (5)    :class:`int`
    :attr:`portStateChange`                   744:745 (1)    :class:`int`
    :attr:`reserved1`                         752:753 (1)    :class:`int`
    :attr:`optimizedSLtoVLMappingProgramming` 760:761 (1)    :class:`int`
    :attr:`LIDsPerPort`                       768:784 (16)   :class:`int`
    :attr:`partitionEnforcementCap`           896:912 (16)   :class:`int`
    :attr:`inboundEnforcementCap`             1024:1025 (1)  :class:`int`
    :attr:`outboundEnforcementCap`            1032:1033 (1)  :class:`int`
    :attr:`filterRawInboundCap`               1040:1041 (1)  :class:`int`
    :attr:`filterRawOutboundCap`              1048:1049 (1)  :class:`int`
    :attr:`enhancedPort0`                     1056:1057 (1)  :class:`int`
    :attr:`reserved2`                         1064:1067 (3)  :class:`int`
    :attr:`reserved3`                         1088:1112 (24) :class:`int`
    ========================================= ============== ============

.. class:: rdma.IBA.SMPVLArbitrationTable

    List of Weights (section 14.2.5.9)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ===================== ========== =================
    Member                Position   Type             
    ===================== ========== =================
    :attr:`VLWeightBlock` 0:512 (16) [:class:`int`]*32
    ===================== ========== =================

.. class:: rdma.IBA.SMPVendorDiag

    Vendor Specific Diagnostic (section 14.2.5.14)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET

    ================= ============= =======================
    Member            Position      Type                   
    ================= ============= =======================
    :attr:`nextIndex` 0:16 (16)     :class:`int`           
    :attr:`reserved1` 128:144 (16)  :class:`int`           
    :attr:`diagData`  256:736 (480) :class:`bytearray` (60)
    ================= ============= =======================

Subnet Administration (15)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.SAFormat

    SA Format (section 15.2.1.1)

    .. attribute:: MAD_LENGTH = 256

    ================ =============== ===========================
    Member           Position        Type                       
    ================ =============== ===========================
    :attr:`SAHeader` 0:448 (448)     :class:`~rdma.IBA.SAHeader`
    :attr:`data`     448:2048 (1600) :class:`bytearray` (200)   
    ================ =============== ===========================

.. class:: rdma.IBA.SAGUIDInfoRecord

    Container for port GUIDInfo (section 15.2.5.18)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================= ============== ==============================
    Member            Position       Type                          
    ================= ============== ==============================
    :attr:`LID`       0:16 (16)      :class:`int`                  
    :attr:`blockNum`  128:136 (8)    :class:`int`                  
    :attr:`reserved1` 192:200 (8)    :class:`int`                  
    :attr:`reserved2` 256:288 (32)   :class:`int`                  
    :attr:`GUIDInfo`  512:1024 (512) :class:`~rdma.IBA.SMPGUIDInfo`
    ================= ============== ==============================

.. class:: rdma.IBA.SAHeader

    SA Header (section 15.2.1.1)

    .. attribute:: MAD_LENGTH = 56
    .. attribute:: MAD_CLASS = 0x3
    .. attribute:: MAD_CLASS_VERSION = 0x2

    ======================= ============ =============================
    Member                  Position     Type                         
    ======================= ============ =============================
    :attr:`RMPPHeader`      0:288 (288)  :class:`~rdma.IBA.RMPPHeader`
    :attr:`SMKey`           288:352 (64) :class:`int`                 
    :attr:`attributeOffset` 352:368 (16) :class:`int`                 
    :attr:`reserved1`       368:384 (16) :class:`int`                 
    :attr:`componentMask`   384:448 (64) :class:`int`                 
    ======================= ============ =============================

.. class:: rdma.IBA.SAInformInfoRecord

    Container for InformInfo (section 15.2.5.12)

    .. attribute:: MAD_LENGTH = 80
    .. attribute:: MAD_ATTRIBUTE_ID = 0xf3
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ===================== =============== ================================
    Member                Position        Type                            
    ===================== =============== ================================
    :attr:`subscriberGID` 0:128 (128)     :class:`~rdma.IBA.GID`          
    :attr:`enumeration`   1024:1040 (16)  :class:`int`                    
    :attr:`reserved1`     1152:1168 (16)  :class:`int`                    
    :attr:`reserved2`     1280:1312 (32)  :class:`int`                    
    :attr:`informInfo`    1536:1824 (288) :class:`~rdma.IBA.MADInformInfo`
    :attr:`reserved3`     3840:4000 (160) :class:`bytearray` (20)         
    ===================== =============== ================================

.. class:: rdma.IBA.SALinearForwardingTableRecord

    Container for LinearForwardingTable entry (section 15.2.5.6)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ============================= ============== ===========================================
    Member                        Position       Type                                       
    ============================= ============== ===========================================
    :attr:`LID`                   0:16 (16)      :class:`int`                               
    :attr:`blockNum`              128:144 (16)   :class:`int`                               
    :attr:`reserved1`             256:288 (32)   :class:`int`                               
    :attr:`linearForwardingTable` 512:1024 (512) :class:`~rdma.IBA.SMPLinearForwardingTable`
    ============================= ============== ===========================================

.. class:: rdma.IBA.SALinkRecord

    Inter-node linkage information (section 15.2.5.13)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================= ============ ============
    Member            Position     Type        
    ================= ============ ============
    :attr:`fromLID`   0:16 (16)    :class:`int`
    :attr:`fromPort`  128:136 (8)  :class:`int`
    :attr:`toPort`    192:200 (8)  :class:`int`
    :attr:`toLID`     256:272 (16) :class:`int`
    :attr:`reserved1` 384:400 (16) :class:`int`
    ================= ============ ============

.. class:: rdma.IBA.SAMCMemberRecord

    Multicast member attribute (section 15.2.5.17)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x38
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE

    ============================== =============== ======================
    Member                         Position        Type                  
    ============================== =============== ======================
    :attr:`MGID`                   0:128 (128)     :class:`~rdma.IBA.GID`
    :attr:`portGID`                1024:1152 (128) :class:`~rdma.IBA.GID`
    :attr:`requesterGID`           2048:2176 (128) :class:`~rdma.IBA.GID`
    :attr:`QKey`                   3072:3104 (32)  :class:`int`          
    :attr:`MLID`                   3328:3344 (16)  :class:`int`          
    :attr:`MTUSelector`            3456:3458 (2)   :class:`int`          
    :attr:`MTU`                    3472:3478 (6)   :class:`int`          
    :attr:`TClass`                 3520:3528 (8)   :class:`int`          
    :attr:`PKey`                   3584:3600 (16)  :class:`int`          
    :attr:`rateSelector`           3712:3714 (2)   :class:`int`          
    :attr:`rate`                   3728:3734 (6)   :class:`int`          
    :attr:`packetLifeTimeSelector` 3776:3778 (2)   :class:`int`          
    :attr:`packetLifeTime`         3792:3798 (6)   :class:`int`          
    :attr:`SL`                     3840:3844 (4)   :class:`int`          
    :attr:`flowLabel`              3872:3892 (20)  :class:`int`          
    :attr:`hopLimit`               4032:4040 (8)   :class:`int`          
    :attr:`scope`                  4096:4100 (4)   :class:`int`          
    :attr:`joinState`              4128:4132 (4)   :class:`int`          
    :attr:`reserved1`              4160:4184 (24)  :class:`int`          
    ============================== =============== ======================

.. class:: rdma.IBA.SAMultiPathRecord

    Request for multiple paths (section 15.2.5.20)

    .. attribute:: MAD_LENGTH = 40
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3a
    .. attribute:: MAD_SUBNADMGETMULTI = 0x14 # MAD_METHOD_GET_MULTI

    ============================== =============== ======================
    Member                         Position        Type                  
    ============================== =============== ======================
    :attr:`rawTraffic`             0:1 (1)         :class:`int`          
    :attr:`reserved1`              8:11 (3)        :class:`int`          
    :attr:`flowLabel`              32:52 (20)      :class:`int`          
    :attr:`hopLimit`               192:200 (8)     :class:`int`          
    :attr:`TClass`                 256:264 (8)     :class:`int`          
    :attr:`reversible`             320:321 (1)     :class:`int`          
    :attr:`numbPath`               328:335 (7)     :class:`int`          
    :attr:`PKey`                   384:400 (16)    :class:`int`          
    :attr:`reserved2`              512:524 (12)    :class:`int`          
    :attr:`SL`                     608:612 (4)     :class:`int`          
    :attr:`MTUSelector`            640:642 (2)     :class:`int`          
    :attr:`MTU`                    656:662 (6)     :class:`int`          
    :attr:`rateSelector`           704:706 (2)     :class:`int`          
    :attr:`rate`                   720:726 (6)     :class:`int`          
    :attr:`packetLifeTimeSelector` 768:770 (2)     :class:`int`          
    :attr:`packetLifeTime`         784:790 (6)     :class:`int`          
    :attr:`reserved3`              832:840 (8)     :class:`int`          
    :attr:`independenceSelector`   896:898 (2)     :class:`int`          
    :attr:`reserved4`              912:918 (6)     :class:`int`          
    :attr:`SGIDCount`              960:968 (8)     :class:`int`          
    :attr:`DGIDCount`              1024:1032 (8)   :class:`int`          
    :attr:`reserved5`              1088:1112 (24)  :class:`int`          
    :attr:`reserved6`              1280:1312 (32)  :class:`int`          
    :attr:`SDGID`                  1536:1664 (128) :class:`~rdma.IBA.GID`
    ============================== =============== ======================

.. class:: rdma.IBA.SAMulticastForwardingTableRecord

    Container for MulticastForwardingTable entry (section 15.2.5.8)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================================ ============== ==============================================
    Member                           Position       Type                                          
    ================================ ============== ==============================================
    :attr:`LID`                      0:16 (16)      :class:`int`                                  
    :attr:`reserved1`                128:130 (2)    :class:`int`                                  
    :attr:`position`                 144:148 (4)    :class:`int`                                  
    :attr:`blockNum`                 176:186 (10)   :class:`int`                                  
    :attr:`reserved2`                256:288 (32)   :class:`int`                                  
    :attr:`multicastForwardingTable` 512:1024 (512) :class:`~rdma.IBA.SMPMulticastForwardingTable`
    ================================ ============== ==============================================

.. class:: rdma.IBA.SANodeRecord

    Container for NodeInfo (section 15.2.5.2)

    .. attribute:: MAD_LENGTH = 108
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ======================= =============== =====================================
    Member                  Position        Type                                 
    ======================= =============== =====================================
    :attr:`LID`             0:16 (16)       :class:`int`                         
    :attr:`reserved1`       128:144 (16)    :class:`int`                         
    :attr:`nodeInfo`        256:576 (320)   :class:`~rdma.IBA.SMPNodeInfo`       
    :attr:`nodeDescription` 2816:3328 (512) :class:`~rdma.IBA.SMPNodeDescription`
    ======================= =============== =====================================

.. class:: rdma.IBA.SAPKeyTableRecord

    Container for P_Key Table (section 15.2.5.11)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x33
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================= ============== ===============================
    Member            Position       Type                           
    ================= ============== ===============================
    :attr:`LID`       0:16 (16)      :class:`int`                   
    :attr:`blockNum`  128:144 (16)   :class:`int`                   
    :attr:`portNum`   256:264 (8)    :class:`int`                   
    :attr:`reserved1` 320:344 (24)   :class:`int`                   
    :attr:`PKeyTable` 512:1024 (512) :class:`~rdma.IBA.SMPPKeyTable`
    ================= ============== ===============================

.. class:: rdma.IBA.SAPathRecord

    Information on paths through the subnet (section 15.2.5.16)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x35
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ============================== =============== ======================
    Member                         Position        Type                  
    ============================== =============== ======================
    :attr:`reserved1`              0:32 (32)       :class:`int`          
    :attr:`reserved2`              256:288 (32)    :class:`int`          
    :attr:`DGID`                   512:640 (128)   :class:`~rdma.IBA.GID`
    :attr:`SGID`                   1536:1664 (128) :class:`~rdma.IBA.GID`
    :attr:`DLID`                   2560:2576 (16)  :class:`int`          
    :attr:`SLID`                   2688:2704 (16)  :class:`int`          
    :attr:`rawTraffic`             2816:2817 (1)   :class:`int`          
    :attr:`reserved3`              2824:2827 (3)   :class:`int`          
    :attr:`flowLabel`              2848:2868 (20)  :class:`int`          
    :attr:`hopLimit`               3008:3016 (8)   :class:`int`          
    :attr:`TClass`                 3072:3080 (8)   :class:`int`          
    :attr:`reversible`             3136:3137 (1)   :class:`int`          
    :attr:`numbPath`               3144:3151 (7)   :class:`int`          
    :attr:`PKey`                   3200:3216 (16)  :class:`int`          
    :attr:`reserved4`              3328:3340 (12)  :class:`int`          
    :attr:`SL`                     3424:3428 (4)   :class:`int`          
    :attr:`MTUSelector`            3456:3458 (2)   :class:`int`          
    :attr:`MTU`                    3472:3478 (6)   :class:`int`          
    :attr:`rateSelector`           3520:3522 (2)   :class:`int`          
    :attr:`rate`                   3536:3542 (6)   :class:`int`          
    :attr:`packetLifeTimeSelector` 3584:3586 (2)   :class:`int`          
    :attr:`packetLifeTime`         3600:3606 (6)   :class:`int`          
    :attr:`preference`             3648:3656 (8)   :class:`int`          
    :attr:`reserved5`              3712:3728 (16)  :class:`int`          
    :attr:`reserved6`              3840:3872 (32)  :class:`int`          
    ============================== =============== ======================

.. class:: rdma.IBA.SAPortInfoRecord

    Container for PortInfo (section 15.2.5.3)

    .. attribute:: MAD_LENGTH = 60
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================== ============= ==============================
    Member             Position      Type                          
    ================== ============= ==============================
    :attr:`endportLID` 0:16 (16)     :class:`int`                  
    :attr:`portNum`    128:136 (8)   :class:`int`                  
    :attr:`reserved1`  192:200 (8)   :class:`int`                  
    :attr:`portInfo`   256:704 (448) :class:`~rdma.IBA.SMPPortInfo`
    ================== ============= ==============================

.. class:: rdma.IBA.SARandomForwardingTableRecord

    Container for RandomForwardingTable entry (section 15.2.5.7)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ============================= ============== ===========================================
    Member                        Position       Type                                       
    ============================= ============== ===========================================
    :attr:`LID`                   0:16 (16)      :class:`int`                               
    :attr:`blockNum`              128:144 (16)   :class:`int`                               
    :attr:`reserved1`             256:288 (32)   :class:`int`                               
    :attr:`randomForwardingTable` 512:1024 (512) :class:`~rdma.IBA.SMPRandomForwardingTable`
    ============================= ============== ===========================================

.. class:: rdma.IBA.SASLToVLMappingTableRecord

    Container for SLtoVLMappingTable entry (section 15.2.5.4)

    .. attribute:: MAD_LENGTH = 16
    .. attribute:: MAD_ATTRIBUTE_ID = 0x13
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ========================== ============ ========================================
    Member                     Position     Type                                    
    ========================== ============ ========================================
    :attr:`LID`                0:16 (16)    :class:`int`                            
    :attr:`inputPortNum`       128:136 (8)  :class:`int`                            
    :attr:`outputPortNum`      192:200 (8)  :class:`int`                            
    :attr:`reserved1`          256:288 (32) :class:`int`                            
    :attr:`SLToVLMappingTable` 512:576 (64) :class:`~rdma.IBA.SMPSLToVLMappingTable`
    ========================== ============ ========================================

.. class:: rdma.IBA.SASMInfoRecord

    Container for SMInfo (section 15.2.5.10)

    .. attribute:: MAD_LENGTH = 28
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================= ============= ============================
    Member            Position      Type                        
    ================= ============= ============================
    :attr:`LID`       0:16 (16)     :class:`int`                
    :attr:`reserved1` 128:144 (16)  :class:`int`                
    :attr:`SMInfo`    256:448 (192) :class:`~rdma.IBA.SMPSMInfo`
    ================= ============= ============================

.. class:: rdma.IBA.SAServiceAssociationRecord

    ServiceRecord ServiceName/ServiceKey association (section 15.2.5.15)

    .. attribute:: MAD_LENGTH = 80
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3b
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    =================== ============= ============================
    Member              Position      Type                        
    =================== ============= ============================
    :attr:`serviceKey`  0:128 (128)   :class:`~rdma.IBA.GID`      
    :attr:`serviceName` 1024:1536 (8) [:class:`bytearray` (64)]*64
    =================== ============= ============================

.. class:: rdma.IBA.SAServiceRecord

    Information on advertised services (section 15.2.5.14)

    .. attribute:: MAD_LENGTH = 176
    .. attribute:: MAD_ATTRIBUTE_ID = 0x31
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE

    ===================== ================ ============================
    Member                Position         Type                        
    ===================== ================ ============================
    :attr:`serviceID`     0:64 (64)        :class:`int`                
    :attr:`serviceGID`    512:640 (128)    :class:`~rdma.IBA.GID`      
    :attr:`servicePKey`   1536:1552 (16)   :class:`int`                
    :attr:`reserved1`     1664:1680 (16)   :class:`int`                
    :attr:`serviceLease`  1792:1824 (32)   :class:`int`                
    :attr:`serviceKey`    2048:2176 (128)  :class:`~rdma.IBA.GID`      
    :attr:`serviceName`   3072:3584 (8)    [:class:`bytearray` (64)]*64
    :attr:`serviceData8`  7168:7296 (8)    [:class:`bytearray` (16)]*16
    :attr:`serviceData16` 8192:8320 (16)   [:class:`int`]*8            
    :attr:`serviceData32` 9216:9344 (32)   [:class:`int`]*4            
    :attr:`serviceData64` 10240:10368 (64) [:class:`int`]*2            
    ===================== ================ ============================

.. class:: rdma.IBA.SASwitchInfoRecord

    Container for SwitchInfo (section 15.2.5.5)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ================== ============= ================================
    Member             Position      Type                            
    ================== ============= ================================
    :attr:`LID`        0:16 (16)     :class:`int`                    
    :attr:`reserved1`  128:144 (16)  :class:`int`                    
    :attr:`switchInfo` 256:416 (160) :class:`~rdma.IBA.SMPSwitchInfo`
    ================== ============= ================================

.. class:: rdma.IBA.SATraceRecord

    Path trace information (section 15.2.5.19)

    .. attribute:: MAD_LENGTH = 48
    .. attribute:: MAD_ATTRIBUTE_ID = 0x39
    .. attribute:: MAD_SUBNADMGETTRACETABLE = 0x13 # MAD_METHOD_GET_TRACE_TABLE

    ==================== ============== ============
    Member               Position       Type        
    ==================== ============== ============
    :attr:`GIDPrefix`    0:64 (64)      :class:`int`
    :attr:`IDGeneration` 512:528 (16)   :class:`int`
    :attr:`reserved1`    640:648 (8)    :class:`int`
    :attr:`nodeType`     704:712 (8)    :class:`int`
    :attr:`nodeID`       768:832 (64)   :class:`int`
    :attr:`chassisID`    1280:1344 (64) :class:`int`
    :attr:`entryPortID`  1792:1856 (64) :class:`int`
    :attr:`exitPortID`   2304:2368 (64) :class:`int`
    :attr:`entryPort`    2816:2824 (8)  :class:`int`
    :attr:`exitPort`     2880:2888 (8)  :class:`int`
    :attr:`reserved2`    2944:2960 (16) :class:`int`
    ==================== ============== ============

.. class:: rdma.IBA.SAVLArbitrationTableRecord

    Container for VLArbitrationTable entry (section 15.2.5.9)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x36
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE

    ========================== ============== ========================================
    Member                     Position       Type                                    
    ========================== ============== ========================================
    :attr:`LID`                0:16 (16)      :class:`int`                            
    :attr:`outputPortNum`      128:136 (8)    :class:`int`                            
    :attr:`blockNum`           192:200 (8)    :class:`int`                            
    :attr:`reserved1`          256:288 (32)   :class:`int`                            
    :attr:`VLArbitrationTable` 512:1024 (512) :class:`~rdma.IBA.SMPVLArbitrationTable`
    ========================== ============== ========================================

Performance Management (16.1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.PMFormat

    Performance Management MAD Format (section 16.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x4
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ================= =============== ============================
    Member            Position        Type                        
    ================= =============== ============================
    :attr:`MADHeader` 0:192 (192)     :class:`~rdma.IBA.MADHeader`
    :attr:`reserved1` 192:512 (320)   :class:`bytearray` (40)     
    :attr:`data`      512:2048 (1536) :class:`bytearray` (192)    
    ================= =============== ============================

.. class:: rdma.IBA.PMPortCounters

    Port Basic Performance and Error Counters (section 16.1.3.5)

    .. attribute:: MAD_LENGTH = 44
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ==================================== ============== ============
    Member                               Position       Type        
    ==================================== ============== ============
    :attr:`reserved1`                    0:8 (8)        :class:`int`
    :attr:`portSelect`                   64:72 (8)      :class:`int`
    :attr:`counterSelect`                128:144 (16)   :class:`int`
    :attr:`symbolErrorCounter`           256:272 (16)   :class:`int`
    :attr:`linkErrorRecoveryCounter`     384:392 (8)    :class:`int`
    :attr:`linkDownedCounter`            448:456 (8)    :class:`int`
    :attr:`portRcvErrors`                512:528 (16)   :class:`int`
    :attr:`portRcvRemotePhysicalErrors`  640:656 (16)   :class:`int`
    :attr:`portRcvSwitchRelayErrors`     768:784 (16)   :class:`int`
    :attr:`portXmitDiscards`             896:912 (16)   :class:`int`
    :attr:`portXmitConstraintErrors`     1024:1032 (8)  :class:`int`
    :attr:`portRcvConstraintErrors`      1088:1096 (8)  :class:`int`
    :attr:`counterSelect2`               1152:1160 (8)  :class:`int`
    :attr:`localLinkIntegrityErrors`     1216:1220 (4)  :class:`int`
    :attr:`excessiveBufferOverrunErrors` 1248:1252 (4)  :class:`int`
    :attr:`reserved2`                    1280:1296 (16) :class:`int`
    :attr:`VL15Dropped`                  1408:1424 (16) :class:`int`
    :attr:`portXmitData`                 1536:1568 (32) :class:`int`
    :attr:`portRcvData`                  1792:1824 (32) :class:`int`
    :attr:`portXmitPkts`                 2048:2080 (32) :class:`int`
    :attr:`portRcvPkts`                  2304:2336 (32) :class:`int`
    :attr:`portXmitWait`                 2560:2592 (32) :class:`int`
    ==================================== ============== ============

.. class:: rdma.IBA.PMPortCountersExt

    Extended Port Counters (section 16.1.4.11)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1d
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ============================= ============== ============
    Member                        Position       Type        
    ============================= ============== ============
    :attr:`reserved1`             0:8 (8)        :class:`int`
    :attr:`portSelect`            64:72 (8)      :class:`int`
    :attr:`counterSelect`         128:144 (16)   :class:`int`
    :attr:`reserved2`             256:288 (32)   :class:`int`
    :attr:`portXmitData`          512:576 (64)   :class:`int`
    :attr:`portRcvData`           1024:1088 (64) :class:`int`
    :attr:`portXmitPkts`          1536:1600 (64) :class:`int`
    :attr:`portRcvPkts`           2048:2112 (64) :class:`int`
    :attr:`portUnicastXmitPkts`   2560:2624 (64) :class:`int`
    :attr:`portUnicastRcvPkts`    3072:3136 (64) :class:`int`
    :attr:`portMulticastXmitPkts` 3584:3648 (64) :class:`int`
    :attr:`portMulticastRcvPkts`  4096:4160 (64) :class:`int`
    ============================= ============== ============

.. class:: rdma.IBA.PMPortFlowCtlCounters

    Port Flow Control Counters (section 16.1.4.4)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ======================== ============ ============
    Member                   Position     Type        
    ======================== ============ ============
    :attr:`reserved1`        0:8 (8)      :class:`int`
    :attr:`portSelect`       64:72 (8)    :class:`int`
    :attr:`counterSelect`    128:144 (16) :class:`int`
    :attr:`portXmitFlowPkts` 256:288 (32) :class:`int`
    :attr:`portRcvFlowPkts`  512:544 (32) :class:`int`
    ======================== ============ ============

.. class:: rdma.IBA.PMPortOpRcvCounters

    Port Receive Counters per Op Code (section 16.1.4.3)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== ============ ============
    Member                Position     Type        
    ===================== ============ ============
    :attr:`opCode`        0:8 (8)      :class:`int`
    :attr:`portSelect`    64:72 (8)    :class:`int`
    :attr:`counterSelect` 128:144 (16) :class:`int`
    :attr:`portOpRcvPkts` 256:288 (32) :class:`int`
    :attr:`portOpRcvData` 512:544 (32) :class:`int`
    ===================== ============ ============

.. class:: rdma.IBA.PMPortRcvErrorDetails

    Port Detailed Error Counters (section 16.1.4.1)

    .. attribute:: MAD_LENGTH = 16
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ================================= ============ ============
    Member                            Position     Type        
    ================================= ============ ============
    :attr:`reserved1`                 0:8 (8)      :class:`int`
    :attr:`portSelect`                64:72 (8)    :class:`int`
    :attr:`counterSelect`             128:144 (16) :class:`int`
    :attr:`portLocalPhysicalErrors`   256:272 (16) :class:`int`
    :attr:`portMalformedPacketErrors` 384:400 (16) :class:`int`
    :attr:`portBufferOverrunErrors`   512:528 (16) :class:`int`
    :attr:`portDLIDMappingErrors`     640:656 (16) :class:`int`
    :attr:`portVLMappingErrors`       768:784 (16) :class:`int`
    :attr:`portLoopingErrors`         896:912 (16) :class:`int`
    ================================= ============ ============

.. class:: rdma.IBA.PMPortSamplesCtl

    Port Performance Data Sampling Control (section 16.1.3.2)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ============================= =============== ========================
    Member                        Position        Type                    
    ============================= =============== ========================
    :attr:`opCode`                0:8 (8)         :class:`int`            
    :attr:`portSelect`            64:72 (8)       :class:`int`            
    :attr:`tick`                  128:136 (8)     :class:`int`            
    :attr:`reserved1`             192:197 (5)     :class:`int`            
    :attr:`counterWidth`          232:235 (3)     :class:`int`            
    :attr:`reserved2`             256:258 (2)     :class:`int`            
    :attr:`counterMask0`          272:275 (3)     :class:`int`            
    :attr:`counterMask1`          296:299 (3)     :class:`int`            
    :attr:`counterMask2`          320:323 (3)     :class:`int`            
    :attr:`counterMask3`          344:347 (3)     :class:`int`            
    :attr:`counterMask4`          368:371 (3)     :class:`int`            
    :attr:`counterMask5`          392:395 (3)     :class:`int`            
    :attr:`counterMask6`          416:419 (3)     :class:`int`            
    :attr:`counterMask7`          440:443 (3)     :class:`int`            
    :attr:`counterMask8`          464:467 (3)     :class:`int`            
    :attr:`counterMask9`          488:491 (3)     :class:`int`            
    :attr:`reserved3`             512:513 (1)     :class:`int`            
    :attr:`counterMask10`         520:523 (3)     :class:`int`            
    :attr:`counterMask11`         544:547 (3)     :class:`int`            
    :attr:`counterMask12`         568:571 (3)     :class:`int`            
    :attr:`counterMask13`         592:595 (3)     :class:`int`            
    :attr:`counterMask14`         616:619 (3)     :class:`int`            
    :attr:`sampleMechanisms`      640:648 (8)     :class:`int`            
    :attr:`reserved4`             704:710 (6)     :class:`int`            
    :attr:`sampleStatus`          752:754 (2)     :class:`int`            
    :attr:`optionMask`            768:832 (64)    :class:`int`            
    :attr:`vendorMask`            1280:1344 (64)  :class:`int`            
    :attr:`sampleStart`           1792:1824 (32)  :class:`int`            
    :attr:`sampleInterval`        2048:2080 (32)  :class:`int`            
    :attr:`tag`                   2304:2320 (16)  :class:`int`            
    :attr:`counterSelect0`        2432:2448 (16)  :class:`int`            
    :attr:`counterSelect1`        2560:2576 (16)  :class:`int`            
    :attr:`counterSelect2`        2688:2704 (16)  :class:`int`            
    :attr:`counterSelect3`        2816:2832 (16)  :class:`int`            
    :attr:`counterSelect4`        2944:2960 (16)  :class:`int`            
    :attr:`counterSelect5`        3072:3088 (16)  :class:`int`            
    :attr:`counterSelect6`        3200:3216 (16)  :class:`int`            
    :attr:`counterSelect7`        3328:3344 (16)  :class:`int`            
    :attr:`counterSelect8`        3456:3472 (16)  :class:`int`            
    :attr:`counterSelect9`        3584:3600 (16)  :class:`int`            
    :attr:`counterSelect10`       3712:3728 (16)  :class:`int`            
    :attr:`counterSelect11`       3840:3856 (16)  :class:`int`            
    :attr:`counterSelect12`       3968:3984 (16)  :class:`int`            
    :attr:`counterSelect13`       4096:4112 (16)  :class:`int`            
    :attr:`counterSelect14`       4224:4240 (16)  :class:`int`            
    :attr:`reserved5`             4352:4384 (32)  :class:`int`            
    :attr:`samplesOnlyOptionMask` 4608:4672 (64)  :class:`int`            
    :attr:`reserved6`             5120:6016 (896) :class:`bytearray` (112)
    ============================= =============== ========================

.. class:: rdma.IBA.PMPortSamplesRes

    Port Performance Data Sampling Results (section 16.1.3.4)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET

    ==================== ============ =================
    Member               Position     Type             
    ==================== ============ =================
    :attr:`tag`          0:16 (16)    :class:`int`     
    :attr:`reserved1`    128:142 (14) :class:`int`     
    :attr:`sampleStatus` 240:242 (2)  :class:`int`     
    :attr:`counter`      256:736 (32) [:class:`int`]*15
    ==================== ============ =================

.. class:: rdma.IBA.PMPortSamplesResExt

    Extended Port Samples Result (section 16.1.4.10)

    .. attribute:: MAD_LENGTH = 128
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1e
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== ============= =================
    Member                Position      Type             
    ===================== ============= =================
    :attr:`tag`           0:16 (16)     :class:`int`     
    :attr:`reserved1`     128:142 (14)  :class:`int`     
    :attr:`sampleStatus`  240:242 (2)   :class:`int`     
    :attr:`extendedWidth` 256:258 (2)   :class:`int`     
    :attr:`reserved2`     272:302 (30)  :class:`int`     
    :attr:`counter`       512:1472 (64) [:class:`int`]*15
    ===================== ============= =================

.. class:: rdma.IBA.PMPortVLOpData

    Port Kilobytes Received per Op Code per VL (section 16.1.4.6)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== ============ =================
    Member                Position     Type             
    ===================== ============ =================
    :attr:`opCode`        0:8 (8)      :class:`int`     
    :attr:`portSelect`    64:72 (8)    :class:`int`     
    :attr:`counterSelect` 128:144 (16) :class:`int`     
    :attr:`portVLOpData`  256:768 (32) [:class:`int`]*16
    ===================== ============ =================

.. class:: rdma.IBA.PMPortVLOpPackets

    Port Packets Received per Op Code per VL (section 16.1.4.5)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ======================= ============ =================
    Member                  Position     Type             
    ======================= ============ =================
    :attr:`opCode`          0:8 (8)      :class:`int`     
    :attr:`portSelect`      64:72 (8)    :class:`int`     
    :attr:`counterSelect`   128:144 (16) :class:`int`     
    :attr:`portVLOpPackets` 256:512 (16) [:class:`int`]*16
    ======================= ============ =================

.. class:: rdma.IBA.PMPortVLXmitFlowCtlUpdateErrors

    Port Flow Control update errors per VL (section 16.1.4.7)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1b
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================================== ============ ============================
    Member                                Position     Type                        
    ===================================== ============ ============================
    :attr:`reserved1`                     0:8 (8)      :class:`int`                
    :attr:`portSelect`                    64:72 (8)    :class:`int`                
    :attr:`counterSelect`                 128:144 (16) :class:`int`                
    :attr:`portVLXmitFlowCtlUpdateErrors` 256:288 (2)  [:class:`bytearray` (16)]*16
    ===================================== ============ ============================

.. class:: rdma.IBA.PMPortVLXmitWaitCounters

    Port Ticks Waiting to Transmit Counters per VL (section 16.1.4.8)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1c
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ====================== ============ =================
    Member                 Position     Type             
    ====================== ============ =================
    :attr:`reserved1`      0:8 (8)      :class:`int`     
    :attr:`portSelect`     64:72 (8)    :class:`int`     
    :attr:`counterSelect`  128:144 (16) :class:`int`     
    :attr:`portVLXmitWait` 256:512 (16) [:class:`int`]*16
    ====================== ============ =================

.. class:: rdma.IBA.PMPortXmitDiscardDetails

    Port Transmit Discard Counters (section 16.1.4.2)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    =================================== ============ ============
    Member                              Position     Type        
    =================================== ============ ============
    :attr:`reserved1`                   0:8 (8)      :class:`int`
    :attr:`portSelect`                  64:72 (8)    :class:`int`
    :attr:`counterSelect`               128:144 (16) :class:`int`
    :attr:`portInactiveDiscards`        256:272 (16) :class:`int`
    :attr:`portNeighborMTUDiscards`     384:400 (16) :class:`int`
    :attr:`portSwLifetimeLimitDiscards` 512:528 (16) :class:`int`
    :attr:`portSwHOQLimitDiscards`      640:656 (16) :class:`int`
    =================================== ============ ============

.. class:: rdma.IBA.PMSwPortVLCongestion

    Switch Port Congestion per VL (section 16.1.4.9)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ========================== ============ =================
    Member                     Position     Type             
    ========================== ============ =================
    :attr:`reserved1`          0:8 (8)      :class:`int`     
    :attr:`portSelect`         64:72 (8)    :class:`int`     
    :attr:`counterSelect`      128:144 (16) :class:`int`     
    :attr:`swPortVLCongestion` 256:512 (16) [:class:`int`]*16
    ========================== ============ =================

Device Management (16.3)
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.DMDiagCode

    Vendor-Specific Device Diagnostic Information (section 16.3.3.10)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x24
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ================= ============ ============
    Member            Position     Type        
    ================= ============ ============
    :attr:`diagCode`  0:16 (16)    :class:`int`
    :attr:`reserved1` 128:144 (16) :class:`int`
    ================= ============ ============

.. class:: rdma.IBA.DMDiagnosticTimeout

    Get the Maximum Time for Completion of a Diagnostic Test (section 16.3.3.6)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    =================== ========= ============
    Member              Position  Type        
    =================== ========= ============
    :attr:`maxDiagTime` 0:32 (32) :class:`int`
    =================== ========= ============

.. class:: rdma.IBA.DMFormat

    Device Management MAD Format (section 16.3.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x6
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ================= =============== ============================
    Member            Position        Type                        
    ================= =============== ============================
    :attr:`MADHeader` 0:192 (192)     :class:`~rdma.IBA.MADHeader`
    :attr:`reserved1` 192:512 (320)   :class:`bytearray` (40)     
    :attr:`data`      512:2048 (1536) :class:`bytearray` (192)    
    ================= =============== ============================

.. class:: rdma.IBA.DMIOControllerProfile

    I/O Controller Profile Information (section 16.3.3.4)

    .. attribute:: MAD_LENGTH = 128
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ================================ ============== ============================
    Member                           Position       Type                        
    ================================ ============== ============================
    :attr:`GUID`                     0:64 (64)      :class:`~rdma.IBA.GUID`     
    :attr:`vendorID`                 512:536 (24)   :class:`int`                
    :attr:`reserved1`                704:712 (8)    :class:`int`                
    :attr:`deviceID`                 768:800 (32)   :class:`int`                
    :attr:`deviceVersion`            1024:1040 (16) :class:`int`                
    :attr:`reserved2`                1152:1168 (16) :class:`int`                
    :attr:`subsystemVendorID`        1280:1304 (24) :class:`int`                
    :attr:`reserved3`                1472:1480 (8)  :class:`int`                
    :attr:`subsystemID`              1536:1568 (32) :class:`int`                
    :attr:`IOClass`                  1792:1808 (16) :class:`int`                
    :attr:`IOSubclass`               1920:1936 (16) :class:`int`                
    :attr:`protocol`                 2048:2064 (16) :class:`int`                
    :attr:`protocolVersion`          2176:2192 (16) :class:`int`                
    :attr:`reserved4`                2304:2320 (16) :class:`int`                
    :attr:`reserved5`                2432:2448 (16) :class:`int`                
    :attr:`sendMessageDepth`         2560:2576 (16) :class:`int`                
    :attr:`reserved6`                2688:2696 (8)  :class:`int`                
    :attr:`RDMAReadDepth`            2752:2760 (8)  :class:`int`                
    :attr:`sendMessageSize`          2816:2848 (32) :class:`int`                
    :attr:`RDMATransferSize`         3072:3104 (32) :class:`int`                
    :attr:`controllerOperationsMask` 3328:3336 (8)  :class:`int`                
    :attr:`reserved7`                3392:3400 (8)  :class:`int`                
    :attr:`serviceEntries`           3456:3464 (8)  :class:`int`                
    :attr:`reserved8`                3520:3528 (8)  :class:`int`                
    :attr:`reserved9`                3584:3648 (64) :class:`int`                
    :attr:`IDString`                 4096:4608 (8)  [:class:`bytearray` (64)]*64
    ================================ ============== ============================

.. class:: rdma.IBA.DMIOUnitInfo

    List of all I/O Controllers in a I/O Unit (section 16.3.3.3)

    .. attribute:: MAD_LENGTH = 132
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ====================== =============== ========================
    Member                 Position        Type                    
    ====================== =============== ========================
    :attr:`changeID`       0:16 (16)       :class:`int`            
    :attr:`maxControllers` 128:136 (8)     :class:`int`            
    :attr:`reserved1`      192:198 (6)     :class:`int`            
    :attr:`diagDeviceID`   240:241 (1)     :class:`int`            
    :attr:`optionROM`      248:249 (1)     :class:`int`            
    :attr:`controllerList` 256:1280 (1024) :class:`bytearray` (128)
    ====================== =============== ========================

.. class:: rdma.IBA.DMPrepareToTest

    Prepare Device for Test (section 16.3.3.7)

    .. attribute:: MAD_LENGTH = 0
    .. attribute:: MAD_ATTRIBUTE_ID = 0x21
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET

    ====== ======== ====
    Member Position Type
    ====== ======== ====
    ====== ======== ====

.. class:: rdma.IBA.DMServiceEntries

    List of Supported Services and Their Associated Service IDs (section 16.3.3.5)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ==================== ============ =====================================
    Member               Position     Type                                 
    ==================== ============ =====================================
    :attr:`serviceEntry` 0:1536 (384) [:class:`~rdma.IBA.DMServiceEntry`]*4
    ==================== ============ =====================================

.. class:: rdma.IBA.DMServiceEntry

    Service Entry (section 16.3.3)

    .. attribute:: MAD_LENGTH = 48

    =================== ============== ============================
    Member              Position       Type                        
    =================== ============== ============================
    :attr:`serviceName` 0:320 (8)      [:class:`bytearray` (40)]*40
    :attr:`serviceID`   2560:2624 (64) :class:`int`                
    =================== ============== ============================

.. class:: rdma.IBA.DMTestDeviceLoop

    Test Device Continuously (section 16.3.3.9)

    .. attribute:: MAD_LENGTH = 0
    .. attribute:: MAD_ATTRIBUTE_ID = 0x23
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET

    ====== ======== ====
    Member Position Type
    ====== ======== ====
    ====== ======== ====

.. class:: rdma.IBA.DMTestDeviceOnce

    Test Device Once (section 16.3.3.8)

    .. attribute:: MAD_LENGTH = 0
    .. attribute:: MAD_ATTRIBUTE_ID = 0x22
    .. attribute:: MAD_DEVMGTSET = 0x2 # MAD_METHOD_SET

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

    ===================== ========= ============================
    Member                Position  Type                        
    ===================== ========= ============================
    :attr:`communityName` 0:512 (8) [:class:`bytearray` (64)]*64
    ===================== ========= ============================

.. class:: rdma.IBA.SNMPFormat

    SNMP Tunneling MAD Format (section 16.4.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x8
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ===================== =============== ============================
    Member                Position        Type                        
    ===================== =============== ============================
    :attr:`MADHeader`     0:192 (192)     :class:`~rdma.IBA.MADHeader`
    :attr:`reserved1`     192:448 (256)   :class:`bytearray` (32)     
    :attr:`RAddress`      448:480 (32)    :class:`int`                
    :attr:`payloadLength` 480:488 (8)     :class:`int`                
    :attr:`segmentNumber` 488:496 (8)     :class:`int`                
    :attr:`sourceLID`     496:512 (16)    :class:`int`                
    :attr:`data`          512:2048 (1536) :class:`bytearray` (192)    
    ===================== =============== ============================

.. class:: rdma.IBA.SNMPPDUInfo

    Data Segment (section 16.4.3.3)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SNMPSEND = 0x3 # MAD_METHOD_SEND

    =============== ============= ========================
    Member          Position      Type                    
    =============== ============= ========================
    :attr:`PDUData` 0:1536 (1536) :class:`bytearray` (192)
    =============== ============= ========================

Miscellaneous IBA Structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.CMFormat

    Request for Communication (section 16.7.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x7
    .. attribute:: MAD_CLASS_VERSION = 0x2

    ================= =============== ============================
    Member            Position        Type                        
    ================= =============== ============================
    :attr:`MADHeader` 0:192 (192)     :class:`~rdma.IBA.MADHeader`
    :attr:`data`      192:2048 (1856) :class:`bytearray` (232)    
    ================= =============== ============================

.. class:: rdma.IBA.HdrAETH

    ACK Extended Transport Header (section 9.3.5)

    .. attribute:: MAD_LENGTH = 4

    ================ ========== ============
    Member           Position   Type        
    ================ ========== ============
    :attr:`syndrome` 0:8 (8)    :class:`int`
    :attr:`MSN`      64:88 (24) :class:`int`
    ================ ========== ============

.. class:: rdma.IBA.HdrAtomicAckETH

    Atomic Acknowledge Extended Transport Header (section 9.5.3)

    .. attribute:: MAD_LENGTH = 8

    ================= ========= ============
    Member            Position  Type        
    ================= ========= ============
    :attr:`origRData` 0:64 (64) :class:`int`
    ================= ========= ============

.. class:: rdma.IBA.HdrAtomicETH

    Atomic Extended Transport Header (section 9.3.4)

    .. attribute:: MAD_LENGTH = 28

    ================ ============== ============
    Member           Position       Type        
    ================ ============== ============
    :attr:`VA`       0:64 (64)      :class:`int`
    :attr:`RKey`     512:544 (32)   :class:`int`
    :attr:`swapData` 768:832 (64)   :class:`int`
    :attr:`cmpData`  1280:1344 (64) :class:`int`
    ================ ============== ============

.. class:: rdma.IBA.HdrBTH

    Base Transport Header (section 9.2)

    .. attribute:: MAD_LENGTH = 12

    ================= ============ ============
    Member            Position     Type        
    ================= ============ ============
    :attr:`service`   0:3 (3)      :class:`int`
    :attr:`function`  24:29 (5)    :class:`int`
    :attr:`SE`        64:65 (1)    :class:`int`
    :attr:`migReq`    72:73 (1)    :class:`int`
    :attr:`padCnt`    80:82 (2)    :class:`int`
    :attr:`TVer`      96:100 (4)   :class:`int`
    :attr:`PKey`      128:144 (16) :class:`int`
    :attr:`reserved1` 32:40 (8)    :class:`int`
    :attr:`destQP`    68:92 (24)   :class:`int`
    :attr:`ackReq`    64:65 (1)    :class:`int`
    :attr:`reserved2` 16:23 (7)    :class:`int`
    :attr:`PSN`       72:96 (24)   :class:`int`
    ================= ============ ============

.. class:: rdma.IBA.HdrDETH

    Datagram Extended Transport Header (section 9.3.2)

    .. attribute:: MAD_LENGTH = 8

    ================= ============ ============
    Member            Position     Type        
    ================= ============ ============
    :attr:`QKey`      0:32 (32)    :class:`int`
    :attr:`reserved1` 256:264 (8)  :class:`int`
    :attr:`srcQP`     320:344 (24) :class:`int`
    ================= ============ ============

.. class:: rdma.IBA.HdrFlowControl

    Flow Control Packet (section 7.9.4)

    .. attribute:: MAD_LENGTH = 4

    ============= ============ ============
    Member        Position     Type        
    ============= ============ ============
    :attr:`op`    0:4 (4)      :class:`int`
    :attr:`FCTBS` 32:44 (12)   :class:`int`
    :attr:`VL`    128:132 (4)  :class:`int`
    :attr:`FCCL`  160:172 (12) :class:`int`
    ============= ============ ============

.. class:: rdma.IBA.HdrGRH

    Global Route Header (section 8.3)

    .. attribute:: MAD_LENGTH = 40

    ================= ============= ======================
    Member            Position      Type                  
    ================= ============= ======================
    :attr:`IPVer`     0:4 (4)       :class:`int`          
    :attr:`TClass`    32:40 (8)     :class:`int`          
    :attr:`flowLabel` 96:116 (20)   :class:`int`          
    :attr:`payLen`    32:48 (16)    :class:`int`          
    :attr:`nxtHdr`    132:140 (8)   :class:`int`          
    :attr:`hopLmt`    196:204 (8)   :class:`int`          
    :attr:`SGID`      64:192 (128)  :class:`~rdma.IBA.GID`
    :attr:`DGID`      192:320 (128) :class:`~rdma.IBA.GID`
    ================= ============= ======================

.. class:: rdma.IBA.HdrIETH

    Invalidate Extended Transport Header (section 9.3.7)

    .. attribute:: MAD_LENGTH = 4

    ============ ========= ============
    Member       Position  Type        
    ============ ========= ============
    :attr:`RKey` 0:32 (32) :class:`int`
    ============ ========= ============

.. class:: rdma.IBA.HdrImmDt

    Immediate Extended Transport Header (section 9.3.6)

    .. attribute:: MAD_LENGTH = 4

    ===================== ========= ============
    Member                Position  Type        
    ===================== ========= ============
    :attr:`immediateData` 0:32 (32) :class:`int`
    ===================== ========= ============

.. class:: rdma.IBA.HdrLRH

    Local Route Header (section 7.7)

    .. attribute:: MAD_LENGTH = 8

    ================= ============ ============
    Member            Position     Type        
    ================= ============ ============
    :attr:`VL`        0:4 (4)      :class:`int`
    :attr:`LVer`      32:36 (4)    :class:`int`
    :attr:`SL`        64:68 (4)    :class:`int`
    :attr:`reserved1` 96:98 (2)    :class:`int`
    :attr:`LNH`       112:114 (2)  :class:`int`
    :attr:`DLID`      128:144 (16) :class:`int`
    :attr:`reserved2` 4:9 (5)      :class:`int`
    :attr:`pktLen`    44:55 (11)   :class:`int`
    :attr:`SLID`      132:148 (16) :class:`int`
    ================= ============ ============

.. class:: rdma.IBA.HdrRDETH

    Reliable Datagram Extended Transport Header (section 9.3.1)

    .. attribute:: MAD_LENGTH = 4

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`reserved1` 0:8 (8)    :class:`int`
    :attr:`EEC`       64:88 (24) :class:`int`
    ================= ========== ============

.. class:: rdma.IBA.HdrRETH

    RDMA Extended Transport Header (section 9.3.3)

    .. attribute:: MAD_LENGTH = 16

    ============== ============ ============
    Member         Position     Type        
    ============== ============ ============
    :attr:`VA`     0:64 (64)    :class:`int`
    :attr:`RKey`   512:544 (32) :class:`int`
    :attr:`DMALen` 768:800 (32) :class:`int`
    ============== ============ ============

.. class:: rdma.IBA.HdrRWH

    Raw Header (section 5.3)

    .. attribute:: MAD_LENGTH = 4

    ================= ============ ============
    Member            Position     Type        
    ================= ============ ============
    :attr:`reserved1` 0:16 (16)    :class:`int`
    :attr:`etherType` 128:144 (16) :class:`int`
    ================= ============ ============

