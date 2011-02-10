from __future__ import with_statement;
import sys;
import rdma;
import rdma.path;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
from libibtool import *;
from libibtool.libibopts import *;

def do_ni(umad,kind,path,attr):
    print "# Node info:",path;
    ni = umad.SubnGet(kind,path,attr);
    ni.printer(sys.stdout,**_format_args);

def do_nd(umad,kind,path,attr):
    nd = umad.SubnGet(kind,path,attr);
    print "Node Description: %r"%(IBA_describe.description(nd.nodeString));

def do_pi(umad,kind,path,attr):
    print "# Port info:",path;
    pi = umad.SubnGet(kind,path,attr);
    pi.printer(sys.stdout,**_format_args);

def do_si(umad,kind,path,attr):
    print "# Switch info:",path;
    si = umad.SubnGet(kind,path,attr);
    si.printer(sys.stdout,**_format_args);

def do_pkeys(umad,kind,path,attr):
    ni = umad.SubnGet(IBA.SMPNodeInfo,path);
    if attr > ni.numPorts:
        raise CmdError("Invalid port number");
    if ni.nodeType == IBA.NODE_SWITCH and attr != 0:
        si = umad.SubnGet(IBA.SMPSwitchInfo,path);
        count = si.partitionEnforcementCap
    else:
        count = ni.partitionCap;

    pkeys = [];
    for I in range((count+31)//32):
        pkeys.extend(umad.SubnGet(kind,path,(attr << 16) | I).PKeyBlock);

    for num,I in enumerate(pkeys[:count]):
        if num % 8 == 0:
            if num != 0:
                print;
            print "%4u:"%(num),
        print "0x%04x"%(I),
    if count != 0:
        print;
    print "%u pkeys capacity for this port"%(count);

def do_sl2vl(umad,kind,path,attr):
    ni = umad.SubnGet(IBA.SMPNodeInfo,path);

    if ni.nodeType == IBA.NODE_SWITCH:
        sl2vl = [None]*(ni.numPorts+1);
        for I in range(ni.numPorts+1):
            sl2vl[I] = umad.SubnGet(kind,path,I << 8 | attr).SLtoVL;
    else:
        attr = ni.localPortNum;
        sl2vl = (umad.SubnGet(kind,path,attr).SLtoVL,);

    print "# SL2VL table",path
    print "#                 SL: |" + "|".join("%2u"%(I) for I in range(16))+"|";
    for iport,I in enumerate(sl2vl):
        print "ports: in %2u, out %2u: |"%(iport,attr) + "|".join("%2u"%(J) for J in I)+"|";

def dump_vlarb(umad,path,attr,name,offset,cap):
    print "# %s priority VL Arbitration Table:"%(name);
    vl = [];
    for I in range((cap + 31)//32):
        vl.extend(umad.SubnGet(IBA.SMPVLArbitrationTable,path,
                               (offset + I) << 16 | attr).VLWeightBlock);
    print "VL    : |" + "|".join("%-4s"%("0x%x"%((I >> 8) & 0xF)) for I in vl[:cap]) + "|";
    print "WEIGHT: |" + "|".join("%-4s"%("0x%x"%(I & 0xFF)) for I in vl[:cap]) + "|";

def do_vlarb(umad,kind,path,attr):
    ni = umad.SubnGet(IBA.SMPNodeInfo,path);
    if attr == 0:
        if ni.nodeType == IBA.NODE_SWITCH:
            si = umad.SubnGet(IBA.SMPSwitchInfo,path);
            if not si.enhancedPort0:
                print "# No VLArbitration tables (BSP0): %s port %u"%(path,attr);
                return;

    pi = umad.SubnGet(IBA.SMPPortInfo,path,attr);
    print "# VLArbitration tables: %s port %u LowCap %u High Cap %u"%(
        path,attr,pi.VLArbitrationLowCap,pi.VLArbitrationHighCap);
    if pi.VLArbitrationLowCap > 0:
        dump_vlarb(umad,path,attr,"Low",1,pi.VLArbitrationLowCap);
    if pi.VLArbitrationHighCap > 0:
        dump_vlarb(umad,path,attr,"High",3,pi.VLArbitrationHighCap);

def do_guid(umad,kind,path,attr):
    pi = umad.SubnGet(IBA.SMPPortInfo,path);
    count = pi.GUIDCap;

    guids = [];
    for I in range((count+7)//8):
        guids.extend(umad.SubnGet(kind,path,(attr << 16) | I).GUIDBlock);

    for num,I in enumerate(guids[:count]):
        if num % 2 == 0:
            if num != 0:
                print;
            print "%4u:"%(num),
        print I,
    if count != 0:
        print;
    print "%u guids capacity for this port"%(count);

OPS = {"NodeInfo": ("NI",IBA.SMPNodeInfo,do_ni),
       "NodeDesc": ("ND",IBA.SMPNodeDescription,do_nd),
       "PortInfo": ("PI",IBA.SMPPortInfo,do_pi),
       "SwitchInfo": ("SI",IBA.SMPSwitchInfo,do_si),
       "PKeyTable": ("PKeys",IBA.SMPPKeyTable,do_pkeys),
       "SL2VLTable": ("SL2VL",IBA.SMPSLToVLMappingTable,do_sl2vl),
       "VLArbitration": ("VLArb",IBA.SMPVLArbitrationTable,do_vlarb),
       "GUIDInfo": ("GI",IBA.SMPGUIDInfo,do_guid)};

def tmpl_op(s):
    s = s.lower();
    res = None;
    for k,v in OPS.iteritems():
        k = k.lower();
        k2 = v[0].lower();
        k3 = v[1].__name__.lower();
        if (k == s or k.startswith(s) or
            k2 == s or k2.startswith(s) or
            k3 == s or k3.startswith(s)):
            if res is not None:
                raise CmdError("Ambiguous operation %r"%(s));
            res = v;
    if res is None:
        raise CmdError("Unknown operation %r"%(s));
    return res;

def cmd_smpquery_help(o,cmd,usage):
    """Generate the help text by merging in information from OPS."""
    def doc_op():
        for k,v in OPS.iteritems():
            if v[0]:
                yield "%s %s"%(k,v[0]);
            else:
                yield k;
    return usage + "\n    " + "\n    ".join(doc_op());

def cmd_smpquery(argv,o):
    """Display a SMP record
       Usage: %prog smpdump OP TARGET [ATTR_MOD]

       Supported OP:
       """
    LibIBOpts.setup(o);
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,3,(tmpl_op,tmpl_target,tmpl_int));
    if len(values) < 2:
        raise CmdError("Too few arguments");

    global _format_args
    _format_args = lib.format_args;

    with lib.get_umad_for_target(values[1]) as umad:
        values[0][2](umad,values[0][1],lib.path,values[2] if len(values) >= 3 else 0);
    return True;
