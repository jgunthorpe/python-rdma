from __future__ import with_statement;
import inspect
import sys;
import copy;
import rdma;
import rdma.path;
import rdma.sched;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
from libibtool import *;
from libibtool.libibopts import *;

def arg_nr(query,values):
    """LID"""
    query.LID = IBA.conv_lid(values[0]);
    del values[0];

def arg_pir(query,values):
    """[LID]/[PORT]"""
    s = values[0].split('/');
    if s[0]:
        query.LID = IBA.conv_lid(s[0]);
    if s[1]:
        query.portNum = int(s[1],0);
    del values[0];

def arg_sl2vl(query,values):
    """[lid]/[in_port]/[out_port]"""
    s = values[0].split('/');
    if s[0]:
        query.LID = IBA.conv_lid(s[0]);
    if s[1]:
        query.inputPortNum = int(s[1],0);
    if s[2]:
        query.outputPortNum = int(s[2],0);
    del values[0];

def arg_pkey(query,values):
    """[lid]/[port]/[block]"""
    s = values[0].split('/');
    if s[0]:
        query.LID = IBA.conv_lid(s[0]);
    if s[1]:
        query.portNum = int(s[1],0);
    if s[2]:
        query.blockNum = int(s[2],0);
    del values[0];

def arg_vlarb(query,values):
    """[lid]/[port]/[block]"""
    s = values[0].split('/');
    if s[0]:
        query.LID = IBA.conv_lid(s[0]);
    if s[1]:
        query.outputPortNum = int(s[1],0);
    if s[2]:
        query.blockNum = int(s[2],0);
    del values[0];

def arg_link(query,values):
    """[from_lid]/[from_port] [to_lid]/[to_port]"""
    s = values[0].split('/');
    if s[0]:
        query.fromLID = IBA.conv_lid(s[0]);
    if s[1]:
        query.fromPort = int(s[1],0);
    del values[0];

    if not values:
        return;

    s = values[0].split('/');
    if s[0]:
        query.toLID = IBA.conv_lid(s[0]);
    if s[1]:
        query.toPort = int(s[1],0);
    del values[0];

def arg_lft(query,values):
    """[lid]/[block]"""
    s = values[0].split('/');
    if s[0]:
        query.LID = IBA.conv_lid(s[0]);
    if s[1]:
        query.blockNum = int(s[1],0);
    del values[0];

def arg_mft(query,values):
    """[lid]/[block]"""
    s = values[0].split('/');
    if s[0]:
        query.LID = IBA.conv_lid(s[0]);
    if s[1]:
        query.blockNum = int(s[1],0);
    del values[0];

OPS = {"ClassPortInfo": ("CPI",IBA.MADClassPortInfo),
       "GUIDInfoRecord": ("",IBA.SAGUIDInfoRecord),
       "InformInfoRecord": ("IIR",IBA.SAInformInfoRecord),
       "LFTRecord": ("LFTR",IBA.SALinearForwardingTableRecord,arg_lft),
       "LinkRecord": ("LR",IBA.SALinkRecord,arg_link),
       "MCMemberRecord": ("MCMR",IBA.SAMCMemberRecord),
        # "MultiPathRecord": ("",IBA.SAMultiPathRecord),
       "MFTRecord": ("MFTR",IBA.SAMulticastForwardingTableRecord,arg_mft),
       "NodeRecord": ("NR",IBA.SANodeRecord,arg_nr),
       "PKeyTableRecord": ("PKTR",IBA.SAPKeyTableRecord,arg_pkey),
       "PathRecord": ("PR",IBA.SAPathRecord),
       "PortInfoRecord": ("PIR",IBA.SAPortInfoRecord,arg_pir),
       "RFTRecord": ("",IBA.SARandomForwardingTableRecord),
       "SL2VLTableRecord": ("SL2VL",IBA.SASLToVLMappingTableRecord,arg_sl2vl),
       "SMInfo": ("",IBA.SASMInfoRecord),
       "ServiceAssociationRecord": ("",IBA.SAServiceAssociationRecord),
       "ServiceRecord": ("SR",IBA.SAServiceRecord),
       "SwitchInfo": ("SWI",IBA.SASwitchInfoRecord),
       "VLArbitrationTableRecord": ("VLAR",IBA.SAVLArbitrationTableRecord,arg_vlarb),
       };

