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
    :attr:`reserved1`          125:128 (3)     :class:`int`            
    :attr:`reserved2`          128:160 (32)    :class:`int`            
    :attr:`altSLID`            160:176 (16)    :class:`int`            
    :attr:`altDLID`            176:192 (16)    :class:`int`            
    :attr:`altSGID`            192:320 (128)   :class:`~rdma.IBA.GID`  
    :attr:`altDGID`            320:448 (128)   :class:`~rdma.IBA.GID`  
    :attr:`altFlowLabel`       448:468 (20)    :class:`int`            
    :attr:`reserved3`          468:472 (4)     :class:`int`            
    :attr:`altTClass`          472:480 (8)     :class:`int`            
    :attr:`altHopLimit`        480:488 (8)     :class:`int`            
    :attr:`reserved4`          488:490 (2)     :class:`int`            
    :attr:`altIPD`             490:496 (6)     :class:`int`            
    :attr:`altSL`              496:500 (4)     :class:`int`            
    :attr:`altSubnetLocal`     500:501 (1)     :class:`int`            
    :attr:`reserved5`          501:504 (3)     :class:`int`            
    :attr:`altLocalACKTimeout` 504:509 (5)     :class:`int`            
    :attr:`reserved6`          509:512 (3)     :class:`int`            
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
    :attr:`reserved1`      66:72 (6)      :class:`int`            
    :attr:`serviceTimeout` 72:77 (5)      :class:`int`            
    :attr:`reserved2`      77:80 (3)      :class:`int`            
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
    :attr:`reserved1`       308:312 (4)   :class:`int`          
    :attr:`reserved2`       312:314 (2)   :class:`int`          
    :attr:`PD`              314:320 (6)   :class:`int`          
    :attr:`TClass`          320:328 (8)   :class:`int`          
    :attr:`hopLimit`        328:336 (8)   :class:`int`          
    :attr:`SL`              336:340 (4)   :class:`int`          
    :attr:`subnetLocal`     340:341 (1)   :class:`int`          
    :attr:`reserved3`       341:344 (3)   :class:`int`          
    :attr:`localACKTimeout` 344:349 (5)   :class:`int`          
    :attr:`reserved4`       349:352 (3)   :class:`int`          
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
    :attr:`reserved1`        66:72 (6)       :class:`int`            
    :attr:`rejectInfoLength` 72:79 (7)       :class:`int`            
    :attr:`reserved2`        79:80 (1)       :class:`int`            
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
    :attr:`failoverAccepted`   213:215 (2)     :class:`int`            
    :attr:`flowControl`        215:216 (1)     :class:`int`            
    :attr:`RNRRetryCount`      216:219 (3)     :class:`int`            
    :attr:`reserved4`          219:224 (5)     :class:`int`            
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
    :attr:`transportService`      349:351 (2)     :class:`int`             
    :attr:`flowControl`           351:352 (1)     :class:`int`             
    :attr:`startingPSN`           352:376 (24)    :class:`int`             
    :attr:`localResponseTimeout`  376:381 (5)     :class:`int`             
    :attr:`retryCount`            381:384 (3)     :class:`int`             
    :attr:`PKey`                  384:400 (16)    :class:`int`             
    :attr:`pathPacketMTU`         400:404 (4)     :class:`int`             
    :attr:`RDCExists`             404:405 (1)     :class:`int`             
    :attr:`RNRRetryCount`         405:408 (3)     :class:`int`             
    :attr:`maxCMRetries`          408:412 (4)     :class:`int`             
    :attr:`reserved2`             412:416 (4)     :class:`int`             
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
    .. attribute:: COMPONENT_MASK = {'baseVersion':0, 'classVersion':1, 'capabilityMask':2, 'capabilityMask2':3, 'respTimeValue':4, 'redirectGID':5, 'redirectTC':6, 'redirectSL':7, 'redirectFL':8, 'redirectLID':9, 'redirectPKey':10, 'reserved1':11, 'redirectQP':12, 'redirectQKey':13, 'trapGID':14, 'trapTC':15, 'trapSL':16, 'trapFL':17, 'trapLID':18, 'trapPKey':19, 'trapHL':20, 'trapQP':21, 'trapQKey':22}

    ======================= ============= ======================
    Member                  Position      Type                  
    ======================= ============= ======================
    :attr:`baseVersion`     0:8 (8)       :class:`int`          
    :attr:`classVersion`    8:16 (8)      :class:`int`          
    :attr:`capabilityMask`  16:32 (16)    :class:`int`          
    :attr:`capabilityMask2` 32:59 (27)    :class:`int`          
    :attr:`respTimeValue`   59:64 (5)     :class:`int`          
    :attr:`redirectGID`     64:192 (128)  :class:`~rdma.IBA.GID`
    :attr:`redirectTC`      192:200 (8)   :class:`int`          
    :attr:`redirectSL`      200:204 (4)   :class:`int`          
    :attr:`redirectFL`      204:224 (20)  :class:`int`          
    :attr:`redirectLID`     224:240 (16)  :class:`int`          
    :attr:`redirectPKey`    240:256 (16)  :class:`int`          
    :attr:`reserved1`       256:264 (8)   :class:`int`          
    :attr:`redirectQP`      264:288 (24)  :class:`int`          
    :attr:`redirectQKey`    288:320 (32)  :class:`int`          
    :attr:`trapGID`         320:448 (128) :class:`~rdma.IBA.GID`
    :attr:`trapTC`          448:456 (8)   :class:`int`          
    :attr:`trapSL`          456:460 (4)   :class:`int`          
    :attr:`trapFL`          460:480 (20)  :class:`int`          
    :attr:`trapLID`         480:496 (16)  :class:`int`          
    :attr:`trapPKey`        496:512 (16)  :class:`int`          
    :attr:`trapHL`          512:520 (8)   :class:`int`          
    :attr:`trapQP`          520:544 (24)  :class:`int`          
    :attr:`trapQKey`        544:576 (32)  :class:`int`          
    ======================= ============= ======================

.. class:: rdma.IBA.MADHeader

    MAD Base Header (section 13.4.3)

    .. attribute:: MAD_LENGTH = 24

    ========================= ============ ============
    Member                    Position     Type        
    ========================= ============ ============
    :attr:`baseVersion`       0:8 (8)      :class:`int`
    :attr:`mgmtClass`         8:16 (8)     :class:`int`
    :attr:`classVersion`      16:24 (8)    :class:`int`
    :attr:`method`            24:32 (8)    :class:`int`
    :attr:`status`            32:48 (16)   :class:`int`
    :attr:`classSpecific`     48:64 (16)   :class:`int`
    :attr:`transactionID`     64:128 (64)  :class:`int`
    :attr:`attributeID`       128:144 (16) :class:`int`
    :attr:`reserved1`         144:160 (16) :class:`int`
    :attr:`attributeModifier` 160:192 (32) :class:`int`
    ========================= ============ ============

.. class:: rdma.IBA.MADHeaderDirected

    MAD Base Header Directed (section 13.4.3)

    .. attribute:: MAD_LENGTH = 24

    ========================= ============ ============
    Member                    Position     Type        
    ========================= ============ ============
    :attr:`baseVersion`       0:8 (8)      :class:`int`
    :attr:`mgmtClass`         8:16 (8)     :class:`int`
    :attr:`classVersion`      16:24 (8)    :class:`int`
    :attr:`method`            24:32 (8)    :class:`int`
    :attr:`D`                 32:33 (1)    :class:`int`
    :attr:`status`            33:48 (15)   :class:`int`
    :attr:`hopPointer`        48:56 (8)    :class:`int`
    :attr:`hopCount`          56:64 (8)    :class:`int`
    :attr:`transactionID`     64:128 (64)  :class:`int`
    :attr:`attributeID`       128:144 (16) :class:`int`
    :attr:`reserved1`         144:160 (16) :class:`int`
    :attr:`attributeModifier` 160:192 (32) :class:`int`
    ========================= ============ ============

