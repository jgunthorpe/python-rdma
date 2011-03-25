# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
from __future__ import with_statement;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
from libibtool import *;
from libibtool.libibopts import *;

class CheckError(CmdError):
    pass
warnings = []
def red(s):
    if lib.args.colour:
        return "\033[1;031m%s\033[0;39m"%(s);
    return s;
def green(s):
    if lib.args.colour:
        return "\033[1;032m%s\033[0;39m"%(s);
    return s;
def blue(s):
    if lib.args.colour:
        return "\033[1;034m%s\033[0;39m"%(s);
    return s;

def load_thresholds(fn):
    """Load the performance counters threshold file."""
    if fn is None:
        return {'portRcvErrors': 10,
                'portXmitConstraintErrors': 100,
                'symbolErrorCounter': 10,
                'VL15Dropped': 100,
                'portXmitDiscards': 100,
                'excessiveBufferOverrunErrors': 10,
                'linkErrorRecoveryCounter': 10,
                'portRcvSwitchRelayErrors': 100,
                'portRcvRemotePhysicalErrors': 100,
                'localLinkIntegrityErrors': 10,
                'portRcvConstraintErrors': 100,
                'linkDownedCounter': 10};
    else:
        with open(fn,"rt") as F:
            res = {}
            for I in F.readlines():
                I = I.strip();
                if not I:
                    continue;
                if I[0] == "#":
                    continue;
                try:
                    p = I.partition('=')
                    res[p[0].strip()] = int(p[2].strip(),0);
                except ValueError:
                    raise CmdError("Invalid threshold line %r"%(I));

    # Canonize and check the names
    res2 = {};
    keys = set(I[0] for I in IBA.PMPortCounters.MEMBERS);
    onames = dict((v,k) for k,v in libib_name_map_perfquery.iteritems());
    for k,v in res.iteritems():
        if k not in keys:
            k = onames.get(k,k);
        if k not in keys:
            kl = k.lower();
            for I in keys:
                if I.lower() == kl:
                    k = I;
                    break;
        if k not in keys:
            raise CmdError("Threshold key %r is not known"%(k));
        res2[k] = v;
    return res2;

def check(o,a,v,comp,compn,fmt,desc,error=False):
    c = getattr(o,a);
    if comp(c,v):
        if lib.debug >= 1:
            print "D: Check OK: %r %r against %r: %s"%(a,fmt(c),fmt(v),desc)
        return;
    msg = "%s is %r, %s %r: %s"%(a,fmt(c),compn,fmt(v),desc);
    if error:
        raise CheckError(msg);
    warnings.append(msg);
def checkEQ(o,a,v,desc,fmt=str,error=False):
    check(o,a,v,(lambda a,b:a == b),"expected",fmt,desc,error);
def checkNEQ(o,a,v,desc,fmt=str,error=False):
    check(o,a,v,(lambda a,b:a != b),"but shouldn't be",fmt,desc,error);
def checkLTE(o,a,v,desc,fmt=str,error=False):
    check(o,a,v,(lambda a,b:a <= b),"expected less than",fmt,desc,error);
def get_max(v):
    if v == 0:
        return 0;
    I = -1;
    while v != 0:
        v = v >> 1;
        I = I + 1;
    return 1<<I;

# Decorators to tell what kind of check the function is doing so the
# caller code can do the right thing.
KIND_NODE = (1<<0)
KIND_PORT = (1<<1)
KIND_PERF = (1<<2)
KIND_CLEAR = (1<<3)
def node_check(func):
    func.kind = KIND_NODE;
    return func;
def perf_check(func):
    func.kind = KIND_PERF;
    return func;
def port_check(func):
    func.kind = KIND_PORT;
    return func;
def clear_check(func):
    func.kind = KIND_CLEAR;
    return func;

