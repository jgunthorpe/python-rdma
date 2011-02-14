import sys;
import rdma;
import rdma.path;
import rdma.madtransactor;
import rdma.IBA as IBA;

class SATransactor(rdma.madtransactor.MADTransactor):
    """This class wrappers another MADTransactor and transparently changes SMP
    queries into corrisponding SA queries. It is useful to write applications
    that need to support both methods.

    There are some limitations due to how the SA interface is
    defined. :class:`~rdma.IBA.SMPPortInfo` requires the port number, which is
    often 0. This requires extra work unless the node type is known since the
    SA does not support the same port 0 semantics. Generally using
    `ninf.localPortNum` as the attributeModifier works around this.

    When using the async interface it is not possible to use a
    :class:`~rdma.path.IBDRPath` since that requires multiple MADs to resolve
    the DR path to a LID through the SA.

    The class will collect and cache information in the path to try and work
    around some of these issues.

    It is also a context manager that wrappers the *parent*'s :meth:`close`."""

    def __init__(self,parent):
        """*parent* is the :class:`~rdma.madtransactor.MADTransactor` we are
        wrappering."""
        self._parent = parent;
        self.end_port = parent.end_port;

    def get_path_lid(self,path):
        """Resolve *path* to a LID. This is only does something if *path*
        is directed route."""
        if not isinstance(path,rdma.path.IBDRPath):
            return path.DLID;

        if path.drDLID != IBA.LID_PERMISSIVE:
            return path.drDLID;

        # FIXME: What to do in async mode?
        # FIXME: Use the SA for this!
        try:
            return path._cached_resolved_dlid;
        except AttributeError:
            pass;

        start_lid = path.DLID;
        if start_lid == IBA.LID_PERMISSIVE:
            start_lid = self.end_port.lid;

        if len(path.drPath) > 1:
            assert(self._parent.is_async == False);

        # Use the SA to resolve the DR path to a LID.
        req = IBA.ComponentMask(IBA.SALinkRecord());
        first = True;
        for I in path.drPath[1:]:
            req.fromLID = start_lid;
            if not first:
                req.fromPort = ord(I);
            first = False;
            start_lid = self._parent.SubnAdmGet(req).toLID;
        path._cached_resolved_dlid = start_lid;
        return start_lid;

    def _get_new_TID(self):
        return self._parent._get_new_TID();

    def _doMAD(self,fmt,payload,path,attributeModifier,method,completer=None):
        return self._parent._doMAD(fmt,payload,path,attributeModifier,method,
                                   completer);

    def _sa_error(self,rfmt,class_code):
        """IMHO it is an error for the SA to return NO_RECORDS for a valid
        query - just because it has no programmed records for that position.
        But opensm does, so we handle it by returning 0 for the record
        request. In the instance valid means 'within the bounds set by the
        other records'. In general though if you hit this you should probably
        be using a :meth:`SubnAdmGetTable` anyhow...."""
        if class_code == IBA.MAD_STATUS_SA_NO_RECORDS:
            return IBA.ATTR_TO_STRUCT[self.req_fmt.__class__,
                                      self.req_fmt.attributeID]();

    def _finish_port_info_attr0(self,rpayload):
        if len(rpayload) == 0:
            raise rdma.MADError(req=self.req_fmt,path=self.req_path,
                                rep=self.reply_fmt,
                                msg="Empty SAPortInfoRecord");

        for I in rpayload:
            if I.portNum == 0:
                return I.portInfo;
        return rpayload[0].portInfo;

    def _finish_nodedesc(self,rpayload):
        self.req_path._cached_node_type = rpayload.nodeInfo.nodeType;
        return rpayload.nodeDescription;
    def _finish_nodeinfo(self,rpayload):
        self.req_path._cached_node_type = rpayload.nodeInfo.nodeType;
        return rpayload.nodeInfo;

    def SubnGet(self,payload,path,attributeModifier=0):
        ID = payload.MAD_ATTRIBUTE_ID;
        meth = payload.MAD_SUBNGET;
        if ID == IBA.SMPGUIDInfo.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SAGUIDInfoRecord());
            req.LID = self.get_path_lid(path);
            req.blockNum = attributeModifier;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     lambda x:x.GUIDInfo);
        if ID == IBA.SMPLinearForwardingTable.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SALinearForwardingTableRecord());
            req.LID = self.get_path_lid(path);
            req.blockNum = attributeModifier;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     (lambda x:x.linearForwardingTable,
                                      self._sa_error));
        if ID == IBA.SMPMulticastForwardingTable.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SAMulticastForwardingTableRecord());
            req.LID = self.get_path_lid(path);
            req.blockNum = attributeModifier & ((1<<9)-1);
            req.position = (attributeModifier >> 12) & 0xF;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     (lambda x:x.multicastForwardingTable,
                                      self._sa_error));
        if ID == IBA.SMPNodeDescription.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SANodeRecord());
            req.LID = self.get_path_lid(path);
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     self._finish_nodedesc);
        if ID == IBA.SMPNodeInfo.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SANodeRecord());
            req.LID = self.get_path_lid(path);
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     self._finish_nodeinfo);

        if ID == IBA.SMPPKeyTable.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SAPKeyTableRecord());
            req.LID = self.get_path_lid(path);
            nt = getattr(path,"_cached_node_type",None);
            if nt is None or nt == IBA.NODE_SWITCH:
                req.portNum = attributeModifier >> 16;
            req.blockNum = attributeModifier & 0xFFFF;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     (lambda x:x.PKeyTable,
                                      self._sa_error));

        if ID == IBA.SMPPortInfo.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SAPortInfoRecord());
            req.endportLID = self.get_path_lid(path);
            if (attributeModifier == 0 and
                getattr(path,"_cached_node_type",None) == None):
                # This can mean 'whatever port' or it can mean 'switch port 0'
                # If we don't know the node type then do a get table and
                # figure it out.
                return self._subn_adm_do(req,self.end_port.sa_path,0,
                                         req.MAD_SUBNADMGETTABLE,
                                         self._finish_port_info_attr0);

            req.portNum = attributeModifier;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     lambda x:x.portInfo);
        if ID == IBA.SMPSLToVLMappingTable.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SASLToVLMappingTableRecord());
            req.LID = self.get_path_lid(path);
            req.inputPortNum = (attributeModifier >> 8) & 0xFF;
            req.outputPortNum = attributeModifier & 0xFF;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     (lambda x:x.SLToVLMappingTable,
                                      self._sa_error));
        if ID == IBA.SMPSMInfo.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SASMInfoRecord());
            req.LID = self.get_path_lid(path);
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     lambda x:x.SMInfo);
        if ID == IBA.SMPSwitchInfo.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SASwitchInfoRecord());
            req.LID = self.get_path_lid(path);
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     lambda x:x.switchInfo);
        if ID == IBA.SMPVLArbitrationTable.MAD_ATTRIBUTE_ID:
            req = IBA.ComponentMask(IBA.SAVLArbitrationTableRecord());
            req.LID = self.get_path_lid(path);
            req.outputPortNum = attributeModifier & 0xFFFF;
            req.blockNum = (attributeModifier >> 16) & 0xFFFF;
            return self._subn_adm_do(req,self.end_port.sa_path,0,
                                     req.MAD_SUBNADMGET,
                                     (lambda x:x.VLArbitrationTable,
                                      self._sa_error));

        return self._parent.SubnGet(payload,path,attributeModifier);

    def __getattr__(self,name):
        """Let us wrapper things with additional members."""
        return getattr(self._parent,name);

    def __enter__(self):
        return self;
    def __exit__(self,*exc_info):
        return self._parent.close();
    def close(self):
        return self._parent.close();
