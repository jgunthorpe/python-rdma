from __future__ import with_statement;

import collections;
import mmap;
import rdma.ibverbs as ibv;

class BufferPool(object):
    """Hold onto a block of fixed size buffers and provide some helpers for
    using them as send and receive buffers with a QP.

    This can be used to provide send buffers for a QP, as well as receive
    buffers for a QP or a SRQ. Generally the *qp* argument to methods of this
    class can be a :class:`rdma.ibverbs.QP` or :class:`rdma.ibverbs.SRQ`."""
    #: Constant value to set wr_id to when it is not being used.
    NO_WR_ID = 0xFFFFFFFF;
    _mr = None;
    _mem = None;
    #: `deque` of buffer indexes
    _buffers = None;
    #: Size of the buffers
    size = 0;
    #: Number of buffers
    count = 0;

    def __init__(self,pd,count,size):
        """Create a :class:`rdma.ibverbs.MR` in *pd* with *count* buffers of
        *size* bytes."""
        self.count = count;
        self.size = size;
        self._mem = mmap.mmap(-1,count*size);
        self._mr = pd.mr(self._mem,ibv.IBV_ACCESS_LOCAL_WRITE |
                         ibv.IBV_ACCESS_LOCAL_WRITE);
        self._buffers = collections.deque(xrange(count),count);

    def close(self):
        """Close held objects"""
        if self._mr is not None:
            self._mr.close();
            self._mr = None;
        if self._mem is not None:
            self._mem.close();
            self._mem = None;

    def pop(self):
        """Return a new buffer index."""
        return self._buffers.pop();

    def post_recvs(self,qp,count):
        """Post *count* buffers for receive to *qp*, which may be any object
        with a `post_recv` method."""
        if count == 0:
            return;

        wr = [];
        for I in range(count):
            buf_idx = self._buffers.pop();
            wr.append(ibv.recv_wr(wr_id=buf_idx,
                                  sg_list=self.make_sge(buf_idx,self.size)));
        qp.post_recv(wr);

    def finish_wcs(self,qp,wcs):
        """Process work completion list *wcs* to recover buffers attached to
        completed work and re-post recv buffers to qp. Every work request with
        an attached buffer must have a signaled completion to recover the buffer.

        :raises rdma.ibverbs.WCError: For WC's marked as error."""
        new_recvs = 0;
        for wc in wcs:
            if wc is None:
                continue;
            if wc.status != ibv.IBV_WC_SUCCESS:
                raise ibv.WCError(wc);
            if wc.opcode & ibv.IBV_WC_RECV:
                if wc.wr_id != self.NO_WR_ID:
                    self._buffers.append(wc.wr_id);
                new_recvs = new_recvs + 1;
            if (wc.opcode == ibv.IBV_WC_SEND or
                wc.opcode == ibv.IBV_WC_RDMA_WRITE or
                wc.opcode == ibv.IBV_WC_RDMA_READ):
                if wc.wr_id != self.NO_WR_ID:
                    self._buffers.append(wc.wr_id);
        self.post_recvs(qp,new_recvs);

    def make_sge(self,buf_idx,buf_len):
        """Return a :class:`rdma.ibverbs.SGE` for *buf_idx*."""
        return self._mr.sge(buf_len,buf_idx*self.size);

    def copy_from(self,buf_idx,offset=0,length=0xFFFFFFFF):
        """Return a copy of buffer *buf_idx*.

        :rtype: :class:`bytearray`"""
        length = min(length,self.size - offset)
        return bytearray(self._mem[buf_idx*self.size + offset:
                                   buf_idx*self.size + offset + length]);

    def copy_to(self,buf,buf_idx,offset=0,length=0xFFFFFFFF):
        """Copy *buf* into the buffer *buf_idx*"""
        blen = len(buf)
        length = min(length,self.size - offset,blen)
        if isinstance(buf,bytearray):
            buf = bytes(buf);
        if blen > length:
            self._mem[buf_idx*self.size + offset:
                      buf_idx*self.size + offset + length] = buf[:blen];
        else:
            self._mem[buf_idx*self.size + offset:
                      buf_idx*self.size + offset + length] = buf;
