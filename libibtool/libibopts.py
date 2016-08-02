# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from __future__ import with_statement;
import optparse;
import os;
import sys;
import rdma;
import rdma.path;
import rdma.IBA as IBA;
from libibtool import *;

def tmpl_target(s,default_end_port,require_dev,require_ep):
    return rdma.path.from_string(s,default_end_port,require_dev,
                                 require_ep);
def tmpl_int(s):
    return int(s,0);

def tmpl_node_guid(s):
    return IBA.GUID(s);

def tmpl_port_guid(s):
    return IBA.GUID(s);

def _set_sa_path(option,opt,value,parser):
    try:
        path = rdma.path.from_string(value)
        path.dqpn = 1
        path.sqpn = 1
        path.qkey = IBA.IB_DEFAULT_QP1_QKEY
        parser.values.sa_path = path
        parser.values.use_sa = True
    except ValueError:
        parser.error("invalid path: %s" % value)

class LibIBOpts(object):
    """Emulate the commandline parsing of legacy tools."""
    debug = 0;
    sbn = None;
    sbn_loaded = None;
    end_port = None;

    def __init__(self,o,args,values=None,max_values=0,template=None):
        self.args = args;
        self.o = o;

        self.debug = args.debug;
        o.verbosity = max(self.debug,getattr(args,"verbosity",0));

        self.end_port = self.get_end_port();
        if template:
            if len(values) > max_values:
                raise CmdError("Too many arguments, expected no more than %u."%(
                    max_values));

            # Special processing for tmpl_target. The target path specified
            # can choose the local end port, however all specified targets on
            # the command line must share the same end port. The selection
            # must also be consistent with the command line arguments.
            default_end_port = self.end_port;
            require_ep = None;
            require_dev = None
            if self.args.port is not None:
                require_ep = default_end_port;
            elif self.args.CA is not None:
                require_dev = default_end_port.parent;

            for I in range(len(values)):
                try:
                    tmpl = template[I];
                    v = values[I];
                    if tmpl == tmpl_target:
                        if self.args.addr_direct:
                            # -D 0 is the same as our 0,
                            try:
                                desc = int(v,0);
                                v = "%u,"%(int(v,0));
                            except ValueError:
                                pass
                        if self.args.addr_guid:
                            # Will will Parse the infiniband diags hex format
                            # GUIDs if -G is specified.
                            try:
                                v = str(IBA.GUID(int(v,16)));
                            except ValueError:
                                pass

                        path = tmpl(v,default_end_port,
                                    require_dev,require_ep);

                        if self.args.addr_direct and not isinstance(path,rdma.path.IBDRPath):
                            raise ValueError("Not a directed route");
                        if self.args.addr_guid and path.DGID is None:
                            raise ValueError("Not a GUID");
                        if self.args.addr_lid and path.DLID == 0:
                            raise ValueError("Not a LID");

                        values[I] = path;
                        if path.end_port is not None:
                            require_ep = path.end_port;
                            require_dev = None;
                            default_end_port = require_ep
                    else:
                        values[I] = tmpl(v);
                except ValueError as err:
                    raise CmdError("Invalid command line argument #%u %r - %s"%(
                        I+1,values[I],err));
            self.end_port = default_end_port;

        self.end_port.sa_path.SMKey = getattr(args,"smkey",0);
        if self.debug >= 1:
            print "D: Using end port %s %s"%(self.end_port,self.end_port.default_gid);

        if "discovery" in args.__dict__:
            if (args.discovery is None and
                (self.end_port.state != IBA.PORT_STATE_ACTIVE or
                 not 0 < self.end_port.lid < IBA.LID_MULTICAST)):
                args.discovery = "DR";
            if args.use_sa and args.discovery is not None and args.discovery != "SA":
                raise CmdError("Can't combine --sa with discovery mode %r"%(args.discovery));
            if args.use_sa:
                args.discovery = "SA";
            if args.discovery == "SA":
                args.use_sa = True;
            if args.discovery is None:
                args.discovery = "LID";

        if o.verbosity >= 2:
            self.format_args = {"format": "dump"};
        else:
            cmd = str(getattr(o,"current_command",""));
            if (cmd.find("saquery") != -1 or
                cmd.find("ibportstate") != -1):
                self.format_args = {"header": False, "colon": False, "format": "dotted",
                                    "name_map": libib_name_map_saquery, "column": 25,
                                    "skip_reserved": False};
            elif cmd.find("perfquery") != -1:
                self.format_args = {"header": False, "colon": True, "format": "dotted",
                                    "name_map": libib_name_map_perfquery, "dump_list": True};

            elif cmd.find("smpquery") != -1:
                self.format_args = {"header": False, "colon": True, "format": "dotted",
                                    "name_map": libib_name_map_smpquery};
            else:
                self.format_args = {"header": False, "colon": False, "format": "dotted"};

            if getattr(args,"int_names",True):
                self.format_args = {"header": False, "colon": False, "format": "dotted"};

    def debug_print_path(self,name,path):
        name = "D: "+name;
        if self.debug >= 1:
            print name,path;
            print " "*len(name),repr(path);

    @staticmethod
    def setup(o,address=True,discovery=False):
        o.add_option("-C","--Ca",dest="CA",
                     help="RDMA device to use. Specify a device name or node GUID");
        o.add_option("-P","--Port",dest="port",
                     help="RDMA end port to use. Specify a GID, port GUID, DEVICE/PORT or port number.");
        o.add_option("-d","--debug",dest="debug",action="count",default=0,
                     help="Increase the debug level, each -d increases by 1.")
        o.add_option("-v","--verbosity",dest="verbosity",action="count",default=0,
                     help="Increase the verbosity level of diagnostic messages, each -v increases by 1.")
        o.add_option("--smkey",dest="smkey",action="store",default=1,type=int,
                     help="Use this as the SAFormat.SMKey value.")
        o.add_option("--int-names",dest="int_names",action="store_true",
                     help="Use internal names for all the fields instead of libib compatible names.");
        o.add_option("--sa",dest="use_sa",action="store_true",
                     help="Instead of issuing SMPs, use corresponding record queries to the SA.");
        o.add_option("--sa-path",action="callback",callback=_set_sa_path,type=str,dest="sa_path",
                     help="Specify the path to the SA, implies --sa.");

        if address:
            try:
                o.add_option("-D","--Direct",action="store_true",dest="addr_direct",
                             help="The address is a directed route path. A comma separated list of port numbers starting with 0.");
            except optparse.OptionConflictError:
                o.add_option("--Direct",action="store_true",dest="addr_direct",
                             help="The address is a directed route path. A comma separated list of port numbers starting with 0.");
            try:
                o.add_option("-L","--Lid",action="store_true",dest="addr_lid",
                             help="The address is a LID integer.");
            except optparse.OptionConflictError:
                o.add_option("--Lid",action="store_true",dest="addr_lid",
                             help="The address is a LID integer.");
            o.add_option("-G","--Guid",action="store_true",dest="addr_guid",
                         help="The address is a GUID hex integer.");

        if discovery:
            o.add_option("--discovery",action="store",dest="discovery",
                         metavar="{LID|DR|SA}",
                         default=None,choices=("LID","DR","SA"),
                         help="Method to use for discovering the subnet");
            o.add_option("--refresh-cache",action="store_true",dest="drop_cache",
                         help="Don't load data from the discovery cache.");
            o.add_option("--cache",action="store",dest="cache",
                         default=None,
                         help="File to save/restore cached discovery data.");

    def get_path(self,umad,path,smp=False):
        """Check *path* for correctness and return it."""
        if isinstance(path,rdma.path.IBDRPath):
            return path;

        if path.complete():
            return path;

        # VL15 packets don't have a SL so we don't have to do a PR query.
        if smp and path.DLID != 0:
            path.SLID = path.end_port.lid;
            return path;

        self.debug_print_path("SA",self.end_port.sa_path);
        if umad == None:
            with self.get_umad() as umad:
                return rdma.path.resolve_path(umad,path);
        return rdma.path.resolve_path(umad,path);

    def get_smp_path(self,path,umad):
        """Return a :class:`rdma.path.IBPath` for *path. The path is suitable
        for use with SMPs."""
        if path:
            if path.dqpn is None:
                path.dqpn = 0;
            if path.qkey is None:
                path.qkey = IBA.IB_DEFAULT_QP0_QKEY;
            path.sqpn = 0;
            path = self.get_path(umad,path,True);
        else:
            path = rdma.path.IBDRPath(self.end_port);
        self.debug_print_path("SMP",path);
        return path;

    def get_gmp_path(self,path,umad):
        """Return a :class:`rdma.path.IBPath` for *path. The path is suitable
        for use with SMPs."""
        if path:
            if path.dqpn is None:
                path.dqpn = 1;
            if path.qkey is None:
                path.qkey = IBA.IB_DEFAULT_QP1_QKEY;
            path = self.get_path(umad,path);
            if isinstance(path,rdma.path.IBDRPath):
                # Convert the DR path into a LID path for use with GMPs using
                # the SA.
                if self.args.use_sa:
                    sat = umad
                else:
                    __import__("rdma.satransactor");
                    import sys;
                    sat = sys.modules["rdma.satransactor"].SATransactor(umad);
                path = rdma.path.get_mad_path(umad,sat.get_path_lid(path),
                                              dqpn=1,qkey=IBA.IB_DEFAULT_QP1_QKEY);
        else:
            path = rdma.path.IBPath(
                umad.end_port,
                SLID=self.end_port.lid,
                DLID=self.end_port.lid,
                DGID=self.end_port.default_gid,
                qkey = IBA.IB_DEFAULT_QP1_QKEY,
                dqpn = 1);
        self.debug_print_path("GMP",path);
        return path;

    def get_umad(self,gmp=False,local_sa=False):
        """Return a generic umad."""
        return self.get_umad_for_target(gmp=gmp,local_sa=local_sa);

    def get_umad_for_target(self,path=False,gmp=False,local_sa=False):
        """Return a UMAD suitable for use to talk to *path*. *path* is an
        :class:`rdma.path.IBPath`. If *path* is `None` then a loopback path is
        resolved, if *path* is `False` then no path is resolved.
        """
        if path:
            assert(path.end_port == self.end_port);
        umad = rdma.get_umad(self.end_port);
        try:
            if self.debug >= 1:
                umad.trace_func = rdma.madtransactor.simple_tracer;
            if self.debug >= 2:
                umad.trace_func = rdma.madtransactor.dumper_tracer;

            if self.args.use_sa:
                __import__("rdma.satransactor");
                import sys;
                if local_sa or self.args.sa_path is None:
                    sa_path = self.end_port.sa_path
                else:
                    sa_path = self.args.sa_path
                    rdma.path.resolve_path(umad, sa_path)
                umad = sys.modules["rdma.satransactor"].SATransactor(umad,sa_path);

            if path is False:
                self.path = None;
            elif gmp:
                self.path = self.get_gmp_path(path,umad);
            else:
                self.path = self.get_smp_path(path,umad);
            return umad;
        except:
            umad.close();
            raise

    def get_sched(self,umad,path=None):
        """Return a :class:`rdma.madschedule.MADSchedule` for the result
        of get_umad_for_target. Required to support `--sa`."""
        import rdma.sched;
        if self.args.use_sa:
            if path is not None:
                umad.get_path_lid(path);
            return umad.__class__(rdma.sched.MADSchedule(umad._parent), self.args.sa_path);
        return rdma.sched.MADSchedule(umad);

    def get_end_port(self):
        """Process the options for specifying the device similar to libib, this
        version is much richer though."""
        if self.args.CA is None and self.args.port is None:
            for dev in rdma.get_devices():
                for ep in dev.end_ports:
                    if ep.state >= IBA.PORT_STATE_INIT:
                        return ep
            return rdma.get_end_port();
        if self.args.CA is None:
            try:
                return rdma.get_end_port(self.args.port);
            except rdma.RDMAError:
                pass;
            dev = rdma.get_device()
        else:
            dev = rdma.get_device(self.args.CA);
        if self.args.port is None:
            return dev.end_ports.first();
        return rdma.get_end_port("%s/%s"%(dev.name,self.args.port));

    def compute_cache_fn(self,fn):
        from string import Template
        if fn is None:
            return None;
        return Template(fn).safe_substitute(
            C=str(self.end_port.parent),
            CA=str(self.end_port.parent),
            P=str(self.end_port.port_id),
            PORT=str(self.end_port.port_id),
            A="%s-%s"%(str(self.end_port.parent),self.end_port.port_id));

    @property
    def cache_fn(self):
        """Return the cache filename. This does a template substitution,
        where:
        - $C and ${CA} are the device name.
        - $P and ${PORT} are the port id.
        - $A is $C-$P.
        """
        try:
            return self.__dict_-["cache_fn"];
        except AttributeError:
            pass;
        ret = self.__dict__["cache_fn"] = self.compute_cache_fn(self.args.cache);
        return ret;

    def get_subnet(self,sched=None,stuff=None):
        """Return a :class:`rdma.subnet.Subnet` instance. Depending
        on command line options the instance may be preloaded with
        cached data. If a `load_\*` argument is specified then a
        topology discovery is completed before returning."""
        import rdma.subnet;
        import rdma.discovery;
        try:
            import cPickle as pickle
        except ImportError:
            import pickle;

        fn = self.cache_fn;
        if not self.args.drop_cache and fn is not None and os.path.exists(fn):
            with open(fn,"rb") as F:
                if self.o.verbosity >= 1:
                    print "D: Loading discovery cache from %r"%(fn);
                try:
                    sbn = pickle.load(F);
                    self.sbn_loaded = set(sbn.loaded)
                except:
                    e = sys.exc_info()[1]
                    raise CmdError("The file %r is not a valid cache file, could not unpickle - %s: %s"%(
                        fn,type(e).__name__,e));
            if not isinstance(sbn,rdma.subnet.Subnet):
                raise CmdError("The file %r is not a valid cache file, wrong object returned: %r"%(fn,sbn));
        else:
            sbn = rdma.subnet.Subnet();

        if stuff is not None:
            if self.o.verbosity >= 1:
                print "D: Performing discovery using mode %r"%(self.args.discovery);
            sbn.lid_routed = self.args.discovery != "DR";
            rdma.discovery.load(sched,sbn,stuff);
        self.sbn = sbn;
        return sbn;

    def done(self):
        if self.sbn is None:
            return True;

        try:
            import cPickle as pickle
        except ImportError:
            import pickle;
        if self.o.verbosity >= 1:
            print "D: Discovered: %r"%(", ".join(sorted(self.sbn.loaded)))
        fn = self.cache_fn;
        if fn is not None and self.sbn_loaded != self.sbn.loaded:
            fn_tmp = fn + ".new";
            with open(fn_tmp,"wb") as F:
                if self.o.verbosity >= 1:
                    print "D: Saving discovery cache to %r"%(fn);
                pickle.dump(self.sbn,F,-1);
            os.rename(fn_tmp,fn);
        return True;

