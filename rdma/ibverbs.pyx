# -*- Python -*-
import errno as mod_errno
from util import struct
import rdma.devices

class WRError(rdma.SysError):
    def __init__(self,errno,func,msg,bad_index):
        rdma.SysError.__init__(self,errno,func,msg);
        self.bad_index = bad_index;

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

cdef class Context:
    """Verbs context handle, this is a context manager. Call :func:`rdma.get_verbs` to get
    an instance of this."""
    cdef c.ibv_context *_ctx
    cdef public object node
    cdef public object port
    cdef list _children

    def __cinit__(self,parent):
        '''Create a :class:`rdma.uverbs.UVerbs` instance for the associated
        :class:`rdma.devices.RDMADevice`/:class:`rdma.devices.EndPort`.'''
        cdef c.ibv_device **dev_list
        cdef int i
        cdef int count

        if typecheck(parent,rdma.devices.RDMADevice):
            self.node = parent
            self.port = None
        else:
            self.node = parent.parent
            self.port = parent

        dev_list = c.ibv_get_device_list(&count)
        if dev_list == NULL:
            raise rdma.SysError(errno,"ibv_get_device_list",
                                "Failed to get device list")

        try:
            for 0 <= i < count:
                if dev_list[i].name == self.node.name:
                    break
            else:
                raise rdma.RDMAError("RDMA verbs device %r not found."%(self.node));

            self._ctx = c.ibv_open_device(dev_list[i])
            if self._ctx == NULL:
                raise rdma.SysError(errno,"ibv_open_device",
                                    "Failed to get device list")
        finally:
            c.ibv_free_device_list(dev_list)

        self._children = list();

    def __dealloc__(self):
        self.close();

    def __enter__(self):
        return self;

    def __exit__(self,*exc_info):
        return self.close();

    def close(self):
        """Free the verbs context handle and all resources allocated by it."""
        cdef int e
        while self._children:
            self._children.pop().close();
        if self._ctx != NULL:
            e = c.ibv_close_device(self._ctx)
            if e != 0:
                raise rdma.SysError(e,"ibv_close_device",
                                    "Failed to close device %s"%self._ctx.device.name)
            self._ctx = NULL

    def query_port(self, port_id=None):
        """Return a :class:port_attr: for the *port_id*. If *port_id* is
        none then the port info is returned for the end port this context was
        created against.

        :rtype: :class:`rdma.ibverbs.port_attr`"""
        cdef c.ibv_port_attr cattr
        cdef int e
        if port_id is None:
            port_id = self.port.port_id;

        e = c.ibv_query_port(self._ctx, port_id, &cattr)
        if e != 0:
            raise rdma.SysError(e,"ibv_query_port",
                                "Failed to query port %r"%(port_id))

        return port_attr(state = cattr.state,
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

    def pd(self):
        """Create a new :class:`rdma.ibverbs.PD` for this context."""
        ret = PD(self);
        self._children.append(ret);
        return ret;

    def cq(self,**kwargs):
        """Create a new :class:`rdma.ibverbs.CQ` for this context."""
        ret = CQ(self,**kwargs);
        self._children.append(ret);
        return ret;

    def comp_channel(self):
        """Create a new :class:`rdma.ibverbs.CompChannel` for this context."""
        ret = CompChannel(self);
        self._children.append(ret);
        return ret;

cdef class PD:
    """Protection domain handle, this is a context manager."""
    cdef Context _context
    cdef c.ibv_pd *_pd
    cdef list _children

    property ctx:
        def __get__(self):
            return self._context;

    def __cinit__(self, Context ctx not None):
        self._context = ctx
        self._pd = c.ibv_alloc_pd(ctx._ctx)
        if self._pd == NULL:
            raise rdma.SysError(errno,"ibv_alloc_pd",
                                "Failed to allocate protection domain")
        self._children = list();

    def __dealloc__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        return self.close()

    def close(self):
        """Free the verbs pd handle."""
        cdef int rc
        while self._children:
            self._children.pop().close();
        if self._pd != NULL:
            if self._context._ctx == NULL:
                raise rdma.RDMAError("Context closed before owned object");
            rc = c.ibv_dealloc_pd(self._pd)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_dealloc_pd",
                                    "Failed to deallocate protection domain")
            self._pd = NULL
            self._context = None;

    def qp(self,init):
        """Create a new :class:`rdma.ibverbs.QP` for this protection domain."""
        ret = QP(self,init);
        self._children.append(ret);
        return ret;

    def mr(self,buf,access=0):
        """Create a new :class:`rdma.ibverbs.MR` for this protection domain."""
        ret = MR(self,buf,access);
        self._children.append(ret);
        return ret;

    def ah(self,attr):
        """Create a new :class:`rdma.ibverbs.AH` for this protection domain."""
        ret = AH(self,attr);
        self._children.append(ret);
        return ret;