.. class:: rdma.IBA.MADInformInfo

    InformInfo (section 13.4.8.3)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: COMPONENT_MASK = {'GID':0, 'LIDRangeBegin':1, 'LIDRangeEnd':2, 'reserved1':3, 'isGeneric':4, 'subscribe':5, 'type':6, 'trapNumber':7, 'QPN':8, 'reserved2':9, 'respTimeValue':10, 'reserved3':11, 'producerType':12}

    ===================== ============ ======================
    Member                Position     Type                  
    ===================== ============ ======================
    :attr:`GID`           0:128 (128)  :class:`~rdma.IBA.GID`
    :attr:`LIDRangeBegin` 128:144 (16) :class:`int`          
    :attr:`LIDRangeEnd`   144:160 (16) :class:`int`          
    :attr:`reserved1`     160:176 (16) :class:`int`          
    :attr:`isGeneric`     176:184 (8)  :class:`int`          
    :attr:`subscribe`     184:192 (8)  :class:`int`          
    :attr:`type`          192:208 (16) :class:`int`          
    :attr:`trapNumber`    208:224 (16) :class:`int`          
    :attr:`QPN`           224:248 (24) :class:`int`          
    :attr:`reserved2`     248:251 (3)  :class:`int`          
    :attr:`respTimeValue` 251:256 (5)  :class:`int`          
    :attr:`reserved3`     256:264 (8)  :class:`int`          
    :attr:`producerType`  264:288 (24) :class:`int`          
    ===================== ============ ======================

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
    :attr:`RMPPFlags`   213:216 (3)  :class:`int`                
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
    :attr:`RMPPFlags`   213:216 (3) :class:`int`                
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

    An *aggregation* of: MADHeader

    SMP Format - LID Routed (section 14.2.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x1
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ========================= ================ ========================
    Member                    Position         Type                    
    ========================= ================ ========================
    :attr:`baseVersion`       0:8 (8)          :class:`int`            
    :attr:`mgmtClass`         8:16 (8)         :class:`int`            
    :attr:`classVersion`      16:24 (8)        :class:`int`            
    :attr:`method`            24:32 (8)        :class:`int`            
    :attr:`status`            32:48 (16)       :class:`int`            
    :attr:`classSpecific`     48:64 (16)       :class:`int`            
    :attr:`transactionID`     64:128 (64)      :class:`int`            
    :attr:`attributeID`       128:144 (16)     :class:`int`            
    :attr:`reserved1`         144:160 (16)     :class:`int`            
    :attr:`attributeModifier` 160:192 (32)     :class:`int`            
    :attr:`MKey`              192:256 (64)     :class:`int`            
    :attr:`reserved2`         256:512 (256)    :class:`bytearray` (32) 
    :attr:`data`              512:1024 (512)   :class:`bytearray` (64) 
    :attr:`reserved3`         1024:2048 (1024) :class:`bytearray` (128)
    ========================= ================ ========================

.. class:: rdma.IBA.SMPFormatDirected

    An *aggregation* of: MADHeaderDirected

    SMP Format - Direct Routed (section 14.2.1.2)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x81
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ========================= ============== ============================
    Member                    Position       Type                        
    ========================= ============== ============================
    :attr:`baseVersion`       0:8 (8)        :class:`int`                
    :attr:`mgmtClass`         8:16 (8)       :class:`int`                
    :attr:`classVersion`      16:24 (8)      :class:`int`                
    :attr:`method`            24:32 (8)      :class:`int`                
    :attr:`D`                 32:33 (1)      :class:`int`                
    :attr:`status`            33:48 (15)     :class:`int`                
    :attr:`hopPointer`        48:56 (8)      :class:`int`                
    :attr:`hopCount`          56:64 (8)      :class:`int`                
    :attr:`transactionID`     64:128 (64)    :class:`int`                
    :attr:`attributeID`       128:144 (16)   :class:`int`                
    :attr:`reserved1`         144:160 (16)   :class:`int`                
    :attr:`attributeModifier` 160:192 (32)   :class:`int`                
    :attr:`MKey`              192:256 (64)   :class:`int`                
    :attr:`drSLID`            256:272 (16)   :class:`int`                
    :attr:`drDLID`            272:288 (16)   :class:`int`                
    :attr:`reserved2`         288:512 (224)  :class:`bytearray` (28)     
    :attr:`data`              512:1024 (512) :class:`bytearray` (64)     
    :attr:`initialPath`       1024:1536 (8)  [:class:`bytearray` (64)]*64
    :attr:`returnPath`        1536:2048 (8)  [:class:`bytearray` (64)]*64
    ========================= ============== ============================

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

    ================= ========= ============
    Member            Position  Type        
    ================= ========= ============
    :attr:`LID`       0:16 (16) :class:`int`
    :attr:`valid`     16:17 (1) :class:`int`
    :attr:`LMC`       17:20 (3) :class:`int`
    :attr:`reserved1` 20:24 (4) :class:`int`
    :attr:`port`      24:32 (8) :class:`int`
    ================= ========= ============

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
    :attr:`reserved1` 1:32 (31) :class:`int`
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

    ======================= ============ =======================
    Member                  Position     Type                   
    ======================= ============ =======================
    :attr:`baseVersion`     0:8 (8)      :class:`int`           
    :attr:`classVersion`    8:16 (8)     :class:`int`           
    :attr:`nodeType`        16:24 (8)    :class:`int`           
    :attr:`numPorts`        24:32 (8)    :class:`int`           
    :attr:`systemImageGUID` 32:96 (64)   :class:`~rdma.IBA.GUID`
    :attr:`nodeGUID`        96:160 (64)  :class:`~rdma.IBA.GUID`
    :attr:`portGUID`        160:224 (64) :class:`~rdma.IBA.GUID`
    :attr:`partitionCap`    224:240 (16) :class:`int`           
    :attr:`deviceID`        240:256 (16) :class:`int`           
    :attr:`revision`        256:288 (32) :class:`int`           
    :attr:`localPortNum`    288:296 (8)  :class:`int`           
    :attr:`vendorID`        296:320 (24) :class:`int`           
    ======================= ============ =======================

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

    ==================================== ============ ============
    Member                               Position     Type        
    ==================================== ============ ============
    :attr:`MKey`                         0:64 (64)    :class:`int`
    :attr:`GIDPrefix`                    64:128 (64)  :class:`int`
    :attr:`LID`                          128:144 (16) :class:`int`
    :attr:`masterSMLID`                  144:160 (16) :class:`int`
    :attr:`capabilityMask`               160:192 (32) :class:`int`
    :attr:`diagCode`                     192:208 (16) :class:`int`
    :attr:`MKeyLeasePeriod`              208:224 (16) :class:`int`
    :attr:`localPortNum`                 224:232 (8)  :class:`int`
    :attr:`linkWidthEnabled`             232:240 (8)  :class:`int`
    :attr:`linkWidthSupported`           240:248 (8)  :class:`int`
    :attr:`linkWidthActive`              248:256 (8)  :class:`int`
    :attr:`linkSpeedSupported`           256:260 (4)  :class:`int`
    :attr:`portState`                    260:264 (4)  :class:`int`
    :attr:`portPhysicalState`            264:268 (4)  :class:`int`
    :attr:`linkDownDefaultState`         268:272 (4)  :class:`int`
    :attr:`MKeyProtectBits`              272:274 (2)  :class:`int`
    :attr:`reserved1`                    274:277 (3)  :class:`int`
    :attr:`LMC`                          277:280 (3)  :class:`int`
    :attr:`linkSpeedActive`              280:284 (4)  :class:`int`
    :attr:`linkSpeedEnabled`             284:288 (4)  :class:`int`
    :attr:`neighborMTU`                  288:292 (4)  :class:`int`
    :attr:`masterSMSL`                   292:296 (4)  :class:`int`
    :attr:`VLCap`                        296:300 (4)  :class:`int`
    :attr:`initType`                     300:304 (4)  :class:`int`
    :attr:`VLHighLimit`                  304:312 (8)  :class:`int`
    :attr:`VLArbitrationHighCap`         312:320 (8)  :class:`int`
    :attr:`VLArbitrationLowCap`          320:328 (8)  :class:`int`
    :attr:`initTypeReply`                328:332 (4)  :class:`int`
    :attr:`MTUCap`                       332:336 (4)  :class:`int`
    :attr:`VLStallCount`                 336:339 (3)  :class:`int`
    :attr:`HOQLife`                      339:344 (5)  :class:`int`
    :attr:`operationalVLs`               344:348 (4)  :class:`int`
    :attr:`partitionEnforcementInbound`  348:349 (1)  :class:`int`
    :attr:`partitionEnforcementOutbound` 349:350 (1)  :class:`int`
    :attr:`filterRawInbound`             350:351 (1)  :class:`int`
    :attr:`filterRawOutbound`            351:352 (1)  :class:`int`
    :attr:`MKeyViolations`               352:368 (16) :class:`int`
    :attr:`PKeyViolations`               368:384 (16) :class:`int`
    :attr:`QKeyViolations`               384:400 (16) :class:`int`
    :attr:`GUIDCap`                      400:408 (8)  :class:`int`
    :attr:`clientReregister`             408:409 (1)  :class:`int`
    :attr:`reserved2`                    409:411 (2)  :class:`int`
    :attr:`subnetTimeOut`                411:416 (5)  :class:`int`
    :attr:`reserved3`                    416:419 (3)  :class:`int`
    :attr:`respTimeValue`                419:424 (5)  :class:`int`
    :attr:`localPhyErrors`               424:428 (4)  :class:`int`
    :attr:`overrunErrors`                428:432 (4)  :class:`int`
    :attr:`reserved4`                    432:448 (16) :class:`int`
    ==================================== ============ ============

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

    ============== ======== =================
    Member         Position Type             
    ============== ======== =================
    :attr:`SLtoVL` 0:64 (4) [:class:`int`]*16
    ============== ======== =================

.. class:: rdma.IBA.SMPSMInfo

    Subnet Management Information (section 14.2.5.13)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ================= ============ =======================
    Member            Position     Type                   
    ================= ============ =======================
    :attr:`GUID`      0:64 (64)    :class:`~rdma.IBA.GUID`
    :attr:`SMKey`     64:128 (64)  :class:`int`           
    :attr:`actCount`  128:160 (32) :class:`int`           
    :attr:`priority`  160:164 (4)  :class:`int`           
    :attr:`SMState`   164:168 (4)  :class:`int`           
    :attr:`reserved1` 168:192 (24) :class:`int`           
    ================= ============ =======================

.. class:: rdma.IBA.SMPSwitchInfo

    Switch Information (section 14.2.5.4)

    .. attribute:: MAD_LENGTH = 20
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_SUBNGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNSET = 0x2 # MAD_METHOD_SET

    ========================================= ============ ============
    Member                                    Position     Type        
    ========================================= ============ ============
    :attr:`linearFDBCap`                      0:16 (16)    :class:`int`
    :attr:`randomFDBCap`                      16:32 (16)   :class:`int`
    :attr:`multicastFDBCap`                   32:48 (16)   :class:`int`
    :attr:`linearFDBTop`                      48:64 (16)   :class:`int`
    :attr:`defaultPort`                       64:72 (8)    :class:`int`
    :attr:`defaultMulticastPrimaryPort`       72:80 (8)    :class:`int`
    :attr:`defaultMulticastNotPrimaryPort`    80:88 (8)    :class:`int`
    :attr:`lifeTimeValue`                     88:93 (5)    :class:`int`
    :attr:`portStateChange`                   93:94 (1)    :class:`int`
    :attr:`reserved1`                         94:95 (1)    :class:`int`
    :attr:`optimizedSLtoVLMappingProgramming` 95:96 (1)    :class:`int`
    :attr:`LIDsPerPort`                       96:112 (16)  :class:`int`
    :attr:`partitionEnforcementCap`           112:128 (16) :class:`int`
    :attr:`inboundEnforcementCap`             128:129 (1)  :class:`int`
    :attr:`outboundEnforcementCap`            129:130 (1)  :class:`int`
    :attr:`filterRawInboundCap`               130:131 (1)  :class:`int`
    :attr:`filterRawOutboundCap`              131:132 (1)  :class:`int`
    :attr:`enhancedPort0`                     132:133 (1)  :class:`int`
    :attr:`reserved2`                         133:136 (3)  :class:`int`
    :attr:`reserved3`                         136:160 (24) :class:`int`
    ========================================= ============ ============

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

    ================= ============ =======================
    Member            Position     Type                   
    ================= ============ =======================
    :attr:`nextIndex` 0:16 (16)    :class:`int`           
    :attr:`reserved1` 16:32 (16)   :class:`int`           
    :attr:`diagData`  32:512 (480) :class:`bytearray` (60)
    ================= ============ =======================

Subnet Administration (15)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.SAFormat

    An *aggregation* of: SAHeader

    SA Format (section 15.2.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x3
    .. attribute:: MAD_CLASS_VERSION = 0x2

    ========================= =============== ========================
    Member                    Position        Type                    
    ========================= =============== ========================
    :attr:`baseVersion`       0:8 (8)         :class:`int`            
    :attr:`mgmtClass`         8:16 (8)        :class:`int`            
    :attr:`classVersion`      16:24 (8)       :class:`int`            
    :attr:`method`            24:32 (8)       :class:`int`            
    :attr:`status`            32:48 (16)      :class:`int`            
    :attr:`classSpecific`     48:64 (16)      :class:`int`            
    :attr:`transactionID`     64:128 (64)     :class:`int`            
    :attr:`attributeID`       128:144 (16)    :class:`int`            
    :attr:`reserved1`         144:160 (16)    :class:`int`            
    :attr:`attributeModifier` 160:192 (32)    :class:`int`            
    :attr:`RMPPVersion`       192:200 (8)     :class:`int`            
    :attr:`RMPPType`          200:208 (8)     :class:`int`            
    :attr:`RRespTime`         208:213 (5)     :class:`int`            
    :attr:`RMPPFlags`         213:216 (3)     :class:`int`            
    :attr:`RMPPStatus`        216:224 (8)     :class:`int`            
    :attr:`data1`             224:256 (32)    :class:`int`            
    :attr:`data2`             256:288 (32)    :class:`int`            
    :attr:`SMKey`             288:352 (64)    :class:`int`            
    :attr:`attributeOffset`   352:368 (16)    :class:`int`            
    :attr:`reserved2`         368:384 (16)    :class:`int`            
    :attr:`componentMask`     384:448 (64)    :class:`int`            
    :attr:`data`              448:2048 (1600) :class:`bytearray` (200)
    ========================= =============== ========================

.. class:: rdma.IBA.SAGUIDInfoRecord

    Container for port GUIDInfo (section 15.2.5.18)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved1':2, 'reserved2':3, 'GUIDInfo.GUIDBlock':4}

    ================= ============ ==============================
    Member            Position     Type                          
    ================= ============ ==============================
    :attr:`LID`       0:16 (16)    :class:`int`                  
    :attr:`blockNum`  16:24 (8)    :class:`int`                  
    :attr:`reserved1` 24:32 (8)    :class:`int`                  
    :attr:`reserved2` 32:64 (32)   :class:`int`                  
    :attr:`GUIDInfo`  64:576 (512) :class:`~rdma.IBA.SMPGUIDInfo`
    ================= ============ ==============================

.. class:: rdma.IBA.SAHeader

    An *aggregation* of: MADHeader, RMPPHeader

    SA Header (section 15.2.1.1)

    .. attribute:: MAD_LENGTH = 56
    .. attribute:: MAD_CLASS = 0x3
    .. attribute:: MAD_CLASS_VERSION = 0x2

    ========================= ============ ============
    Member                    Position     Type        
    ========================= ============ ============
    :attr:`baseVersion`       0:8 (8)      :class:`int`
    :attr:`mgmtClass`         8:16 (8)     :class:`int`
    :attr:`classVersion`      16:24 (8)    :class:`int`
    :attr:`method`            24:32 (8)    :class:`int`
    :attr:`status`            32:48 (16)   :class:`int`
    :attr:`classSpecific`     48:64 (16)   :class:`int`
    :attr:`transactionID`     64:128 (64)  :class:`int`
    :attr:`attributeID`       128:144 (16) :class:`int`
    :attr:`reserved1`         144:160 (16) :class:`int`
    :attr:`attributeModifier` 160:192 (32) :class:`int`
    :attr:`RMPPVersion`       192:200 (8)  :class:`int`
    :attr:`RMPPType`          200:208 (8)  :class:`int`
    :attr:`RRespTime`         208:213 (5)  :class:`int`
    :attr:`RMPPFlags`         213:216 (3)  :class:`int`
    :attr:`RMPPStatus`        216:224 (8)  :class:`int`
    :attr:`data1`             224:256 (32) :class:`int`
    :attr:`data2`             256:288 (32) :class:`int`
    :attr:`SMKey`             288:352 (64) :class:`int`
    :attr:`attributeOffset`   352:368 (16) :class:`int`
    :attr:`reserved2`         368:384 (16) :class:`int`
    :attr:`componentMask`     384:448 (64) :class:`int`
    ========================= ============ ============

.. class:: rdma.IBA.SAInformInfoRecord

    Container for InformInfo (section 15.2.5.12)

    .. attribute:: MAD_LENGTH = 80
    .. attribute:: MAD_ATTRIBUTE_ID = 0xf3
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'subscriberGID':0, 'enumeration':1, 'reserved1':2, 'reserved2':3, 'informInfo.GID':4, 'informInfo.LIDRangeBegin':5, 'informInfo.LIDRangeEnd':6, 'informInfo.reserved1':7, 'informInfo.isGeneric':8, 'informInfo.subscribe':9, 'informInfo.type':10, 'informInfo.trapNumber':11, 'informInfo.QPN':12, 'informInfo.reserved2':13, 'informInfo.respTimeValue':14, 'informInfo.reserved3':15, 'informInfo.producerType':16, 'reserved3':17}

    ===================== ============= ================================
    Member                Position      Type                            
    ===================== ============= ================================
    :attr:`subscriberGID` 0:128 (128)   :class:`~rdma.IBA.GID`          
    :attr:`enumeration`   128:144 (16)  :class:`int`                    
    :attr:`reserved1`     144:160 (16)  :class:`int`                    
    :attr:`reserved2`     160:192 (32)  :class:`int`                    
    :attr:`informInfo`    192:480 (288) :class:`~rdma.IBA.MADInformInfo`
    :attr:`reserved3`     480:640 (160) :class:`bytearray` (20)         
    ===================== ============= ================================

.. class:: rdma.IBA.SALinearForwardingTableRecord

    Container for LinearForwardingTable entry (section 15.2.5.6)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x15
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved1':2, 'linearForwardingTable.portBlock':3}

    ============================= ============ ===========================================
    Member                        Position     Type                                       
    ============================= ============ ===========================================
    :attr:`LID`                   0:16 (16)    :class:`int`                               
    :attr:`blockNum`              16:32 (16)   :class:`int`                               
    :attr:`reserved1`             32:64 (32)   :class:`int`                               
    :attr:`linearForwardingTable` 64:576 (512) :class:`~rdma.IBA.SMPLinearForwardingTable`
    ============================= ============ ===========================================

.. class:: rdma.IBA.SALinkRecord

    Inter-node linkage information (section 15.2.5.13)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x20
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'fromLID':0, 'fromPort':1, 'toPort':2, 'toLID':3, 'reserved1':4}

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`fromLID`   0:16 (16)  :class:`int`
    :attr:`fromPort`  16:24 (8)  :class:`int`
    :attr:`toPort`    24:32 (8)  :class:`int`
    :attr:`toLID`     32:48 (16) :class:`int`
    :attr:`reserved1` 48:64 (16) :class:`int`
    ================= ========== ============