def get_perf(sched,path,ninf,portIdx,reset=False,select=0xFFFF):
    """Coroutine to get port counters."""
    cnts = IBA.PMPortCounters();
    if portIdx is None:
        cnts.portSelect = ninf.localPortNum;
        if ninf.nodeType == IBA.NODE_SWITCH and cnts.portSelect == 0:
            cnts.portSelect = 1;
    else:
        cnts.portSelect = portIdx;

    accumulate = False;
    if cnts.portSelect == 0xFF:
        cpinf = yield sched.PerformanceGet(IBA.MADClassPortInfo,path);
        path.resp_time = cpinf.respTimeValue;
        accumulate = not (cpinf.capabilityMask & IBA.allPortSelect);
        if accumulate and ninf.nodeType == IBA.NODE_CA:
            raise CmdError("Can't iterate over all ports on a CA.");

    if reset:
        cnts.counterSelect = select;

    if accumulate:
        def get_cnts(port):
            cnts.portSelect = port;
            if reset:
                yield sched.PerformanceSet(cnts,path);
            else:
                results[port] = yield sched.PerformanceGet(cnts,path);
        results = [None]*(ninf.numPorts+1);
        yield sched.mqueue(get_cnts(I)
                          for I in range(1,ninf.numPorts+1));
        if reset:
            return

        res = sum_result(results);
    else:
        if reset:
            yield sched.PerformanceSet(cnts,path);
            return
        else:
            res = yield sched.PerformanceGet(cnts,path);
    res.portSelect = cnts.portSelect;
    sched.result = res;

@node_check
def do_check_node(sched,path,portGUID,ninf,**kwargs):
    """Coroutine to do the checknode action"""
    req = IBA.ComponentMask(IBA.SANodeRecord());
    if isinstance(path,rdma.path.IBDRPath):
        req.nodeInfo.portGUID = portGUID;
    else:
        req.LID = path.DLID;
    ninfr = yield sched.SubnAdmGet(req);

    if portGUID != ninfr.nodeInfo.portGUID:
        raise CheckError("SA and SMP NodeInfo's differ %r != %r"%(
            portGUID,ninfr.nodeInfo.portGUID));

    try:
        npath = yield rdma.path.get_mad_path(sched,portGUID,
                                             dqpn=1,
                                             qkey=IBA.IB_DEFAULT_QP1_QKEY);
        if lib.debug >= 1:
            print "D: SA path to end port is",repr(npath);
    except rdma.path.SAPathNotFoundError:
        raise CheckError("SA could not find a path for %r"%(ninf.portGUID));
    path._cached_gmp_path = npath;

@port_check
def do_check_port(sched,path,desc,ninf,pinf,portIdx,port,sbn,**kwargs):
    """Coroutine to do the checkport action"""
    # Figure out the max speed of both sides of the link if we have topology.
    max_speed = get_max(pinf.linkSpeedSupported);
    if sbn is not None:
        peer_port = sbn.topology.get(port);
        if peer_port is not None and peer_port.pinf is not None:
            max_speed = min(max_speed,get_max(peer_port.pinf.linkSpeedSupported));
    checkEQ(pinf,"linkSpeedActive",
            max_speed,
            desc=desc,fmt=IBA_describe.link_speed);
    checkNEQ(pinf,"LID",0,desc=desc);
    checkNEQ(pinf,"masterSMLID",0,desc=desc);
    if ninf.nodeType != IBA.NODE_SWITCH:
        checkEQ(pinf,"localPortNum",portIdx,desc=desc);

@port_check
def do_check_portstate(sched,path,desc,pinf,**kwargs):
    """Coroutine to do the checkportstate action"""
    checkEQ(pinf,"portPhysicalState",IBA.PHYS_PORT_STATE_LINK_UP,
            desc=desc,error=True,fmt=IBA_describe.phys_link_state);
    checkEQ(pinf,"portState",IBA.PORT_STATE_ACTIVE,
            desc=desc,fmt=IBA_describe.link_state);

@port_check
def do_check_portwidth(sched,path,desc,pinf,port,sbn,**kwargs):
    """Coroutine to do the checkportwidth action"""
    # Figure out the max width of both sides of the link if we have topology.
    max_width = get_max(pinf.linkWidthSupported);
    if sbn is not None:
        peer_port = sbn.topology.get(port);
        if peer_port is not None and peer_port.pinf is not None:
            max_width = min(max_width,get_max(peer_port.pinf.linkWidthSupported));
    # FIXME: What about 12x ports vs three 4x ports? How is that reported?
    checkEQ(pinf,"linkWidthActive",
            max_width,
            desc=desc,
            fmt=lambda v:"%ux"%(IBA_describe.link_width(v)));