# libib has all sorts of interesting ideas what to name the fields. We don't, ours
# are uniform. These tables switch our names to libib's. This isn't perfect, libib
# is somewhat context sensitive to how it chooses a name. :(
libib_name_map_saquery = {
    # saquery
    'nodeDescription': 'NodeDescription',
    'RespTimeValue': 'Response time value',
    'SGID': 'sgid',
    'ClassVersion': 'Class version',
    'CapabilityMask2': 'Capability mask 2',
    'DGID': 'dgid',
    'SLID': 'slid',
    'CapabilityMask': 'Capability mask',
    'ServiceID': 'service_id',
    'DLID': 'dlid',
    'SL': 'sl',
    'PKey': 'pkey',
    'TClass': 'tclass',
    'BaseVersion': 'Base version',
    'PortGID': 'PortGid',
    'BlockNum': 'Block',
    'nodeDescription': 'NodeDescription',
    'InputPortNum': 'InPort',
    'OutputPortNum': 'OutPort',
    'RedirectGID': 'Redirect GID',
    'RedirectLID': 'Redirect LID',
    'RedirectQP': 'Redirect QP',
    'RedirectQKey': 'Redirect QKey',
    'RedirectPKey': 'Redirect PKey',
    'MLID': 'mlid',
    'MTU': 'mtu',
    'PacketLifeTime': 'pkt_life',
    'Preference': 'preference',
    'Rate': 'rate',
    'QKey': 'qkey',
    'QOSClass': 'qos_class',
    'OutPort': 'Port',
    'EndportLID': 'EndPortLid',
    'TrapPKey': 'Trap PKey',
    'TrapQKey': 'Trap QKey',
    'TrapGID': 'Trap GID',
    'TrapLID': 'Trap LID',
    'PortNum': 'Port',

    # Structure names.
    'SAServiceRecord': 'ServiceRecord',
    'SALinkRecord': 'LinkRecord',
    'SASMInfoRecord': 'SMInfoRecord',
    'SANodeRecord': 'NodeRecord',
    'SAPortInfoRecord': 'PortInfoRecord',
    'SASwitchInfoRecord': 'SwitchInfoRecord',
    'SAPathRecord': 'PathRecord',
    'MADClassPortInfo': 'SA ClassPortInfo',
    'SAMCMemberRecord': 'MCMember Record',
    'SAServiceAssociationRecord': 'ServiceAssociationRecord',
    'SAGUIDInfoRecord': 'GUIDInfoRecord',
    'SAVLArbitrationTableRecord': 'VLArbTableRecord',
    'SASLToVLMappingTableRecord': 'SL2VLTableRecord',
    'SAPKeyTableRecord': 'PKeyTableRecord',
    'SARandomForwardingTableRecord': 'RandomForwardingTableRecord',
    'SALinearForwardingTableRecord': 'LFT Record',
    'SAMulticastForwardingTableRecord': 'MFT Record',
    'SAInformInfoRecord': 'InformInfoRecord',

    'NodeType': 'node_type',
    'NumPorts': 'num_ports',
    'SystemImageGUID': 'sys_guid',
    'NodeGUID': 'node_guid',
    'PortGUID': 'port_guid',
    'PartitionCap': 'partition_cap',
    'LocalPortNum': 'port_num',
    'VendorID': 'vendor_id',
    'DeviceID': 'device_id',
    'revision': 'revision',
}

