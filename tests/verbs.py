#!/usr/bin/python
import unittest;
import mmap;
import rdma;
import rdma.IBA as IBA;
import rdma.ibverbs as ibv;

class umad_self_test(unittest.TestCase):
    umad = None;
    tid = 0;

    def setUp(self):
        self.end_port = rdma.get_end_port();
        self.ctx = rdma.get_verbs(self.end_port);
        self.umad = rdma.get_umad(self.end_port);

    def tearDown(self):
        self.ctx.close();
        self.ctx = None;
        self.umad.close();
        self.umad = None;

    def test_basic(self):
        print self.ctx.query_port();
        print self.ctx.query_device();
        pd = self.ctx.pd();
        cq = self.ctx.cq();
        self.assertEqual(cq.poll(),[]);
        comp = self.ctx.comp_channel();
        buf = mmap.mmap(-1,4096);
        # qp
        mr = pd.mr(buf,ibv.IBV_ACCESS_LOCAL_WRITE|ibv.IBV_ACCESS_REMOTE_WRITE);
        print "MR",mr.addr,mr.length,mr.lkey,mr.rkey
        self.assertRaises(TypeError,pd.ah,None);
        print pd.ah(self.end_port.sa_path);