@node_check
def do_check_duplicates(sched,path,desc,pinf,port,sbn,**kwargs):
    """Coroutine to check that LIDs, port GUIDs and node GUIDs are not
    duplicated."""
    global all_lids
    global all_pguids
    global all_nguids

    for I in IBA.lid_lmc_range(pinf.LID,pinf.LMC):
        tport = all_lids.get(I);
        if tport is None:
            all_lids[I] = port;
        else:
            if tport != port:
                raise CheckError("Duplicate LIDs found, %s %s, at %s"%(
                    tport.portGUID,port.portGUID,desc));

    # Discovery will explode before it causes either of these..
    ng = port.parent.ninf.nodeGUID
    tnode = all_nguids.get(ng);
    if tnode is None:
        all_nguids[ng] = port.parent;
    else:
        if tnode != port.parent:
            raise CheckError("Duplicate node GUIDs found, GUID %s at %s"%(
                ng,desc));
    tport = all_pguids.get(port.portGUID);
    if tport is None:
        all_pguids[port.portGUID] = port;
    else:
        if tport != port:
            raise CheckError("Duplicate port GUIDs found, GUID %s at %s"%(
                port.portGUID,desc));

@perf_check
def do_check_errors(sched,path,gpath,ninf,pinf,portGUID,portIdx,**kwargs):
    """Coroutine to check the performance counters for a port."""
    ret = yield get_perf(sched,gpath,ninf,portIdx);

    if portIdx == 255:
        desc = "lid %u all ports"%(pinf.LID);
    else:
        desc = "lid %u port %u"%(pinf.LID,ret.portSelect);

    for k,v in thresh.iteritems():
        if v > 0 and hasattr(ret,k):
            checkLTE(ret,k,v,desc=desc);

@perf_check
def do_show_counts(sched,path,gpath,ninf,pinf,portGUID,portIdx,**kwargs):
    """Coroutine to display the performance counters for a port."""
    ret = yield get_perf(sched,gpath,ninf,portIdx);
    def do_print(field):
        n = field[0].upper() + field[1:];
        if not getattr(lib.args,"int_names",True):
            n = libib_name_map_perfquery.get(n,n);
        print "%s:%s%u"%(n,"."*(33 - len(n)),getattr(ret,field))
    if portIdx == 255:
        print "# Port counters: Lid %u all ports"%(pinf.LID);
    else:
        print "# Port counters: Lid %u port %u"%(pinf.LID,ret.portSelect);
    do_print("portXmitData");
    do_print("portRcvData");
    do_print("portXmitPkts");
    do_print("portRcvPkts");

@clear_check
def do_clear_counters(sched,path,gpath,ninf,pinf,portIdx,**kwargs):
    """Coroutine to clear the performance counters for a port."""
    yield get_perf(sched,gpath,ninf,portIdx,True);

@clear_check
def do_clear_error_counters(sched,path,gpath,ninf,portIdx,**kwargs):
    """Coroutine to clear the error performance counters for a port."""
    yield get_perf(sched,gpath,ninf,portIdx,True,0xFFF);

def print_header(ninf,pinf,desc,portIdx,failed,kind):
    if lib.args.verbosity >= 1 or failed or warnings:
        if desc:
            desc = " (%s) "%(IBA_describe.dstr(desc));
        else:
            desc = '';
        if kind & KIND_PORT:
            print "Port check lid %u%sport %u:"%(pinf.LID,desc,portIdx),
        if kind & KIND_PERF:
            if portIdx == 0xFF:
                print "Error check lid %u%sall ports:"%(pinf.LID,desc),
            else:
                print "Error check lid %u%sport %u:"%(pinf.LID,desc,portIdx),
        if kind & KIND_CLEAR:
            if portIdx == 0xFF:
                print "Clear counters lid %u%sall ports:"%(pinf.LID,desc),
            else:
                print "Clear counters lid %u%sport %u:"%(pinf.LID,desc,portIdx),
        if kind & KIND_NODE:
            if ninf.nodeType == IBA.NODE_SWITCH:
                print "# Checking %s: nodeguid %s lid %s"%(
                    IBA_describe.node_type(ninf.nodeType),
                    ninf.nodeGUID,pinf.LID);
            else:
                print "# Checking %s: nodeguid %s lid %s port %u"%(
                    IBA_describe.node_type(ninf.nodeType),
                    ninf.nodeGUID,pinf.LID,portIdx);
            print "Node check lid %u:"%(pinf.LID),
        if failed is not None:
            print (red("FAILED") if failed else
                   blue("WARNING") if warnings else
                   green("OK"));
    for I in warnings:
        print blue("#warn: %s"%(I));
    return not (failed or warnings);

