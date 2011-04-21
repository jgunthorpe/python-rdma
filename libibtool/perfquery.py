# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from __future__ import with_statement;
import sys;
import os;
import time;
import rdma;
import rdma.path;
import rdma.tools;
import rdma.IBA as IBA;
from libibtool import *;
from libibtool.libibopts import *;

def sum_result(results):
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
    return res;

class Querier(object):
    thresh = None;

    def __init__(self,umad,path,args,format_args):
        self.umad = umad;
        self.path = path;
        self.args = args;
        self.format_args = format_args
        if args.kind is None:
            args.kind = IBA.PMPortCounters;

    @staticmethod
    def add_options(o):
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

    @property
    def cpinf(self):
        try:
            return self.__dict__["cpinf"];
        except KeyError:
            pass
        cpinf = self.umad.PerformanceGet(IBA.MADClassPortInfo,self.path);
        self.path.resp_time = cpinf.respTimeValue;
        self.__dict__["cpinf"] = cpinf;
        return cpinf;

    @property
    def ninf(self):
        try:
            return self.__dict__["ninf"];
        except KeyError:
            pass
        ninf = IBA.ComponentMask(IBA.SANodeRecord());
        ninf.LID = self.path.DLID;
        ninf = self.umad.SubnAdmGet(ninf);
        self.__dict__["ninf"] = ninf;
        if self.path.DGID is None:
            self.path.DGID = IBA.GID(prefix=IBA.GID_DEFAULT_PREFIX,
                                     guid=ninf.nodeInfo.portGUID);
        return ninf;

    def setup(self,cnts,port,resetSelect=None):
        if self.args.all:
            cnts.portSelect = 0xFF;
        elif port == -1:
            cnts.portSelect = self.path.end_port.port_id;
        elif port is not None:
            cnts.portSelect = port;
        else:
            # Hmm. Lets be smarter here, display the 'natural' port number
            # for HCAs, and something random for switches. I think this is
            # better than returning an invalid port select error code.
            #ninf = umad.SubnGet(IBA.SMPNodeInfo,path.copy(dqpn=0,sqpn=0));
            #cnts.portSelect = ninf.localPortNum;
            cnts.portSelect = self.ninf.nodeInfo.localPortNum;
            if self.ninf.nodeInfo.nodeType == IBA.NODE_SWITCH and cnts.portSelect == 0:
                cnts.portSelect = 1;

        self.accumulate = self.args.loop;
        if cnts.portSelect == 0xFF:
            self.accumulate = not (self.cpinf.capabilityMask & IBA.allPortSelect);

        if self.accumulate:
            if not self.args.loop:
                print "Emulating AllPortSelect by iterating through all ports";
            if self.ninf.nodeInfo.nodeType == IBA.NODE_CA:
                raise CmdError("Can't fetch all ports on a CA.");
            numPorts = self.ninf.nodeInfo.numPorts;

        self.reset = self.args.reset_only or self.args.reset;
        if self.reset:
            if resetSelect is None:
                resetSelect = 0xFFFFFF
            cnts.counterSelect = resetSelect & 0xFFFF;
            try:
                cnts.counterSelect2 = resetSelect >> 16;
            except AttributeError:
                pass;

    def fetch(self,sched,cnts):
        """Coroutine to fetch/reset the configured performance mad(s)."""
        # The port does not support all counters. Accumulate the port select
        # values manually. Note this does not work for HCA ports since
        # we cannot access them using only port select.
        if self.accumulate:
            def get_cnts(sched,res,port,path):
                if not self.args.reset_only:
                    cnts.portSelect = port;
                    res[port] = yield sched.PerformanceGet(cnts,path);
                if self.reset:
                    cnts.portSelect = port;
                    yield sched.PerformanceSet(cnts,path);

            numPorts = self.ninf.nodeInfo.numPorts;
            results = [None]*(numPorts+1);
            yield sched.mqueue(get_cnts(sched,results,I,self.path)
                               for I in range(1,numPorts+1));

            if self.args.reset_only:
                return;

            if self.args.loop:
                sched.result = results;
                return;

            # Add the results together...
            res = sum_result(results);
        else:
            try:
                if not self.args.reset_only:
                    res = yield sched.PerformanceGet(cnts,self.path);
                if self.reset:
                    yield sched.PerformanceSet(cnts,self.path);
                    if self.args.reset_only:
                        return;
            except rdma.MADError as err:
                if err.status != 0:
                    err.message("Failed trying to get PM information for port %u"%(cnts.portSelect));
                raise;
        sched.result = res;

    def header(self,F,res):
        if self.path.DGID is not None:
            print >> F,"# Port counters: Lid %u (%s) port %u"%(self.path.DLID,self.path.DGID,
                                                          res.portSelect);
        else:
            print >> F,"# Port counters: Lid %u port %u"%(self.path.DLID,res.portSelect);
    def printer(self,F,res):
        self.header(F,res);
        res.printer(F,**self.format_args);

    def _print_one(self,F,oname,cname,column,refv,lastv,dtime):
        if lastv != refv:
            if dtime is not None:
                s = "%-8u (+ %.3f/s)"%(refv,(refv - lastv)/dtime);
            else:
                s = "%-8u (+ %d)"%(refv,refv - lastv);
        else:
            s = "%u"%(refv);
        print >> F, "%s%s%s"%(cname,"."*(column-len(cname)),s);

    def _print_thresh(self,F,oname,cname,column,refv,lastv,dtime):
        if lastv == refv or dtime is None:
            return;
        rate = (refv - lastv)/dtime;
        if rate < self.thresh.get(oname,0xFFFFFFFF):
            return;
        s = "%-8u (+ %.3f/s)"%(refv,rate);
        print >> F, "%s%s%s"%(cname,"."*(column-len(cname)),s);

    def printer_delta(self,F,res,last,dtime):
        self.header(F,res);
        printer = self._print_one if self.thresh is None else self._print_thresh;
        name_map = self.format_args.get("name_map");
        column = self.format_args.get("column",33);
        for name,mbits,count in res.MEMBERS:
            if (name.startswith("reserved_") or name.startswith("portSelect") or
                name.startswith("counterSelect")):
                continue;
            cname = name[0].upper() + name[1:];
            if name_map:
                cname = name_map.get(cname,cname);

            attr = getattr(res,name);
            if attr is None:
                continue;
            if last is not None:
                lastv = getattr(last,name);
            else:
                lastv = attr;

            if count == 1:
                printer(F,name,cname,column,attr,lastv,dtime);
            else:
                for idx in range(0,count):
                    printer(F,name,"%s[%u]"%(cname,idx),column,
                            attr[idx],lastv[idx],dtime);

