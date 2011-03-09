from __future__ import with_statement;
import optparse;
import rdma;
import rdma.path;
import rdma.IBA as IBA;
from libibtool import *;

def tmpl_target(s):
    dr = s.split(",");
    if len(dr) == 1:
        try:
            return rdma.IBA.conv_ep_addr(s);
        except ValueError:
            return s;

    if dr[-1] == '':
        dr = [int(I) for I in dr[:-1]];
    else:
        dr = [int(I) for I in dr];
    for I in dr:
        if I >= 255:
            raise CmdError("Invalid DR path");
    return dr;
def tmpl_int(s):
    return int(s,0);

def tmpl_node_guid(s):
    return IBA.GUID(s);

class LibIBOpts(object):
    """Emulate the commandline parsing of legacy tools."""
    debug = 0;
    sbn = None;

    def __init__(self,o,args,values=None,max_values=0,template=None):
        self.args = args;
        self.o = o;
        self.end_port = self.get_end_port();
        self.end_port.sa_path.SMKey = getattr(args,"smkey",0);
        self.debug = args.debug;
        if self.debug > 1:
            print "debug: Using end port %s %s"%(self.end_port,self.end_port.default_gid);
        o.verbosity = max(self.debug,getattr(args,"verbosity",0));

        if "discovery" in args.__dict__:
            if args.discovery is None and self.end_port.state != IBA.PORT_STATE_ACTIVE:
                args.discovery = "DR";
            if args.use_sa and args.discovery is not None and args.discovery != "SA":
                raise CmdError("Can't combine --sa with discovery mode %r"%(args.discovery));
            if args.use_sa:
                args.discovery = "SA";
            if args.discovery == "SA":
                args.use_sa = True;
            if args.discovery is None:
                args.discovery = "LID";

        if template:
            if len(values) > max_values:
                raise CmdError("Too many arguments, expected no more than %u."%(
                    max_values));
            for I in range(len(values)):
                try:
                    values[I] = template[I](values[I]);
                except ValueError as err:
                    raise CmdError("Invalid command line argument #%u %r"%(
                        I+1,values[I]));

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
        name = "debug: "+name;
        if self.debug >= 1:
            print name,path;
        if self.debug >= 2:
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

    def get_path(self,umad,desc,smp=False):
        """Return a :class:`rdma.path.IBPath` for the destination description desc."""
        if isinstance(desc,list):
            # tmp_target does the parse for us
            return rdma.path.IBDRPath(self.end_port,
                                      drPath = bytes("").join("%c"%(I) for I in desc));

        if self.args.addr_direct:
            # -D 0 is the same as our 0,
            try:
                desc = int(desc,0);
            except ValueError:
                raise CmdError("Target was not parsed as directed route");
            return rdma.path.IBDRPath(self.end_port,
                                      drPath = bytes("%c"%(desc)));

        try:
            ep = rdma.IBA.conv_ep_addr(desc);
        except ValueError:
            raise CmdError("Could not parse %r as a TARGET. Tried as a GID, port GUID, directed route and LID."%(desc))

        if self.args.addr_guid and not isinstance(ep,IBA.GID):
            raise CmdError("Target was not parsed as a GUID");
        if self.args.addr_lid and not (isinstance(ep,int) or isinstance(ep,long)):
            raise CmdError("Target was not parsed as a LID");

        # VL15 packets don't have a SL so we don't have to do a PR query.
        if smp and isinstance(ep,int) or isinstance(ep,long):
            return rdma.path.IBPath(umad.end_port,
                                    SLID=umad.end_port.lid,
                                    DLID=ep);

        self.debug_print_path("SA",self.end_port.sa_path);
        if umad == None:
            with self.get_umad() as umad:
                return rdma.path.get_mad_path(umad,ep);
        return rdma.path.get_mad_path(umad,ep);

    def get_smp_path(self,desc,umad):
        """Return a :class:`rdma.path.IBPath` for the destination description desc.
        The path is suitable for use with SMPs."""
        if desc:
            path = self.get_path(umad,desc,True);
            path.dqpn = 0;
            path.sqpn = 0;
            path.qkey = IBA.IB_DEFAULT_QP0_QKEY;
        else:
            path = rdma.path.IBDRPath(self.end_port);
        self.debug_print_path("SMP",path);
        return path;

    def get_gmp_path(self,desc,umad):
        """Return a :class:`rdma.path.IBPath` for the destination description desc.
        The path is suitable for use with SMPs."""
        if desc:
            path = self.get_path(umad,desc);
            if isinstance(path,rdma.path.IBDRPath):
                # Convert the DR path into a LID path for use with GMPs using
                # the SA.
                if self.args.use_sa:
                    sat = umad
                else:
                    __import__("rdma.satransactor");
                    import sys;
                    sat = sys.modules["rdma.satransactor"].SATransactor(umad);
                path = rdma.path.get_mad_path(umad,sat.get_path_lid(path));
            path.dqpn = 1;
            path.sqpn = 1;
            path.qkey = IBA.IB_DEFAULT_QP1_QKEY;
        else:
            path = rdma.path.IBPath(
                umad.end_port,
                SLID=self.end_port.lid,
                DLID=self.end_port.lid,
                DGID=self.end_port.default_gid,
                qkey = IBA.IB_DEFAULT_QP1_QKEY,
                dqpn = 1,
                sqpn = 1);
        self.debug_print_path("GMP",path);
        return path;

    def get_umad(self,gmp=False):
        """Return a generic umad."""
        return self.get_umad_for_target(None,gmp=gmp);

    def get_umad_for_target(self,dest,gmp=False):
        """Return a UMAD suitable for use to talk to dest."""
        # FIXME: dest should play a role in determining the local end port if it is
        # a GID
        umad = rdma.get_umad(self.end_port);
        try:
            if self.debug >= 1:
                umad.trace_func = rdma.madtransactor.simple_tracer;
            if self.debug >= 2:
                umad.trace_func = rdma.madtransactor.dumper_tracer;

            if self.args.use_sa:
                __import__("rdma.satransactor");
                import sys;
                umad = sys.modules["rdma.satransactor"].SATransactor(umad);

            if dest is None:
                self.path = None;
            elif gmp:
                self.path = self.get_gmp_path(dest,umad);
            else:
                self.path = self.get_smp_path(dest,umad);
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
            return umad.__class__(rdma.sched.MADSchedule(umad._parent));
        return rdma.sched.MADSchedule(umad);

    def get_end_port(self):
        """Process the options for specifying the device similar to libib, this
        version is much richer though."""
        if self.args.CA is None and self.args.port is None:
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

    def get_subnet(self,sched=None,stuff=None):
        """Return a :class:`rdma.subnet.Subnet` instance. Depending
        on command line options the instance may be preloaded with
        cached data. If a `load_\*` argument is specified then a
        topology discovery is completed before returning."""
        import rdma.subnet;
        import rdma.discovery;
        sbn = rdma.subnet.Subnet();
        if stuff is not None:
            if self.o.verbosity >= 1:
                print "D: Performing discovery using mode %r"%(self.args.discovery);
            sbn.lid_routed = self.args.discovery != "DR";
            rdma.discovery.load(sched,sbn,stuff);
        self.sbn = sbn;
        return sbn;

    def done(self):
        if self.o.verbosity >= 1 and self.sbn is not None:
            print "D: Discovered: %r"%(", ".join(sorted(self.sbn.loaded)))
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