cdef class AH:
    """Address handle, this is a context manager."""
    cdef c.ibv_ah *_ah

    def __cinit__(self, PD pd not None, attr):
        cdef c.ibv_ah_attr cattr

        copy_ah_attr(&cattr, attr)
        self._ah = c.ibv_create_ah(pd._pd, &cattr)
        if self._ah == NULL:
            raise rdma.SysError(errno,"ibv_create_ah",
                                "Failed to create address handle")

    def __dealloc__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        return self.close()

    def close(self):
        """Free the verbs AH handle."""
        cdef int rc
        if self._ah != NULL:
            rc = c.ibv_destroy_ah(self._ah)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_destroy_ah",
                                    "Failed to destroy address handle")
            self._ah = NULL

cdef class CompChannel:
    """Completion channel, this is a context manager."""
    cdef Context _context
    cdef c.ibv_comp_channel *_chan

    property ctx:
        def __get__(self):
            return self._context;

    def __cinit__(self, Context ctx not None):
        self._context = ctx
        self._chan = c.ibv_create_comp_channel(ctx._ctx)
        if self._chan == NULL:
            raise rdma.SysError(errno,"ibv_create_comp_channel",
                                "Failed to create completion channel")

    def __dealloc__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        return self.close()

    def close(self):
        """Free the verbs completion channel handle."""
        cdef int rc
        if self._chan != NULL:
            if self._context._ctx == NULL:
                raise rdma.RDMAError("Context closed before owned object");
            rc = c.ibv_destroy_comp_channel(self._chan)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_destroy_comp_channel",
                                    "Failed to destroy completion channel")
            self._chan = NULL
            self._context = None;

cdef class CQ:
    """Completion queue, this is a context manager."""
    cdef Context _context
    cdef c.ibv_cq *_cq
    cdef object _cookie

    property ctx:
        def __get__(self):
            return self._context;

    def __cinit__(self, Context ctx not None, int nelems=100, cookie=None,
                  CompChannel chan or None=None, int vec=0):
        cdef c.ibv_comp_channel *c_chan
        if chan is None:
            c_chan = NULL
        else:
            c_chan = chan._chan
        self._context = ctx
        self._cookie = cookie
        self._cq = c.ibv_create_cq(ctx._ctx, nelems, <void*>cookie, c_chan, vec)
        if self._cq == NULL:
            raise rdma.SysError(errno,"ibv_create_cq",
                                "Failed to create completion queue")

    def __dealloc__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        return self.close()

    def close(self):
        """Free the verbs CQ handle."""
        cdef int rc
        if self._cq != NULL:
            if self._context._ctx == NULL:
                raise rdma.RDMAError("Context closed before owned object");
            rc = c.ibv_destroy_cq(self._cq)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_destroy_cq",
                                    "Failed to destroy completion queue")
            self._cq = NULL
            self._context = None;

    def poll(self):
        """Perform the poll_cq operation, return a list of work requests."""
        cdef c.ibv_wc lwc
        cdef int n
        cdef list L
        L = []
        while True:
            n = c.ibv_poll_cq(self._cq, 1, &lwc)
            if n == 0:
                break
            elif n < 0:
                raise rdma.SysError(errno,"ibv_poll_cq");
            else:
                L.append(wc(wr_id = lwc.wr_id,
                            status = lwc.status,
                            opcode = lwc.opcode,
                            vendor_err = lwc.vendor_err,
                            byte_len = lwc.byte_len,
                            imm_data = lwc.imm_data,
                            qp_num = lwc.qp_num,
                            src_qp = lwc.src_qp,
                            wc_flags = lwc.wc_flags,
                            pkey_index = lwc.pkey_index,
                            slid = lwc.slid,
                            sl = lwc.sl,
                            dlid_path_bits = lwc.dlid_path_bits))
        return L