# FIXME: I think Ira fixed libib to be more sane, so these are old.
libib_name_map_perfquery = {
    'PortRcvErrors': 'RcvErrors',
    'PortXmitConstraintErrors': 'XmtConstraintErrors',
    'SymbolErrorCounter': 'SymbolErrors',
    'PortXmitDiscards': 'XmtDiscards',
    'PortRcvRemotePhysicalErrors': 'RcvRemotePhysErrors',
    'ExcessiveBufferOverrunErrors': 'ExcBufOverrunErrors',
    'PortXmitData': 'XmtData',
    'LinkErrorRecoveryCounter': 'LinkRecovers',
    'PortRcvSwitchRelayErrors': 'RcvSwRelayErrors',
    'PortXmitWait': 'XmtWait',
    'LocalLinkIntegrityErrors': 'LinkIntegrityErrors',
    'PortRcvData': 'RcvData',
    'PortRcvConstraintErrors': 'RcvConstraintErrors',
    'LinkDownedCounter': 'LinkDowned',
    'PortXmitPkts': 'XmtPkts',
    'PortSwHOQLimitDiscards': 'PortSwHOQLifetimeLimitDiscards',
    'PortRcvPkts': 'RcvPkts',
}

libib_name_map_smpquery = {
    'PartitionEnforcementCap': 'PartEnforceCap',
    'VendorID': 'VendorId',
    'LinkDownDefaultState': 'LinkDownDefState',
    'InitTypeReply': 'InitReply',
    'MTUCap': 'MtuCap',
    'PortPhysicalState': 'PhysLinkState',
    'DefaultPort': 'DefPort',
    'PKeyViolations': 'PkeyViolations',
    'RespTimeValue': 'RespTimeVal',
    'OverrunErrors': 'OverrunErr',
    'LinkRoundTripLatency': 'RoundTrip',
    'SubnetTimeOut': 'SubnetTimeout',
    'MasterSMSL': 'SMSL',
    'MKeyViolations': 'MkeyViolations',
    'MulticastFDBCap': 'McastFdbCap',
    'VLArbitrationHighCap': 'VLArbHighCap',
    'MKeyProtectBits': 'ProtectBits',
    'LifeTimeValue': 'LifeTime',
    'ClassVersion': 'ClassVers',
    'DefaultMulticastPrimaryPort': 'DefMcastPrimPort',
    'LinearFDBTop': 'LinearFdbTop',
    'PortState': 'LinkState',
    'BaseVersion': 'BaseVers',
    'DefaultMulticastNotPrimaryPort': 'DefMcastNotPrimPort',
    'QKeyViolations': 'QkeyViolations',
    'FilterRawOutbound': 'FilterRawOutb',
    'OperationalVLs': 'OperVLs',
    'LocalPortNum': 'LocalPort',
    'FilterRawInbound': 'FilterRawInb',
    'CapabilityMask': 'CapMask',
    'HOQLife': 'HoqLife',
    'GUIDCap': 'GuidCap',
    'MKeyLeasePeriod': 'MkeyLeasePeriod',
    'PartitionEnforcementOutbound': 'PartEnforceOutb',
    'LocalPhyErrors': 'LocalPhysErr',
    'NodeGUID': 'Guid',
    'DeviceID': 'DevId',
    'LID': 'Lid',
    'LinearFDBCap': 'LinearFdbCap',
    'SystemImageGUID': 'SystemGuid',
    'MKey': 'Mkey',
    'VLArbitrationLowCap': 'VLArbLowCap',
    'PortGUID': 'PortGuid',
    'RandomFDBCap': 'RandomFdbCap',
    'PortStateChange': 'StateChange',
    'PartitionEnforcementInbound': 'PartEnforceInb',
    'GIDPrefix': 'GidPrefix',
    'FilterRawInboundCap': 'FilterRawInbound',
    'FilterRawOutboundCap': 'FilterRawOutbound',
    'OutboundEnforcementCap': 'OutboundPartEnf',
    'InboundEnforcementCap': 'InboundPartEnf',
    'PartitionCap': 'PartCap',
    'MasterSMLID': 'SMLid',
    'OptimizedSLtoVLMappingProgramming': 'OptSLtoVLMapping',
    'LIDsPerPort': 'LidsPerPort',
}
