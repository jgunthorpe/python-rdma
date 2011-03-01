# -*- Python -*-
"""
Provides Python interface to libibverbs.  All of the symbols retain
their names, but there are some differences between C and Python use:

- constructors are used to initialize structures.  For example:
      init = ibv_qp_init_attr(send_cq=cq, recv_cq=cq)
  all of the parameters are optional, so it is still possible
  to do this:
      init = ibv_qp_init_attr()
      init.send_cq = cq
      init.recv_cq = cq
      ...
      qp = ibv_create_qp(pd, init)

- verbs raise exceptions rather than return error codes

- there are no pointers.  When posting a request to a QP, the sg_list
  is a tuple of ibv_mr objects.  These are constructed from any
  Python object supporting the buffer interface and are automatically
  associated with a memory region.  It is the caller's responsibility
  to keep a reference to the region until the relevant completion is
  reaped.

    m = mmap(-1,length)
    mr1 = ibv_mr(m, IBV_LOCAL_WRITE)
    mr2 = ibv_mr('foo')

    wr = ibv_send_wr()
    wr.sg_list=(ibv_sge(addr=mr.addr,length=mr.length,lkey=mr.lkey),
                ibv_sge(addr=mr2.addr,length=mr2.length,lkey=mr2.key))
    ...
    rc = ibv_post_send(



- can use methods on verb objects, eg:
      qp.modify(attr, mask)
  is equivalent to:
      ibv_modify_qp(qp, attr, mask)

- structure objects maintain the attribute mask by monitoring
  field assignments made by the constructor and subsequent
  assignment statements.

       attr = ibv_qp_attr()
       attr.qp_state        = IBV_QPS_INIT
       attr.pkey_index      = 0
       attr.port_num        = port
       attr.qp_access_flags = IBV_ACCESS_REMOTE_WRITE
       ibv_modify_qp(qp, attr, attr.MASK)

  Remember to zero out MASK if the attr object is reused
  for another call.
"""
import errno as mod_errno
from util import struct

class VerbError(Exception):
    def __init__(self,**kwargs):
        for k,v in kwargs.iteritems():
            setattr(self,k,v)

debug = False

cimport libibverbs as c

cdef extern from 'types.h':
    ctypedef void **const_void_ptr_ptr

cdef extern from 'errno.h':
    int errno

cdef extern from 'stdlib.h':
    int sizeof(...)
    void *malloc(int size)
    void *calloc(int n, int size)
    void free(void *ptr)

cdef extern from 'stdint.h':
    ctypedef int uintptr_t
    ctypedef long uint64_t

cdef extern from 'Python.h':
    ctypedef int Py_ssize_t
    int PyObject_AsReadBuffer(object o, void **buffer, Py_ssize_t *len)
    int PyObject_AsWriteBuffer(object o, void **buffer, Py_ssize_t *len)
    void Py_INCREF(object o)
    void Py_DECREF(object o)

include 'libibverbs.pxi'