def perform_single_check(argv,o,funcs):
    o.add_option("-N","--nocolor",action="store_false",dest="colour",
                 default=True,
                 help="Do not colorize the output");
    if not isinstance(funcs,list):
        funcs = [funcs];
    funcs.sort(key=lambda x:x.kind);
    kinds = reduce(lambda x,y:x | y,(I.kind for I in funcs));
    if kinds & KIND_PERF:
        o.add_option("-s","--show_thresholds",action="store_true",dest="show_thresh",
                     default=False,
                     help="Only show the thresholds in use.");
        o.add_option("-T",action="store",dest="load_thresh",metavar="FILE",
                     help="Load threshold values from this file.");
    LibIBOpts.setup(o);
    global lib
    if kinds & KIND_PERF:
        (args,values) = o.parse_args(argv);
        lib = LibIBOpts(o,args,values,2,(tmpl_target,tmpl_int));
        global thresh
        thresh = load_thresholds(args.load_thresh);
        if args.show_thresh:
            for I in sorted(thresh.iteritems()):
                print "%s=%u"%I
            return True;
        if len(values) < 1:
            raise CmdError("Got %u arguments but expected at least 1"%(len(values)));
        if len(values) < 2:
            values.append(0xFF);
    elif kinds & KIND_PORT:
        (args,values) = o.parse_args(argv,expected_values=2);
        lib = LibIBOpts(o,args,values,2,(tmpl_target,tmpl_int));
    else:
        (args,values) = o.parse_args(argv,expected_values=1);
        lib = LibIBOpts(o,args,values,1,(tmpl_target,));

    with lib.get_umad_for_target(values[0]) as umad:
        sched = lib.get_sched(umad);
        path = lib.path
        kwargs = {};
        kwargs["sbn"] = None;
        kwargs["port"] = None;
        kwargs["ninf"] = ninf = umad.SubnGet(IBA.SMPNodeInfo,path);
        if kinds & (KIND_PERF | KIND_PORT):
            kwargs["portIdx"] = values[1];
        if kinds & KIND_PORT:
            kwargs["pinf"] = pinf = umad.SubnGet(IBA.SMPPortInfo,path,values[1]);
            kwargs["desc"] = "lid %u port %u"%(pinf.LID,values[1]);
        else:
            kwargs["pinf"] = pinf = umad.SubnGet(IBA.SMPPortInfo,path);
        kwargs["portGUID"] = portGUID = kwargs["ninf"].portGUID;
        nodeDesc = None;
        if kinds & KIND_PERF:
            nodeDesc = IBA_describe.description(umad.SubnGet(IBA.SMPNodeDescription,path).nodeString);

        def done_checks(kind,failed=False):
            if kind & KIND_PERF and warnings:
                failed = True;
            if lib.args.verbosity >= 1:
                print (red("FAILED") if failed else
                       blue("WARNING") if warnings else
                       green("OK"));
                for I in warnings:
                    print blue("#warn: %s"%(I));
            else:
                print_header(ninf,pinf,nodeDesc,ninf.localPortNum,failed,
                             kind);

        try:
            printed = 0;
            last_kind = 0;
            for func in funcs:
                if lib.args.verbosity >= 1 and not (printed & func.kind):
                    print_header(ninf,pinf,nodeDesc,ninf.localPortNum,None,
                                 func.kind);

                if printed != 0 and last_kind != func.kind:
                    done_checks(last_kind);
                printed = printed | func.kind;
                last_kind = func.kind;

                if func.kind & (KIND_PERF|KIND_CLEAR) and "gpath" not in kwargs:
                    kwargs["gpath"] = gpath = getattr(path,"_cached_gmp_path",None);
                    if gpath is None:
                        gpath = rdma.path.get_mad_path(umad,portGUID,
                                                       dqpn=1,
                                                       qkey=IBA.IB_DEFAULT_QP1_QKEY);
                        path._cached_gmp_path = gpath;
                        kwargs["gpath"] = gpath;

                del warnings[:];
                sched.run(queue=func(sched,path,**kwargs));
        except (CmdError,rdma.RDMAError):
            done_checks(last_kind,True);
            raise
        done_checks(last_kind);
    return lib.done();