def set_mad_attr(attr,name,v):
    try:
        # Need to use eval because name could have dots in it.
        arg = eval("attr.%s"%(name))
    except AttributeError:
        raise CmdError("%r is not a valid attribute for %r"%(name,attr));
    try:
        if isinstance(arg,int) or isinstance(arg,long):
            v = int(v,0);
        elif isinstance(arg,IBA.GID):
            v = IBA.GID(v);
        elif isinstance(arg,IBA.GUID):
            v = IBA.GUID(v);
        elif isinstance(arg,bytearray):
            v = v.decode("string_escape");
            if len(v) > len(arg):
                raise CmdError("String %r is too long, can only be up to %u"%(
                    v,len(arg)));
            if len(v) < len(arg):
                v = v + bytearray(len(arg) - len(v));
        elif isinstance(arg,list):
            raise CmdError("Lists currently cannot be set.");
        else:
            raise CmdError("Internal Error, I don't know what %s %r is."%(
                type(arg),arg));
    except ValueError as err:
        raise CmdError("String %r did not parse: %s"%(v,err));
    exec "attr.%s = v"%(name)

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

class Indentor(object):
    def __init__(self,F):
        self.F = F;
        self._next_tab = True;

    def write(self,v):
        if self._next_tab:
            self.F.write("\t\t");
            self._next_tab = False;

        if v[-1] == '\n':
            v = v[:-1];
            self._next_tab = True;
        self.F.write(v.replace("\n","\n\t\t"));
        if self._next_tab:
            self.F.write("\n");

def do_print(out,s):
    """Special printing for some things to look like libib."""
    if isinstance(s,IBA.SANodeRecord):
        ninf = s.nodeInfo;
        desc = s.nodeDescription;
        s.nodeInfo = None;
        s.nodeDescription = None;
        if _format_args.get("name_map") is not None:
            args = copy.copy(_format_args);
            args["column"] = 24;
        else:
            args = _format_args;
        s.printer(out,**args);
        ninf.printer(out,**args);
        print >> out,"NodeDescription..........%s"%(IBA_describe.dstr(IBA_describe.description(desc.nodeString)));
    elif isinstance(s,IBA.SAPortInfoRecord):
        pinf = s.portInfo;
        s.portInfo = None;
        print "\tRID:"
        s.printer(out,**_format_args);
        print "\tPortInfo dump:"
        if _format_args.get("name_map") is not None:
            args = copy.copy(_format_args);
            args["name_map"] = libib_name_map_smpquery;
            args["colon"] = True;
            args["column"] = 33;
        else:
            args = _format_args;
        pinf.printer(out,**args);
    elif isinstance(s,IBA.SASwitchInfoRecord):
        sinf = s.switchInfo;
        s.switchInfo = None;
        print "\tRID:"
        s.printer(out,**_format_args);
        print "\tSwitchInfo dump:"
        if _format_args.get("name_map") is not None:
            args = copy.copy(_format_args);
            args["name_map"] = libib_name_map_smpquery;
            args["colon"] = True;
            args["column"] = 33;
        else:
            args = _format_args;
        sinf.printer(out,**args);
    elif isinstance(s,IBA.SAMulticastForwardingTableRecord):
        ft = s.multicastForwardingTable.portMaskBlock;
        s.multicastForwardingTable = None;
        s.printer(out,**_format_args);
        print >> out,"MFT:"
        print >> out,"MLID\tPort Mask"
        for I,v in enumerate(ft):
            print >> out,"0x%x\t0x%x"%(IBA.LID_MULTICAST + I + s.blockNum*32,v);
    elif isinstance(s,IBA.SALinearForwardingTableRecord):
        ft = s.linearForwardingTable.portBlock;
        s.linearForwardingTable = None;
        s.printer(out,**_format_args);
        print >> out,"LFT:"
        print >> out,"LID\tPort Number"
        for I,v in enumerate(ft):
            print >> out,"%u\t%u"%(I + s.blockNum*64,v);
    elif isinstance(s,IBA.SAPKeyTableRecord):
        pk = s.PKeyTable.PKeyBlock;
        s.PKeyTable = None;
        s.printer(out,**_format_args);
        print >> out,"PKey Table:"
        for num,I in enumerate(pk):
            if num % 8 == 0:
                if num != 0:
                    print >> out;
            print >> out,"0x%04x"%(I),
        print >> out;
    elif isinstance(s,IBA.SAVLArbitrationTableRecord):
        vl = s.VLArbitrationTable.VLWeightBlock;
        s.VLArbitrationTable = None;
        s.printer(out,**_format_args);
        print >> out, "VL    :" + "|".join(("%2u"%((I >> 8) & 0xF)) for I in vl[:16]) + "|";
        print >> out, "Weight:" + "|".join(("%2u"%(I & 0xFF)) for I in vl[:16]) + "|";
        print >> out, "VL    :" + "|".join(("%2u"%((I >> 8) & 0xF)) for I in vl[16:]) + "|";
        print >> out, "Weight:" + "|".join(("%2u"%(I & 0xFF)) for I in vl[16:]) + "|";
    else:
        s.printer(out,**_format_args);

