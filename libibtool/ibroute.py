# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
from __future__ import with_statement;
import sys
import rdma;
import rdma.satransactor;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
import rdma.discovery;
import rdma.subnet;
from libibtool import *;
from libibtool.libibopts import *;

def display_MFDB(switch,path,all):
    print "Multicast mlids [0x%x-0x%x] of switch %s %r"%(
        IBA.LID_MULTICAST,IBA.LID_MULTICAST+len(switch.mfdb)-1,
        path,switch.desc);
    print "     Ports:"," ".join("%3u"%(I) for I in range(switch.ninf.numPorts+1));
    print " MLid"
    count = 0;
    for lid,bits in enumerate(switch.mfdb):
        if bits == 0 and not all:
            continue;

        s = " ".join((" x " if bits & (1<<I) else "   ")
                     for I in range(switch.ninf.numPorts+1))
        count = count+1;
        print "0x%x       %s"%(IBA.LID_MULTICAST+lid,s)
    if all:
        print "%u mlids dumped"%(count);
    else:
        print "%u valid mlids dumped"%(count);

def display_LFDB(switch,sbn,path,all):
    max_port = switch.ninf.numPorts;
    print "Unicast lids [%u-%u] of switch %s %r"%(0,len(switch.lfdb)-1,
                                                  path,switch.desc);
    print "  Lid  Out   Destination";
    print "       Port     Info";
    top_lid = len(sbn.lids);
    count = 0
    for lid,oport in enumerate(switch.lfdb):
        desc = '';
        if oport <= max_port:
            if lid < top_lid:
                port = sbn.lids[lid];
                if port is not None and port.parent is not None:
                    desc = "(%s portguid %s %r)"%(
                        IBA_describe.node_type(port.parent.ninf.nodeType),
                        port.portGUID,port.parent.desc);
        else:
            if not all:
                continue;
            if lid == IBA.LID_RESERVED:
                desc = "(reserved LID - illegal port)";
            else:
                desc = "(illegal port)";

        count = count+1;
        print "%6u %03u : %s"%(lid,oport,desc);
    if all:
        print "%u lids dumped"%(count);
    else:
        print "%u valid lids dumped"%(count);

def get_switch(sched,sbn,args,path):
    ninf = yield sched.SubnGet(IBA.SMPNodeInfo,path);
    node,port = sbn.get_node_ninf(ninf,path);

    if not isinstance(node,rdma.subnet.Switch):
        if args.verbosity >= 1:
            ninf.printer(sys.stdout);
        raise CmdError("Not a switch at %r"%(path));

    if node.swinf is None:
        yield node.get_switch_inf(sched,path);
    sched.mqueue(node.get_switch_fdb(sched,args.do_lfdb,args.do_mfdb,path));

def get_top_switch(sched,sbn,args,path):
    yield get_switch(sched,sbn,args,path);
    if isinstance(sched,rdma.satransactor.SATransactor) and not args.no_dests:
        yield rdma.discovery.subnet_ninf_SA(sched,sbn);

def cmd_ibroute(argv,o):
    """Display switch forwarding tables.
       Usage: %prog TARGET [START_LID [END_LID]]"""
    o.add_option("-a","--all",action="store_true",dest="all",
                 help="Display all ports");
    o.add_option("-n","--no_dests",action="store_true",dest="no_dests",
                 help="Do not try to get information about what the destination LID is.");
    o.add_option("-M","--Multicast",action="store_true",dest="multicast",
                 help="Display the multicast forwarding table.");
    LibIBOpts.setup(o,discovery=True);
    (args,values) = o.parse_args(argv,expected_values=1);
    lib = LibIBOpts(o,args,values,3,(tmpl_target,tmpl_int,tmpl_int));

    if args.multicast:
        args.do_lfdb = False;
        args.do_mfdb = True;
        args.no_dests = True;
    else:
        args.do_lfdb = True;
        args.do_mfdb = False;

    # FIXME: Handle start_lid/end_lid

    with lib.get_umad_for_target(values[0]) as umad:
        sched = lib.get_sched(umad,lib.path);
        sbn = lib.get_subnet(sched);

        # FIXME: Better handle a possible cache sbn
        sched.run(mqueue=get_top_switch(sched,sbn,args,lib.path));

        switch = sbn.search_end_port(path=lib.path).parent;

        if not args.no_dests:
            if not isinstance(sched,rdma.satransactor.SATransactor):
                max_port = switch.ninf.numPorts;
                LIDs = [LID for LID,port in enumerate(switch.lfdb)
                        if port <= max_port];

                sched.run(queue=rdma.discovery.subnet_ninf_LIDS_SMP(sched,sbn,LIDs,
                                                                    True));
            else:
                rdma.discovery.load(sched,sbn,["all_LIDs","all_NodeDescription",
                                               "all_NodeInfo"]);

        sbn.paths = {switch.ports[0]: lib.path};
        switch.trim_db();
        if args.do_mfdb:
            display_MFDB(switch,lib.path,args.all);
        if args.do_lfdb:
            display_LFDB(switch,sbn,lib.path,args.all);
    return lib.done();

def get_switch_incr(sched,sbn,switch,args):
    path = sbn.get_path_smp(sched,switch.ports[0]);
    yield sched.mqueue(switch.get_switch_fdb(sched,args.do_lfdb,args.do_mfdb,path));
    switch.path = path;
    if args.do_mfdb:
        display_MFDB(switch,path,args.all);
        switch.mfdb = None;
    if args.do_lfdb:
        display_LFDB(switch,sbn,path,args.all);
        switch.lfdb = None;