cdef class ibv_context:
    cdef c.ibv_context *_ctx

    def __cinit__(self, name):
        cdef c.ibv_device **dev_list
        cdef int i
        cdef int count
        cdef int e

        dev_list = c.ibv_get_device_list(&count)
        if dev_list == NULL:
            raise OSError(errno, "Failed to get device list")

        for 0 <= i < count:
            if dev_list[i].name == name:
                break
        if i == count:
            e = mod_errno.ENODEV
        else:
            self._ctx = c.ibv_open_device(dev_list[i])
            if self._ctx == NULL:
                e = errno

        c.ibv_free_device_list(dev_list)
        if e != 0:
            raise OSError(e, None)

    def __dealloc__(self):
        cdef int e
        if self._ctx != NULL:
            e = c.ibv_close_device(self._ctx)
            if e != 0:
                raise OSError(e, "Failed to close device %s"%self._ctx.device.name)

    def query_port(self, port_num):
        cdef c.ibv_port_attr cattr
        cdef int e
        e = c.ibv_query_port(self._ctx, port_num, &cattr)
        if e != 0:
            raise OSError(e, "Failed to query port")

        return ibv_port_attr(state = cattr.state,
                             max_mtu = cattr.max_mtu,
                             active_mtu = cattr.active_mtu,
                             gid_tbl_len = cattr.gid_tbl_len,
                             port_cap_flags = cattr.port_cap_flags,
                             max_msg_sz = cattr.max_msg_sz,
                             bad_pkey_cntr = cattr.bad_pkey_cntr,
                             qkey_viol_cntr = cattr.qkey_viol_cntr,
                             pkey_tbl_len = cattr.pkey_tbl_len,
                             lid = cattr.lid,
                             sm_lid = cattr.sm_lid,
                             lmc = cattr.lmc,
                             max_vl_num = cattr.max_vl_num,
                             sm_sl = cattr.sm_sl,
                             subnet_timeout = cattr.subnet_timeout,
                             init_type_reply = cattr.init_type_reply,
                             active_width = cattr.active_width,
                             active_speed = cattr.active_speed,
                             phys_state = cattr.phys_state)

cdef class ibv_pd:
    cdef object ctx
    cdef c.ibv_pd *_pd

    def __cinit__(self, ibv_context ctx not None):
        self.ctx = ctx
        self._pd = c.ibv_alloc_pd(ctx._ctx)
        if self._pd == NULL:
            raise OSError(errno, "Failed to allocate protection domain")

    def __dealloc__(self):
        cdef int rc
        rc = c.ibv_dealloc_pd(self._pd)
        if rc != 0:
            raise OSError(rc, "Failed to deallocate protection domain")

cdef class ibv_ah:
    cdef c.ibv_ah *_ah

    def __cinit__(self, ibv_pd pd not None, attr):
        cdef c.ibv_ah_attr cattr

        copy_ah_attr(&cattr, attr)
        self._ah = c.ibv_create_ah(pd._pd, &cattr)
        if self._ah == NULL:
            raise OSError(errno, "Failed to create address handle")

    def __dealloc__(self):
        cdef int rc
        if self._ah != NULL:
            rc = c.ibv_destroy_ah(self._ah)
            if rc != 0:
                raise OSError(rc, "Failed to destroy address handle")

cdef class ibv_comp_channel:
    cdef object ctx
    cdef c.ibv_comp_channel *_chan

    def __cinit__(self, ibv_context ctx not None):
        self.ctx = ctx
        self._chan = c.ibv_create_comp_channel(ctx._ctx)
        if self._chan == NULL:
            raise OSError(errno, "Failed to create completion channel")
        self.ctx._chans[self] = 1

    def __dealloc__(self):
        cdef int rc
        rc = c.ibv_destroy_comp_channel(self._chan)
        if rc != 0:
            raise OSError(rc, "Failed to destroy completion channel")
        del self.ctx._chans[self]

cdef class ibv_cq:
    cdef object ctx
    cdef c.ibv_cq *_cq
    cdef object _cookie

    def __cinit__(self, ibv_context ctx not None, int nelems=100, cookie=None,
                  ibv_comp_channel chan or None=None, int vec=0):
        cdef c.ibv_comp_channel *c_chan
        if chan is None:
            c_chan = NULL
        else:
            c_chan = chan._chan
        self.ctx = ctx
        self._cookie = cookie
        self._cq = c.ibv_create_cq(ctx._ctx, nelems, <void*>cookie, c_chan, vec)
        if self._cq == NULL:
            raise OSError(errno, "Failed to create completion queue")

    def __dealloc__(self):
        cdef int rc
        if self._cq == NULL:
            return
        rc = c.ibv_destroy_cq(self._cq)
        if rc != 0:
            raise OSError(rc, "Failed to destroy completion queue")

    def poll(self):
        cdef c.ibv_wc wc
        cdef int n
        cdef list L
        L = []
        while True:
            n = c.ibv_poll_cq(self._cq, 1, &wc)
            if n == 0:
                break
            elif n < 0:
                raise OSError(errno, None)
            else:
                L.append(ibv_wc(wr_id = wc.wr_id,
                                status = wc.status,
                                opcode = wc.opcode,
                                vendor_err = wc.vendor_err,
                                byte_len = wc.byte_len,
                                imm_data = wc.imm_data,
                                qp_num = wc.qp_num,
                                src_qp = wc.src_qp,
                                wc_flags = wc.wc_flags,
                                pkey_index = wc.pkey_index,
                                slid = wc.slid,
                                sl = wc.sl,
                                dlid_path_bits = wc.dlid_path_bits))
        return L

