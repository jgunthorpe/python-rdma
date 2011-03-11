from __future__ import with_statement;

import collections;
import os;
import rdma;
import rdma.devices;
import rdma.IBA as IBA;
import rdma.ibverbs as ibv;
import rdma.madtransactor
import rdma.vtools;

class VMAD(rdma.madtransactor.MADTransactor):
    '''Provide a UMAD style interface that runs on ibverbs. This can be
    used with GMP (eg QPN=1) traffic.'''
    #: :class:`rdma.devices.EndPort` this is associated with.
    end_port = None;

    _pd = None;
    _cq = None;
    _ctx = None;
    _allocated_ctx = False;

    def __init__(self,parent,path,depth=16):
        """*path* is used to set the PKey and QKey for all MADs sent through
        this interface."""
        rdma.madtransactor.MADTransactor.__init__(self);
        self._tid = int(os.urandom(8).encode("hex"),16);

        if isinstance(parent,rdma.devices.EndPort):
            self._ctx = rdma.get_verbs(parent);
            self._allocated_ctx = True;
        elif isinstance(parent,ibv.Context):
            self._ctx = parent;
        self.end_port = self._ctx.end_port;

        self._cc = self._ctx.comp_channel();
        self._cq = self._ctx.cq(2*depth,self._cc);
        self._poller = rdma.vtools.CQPoller(self._cq);

        self._pd = self._ctx.pd();
        self._pool = rdma.vtools.BufferPool(self._pd,2*depth,256+40);
        self._qp = self._pd.qp(ibv.IBV_QPT_UD,depth,self._cq,
                               depth,self._cq);
        self._pool.post_recvs(self._qp,min(self._qp.max_recv_wr,depth));
        self._recvs = collections.deque();

        # Adjust the number of buffers so that we can't exceed the send q depth
        while len(self._pool._buffers) > self._qp.max_send_wr:
            self._pool._buffers.pop();

        path = path.copy(sqpn=self._qp.qp_num,sqpsn=self._tid&0xFFFFFF);
        self._qp.establish(path);
        self.qkey = path.qkey;
        self.pkey = path.pkey;

    def sendto(self,buf,path):
        '''Send a MAD packet. *buf* is the raw MAD to send, starting with the first
        byte of :class:`rdma.IBA.MADHeader`. *path* is the destination.'''
        while not self._pool._buffers:
            self._cq_drain();
            if not self._pool._buffers:
                self._cq_sleep(None);

        if path.qkey != self.qkey or path.pkey != self.pkey:
            raise rdma.RDMAError("Destination %r does not match the qkey or pkey of this VMAD instance."%(path));

        buf_idx = self._pool.pop();
        self._pool.copy_to(buf,buf_idx);
        self._qp.post_send(self._pool.make_send_wr(buf_idx,len(buf),path));

    def _cq_drain(self):
        """Empty the CQ and return and send buffers back to the pool. receive
        buffers are queued onto :attr:`_recvs` for later retrieval."""
        wcs = self._cq.poll();
        for I,wc in enumerate(wcs):
            if wc.opcode == ibv.IBV_WC_RECV and wc.status == ibv.IBV_WC_SUCCESS:
                wcs[I] = None;
                self._recvs.appendleft(wc);
        self._pool.finish_wcs(self._qp,wcs);

    def recvfrom(self,wakeat):
        '''Receive a MAD packet. If the value of
        :func:`rdma.tools.clock_monotonic()` exceeds *wakeat* then :class:`None`
        is returned.

        :returns: tuple(buf,path)'''
        pool = self._pool
        while True:
            if self._recvs:
                wc = self._recvs.pop();
                buf = pool.copy_from(wc.wr_id,40,wc.byte_len);
                pool.finish_wcs(self._qp,wc);
                return (buf,ibv.WCPath(self.end_port,wc,
                                       pool._mem,
                                       (wc.wr_id & pool.BUF_IDX_MASK)*pool.size,
                                       pkey=self.pkey,
                                       qkey=self.qkey));

            self._cq.req_notify();
            self._cq_drain();
            if not self._recvs:
                if not self._poller.sleep(wakeat):
                    return None;

    def _execute(self,buf,path,sendOnly = False):
        """Send the fully formed MAD in buf to path and copy the reply
        into buf. Return path of the reply. This is a synchronous method, all
        MADs received during this call are discarded until the reply is seen."""
        self.sendto(buf,path);
        if sendOnly:
            return None;
        rmatch = self._get_reply_match_key(buf);
        expire = path.mad_timeout + rdma.tools.clock_monotonic();
        retries = path.retries;
        while True:
            ret = self.recvfrom(expire);
            if ret is None:
                if retries == 0:
                    return None;
                retries = retries - 1;
                self._execute(buf,path,True);

                expire = path.mad_timeout + rdma.tools.clock_monotonic();
                continue;
            elif rmatch == self._get_match_key(ret[0]):
                return ret;
            else:
                if self.trace_func is not None:
                    self.trace_func(self,rdma.madtransactor.TRACE_UNEXPECTED,
                                    path=path,ret=ret);

    def __enter__(self):
        return self;

    def __exit__(self,*exc_info):
        return self.close();

    def close(self):
        """Free the resources held by the object."""
        if self._pool is not None:
            self._pool.close();
        if self._pd is not None:
            self._pd.close();
        if self._cq is not None:
            self._cq.close();
        if self._cc is not None:
            self._cc.close();
        if self._allocated_ctx and self._ctx is not None:
            self._ctx.close();

    def _get_new_TID(self):
        self._tid = (self._tid + 1) % (1 << 32);
        return self._tid;

    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self.end_port,
                id(self));

