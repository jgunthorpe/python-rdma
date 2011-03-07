from __future__ import with_statement;
import sys;
import rdma;
import rdma.path;
import rdma.IBA as IBA;
from libibtool import *;
from libibtool.libibopts import *;

def do_print(res,path):
    if path.DGID is not None:
        print "# Port counters: Lid %u (%s) port %u"%(path.DLID,path.DGID,res.portSelect);
    else:
        print "# Port counters: Lid %u port %u"%(path.DLID,res.portSelect);
    res.printer(sys.stdout,**_format_args);

def cmd_perfquery(argv,o):
    """Display the performance manager values for a port
       Usage: %prog perfquery [TARGET [PORT [RESET]]]"""

    o.add_option("-x","--extended",action="store_const",dest="kind",
                 const=IBA.PMPortCountersExt,
                 help="Show extended port counters");
    o.add_option("-X","--xmtsl",action="store_const",dest="kind",
                 const=IBA.PMPortXmitDataSL,
                 help="Show transmit SL port counters");
    o.add_option("-S","--rcvsl",action="store_const",dest="kind",
                 const=IBA.PMPortRcvDataSL,
                 help="Show receive SL port counters");
    o.add_option("-D","--xmtdisc",action="store_const",dest="kind",
                 const=IBA.PMPortXmitDiscardDetails,
                 help="Show transmit discard details");
    o.add_option("-E","--rcverr",action="store_const",dest="kind",
                 const=IBA.PMPortRcvErrorDetails,
                 help="Show receive error details");
    o.add_option("-F","--flow",action="store_const",dest="kind",
                 const=IBA.PMPortFlowCtlCounters,
                 help="Show port flow control counters");
    o.add_option("--vl-xmit-errs",action="store_const",dest="kind",
                 const=IBA.PMPortVLXmitFlowCtlUpdateErrors,
                 help="Show port flow control transmit update errors");
    o.add_option("--vl-xmit-wait",action="store_const",dest="kind",
                 const=IBA.PMPortVLXmitWaitCounters,
                 help="Show port flow control transmit wait counts");
    o.add_option("--vl-congestion",action="store_const",dest="kind",
                 const=IBA.PMSwPortVLCongestion,
                 help="Show switch port per VL congestion");

    o.add_option("-a","--all_ports",action="store_true",dest="all",
                 help="Show/reset aggregated counters");
    o.add_option("-l","--loop_ports",action="store_true",dest="loop",
                 help="Show/reset all ports");
    o.add_option("-r","--reset_after_read",action="store_true",dest="reset",
                 help="Reset counters after reading");
    o.add_option("-R","--Reset_only",action="store_true",dest="reset_only",
                 help="Reset counters without any display");
    LibIBOpts.setup(o);
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,3,(tmpl_target,tmpl_int,tmpl_int));

    if len(values) == 0:
        values = ('',);

    global _format_args
    _format_args = lib.format_args;

    if args.kind is None:
        args.kind = IBA.PMPortCounters;

    with lib.get_umad_for_target(values[0],gmp=True) as umad:
        path = lib.path;

        cnts = args.kind();

        nr = None;
        cpinf = None;
        if args.all:
            cnts.portSelect = 0xFF;
        elif len(values) >= 2:
            cnts.portSelect = values[1];
        elif not values[0]:
            cnts.portSelect = umad.end_port.port_id;
        else:
            # Hmm. Lets be smarter here, display the 'natural' port number
            # for HCAs, and something random for switches. I think this is
            # better than returning an invalid port select error code.
            #ninf = umad.SubnGet(IBA.SMPNodeInfo,path.copy(dqpn=0,sqpn=0));
            #cnts.portSelect = ninf.localPortNum;
            nr = IBA.ComponentMask(IBA.SANodeRecord());
            nr.LID = path.DLID;
            nr = umad.SubnAdmGet(nr);
            cnts.portSelect = nr.nodeInfo.localPortNum;
            if nr.nodeInfo.nodeType == IBA.NODE_SWITCH and cnts.portSelect == 0:
                cnts.portSelect = 1;

        accumulate = args.loop;
        if cnts.portSelect == 0xFF:
            cpinf = umad.PerformanceGet(IBA.MADClassPortInfo,path);
            path.resp_time = cpinf.respTimeValue;
            accumulate = not (cpinf.capabilityMask & IBA.allPortSelect);

        if accumulate:
            if not args.loop:
                print "Emulating AllPortSelect by iterating through all ports";
            if nr is None:
                nr = IBA.ComponentMask(IBA.SANodeRecord());
                nr.LID = path.DLID;
                nr = umad.SubnAdmGet(nr);
            if nr.nodeInfo.nodeType == IBA.NODE_CA:
                raise CmdError("Can't iterate over all ports on a CA.");
            numPorts = nr.nodeInfo.numPorts;
            if path.DGID is None:
                path.DGID = IBA.GID(prefix=IBA.GID_DEFAULT_PREFIX,
                                    guid=nr.nodeInfo.portGUID);

        reset = args.reset_only or args.reset;
        if reset:
            if len(values) >= 3:
                cnts.counterSelect = values[2];
                try:
                    cnts.counterSelect2 = values[2] >> 16;
                except AttributeError:
                    pass;
            else:
                cnts.counterSelect = 0xFFFF;
                if cpinf is None:
                    cpinf = umad.PerformanceGet(IBA.MADClassPortInfo,path);
                    path.resp_time = cpinf.respTimeValue;
                if cpinf.capabilityMask & IBA.portCountersXmitWaitSupported:
                    cnts.counterSelect2 = 0xFF;

        # The port does not support all counters. Accumulate the port select
        # values manually. Note this does not work for HCA ports since
        # we cannot access them using only port select.
        if accumulate:
            def get_cnts(sched,res,port,path):
                if not args.reset_only:
                    cnts.portSelect = port;
                    res[port] = yield sched.PerformanceGet(cnts,path);
                if reset:
                    cnts.portSelect = port;
                    yield sched.PerformanceSet(cnts,path);

            sched = lib.get_sched(umad,path);
            results = [None]*(numPorts+1);
            sched.run(mqueue=(get_cnts(sched,results,I,path)
                              for I in range(1,numPorts+1)));

            if args.reset_only:
                return True;

            if args.loop:
                for I in results[1:]:
                    do_print(I,path);
                return True;

            # Add the results together...
            res = results[1];
            for I in res.MEMBERS:
                name = I[0];
                saturate = (1<<I[1])-1;
                for res2 in results[2:]:
                    attr2 = getattr(res2,name);
                    if isinstance(attr2,list):
                        attr = getattr(res,name);
                        for n,J in enumerate(attr2):
                            attr[n] = min(attr[n] + J,saturate);
                    else:
                        setattr(res,name,min(getattr(res,name) + attr2,saturate));
            res.portSelect = 0xFF;
            res.counterSelect = 0;
        else:
            try:
                if not args.reset_only:
                    res = umad.PerformanceGet(cnts,path);
                if reset:
                    umad.PerformanceSet(cnts,path);
                    if args.reset_only:
                        return True;
            except rdma.MADError as err:
                if err.status != 0:
                    err.message("Failed trying to get PM information for port %u"%(cnts.portSelect));
                raise;

        do_print(res,path);
    return True;
