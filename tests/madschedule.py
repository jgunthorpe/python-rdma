#!/usr/bin/python
from __future__ import with_statement;
import unittest
import sys;
from contextlib import contextmanager;
import rdma,rdma.path,rdma.sched;
import rdma.IBA as IBA;

class madschedule_test(unittest.TestCase):
    umad = None;
    tid = 0;

    def setUp(self):
        self.end_port = rdma.get_end_port();
        self.umad = rdma.get_umad(self.end_port);
        self.local_path = rdma.path.IBDRPath(self.end_port);

    def tearDown(self):
        self.umad.close();
        self.umad = None;

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

    def test_except(self):
        """Check that exceptions flow up the coroutine call chain."""
        def second(self):
            self.count = self.count + 1;
            raise rdma.RDMAError("moo");

        def first(self):
            try:
                yield second(self);
            except rdma.RDMAError:
                self.count = self.count + 1;
                raise

        self.count = 0;
        sched = rdma.sched.MADSchedule(self.umad);
        with self.with_assertRaises(rdma.RDMAError):
            sched.run(first(self));
        self.assertEqual(self.count,2);

    def test_except_mad(self):
        """Check that exceptions flow from the MAD decoder."""
        def first(self,sched):
            inf = yield sched.SubnGet(IBA.SMPNodeInfo,self.local_path);
            with self.with_assertRaises(rdma.MADError):
                yield sched.SubnGet(IBA.SMPPortInfo,
                                    self.local_path,inf.numPorts+1);

        sched = rdma.sched.MADSchedule(self.umad);
        sched.run(first(self,sched));

    def get_port_info(self,sched,path,port,follow):
        print "Get port_info %u follow=%r"%(port,follow)
        pinf = yield sched.SubnGet(IBA.SMPPortInfo,path,port);
        print "Done port",port;
        #pinf.printer(sys.stdout);

        if follow and pinf.portState != IBA.PORT_STATE_DOWN:
            npath = rdma.path.IBDRPath(self.end_port);
            npath.drPath = path.drPath + chr(port);
            print "Probe port",port,repr(npath.drPath)
            yield self.get_node_info(sched,npath);

    def get_node_info(self,sched,path):
        ninf = yield sched.SubnGet(IBA.SMPNodeInfo,path);
        if ninf.nodeGUID in self.guids:
            return;
        self.guids.add(ninf.nodeGUID);

        print "Got Node %r"%(ninf.nodeGUID);
        if ninf.nodeType == IBA.NODE_SWITCH:
            sched.mqueue(self.get_port_info(sched,path,I,True) \
                         for I in range(1,ninf.numPorts+1));
            pinf = yield sched.SubnGet(IBA.SMPPortInfo,path,0);
        else:
            yield self.get_port_info(sched,path,ninf.localPortNum,
                                     len(path.drPath) == 1);

    def test_sched(self):
        """Do a simple directed route discovery of the subnet"""
        self.guids = set();
        sched = rdma.sched.MADSchedule(self.umad)
        try:
            sched.run(self.get_node_info(sched,self.local_path));
        except rdma.MADError as err:
            print err
            err.req._buf = bytes(err.req._buf);
            err.req.printer(sys.stdout);
            raise;