def cmd_ibchecknode(argv,o):
    """Check SMPNodeInfo, SMPPortInfo and SANodeInfoRecord for a node.
       Usage: %prog TARGET"""
    return perform_single_check(argv,o,do_check_node)

def cmd_ibcheckport(argv,o):
    """Check portPhysicalState, portState, linkWidthActive and linkSpeed on a port.
       Usage: %prog TARGET PORT"""
    return perform_single_check(argv,o,[do_check_portstate,
                                        do_check_portwidth,
                                        do_check_port])

def cmd_ibcheckportstate(argv,o):
    """Check portPhysicalState, and portState
       Usage: %prog TARGET PORT"""
    return perform_single_check(argv,o,do_check_portstate)

def cmd_ibcheckportwidth(argv,o):
    """Check linkWidthActive
       Usage: %prog TARGET PORT"""
    return perform_single_check(argv,o,do_check_portwidth)

def cmd_ibcheckerrs(argv,o):
    """Check PMPortCounters for error values
       Usage: %prog TARGET [PORT]"""
    return perform_single_check(argv,o,do_check_errors)

def cmd_ibdatacounts(argv,o):
    """Check PMPortCounters for error values
       Usage: %prog TARGET [PORT]"""
    return perform_single_check(argv,o,do_show_counts)

