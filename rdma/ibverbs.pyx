# -*- Python -*-
import select
import collections
import errno as mod_errno
import util;
import struct;
import weakref;
import rdma.devices
import rdma.IBA as IBA;
import rdma.path;

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
    object PyBytes_FromStringAndSize(char *str, Py_ssize_t len)
    int PyObject_AsReadBuffer(object o, void **buffer, Py_ssize_t *len)
    int PyObject_AsWriteBuffer(object o, void **buffer, Py_ssize_t *len)
    void Py_INCREF(object o)
    void Py_DECREF(object o)

cdef extern from 'arpa/inet.h':
    unsigned int ntohl(unsigned int v)

include 'libibverbs.pxi'

debug = False

cdef class Context
cdef class PD
cdef class AH
cdef class CompChannel
cdef class CQ
cdef class MR
cdef class QP

class _my_weakset(weakref.WeakKeyDictionary):
    def add(self,v):
        self[v] = None;
    def pop(self):
        return weakref.WeakKeyDictionary.popitem(self)[0];
WeakSet = weakref.__dict__.get("WeakSet",_my_weakset)

class WRError(rdma.SysError):
    """Raised when an error occurs posting work requests. :attr:`bad_index`
    is the index into the work request list what failed to post."""
    def __init__(self,errno,func,msg,bad_index):
        rdma.SysError.__init__(self,errno,func,msg);
        self.bad_index = bad_index;

def wc_status_str(status):
    """Convert a :attr:`rdma.ibverbs.wc.status` value into a string."""
    return c.ibv_wc_status_str(status);

class WCError(rdma.RDMAError):
    """Raised when a WC is completed with error."""
    def __init__(self,wc,msg=None):
        if msg is not None:
            s = "Got error on a CQ - op=%u (%d %s vend=0x%x)"%(
                wc.opcode,wc.stats,c.ibv_wc_status_str(wc.status),
                wc.evndor_err);
        else:
            s = "%s - op=%u (%d %s vend=0x%x)"%(msg,
                wc.opcode,wc.stats,c.ibv_wc_status_str(wc.status),
                wc.evndor_err);
        rdma.RDMAError.__init__(self,s);
        self.wc = wc;

    #wc_status_str = staticmethod(wc_status_str)

def WCPath(end_port,wc,buf=None,off=0,**kwargs):
    """Create a :class:`rdma.path.IBPath` from a work completion. *buf* should
    be the receive buffer when this is used with a UD QP, the first 40 bytes
    of that buffer could be a GRH. *off* is the offset into *buf*. *kwargs*
    are applied to :class:`rdma.path.IBPath`

    Note: wc.pkey_index is not used, if the WC is associated witha GSI QP
    (unlikely) then the caller can pass `pkey_index=wc.pkey_index` as an
    argument."""
    cdef c.ibv_grh *grh
    cdef void *tmp
    cdef Py_ssize_t length
    cdef int flow_class
    cdef object path

    path = rdma.path.IBPath(end_port,sqpn=wc.src_qp,
                            dqpn=wc.qp_num,
                            SLID=wc.slid,
                            SL=wc.sl,
                            DLID_bits=wc.dlid_path_bits,
                            **kwargs);
    if wc.wc_flags & IBV_WC_GRH and buf is not None:
        path.has_grh = True
        flow_class = off;
        if PyObject_AsReadBuffer(buf, <const_void_ptr_ptr>&tmp, &length) != 0:
            raise TypeError("Expected buffer")
        if length - flow_class < 40:
            raise TypeError("buf must be at least 40 bytes long")
        grh = <c.ibv_grh *>(<char *>tmp + flow_class)
        path.DGID = IBA.GID(PyBytes_FromStringAndSize(<char *>grh.dgid.raw,16),True);
        path.SGID = IBA.GID(PyBytes_FromStringAndSize(<char *>grh.sgid.raw,16),True);
        path.hop_limit = grh.hop_limit
        flow_class = ntohl(grh.version_tclass_flow)
        path.traffic_class = (flow_class >> 20) & 0xFF
        path.flow_label = flow_class & 0xFFFFF
    return path;