def cmd_saquery_help(o,cmd,usage):
    """Generate the help text by merging in information from OPS."""
    def doc_op():
        for k,v in OPS.iteritems():
            if v[0]:
                yield "%s %s"%(k,v[0]);
            else:
                yield k;
            if len(v) >= 3:
                yield "   ARG: %s"%(inspect.getdoc(v[2]));

    for I in o.option_list:
        if I.dest and I.dest.startswith("X_"):
            name = I.dest[2:];
            I.metavar = "MATCH";
            I.help = "Match using the %s member."%(name);
            ret = [];
            for k,v in OPS.iteritems():
                if name in v[1].COMPONENT_MASK:
                    ret.append(k);
            if ret:
                I.help += " Use with: %s"%(", ".join(ret));
        if I.dest == "kind":
            for k,v in OPS.iteritems():
                if v[1] == I.const:
                    I.help = "Perform a query for %s"%(k);
                    break;
    return usage + "\n    " + "\n    ".join(doc_op());

def cmd_saquery(argv,o):
    """Issue a SubnAdmGetTable() request to the SA for an attribute
       Usage: %prog saquery [OPTIONS] [ITEM] [ARG] [MEMBER=VALUE]*

       This command performs a search at the SA for ITEM things that match
       the pattern. Each SA search is specified by setting matching parameters
       in the request. The search to perform can be specified via an option
       or via the ITEM argument. If an option is specified then ITEM is ignored.

       Each search type supports an optional quick matching ARG which is type
       specific. The ARG sets fields to match. After ARG is a series of
       MEMBER=VALUE lines which specify named fields to match. eg
       nodeInfo.portGUID=0017:77ff:feb6:2ca4 will match NodeRecords with
       that port GUID.

       There are also several option shortcuts that are equivalent to the above
       with different field names.

       Supported ITEM:
       """
    # FIXME: selector/*
    LibIBOpts.setup(o,address=False);
    o.add_option("-p",action="store_const",dest="kind",
                 const=IBA.SAPathRecord);
    o.add_option("-N",action="store_const",dest="kind",
                 const=IBA.SANodeRecord);
    o.add_option("-g",action="store_const",dest="kind",
                 const=IBA.SAMCMemberRecord);
    o.add_option("-m",action="store_const",dest="kind",
                 const=IBA.SAMCMemberRecord);
    o.add_option("-x",action="store_const",dest="kind",
                 const=IBA.SALinkRecord);
    o.add_option("-c",action="store_const",dest="kind",
                 const=IBA.MADClassPortInfo);
    o.add_option("-I",action="store_const",dest="kind",
                 const=IBA.SAInformInfoRecord);

    o.add_option("--dlid",action="store",dest="X_DLID");
    o.add_option("--slid",action="store",dest="X_SLID");
    o.add_option("--mlid",action="store",dest="X_MLID");
    o.add_option("--sgid",action="store",dest="X_SGID");
    o.add_option("--dgid",action="store",dest="X_DGID");
    o.add_option("--gid",action="store",dest="X_portGID");
    o.add_option("--mgid",action="store",dest="X_MGID");
    o.add_option("-r","--reversible",action="store",dest="X_reversible");
    o.add_option("-n","--numb_path",action="store",dest="X_numbPath");
    o.add_option("--pkey",action="store",dest="X_PKey");
    o.add_option("-Q","--qos_class",action="store",dest="X_QOSClass");
    o.add_option("--sl",action="store",dest="X_SL");
    o.add_option("-M","--mtu",action="store",dest="X_MTU");
    o.add_option("-R","--rate",action="store",dest="X_rate");
    o.add_option("--pkt_lifetime",action="store",dest="X_packetLifeTime");
    o.add_option("-q","--qkey",action="store",dest="X_QKey");
    o.add_option("-T","--tclass",action="store",dest="X_TClass");
    o.add_option("-f","--flow_label",action="store",dest="X_flowLabel");
    o.add_option("-H","--hop_limit",action="store",dest="X_hopLimit");
    o.add_option("--scope",action="store",dest="X_scope");
    o.add_option("-J","--join_state",action="store",dest="X_joinState");
    o.add_option("-X","--proxy_join",action="store",dest="X_proxyJoin");

    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args);

    global _format_args
    _format_args = lib.format_args;
    if _format_args["format"] != "dotted":
        out = sys.stdout;
    else:
        out = Indentor(sys.stdout);

    if args.kind is None:
        if len(values) < 1:
            args.kind = IBA.SANodeRecord;
        else:
            args.kind = tmpl_op(values[0])[1];
            del values[0];

    to_set = []
    for elm in range(len(values)-1,-1,-1):
        I = values[elm];
        idx = I.find("=");
        if idx == -1:
            del values[elm+1:];
            break;
        to_set.insert(0,(I[:idx],I[idx+1:]));
    else:
        del values[:];

    query = args.kind();
    query_cm = IBA.ComponentMask(query);
    if len(values) >= 1:
        # The first value(s) are a kind specific thing, parsed with the kind
        # helper.
        for v in OPS.itervalues():
            if v[1] == args.kind and len(v) >= 3:
                try:
                    v[2](query_cm,values);
                except ValueError:
                    raise CmdError("Argument %r did not match %s"%(
                        values[0],v[2].__doc__));

    if values:
        raise CmdError("Arguments %r are not understood."%(values));

    # Parse command line options that set members.
    for I in dir(args):
        if not I.startswith("X_"):
            continue;
        arg = getattr(args,I);
        if arg is not None:
            to_set.append((I[2:],arg));

    if to_set and getattr(query,"COMPONENT_MASK",None) is None:
        raise CmdError("Cannot set member queries with type %s"%(
            query.__class__.__name__));

    # Set member arguments using introspection.
    for n,v in to_set:
        if n not in query.COMPONENT_MASK:
            raise CmdError("Cannot set member %s on %s. Try one of %s"%(
                n,query.__class__.__name__,", ".join(query.COMPONENT_MASK.iterkeys())));
        set_mad_attr(query_cm,n,v);

    # Diagnostic output to show what the query argument is.
    if o.verbosity >= 1:
        cm = query_cm.component_mask;
        ret = [];
        for k,v in query.COMPONENT_MASK.iteritems():
            if cm & (1 << v):
                ret.append((v,k,eval("query_cm.%s"%(k))))
        ret.sort();
        if ret:
            print "Performing query on %s with component mask:"%(query.__class__.__name__);
            for v,k,arg in ret:
                print "  %2u %s = %r"%(v,k,arg);

    with lib.get_umad(gmp=True) as umad:
        path = umad.end_port.sa_path;

        name_map = _format_args.get("name_map",{});
        if getattr(query,"MAD_SUBNADMGETTABLE",None) is None:
            ret = umad.SubnAdmGet(query_cm,path);
            n = ret.__class__.__name__;
            print "%s:"%(name_map.get(n,n));
            do_print(out,ret);
        else:
            ret = umad.SubnAdmGetTable(query_cm,path);
            for I in ret:
                n = I.__class__.__name__;
                print "%s dump:"%(name_map.get(n,n));
                do_print(out,I);
    return True;
