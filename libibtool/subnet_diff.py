# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from libibtool import *;
from libibtool.libibopts import *;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;

try:
    import cPickle as pickle
except ImportError:
    import pickle;

def load_cache(lib,fn,need):
    if lib is not None:
        fn = lib.compute_cache_fn(fn)
    with open(fn,"r") as F:
        try:
            sbn = pickle.load(F);
        except:
            e = sys.exc_info()[1]
            raise CmdError("The file %r is not a valid cache file, could not unpickle - %s: %s"%(
                fn,type(e).__name__,e));

        if not need.issubset(sbn.loaded):
            raise CmdError("The file %r does not contain enough info. Has %r, wanted %r"%(
                fn,sbn.loaded,need));
    return sbn;

def cmd_subnet_diff(argv,o):
    """Compute the difference between a stored subnet and the current subnet
       Usage: %prog REFERENCE [CURRENT]

       If the current subnet is loaded from a cache file then this program
       will compare two cache files. The REFERENCE file is a cache file created
       by ibnetdiscover --cache=FOO --refresh-cache."""
    LibIBOpts.setup(o,address=False,discovery=True);
    (args,values) = o.parse_args(argv);

    need = set(("all_NodeInfo","all_NodeDescription",
                "all_PortInfo","all_topology","all_LIDs"));

    if len(values) <= 0:
        raise CmdError("Too few arguments");

    if len(values) > 1:
        rsbn = load_cache(None,values[0],need);
        sbn = load_cache(None,values[1],need);
    else:
        lib = LibIBOpts(o,args,values);
        rsbn = load_cache(lib,values[0],need);
        with lib.get_umad() as umad:
            sched = lib.get_sched(umad);
            sbn = lib.get_subnet(sched,need);

    def diff_set(fn):
        ep = set(fn(sbn))
        rep = set(fn(rsbn))
        return (ep.difference(rep),rep.difference(ep),rep,ep);
    def diff_map(fn):
        ep = dict(fn(sbn));
        rep = dict(fn(rsbn));
        ep_s = set(ep.iterkeys());
        rep_s = set(rep.iterkeys());
        map_diff = {}
        map_diff.update((I,(ep[I],None))
                        for I in ep_s.difference(rep_s));
        map_diff.update((I,(None,rep[I]))
                        for I in rep_s.difference(ep_s));
        map_diff.update((I,(ep[I],rep[I]))
                        for I in ep_s.intersection(rep_s)
                        if ep[I] != rep[I])
        return (map_diff,None,rep_s,ep_s);

    def report(v,extra,same,printer=str):
        v = sorted(v);
        if v:
            print extra%(len(v));
            for I in v:
                print "  ",printer(I)
        else:
            print same;

    # Difference port GUIDs
    df = diff_set(lambda x:(I.portGUID
                        for I in x.iterbfs(next(x.topology.itervalues()).to_end_port())));
    print "Current subnet has %u end ports, reference subnet has %u end ports"%(
        len(df[3]),len(df[2]));
    report(df[0]," Current subnet has %u more end ports than the reference subnet:",
           " All end ports in the current subnet are in the reference subnet.");
    report(df[1],"Reference subnet has %u more end ports than the current subnet:",
           " All end ports in the reference subnet are in the current subnet.");

    # Difference node GUIDs
    df = diff_set(lambda x:(I.parent.ninf.nodeGUID
                        for I in x.iterbfs(next(x.topology.itervalues()).to_end_port())));
    print "Current subnet has %u nodes, reference subnet has %u nodes"%(
        len(df[3]),len(df[2]));
    report(df[0]," Current subnet has %u more nodes than the reference subnet:",
           " All nodes in the current subnet are in the reference subnet.");
    report(df[1],"Reference subnet has %u more nodes than the current subnet:",
           " All nodes in the reference subnet are in the current subnet.");

    # Difference topology
    def link(a,b):
        a = (a.to_end_port().portGUID,a.port_id);
        b = (b.to_end_port().portGUID,b.port_id);
        return (a,b) if a > b else (b,a);
    df = diff_set(lambda x:(link(k,v)
                        for k,v in x.topology.iteritems()));
    print "Current subnet has %u links, reference subnet has %u links"%(
        len(df[3]),len(df[2]));
    print_link = lambda x:"%s[%u] <=> %s[%u]"%(x[0][0],x[0][1],
                                               x[1][0],x[1][1]);
    report(df[0]," Current subnet has %u more links than the reference subnet:",
           " All links in the current subnet are in the reference subnet.",
           print_link);
    report(df[1],"Reference subnet has %u more links than the current subnet:",
           " All links in the reference subnet are in the current subnet.",
           print_link);

    # Check that the rate and width are the same
    same_links = df[2].intersection(df[3]);
    def link_prop(x,link):
        portGUID,portIdx = link[0]
        pinf = x.ports[portGUID].parent.ports[portIdx].pinf;
        return (portGUID,(pinf.linkSpeedActive,pinf.linkWidthActive,link));
    df = diff_map(lambda x:(link_prop(x,I)
                            for I in same_links));
    def print_rate(kv):
        portGUID,v = kv;
        cur,ref = v;
        link = cur[2];
        return "%s[%u] <=> %s[%u]: %s %sx  %s %sx"%(
            link[0][0],link[0][1],
            link[1][0],link[1][1],
            IBA_describe.link_speed(cur[0]),
            IBA_describe.link_width(cur[1]),
            IBA_describe.link_speed(ref[0]),
            IBA_describe.link_width(ref[1]));

    report(df[0].iteritems()," The subnets have %u different link rates",
           " All links in the current subnet have the same rate in the reference subnet.",
           print_rate);

    # Difference LID assignment
    df = diff_map(lambda x:((LID,I.portGUID)
                        for LID,I in enumerate(x.lids) if I is not None))
    print "Current subnet has %u LIDs, reference subnet has %u LIDs"%(
        len(df[3]),len(df[2]));
    def print_lid(v):
        lid,tp = v;
        if tp[0] is None:
            return "%5u: %-19s %s"%(lid,"      !Cur",tp[1]);
        if tp[1] is None:
            return "%5u: %s %-19s"%(lid,tp[0],"      !Ref");
        return "%5u: %s %s"%(lid,tp[0],tp[1]);
    report(df[0].iteritems()," The subnets have %u different LID assignments (LID: Current portGUID, Reference portGUID):",
           " All LIDs in the current subnet are the same as the reference subnet.",
           print_lid);