cdef class Context:
    """Verbs context handle, this is a context manager. Call :func:`rdma.get_verbs` to get
    an instance of this."""
    cdef c.ibv_context *_ctx
    cdef public object node
    cdef public object end_port
    cdef object _children_pd
    cdef object _children_cq
    cdef object _children_cc

    def __cinit__(self,parent):
        '''Create a :class:`rdma.uverbs.UVerbs` instance for the associated
        :class:`rdma.devices.RDMADevice`/:class:`rdma.devices.EndPort`.'''
        cdef c.ibv_device **dev_list
        cdef int i
        cdef int count

        if typecheck(parent,rdma.devices.RDMADevice):
            self.node = parent
            self.end_port = None
        else:
            self.node = parent.parent
            self.end_port = parent

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

        self._children_pd = WeakSet();
        self._children_cq = WeakSet();
        self._children_cc = WeakSet();

    def __dealloc__(self):
        self._close();

    def __enter__(self):
        return self;

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs context handle and all resources allocated by it."""
        self._close();

    cdef _close(self):
        cdef int e
        while self._children_pd:
            self._children_pd.pop().close();
        while self._children_cq:
            self._children_cq.pop().close();
        while self._children_cc:
            self._children_cc.pop().close();
        if self._ctx != NULL:
            e = c.ibv_close_device(self._ctx)
            if e != 0:
                raise rdma.SysError(e,"ibv_close_device",
                                    "Failed to close device %s"%self._ctx.device.name)
            self._ctx = NULL

    def query_device(self):
        """Return a :class:`rdma.ibverbs.device_attr` for the device.

        :rtype: :class:`rdma.ibverbs.device_attr`"""
        cdef c.ibv_device_attr dattr
        cdef int e

        e = c.ibv_query_device(self._ctx, &dattr)
        if e != 0:
            raise rdma.SysError(e,"ibv_query_device",
                                "Failed to query port")
        return device_attr(fw_ver = dattr.fw_ver,
                           node_guid = IBA.GUID(struct.pack("=Q",dattr.node_guid),True),
                           sys_image_guid = IBA.GUID(struct.pack("=Q",dattr.sys_image_guid),True),
                           max_mr_size = dattr.max_mr_size,
                           page_size_cap = dattr.page_size_cap,
                           vendor_id = dattr.vendor_id,
                           vendor_part_id = dattr.vendor_part_id,
                           hw_ver = dattr.hw_ver,
                           max_qp = dattr.max_qp,
                           max_qp_wr = dattr.max_qp_wr,
                           device_cap_flags = dattr.device_cap_flags,
                           max_sge = dattr.max_sge,
                           max_sge_rd = dattr.max_sge_rd,
                           max_cq = dattr.max_cq,
                           max_cqe = dattr.max_cqe,
                           max_mr = dattr.max_mr,
                           max_pd = dattr.max_pd,
                           max_qp_rd_atom = dattr.max_qp_rd_atom,
                           max_ee_rd_atom = dattr.max_ee_rd_atom,
                           max_res_rd_atom = dattr.max_res_rd_atom,
                           max_qp_init_rd_atom = dattr.max_qp_init_rd_atom,
                           max_ee_init_rd_atom = dattr.max_ee_init_rd_atom,
                           atomic_cap = dattr.atomic_cap,
                           max_ee = dattr.max_ee,
                           max_rdd = dattr.max_rdd,
                           max_mw = dattr.max_mw,
                           max_raw_ipv6_qp = dattr.max_raw_ipv6_qp,
                           max_raw_ethy_qp = dattr.max_raw_ethy_qp,
                           max_mcast_grp = dattr.max_mcast_grp,
                           max_mcast_qp_attach = dattr.max_mcast_qp_attach,
                           max_total_mcast_qp_attach = dattr.max_total_mcast_qp_attach,
                           max_ah = dattr.max_ah,
                           max_fmr = dattr.max_fmr,
                           max_map_per_fmr = dattr.max_map_per_fmr,
                           max_srq = dattr.max_srq,
                           max_srq_wr = dattr.max_srq_wr,
                           max_srq_sge = dattr.max_srq_sge,
                           max_pkeys = dattr.max_pkeys,
                           local_ca_ack_delay = dattr.local_ca_ack_delay,
                           phys_port_cnt = dattr.phys_port_cnt);

    def query_port(self, port_id=None):
        """Return a :class:`rdma.ibverbs.port_attr` for the *port_id*. If
        *port_id* is none then the port info is returned for the end port this
        context was created against.

        :rtype: :class:`rdma.ibverbs.port_attr`"""
        cdef c.ibv_port_attr cattr
        cdef int e
        if port_id is None:
            port_id = self.end_port.port_id;

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
        self._children_pd.add(ret);
        return ret;

    def cq(self,nelems=100,cc=None,vec=0):
        """Create a new :class:`rdma.ibverbs.CQ` for this context."""
        ret = CQ(self,nelems,cc,vec);
        self._children_cq.add(ret);
        return ret;

    def comp_channel(self):
        """Create a new :class:`rdma.ibverbs.CompChannel` for this context."""
        ret = CompChannel(self);
        self._children_cc.add(ret);
        return ret;

cdef class PD:
    """Protection domain handle, this is a context manager."""
    cdef object __weakref__
    cdef Context _context
    cdef c.ibv_pd *_pd
    cdef object _children_qp
    cdef object _children_mr
    cdef object _children_ah
    cdef object _path_ah # FIXME: should be str

    property ctx:
        def __get__(self):
            return self._context;

    def __cinit__(self, Context ctx not None):
        self._context = ctx
        self._pd = c.ibv_alloc_pd(ctx._ctx)
        if self._pd == NULL:
            raise rdma.SysError(errno,"ibv_alloc_pd",
                                "Failed to allocate protection domain")
        self._children_qp = WeakSet();
        self._children_mr = WeakSet();
        self._children_ah = WeakSet();
        self._path_ah = "_cached_pd%x_ah"%(id(self));

    def __dealloc__(self):
        self._close();

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs pd handle."""
        self._close();

    cdef _close(self):
        cdef int rc
        while self._children_ah:
            self._children_ah.pop().close();
        while self._children_qp:
            self._children_qp.pop().close();
        while self._children_mr:
            self._children_mr.pop().close();
        if self._pd != NULL:
            if self._context._ctx == NULL:
                raise rdma.RDMAError("Context closed before owned object");
            rc = c.ibv_dealloc_pd(self._pd)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_dealloc_pd",
                                    "Failed to deallocate protection domain")
            self._pd = NULL
            self._context = None;

    def qp_raw(self,init):
        """Create a new :class:`rdma.ibverbs.QP` for this protection
        domain. *init* is a :class:`rdma.ibverbs.qp_init_attr`."""
        ret = QP(self,init);
        self._children_qp.add(ret);
        return ret;

    def qp(self,
           qp_type,
           max_send_wr,
           send_cq,
           max_recv_wr,
           recv_cq,
           srq=None,
           sq_sig_all=1,
           max_send_sge=1,
           max_recv_sge=1,
           max_inline_data=0):
        """Create a new :class:`rdma.ibverbs.QP` for this protection domain.
        This version expresses the QP creation attributes as keyword
        arguments."""
        cap = qp_cap(max_send_wr=max_send_wr,
                     max_recv_wr=max_recv_wr,
                     max_send_sge=max_send_sge,
                     max_recv_sge=max_recv_sge,
                     max_inline_data=max_inline_data)
        init = qp_init_attr(send_cq=send_cq,
                            recv_cq=recv_cq,
                            srq=srq,
                            cap=cap,
                            qp_type=qp_type,
                            sq_sig_all=sq_sig_all)
        ret = QP(self,init);
        self._children_qp.add(ret);
        return ret;

    def mr(self,buf,access=0):
        """Create a new :class:`rdma.ibverbs.MR` for this protection domain."""
        ret = MR(self,buf,access);
        self._children_mr.add(ret);
        return ret;

    def ah(self,attr):
        """Create a new :class:`rdma.ibverbs.AH` for this protection domain.
        *attr* may be a :class:`rdma.ibverbs.ah_attr` or
        :class:`rdma.path.IBPath`. When used with a :class:`~rdma.path.IBPath`
        this function will cache the AH in the
        `IBPath`. :meth:`rdma.path.Path.drop_cache` must be called to release
        all references to the AH."""
        cdef AH ret
        if isinstance(attr,rdma.path.IBPath):
            # We cache the AH in the  onto the AH in the path
            # FIXME: should be getattr but the 3 argument version won't compile
            ret = attr.__dict__.get(self._path_ah);
            if ret is None or ret._ah == NULL:
                ret = AH(self,attr);
                setattr(attr,self._path_ah,ret);
                self._children_ah.add(ret);
            return ret;
        else:
            ret = AH(self,attr);
            self._children_ah.add(ret);
        return ret;