.. class:: rdma.IBA.SAMCMemberRecord

    Multicast member attribute (section 15.2.5.17)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x38
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    .. attribute:: COMPONENT_MASK = {'MGID':0, 'portGID':1, 'requesterGID':2, 'QKey':3, 'MLID':4, 'MTUSelector':5, 'MTU':6, 'TClass':7, 'PKey':8, 'rateSelector':9, 'rate':10, 'packetLifeTimeSelector':11, 'packetLifeTime':12, 'SL':13, 'flowLabel':14, 'hopLimit':15, 'scope':16, 'joinState':17, 'reserved1':18}

    ============================== ============= ======================
    Member                         Position      Type                  
    ============================== ============= ======================
    :attr:`MGID`                   0:128 (128)   :class:`~rdma.IBA.GID`
    :attr:`portGID`                128:256 (128) :class:`~rdma.IBA.GID`
    :attr:`requesterGID`           256:384 (128) :class:`~rdma.IBA.GID`
    :attr:`QKey`                   384:416 (32)  :class:`int`          
    :attr:`MLID`                   416:432 (16)  :class:`int`          
    :attr:`MTUSelector`            432:434 (2)   :class:`int`          
    :attr:`MTU`                    434:440 (6)   :class:`int`          
    :attr:`TClass`                 440:448 (8)   :class:`int`          
    :attr:`PKey`                   448:464 (16)  :class:`int`          
    :attr:`rateSelector`           464:466 (2)   :class:`int`          
    :attr:`rate`                   466:472 (6)   :class:`int`          
    :attr:`packetLifeTimeSelector` 472:474 (2)   :class:`int`          
    :attr:`packetLifeTime`         474:480 (6)   :class:`int`          
    :attr:`SL`                     480:484 (4)   :class:`int`          
    :attr:`flowLabel`              484:504 (20)  :class:`int`          
    :attr:`hopLimit`               504:512 (8)   :class:`int`          
    :attr:`scope`                  512:516 (4)   :class:`int`          
    :attr:`joinState`              516:520 (4)   :class:`int`          
    :attr:`reserved1`              520:544 (24)  :class:`int`          
    ============================== ============= ======================