cdef class MR:
    """Memory registration, this is a context manager."""
    cdef PD _pd
    cdef c.ibv_mr *_mr
    cdef object _buf

    property pd:
        def __get__(self):
            return self._pd;

    property ctx:
        def __get__(self):
            return self._pd._context;

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

    def __cinit__(self, PD pd not None, buf, access=0):
        cdef void *addr
        cdef Py_ssize_t length
        cdef int rc

        if access & (c.IBV_ACCESS_LOCAL_WRITE | c.IBV_ACCESS_REMOTE_WRITE) != 0:
            rc = PyObject_AsWriteBuffer(buf, &addr, &length)
        else:
            rc = PyObject_AsReadBuffer(buf, <const_void_ptr_ptr>&addr, &length)
        if rc != 0:
            raise TypeError("Expected buffer")

        self._pd = pd
        self._buf = buf
        self._mr = c.ibv_reg_mr(pd._pd, addr, length, access)
        if self._mr == NULL:
            raise rdma.SysError(errno,"ibv_reg_mr",
                                "Failed to register memory region")

    def __dealloc__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        return self.close()

    def close(self):
        """Free the verbs MR handle."""
        cdef int rc
        if self._mr != NULL:
            rc = c.ibv_dereg_mr(self._mr)
            if rc != 0:
                raise rdma.SysError(errno,"ibv_dereg_mr",
                                    "Failed to deregister memory region")
            self._mr = NULL

cdef void copy_ah_attr(c.ibv_ah_attr *cattr, attr):
    if not typecheck(attr, ibv_ah_attr):
        raise TypeError("attr must be an ah_attr")

    cattr.is_global = attr.is_global
    if cattr.is_global:
        if not typecheck(attr.grh, global_route):
            raise TypeError("attr.grh must be an global_route")
        if not typecheck(attr.grh.dgid, gid):
            raise TypeError("attr.grh.dgid must be an gid")
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