cdef class AH:
    """Address handle, this is a context manager."""
    cdef object __weakref__
    cdef c.ibv_ah *_ah

    def __cinit__(self, PD pd not None, attr):
        cdef c.ibv_ah_attr cattr

        copy_ah_attr(&cattr, attr)
        self._ah = c.ibv_create_ah(pd._pd, &cattr)
        if self._ah == NULL:
            raise rdma.SysError(errno,"ibv_create_ah",
                                "Failed to create address handle")

    def __dealloc__(self):
        self._close();

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs AH handle."""
        self._close();

    cdef _close(self):
        cdef int rc
        if self._ah != NULL:
            rc = c.ibv_destroy_ah(self._ah)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_destroy_ah",
                                    "Failed to destroy address handle")
            self._ah = NULL

cdef class CompChannel:
    """Completion channel, this is a context manager."""
    cdef object __weakref__
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
        self._close();

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs completion channel handle."""
        self._close();

    cdef _close(self):
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

    def fileno(self):
        """Return the FD associated with this completion channel."""
        return self._chan.fd;

    def register_poll(self,poll):
        """Add the FD associated with this object to :class:`select.poll`
        object *poll*."""
        poll.register(self._chan.fd,select.POLLIN);

    def check_poll(self,pevent,solicited_only=False):
        """Returns a :class:`rdma.ibverbs.CQ` that got at least one completion
        event, or `None`. This updates the comp channel and keeps track of
        received events, and appropriately calls ibv_ack_cq_events
        internally. The CQ is re-armed via
        :meth:`rdma.ibverbs.CQ.req_notify_cq`"""
        cdef c.ibv_cq *_cq
        cdef void *p_cq
        cdef CQ cq
        cdef int rc

        if pevent[0] != self._chan.fd:
            return None;
        if pevent[1] & select.POLLIN == 0:
            return None;

        if c.ibv_get_cq_event(self._chan,&_cq,&p_cq) != 0:
            raise rdma.RDMAError("ibv_get_cq_event failed");
        cq = <object>p_cq;

        cq.comp_events = cq.comp_events + 1;
        if cq.comp_events >= (1<<30):
            c.ibv_ack_cq_events(_cq,cq.comp_events);
            cq.comp_events = 0;
        cq.req_notify_cq(solicited_only);
        return cq;

