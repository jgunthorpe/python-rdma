# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import sys
import copy
import rdma;
import rdma.IBA as IBA;
import rdma.IBA_describe as IBA_describe;
import rdma.madtransactor;
import rdma.discovery;
import rdma.subnet;
from libibtool import *;
from libibtool.libibopts import *;

def cmd_init_all_ports(argv,o):
    """Set the port state value to INIT for all links.
       Usage: %prog

       This can be used to try and recover a subnet that has deadlock or other
       fabric issues by dropping all the links back to INIT and thus blocking
       non-management traffic. It may need to be run multiple times before
       it completes."""
    LibIBOpts.setup(o);
    (args,values) = o.parse_args(argv,expected_values=0);
    lib = LibIBOpts(o,args,values);

    with lib.get_umad_for_target(False) as umad:
        sched = lib.get_sched(umad,lib.path);

        # We borrow the internal topology scanner to make this go
        # appropriately.
        class MyTopo(rdma.discovery._SubnetTopo):
            def do_port(self,path,node,aport,portIdx,depth):
                yield rdma.discovery._SubnetTopo.do_port(self,path,node,
                                                         aport,portIdx,depth);
                try:
                    pinf = copy.copy(aport.pinf);
                    if (pinf is None or portIdx == 0 or
                        pinf.portState == IBA.PORT_STATE_DOWN or
                        pinf.portState == IBA.PORT_STATE_INIT):
                        return;
                    pinf.portPhysicalState = 0;
                    pinf.linkSpeedEnabled = 0;
                    pinf.linkWidthEnabled = 0;
                    pinf.portState = IBA.PORT_STATE_DOWN;
                    yield self.sched.SubnSet(pinf,path,portIdx);
                except rdma.MADError as e:
                    print "Failed to set port state on %s via %s"%(aport,path);
                    print "   ",e

        sbn = rdma.subnet.Subnet();
        fetcher = MyTopo(sched,sbn,get_desc=False,lid_route=False);
        path = rdma.path.IBDRPath(sched.end_port,retries=10);
        sched.run(queue=(fetcher.do_node(path),));
    return lib.done();

def cmd_set_port_state(argv,o):
    """Set the port state value for multiple end ports.
       Usage: %prog [TARGET@PORT_NUM]+

       This intelligently selects a DR path to disable/enable links in the
       network. For instance if this command is used to create a partition in
       the network then it will find DR paths that do not cross the partition
       and ensure that the arguments are all on this side of the partition.

       Use --disable to turn the ports off, --enable to turn them back on, or
       --init to reset ports back to INIT."""
    o.add_option("--disable",dest="phys_state",action="store_const",
                 default=0,const=IBA.PHYS_PORT_STATE_DISABLED,
                 help="Set the physical port state to disabled.");
    o.add_option("--enable",dest="phys_state",action="store_const",
                 default=0,const=IBA.PHYS_PORT_STATE_POLLING,
                 help="Set the physical port state to polling.");
    o.add_option("--init",dest="port_state",action="store_const",
                 default=0,const=IBA.PORT_STATE_INIT,
                 help="Set the port state to initialize.");
    LibIBOpts.setup(o,address=True,discovery=True);
    (args,values) = o.parse_args(argv);

    # Strip off the @ index
    nvalues = [];
    portIdxs = [];
    for I in range(len(values)):
        s = values[I].partition('@');
        nvalues.append(s[0]);
        if s[2] == '':
            portIdxs.append(None);
        else:
            portIdxs.append(int(s[2]));
    values = nvalues;

    tmpl = tuple(tmpl_target for I in values);
    lib = LibIBOpts(o,args,values,min(1,len(tmpl)),tmpl);

    with lib.get_umad_for_target(False) as umad:
        sched = lib.get_sched(umad,lib.path);
        sbn = lib.get_subnet(sched,
                             ["all_NodeInfo",
                              "all_PortInfo",
                              "all_topology"]);

        otopology = copy.copy(sbn.topology);
        eps = [];
        for I in range(len(values)):
            path = values[I];
            # path_to_port can resolve the possible command line arguments, so
            # we do not need to use path.resolve_path.
            port = sbn.path_to_port(path);
            if port is None:
                raise CmdError("Could not find path %s in the subnet"%(path))
            eps.append(port);
            portIdx = portIdxs[I];
            if portIdx is None:
                if not isinstance(port.parent,rdma.subnet.Switch):
                    portIdxs[I] = portIdx = port.port_id;
                else:
                    raise CmdError("Need to have a port index for switch %s"%(
                        port.portGUID));

            # Remove the links we are going to affect from the topology
            port = port.parent.get_port(portIdx);
            peer = sbn.topology.get(port);
            try:
                del sbn.topology[path];
            except KeyError:
                pass
            try:
                del sbn.topology[peer];
            except KeyError:
                pass

        def get_path(ep,portIdx):
            try:
                return dr.get_path(ep);
            except ValueError:
                pass

            # Hmm, the user picked the wrong port somehow, try to help the
            # user.
            peer = otopology.get(ep.parent.get_port(portIdx));
            try:
                dr.get_path(peer.to_end_port());
            except ValueError:
                raise CmdError("No DR path exists to %s port %u"%(
                    ep.portGUID,portIdx));
            raise CmdError("No DR path exists to %s port %u - try using the peer %s port %u"%(
                ep.portGUID,portIdx,peer.to_end_port().portGUID,
                peer.port_id));

        dr = sbn.get_dr_cache(umad.parent);
        dpath = [get_path(port,portIdx) for port,portIdx in zip(eps,portIdxs)];

        pinfs = [umad.SubnGet(IBA.SMPPortInfo,path,portIdx)
                for path,portIdx in zip(dpath,portIdxs)];

        # Do all the sets at once, at the end.
        for pinf,path,portIdx,port in zip(pinfs,dpath,portIdxs,eps):
            # NOP the modification pinf.
            mpinf = copy.copy(pinf);
            mpinf.portState = args.port_state;
            mpinf.portPhysicalState = args.phys_state;
            mpinf.linkSpeedEnabled = 0;
            mpinf.linkWidthEnabled = 0;

            if args.phys_state != 0:
                umad.SubnSet(mpinf,path,portIdx);
            else:
                print "Would have changed %s@%u on %s"%(
                    port.portGUID,portIdx,path);
    return lib.done();