.. class:: rdma.IBA.SAMultiPathRecord

    Request for multiple paths (section 15.2.5.20)

    .. attribute:: MAD_LENGTH = 40
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3a
    .. attribute:: MAD_SUBNADMGETMULTI = 0x14 # MAD_METHOD_GET_MULTI
    .. attribute:: COMPONENT_MASK = {'rawTraffic':0, 'reserved1':1, 'flowLabel':2, 'hopLimit':3, 'TClass':4, 'reversible':5, 'numbPath':6, 'PKey':7, 'reserved2':8, 'SL':9, 'MTUSelector':10, 'MTU':11, 'rateSelector':12, 'rate':13, 'packetLifeTimeSelector':14, 'packetLifeTime':15, 'reserved3':16, 'independenceSelector':17, 'reserved4':18, 'SGIDCount':19, 'DGIDCount':20, 'reserved5':21, 'reserved6':22, 'SDGID':23}

    ============================== ============= ======================
    Member                         Position      Type                  
    ============================== ============= ======================
    :attr:`rawTraffic`             0:1 (1)       :class:`int`          
    :attr:`reserved1`              1:4 (3)       :class:`int`          
    :attr:`flowLabel`              4:24 (20)     :class:`int`          
    :attr:`hopLimit`               24:32 (8)     :class:`int`          
    :attr:`TClass`                 32:40 (8)     :class:`int`          
    :attr:`reversible`             40:41 (1)     :class:`int`          
    :attr:`numbPath`               41:48 (7)     :class:`int`          
    :attr:`PKey`                   48:64 (16)    :class:`int`          
    :attr:`reserved2`              64:76 (12)    :class:`int`          
    :attr:`SL`                     76:80 (4)     :class:`int`          
    :attr:`MTUSelector`            80:82 (2)     :class:`int`          
    :attr:`MTU`                    82:88 (6)     :class:`int`          
    :attr:`rateSelector`           88:90 (2)     :class:`int`          
    :attr:`rate`                   90:96 (6)     :class:`int`          
    :attr:`packetLifeTimeSelector` 96:98 (2)     :class:`int`          
    :attr:`packetLifeTime`         98:104 (6)    :class:`int`          
    :attr:`reserved3`              104:112 (8)   :class:`int`          
    :attr:`independenceSelector`   112:114 (2)   :class:`int`          
    :attr:`reserved4`              114:120 (6)   :class:`int`          
    :attr:`SGIDCount`              120:128 (8)   :class:`int`          
    :attr:`DGIDCount`              128:136 (8)   :class:`int`          
    :attr:`reserved5`              136:160 (24)  :class:`int`          
    :attr:`reserved6`              160:192 (32)  :class:`int`          
    :attr:`SDGID`                  192:320 (128) :class:`~rdma.IBA.GID`
    ============================== ============= ======================

.. class:: rdma.IBA.SAMulticastForwardingTableRecord

    Container for MulticastForwardingTable entry (section 15.2.5.8)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved1':1, 'position':2, 'blockNum':3, 'reserved2':4, 'multicastForwardingTable.portMaskBlock':5}

    ================================ ============ ==============================================
    Member                           Position     Type                                          
    ================================ ============ ==============================================
    :attr:`LID`                      0:16 (16)    :class:`int`                                  
    :attr:`reserved1`                16:18 (2)    :class:`int`                                  
    :attr:`position`                 18:22 (4)    :class:`int`                                  
    :attr:`blockNum`                 22:32 (10)   :class:`int`                                  
    :attr:`reserved2`                32:64 (32)   :class:`int`                                  
    :attr:`multicastForwardingTable` 64:576 (512) :class:`~rdma.IBA.SMPMulticastForwardingTable`
    ================================ ============ ==============================================

.. class:: rdma.IBA.SANodeRecord

    Container for NodeInfo (section 15.2.5.2)

    .. attribute:: MAD_LENGTH = 108
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved1':1, 'nodeInfo.baseVersion':2, 'nodeInfo.classVersion':3, 'nodeInfo.nodeType':4, 'nodeInfo.numPorts':5, 'nodeInfo.systemImageGUID':6, 'nodeInfo.nodeGUID':7, 'nodeInfo.portGUID':8, 'nodeInfo.partitionCap':9, 'nodeInfo.deviceID':10, 'nodeInfo.revision':11, 'nodeInfo.localPortNum':12, 'nodeInfo.vendorID':13, 'nodeDescription.nodeString':14}

    ======================= ============= =====================================
    Member                  Position      Type                                 
    ======================= ============= =====================================
    :attr:`LID`             0:16 (16)     :class:`int`                         
    :attr:`reserved1`       16:32 (16)    :class:`int`                         
    :attr:`nodeInfo`        32:352 (320)  :class:`~rdma.IBA.SMPNodeInfo`       
    :attr:`nodeDescription` 352:864 (512) :class:`~rdma.IBA.SMPNodeDescription`
    ======================= ============= =====================================

.. class:: rdma.IBA.SAPKeyTableRecord

    Container for P_Key Table (section 15.2.5.11)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x33
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'portNum':2, 'reserved1':3, 'PKeyTable.PKeyBlock':4}

    ================= ============ ===============================
    Member            Position     Type                           
    ================= ============ ===============================
    :attr:`LID`       0:16 (16)    :class:`int`                   
    :attr:`blockNum`  16:32 (16)   :class:`int`                   
    :attr:`portNum`   32:40 (8)    :class:`int`                   
    :attr:`reserved1` 40:64 (24)   :class:`int`                   
    :attr:`PKeyTable` 64:576 (512) :class:`~rdma.IBA.SMPPKeyTable`
    ================= ============ ===============================

.. class:: rdma.IBA.SAPathRecord

    Information on paths through the subnet (section 15.2.5.16)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x35
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'reserved1':0, 'reserved2':1, 'DGID':2, 'SGID':3, 'DLID':4, 'SLID':5, 'rawTraffic':6, 'reserved3':7, 'flowLabel':8, 'hopLimit':9, 'TClass':10, 'reversible':11, 'numbPath':12, 'PKey':13, 'reserved4':14, 'SL':15, 'MTUSelector':16, 'MTU':17, 'rateSelector':18, 'rate':19, 'packetLifeTimeSelector':20, 'packetLifeTime':21, 'preference':22, 'reserved5':23, 'reserved6':24}

    ============================== ============= ======================
    Member                         Position      Type                  
    ============================== ============= ======================
    :attr:`reserved1`              0:32 (32)     :class:`int`          
    :attr:`reserved2`              32:64 (32)    :class:`int`          
    :attr:`DGID`                   64:192 (128)  :class:`~rdma.IBA.GID`
    :attr:`SGID`                   192:320 (128) :class:`~rdma.IBA.GID`
    :attr:`DLID`                   320:336 (16)  :class:`int`          
    :attr:`SLID`                   336:352 (16)  :class:`int`          
    :attr:`rawTraffic`             352:353 (1)   :class:`int`          
    :attr:`reserved3`              353:356 (3)   :class:`int`          
    :attr:`flowLabel`              356:376 (20)  :class:`int`          
    :attr:`hopLimit`               376:384 (8)   :class:`int`          
    :attr:`TClass`                 384:392 (8)   :class:`int`          
    :attr:`reversible`             392:393 (1)   :class:`int`          
    :attr:`numbPath`               393:400 (7)   :class:`int`          
    :attr:`PKey`                   400:416 (16)  :class:`int`          
    :attr:`reserved4`              416:428 (12)  :class:`int`          
    :attr:`SL`                     428:432 (4)   :class:`int`          
    :attr:`MTUSelector`            432:434 (2)   :class:`int`          
    :attr:`MTU`                    434:440 (6)   :class:`int`          
    :attr:`rateSelector`           440:442 (2)   :class:`int`          
    :attr:`rate`                   442:448 (6)   :class:`int`          
    :attr:`packetLifeTimeSelector` 448:450 (2)   :class:`int`          
    :attr:`packetLifeTime`         450:456 (6)   :class:`int`          
    :attr:`preference`             456:464 (8)   :class:`int`          
    :attr:`reserved5`              464:480 (16)  :class:`int`          
    :attr:`reserved6`              480:512 (32)  :class:`int`          
    ============================== ============= ======================

