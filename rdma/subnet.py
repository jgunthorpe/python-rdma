import collections;
import rdma;
import rdma.path;
import rdma.satransactor;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;

class Node(object):
    """Hold onto information about a single node in the network. A node is a
    switch, \*CA, or router with multiple end ports. A node has a single
    `nodeGUID` and there can not be duplicate nodeGUID's. The port information
    in the :attr:`ninf` stores a random port."""
    #__slots__ = ("ninf","desc","ports");

    #: Instance of :class:`rdma.IBA.SMPNodeInfo`
    ninf = None;
    #: Result of :func:`rdma.IBA_describe.description` on the nodeString.
    desc = None;
    #: Array of :class`Port`. Note: CA port 1 is stored in index 1.
    ports = None;

    def get_port(self,portIdx):
        """Return the port for index *portIdx*."""
        if self.ports is None or len(self.ports) <= portIdx:
            port = Port(self);
            self.set_port(portIdx,port);
            return port;
        port = self.ports[portIdx];
        if port is None:
            port = Port(self);
            self.ports[portIdx] = port;
        return port;

    def set_port(self,portIdx,port):
        """Store *port* in *portIdx* for :attr:`ports`."""
        if self.ports is None:
            self.ports = [None]*(portIdx+1);
        if len(self.ports) <= portIdx:
            self.ports.extend(None for I in range(len(self.ports),portIdx+1));
        self.ports[portIdx] = port;

    def set_desc(self,nodeString):
        """Set the description from a *nodeString* type value."""
        self.desc = IBA_describe.description(nodeString);

    def get_desc(self,sched,path):
        """Coroutine to fetch the node description"""
        ns = yield sched.SubnGet(IBA.SMPNodeDescription,path);
        self.set_desc(ns.nodeString);

    def iterports(self):
        """Iterate over all ports. This only returns ports that are in the
        network, ie ports on a CA that are not reachable are not returned.

        :rtype: generator of tuple(:class:`Port`,portIdx)"""
        if self.ninf is None:
            num = len(self.ports)
        else:
            num = self.ninf.numPorts+1;
        for I in range(1,num+1):
            port = self.get_port(I);
            if (port.portGUID is not None or port.LID is not None):
                yield (port,I);

    def iterend_ports(self):
        """Iterate over all end ports. This only returns ports that are in the
        network, ie ports on a CA that are not reachable are not returned.

        :rtype: generator of :class:`Port`"""
        if self.ports is not None:
            return (I for I in self.ports[1:] if I is not None and
                    (I.portGUID is not None or I.LID is not None));

    def to_end_port(self,port):
        """Return the end port that is associated with *port*.
        For switches this returns port 0, otherwise it returns *port*."""
        return port;

class Port(object):
    #__slots__ = ("parent","pinf","portGUID");
    #: :class:`Node` this port belongs to
    parent = None;
    #: Instance of :class:`rdma.IBA.SMPPortInfo`
    pinf = None;
    #: GUID for the port
    portGUID = None;
    #: Base LID if it is an end port
    LID = None;

    def __init__(self,parent):
        if parent is not None:
            self.parent = parent;

    def to_end_port(self):
        """Return the end port that is associated with this port.
        For switches this returns port 0, otherwise it returns itself."""
        return self.parent.to_end_port(self);

class CA(Node):
    """Hold onto information about a single CA node in the network."""

class Router(Node):
    """Hold onto information about a single router node in the network."""