cdef class CQ:
    """Completion queue, this is a context manager."""
    cdef object __weakref__
    cdef Context _context
    cdef c.ibv_cq *_cq
    cdef CompChannel _chan
    cdef public int comp_events

    property ctx:
        def __get__(self):
            return self._context;

    def __cinit__(self, Context ctx not None, int nelems=100,
                  CompChannel chan or None=None, int vec=0):
        cdef c.ibv_comp_channel *c_chan
        if chan is None:
            c_chan = NULL
        else:
            c_chan = chan._chan
        self._context = ctx
        self._chan = chan;
        self.comp_events = 0;
        self._cq = c.ibv_create_cq(ctx._ctx, nelems, <void*>self, c_chan, vec)
        if self._cq == NULL:
            raise rdma.SysError(errno,"ibv_create_cq",
                                "Failed to create completion queue")

    def __dealloc__(self):
        self._close();

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs CQ handle."""
        self._close();

    cdef _close(self):
        cdef int rc
        if self._cq != NULL:
            if self._context._ctx == NULL:
                raise rdma.RDMAError("Context closed before owned object");
            if self.comp_events != 0:
                c.ibv_ack_cq_events(self._cq,self.comp_events);
                self.comp_events = 0;
            rc = c.ibv_destroy_cq(self._cq)
            if rc != 0:
                raise rdma.SysError(rc,"ibv_destroy_cq",
                                    "Failed to destroy completion queue")
            self._cq = NULL
            self._context = None;
            self._chan = None;

    def req_notify_cq(self,solicited_only=False):
        """Request event notification for CQEs added to the CQ."""
        cdef int rc
        rc = c.ibv_req_notify_cq(self._cq,solicited_only);
        if rc != 0:
            raise rdma.SysError(rc,"ibv_req_notify_cq",
                                "Failed to request notification");

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
    cdef object __weakref__
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
        self._close();

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs MR handle."""
        self._close();

    cdef _close(self):
        cdef int rc
        if self._mr != NULL:
            rc = c.ibv_dereg_mr(self._mr)
            if rc != 0:
                raise rdma.SysError(errno,"ibv_dereg_mr",
                                    "Failed to deregister memory region")
            self._mr = NULL