.. class:: rdma.IBA.SAPortInfoRecord

    Container for PortInfo (section 15.2.5.3)

    .. attribute:: MAD_LENGTH = 60
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'endportLID':0, 'portNum':1, 'reserved1':2, 'portInfo.MKey':3, 'portInfo.GIDPrefix':4, 'portInfo.LID':5, 'portInfo.masterSMLID':6, 'portInfo.capabilityMask':7, 'portInfo.diagCode':8, 'portInfo.MKeyLeasePeriod':9, 'portInfo.localPortNum':10, 'portInfo.linkWidthEnabled':11, 'portInfo.linkWidthSupported':12, 'portInfo.linkWidthActive':13, 'portInfo.linkSpeedSupported':14, 'portInfo.portState':15, 'portInfo.portPhysicalState':16, 'portInfo.linkDownDefaultState':17, 'portInfo.MKeyProtectBits':18, 'portInfo.reserved1':19, 'portInfo.LMC':20, 'portInfo.linkSpeedActive':21, 'portInfo.linkSpeedEnabled':22, 'portInfo.neighborMTU':23, 'portInfo.masterSMSL':24, 'portInfo.VLCap':25, 'portInfo.initType':26, 'portInfo.VLHighLimit':27, 'portInfo.VLArbitrationHighCap':28, 'portInfo.VLArbitrationLowCap':29, 'portInfo.initTypeReply':30, 'portInfo.MTUCap':31, 'portInfo.VLStallCount':32, 'portInfo.HOQLife':33, 'portInfo.operationalVLs':34, 'portInfo.partitionEnforcementInbound':35, 'portInfo.partitionEnforcementOutbound':36, 'portInfo.filterRawInbound':37, 'portInfo.filterRawOutbound':38, 'portInfo.MKeyViolations':39, 'portInfo.PKeyViolations':40, 'portInfo.QKeyViolations':41, 'portInfo.GUIDCap':42, 'portInfo.clientReregister':43, 'portInfo.reserved2':44, 'portInfo.subnetTimeOut':45, 'portInfo.reserved3':46, 'portInfo.respTimeValue':47, 'portInfo.localPhyErrors':48, 'portInfo.overrunErrors':49, 'portInfo.reserved4':50}

    ================== ============ ==============================
    Member             Position     Type                          
    ================== ============ ==============================
    :attr:`endportLID` 0:16 (16)    :class:`int`                  
    :attr:`portNum`    16:24 (8)    :class:`int`                  
    :attr:`reserved1`  24:32 (8)    :class:`int`                  
    :attr:`portInfo`   32:480 (448) :class:`~rdma.IBA.SMPPortInfo`
    ================== ============ ==============================

.. class:: rdma.IBA.SARandomForwardingTableRecord

    Container for RandomForwardingTable entry (section 15.2.5.7)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'blockNum':1, 'reserved1':2, 'randomForwardingTable.LIDPortBlock':3}

    ============================= ============ ===========================================
    Member                        Position     Type                                       
    ============================= ============ ===========================================
    :attr:`LID`                   0:16 (16)    :class:`int`                               
    :attr:`blockNum`              16:32 (16)   :class:`int`                               
    :attr:`reserved1`             32:64 (32)   :class:`int`                               
    :attr:`randomForwardingTable` 64:576 (512) :class:`~rdma.IBA.SMPRandomForwardingTable`
    ============================= ============ ===========================================

.. class:: rdma.IBA.SASLToVLMappingTableRecord

    Container for SLtoVLMappingTable entry (section 15.2.5.4)

    .. attribute:: MAD_LENGTH = 16
    .. attribute:: MAD_ATTRIBUTE_ID = 0x13
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'inputPortNum':1, 'outputPortNum':2, 'reserved1':3, 'SLToVLMappingTable.SLtoVL':4}

    ========================== =========== ========================================
    Member                     Position    Type                                    
    ========================== =========== ========================================
    :attr:`LID`                0:16 (16)   :class:`int`                            
    :attr:`inputPortNum`       16:24 (8)   :class:`int`                            
    :attr:`outputPortNum`      24:32 (8)   :class:`int`                            
    :attr:`reserved1`          32:64 (32)  :class:`int`                            
    :attr:`SLToVLMappingTable` 64:128 (64) :class:`~rdma.IBA.SMPSLToVLMappingTable`
    ========================== =========== ========================================

.. class:: rdma.IBA.SASMInfoRecord

    Container for SMInfo (section 15.2.5.10)

    .. attribute:: MAD_LENGTH = 28
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved1':1, 'SMInfo.GUID':2, 'SMInfo.SMKey':3, 'SMInfo.actCount':4, 'SMInfo.priority':5, 'SMInfo.SMState':6, 'SMInfo.reserved1':7}

    ================= ============ ============================
    Member            Position     Type                        
    ================= ============ ============================
    :attr:`LID`       0:16 (16)    :class:`int`                
    :attr:`reserved1` 16:32 (16)   :class:`int`                
    :attr:`SMInfo`    32:224 (192) :class:`~rdma.IBA.SMPSMInfo`
    ================= ============ ============================

.. class:: rdma.IBA.SAServiceAssociationRecord

    ServiceRecord ServiceName/ServiceKey association (section 15.2.5.15)

    .. attribute:: MAD_LENGTH = 80
    .. attribute:: MAD_ATTRIBUTE_ID = 0x3b
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'serviceKey':0, 'serviceName':1}

    =================== =========== ============================
    Member              Position    Type                        
    =================== =========== ============================
    :attr:`serviceKey`  0:128 (128) :class:`~rdma.IBA.GID`      
    :attr:`serviceName` 128:640 (8) [:class:`bytearray` (64)]*64
    =================== =========== ============================

.. class:: rdma.IBA.SAServiceRecord

    Information on advertised services (section 15.2.5.14)

    .. attribute:: MAD_LENGTH = 176
    .. attribute:: MAD_ATTRIBUTE_ID = 0x31
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMSET = 0x2 # MAD_METHOD_SET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: MAD_SUBNADMDELETE = 0x15 # MAD_METHOD_DELETE
    .. attribute:: COMPONENT_MASK = {'serviceID':0, 'serviceGID':1, 'servicePKey':2, 'reserved1':3, 'serviceLease':4, 'serviceKey':5, 'serviceName':6, 'serviceData8':7, 'serviceData16':8, 'serviceData32':9, 'serviceData64':10}

    ===================== ============== ============================
    Member                Position       Type                        
    ===================== ============== ============================
    :attr:`serviceID`     0:64 (64)      :class:`int`                
    :attr:`serviceGID`    64:192 (128)   :class:`~rdma.IBA.GID`      
    :attr:`servicePKey`   192:208 (16)   :class:`int`                
    :attr:`reserved1`     208:224 (16)   :class:`int`                
    :attr:`serviceLease`  224:256 (32)   :class:`int`                
    :attr:`serviceKey`    256:384 (128)  :class:`~rdma.IBA.GID`      
    :attr:`serviceName`   384:896 (8)    [:class:`bytearray` (64)]*64
    :attr:`serviceData8`  896:1024 (8)   [:class:`bytearray` (16)]*16
    :attr:`serviceData16` 1024:1152 (16) [:class:`int`]*8            
    :attr:`serviceData32` 1152:1280 (32) [:class:`int`]*4            
    :attr:`serviceData64` 1280:1408 (64) [:class:`int`]*2            
    ===================== ============== ============================

.. class:: rdma.IBA.SASwitchInfoRecord

    Container for SwitchInfo (section 15.2.5.5)

    .. attribute:: MAD_LENGTH = 24
    .. attribute:: MAD_ATTRIBUTE_ID = 0x14
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'reserved1':1, 'switchInfo.linearFDBCap':2, 'switchInfo.randomFDBCap':3, 'switchInfo.multicastFDBCap':4, 'switchInfo.linearFDBTop':5, 'switchInfo.defaultPort':6, 'switchInfo.defaultMulticastPrimaryPort':7, 'switchInfo.defaultMulticastNotPrimaryPort':8, 'switchInfo.lifeTimeValue':9, 'switchInfo.portStateChange':10, 'switchInfo.reserved1':11, 'switchInfo.optimizedSLtoVLMappingProgramming':12, 'switchInfo.LIDsPerPort':13, 'switchInfo.partitionEnforcementCap':14, 'switchInfo.inboundEnforcementCap':15, 'switchInfo.outboundEnforcementCap':16, 'switchInfo.filterRawInboundCap':17, 'switchInfo.filterRawOutboundCap':18, 'switchInfo.enhancedPort0':19, 'switchInfo.reserved2':20, 'switchInfo.reserved3':21}

    ================== ============ ================================
    Member             Position     Type                            
    ================== ============ ================================
    :attr:`LID`        0:16 (16)    :class:`int`                    
    :attr:`reserved1`  16:32 (16)   :class:`int`                    
    :attr:`switchInfo` 32:192 (160) :class:`~rdma.IBA.SMPSwitchInfo`
    ================== ============ ================================

.. class:: rdma.IBA.SATraceRecord

    Path trace information (section 15.2.5.19)

    .. attribute:: MAD_LENGTH = 48
    .. attribute:: MAD_ATTRIBUTE_ID = 0x39
    .. attribute:: MAD_SUBNADMGETTRACETABLE = 0x13 # MAD_METHOD_GET_TRACE_TABLE
    .. attribute:: COMPONENT_MASK = {'GIDPrefix':0, 'IDGeneration':1, 'reserved1':2, 'nodeType':3, 'nodeID':4, 'chassisID':5, 'entryPortID':6, 'exitPortID':7, 'entryPort':8, 'exitPort':9, 'reserved2':10}

    ==================== ============ ============
    Member               Position     Type        
    ==================== ============ ============
    :attr:`GIDPrefix`    0:64 (64)    :class:`int`
    :attr:`IDGeneration` 64:80 (16)   :class:`int`
    :attr:`reserved1`    80:88 (8)    :class:`int`
    :attr:`nodeType`     88:96 (8)    :class:`int`
    :attr:`nodeID`       96:160 (64)  :class:`int`
    :attr:`chassisID`    160:224 (64) :class:`int`
    :attr:`entryPortID`  224:288 (64) :class:`int`
    :attr:`exitPortID`   288:352 (64) :class:`int`
    :attr:`entryPort`    352:360 (8)  :class:`int`
    :attr:`exitPort`     360:368 (8)  :class:`int`
    :attr:`reserved2`    368:384 (16) :class:`int`
    ==================== ============ ============

.. class:: rdma.IBA.SAVLArbitrationTableRecord

    Container for VLArbitrationTable entry (section 15.2.5.9)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x36
    .. attribute:: MAD_SUBNADMGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_SUBNADMGETTABLE = 0x12 # MAD_METHOD_GET_TABLE
    .. attribute:: COMPONENT_MASK = {'LID':0, 'outputPortNum':1, 'blockNum':2, 'reserved1':3, 'VLArbitrationTable.VLWeightBlock':4}

    ========================== ============ ========================================
    Member                     Position     Type                                    
    ========================== ============ ========================================
    :attr:`LID`                0:16 (16)    :class:`int`                            
    :attr:`outputPortNum`      16:24 (8)    :class:`int`                            
    :attr:`blockNum`           24:32 (8)    :class:`int`                            
    :attr:`reserved1`          32:64 (32)   :class:`int`                            
    :attr:`VLArbitrationTable` 64:576 (512) :class:`~rdma.IBA.SMPVLArbitrationTable`
    ========================== ============ ========================================

