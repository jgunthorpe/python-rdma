# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from __future__ import with_statement;
import rdma;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
import rdma.discovery;
import rdma.subnet;
from libibtool import *;
from libibtool.libibopts import *;

def _fetch_mcast_link(sched,sbn,out_port,path,mlid,topo):
    if out_port in topo:
        return

    npath = sbn.advance_dr(path,out_port.port_id);
    nport = sbn.topology.get(out_port);
    if nport is None:
        yield sched.queue(rdma.discovery.topo_peer_SMP(sched,sbn,out_port,
                                                       path=path,
                                                       peer_path=npath));
        nport = sbn.topology[out_port];
    sched.run(mqueue=rdma.discovery.subnet_fill_port(sched,sbn,nport,
                                                     path=npath));

    topo[out_port] = nport;
    if not isinstance(nport.parent,rdma.subnet.Switch):
        return
    if sbn.lid_routed:
        npath = sbn.get_path_smp(sched,nport.to_end_port());
    yield _fetch_mcast(sched,sbn,nport,npath,mlid,topo);

def _fetch_mcast(sched,sbn,port,path,mlid,topo):
    """Get the downstream ports for the *mlid* and follow down those paths."""
    switch = port.parent;
    assert(mlid >= IBA.LID_MULTICAST)
    idx = mlid - IBA.LID_MULTICAST;
    positions = (switch.ninf.numPorts + 15)//16;
    block = [0]*32;

    # Compute the default value for 0 MFT entries.
    defbits = 0;
    if 0 < switch.swinf.defaultMulticastPrimaryPort <= switch.ninf.numPorts:
        defbits = defbits | (1 << switch.swinf.defaultMulticastPrimaryPort);
        if 0 < switch.swinf.defaultMulticastNotPrimaryPort <= switch.ninf.numPorts:
            defbits = defbits | (1 << switch.swinf.defaultMulticastNotPrimaryPort);

    def get_block(pos):
        inf = yield sched.SubnGet(IBA.SMPMulticastForwardingTable,
                                  path,(idx//32) | (pos << 28));
        for I,v in enumerate(inf.portMaskBlock):
            block[I] = block[I] | (v << pos*16);
    yield sched.mqueue(get_block(pos) for pos in range(0,positions));

    port_id = port.port_id;
    ports = block[idx % 32];
    if ports == 0:
        ports = defbits;
    sched.mqueue(_fetch_mcast_link(sched,sbn,switch.get_port(I),path,mlid,topo)
                 for I in range(0,switch.ninf.numPorts+1)
                 if ports & (1 << I) and I != port_id);

def fetch_mcast(sched,sbn,port,path,mlid):
    """Coroutine to fetch the multicast spanning tree for *mlid*, starting at
    *port*."""
    topo = {};
    # FIXME: We probably don't need to load node description for the
    # entire tree...
    if isinstance(port.parent,rdma.subnet.Switch):
        sched.run(queue=_fetch_mcast(sched,sbn,port,path,mlid,topo));
    else:
        sched.run(queue=_fetch_mcast_link(sched,sbn,port,path,mlid,topo));
    return topo;

def _trace_mcast(lst,topo,port,dport):
    if port == dport:
        return True;
    if not isinstance(port.parent,rdma.subnet.Switch):
        return False;
    lst.append(None);
    for I,port_id in port.parent.iterports():
        lst[-1] = I;
        nport = topo.get(I);
        if nport is None:
            continue;
        if nport in lst:
            continue;
        if _trace_mcast(lst,topo,nport,dport):
            return True;
    del lst[-1];
    return False;

def trace_mcast(topo,port,dport):
    """Simple exhaustive recursive search to find a path in what should
    be a spanning tree."""
    lst = [];
    if not isinstance(port.parent,rdma.subnet.Switch):
        port = topo[port];
        if port is None:
            raise CmdError("Could not find a path through the multicast spanning tree.");
    if not _trace_mcast(lst,topo,port,dport):
        raise CmdError("Could not find a path through the multicast spanning tree.");
    return lst;

def trace(umad,sched,sbn,sport,spath,dport,dpath,step_fn):
    cport = sport
    cpath = spath
    DLID = dpath.DLID;
    seen = set()
    while cport != dport:
        #print cpath,DLID
        if isinstance(cport.parent,rdma.subnet.Switch):
            inf = umad.SubnGet(IBA.SMPLinearForwardingTable,
                               cpath,DLID/64);
            port_id = inf.portBlock[DLID % 64];
            out_port = cport.parent.get_port(port_id);
        else:
            out_port = cport;

        out_port_ep = out_port.to_end_port();
        if out_port == dport and out_port == out_port_ep:
            break;
        if out_port_ep == out_port and out_port != dport and cport != sport:
            raise CmdError("Reached end port %s which is not the requested destination %r"%(
                out_port.to_end_port().portGUID,
                dport.portGUID));

        npath = sbn.advance_dr(cpath,out_port.port_id);
        nport = sbn.topology.get(out_port);
        if nport is None:
            sched.run(queue=rdma.discovery.topo_peer_SMP(sched,sbn,out_port,
                                                         path=cpath,
                                                         peer_path=npath));
            nport = sbn.topology[out_port];

        sched.run(mqueue=rdma.discovery.subnet_fill_port(sched,sbn,nport,
                                                         path=npath));

        step_fn(out_port,nport);
        if nport in seen:
            raise CmdError("Looping detected from %s to %s"%(
                cport.to_end_port().portGUID,nport.to_end_port().portGUID));
        seen.add(nport);
        cport = nport;
        if sbn.lid_routed:
            cpath = sbn.get_path_smp(sched,cport.to_end_port());
        else:
            cpath = npath
    return cpath

def resolve_path(umad,sbn,path):
    """We need to be able to issue SMPs to the given path.."""
    path.dqpn = 0;
    path.sqpn = 0;
    path.qkey = IBA.IB_DEFAULT_QP0_QKEY
    path.SLID = path.end_port.lid;
    if isinstance(path,rdma.path.IBDRPath):
        return path;
    if path.DLID != 0:
        return path;
    if path.DGID is None:
        raise CmdError("Incomplete path %r"%(path))

    # Try and find it in our database..
    port = sbn.path_to_port(path);
    if port is not None:
        return sbn.get_path_smp(umad,port);

    # Resolve the GID with the SA
    return rdma.path.get_mad_path(umad,path.DGID,
                                  dqpn=0,sqpn=0,
                                  qkey=IBA.IB_DEFAULT_QP0_QKEY);

def cmd_ibtracert(argv,o):
    """Show the route a path will take in the network
       Usage: %prog {TARGET}|{SOURCE TARGET}

       If SOURCE is not specified then the local end port is used.

       When tracing a multicast path the entire multicast spanning tree
       for the MLID is loaded, and the route that goes between start/end
       is printed"""
    LibIBOpts.setup(o,address=True,discovery=True);
    o.add_option("-r","--reverse",action="store_true",dest="reverse",
                 help="Swap source and target");
    o.add_option("-m","--mlid",action="store",dest="mlid",
                 type=int,
                 help="Report on a multicast path");
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,2,(tmpl_target,tmpl_target));

    if len(values) <= 0:
        raise CmdError("Too few arguments");

    with lib.get_umad_for_target() as umad:
        sched = lib.get_sched(umad);
        sbn = lib.get_subnet(sched,["all_SwitchInfo"]);

        # Index 0 is the source, 1 is the target, 2 is the first source
        if len(values) == 1:
            paths = [rdma.path.IBPath(sched.end_port,
                                      SLID=sched.end_port.lid,
                                      DLID=sched.end_port.lid),
                     values[0]];
            spath,dpath = paths;

            # If the target has source information then copy it in to the
            # source path.
            if dpath.SLID != 0:
                spath.DLID = dpath.SLID;
            if dpath.SGID is not None:
                spath.DGID = dpath.SGID;
        else:
            paths = list(values);

        if args.reverse:
            paths.reverse();

        # Resolve the paths to something usable
        paths = [resolve_path(umad,sbn,I) for I in paths];
        sched.run(mqueue=(rdma.discovery.subnet_get_port(sched,sbn,I)
                          for I in paths));
        ports = [sbn.path_to_port(I) for I in paths];

        # If we are starting at something other than a switch port, or our
        # local port then we need to have the connected switch port because we
        # cannot DR from a CA port. Simplest way to get this is to
        # trace to the target from the local port.
        sport = ports[0];
        dport = ports[1];
        if (not isinstance(sport.parent,rdma.subnet.Switch) and
            sport not in sbn.topology and
            sport.LID != paths[0].end_port.lid and
            not isinstance(paths[0],rdma.path.IBDRPath) and
            not isinstance(sched,rdma.satransactor.SATransactor)):
            if sbn.lid_routed:
                lpath = rdma.path.IBPath(sched.end_port,SLID=sched.end_port.lid,
                                         DLID=sched.end_port.lid,
                                         dqpn=0,sqpn=0,qkey=IBA.IB_DEFAULT_QP0_QKEY);
            else:
                lpath = rdma.path.IBDRPath(sched.end_port);
            if lib.debug >= 1:
                print "D: Figuring out route from local port to source"
            paths.append(lpath);
            sched.run(queue=rdma.discovery.subnet_get_port(sched,sbn,lpath));
            lport = sbn.path_to_port(lpath);
            ports.append(lport);
            paths[0] = trace(umad,sched,sbn,lport,lpath,sport,paths[0],
                             lambda x,y: None)

        # The target must be LID routed.
        if dport.LID == 0:
            raise CmdError("Target port %s does not have a valid LID"%(
                ports[2].portGUID));
        if isinstance(paths[1],rdma.path.IBDRPath):
            paths[1] = rdma.path.IBPath(sched.end_port,
                                        DLID=ports[1].LID,
                                        dqpn=0,sqpn=0,
                                        qkey=IBA.IB_DEFAULT_QP0_QKEY);

        if lib.debug >= 1:
            for n,path,port in zip(("SRC","DST","START"),paths,ports):
                print "D: %s is %s (%s)"%(n,path,port.portGUID);


        print "From %s %s portnum %u LID %u/%u %s"%(
            IBA_describe.node_type(sport.parent.ninf.nodeType),
            sport.portGUID,sport.port_id,
            sport.LID,16-sport.pinf.LMC,
            IBA_describe.dstr(sport.parent.desc,quotes=True));
        def step(out_port,nport):
            nport_ep = nport.to_end_port();
            print "[%u] -> %s port %s[%u] lid %u/%u %s"%(
                out_port.port_id,
                IBA_describe.node_type(nport.parent.ninf.nodeType),
                nport_ep.portGUID,
                nport.port_id,
                nport_ep.LID,16 - nport_ep.pinf.LMC,
                IBA_describe.dstr(nport.parent.desc,quotes=True));

        if args.mlid is not None:
            if args.mlid < IBA.LID_MULTICAST:
                raise CmdError("Multicast LID %r is invalid"%(args.mlid));
            topo = fetch_mcast(sched,sbn,sport,paths[0],args.mlid);
            if lib.debug >= 1:
                print "D: Multicast spanning tree topology contains %u entries"%(len(topo))
            lst = trace_mcast(topo,ports[0],ports[1]);
            step(ports[0],topo[ports[0]]);
            for I in lst:
                step(I,topo[I]);
        else:
            trace(umad,sched,sbn,ports[0],paths[0],ports[1],paths[1],step);

        print "To %s %s portnum %u LID %u/%u %s"%(
            IBA_describe.node_type(dport.parent.ninf.nodeType),
            dport.portGUID,dport.port_id,
            paths[1].DLID,16-dport.pinf.LMC,
            IBA_describe.dstr(dport.parent.desc,quotes=True));

    return lib.done();
