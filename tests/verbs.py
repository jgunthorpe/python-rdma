#!/usr/bin/python
import unittest;
import mmap;
import sys;
import errno;
import select;
import rdma;
import rdma.vmad;
import rdma.IBA as IBA;
import rdma.ibverbs as ibv;
import rdma.satransactor;
import rdma.path;

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
        print pd,repr(pd)
        cq = self.ctx.cq(100);
        print cq,repr(cq)
        try:
            cq.resize(200);
        except rdma.SysError as e:
            if e.errno != errno.ENOSYS:
                raise;
        self.assertEqual(cq.poll(),[]);
        comp = self.ctx.comp_channel();
        print comp,repr(comp)
        qp = pd.qp(ibv.IBV_QPT_UD,100,cq,100,cq);
        print qp,repr(qp)
        print qp.query(0xFFFF);
        mpath = rdma.path.IBPath(self.ctx.end_port,DLID=0xC000,
                                 DGID=IBA.GID("ff02::1"));
        qp.attach_mcast(mpath);
        qp.detach_mcast(mpath);
        buf = mmap.mmap(-1,4096);
        mr = pd.mr(buf,ibv.IBV_ACCESS_LOCAL_WRITE|ibv.IBV_ACCESS_REMOTE_WRITE);
        print mr,repr(mr)
        print "MR",mr.addr,mr.length,mr.lkey,mr.rkey
        self.assertRaises(TypeError,pd.ah,None);
        ah = pd.ah(self.end_port.sa_path);
        print ah,repr(ah)

        srq = pd.srq();
        print srq,repr(srq)
        print srq.query();
        srq.modify(100);

    def _get_loop(self,pd,qp_type,depth=16):
        cc = self.ctx.comp_channel()
        cq = self.ctx.cq(2*depth,cc);
        poller = rdma.vtools.CQPoller(cq,cc);
        srq = pd.srq(depth)
        pool = rdma.vtools.BufferPool(pd,2*depth,256+40);
        pool.post_recvs(srq,depth);

        path_a = rdma.path.IBPath(self.end_port,qkey=999,
                                  DGID=self.end_port.default_gid);
        with rdma.vmad.VMAD(self.ctx,self.end_port.sa_path) as vmad:
            rdma.path.resolve_path(vmad,path_a,reversible=True);
        qp_a = pd.qp(qp_type,depth,cq,depth,cq,srq=srq);
        rdma.path.fill_path(qp_a,path_a,max_rd_atomic=0);

        qp_b = pd.qp(qp_type,depth,cq,depth,cq,srq=srq);
        path_b = path_a.copy().reverse(for_reply=False);
        rdma.path.fill_path(qp_b,path_b,max_rd_atomic=0);
        qp_b.establish(path_b);
        #print "Path B is",repr(path_b)

        path_a = path_b.copy().reverse(for_reply=False);
        qp_a.establish(path_a);
        #print "Path A is",repr(path_a)

        return (path_a,qp_a,path_b,qp_b,poller,srq,pool)

    def _do_loop_test(self,qp_type_name):
        """Test HCA loop back between two QPs as well as SRQ."""
        qp_type = getattr(ibv,"IBV_QPT_%s"%(qp_type_name));
        print "Testing QP to QP loop type %u %s"%(qp_type,qp_type_name)
        with self.ctx.pd() as pd:
            path_a,qp_a,path_b,qp_b,poller,srq,pool = \
                    self._get_loop(pd,qp_type);
            qp_b.post_send(pool.make_send_wr(pool.pop(),256,path_b));
            qp_a.post_send(pool.make_send_wr(pool.pop(),256,path_a));

            recvs = 0;
            sends = 0
            for wc in poller.iterwc(count=4,timeout=0.5):
                if wc.opcode & ibv.IBV_WC_RECV:
                    recvs = recvs + 1
                if wc.opcode == ibv.IBV_WC_SEND:
                    sends = sends + 1
                pool.finish_wcs(srq,wc);
            self.assertFalse(poller.timedout);
            self.assertEquals(recvs,2);
            self.assertEquals(sends,2);

    def test_ud_loop(self):
        self._do_loop_test("UD");
    def test_rc_loop(self):
        self._do_loop_test("RC");
    def test_uc_loop(self):
        self._do_loop_test("UC");

    def test_vmad(self):
        with rdma.vmad.VMAD(self.ctx,self.end_port.sa_path) as vmad:
            ret = vmad.SubnAdmGet(IBA.MADClassPortInfo);
            print repr(vmad.reply_path);
            ret.printer(sys.stdout);

            # Try sending to the SA with a GRH
            path = self.end_port.sa_path.copy();
            rdma.path.resolve_path(vmad,path,True);
            path.has_grh = True;
            path.hop_limit = 255;
            ret = vmad.SubnAdmGet(IBA.MADClassPortInfo,path);
            print "SA reply path grh",repr(vmad.reply_path);

            # Get a LID path to our immediate peer
            drpath = rdma.path.IBDRPath(self.end_port,
                                        drPath="\0%c"%(self.end_port.port_id));
            smad = rdma.satransactor.SATransactor(vmad);
            peer_path = rdma.path.get_mad_path(vmad,smad.get_path_lid(drpath),
                                               dqpn=1,
                                               qkey=IBA.IB_DEFAULT_QP1_QKEY)
            print "Got peer path",repr(peer_path)

            # Try some GMPs to the peer
            ret = vmad.PerformanceGet(IBA.MADClassPortInfo,peer_path);
            print "Got peer reply path",repr(vmad.reply_path);
            ret = vmad.PerformanceGet(IBA.MADClassPortInfo,
                                      peer_path.copy(has_grh=True,
                                                     hop_limit=255));
            print "Got peer reply path grh",repr(vmad.reply_path);

    def test_wr_error(self):
        "Test failing post_send"
        with self.ctx.pd() as pd:
            depth = 16
            path_a,qp_a,path_b,qp_b,poller,srq,pool = \
                    self._get_loop(pd,ibv.IBV_QPT_UD,depth);

            # Overflow the send q
            wr = pool.make_send_wr(pool.pop(),256,path_b);
            self.assertRaises(ibv.WRError,qp_b.post_send,
                              [wr for I in range(0,depth*1024)]);

    def test_wc_raise(self):
        "Test raising a WCError exception"
        with self.ctx.pd() as pd:
            depth = 16
            path_a,qp_a,path_b,qp_b,poller,srq,pool = \
                    self._get_loop(pd,ibv.IBV_QPT_UD,depth);

            # Go past the end of our MR during send
            wr = pool.make_send_wr(pool.pop(),256,path_b);
            wr.sg_list.length = 1024*1024;
            qp_b.post_send(wr);

            for wc in poller.iterwc(count=1,timeout=0.5):
                if wc.status != ibv.IBV_WC_SUCCESS:
                    if wc.qp_num == qp_b.qp_num:
                        print "Expect SEND WC error",ibv.WCError(wc,poller._cq)
                    else:
                        print "Expect RECV WC error",ibv.WCError(wc,poller._cq)
                    self.assertRaises(ibv.WCError,pool.finish_wcs,srq,wc);
                else:
                    pool.finish_wcs(srq,wc);

    def test_async_handle(self):
        "Test async event functionality"
        print ibv.AsyncError((ibv.IBV_EVENT_LID_CHANGE,self.end_port))
        print ibv.AsyncError((ibv.IBV_EVENT_QP_FATAL,None))

        self.ctx.handle_async_event((ibv.IBV_EVENT_LID_CHANGE,self.end_port))
        self.ctx.handle_async_event((ibv.IBV_EVENT_PKEY_CHANGE,self.end_port))
        self.ctx.handle_async_event((ibv.IBV_EVENT_SM_CHANGE,self.end_port))
        self.assertRaises(ibv.AsyncError,self.ctx.handle_async_event,
                          (ibv.IBV_EVENT_SRQ_ERR,None))

    def test_remote_caused_wc_err(self):
        with self.ctx.pd() as pd:
            depth = 16
            path_a,qp_a,path_b,qp_b,poller,srq,pool = \
                    self._get_loop(pd,ibv.IBV_QPT_UD,depth);

            # Send a packet larger than we can receive
            qp_b.post_send(pool.make_send_wr(0,256,path_b));
            wr = pool.make_send_wr(0,pool.size,path_b);
            wr.sg_list.length = 1000;
            qp_b.post_send(wr);
            qp_b.post_send(pool.make_send_wr(0,256,path_b));

            for wc in poller.iterwc(count=6,timeout=1):
                if wc.status != ibv.IBV_WC_SUCCESS:
                    if wc.qp_num == qp_b.qp_num:
                        print "Expect SEND WC error",ibv.WCError(wc,poller._cq)
                    else:
                        print "Expect RECV WC error",ibv.WCError(wc,poller._cq)
                    self.assertRaises(ibv.WCError,pool.finish_wcs,srq,wc);
                else:
                    pool.finish_wcs(srq,wc);
            self.assertFalse(poller.timedout);

if __name__ == '__main__':
    unittest.main()