cdef class ibv_mr:
    cdef public object pd
    cdef c.ibv_mr *_mr
    cdef object _buf

    property addr:
        def __get__(self):
            return <uintptr_t>self._mr.addr

    property length:
        def __get__(self):
            return self._mr.length

    property lkey:
        def __get__(self):
            return self._mr.lkey

    property rkey:
        def __get__(self):
            return self._mr.rkey

    def __cinit__(self, ibv_pd pd not None, buf, access=0):
        cdef void *addr
        cdef Py_ssize_t length
        cdef int rc

        if access & (c.IBV_ACCESS_LOCAL_WRITE | c.IBV_ACCESS_REMOTE_WRITE) != 0:
            rc = PyObject_AsWriteBuffer(buf, &addr, &length)
        else:
            rc = PyObject_AsReadBuffer(buf, <const_void_ptr_ptr>&addr, &length)
        if rc != 0:
            raise TypeError("Expected buffer")

        self.pd = pd
        self._buf = buf
        self._mr = c.ibv_reg_mr(pd._pd, addr, length, access)
        if self._mr == NULL:
            raise OSError(errno, "Failed to register memory region")

    def __dealloc__(self):
        cdef int rc
        if self._mr != NULL:
            rc = c.ibv_dereg_mr(self._mr)
            if rc != 0:
                raise OSError(errno, "Failed to deregister memory region")

cdef void copy_ah_attr(c.ibv_ah_attr *cattr, attr):
    if not typecheck(attr, ibv_ah_attr):
        raise TypeError("attr must be an ibv_ah_attr")

    cattr.is_global = attr.is_global
    if cattr.is_global:
        if not typecheck(attr.grh, ibv_global_route):
            raise TypeError("attr.grh must be an ibv_global_route")
        if not typecheck(attr.grh.dgid, ibv_gid):
            raise TypeError("attr.grh.dgid must be an ibv_gid")
        for 0 <= i < 16:
            cattr.grh.dgid.raw[i] = attr.grh.dgid.raw[i]
        cattr.grh.flow_label = attr.grh.flow_label
        cattr.grh.sgid_index = attr.grh.sgid_index
        cattr.grh.hop_limit = attr.grh.hop_limit
        cattr.grh.traffic_class = attr.grh.traffic_class

    cattr.dlid = attr.dlid
    cattr.sl = attr.sl
    cattr.src_path_bits = attr.src_path_bits
    cattr.static_rate = attr.static_rate
    cattr.port_num = attr.port_num