def cmd_dump_lfts(argv,o):
    """Display switch forwarding tables from all switches.
       Usage: %prog"""
    LibIBOpts.setup(o,address=False,discovery=True);
    o.add_option("-a","--all",action="store_true",dest="all",
                 help="Display all ports");
    o.add_option("-D",action="store_const",dest="discovery",
                 const="DR",
                 help="Perform discovery using directed routing.");
    (args,values) = o.parse_args(argv,expected_values=0);
    lib = LibIBOpts(o,args,values);

    args.do_lfdb = True;
    args.do_mfdb = False;

    with lib.get_umad_for_target(None) as umad:
        sched = lib.get_sched(umad);
        sbn = lib.get_subnet(sched,
                             ["all_LIDs",
                              "all_NodeDescription",
                              "all_SwitchInfo"]);
        sched.run(mqueue=(get_switch_incr(sched,sbn,I,args) for I in
                          sbn.iterswitches()));
    return lib.done();

def cmd_dump_mfts(argv,o):
    """Display switch multicast forwarding tables from all switches.
       Usage: %prog"""
    LibIBOpts.setup(o,address=False,discovery=True);
    o.add_option("-a","--all",action="store_true",dest="all",
                 help="Display all ports");
    o.add_option("-D",action="store_true",dest="direct",
                 help="Perform discovery using directed routing.");
    (args,values) = o.parse_args(argv,expected_values=0);
    lib = LibIBOpts(o,args,values);

    args.do_lfdb = False;
    args.do_mfdb = True;
    args.no_dests = True;

    with lib.get_umad_for_target(None) as umad:
        sched = lib.get_sched(umad);
        sbn = lib.get_subnet(sched,
                             ["all_SwitchInfo"]);
        sched.run(mqueue=(get_switch_incr(sched,sbn,I,args) for I in
                          sbn.iterswitches()));
    return lib.done();

def cmd_ibfindnodesusing(argv,o):
    """Display the LFT forwarding tables relative to a single link.
       Usage: %prog TARGET PORT

       Use -v to display GUID and LID information for the routed end ports."""
    LibIBOpts.setup(o,address=True,discovery=True);
    o.add_option("-a","--all",action="store_true",dest="all_nodes",
                 help="Display all routed end ports, not just CAs");
    (args,values) = o.parse_args(argv,expected_values=2);
    lib = LibIBOpts(o,args,values,2,(tmpl_target,tmpl_int));

    args.do_mfdb = False;
    args.do_lfdb = True;

    args.port = values[1];

    def display_nodes(val):
        ports = set();
        for I in val:
            port = sbn.lids[I];
            if port is not None and (args.all_nodes == False or
                                     isinstance(port.parent,rdma.subnet.CA)):
                ports.add(port);

        ports = list(ports);
        ports.sort(key=lambda x:x.parent.desc);

        if o.verbosity >= 1:
            for I in ports:
                print ' %s lid %u "%s"'%(I.portGUID,I.LID,
                                         IBA_describe.dstr(I.parent.desc));
        else:
            for I in ports:
                print ' %s'%(IBA_describe.dstr(I.parent.desc));

    with lib.get_umad_for_target(values[0]) as umad:
        path = lib.path;
        sched = lib.get_sched(umad,path);
        sbn = lib.get_subnet(sched);
        if isinstance(path,rdma.path.IBDRPath):
            sbn.lid_routed = False;
            sbn.paths = {};

        sched.run(queue=get_switch(sched,sbn,args,path));
        switch = sbn.search_end_port(path=path).parent;
        if args.port <= 0 or args.port > switch.ninf.numPorts:
            raise CmdError("Port %u is invalid, switch has %u ports"%(
                args.port,switch,ninf.numPorts));
        port = switch.get_port(args.port);
        eport = port.to_end_port();
        LIDs = set(LID for LID,port in enumerate(switch.lfdb)
                   if port == args.port)

        sched.run(queue=rdma.discovery.topo_peer_SMP(sched,sbn,port));
        pport = sbn.topology[port];
        if pport is None:
            raise CmdError("No link on port %u"%(args.port));
        peport = pport.to_end_port();
        pnode = pport.parent;
        if isinstance(pnode,rdma.subnet.Switch):
            ppath = sbn.get_path_smp(sched,pport.to_end_port());
            sched.run(queue=pnode.get_switch_inf(sched,ppath));
            sched.run(queue=pnode.get_switch_fdb(sched,True,False,ppath));
            pportIdx = pnode.ports.index(pport);
            LIDs.update(LID for LID,port in enumerate(pnode.lfdb)
                        if port == pportIdx);

        sched.run(queue=rdma.discovery.subnet_ninf_LIDS_SMP(sched,sbn,list(LIDs),
                                                            True));
        print '%s %u "%s" ==>> %s %u "%s"'%(eport.portGUID,
                                            switch.ports.index(port),
                                            IBA_describe.dstr(switch.desc),
                                            peport.portGUID,
                                            pnode.ports.index(pport),
                                            IBA_describe.dstr(pnode.desc));
        display_nodes(LID for LID,port in enumerate(switch.lfdb) if port == args.port);

        print
        print '%s %u "%s" <<== %s %u "%s"'%(eport.portGUID,
                                            switch.ports.index(port),
                                            IBA_describe.dstr(switch.desc),
                                            peport.portGUID,
                                            pnode.ports.index(pport),
                                            IBA_describe.dstr(pnode.desc));
        if not isinstance(pnode,rdma.subnet.Switch):
            print " ** Not a switch **";
        else:
            display_nodes(LID for LID,port in enumerate(pnode.lfdb) if port == pportIdx);

    return lib.done();