Performance Management (16.1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.PMFormat

    An *aggregation* of: MADHeader

    Performance Management MAD Format (section 16.1.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x4
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ========================= =============== ========================
    Member                    Position        Type                    
    ========================= =============== ========================
    :attr:`baseVersion`       0:8 (8)         :class:`int`            
    :attr:`mgmtClass`         8:16 (8)        :class:`int`            
    :attr:`classVersion`      16:24 (8)       :class:`int`            
    :attr:`method`            24:32 (8)       :class:`int`            
    :attr:`status`            32:48 (16)      :class:`int`            
    :attr:`classSpecific`     48:64 (16)      :class:`int`            
    :attr:`transactionID`     64:128 (64)     :class:`int`            
    :attr:`attributeID`       128:144 (16)    :class:`int`            
    :attr:`reserved1`         144:160 (16)    :class:`int`            
    :attr:`attributeModifier` 160:192 (32)    :class:`int`            
    :attr:`reserved2`         192:512 (320)   :class:`bytearray` (40) 
    :attr:`data`              512:2048 (1536) :class:`bytearray` (192)
    ========================= =============== ========================

.. class:: rdma.IBA.PMPortCounters

    Port Basic Performance and Error Counters (section 16.1.3.5)

    .. attribute:: MAD_LENGTH = 44
    .. attribute:: MAD_ATTRIBUTE_ID = 0x12
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ==================================== ============ ============
    Member                               Position     Type        
    ==================================== ============ ============
    :attr:`reserved1`                    0:8 (8)      :class:`int`
    :attr:`portSelect`                   8:16 (8)     :class:`int`
    :attr:`counterSelect`                16:32 (16)   :class:`int`
    :attr:`symbolErrorCounter`           32:48 (16)   :class:`int`
    :attr:`linkErrorRecoveryCounter`     48:56 (8)    :class:`int`
    :attr:`linkDownedCounter`            56:64 (8)    :class:`int`
    :attr:`portRcvErrors`                64:80 (16)   :class:`int`
    :attr:`portRcvRemotePhysicalErrors`  80:96 (16)   :class:`int`
    :attr:`portRcvSwitchRelayErrors`     96:112 (16)  :class:`int`
    :attr:`portXmitDiscards`             112:128 (16) :class:`int`
    :attr:`portXmitConstraintErrors`     128:136 (8)  :class:`int`
    :attr:`portRcvConstraintErrors`      136:144 (8)  :class:`int`
    :attr:`counterSelect2`               144:152 (8)  :class:`int`
    :attr:`localLinkIntegrityErrors`     152:156 (4)  :class:`int`
    :attr:`excessiveBufferOverrunErrors` 156:160 (4)  :class:`int`
    :attr:`reserved2`                    160:176 (16) :class:`int`
    :attr:`VL15Dropped`                  176:192 (16) :class:`int`
    :attr:`portXmitData`                 192:224 (32) :class:`int`
    :attr:`portRcvData`                  224:256 (32) :class:`int`
    :attr:`portXmitPkts`                 256:288 (32) :class:`int`
    :attr:`portRcvPkts`                  288:320 (32) :class:`int`
    :attr:`portXmitWait`                 320:352 (32) :class:`int`
    ==================================== ============ ============

.. class:: rdma.IBA.PMPortCountersExt

    Extended Port Counters (section 16.1.4.11)

    .. attribute:: MAD_LENGTH = 72
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1d
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ============================= ============ ============
    Member                        Position     Type        
    ============================= ============ ============
    :attr:`reserved1`             0:8 (8)      :class:`int`
    :attr:`portSelect`            8:16 (8)     :class:`int`
    :attr:`counterSelect`         16:32 (16)   :class:`int`
    :attr:`reserved2`             32:64 (32)   :class:`int`
    :attr:`portXmitData`          64:128 (64)  :class:`int`
    :attr:`portRcvData`           128:192 (64) :class:`int`
    :attr:`portXmitPkts`          192:256 (64) :class:`int`
    :attr:`portRcvPkts`           256:320 (64) :class:`int`
    :attr:`portUnicastXmitPkts`   320:384 (64) :class:`int`
    :attr:`portUnicastRcvPkts`    384:448 (64) :class:`int`
    :attr:`portMulticastXmitPkts` 448:512 (64) :class:`int`
    :attr:`portMulticastRcvPkts`  512:576 (64) :class:`int`
    ============================= ============ ============

.. class:: rdma.IBA.PMPortFlowCtlCounters

    Port Flow Control Counters (section 16.1.4.4)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x18
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ======================== ========== ============
    Member                   Position   Type        
    ======================== ========== ============
    :attr:`reserved1`        0:8 (8)    :class:`int`
    :attr:`portSelect`       8:16 (8)   :class:`int`
    :attr:`counterSelect`    16:32 (16) :class:`int`
    :attr:`portXmitFlowPkts` 32:64 (32) :class:`int`
    :attr:`portRcvFlowPkts`  64:96 (32) :class:`int`
    ======================== ========== ============

.. class:: rdma.IBA.PMPortOpRcvCounters

    Port Receive Counters per Op Code (section 16.1.4.3)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x17
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== ========== ============
    Member                Position   Type        
    ===================== ========== ============
    :attr:`opCode`        0:8 (8)    :class:`int`
    :attr:`portSelect`    8:16 (8)   :class:`int`
    :attr:`counterSelect` 16:32 (16) :class:`int`
    :attr:`portOpRcvPkts` 32:64 (32) :class:`int`
    :attr:`portOpRcvData` 64:96 (32) :class:`int`
    ===================== ========== ============

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
    :attr:`portSelect`                8:16 (8)     :class:`int`
    :attr:`counterSelect`             16:32 (16)   :class:`int`
    :attr:`portLocalPhysicalErrors`   32:48 (16)   :class:`int`
    :attr:`portMalformedPacketErrors` 48:64 (16)   :class:`int`
    :attr:`portBufferOverrunErrors`   64:80 (16)   :class:`int`
    :attr:`portDLIDMappingErrors`     80:96 (16)   :class:`int`
    :attr:`portVLMappingErrors`       96:112 (16)  :class:`int`
    :attr:`portLoopingErrors`         112:128 (16) :class:`int`
    ================================= ============ ============

.. class:: rdma.IBA.PMPortSamplesCtl

    Port Performance Data Sampling Control (section 16.1.3.2)

    .. attribute:: MAD_LENGTH = 192
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ============================= ============== ========================
    Member                        Position       Type                    
    ============================= ============== ========================
    :attr:`opCode`                0:8 (8)        :class:`int`            
    :attr:`portSelect`            8:16 (8)       :class:`int`            
    :attr:`tick`                  16:24 (8)      :class:`int`            
    :attr:`reserved1`             24:29 (5)      :class:`int`            
    :attr:`counterWidth`          29:32 (3)      :class:`int`            
    :attr:`reserved2`             32:34 (2)      :class:`int`            
    :attr:`counterMask0`          34:37 (3)      :class:`int`            
    :attr:`counterMask1`          37:40 (3)      :class:`int`            
    :attr:`counterMask2`          40:43 (3)      :class:`int`            
    :attr:`counterMask3`          43:46 (3)      :class:`int`            
    :attr:`counterMask4`          46:49 (3)      :class:`int`            
    :attr:`counterMask5`          49:52 (3)      :class:`int`            
    :attr:`counterMask6`          52:55 (3)      :class:`int`            
    :attr:`counterMask7`          55:58 (3)      :class:`int`            
    :attr:`counterMask8`          58:61 (3)      :class:`int`            
    :attr:`counterMask9`          61:64 (3)      :class:`int`            
    :attr:`reserved3`             64:65 (1)      :class:`int`            
    :attr:`counterMask10`         65:68 (3)      :class:`int`            
    :attr:`counterMask11`         68:71 (3)      :class:`int`            
    :attr:`counterMask12`         71:74 (3)      :class:`int`            
    :attr:`counterMask13`         74:77 (3)      :class:`int`            
    :attr:`counterMask14`         77:80 (3)      :class:`int`            
    :attr:`sampleMechanisms`      80:88 (8)      :class:`int`            
    :attr:`reserved4`             88:94 (6)      :class:`int`            
    :attr:`sampleStatus`          94:96 (2)      :class:`int`            
    :attr:`optionMask`            96:160 (64)    :class:`int`            
    :attr:`vendorMask`            160:224 (64)   :class:`int`            
    :attr:`sampleStart`           224:256 (32)   :class:`int`            
    :attr:`sampleInterval`        256:288 (32)   :class:`int`            
    :attr:`tag`                   288:304 (16)   :class:`int`            
    :attr:`counterSelect0`        304:320 (16)   :class:`int`            
    :attr:`counterSelect1`        320:336 (16)   :class:`int`            
    :attr:`counterSelect2`        336:352 (16)   :class:`int`            
    :attr:`counterSelect3`        352:368 (16)   :class:`int`            
    :attr:`counterSelect4`        368:384 (16)   :class:`int`            
    :attr:`counterSelect5`        384:400 (16)   :class:`int`            
    :attr:`counterSelect6`        400:416 (16)   :class:`int`            
    :attr:`counterSelect7`        416:432 (16)   :class:`int`            
    :attr:`counterSelect8`        432:448 (16)   :class:`int`            
    :attr:`counterSelect9`        448:464 (16)   :class:`int`            
    :attr:`counterSelect10`       464:480 (16)   :class:`int`            
    :attr:`counterSelect11`       480:496 (16)   :class:`int`            
    :attr:`counterSelect12`       496:512 (16)   :class:`int`            
    :attr:`counterSelect13`       512:528 (16)   :class:`int`            
    :attr:`counterSelect14`       528:544 (16)   :class:`int`            
    :attr:`reserved5`             544:576 (32)   :class:`int`            
    :attr:`samplesOnlyOptionMask` 576:640 (64)   :class:`int`            
    :attr:`reserved6`             640:1536 (896) :class:`bytearray` (112)
    ============================= ============== ========================

.. class:: rdma.IBA.PMPortSamplesRes

    Port Performance Data Sampling Results (section 16.1.3.4)

    .. attribute:: MAD_LENGTH = 64
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET

    ==================== =========== =================
    Member               Position    Type             
    ==================== =========== =================
    :attr:`tag`          0:16 (16)   :class:`int`     
    :attr:`reserved1`    16:30 (14)  :class:`int`     
    :attr:`sampleStatus` 30:32 (2)   :class:`int`     
    :attr:`counter`      32:512 (32) [:class:`int`]*15
    ==================== =========== =================

.. class:: rdma.IBA.PMPortSamplesResExt

    Extended Port Samples Result (section 16.1.4.10)

    .. attribute:: MAD_LENGTH = 128
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1e
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== ============ =================
    Member                Position     Type             
    ===================== ============ =================
    :attr:`tag`           0:16 (16)    :class:`int`     
    :attr:`reserved1`     16:30 (14)   :class:`int`     
    :attr:`sampleStatus`  30:32 (2)    :class:`int`     
    :attr:`extendedWidth` 32:34 (2)    :class:`int`     
    :attr:`reserved2`     34:64 (30)   :class:`int`     
    :attr:`counter`       64:1024 (64) [:class:`int`]*15
    ===================== ============ =================

.. class:: rdma.IBA.PMPortVLOpData

    Port Kilobytes Received per Op Code per VL (section 16.1.4.6)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1a
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== =========== =================
    Member                Position    Type             
    ===================== =========== =================
    :attr:`opCode`        0:8 (8)     :class:`int`     
    :attr:`portSelect`    8:16 (8)    :class:`int`     
    :attr:`counterSelect` 16:32 (16)  :class:`int`     
    :attr:`portVLOpData`  32:544 (32) [:class:`int`]*16
    ===================== =========== =================

.. class:: rdma.IBA.PMPortVLOpPackets

    Port Packets Received per Op Code per VL (section 16.1.4.5)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x19
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ======================= =========== =================
    Member                  Position    Type             
    ======================= =========== =================
    :attr:`opCode`          0:8 (8)     :class:`int`     
    :attr:`portSelect`      8:16 (8)    :class:`int`     
    :attr:`counterSelect`   16:32 (16)  :class:`int`     
    :attr:`portVLOpPackets` 32:288 (16) [:class:`int`]*16
    ======================= =========== =================

.. class:: rdma.IBA.PMPortVLXmitFlowCtlUpdateErrors

    Port Flow Control update errors per VL (section 16.1.4.7)

    .. attribute:: MAD_LENGTH = 8
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1b
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================================== ========== =================
    Member                                Position   Type             
    ===================================== ========== =================
    :attr:`reserved1`                     0:8 (8)    :class:`int`     
    :attr:`portSelect`                    8:16 (8)   :class:`int`     
    :attr:`counterSelect`                 16:32 (16) :class:`int`     
    :attr:`portVLXmitFlowCtlUpdateErrors` 32:64 (2)  [:class:`int`]*16
    ===================================== ========== =================

.. class:: rdma.IBA.PMPortVLXmitWaitCounters

    Port Ticks Waiting to Transmit Counters per VL (section 16.1.4.8)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x1c
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ====================== =========== =================
    Member                 Position    Type             
    ====================== =========== =================
    :attr:`reserved1`      0:8 (8)     :class:`int`     
    :attr:`portSelect`     8:16 (8)    :class:`int`     
    :attr:`counterSelect`  16:32 (16)  :class:`int`     
    :attr:`portVLXmitWait` 32:288 (16) [:class:`int`]*16
    ====================== =========== =================

.. class:: rdma.IBA.PMPortXmitDiscardDetails

    Port Transmit Discard Counters (section 16.1.4.2)

    .. attribute:: MAD_LENGTH = 12
    .. attribute:: MAD_ATTRIBUTE_ID = 0x16
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    =================================== ========== ============
    Member                              Position   Type        
    =================================== ========== ============
    :attr:`reserved1`                   0:8 (8)    :class:`int`
    :attr:`portSelect`                  8:16 (8)   :class:`int`
    :attr:`counterSelect`               16:32 (16) :class:`int`
    :attr:`portInactiveDiscards`        32:48 (16) :class:`int`
    :attr:`portNeighborMTUDiscards`     48:64 (16) :class:`int`
    :attr:`portSwLifetimeLimitDiscards` 64:80 (16) :class:`int`
    :attr:`portSwHOQLimitDiscards`      80:96 (16) :class:`int`
    =================================== ========== ============

.. class:: rdma.IBA.PMSwPortVLCongestion

    Switch Port Congestion per VL (section 16.1.4.9)

    .. attribute:: MAD_LENGTH = 36
    .. attribute:: MAD_ATTRIBUTE_ID = 0x30
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ========================== =========== =================
    Member                     Position    Type             
    ========================== =========== =================
    :attr:`reserved1`          0:8 (8)     :class:`int`     
    :attr:`portSelect`         8:16 (8)    :class:`int`     
    :attr:`counterSelect`      16:32 (16)  :class:`int`     
    :attr:`swPortVLCongestion` 32:288 (16) [:class:`int`]*16
    ========================== =========== =================

.. class:: rdma.IBA.PMPortRcvDataSL

    Receive SL Port Counters (section A13.6.5)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x37
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ===================== =========== =================
    Member                Position    Type             
    ===================== =========== =================
    :attr:`reserved1`     0:8 (8)     :class:`int`     
    :attr:`portSelect`    8:16 (8)    :class:`int`     
    :attr:`counterSelect` 16:32 (16)  :class:`int`     
    :attr:`portRcvDataSL` 64:576 (32) [:class:`int`]*16
    ===================== =========== =================

.. class:: rdma.IBA.PMPortXmitDataSL

    Transmit SL Port Counters (section A13.6.5)

    .. attribute:: MAD_LENGTH = 68
    .. attribute:: MAD_ATTRIBUTE_ID = 0x36
    .. attribute:: MAD_PERFORMANCEGET = 0x1 # MAD_METHOD_GET
    .. attribute:: MAD_PERFORMANCESET = 0x2 # MAD_METHOD_SET

    ====================== =========== =================
    Member                 Position    Type             
    ====================== =========== =================
    :attr:`reserved1`      0:8 (8)     :class:`int`     
    :attr:`portSelect`     8:16 (8)    :class:`int`     
    :attr:`counterSelect`  16:32 (16)  :class:`int`     
    :attr:`portXmitDataSL` 64:576 (32) [:class:`int`]*16
    ====================== =========== =================

Device Management (16.3)
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: rdma.IBA.DMDiagCode

    Vendor-Specific Device Diagnostic Information (section 16.3.3.10)

    .. attribute:: MAD_LENGTH = 4
    .. attribute:: MAD_ATTRIBUTE_ID = 0x24
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`diagCode`  0:16 (16)  :class:`int`
    :attr:`reserved1` 16:32 (16) :class:`int`
    ================= ========== ============

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

    An *aggregation* of: MADHeader

    Device Management MAD Format (section 16.3.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x6
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ========================= =============== ========================
    Member                    Position        Type                    
    ========================= =============== ========================
    :attr:`baseVersion`       0:8 (8)         :class:`int`            
    :attr:`mgmtClass`         8:16 (8)        :class:`int`            
    :attr:`classVersion`      16:24 (8)       :class:`int`            
    :attr:`method`            24:32 (8)       :class:`int`            
    :attr:`status`            32:48 (16)      :class:`int`            
    :attr:`classSpecific`     48:64 (16)      :class:`int`            
    :attr:`transactionID`     64:128 (64)     :class:`int`            
    :attr:`attributeID`       128:144 (16)    :class:`int`            
    :attr:`reserved1`         144:160 (16)    :class:`int`            
    :attr:`attributeModifier` 160:192 (32)    :class:`int`            
    :attr:`reserved2`         192:512 (320)   :class:`bytearray` (40) 
    :attr:`data`              512:2048 (1536) :class:`bytearray` (192)
    ========================= =============== ========================

.. class:: rdma.IBA.DMIOControllerProfile

    I/O Controller Profile Information (section 16.3.3.4)

    .. attribute:: MAD_LENGTH = 128
    .. attribute:: MAD_ATTRIBUTE_ID = 0x11
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ================================ ============ ============================
    Member                           Position     Type                        
    ================================ ============ ============================
    :attr:`GUID`                     0:64 (64)    :class:`~rdma.IBA.GUID`     
    :attr:`vendorID`                 64:88 (24)   :class:`int`                
    :attr:`reserved1`                88:96 (8)    :class:`int`                
    :attr:`deviceID`                 96:128 (32)  :class:`int`                
    :attr:`deviceVersion`            128:144 (16) :class:`int`                
    :attr:`reserved2`                144:160 (16) :class:`int`                
    :attr:`subsystemVendorID`        160:184 (24) :class:`int`                
    :attr:`reserved3`                184:192 (8)  :class:`int`                
    :attr:`subsystemID`              192:224 (32) :class:`int`                
    :attr:`IOClass`                  224:240 (16) :class:`int`                
    :attr:`IOSubclass`               240:256 (16) :class:`int`                
    :attr:`protocol`                 256:272 (16) :class:`int`                
    :attr:`protocolVersion`          272:288 (16) :class:`int`                
    :attr:`reserved4`                288:304 (16) :class:`int`                
    :attr:`reserved5`                304:320 (16) :class:`int`                
    :attr:`sendMessageDepth`         320:336 (16) :class:`int`                
    :attr:`reserved6`                336:344 (8)  :class:`int`                
    :attr:`RDMAReadDepth`            344:352 (8)  :class:`int`                
    :attr:`sendMessageSize`          352:384 (32) :class:`int`                
    :attr:`RDMATransferSize`         384:416 (32) :class:`int`                
    :attr:`controllerOperationsMask` 416:424 (8)  :class:`int`                
    :attr:`reserved7`                424:432 (8)  :class:`int`                
    :attr:`serviceEntries`           432:440 (8)  :class:`int`                
    :attr:`reserved8`                440:448 (8)  :class:`int`                
    :attr:`reserved9`                448:512 (64) :class:`int`                
    :attr:`IDString`                 512:1024 (8) [:class:`bytearray` (64)]*64
    ================================ ============ ============================

.. class:: rdma.IBA.DMIOUnitInfo

    List of all I/O Controllers in a I/O Unit (section 16.3.3.3)

    .. attribute:: MAD_LENGTH = 132
    .. attribute:: MAD_ATTRIBUTE_ID = 0x10
    .. attribute:: MAD_DEVMGTGET = 0x1 # MAD_METHOD_GET

    ====================== ============== ========================
    Member                 Position       Type                    
    ====================== ============== ========================
    :attr:`changeID`       0:16 (16)      :class:`int`            
    :attr:`maxControllers` 16:24 (8)      :class:`int`            
    :attr:`reserved1`      24:30 (6)      :class:`int`            
    :attr:`diagDeviceID`   30:31 (1)      :class:`int`            
    :attr:`optionROM`      31:32 (1)      :class:`int`            
    :attr:`controllerList` 32:1056 (1024) :class:`bytearray` (128)
    ====================== ============== ========================

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

    =================== ============ ============================
    Member              Position     Type                        
    =================== ============ ============================
    :attr:`serviceName` 0:320 (8)    [:class:`bytearray` (40)]*40
    :attr:`serviceID`   320:384 (64) :class:`int`                
    =================== ============ ============================

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

    An *aggregation* of: MADHeader

    SNMP Tunneling MAD Format (section 16.4.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x8
    .. attribute:: MAD_CLASS_VERSION = 0x1

    ========================= =============== ========================
    Member                    Position        Type                    
    ========================= =============== ========================
    :attr:`baseVersion`       0:8 (8)         :class:`int`            
    :attr:`mgmtClass`         8:16 (8)        :class:`int`            
    :attr:`classVersion`      16:24 (8)       :class:`int`            
    :attr:`method`            24:32 (8)       :class:`int`            
    :attr:`status`            32:48 (16)      :class:`int`            
    :attr:`classSpecific`     48:64 (16)      :class:`int`            
    :attr:`transactionID`     64:128 (64)     :class:`int`            
    :attr:`attributeID`       128:144 (16)    :class:`int`            
    :attr:`reserved1`         144:160 (16)    :class:`int`            
    :attr:`attributeModifier` 160:192 (32)    :class:`int`            
    :attr:`reserved2`         192:448 (256)   :class:`bytearray` (32) 
    :attr:`RAddress`          448:480 (32)    :class:`int`            
    :attr:`payloadLength`     480:488 (8)     :class:`int`            
    :attr:`segmentNumber`     488:496 (8)     :class:`int`            
    :attr:`sourceLID`         496:512 (16)    :class:`int`            
    :attr:`data`              512:2048 (1536) :class:`bytearray` (192)
    ========================= =============== ========================

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

    An *aggregation* of: MADHeader

    Request for Communication (section 16.7.1)

    .. attribute:: MAD_LENGTH = 256
    .. attribute:: MAD_CLASS = 0x7
    .. attribute:: MAD_CLASS_VERSION = 0x2

    ========================= =============== ========================
    Member                    Position        Type                    
    ========================= =============== ========================
    :attr:`baseVersion`       0:8 (8)         :class:`int`            
    :attr:`mgmtClass`         8:16 (8)        :class:`int`            
    :attr:`classVersion`      16:24 (8)       :class:`int`            
    :attr:`method`            24:32 (8)       :class:`int`            
    :attr:`status`            32:48 (16)      :class:`int`            
    :attr:`classSpecific`     48:64 (16)      :class:`int`            
    :attr:`transactionID`     64:128 (64)     :class:`int`            
    :attr:`attributeID`       128:144 (16)    :class:`int`            
    :attr:`reserved1`         144:160 (16)    :class:`int`            
    :attr:`attributeModifier` 160:192 (32)    :class:`int`            
    :attr:`data`              192:2048 (1856) :class:`bytearray` (232)
    ========================= =============== ========================

.. class:: rdma.IBA.HdrAETH

    ACK Extended Transport Header (section 9.3.5)

    .. attribute:: MAD_LENGTH = 4

    ================ ========= ============
    Member           Position  Type        
    ================ ========= ============
    :attr:`syndrome` 0:8 (8)   :class:`int`
    :attr:`MSN`      8:32 (24) :class:`int`
    ================ ========= ============

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

    ================ ============ ============
    Member           Position     Type        
    ================ ============ ============
    :attr:`VA`       0:64 (64)    :class:`int`
    :attr:`RKey`     64:96 (32)   :class:`int`
    :attr:`swapData` 96:160 (64)  :class:`int`
    :attr:`cmpData`  160:224 (64) :class:`int`
    ================ ============ ============

.. class:: rdma.IBA.HdrBTH

    Base Transport Header (section 9.2)

    .. attribute:: MAD_LENGTH = 12

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`service`   0:3 (3)    :class:`int`
    :attr:`function`  3:8 (5)    :class:`int`
    :attr:`SE`        8:9 (1)    :class:`int`
    :attr:`migReq`    9:10 (1)   :class:`int`
    :attr:`padCnt`    10:12 (2)  :class:`int`
    :attr:`TVer`      12:16 (4)  :class:`int`
    :attr:`PKey`      16:32 (16) :class:`int`
    :attr:`reserved1` 32:40 (8)  :class:`int`
    :attr:`destQP`    40:64 (24) :class:`int`
    :attr:`ackReq`    64:65 (1)  :class:`int`
    :attr:`reserved2` 65:72 (7)  :class:`int`
    :attr:`PSN`       72:96 (24) :class:`int`
    ================= ========== ============

.. class:: rdma.IBA.HdrDETH

    Datagram Extended Transport Header (section 9.3.2)

    .. attribute:: MAD_LENGTH = 8

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`QKey`      0:32 (32)  :class:`int`
    :attr:`reserved1` 32:40 (8)  :class:`int`
    :attr:`srcQP`     40:64 (24) :class:`int`
    ================= ========== ============

.. class:: rdma.IBA.HdrFlowControl

    Flow Control Packet (section 7.9.4)

    .. attribute:: MAD_LENGTH = 4

    ============= ========== ============
    Member        Position   Type        
    ============= ========== ============
    :attr:`op`    0:4 (4)    :class:`int`
    :attr:`FCTBS` 4:16 (12)  :class:`int`
    :attr:`VL`    16:20 (4)  :class:`int`
    :attr:`FCCL`  20:32 (12) :class:`int`
    ============= ========== ============

.. class:: rdma.IBA.HdrGRH

    Global Route Header (section 8.3)

    .. attribute:: MAD_LENGTH = 40

    ================= ============= ======================
    Member            Position      Type                  
    ================= ============= ======================
    :attr:`IPVer`     0:4 (4)       :class:`int`          
    :attr:`TClass`    4:12 (8)      :class:`int`          
    :attr:`flowLabel` 12:32 (20)    :class:`int`          
    :attr:`payLen`    32:48 (16)    :class:`int`          
    :attr:`nxtHdr`    48:56 (8)     :class:`int`          
    :attr:`hopLmt`    56:64 (8)     :class:`int`          
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

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`VL`        0:4 (4)    :class:`int`
    :attr:`LVer`      4:8 (4)    :class:`int`
    :attr:`SL`        8:12 (4)   :class:`int`
    :attr:`reserved1` 12:14 (2)  :class:`int`
    :attr:`LNH`       14:16 (2)  :class:`int`
    :attr:`DLID`      16:32 (16) :class:`int`
    :attr:`reserved2` 32:37 (5)  :class:`int`
    :attr:`pktLen`    37:48 (11) :class:`int`
    :attr:`SLID`      48:64 (16) :class:`int`
    ================= ========== ============

.. class:: rdma.IBA.HdrRDETH

    Reliable Datagram Extended Transport Header (section 9.3.1)

    .. attribute:: MAD_LENGTH = 4

    ================= ========= ============
    Member            Position  Type        
    ================= ========= ============
    :attr:`reserved1` 0:8 (8)   :class:`int`
    :attr:`EEC`       8:32 (24) :class:`int`
    ================= ========= ============

.. class:: rdma.IBA.HdrRETH

    RDMA Extended Transport Header (section 9.3.3)

    .. attribute:: MAD_LENGTH = 16

    ============== =========== ============
    Member         Position    Type        
    ============== =========== ============
    :attr:`VA`     0:64 (64)   :class:`int`
    :attr:`RKey`   64:96 (32)  :class:`int`
    :attr:`DMALen` 96:128 (32) :class:`int`
    ============== =========== ============

.. class:: rdma.IBA.HdrRWH

    Raw Header (section 5.3)

    .. attribute:: MAD_LENGTH = 4

    ================= ========== ============
    Member            Position   Type        
    ================= ========== ============
    :attr:`reserved1` 0:16 (16)  :class:`int`
    :attr:`etherType` 16:32 (16) :class:`int`
    ================= ========== ============