class Switch(Node):
    """Hold onto information about a single switch node in the network. Switches
    have several unique bits of information."""
    #__slots__ = ("swinf","mfdb","lfdb");
    #: Instance of :class:`rdma.IBA.SMPSwitchInfo`
    swinf = None;
    #: class:`list` starting at LID :data:`rmda.IBA.LID_MULTICAST` holding the multicast
    #: forwarding database.
    mfdb = None;
    #: :class:`list` starting at LID 0 holding the linear forwarding databse.
    lfdb = None;

    def __init__(self):
        Node.__init__(self);

    def iterend_ports(self):
        """Iterate over all end ports.

        :rtype: generator of :class:`Port`"""
        yield self.get_port(0);

    def iterports(self):
        """Iterate over all ports. This only returns ports that are in the
        network, ie ports on a CA that are not reachable are not returned.  For
        switches all ports are always in the network.

        :rtype: generator of tuple(:class:`Port`,portIdx)"""
        if self.ninf is None:
            return ((self.get_port(I),I) for I in range(0,len(self.ports)));
        else:
            return ((self.get_port(I),I) for I in range(0,self.ninf.numPorts+1));

    def to_end_port(self,port):
        """Return the end port that is associated with *port*.
        For switches this returns port 0, otherwise it returns *port*."""
        return self.get_port(0);

    def trim_db(self):
        """Remove unnecessary entries from the end of the LFDB and MFDB."""
        if self.lfdb:
            for I in range(len(self.lfdb)-1,-1,-1):
                if self.lfdb[I] != 255:
                    del self.lfdb[I+1:];
                    break;
        if self.mfdb:
            # Remove the permissive LID
            del self.mfdb[IBA.LID_COUNT_MULTICAST:];

    @property
    def top_unicast_lid(self):
        """Top unicast lid in the switch forwarding database."""
        return (min(self.swinf.linearFDBTop,self.swinf.linearFDBCap)+63)//64*64;

    def get_switch_fdb(self,sched,do_lfdb,do_mfdb,path):
        """Generator to fetch switch forwarding database."""
        # FIXME: How to tell if this is a random FDB switch?
        if do_lfdb:
            self.lfdb = [None]*self.top_unicast_lid;
            if isinstance(sched,rdma.satransactor.SATransactor):
                yield self._get_LFDB_SA(sched,path);
            else:
                for I in range(len(self.lfdb)/64):
                    yield self._get_LFDB(sched,I,path);
        if do_mfdb:
            self.mfdb = [0]*((self.swinf.multicastFDBCap+31)//32*32);
            if isinstance(sched,rdma.satransactor.SATransactor):
                yield self._get_MFDB_SA(sched,path);
            else:
                positions = (len(self.ports) + 15)//16;
                for I in range(len(self.mfdb)/32):
                    for pos in range(0,positions):
                        yield self._get_MFDB(sched,I,pos,path);

    def get_switch_inf(self,sched,path):
        """Coroutine to fetch a switch info and then can schedual a LFDB/MFDB
        load.

        :returns: via sched a contex t"""
        self.swinf = yield sched.SubnGet(IBA.SMPSwitchInfo,path);

    def _get_LFDB(self,sched,idx,path):
        """Coroutine to fetch a single LFDB block."""
        inf = yield sched.SubnGet(IBA.SMPLinearForwardingTable,
                                  path,idx);
        self.lfdb[idx*64:idx*64+64] = bytearray(inf.portBlock);

    def _get_LFDB_SA(self,sched,path):
        """Coroutine to fetch the entire LFDB from the SA"""
        req = IBA.ComponentMask(IBA.SALinearForwardingTableRecord());
        req.LID = sched.get_path_lid(path);
        res = yield sched.SubnAdmGetTable(req);
        for I in res:
            idx = I.blockNum;
            self.lfdb[idx*64:idx*64+64] = bytearray(I.linearForwardingTable.portBlock);

    def _get_MFDB(self,sched,idx,pos,path):
        """Coroutine to fetch a single MFDB block."""
        inf = yield sched.SubnGet(IBA.SMPMulticastForwardingTable,
                                  path,idx | (pos << 28));
        for I,v in enumerate(inf.portMaskBlock):
            self.mfdb[idx*32+I] = self.mfdb[idx*32+I] | (v << pos*16);

    def _get_MFDB_SA(self,sched,path):
        """Coroutine to fetch the entire MFDB from the SA"""
        req = IBA.ComponentMask(IBA.SAMulticastForwardingTableRecord());
        req.LID = sched.get_path_lid(path);
        res = yield sched.SubnAdmGetTable(req);
        for inf in res:
            pos = inf.position;
            idx = inf.blockNum;
            for I,v in enumerate(inf.multicastForwardingTable.portMaskBlock):
                self.mfdb[idx*32+I] = self.mfdb[idx*32+I] | (v << pos*16);

class Subnet(object):
    """Stores information about an entire IB subnet.

    The database is organized around :class:`Port` and :class:`Node`
    objects. The database can be sparse, a node may not have any associated
    :class:`Port` objects and :class:`Port` objects may be missing nodes. Thus
    it is important to use the accessors to get new objects which properly
    join things together. The storage system is intended to support
    automatically filling in data no matter what the order is.

    To support the discovery module and caching the :attr:`loaded` attribute
    contains a listing of what discovery actions have been performed.
    """
    #: :class:`dict` of nodeGUID to :class:`Node` objects
    nodes = None;
    #: :class:`dict` of portGUID to :class:`Port` objects
    ports = None;
    #: :class:`list` of unicast LID to :class:`Port` objects
    lids = None;
    #: :class:`set` of all :class:`Node`
    all_nodes = None;
    #: :class:`dict` of :class:`Port` to :class:`Port` indicating links.
    topology = None;
    #: :class:`dict` of :class:`Port` to :class:`rdma.path.IBPath` indicating paths.
    #: This should be accessed via get_path_smp as it will probably be
    #: converted into a DR route cache.
    paths = None;
    #: :class:`set` of strings indicating what discovery has been performed.
    loaded = None;
    #: `True` if routes are done via LID not DR
    lid_routed = True;

    def __init__(self):
        self.nodes = {};
        self.ports = {};
        self.lids = [];
        self.all_nodes = set();
        self.loaded = set();

    def set_max_lid(self,max_lid):
        """Make :attr:`lids` sufficiently big to store *max_lid*."""
        if len(self.lids) <= max_lid:
            self.lids.extend(None for I in range(len(self.lids),max_lid+1));

    def get_path_smp(self,sched,end_port):
        """Return a VL15 SMP path to *end_port*. If directed routing is being
        used then this must be used to get paths."""
        if self.paths is not None:
            path = self.paths.get(end_port);
            if path is not None:
                return path;

        path = rdma.path.IBPath(sched.end_port,SLID=sched.end_port.lid,
                                DLID=end_port.LID,
                                dqpn=0,sqpn=0,qkey=IBA.IB_DEFAULT_QP0_QKEY);
        path._cached_subnet_end_port = end_port;
        if self.paths is not None:
            self.paths[end_port] = path;
        return path;

    def link_end_port(self,port,portIdx=None,nodeGUID=None,portGUID=None,
                      path=None,LID=None,LMC=0):
        """Use the provided information about *port* to update the database.

        Note: For switches *portIdx* must be 0."""
        if (LID is None and path is not None and
            not isinstance(path,rdma.path.IBDRPath)):
            LID = path.DLID;

        node = port.parent;

        if portIdx is not None:
            node.set_port(portIdx,port);
        if portGUID is not None and port.portGUID is None:
            port.portGUID = portGUID;
            self.ports[portGUID] = port;
        if LID is not None:
            port.LID = LID;
            self.set_max_lid(LID + (1<<LMC)-1);
            for I in IBA.lid_lmc_range(LID,LMC):
                self.lids[I] = port;
        if path is not None:
            path._cached_subnet_end_port = port;
            # Since we know it, record the DGID into the path. This produces
            # error messages that include the DGID..
            if portGUID is not None and path.DGID is None:
                path.DGID = IBA.GID(prefix=IBA.GID_DEFAULT_PREFIX,
                                    guid=portGUID);
            if self.paths is not None:
                self.paths[port] = path;
        return port;

    def search_end_port(self,portIdx=None,portGUID=None,nodeGUID=None,
                        path=None,LID=None,LMC=0):
        """Return a :class:`Port` instance associated with the supplied
        information if it exists or `None`.

        Note: For switches *portIdx* must be 0."""
        # Note: This is in order of accuracy, LID matching is only accurate
        # if the subnet is properly configured and LIDs assigned correctly.
        port = None;
        if path is not None:
            port = getattr(path,"_cached_subnet_end_port",None);
            if port is not None:
                return port;
        if portGUID is not None:
            port = self.ports.get(portGUID);
            if port is not None:
                return port;
        node = None;
        if nodeGUID is not None:
            node = self.nodes.get(nodeGUID);
        if port is not None:
            node = port.parent;
        if node is not None:
            if isinstance(node,Switch):
                return node.get_port(0);
            if portIdx is not None:
                return node.get_port(portIdx);

        if (LID is None and path is not None and
            not isinstance(path,rdma.path.IBDRPath)):
            LID = path.DLID;
        if LID is not None and LID < len(self.lids):
            port = self.lids[LID];
            if port is not None:
                return port;

        return None;

    def _fixup_change_to_switch(self,node):
        """Due to how we lazy create some of the information we can create switch nodes
        and switch node ports before we know they are switches. If this happens the
        database needs updating so that :attr:`lids` and :attr:`ports` refer to
        switch port 0, not arbitrary switch ports. NOTE: The rule is that all
        calls everywhere must use accurate *portIdx* values!. Doing this should be
        avoided.. """
        if node.ports[0] is None:
            node.ports[0] = Port(node);

        count = sum(1 for I in node.ports if I is not None);
        if count == 1:
            return node.ports[0];

        # We have other ports, fix it up...
        zport = node.ports[0];
        lid = None;
        for I in node.ports:
            if I is None:
                continue;
            if I.portGUID is not None:
                self.ports[I.portGUID] = zport;
                zport.portGUID = I.portGUID;
                I.portGUID = None;
            if I.LID is not None:
                lid = I.LID;
                I.LID = None;

        for I in range(lid,len(self.lids)):
            port = self.lids[I];
            if port is not None:
                if port.parent != node:
                    break;
                self.lids[I] = zport;

    def get_node(self,type_,**kwargs):
        """Return an existing or new :class:`Node` and :class:`Port` instance
        associated with the end port described by *kwargs*.  *kwargs* is the
        same signature as for :meth:`search_port`. *kwargs* must include
        enough information to link a :class:`Port` to the :class:`Node`.

        :rtype: tuple(:class:`Node`, :class:`Port`)"""
        port = self.search_end_port(**kwargs);

        if port is None:
            node = type_();
            self.all_nodes.add(node);
        else:
            node = port.parent;
        if not isinstance(node,type_):
            if isinstance(node,Node):
                # This was a temporary node, re-type it appropriately.
                node.__class__ = type_;
                if isinstance(node,Switch):
                    port = self._fixup_change_to_switch(node);
            else:
                # FIXME: This can happen if the network is messed up, make a
                # better message.
                raise rdma.RDMAError("Node changed type.");
        if isinstance(node,Switch):
            kwargs["portIdx"] = 0;
            port = node.get_port(0);
        if port is None:
            port = Port(node);

        self.link_end_port(port,**kwargs);
        return (node,port);

    def get_node_ninf(self,ninf,path=None,LID=None):
        """Return the :class:`Node` object that holds the associated *ninf*. If
        none exists then one is created. If *path* or *LID* are specified then
        the appropriate information from both is integrated into the database.

        :rtype: tuple(:class:`Node`, :class:`Port`)"""
        portIdx = ninf.localPortNum;
        if ninf.nodeType == IBA.NODE_SWITCH:
            type_ = Switch;
            portIdx = 0;
        elif ninf.nodeType == IBA.NODE_CA:
            type_ = CA;
        elif ninf.nodeType == IBA.NODE_ROUTER:
            type_ = Router;
        else:
            type_ = Node;

        np = self.get_node(type_,portIdx=portIdx,
                           nodeGUID=ninf.nodeGUID,
                           portGUID=ninf.portGUID,
                           path=path,LID=LID);
        self.nodes[ninf.nodeGUID] = np[0];
        np[0].ninf = ninf;
        return np;

    def get_port(self,port_select=None,localPortNum=None,portIdx=None,
                 **kwargs):
        """Return the :class:`Port` object for an arbitrary port (ie a non-end
        port on a switch).  This is designed to be used with information
        available during MAD processing, the main purpose of this function is
        to disambiguate what requested port 0 means.

        If at all possible call this with *portIdx* set correctly and nothing
        else. Otherwise set *localPortNum* to the value returned by the MAD.

        :rtype: :class:`Port`
        :raises ValueError: If the node type is needed but not known."""
        if portIdx is None and port_select != 0:
            portIdx = port_select;

        if portIdx is not None:
            if portIdx == 0:
                # A portIdx of 0 unambigously refers to a switch end port, but callers
                # should not rely on this..
                node,port = self.get_node(Switch,portIdx=portIdx,**kwargs);
            else:
                node,port = self.get_node(Node,portIdx=portIdx,**kwargs);
        else:
            # Okay, requesting port 0.. This is either localPortNum or switch port 0,
            # or unknowable.
            port = self.search_end_port(**kwargs);
            if (port is None or port.parent is None or
                port.parent.__class__ == Node):
                raise ValueError("Trying to get a port before the node type is known.");
            node = port.parent;

            if isinstance(node,Switch):
                portIdx = 0;
            else:
                portIdx = localPortNum;
            if portIdx is None:
                self.link_end_port(port,**kwargs);
                return node,port;

        port = node.get_port(portIdx);
        self.link_end_port(port,**kwargs);
        return port;

    def get_port_pinf(self,pinf,port_select=None,portIdx=None,path=None,LID=None):
        """Return the :class:`Port` object that holds the associated *pinf*. This
        function requires a correct *portIdx* if the node type is not known.

        :rtype: :class:`Port`"""
        port = self.get_port(port_select=port_select,localPortNum=pinf.localPortNum,
                             portIdx=portIdx,path=path,LID=pinf.LID);
        port.pinf = pinf;
        return port;

    def iternodes(self):
        """Iterate over all nodes.

        :rtype: generator of :class:`Node`"""
        return iter(self.all_nodes);

    def iterswitches(self):
        """Iterate over all switches.

        :rtype: generator of :class:`Node`"""
        return (I for I in self.all_nodes if isinstance(I,Switch));

    def iterports(self):
        """Iterate over all ports. This only returns ports that are in the network,
        ie ports on a CA that are no reachable are not returned.

        :rtype: generator of tuple(:class:`Port`,portIdx)"""
        for I in self.all_nodes:
            for J in I.iterports():
                yield J;

    def iterend_ports(self):
        """Iterate over all end ports. This only returns ports that are in the
        network, ie ports on a CA that are not reachable are not returned.

        :rtype: generator of :class:`Port`"""
        for I in self.all_nodes:
            for J in I.iterend_ports():
                yield J;

    def iterpeers(self,start):
        """Iterate over all end ports connected to *start*.

        :rtype: generator of :class:`Port`"""
        if isinstance(start.parent,Switch):
            for I in start.parent.ports[1:]:
                peer = self.topology.get(I);
                if peer is not None:
                    yield peer.to_end_port();
        else:
            peer = self.topology.get(start);
            if peer is not None:
                yield peer.to_end_port();

    def iterbfs(self,start):
        """Iterate over all end ports in a BFS order.

        :rtype: generator of :class:`Port`"""
        todo = collections.deque();
        done = set();
        todo.append(start);
        while todo:
            cur = todo.pop();
            if cur in done:
                continue;

            done.add(cur);
            todo.extend(self.iterpeers(cur));
            yield cur;

