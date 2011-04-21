# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from __future__ import with_statement;
import struct;
import socket;
import time;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
from libibtool import *;
from libibtool.libibopts import *;
import libibtool.vendstruct
import libibtool.vend as vend;

# This is just an illustration how to make this work, and not a complete
# copy of vendstat.
def cmd_vendstat(argv,o):
    """Example how to use vendor MADs.
       Usage: %prog TARGET"""
    libibtool.vendstruct.install_vend();
    LibIBOpts.setup(o);
    o.add_option("-N",action="store_const",dest="kind",
                 const=vend.MlxGeneralInfo,
                 help="Show general Mellanox information");
    o.add_option("--cpi",action="store_const",dest="kind",
                 const=libibtool.vendstruct.MlxClassPortInfo,
                 help="Show the Mellanox vendor class port info.");
    (args,values) = o.parse_args(argv,expected_values=1);
    lib = LibIBOpts(o,args,values,1,(tmpl_target,));

    if args.kind is None:
        raise CmdError("-N must be specified.");

    with lib.get_umad_for_target(values[0],gmp=True) as umad:
        path = lib.path;
        smp_path = path.copy(dqpn=0);
        pi = umad.SubnGet(IBA.SMPPortInfo,smp_path);
        if not pi.capabilityMask & IBA.isVendorClassSupported:
            raise CmdError("Port does not support vendor MADs");
        vinf = umad.VendGet(args.kind,path);
        vinf.printer(sys.stdout,**lib.format_args);
    return lib.done();

def tmpl_ofa_vend(v):
    if v == "ping":
        return vend.OFASysStatPing;
    if v == "host":
        return vend.OFASysStatHostInfo;
    if v == "cpu":
        return vend.OFASysStatCPUInfo;
    if v == "cpi":
        return libibtool.vendstruct.OFASysStatClassPortInfo;
    raise ValueError("Not one of ping, host, cpi or cpu");

def handle_packet(umad,buf,path):
    fmt,req = umad.parse_request(buf,path);
    if fmt.__class__ != libibtool.vendstruct.OFASysStatFormat:
        raise rdma.MADError(req=fmt,req_buf=buf,path=path,
                            reply_status=IBA.MAD_STATUS_UNSUP_METHOD,
                            msg="Unsupported format %s"%(
                                fmt.describe()));
    if fmt.method == IBA.MAD_METHOD_GET:
        if req.__class__ is vend.OFASysStatPing:
            return umad.send_reply(fmt,req,path);
        if req.__class__ is vend.OFASysStatHostInfo:
            rep = vend.OFASysStatHostInfo();
            hostname = socket.gethostbyaddr(socket.gethostname())[0];
            rep.data_str[:len(hostname)] = hostname[:len(rep.data_str)];
            return umad.send_reply(fmt,rep,path);
        if req.__class__ is IBA.MADClassPortInfo:
            return umad.send_reply(fmt,cpi,path);
    elif fmt.method == IBA.MAD_METHOD_SET:
        if req.__class__ is IBA.MADClassPortInfo:
            cpi.trapGID = req.trapGID;
            cpi.trapTC = req.trapTC;
            cpi.trapSL = req.trapSL;
            cpi.trapFL = req.trapFL;
            cpi.trapLID = req.trapLID;
            cpi.trapPKey = req.trapPKey;
            cpi.trapHL = req.trapHL;
            cpi.trapQP = req.trapQP;
            cpi.trapQKey = req.trapQKey;
            return umad.send_reply(fmt,cpi,path);
    else:
        raise rdma.MADError(req=fmt,req_buf=buf,path=path,
                            reply_status=IBA.MAD_STATUS_UNSUP_METHOD,
                            msg="Unsupported method %s"%(
                                fmt.describe()));
    raise rdma.MADError(req=fmt,req_buf=buf,path=path,
                        reply_status=IBA.MAD_STATUS_UNSUP_METHOD_ATTR_COMBO,
                        msg="Unsupported attribute ID %s"%(
                            fmt.describe()));

