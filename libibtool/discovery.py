# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import sys;
import time;
from libibtool import *;
from libibtool.libibopts import *;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
import rdma.subnet;

def as_node_name(node):
    if isinstance(node,rdma.subnet.CA):
        return '"H-%s"'%(node.ninf.nodeGUID);
    if isinstance(node,rdma.subnet.Switch):
        return '"S-%s"'%(node.ninf.nodeGUID);
    return '"?-%s"'%(node.ninf.nodeGUID);

def as_port_name(port):
    node = port.parent;
    if isinstance(node,rdma.subnet.Switch):
        return '%s[%u]'%(as_node_name(node),node.ports.index(port));
    return '%s[%u](%s)'%(as_node_name(node),node.ports.index(port),port.portGUID);

def summary(sched,sbn,node):
    if isinstance(node,rdma.subnet.CA):
        print '%-8s: %s ports %u "%s"'%(
            "Ca",node.ninf.nodeGUID,node.ninf.numPorts,
            IBA_describe.dstr(node.desc));
    elif isinstance(node,rdma.subnet.Switch):
        zport = node.ports[0];
        pinf = zport.pinf;
        for port in node.ports:
            if port.pinf is not None:
                pinf = port.pinf;
                break;
        if pinf is None:
            path = sbn.get_path_smp(sched,zport);
            pinf = yield sched.SubnGet(IBA.SMPPortInfo,path);
            sbn.get_port_pinf(pinf,path=path,portIdx=0);
        print '%-8s: %s ports %u "%s" base port 0 lid %u lmc %u'%(
            "Switch",node.ninf.nodeGUID,node.ninf.numPorts,
            IBA_describe.dstr(node.desc),
            zport.LID,pinf.LMC);
    elif isinstance(node,rdma.subnet.Router):
        print '%-8s: %s ports %u "%s"'%(
            "Router",node.ninf.nodeGUID,node.ninf.numPorts,
            IBA_describe.dstr(node.desc));
    else:
        print '%-8s: %s ports %u "%s"'%(
            "??%u"%(node.ninf.nodeType),node.ninf.nodeGUID,node.ninf.numPorts,
            IBA_describe.dstr(node.desc));

def summary2(node):
    if isinstance(node,rdma.subnet.CA):
        kind = "Ca";
    elif isinstance(node,rdma.subnet.Switch):
        kind = "Switch";
    elif isinstance(node,rdma.subnet.Router):
        kind = "Router";
    else:
        kind = "??%u"%(node.ninf.nodeType);

    print '%-8s: %s ports %u devid 0x%x vendid 0x%x "%s"'%(
        kind,node.ninf.nodeGUID,node.ninf.numPorts,
        node.ninf.deviceID,node.ninf.vendorID,
        IBA_describe.dstr(node.desc));

def go_listing(argv,o,node_type,lib=None):
    if lib is None:
        LibIBOpts.setup(o,address=False,discovery=True);
        (args,values) = o.parse_args(argv,expected_values=0);
        lib = LibIBOpts(o,args,values);

    with lib.get_umad_for_target(None) as umad:
        sched = lib.get_sched(umad);
        sbn = lib.get_subnet(sched,
                             ["all_NodeInfo %u"%(node_type),
                              "all_NodeDescription %u"%(node_type)]);
        itms = [I for I in sbn.iternodes()
                if I.ninf.nodeType == node_type];
        itms.sort(key=lambda x:x.ninf.nodeGUID);
        sched.run(mqueue=(summary(sched,sbn,I) for I in itms));
    return lib.done();

def go_print_node(argv,o,node_type):
    """Display a single ibnetdiscover record searching by node GUID."""
    LibIBOpts.setup(o,address=False,discovery=True);
    o.add_option("-l",action="store_true",dest="list",
                 help="Display all CAs");
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,1,(tmpl_node_guid,));

    if args.list:
        return go_listing(argv,o,node_type,lib);

    if len(values) < 1:
        raise CmdError("Too few arguments");

    node_guid = values[0];
    with lib.get_umad_for_target(None) as umad:
        sched = lib.get_sched(umad);

        if isinstance(sched,rdma.satransactor.SATransactor):
            sbn = lib.get_subnet(sched);
            sched.run(queue=rdma.discovery.subnet_ninf_GUID(sched,sbn,node_guid));
        else:
            # Can't search by node GUID, do it the hard way..
            sbn = lib.get_subnet(sched,
                                 ["all_NodeInfo %u"%(node_type)]);
        # FIXME: Move me
        if sbn.topology is None:
            sbn.topology = {};

        node = sbn.nodes.get(node_guid);
        if node is None:
            raise CmdError("Could not find node %s"%(node_guid));
        sched.run(queue=rdma.discovery.topo_surround_SMP(sched,sbn,node));
        if node.ninf.nodeType != node_type:
            raise CmdError("Node %s was type %u not %u"%(
                node_guid,node.ninf.nodeType,node_type));

        print_ibnetdiscover_single(sbn,node);
    return lib.done();

def cmd_ibhosts(argv,o):
    """Display all CA nodes.
       Usage: %prog"""
    return go_listing(argv,o,IBA.NODE_CA);

def cmd_ibprintca(argv,o):
    """Display a CA node.
       Usage: %prog [-l] [NODE_GUID]"""
    return go_print_node(argv,o,IBA.NODE_CA);

def cmd_ibswitches(argv,o):
    """Display all switch nodes.
       Usage: %prog"""
    return go_listing(argv,o,IBA.NODE_SWITCH);