def cmd_perfquery(argv,o):
    """Display the performance manager values for a port
       Usage: %prog [TARGET [PORT [RESET]]]"""

    Querier.add_options(o);
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
        values = (None,-1);

    with lib.get_umad_for_target(values[0],gmp=True) as umad:
        if len(values) == 1:
            values = (values[0],None);

        q = Querier(umad,lib.path,args,lib.format_args);
        cnts = args.kind();
        q.setup(cnts,values[1],values[3] if len(values) >= 3 else None);

        sched = lib.get_sched(umad,lib.path);
        sched.run(queue=q.fetch(sched,cnts));
        res = sched.result;

        if res is not None:
            if isinstance(res,list):
                for I in res:
                    if I is not None:
                        q.printer(sys.stdout,I);
            else:
                q.printer(sys.stdout,res);
    return lib.done();

def cmd_ibswportwatch(argv,o):
    """Continually display the performance manager values for a port
       Usage: %prog [TARGET [PORT]]

       Despite the name, this works on CA ports as well."""

    o.add_option("-n","--count",action="store",dest="count",
                 type=int,
                 help="Number of iterations, default is infinite.");
    o.add_option("-p",action="store",dest="sleep",default=1,
                 type=float,
                 help="Time between fetches.");
    o.add_option("-b","--delta",action="store_const",dest="mode",
                 const=1,default=1,
                 help="Display the counter increment as a rate. (default)");
    o.add_option("-t","--threshold",action="store_const",dest="mode",
                 const=2,default=1,
                 help="Display only counters that increment faster than the threshold rate.");
    o.add_option("-T",action="store",dest="load_thresh",metavar="FILE",
                 help="Load threshold values from this file.");
    Querier.add_options(o);
    LibIBOpts.setup(o);
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,2,(tmpl_target,tmpl_int));

    args.reset_only = False;
    args.reset = False;
    args.loop = False;
    if len(values) == 0:
        values = (None,-1);

    # The display is smoother if we use buffering no line buffering.
    with os.fdopen(os.dup(sys.stdout.fileno()),"w",64*1024) as bout:
     with lib.get_umad_for_target(values[0],gmp=True) as umad:
        if len(values) == 1:
            values = (values[0],None);

        q = Querier(umad,lib.path,args,lib.format_args);
        if args.mode == 2:
            import libibtool.errors;
            q.thresh = libibtool.errors.load_thresholds(args.load_thresh);
        cnts = args.kind();
        q.setup(cnts,values[1]);
        sched = lib.get_sched(umad,lib.path);

        count = 0;
        start = rdma.tools.clock_monotonic();
        last = None;
        last_time = None;
        dtime = None;
        try:
            while count != args.count:
                sched.run(queue=q.fetch(sched,cnts));
                res = sched.result;

                now = rdma.tools.clock_monotonic();
                if last_time is not None:
                    dtime = now - last_time;
                last_time = now;
                try:
                    if res is not None:
                        if isinstance(res,list):
                            if last is None:
                                last = res;
                            for I,J in zip(res):
                                if cur is not None:
                                    q.printer(bout,I,J,dtime);
                        else:
                            q.printer_delta(bout,res,last,dtime);
                        last = res;
                finally:
                    bout.flush();
                count = count +1;
                if count != args.count:
                    now = rdma.tools.clock_monotonic();
                    # Try and hit the target interval from the starting time,
                    # in an absolute sense..
                    to_sleep = (start + count*args.sleep) - now;
                    if to_sleep > 0:
                        time.sleep(to_sleep);
        except KeyboardInterrupt:
            pass;
    return lib.done();