def cmd_ibsysstat(argv,o):
    """Request the system information MAD
       Usage: %prog [TARGET ping|host|cpu|cpi]

       This program must be running in server mode on the target end port."""
    libibtool.vendstruct.install_vend();
    LibIBOpts.setup(o);
    o.add_option("-S",action="store_true",dest="server",
                 help="Run as a server");
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,2,(tmpl_target,tmpl_ofa_vend));

    if args.server:
        # FIXME: This should really set the capability mask bit, I wonder how?
        # But Mellanox HCA already set it for their own uses. What a silly
        # bit.
        global cpi
        cpi = IBA.MADClassPortInfo();
        cpi.baseVersion = IBA.MAD_BASE_VERSION;
        cpi.classVersion = libibtool.vendstruct.OFASysStatFormat.MAD_CLASS_VERSION;
        cpi.respTimeValue = 16;
        cpi.redirectQKey = cpi.trapQKey = IBA.IB_DEFAULT_QP1_QKEY;
        if len(values) != 0:
            raise CmdError("Too many arguments.");
        with lib.get_umad_for_target(gmp=True) as umad:
            agent_id = umad.register_server_fmt(libibtool.vendstruct.OFASysStatFormat);
            while True:
                buf,path = umad.recvfrom(None);
                if path.umad_agent_id != agent_id:
                    continue;
                try:
                    handle_packet(umad,buf,path);
                except rdma.MADError as err:
                    err.dump_detailed(sys.stderr,"E:",level=1);
                    umad.send_error_exc(err);
        return lib.done()

    if len(values) != 2:
        raise CmdError("Expect 2 arguments.");

    with lib.get_umad_for_target(values[0],gmp=True) as umad:
        path = lib.path;
        vinf = umad.VendGet(values[1],path);
        vinf.printer(sys.stdout,**lib.format_args);
    return lib.done();

def cmd_ibping(argv,o):
    """Perform pings using ibsysstat
       Usage: %prog TARGET

       ibsysstat must be running in server mode on the target end port."""
    libibtool.vendstruct.install_vend();
    LibIBOpts.setup(o);
    o.add_option("-c","--count",action="store",dest="count",
                 type=int,
                 help="Stop after count pings.");
    o.add_option("-f","--flood",action="store_true",dest="flood",
                 help="Flood ping, no delay between packets.");
    (args,values) = o.parse_args(argv,expected_values=1);
    lib = LibIBOpts(o,args,values,1,(tmpl_target,));

    with lib.get_umad_for_target(values[0],gmp=True) as umad:
        path = lib.path;
        count = args.count;
        count = 0;
        lost = 0;
        minrtt = 1<<32;
        maxrtt = 0;
        totalrtt = 0;
        start_time = rdma.tools.clock_monotonic();
        try:
            while count != args.count:
                start = rdma.tools.clock_monotonic();
                try:
                    vinf = umad.VendGet(vend.OFASysStatPing,path);
                except rdma.MADError:
                    lost = lost + 1;
                    count = count + 1;
                    if not args.flood:
                        time.sleep(1);
                    continue;
                count = count + 1;
                rtt = rdma.tools.clock_monotonic() - start;
                minrtt = min(rtt,minrtt);
                maxrtt = max(rtt,maxrtt);
                totalrtt = totalrtt + rtt;
                if not args.flood:
                    print "Ping reply, '%s': seq=%u time %.03f ms"%(
                        path,count,rtt*1000)
                    if count != args.count:
                        time.sleep(1);
        except KeyboardInterrupt:
            pass;
        print "--- %s statistics ---"%(path)
        print "%u packets transmitted, %u received, %u%% packet loss, time %.03fms"%(
            count,count - lost,lost*100/count,
            (rdma.tools.clock_monotonic() - start_time)*1000);
        print "rtt min/avg/max = %.03f/%.03f/%.03f ms"%(
            minrtt*1000,totalrtt/(count-lost)*1000,maxrtt*1000);
    return lib.done();