def cmd_ibprintswitch(argv,o):
    """Display a switch node.
       Usage: %prog [-l] [NODE_GUID]"""
    return go_print_node(argv,o,IBA.NODE_SWITCH);

def cmd_ibrouters(argv,o):
    """Display all router nodes.
       Usage: %prog"""
    return go_listing(argv,o,IBA.NODE_ROUTER);

def cmd_ibprintrt(argv,o):
    """Display a router node.
       Usage: %prog [-l] [NODE_GUID]"""
    return go_print_node(argv,o,IBA.NODE_ROUTER);

def cmd_ibnodes(argv,o):
    """Display all CA or switch nodes.
       Usage: %prog"""
    LibIBOpts.setup(o,address=False,discovery=True);
    (args,values) = o.parse_args(argv,expected_values=0);
    lib = LibIBOpts(o,args,values);

    with lib.get_umad_for_target(None) as umad:
        sched = lib.get_sched(umad);
        sbn = lib.get_subnet(sched,
                             ["all_NodeInfo",
                              "all_NodeDescription"]);
        itms = [I for I in sbn.iternodes()
                if (I.ninf.nodeType == IBA.NODE_CA or
                    I.ninf.nodeType == IBA.NODE_SWITCH)];
        itms.sort(key=lambda x:x.ninf.nodeGUID);
        sched.run(mqueue=(summary(sched,sbn,I) for I in itms));
    return lib.done();

def print_ibnetdiscover_single(sbn,node):
    ninf = node.ninf;
    print '''vendid=0x%x
devid=0x%x
sysimgguid=%s'''%(ninf.vendorID,ninf.deviceID,ninf.systemImageGUID)
    is_switch = False;
    if isinstance(node,rdma.subnet.CA):
        print '''caguid=%s
Ca\t%u %s\t# "%s"'''%(ninf.nodeGUID,ninf.numPorts,as_node_name(node),
                      IBA_describe.dstr(node.desc));
    elif isinstance(node,rdma.subnet.Switch):
        is_switch = True;
        port = node.ports[0];
        print '''switchguid=%s(%s)
Switch\t%u %s\t# "%s" base port 0 lid %u lmc %u'''%\
                (ninf.nodeGUID,port.portGUID,ninf.numPorts,as_node_name(node),
                 IBA_describe.dstr(node.desc),port.LID,port.pinf.LMC);
    else:
        print '''nodeguid=%s
??%u\t%u %s\t# "%s"'''%(ninf.nodeGUID,ninf.nodeType,ninf.numPorts,as_node_name(node),
                      IBA_describe.dstr(node.desc));

    for port,idx in node.iterports():
        peer = sbn.topology.get(port);
        if peer is None:
            continue;

        if is_switch:
            print '%s\t%s\t# "%s" lid %u %ux%s'%(
                    idx,as_port_name(peer),IBA_describe.dstr(peer.parent.desc),
                    peer.to_end_port().LID,IBA_describe.link_width(port.pinf.linkWidthActive),
                    IBA_describe.link_speed(port.pinf.linkSpeedActive));
        else:
            print '%s(%s)\t%s\t# lid %u lmc %u "%s" %ux%s'%(
                idx,port.portGUID,as_port_name(peer),
                port.LID,port.pinf.LMC,
                IBA_describe.dstr(peer.parent.desc),
                IBA_describe.link_width(port.pinf.linkWidthActive),
                IBA_describe.link_speed(port.pinf.linkSpeedActive));

def print_ibnetdiscover_topology(sbn,root):
    """Usual ibnetdiscover output."""
    print "#"
    print "# Topology file: generated on %s"%(time.strftime("%a %b %d %X %Y"))
    print "#"
    print "# Initiated from node %s port %s"%(root.parent.ninf.nodeGUID,
                                              root.portGUID);
    print

    done = set();
    for I in sbn.iterbfs(root):
        node = I.parent;
        if node in done:
            continue;
        done.add(node);
        print_ibnetdiscover_single(sbn,node);
        print

def cmd_ibnetdiscover(argv,o):
    """Display the topology of the subnet.
       Usage: %prog"""
    o.add_option("-l","--list",action="store_true",dest="list",
                 help="Show a summary listing of all nodes");
    o.add_option("-H","--Hca_list",action="store_true",dest="cas",
                 help="Show a summary listing of all CA nodes");
    o.add_option("-S","--Switch_list",action="store_true",dest="switches",
                 help="Show a summary listing of all switch nodes");
    o.add_option("-R","--Router_list",action="store_true",dest="routers",
                 help="Show a summary listing of all router nodes");
    LibIBOpts.setup(o,address=False,discovery=True);
    (args,values) = o.parse_args(argv,expected_values=0);
    lib = LibIBOpts(o,args,values);

    with lib.get_umad_for_target(None) as umad:
        sched = lib.get_sched(umad);
        # Sigh, I'd love to have incremental output but my tidy encapsulation
        # does not allow that.
        sbn = lib.get_subnet(sched,
                             ["all_NodeInfo",
                              "all_NodeDescription",
                              "all_PortInfo",
                              "all_topology"]);

        root = sbn.ports[umad.parent.port_guid];

        node_type = None;
        if args.cas:
            node_type = IBA.NODE_CA;
        if args.switches:
            node_type = IBA.NODE_SWITCH;
        if args.routers:
            node_type = IBA.NODE_ROUTER;

        if args.list or node_type is not None:
            done = set();
            for port in sbn.iterbfs(root):
                node = port.parent;
                if node in done:
                    continue;
                if node_type is None or node_type == node.ninf.nodeType:
                    summary2(node);
        else:
            print_ibnetdiscover_topology(sbn,root);

    return lib.done();