cdef copy_ah_attr(c.ibv_ah_attr *cattr, attr):
    """Fill in an ibv_ah_attr from *attr*. *attr* can be a
    :class:`rdma.ibverbs.ah_attr` which is copied directly (discouraged) or it
    can be a :class:`rdma.path.IBPath` which will setup the AH using the
    forward path parameters."""
    if typecheck(attr, ah_attr):
        cattr.is_global = attr.is_global
        if cattr.is_global:
            if not typecheck(attr.grh, global_route):
                raise TypeError("attr.grh must be a global_route")
            if not typecheck(attr.grh.dgid, IBA.GID):
                raise TypeError("attr.grh.dgid must be an IBA.GID")
            for 0 <= i < 16:
                cattr.grh.dgid.raw[i] = ord(attr.DGID[i]);
            cattr.grh.flow_label = attr.grh.flow_label
            cattr.grh.sgid_index = attr.grh.sgid_index
            cattr.grh.hop_limit = attr.grh.hop_limit
            cattr.grh.traffic_class = attr.grh.traffic_class

        cattr.dlid = attr.dlid
        cattr.sl = attr.sl
        cattr.src_path_bits = attr.src_path_bits
        cattr.static_rate = attr.static_rate
        cattr.port_num = attr.port_num
    elif typecheck(attr, rdma.path.IBPath):
        cattr.is_global = attr.has_grh
        if attr.DGID is not None:
            for 0 <= i < 16:
                cattr.grh.dgid.raw[i] = ord(attr.DGID[i]);
        if cattr.is_global:
            cattr.grh.sgid_index = attr.SGID_index;

        cattr.grh.flow_label = attr.flow_label
        cattr.grh.hop_limit = attr.hop_limit
        cattr.grh.traffic_class = attr.traffic_class

        cattr.dlid = attr.DLID
        cattr.sl = attr.SL
        cattr.src_path_bits = attr.SLID_bits
        cattr.static_rate = attr.rate
        cattr.port_num = attr.end_port.port_id
    else:
        raise TypeError("attr must be an rdma.ibverbs.ah_attr or rdma.path.IBPath.")