cdef class ibv_qp:
    cdef object pd
    cdef c.ibv_qp *_qp
    cdef c.ibv_qp_cap _cap
    cdef int _qp_type

    property qp_num:
        def __get__(self):
            return self._qp.qp_num
    property qp_type:
        def __get__(self):
            return self._qp.qp_type
    property state:
        def __get__(self):
            return self._qp.state

    def __cinit__(self,
                  ibv_pd pd not None,
                  init):
        cdef c.ibv_qp_init_attr cinit
        cdef ibv_cq scq, rcq

        if not typecheck(init.send_cq, ibv_cq):
            raise TypeError("send_cq must be a ibv_cq")
        if not typecheck(init.recv_cq, ibv_cq):
            raise TypeError("recv_cq must be a ibv_cq")
        if not typecheck(init.cap, ibv_qp_cap):
            raise TypeError("cap must be a ibv_qp_cap")
        if init.srq is not None:
            raise TypeError("srq not supported")

        scq = init.send_cq
        rcq = init.recv_cq

        cinit.send_cq = scq._cq
        cinit.recv_cq = rcq._cq
        cinit.srq = NULL
        cinit.cap.max_send_wr = init.cap.max_send_wr
        cinit.cap.max_recv_wr = init.cap.max_recv_wr
        cinit.cap.max_send_sge = init.cap.max_send_sge
        cinit.cap.max_recv_sge = init.cap.max_recv_sge
        cinit.cap.max_inline_data = init.cap.max_inline_data
        cinit.qp_type = init.qp_type
        cinit.sq_sig_all = init.sq_sig_all

        self.pd = pd
        self._qp = c.ibv_create_qp(pd._pd, &cinit)
        if self._qp == NULL:
            raise OSError(errno, "Failed to create queue pair")
        self._qp_type = cinit.qp_type
        self._cap = cinit.cap

    def __dealloc__(self):
        cdef int rc
        if self._qp != NULL:
            rc = c.ibv_destroy_qp(self._qp)
            if rc != 0:
                raise OSError(errno, "Failed to destroy queue pair")

    cdef _modify(self,attr,mask):
        cdef c.ibv_qp_attr cattr
        cdef int rc
        cdef int cmask

        cmask = mask
        if debug:
            print 'modify qp, attr = %s mask = 0x%x' % (str(attr), cmask)
        if not typecheck(mask, int):
            raise TypeError("mask must be an int")
        if not typecheck(attr, ibv_qp_attr):
            raise TypeError("attr must be a qp_attr")
        cattr.qp_state = attr.qp_state
        cattr.cur_qp_state = attr.cur_qp_state
        cattr.en_sqd_async_notify = attr.en_sqd_async_notify
        cattr.qp_access_flags = attr.qp_access_flags
        cattr.pkey_index = attr.pkey_index
        cattr.port_num = attr.port_num
        cattr.qkey = attr.qkey

        if cmask & IBV_QP_AV:
            copy_ah_attr(&cattr.ah_attr, attr.ah_attr)

        cattr.path_mtu = attr.path_mtu
        cattr.timeout = attr.timeout
        cattr.retry_cnt = attr.retry_cnt
        cattr.rnr_retry = attr.rnr_retry
        cattr.rq_psn = attr.rq_psn
        cattr.max_rd_atomic = attr.max_rd_atomic

        if cmask & IBV_QP_ALT_PATH:
            copy_ah_attr(&cattr.alt_ah_attr, attr.alt_ah_attr)
            cattr.alt_pkey_index = attr.alt_pkey_index
            cattr.alt_port_num = attr.alt_port_num
            cattr.alt_timeout = attr.alt_timeout

        cattr.min_rnr_timer = attr.min_rnr_timer
        cattr.sq_psn = attr.sq_psn
        cattr.max_rd_atomic = attr.max_rd_atomic
        cattr.path_mig_state = attr.path_mig_state

        if cmask & c.IBV_QP_CAP:
            cattr.cap.max_send_wr = attr.cap.max_send_wr
            cattr.cap.max_recv_wr = attr.cap.max_recv_wr
            cattr.cap.max_send_sge = attr.cap.max_send_sge
            cattr.cap.max_recv_sge = attr.cap.max_recv_sge
            cattr.cap.max_inline_data = attr.cap.max_inline_data

        cattr.dest_qp_num = attr.dest_qp_num

        rc = c.ibv_modify_qp(self._qp, &cattr, cmask)
        if rc != 0:
            raise OSError(errno, "Failed to modify qp")

        if cmask & c.IBV_QP_CAP:
            self._cap = cattr.cap

    cdef post_check(self, arg, wrtype, max_sge):
        cdef list wrlist
        cdef int i, n

        if isinstance(arg, wrtype):
            wrlist = [arg]
        elif (isinstance(arg, list) or isinstance(arg, tuple)) and len(arg) > 0:
            wrlist = arg
        else:
            raise TypeError("Expecting a work request or a list/tuple of work requests")

        for wr in wrlist:
            if not typecheck(wr, wrtype):
                raise TypeError("Work request must be of type %s" % wrtype.__name__)
            if typecheck(wr.sg_list, ibv_sge):
                sglist = [wr.sg_list]
            elif isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
                sglist = wr.sg_list
            n = len(sglist)
            if n > max_sge:
                raise TypeError("Too many scatter/gather entries in work request")
            for 0 <= i < n:
                if not typecheck(sglist[i], ibv_sge):
                    raise TypeError("sg_list entries must be of type ibv_sge")
        return wrlist

    cdef _post_send(self, arg):
        cdef list sglist, wrlist
        cdef char *mem, *p
        cdef c.ibv_send_wr dummy_wr, *cwr, *cbad_wr
        cdef c.ibv_sge dummy_sge, *csge
        cdef c.ibv_ah dummy_ah, *cah
        cdef int i, j, n, rc, sgsize, wrsize
        cdef ibv_ah ah

        wrlist = self.post_check(arg, ibv_send_wr, self._cap.max_send_wr)

        n = len(wrlist)
        sgsize = sizeof(dummy_sge) * self._cap.max_send_wr
        wrsize = (sizeof(dummy_wr) + sgsize + sizeof(dummy_ah))

        mem = <char *>calloc(1,wrsize*n);
        if mem == NULL:
            raise MemoryError()

        for 0 <= i < n:
            wr = wrlist[i]
            p = mem + wrsize * i
            cwr = <c.ibv_send_wr *>(p)
            cwr.wr_id = <uintptr_t>wr.wr_id
            if i == n - 1:
                cwr.next = NULL
            else:
                cwr.next = <c.ibv_send_wr *>(p + wrsize)
            cwr.sg_list = <c.ibv_sge *>(p + sizeof(dummy_wr))
            if typecheck(wr.sg_list, list) or typecheck(wr.sg_list, tuple):
                sglist = wr.sg_list
            else:
                sglist = [wr.sg_list]
            cwr.num_sge = len(sglist)
            csge = &cwr.sg_list[0]
            for 0 <= j < cwr.num_sge:
                sge = sglist[j]
                csge.addr = sge.addr
                csge.length = sge.length
                csge.lkey = sge.lkey
                csge += 1

            cwr.opcode = wr.opcode
            if (cwr.opcode == c.IBV_WR_RDMA_WRITE or
                cwr.opcode == c.IBV_WR_RDMA_WRITE_WITH_IMM or
                cwr.opcode == c.IBV_WR_RDMA_READ):
                cwr.wr.rdma.remote_addr = wr.wr.rdma.remote_addr
                cwr.wr.rdma.rkey = wr.wr.rdma.rkey
            elif (cwr.opcode == c.IBV_WR_ATOMIC_FETCH_AND_ADD or
                  cwr.opcode == c.IBV_WR_ATOMIC_CMP_AND_SWP):
                cwr.wr.atomic.remote_addr = wr.wr.atomic.remote_addr
                cwr.wr.atomic.compare_add = wr.wr.atomic.compare_add
                cwr.wr.atomic.swap = wr.wr.atomic.swap
                cwr.wr.atomic.rkey = wr.wr.atomic.rkey
            elif self._qp_type == IBV_QPT_UD:
                # FIXME: check type of wr.wr.ud.ah
                cwr.wr.ud.ah = <c.ibv_ah *>(p + sizeof(dummy_wr) + sgsize)
                ah = wr.wr.ud.ah
                cwr.wr.ud.ah.context = ah._ah.context
                cwr.wr.ud.ah.pd = ah._ah.pd
                cwr.wr.ud.ah.handle = ah._ah.handle

                cwr.wr.ud.remote_qpn = wr.wr.ud.remote_qpn
                cwr.wr.ud.remote_qkey = wr.wr.ud.remote_qkey

            cwr.send_flags = wr.send_flags
            cwr.imm_data = wr.imm_data

        rc = c.ibv_post_send(self._qp, <c.ibv_send_wr *>mem, &cbad_wr)
        if rc != 0:
            n = 0
            while cbad_wr != NULL:
                cbad_wr = cbad_wr.next
                n += 1
            free(mem)
            raise VerbError(msg="Failed to post work request(s)",bad_index=n,errno=errno)
        free(mem)

    cdef _post_recv(self, arg):
        cdef list wrlist
        cdef char *mem, *p
        cdef c.ibv_recv_wr dummy_wr, *cwr, *cbad_wr
        cdef c.ibv_sge dummy_sge, *csge
        cdef int i, j, n, rc, wrsize

        wrlist = self.post_check(arg, ibv_recv_wr, self._cap.max_recv_wr)
        n = len(wrlist)
        wrsize = (sizeof(dummy_wr) +
                  sizeof(dummy_sge) * self._cap.max_recv_wr)

        mem = <char *>calloc(1,wrsize*n);
        if mem == NULL:
            raise MemoryError()

        for 0 <= i < n:
            wr = wrlist[i]
            p = mem + wrsize * i
            cwr = <c.ibv_recv_wr *>(p)
            cwr.wr_id = <uintptr_t>wr.wr_id
            if i == n - 1:
                cwr.next = NULL
            else:
                cwr.next = <c.ibv_recv_wr *>(p + wrsize)
            cwr.sg_list = <c.ibv_sge *>(p + sizeof(dummy_wr))
            if typecheck(wr.sg_list, list) or typecheck(wr.sg_list, tuple):
                sglist = wr.sg_list
            else:
                sglist = [wr.sg_list]
            cwr.num_sge = len(sglist)
            csge = &cwr.sg_list[0]
            for 0 <= j < cwr.num_sge:
                sge = sglist[j]
                csge.addr = sge.addr
                csge.length = sge.length
                csge.lkey = sge.lkey
                csge += 1

        rc = c.ibv_post_recv(self._qp, <c.ibv_recv_wr *>mem, &cbad_wr)
        if rc != 0:
            n = 0
            while cbad_wr != NULL:
                cbad_wr = cbad_wr.next
                n += 1
            free(mem)
            raise VerbError(msg="Failed to post work request(s)",bad_index=n,errno=errno)

        free(mem)

    def query(self,mask):
        cdef c.ibv_qp_attr cattr
        cdef c.ibv_qp_init_attr cinit
        cdef int rc

        rc = c.ibv_query_qp(self._qp, &cattr, mask, &cinit)
        if rc != 0:
            raise OSError(rc, "Failed to query queue pair")

        attr = ibv_qp_attr(qp_state = cattr.qp_state)
        init = ibv_qp_init_attr()
        return (attr, init)

    def modify(self,attr,mask):
        self._modify(attr, mask)

    def post_send(self, wrlist):
        self._post_send(wrlist)

    def post_recv(self, wrlist):
        self._post_recv(wrlist)

def ibv_query_port(ctx, port_num): return ctx.query_port(port_num)
def ibv_create_cq(*args): return ibv_cq(*args)
def ibv_modify_qp(qp, *args): return qp.modify(*args)
def ibv_query_qp(qp, *args): return qp.query(*args)
def ibv_post_send(qp, *args): return qp.post_send(*args)
def ibv_post_recv(qp, *args): return qp.post_recv(*args)