cdef class QP:
    """Queue pair, this is a context manager."""
    cdef PD _pd
    cdef c.ibv_qp *_qp
    cdef c.ibv_qp_cap _cap
    cdef int _qp_type

    property pd:
        def __get__(self):
            return self._pd;

    property ctx:
        def __get__(self):
            return self._pd._context;

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
                  PD pd not None,
                  init):
        cdef c.ibv_qp_init_attr cinit
        cdef CQ scq, rcq

        if not typecheck(init.send_cq, CQ):
            raise TypeError("send_cq must be a cq")
        if not typecheck(init.recv_cq, CQ):
            raise TypeError("recv_cq must be a cq")
        if not typecheck(init.cap, qp_cap):
            raise TypeError("cap must be a qp_cap")
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

        self._pd = pd
        self._qp = c.ibv_create_qp(pd._pd, &cinit)
        if self._qp == NULL:
            raise rdma.SysError(errno,"ibv_create_qp",
                                "Failed to create queue pair")
        self._qp_type = cinit.qp_type
        self._cap = cinit.cap

    def __dealloc__(self):
        self.close();

    def __enter__(self):
        return self;

    def __exit__(self,*exc_info):
        return self.close();

    def close(self):
        """Free the verbs QP handle."""
        cdef int rc
        if self._qp != NULL:
            rc = c.ibv_destroy_qp(self._qp)
            if rc != 0:
                raise rdma.SysError(errno,"ibv_destroy_qp",
                                    "Failed to destroy queue pair")
            self._qp = NULL;
            self._pd = None;

    cdef _modify(self,attr,mask):
        cdef c.ibv_qp_attr cattr
        cdef int rc
        cdef int cmask

        cmask = mask
        if debug:
            print 'modify qp, attr = %s mask = 0x%x' % (str(attr), cmask)
        if not typecheck(mask, int):
            raise TypeError("mask must be an int")
        if not typecheck(attr, qp_attr):
            raise TypeError("attr must be a qp_attr")
        cattr.qp_state = attr.qp_state
        cattr.cur_qp_state = attr.cur_qp_state
        cattr.en_sqd_async_notify = attr.en_sqd_async_notify
        cattr.qp_access_flags = attr.qp_access_flags
        cattr.pkey_index = attr.pkey_index
        cattr.port_num = attr.port_num
        cattr.qkey = attr.qkey

        if cmask & c.IBV_QP_AV:
            copy_ah_attr(&cattr.ah_attr, attr.ah_attr)

        cattr.path_mtu = attr.path_mtu
        cattr.timeout = attr.timeout
        cattr.retry_cnt = attr.retry_cnt
        cattr.rnr_retry = attr.rnr_retry
        cattr.rq_psn = attr.rq_psn
        cattr.max_rd_atomic = attr.max_rd_atomic

        if cmask & c.IBV_QP_ALT_PATH:
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
            raise rdma.SysError(errno,"ibv_modify_qp",
                                "Failed to modify qp")

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
            if typecheck(wr.sg_list, sge):
                sglist = [wr.sg_list]
            elif isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
                sglist = wr.sg_list
            n = len(sglist)
            if n > max_sge:
                raise TypeError("Too many scatter/gather entries in work request")
            for 0 <= i < n:
                if not typecheck(sglist[i], sge):
                    raise TypeError("sg_list entries must be of type ibv_sge")
        return wrlist

    cdef _post_send(self, arg):
        cdef list sglist, wrlist
        cdef char *mem, *p
        cdef c.ibv_send_wr dummy_wr, *cwr, *cbad_wr
        cdef c.ibv_sge dummy_sge, *csge
        cdef c.ibv_ah dummy_ah, *cah
        cdef int i, j, n, rc, sgsize, wrsize
        cdef AH ah

        wrlist = self.post_check(arg, send_wr, self._cap.max_send_wr)

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
            elif self._qp_type == c.IBV_QPT_UD:
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
            raise WRError(errno,"ibv_post_send","Failed to post work request(s)",n);
        free(mem)

    cdef _post_recv(self, arg):
        cdef list wrlist
        cdef char *mem, *p
        cdef c.ibv_recv_wr dummy_wr, *cwr, *cbad_wr
        cdef c.ibv_sge dummy_sge, *csge
        cdef int i, j, n, rc, wrsize

        wrlist = self.post_check(arg, recv_wr, self._cap.max_recv_wr)
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
            raise WRError(errno,"ibv_post_recv","Failed to post work request(s)",n);

        free(mem)

    def query(self,mask):
        cdef c.ibv_qp_attr cattr
        cdef c.ibv_qp_init_attr cinit
        cdef int rc

        rc = c.ibv_query_qp(self._qp, &cattr, mask, &cinit)
        if rc != 0:
            raise rdma.SysError(rc,"ibv_query_qp",
                                "Failed to query queue pair")

        attr = qp_attr(qp_state = cattr.qp_state)
        init = qp_init_attr()
        return (attr, init)

    def modify(self,attr,mask):
        self._modify(attr, mask)

    def post_send(self, wrlist):
        self._post_send(wrlist)

    def post_recv(self, wrlist):
        self._post_recv(wrlist)