cdef class QP:
    """Queue pair, this is a context manager."""
    cdef object __weakref__
    cdef PD _pd
    cdef CQ _scq
    cdef CQ _rcq
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
    property max_send_wr:
        def __get__(self):
            return self._cap.max_send_wr;
    property max_send_sge:
        def __get__(self):
            return self._cap.max_send_sge;
    property max_recv_wr:
        def __get__(self):
            return self._cap.max_recv_wr;
    property max_recv_sge:
        def __get__(self):
            return self._cap.max_recv_sge;

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

        self._scq = init.send_cq
        self._rcq = init.recv_cq

        cinit.send_cq = self._scq._cq
        cinit.recv_cq = self._rcq._cq
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
        self._close();

    def __enter__(self):
        return self;

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs QP handle."""
        self._close();

    cdef _close(self):
        cdef int rc
        if self._qp != NULL:
            rc = c.ibv_destroy_qp(self._qp)
            if rc != 0:
                raise rdma.SysError(errno,"ibv_destroy_qp",
                                    "Failed to destroy queue pair")
            self._qp = NULL;
            self._pd = None;
            self._scq = None;
            self._rcq = None;

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

    cdef post_check(self, arg, wrtype, max_sge, int *numsge):
        cdef list wrlist
        cdef int i, n
        cdef int sgec

        if isinstance(arg, wrtype):
            wrlist = [arg]
        elif (isinstance(arg, list) or isinstance(arg, tuple)) and len(arg) > 0:
            wrlist = arg
        else:
            raise TypeError("Expecting a work request or a list/tuple of work requests")

        sgec = 0
        for wr in wrlist:
            if not typecheck(wr, wrtype):
                raise TypeError("Work request must be of type %s" % wrtype.__name__)
            if typecheck(wr.sg_list, sge):
                sgec = sgec + 1;
            elif isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
                sglist = wr.sg_list
                n = len(sglist)
                sgec = sgec + n;
                if n > max_sge:
                    raise TypeError("Too many scatter/gather entries in work request")
                for 0 <= i < n:
                    if not typecheck(sglist[i], sge):
                        raise TypeError("sg_list entries must be of type ibv_sge")
            elif wr.sg_list is not None:
                raise TypeError("sg_list entries must be of type ibv_sge or a list")
        numsge[0] = sgec
        return wrlist

    cdef _post_send(self, arg):
        cdef list sglist, wrlist
        cdef unsigned char *mem
        cdef c.ibv_send_wr dummy_wr, *cwr, *cbad_wr
        cdef c.ibv_sge dummy_sge, *csge
        cdef c.ibv_ah dummy_ah, *cah
        cdef int i, j, n, rc,
        cdef int wr_id
        cdef AH ah
        cdef int num_sge

        wrlist = self.post_check(arg, send_wr, self._cap.max_send_sge, &num_sge)

        n = len(wrlist)
        mem = <unsigned char *>calloc(1,sizeof(dummy_wr)*n + sizeof(dummy_sge)*num_sge);
        if mem == NULL:
            raise MemoryError()
        cwr = <c.ibv_send_wr *>(mem);
        csge = <c.ibv_sge *>(cwr + n);
        for 0 <= i < n:
            wr = wrlist[i]
            wr_id = wr.wr_id;
            cwr.wr_id = <uintptr_t>wr_id
            if i == n - 1:
                cwr.next = NULL
            else:
                cwr.next = cwr + 1

            cwr.sg_list = csge
            if typecheck(wr.sg_list, list) or typecheck(wr.sg_list, tuple):
                cwr.num_sge = len(sglist)
                for 0 <= j < cwr.num_sge:
                    sge = wr.sg_list[j]
                    csge.addr = sge.addr
                    csge.length = sge.length
                    csge.lkey = sge.lkey
                    csge += 1
            elif wr.sg_list is not None:
                cwr.num_sge = 1
                csge.addr = wr.sg_list.addr
                csge.length = wr.sg_list.length
                csge.lkey = wr.sg_list.lkey
                csge += 1

            cwr.opcode = wr.opcode
            if (cwr.opcode == c.IBV_WR_RDMA_WRITE or
                cwr.opcode == c.IBV_WR_RDMA_WRITE_WITH_IMM or
                cwr.opcode == c.IBV_WR_RDMA_READ):
                cwr.wr.rdma.remote_addr = wr.remote_addr
                cwr.wr.rdma.rkey = wr.rkey
            elif (cwr.opcode == c.IBV_WR_ATOMIC_FETCH_AND_ADD or
                  cwr.opcode == c.IBV_WR_ATOMIC_CMP_AND_SWP):
                cwr.wr.atomic.remote_addr = wr.remote_addr
                cwr.wr.atomic.compare_add = wr.compare_add
                cwr.wr.atomic.swap = wr.swap
                cwr.wr.atomic.rkey = wr.rkey
            elif self._qp_type == c.IBV_QPT_UD:
                if not typecheck(wr.ah,AH):
                    free(mem)
                    raise TypeError("AH must be a AH")
                ah = wr.ah;
                cwr.wr.ud.ah = ah._ah
                cwr.wr.ud.remote_qpn = wr.remote_qpn
                cwr.wr.ud.remote_qkey = wr.remote_qkey

            cwr.send_flags = wr.send_flags
            cwr.imm_data = wr.imm_data

        rc = c.ibv_post_send(self._qp, <c.ibv_send_wr *>mem, &cbad_wr)
        if rc != 0:
            cwr = <c.ibv_send_wr *>(mem);
            for 0 <= i < n:
                if cwr == cbad_wr:
                    break;
            free(mem)
            raise WRError(rc,"ibv_post_recv","Failed to post work request",n);
        free(mem)

    cdef _post_recv(self, arg):
        cdef list wrlist
        cdef unsigned char *mem
        cdef c.ibv_recv_wr dummy_wr, *cwr, *cbad_wr
        cdef c.ibv_sge dummy_sge, *csge
        cdef int i, j, n, rc
        cdef int wr_id
        cdef int num_sge

        wrlist = self.post_check(arg, recv_wr, self._cap.max_recv_sge, &num_sge)

        n = len(wrlist)
        mem = <unsigned char *>calloc(1,sizeof(dummy_wr)*n + sizeof(dummy_sge)*num_sge);
        if mem == NULL:
            raise MemoryError()
        cwr = <c.ibv_recv_wr *>(mem);
        csge = <c.ibv_sge *>(cwr + n);
        for 0 <= i < n:
            wr = wrlist[i]
            wr_id = wr.wr_id;
            cwr.wr_id = <uintptr_t>wr_id
            if i == n - 1:
                cwr.next = NULL
            else:
                cwr.next = cwr + 1

            cwr.sg_list = csge
            if typecheck(wr.sg_list, list) or typecheck(wr.sg_list, tuple):
                cwr.num_sge = len(sglist)
                for 0 <= j < cwr.num_sge:
                    sge = wr.sg_list[j]
                    csge.addr = sge.addr
                    csge.length = sge.length
                    csge.lkey = sge.lkey
                    csge += 1
            elif wr.sg_list is not None:
                cwr.num_sge = 1
                sge = wr.sg_list;
                csge.addr = sge.addr
                csge.length = sge.length
                csge.lkey = sge.lkey
                csge += 1

        rc = c.ibv_post_recv(self._qp, <c.ibv_recv_wr *>mem, &cbad_wr)
        if rc != 0:
            cwr = <c.ibv_recv_wr *>(mem);
            for 0 <= i < n:
                if cwr == cbad_wr:
                    break;
            free(mem)
            raise WRError(rc,"ibv_post_recv","Failed to post work request",n);

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
        """When modifying a QP the value *attr.ah_attr* may be a
        :class:`rdma.ibverbs.ah_attr` or :class:`rdma.path.IBPath`."""
        self._modify(attr, mask)

    def modify_to_init(self,path,qp_access_flags=None):
        """Modify the QP to the INIT state."""
        if self._qp_type == c.IBV_QPT_UD:
            attr = qp_attr(qp_state=c.IBV_QPS_INIT,
                           pkey_index=path.pkey_index,
                           port_num=path.end_port.port_id,
                           qkey=path.qkey);
        else:
            if qp_access_flags is None:
                raise TypeError("qp_access_flags must be an integer");
            attr = qp_attr(qp_state=c.IBV_QPS_INIT,
                           pkey_index=path.pkey_index,
                           port_num=path.end_port.port_id,
                           qp_access_flags=qp_access_flags);
        self._modify(attr,attr.MASK)

    def modify_to_rtr(self,path):
        """Modify the QP to the RTR state."""
        if self._qp_type == c.IBV_QPT_UD:
            attr = qp_attr(qp_state=c.IBV_QPS_RTR);
        else:
            attr = qp_attr(qp_state=c.IBV_QPS_RTR,
                           path_mtu=path.MTU,
                           dest_qp_num=path.dqpn,
                           rq_psn=path.dqpsn,
                           max_dest_rd_atomic=path.drdatomic,
                           # Hmm, where does this come from?
                           min_rnr_timer=path.min_rnr_timer,
                           ah_attr=path)
        self._modify(attr,attr.MASK)

    def modify_to_rts(self,path):
        """Modify the QP to the RTS state."""
        if self._qp_type == c.IBV_QPT_UD:
            attr = qp_attr(qp_state=c.IBV_QPS_RTS,
                           sq_psn=path.sqpsn);
        else:
            attr = qp_attr(qp_state=c.IBV_QPS_RTS,
                           timeout=rdma.IBA.to_timer(path.qp_timeout),
                           retry_cnt=path.retries,
                           # FIXME
                           rnr_retry=7,
                           sq_psn=path.sqpsn,
                           max_rd_atomic=path.srdatomic);
        self._modify(attr,attr.MASK)

    def post_send(self, wrlist):
        self._post_send(wrlist)

    def post_recv(self, wrlist):
        self._post_recv(wrlist)