def perform_topo_check(argv,o,funcs):
    o.add_option("-N","--nocolor",action="store_false",dest="colour",
                 default=True,
                 help="Do not colorize the output");
    if not isinstance(funcs,list):
        funcs = [funcs];
    funcs.sort(key=lambda x:x.kind);
    kinds = reduce(lambda x,y:x | y,(I.kind for I in funcs));
    if kinds & KIND_PERF:
        o.add_option("-T",action="store",dest="load_thresh",metavar="FILE",
                     help="Load threshold values from this file.");
    LibIBOpts.setup(o,address=False,discovery=True);
    global lib
    (args,values) = o.parse_args(argv,expected_values=0);
    lib = LibIBOpts(o,args,values);

    if kinds & KIND_PERF:
        global thresh
        thresh = load_thresholds(args.load_thresh);

    def run(path,port,portIdx,kind):
        node = port.parent
        failed = False;
        cidx = (0 if kind == KIND_NODE else
                2 if kind == KIND_PORT else
                4 if kind == KIND_PERF else
                6 if kind == KIND_CLEAR else
                0);
        kwargs = {};
        kwargs["ninf"] = node.ninf;
        kwargs["pinf"] = port.pinf;
        kwargs["port"] = port;
        kwargs["sbn"] = sbn;
        kwargs["portIdx"] = portIdx;
        kwargs["desc"] = "lid %u port %s"%(port.LID,portIdx);
        kwargs["portGUID"] = portGUID = port.to_end_port().portGUID;

        if kind & (KIND_PERF|KIND_CLEAR):
            kwargs["gpath"] = gpath = getattr(path,"_cached_gmp_path",None);
            if gpath is None:
                gpath = yield rdma.path.get_mad_path(sched,portGUID,
                                                     dqpn=1,
                                                     qkey=IBA.IB_DEFAULT_QP1_QKEY);
                path._cached_gmp_path = gpath;
                kwargs["gpath"] = gpath;

        del warnings[:]
        try:
            counts[cidx] = counts[cidx] + 1;
            for func in funcs:
                if func.kind & kind:
                    yield func(sched,path,**kwargs);
        except (CmdError,rdma.RDMAError), e:
            counts[cidx+1] = counts[cidx+1] + 1;
            sched.result = print_header(node.ninf,port.pinf,node.desc,portIdx,True,kind);
            print red("#error: %s"%(e));
        else:
            failed = False;
            if kind & KIND_PERF and warnings:
                if portIdx != 0xFF:
                    counts[cidx+1] = counts[cidx+1] + 1;
                failed = True;
            sched.result = print_header(node.ninf,port.pinf,node.desc,portIdx,failed,kind);

    counts = [0]*8;
    with lib.get_umad() as umad:
        sched = lib.get_sched(umad);
        sbn = lib.get_subnet(sched,("all_NodeInfo","all_PortInfo",
                                    "all_NodeDescription"));
        def do(port):
            """This is a coroutine that does the checks for one end port."""
            path = sbn.get_path_smp(sched,port);
            if kinds & KIND_NODE:
                yield run(path,port,port.port_id,KIND_NODE);
            kind = KIND_NODE*2;
            while kind <= kinds:
                if not kinds & kind:
                    kind = kind*2;
                    continue
                if isinstance(port.parent,rdma.subnet.Switch):
                    # Use all port select on switches, if that
                    # has threshold errors then scan each port for
                    # better diagnostics.
                    ret = False;
                    if kind & (KIND_PERF|KIND_CLEAR):
                        ret = yield run(path,port,0xFF,kind);
                    if ret == False:
                        for I,idx in port.parent.iterports():
                            if not (kind & (KIND_PERF|KIND_CLEAR) and idx == 0):
                                yield run(path,I,idx,kind);
                else:
                    yield run(path,port,port.port_id,kind);
                kind = kind*2;
        sched.run(mqueue=(do(I) for I in sbn.iterend_ports()));
    print "## Summary: %u nodes checked, %u bad nodes found"%(counts[0],counts[1]);
    if kinds & KIND_PORT:
        print "##          %u ports checked, %u ports with bad state found"%(counts[2],counts[3]);
    if kinds & KIND_PERF:
        print "##          %u ports checked, %u ports have errors beyond threshold"%(counts[4],counts[5]);
    if kinds & KIND_CLEAR:
        print "##          %u port counters cleared."%(counts[6]);
    return lib.done();

def cmd_ibcheckstate(argv,o):
    """Run ibchecknode over every node in the network and ibcheckportstate over every port.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_check_node,
                                      do_check_portstate]);

def cmd_ibcheckwidth(argv,o):
    """Run ibchecknode over every node in the network and ibcheckportwidth over every port.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_check_node,
                                      do_check_portwidth]);

def cmd_ibchecknet(argv,o):
    """Run ibchecknode over every node in the network and ibcheckport plus ibcheckerrs over every port.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_check_node,
                                      do_check_portstate,
                                      do_check_portwidth,
                                      do_check_port,
                                      do_check_errors]);

def cmd_ibcheckerrors(argv,o):
    """Run ibchecknode over every node in the network and ibcheckerrs over every port.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_check_node,
                                      do_check_portstate,
                                      do_check_errors]);

def cmd_ibclearcounters(argv,o):
    """Clear all PMPortCounters on every port.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_clear_counters]);

def cmd_ibclearerrors(argv,o):
    """Clear only error counters in PMPortCounters on every port.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_clear_error_counters]);

def cmd_ibdatacounters(argv,o):
    """Show data counters for all ports.
       Usage: %prog"""
    return perform_topo_check(argv,o,[do_show_counts]);

def cmd_ibidsverify(argv,o):
    """Check that there are no duplicate LIDs, nodeGUIDS or portGUIDs in the
       network.
       Usage: %prog

       Note: The discovery process relies on the portGUID to detect looping,
       so duplicates cannot be reliably detected."""
    global all_lids
    global all_pguids
    global all_nguids
    all_lids = {}
    all_pguids = {}
    all_nguids = {}
    return perform_topo_check(argv,o,[do_check_duplicates]);
