# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import unittest
import os.path
import sys
from contextlib import contextmanager;
import tests.ibtool
import rdma;
import rdma.IBA as IBA;
import libibtool;

class ibtool_cmds_test(unittest.TestCase):
    get_cmd_func = None;

    @contextmanager
    def with_assertRaises(self,excClass):
        """Emulate the python 2.7 assertRaises"""
        try:
            yield
        except excClass:
            return
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise self.failureException, "%s not raised" % excName

    @contextmanager
    def ignore_mad_unsupported(self):
        try:
            yield
        except rdma.MADError as err:
            if (err.status != IBA.MAD_STATUS_UNSUP_METHOD_ATTR_COMBO and
                err.status != IBA.MAD_STATUS_INVALID_ATTR_OR_MODIFIER):
                raise;

    def setUp(self):
        self.extra_opts = None;
        if self.get_cmd_func is None:
            self.ibtool = sys.modules["tests.ibtool"];
            self.get_cmd_func = self.ibtool.get_cmd_func;
            self.end_port = rdma.get_end_port();

            self.peer_dr = "0,%u"%(self.end_port.port_id);
            with rdma.get_umad(self.end_port) as umad:
                dr = rdma.path.IBDRPath(self.end_port,drPath="\0" +
                                        chr(self.end_port.port_id));
                self.peer_pinf = umad.SubnGet(IBA.SMPPortInfo,dr);
                self.peer_ninf = umad.SubnGet(IBA.SMPNodeInfo,dr);

    def xcmd(self,*args):
        """Run the libib stuff. Switch this out to use diff to compare outputs."""
        if self.extra_opts:
            nargs = args + self.extra_opts;
        else:
            nargs = args;
        print "------------- Execute",nargs," ------------";
        sys.stdout.flush();
        try:
            os.system("/opt/ofa64-1.5.1/sbin/" + " ".join("%s"%(I) for I in args));
        except:
            pass;

    def cmd(self,*args):
        if self.extra_opts:
            args = args + self.extra_opts;
        print "------------- Execute",args," ------------";
        sys.stdout.flush();
        try:
            func,shown = self.get_cmd_func(args[0]);
            o = libibtool.tools.MyOptParse(func);
            if not func(["%s"%(I) for I in args[1:]],o):
                raise self.ibtool.CmdError("Command failed");
        except:
            print "Command %r threw exception"%(args,);
            raise;

    def test_good(self):
        """Test good calls to ibtools"""
        self.cmd("help");
        self.cmd("ibv_devices");
        self.cmd("ibstat");
        self.cmd("ibstat","-l");
        self.cmd("ibstat","-p");
        self.cmd("ibstat","-s");
        self.cmd("ibstatus");
        self.cmd("ibaddr");
        self.cmd("ibaddr","-D","0,");
        self.cmd("ibaddr","-l");
        self.cmd("ibaddr","-g");
        self.cmd("smpdump","-D","0,","0x15");

        for I in ["NI","ND","PI","PKeys","SL2VL","VLArb","GI","SWI"]:
            with self.ignore_mad_unsupported():
                self.cmd("smpquery",I,"-D","0,");

        self.cmd("perfquery");
        for I in ["-x","-X","-S","-D","-E","-F","--vl-xmit-errs","--vl-xmit-wait",
                  "--vl-congestion"]:
            try:
                self.cmd("perfquery",I);
            except rdma.MADError as err:
                if err.status != IBA.MAD_STATUS_UNSUP_METHOD_ATTR_COMBO:
                    raise;
        self.cmd("query","PerformanceGet","MADClassPortInfo");
        self.cmd("set_nodedesc");

    def test_with_link_exc(self):
        self.assertEquals(self.end_port.state,IBA.PORT_STATE_ACTIVE);
        with self.with_assertRaises(rdma.MADError):
            self.cmd("ibaddr","0,99");
        with self.with_assertRaises(rdma.path.SAPathNotFoundError):
            self.cmd("ibaddr","2::");

    def test_with_link(self):
        self.assertEquals(self.end_port.state,IBA.PORT_STATE_ACTIVE);

        self.cmd("ibaddr","-D",self.peer_dr);
        self.cmd("ibaddr",self.end_port.lid);
        self.cmd("ibaddr",self.end_port.port_guid);

        self.cmd("sminfo");
        self.cmd("sminfo",self.end_port.sm_lid);

        self.cmd("ibroute","-D",self.peer_dr);
        self.cmd("ibroute","-D",self.peer_dr,"-M");
        self.cmd("dump_lfts");
        self.cmd("dump_mfts");

        self.cmd("smpquery","si","-D",self.peer_dr);

        for I in ["NI","ND","PI","PKeys","SL2VL","VLArb","GI","SI"]:
            with self.ignore_mad_unsupported():
                self.cmd("smpquery",I,self.peer_pinf.LID);
            with self.ignore_mad_unsupported():
                if I != "SI":
                    self.cmd("smpquery",I,self.end_port.lid);

        self.cmd("perfquery");
        for I in ["-x","-X","-S","-D","-E","-F","--vl-xmit-errs","--vl-xmit-wait",
                  "--vl-congestion"]:
            with self.ignore_mad_unsupported():
                self.cmd("perfquery",I,self.peer_pinf.LID,self.peer_ninf.localPortNum);

        for I in ['CPI', 'PR', 'IIR', 'VLAR', 'MCMR', 'NR', 'SR', 'LR', 'MFTR', 'LFTR', 'SL2VL', 'PKTR', 'PIR', 'SWI']:
            self.cmd("saquery",I);

        self.cmd("ibportstate","-D",self.peer_dr,"1","query");

        self.cmd("ibtracert",self.peer_pinf.LID);
        self.cmd("ibtracert",self.end_port.lid);
        self.cmd("ibtracert",self.peer_ninf.portGUID);

    def test_discovery(self):
        self.assertEquals(self.end_port.state,IBA.PORT_STATE_ACTIVE);

        self.cmd("ibswitches");
        self.cmd("ibhosts");
        self.cmd("ibrouters");
        self.cmd("ibnodes");
        self.cmd("ibnetdiscover");
        self.cmd("ibfindnodesusing",self.peer_dr,"1");

        self.cmd("ibprintca",self.end_port.parent.node_guid);
        self.cmd("ibprintswitch",self.peer_ninf.nodeGUID);

    def test_with_link_no_sa(self):
        self.assertEquals(self.end_port.state,IBA.PORT_STATE_ACTIVE);
        self.cmd("dump_lfts","-D");
        self.cmd("dump_mfts","-D");

    def test_with_link_sa(self):
        self.assertEquals(self.end_port.state,IBA.PORT_STATE_ACTIVE);
        self.extra_opts = ("--sa",);
        self.test_with_link();
        self.test_discovery();

if __name__ == '__main__':
    unittest.main()
