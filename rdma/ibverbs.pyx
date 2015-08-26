# -*- Python -*-
# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
import select
import collections
import errno as mod_errno
import rdma.tools as tools;
import struct;
import weakref;
import sys
import rdma.devices
import rdma.IBA as IBA;
import rdma.path;

cimport libibverbs as c

cdef extern from 'types.h':
    ctypedef void **const_void_ptr_ptr

cdef extern from 'errno.h':
    int errno

cdef extern from 'string.h':
    void *memset(void *s, int c, size_t n)

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

include 'libibverbs_enums.pxi'
include 'libibverbs.pxi'

debug = False

cdef class Context
cdef class PD
cdef class AH
cdef class CompChannel
cdef class CQ
cdef class MR
cdef class QP
cdef class SRQ

cdef CQ get_cq(c.ibv_cq *v):
    """Go from a C struct ibv_cq to a CQ object."""
    if v == NULL:
        return None
    return <CQ>v.cq_context
cdef SRQ get_srq(c.ibv_srq *v):
    """Go from a C struct ibv_srq to a SRQ object."""
    if v == NULL:
        return None
    return <SRQ>v.srq_context
cdef QP get_qp(c.ibv_qp *v):
    """Go from a C struct ibv_qp to a QP object."""
    if v == NULL:
        return None
    return <QP>v.qp_context

class _my_weakset(weakref.WeakKeyDictionary):
    def add(self,v):
        self[v] = None;
    def pop(self):
        return weakref.WeakKeyDictionary.popitem(self)[0];
WeakSet = weakref.__dict__.get("WeakSet",_my_weakset)

class WRError(rdma.SysError):
    """Raised when an error occurs posting work requests. :attr:`bad_index`
    is the index into the work request list what failed to post."""
    def __init__(self,int errno,char *func,char *msg,int bad_index):
        rdma.SysError.__init__(self,errno,func,msg);
        self.bad_index = bad_index;

def wc_status_str(int status):
    """Convert a :attr:`rdma.ibverbs.wc.status` value into a string."""
    return c.ibv_wc_status_str(status);

cdef to_ah_attr(c.ibv_ah_attr *cattr, object attr):
    """Fill in an ibv_ah_attr from *attr*. *attr* can be a
    :class:`rdma.ibverbs.ah_attr` which is copied directly (discouraged) or it
    can be a :class:`rdma.path.IBPath` which will setup the AH using the
    forward path parameters."""
    if isinstance(attr, ah_attr):
        cattr.is_global = attr.is_global
        if cattr.is_global:
            if not isinstance(attr.grh, global_route):
                raise TypeError("attr.grh must be a global_route")
            if not isinstance(attr.grh.dgid, IBA.GID):
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
    elif isinstance(attr, rdma.path.IBPath):
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

cdef object from_ah_attr(c.ibv_ah_attr *cattr):
    """Return a :class:`rdma.ibverbs.ah_attr` filled in from *cattr."""
    return ah_attr(grh=global_route(dgid=IBA.GID(PyBytes_FromStringAndSize(<char *>cattr.grh.dgid.raw,16),True),
                                    flow_label=cattr.grh.flow_label,
                                    sgid_index=cattr.grh.sgid_index,
                                    hop_limit=cattr.grh.hop_limit,
                                    traffic_class=cattr.grh.traffic_class),
                   dlid=cattr.dlid,
                   sl=cattr.sl,
                   src_path_bits=cattr.src_path_bits,
                   static_rate=cattr.static_rate,
                   is_global=cattr.is_global,
                   port_num=cattr.port_num);

cdef _post_check(object arg, object wrtype, int max_sge, int *numsge):
    """Validate wrs for posting. *arg* can be a single wr or a list. *wrtype*
    is the expected type of the wr, *max_sge* is the maximum number of SGEs
    that can be in each WR, and *numsge* is the total number of SGEs.
    Returns *arg* or *arg* stuffed into a list."""
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
        if not isinstance(wr, wrtype):
            raise TypeError("Work request must be of type %s" % wrtype.__name__)
        if isinstance(wr.sg_list, sge):
            sgec = sgec + 1;
        elif isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
            sglist = wr.sg_list
            n = len(sglist)
            sgec = sgec + n;
            if n > max_sge:
                raise ValueError("Too many scatter/gather entries in work request")
            for 0 <= i < n:
                if not isinstance(sglist[i], sge):
                    raise TypeError("sg_list entries must be of type ibv_sge")
        elif wr.sg_list is not None:
            raise TypeError("sg_list entries must be of type ibv_sge or a list")
    numsge[0] = sgec
    return wrlist

class WCError(rdma.RDMAError):
    """Raised when a WC is completed with error. Note: Not all adaptors
    support returning the `opcode` and `qp_num` in an error WC. For those that
    do the values are decoded."""
    is_rq = None
    cq = None
    qp = None
    srq = None

    def __init__(self,wc,cq,char * msg="Error work completion",
                 obj=None,is_rq=None):
        """*wc* is the error wc, *msg* is an additional descriptive message,
        *cq* is the CQ the error WC was received on and *obj* is a
        :class:`rdma.ibverbs.SRQ` or :class:`rdma.ibverbs.QP` if one is
        known. *is_rq* is `True` if the WC is known to apply to the receive of
        the QP, and `False` if the WC is known the apply to the send queue of
        the QP. `None` if unknown"""
        cdef QP qp

        if obj is not None:
            if isinstance(obj,QP):
                qp = obj
            else:
                qp = obj.pd.from_qp_num(wc.qp_num)
        elif cq is not None:
            qp = cq.ctx.from_qp_num(wc.qp_num)
        else:
            qp = None
            sqp = None

        info = ["op=%s"%(IBA.const_str("IBV_WC_",wc.opcode,True,
                                       sys.modules["rdma.ibverbs"])),
                "vend=0x%x"%(wc.vendor_err)];

        if cq is not None:
            self.cq = cq;
            info.append(str(cq));
        if qp is not None:
            self.qp = qp;
            info.append(str(qp));
            self.srq = qp._srq
        if is_rq is not None:
            self.is_rq = is_rq;
            if is_rq:
                info.append("RQ");
            else:
                info.append("SQ");
        if obj is not None and isinstance(obj,SRQ):
            self.srq = obj;
        if self.srq is not None:
            info.append(str(self.srq));

        s = "%s - %d %s (%s)"%(msg,wc.status,c.ibv_wc_status_str(wc.status),
                               " ".join(info));
        rdma.RDMAError.__init__(self,s);
        self.wc = wc;

class AsyncError(rdma.RDMAError):
    """Raised when an asynchronous error event is received."""
    def __init__(self,event,char *msg="Asynchronous error event"):
        s = "%s - %s for %r"%(
            msg,IBA.const_str("IBV_EVENT_",event[0],True,
                             sys.modules["rdma.ibverbs"]),
            event[1]);
        rdma.RDMAError.__init__(self,s);
        self.event = event

def WCPath(end_port,wc,buf=None,int off=0,**kwargs):
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

        if isinstance(parent,rdma.devices.RDMADevice):
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

        if self.end_port is not None:
            # Fetch the subnet_timeout from verbs
            self.query_port()

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

    def query_port(self,port_id=None):
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

        # Update the end_port's subnet timeout..
        self.node.end_ports[port_id]._cached_subnet_timeout = cattr.subnet_timeout;

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

    def from_qp_num(self,int num):
        """Return a :class:`rdma.ibverbs.QP` for the qp number *num* or `None`
        if one was not found."""
        cdef PD pd
        for I in self._children_pd:
            pd = I
            ret = pd.from_qp_num(num)
            if ret is not None:
                return ret;
        return None;

    def pd(self):
        """Create a new :class:`rdma.ibverbs.PD` for this context."""
        ret = PD(self);
        self._children_pd.add(ret);
        return ret;

    def cq(self,int nelems=100,cc=None,int vec=0):
        """Create a new :class:`rdma.ibverbs.CQ` for this context."""
        ret = CQ(self,nelems,cc,vec);
        self._children_cq.add(ret);
        return ret;

    def comp_channel(self):
        """Create a new :class:`rdma.ibverbs.CompChannel` for this context."""
        ret = CompChannel(self);
        self._children_cc.add(ret);
        return ret;

    def get_async_event(self):
        """Get a single async event for this context. The return result is a
        :class:`namedtuple` of `(event_type,obj` where *obj* will be the
        :class:`rdma.ibverbs.CQ`, :class:`rdma.ibverbs.QP`,
        :class:`rdma.ibverbs.SRQ`, :class:`rdma.devices.EndPort` or
        :class:`rdma.devices.RDMADevice` associated with the event."""
        cdef c.ibv_async_event event
        cdef int rc

        rc = c.ibv_get_async_event(self._ctx,&event)
        if rc != 0:
            if rc == mod_errno.EAGAIN:
                return None;
            raise rdma.SysError(rc,"ibv_get_async_event",
                                "Failed to get an asynchronous event");

        if event.event_type == c.IBV_EVENT_DEVICE_FATAL:
            ret = async_event(event.event_type,self.node);
        elif (event.event_type == c.IBV_EVENT_PORT_ACTIVE or
              event.event_type == c.IBV_EVENT_PORT_ERR or
              event.event_type == c.IBV_EVENT_LID_CHANGE or
              event.event_type == c.IBV_EVENT_PKEY_CHANGE or
              event.event_type == c.IBV_EVENT_SM_CHANGE or
              event.event_type == c.IBV_EVENT_CLIENT_REREGISTER):
            ret = async_event(event.event_type,
                              self.node.end_ports[event.element.port_num]);
        elif (event.event_type == c.IBV_EVENT_SRQ_ERR or
              event.event_type == c.IBV_EVENT_SRQ_LIMIT_REACHED):
            ret = async_event(event.event_type,
                              get_srq(event.element.srq));
        elif event.event_type == c.IBV_EVENT_CQ_ERR:
             ret = async_event(event.event_type,
                               get_cq(event.element.cq));
        elif (event.event_type == c.IBV_EVENT_QP_FATAL or
              event.event_type == c.IBV_EVENT_QP_REQ_ERR or
              event.event_type == c.IBV_EVENT_QP_ACCESS_ERR or
              event.event_type == c.IBV_EVENT_COMM_EST or
              event.event_type == c.IBV_EVENT_SQ_DRAINED or
              event.event_type == c.IBV_EVENT_PATH_MIG or
              event.event_type == c.IBV_EVENT_PATH_MIG_ERR or
              event.event_type == c.IBV_EVENT_QP_LAST_WQE_REACHED):
            ret = async_event(event.event_type,
                              get_qp(event.element.qp));
        else:
            # Hmm. We don't know what member of the enum to decode, so we can't
            # really do anything.
            ret = async_event(event.event_type,None);
        c.ibv_ack_async_event(&event)
        return ret

    def handle_async_event(self,event):
        """This provides a generic handler for async events. Depending
        on the event it will:
        - Raise a :exc:`rdma.ibverbs.AsyncError` exception
        - Reload cached information in the end port"""
        cdef int ty
        ty = event[0]

        if ty == c.IBV_EVENT_DEVICE_FATAL:
            raise AsyncError(event);
        if ty == c.IBV_EVENT_LID_CHANGE:
            event[1].lid_change();
        if ty == c.IBV_EVENT_PKEY_CHANGE:
            event[1].pkey_change();
        if ty == c.IBV_EVENT_SM_CHANGE:
            self.query_port(event[1].port_id);
            event[1].sm_change();
        if ty == c.IBV_EVENT_SRQ_ERR:
            raise AsyncError(event);
        if ty == c.IBV_EVENT_CQ_ERR:
            raise AsyncError(event);
        if ty == c.IBV_EVENT_QP_FATAL:
            raise AsyncError(event);
        if ty == c.IBV_EVENT_QP_REQ_ERR:
            raise AsyncError(event);
        if ty == c.IBV_EVENT_QP_ACCESS_ERR:
            raise AsyncError(event);
        if ty == c.IBV_EVENT_PATH_MIG_ERR:
            raise AsyncError(event);

    def register_poll(self,poll):
        """Add the async event FD associated with this object to
        :class:`select.poll` object *poll*."""
        poll.register(self._ctx.async_fd,select.POLLIN);

    def check_poll(self,pevent):
        """Return `True` if *pevent* indicates that :meth:`get_async_event`
        will return data."""
        if pevent[0] != self._ctx.async_fd:
            return False;
        if pevent[1] & select.POLLIN == 0:
            return False;
        return True;

    def __str__(self):
        return "context:%s"%(self.node)
    def __repr__(self):
        return "Context('%s',fd=%u)"%(self.node,self._ctx.cmd_fd)

cdef class PD:
    """Protection domain handle, this is a context manager."""
    cdef object __weakref__
    cdef Context _context
    cdef c.ibv_pd *_pd
    cdef object _children_qp
    cdef object _children_srq
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
        self._children_srq = WeakSet();
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
        while self._children_qp:
            self._children_qp.pop().close();
        while self._children_ah:
            self._children_ah.pop().close();
        while self._children_srq:
            self._children_srq.pop().close();
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

    def from_qp_num(self,int num):
        """Return a :class:`rdma.ibverbs.QP` for the qp number *num* or `None`
        if one was not found."""
        cdef QP qp
        for I in self._children_qp:
            qp = I;
            if qp._qp.qp_num == num:
                return qp;
        return None;

    def qp_raw(self,init):
        """Create a new :class:`rdma.ibverbs.QP` for this protection
        domain. *init* is a :class:`rdma.ibverbs.qp_init_attr`."""
        ret = QP(self,init);
        self._children_qp.add(ret);
        return ret;

    def qp(self,
           int qp_type,
           int max_send_wr,
           send_cq,
           int max_recv_wr,
           recv_cq,
           srq=None,
           int sq_sig_all=1,
           int max_send_sge=1,
           int max_recv_sge=1,
           int max_inline_data=0):
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

    def srq(self,int max_wr=100,int max_sge=1):
        """Create a new :class:`rdma.ibverbs.SRQ` for this protection
        domain. *init* is a :class:`rdma.ibverbs.srq_init_attr`."""
        ret = SRQ(self,max_wr=max_wr,max_sge=max_sge);
        self._children_srq.add(ret);
        return ret;

    def mr(self,buf,int access=0):
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

    def __str__(self):
        return "pd:%X:%s"%(self._pd.handle,self.ctx.node);
    def __repr__(self):
        return "PD(%r,0x%x)"%(self._context,self._pd.handle);

cdef class AH:
    """Address handle, this is a context manager."""
    cdef object __weakref__
    cdef c.ibv_ah *_ah

    def __cinit__(self, PD pd not None, attr):
        cdef c.ibv_ah_attr cattr

        memset(&cattr,0,sizeof(cattr));
        to_ah_attr(&cattr, attr)
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

    def __str__(self):
        return "ah:%X"%(self._ah.handle)
    def __repr__(self):
        return "AH(0x%x)"%(self._ah.handle);

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

    def check_poll(self,pevent):
        """Returns a :class:`rdma.ibverbs.CQ` that got at least one completion
        event, or `None`. This updates the comp channel and keeps track of
        received events, and appropriately calls ibv_ack_cq_events
        internally. After this call the CQ must be re-armed via
        :meth:`rdma.ibverbs.CQ.req_notify`"""
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
        cq = <CQ>p_cq;

        cq.comp_events = cq.comp_events + 1;
        if cq.comp_events >= (1<<30):
            c.ibv_ack_cq_events(_cq,cq.comp_events);
            cq.comp_events = 0;
        return cq;

    def __str__(self):
        return "comp_channel:%u:%s"%(self._chan.fd,self.ctx.node);
    def __repr__(self):
        return "CompChannel(%r,%u)"%(self._context,self._chan.fd);

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

    property comp_chan:
        def __get__(self):
            return self._chan;

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

    def req_notify(self,int solicited_only=False):
        """Request event notification for CQEs added to the CQ."""
        cdef int rc
        rc = c.ibv_req_notify_cq(self._cq,solicited_only);
        if rc != 0:
            raise rdma.SysError(rc,"ibv_req_notify_cq",
                                "Failed to request notification");

    def resize(self,int cqes):
        """Resize the CQ to have at least *cqes* entries."""
        cdef int rc
        rc = c.ibv_resize_cq(self._cq,cqes);
        if rc != 0:
            raise rdma.SysError(rc,"ibv_resize_cq",
                                "Failed to resize the CQ");

    def poll(self,int limit=-1):
        """Perform the poll_cq operation, return a list of work requests."""
        cdef c.ibv_wc lwc
        cdef int n
        cdef list L
        L = []
        while limit != 0:
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
                if limit > 0:
                    limit = limit - 1;
        return L

    def __str__(self):
        return "cq:%X:%s"%(self._cq.handle,self.ctx.node);
    def __repr__(self):
        return "CQ(%r,0x%x)"%(self._context,self._cq.handle);

cdef class SRQ:
    """Shared Receive queue, this is a context manager."""
    cdef object __weakref__
    cdef PD _pd
    cdef c.ibv_srq *_srq
    cdef int _max_sge

    property pd:
        def __get__(self):
            return self._pd;

    property ctx:
        def __get__(self):
            return self._pd._context;

    def __cinit__(self,PD pd not None,int max_wr,int max_sge):
        cdef c.ibv_srq_init_attr attr

        memset(&attr,0,sizeof(attr));
        self._pd = pd
        attr.srq_context = <void *>self;
        attr.attr.max_wr = max_wr;
        attr.attr.max_sge = max_sge;
        self._max_sge = max_sge
        self._srq = c.ibv_create_srq(pd._pd,&attr);
        if self._srq == NULL:
            raise rdma.SysError(errno,"ibv_create_srq",
                                "Failed to create SRQ")

    def __dealloc__(self):
        self._close();

    def __enter__(self):
        return self

    def __exit__(self,*exc_info):
        self._close();

    def close(self):
        """Free the verbs SRQ handle."""
        self._close();

    cdef _close(self):
        cdef int rc
        if self._srq != NULL:
            rc = c.ibv_destroy_srq(self._srq)
            if rc != 0:
                raise rdma.SysError(errno,"ibv_destroy_srq",
                                    "Failed to destroy SRQ")
            self._srq = NULL

    def modify(self,srq_limit=None,max_wr=None):
        """Modify the *srq_limit* and *max_wr* values of SRQ. If the
        argument is `None` it is not changed."""
        cdef c.ibv_srq_attr cattr
        cdef int cmask

        memset(&cattr,0,sizeof(cattr))
        cmask = 0
        if max_wr is not None:
            cattr.max_wr = max_wr
            cmask |= c.IBV_SRQ_MAX_WR
        if srq_limit is not None:
            cattr.srq_limit = srq_limit
            cmask |= c.IBV_SRQ_LIMIT

        rc = c.ibv_modify_srq(self._srq, &cattr, cmask)
        if rc != 0:
            raise rdma.SysError(errno,"ibv_modify_srq",
                                "Failed to modify a SRQ")

    def query(self):
        """Return a :class:`rdma.ibverbs.srq_attr`."""
        cdef c.ibv_srq_attr cattr

        rc = c.ibv_query_srq(self._srq, &cattr)
        if rc != 0:
            raise rdma.SysError(errno,"ibv_query_srq",
                                "Failed to query a SRQ")

        self._max_sge = cattr.max_sge;
        return srq_attr(max_wr=cattr.max_wr,
                        max_sge=cattr.max_sge,
                        srq_limit=cattr.srq_limit);

    def post_recv(self, arg):
        """*wrlist* may be a single :class:`rdma.ibverbs.recv_wr` or
        a list of them."""
        cdef list wrlist
        cdef unsigned char *mem
        cdef c.ibv_recv_wr dummy_wr
        cdef c.ibv_recv_wr *cwr
        cdef c.ibv_recv_wr *cbad_wr
        cdef c.ibv_sge dummy_sge
        cdef c.ibv_sge *csge
        cdef int i, j, n, rc
        cdef int wr_id
        cdef int num_sge

        # NOTE: A copy of this is in QP.post_recv
        wrlist = _post_check(arg, recv_wr, self._max_sge, &num_sge)

        n = len(wrlist)
        mem = <unsigned char *>calloc(1,sizeof(dummy_wr)*n + sizeof(dummy_sge)*num_sge);
        if mem == NULL:
            raise MemoryError()
        try:
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
                if isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
                    cwr.num_sge = len(wr.sg_list)
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
                cwr = cwr + 1;

            cwr = <c.ibv_recv_wr *>(mem);
            rc = c.ibv_post_srq_recv(self._srq, <c.ibv_recv_wr *>mem, &cbad_wr)
            if rc != 0:
                cwr = <c.ibv_recv_wr *>(mem);
                for 0 <= i < n:
                    if cwr+i == cbad_wr:
                        break;
                raise WRError(rc,"ibv_post_srq_recv","Failed to post work request",n);
        finally:
            free(mem)

    def __str__(self):
        return "srq:%X:%s"%(self._srq.handle,self._pd);
    def __repr__(self):
        return "SRQ(%r,0x%x)"%(self._pd,self._srq.handle);

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

    def __cinit__(self, PD pd not None, buf, int access=0):
        cdef void *addr
        cdef Py_ssize_t length
        cdef int rc

        if access & (c.IBV_ACCESS_LOCAL_WRITE | c.IBV_ACCESS_REMOTE_WRITE) != 0:
            rc = PyObject_AsWriteBuffer(buf, &addr, &length)
            if rc != 0:
                raise TypeError("Expected mutable buffer")
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

    def sge(self,int length=-1,int off=0):
        """Create a :class:`rdma.ibv.sge` referring to *length* bytes of this MR
        starting at *off*. If *length* is -1 (default) then the entire MR from *off*
        to the end is used."""
        cdef int _length
        cdef int _off

        _length = length
        _off = off
        if _off < 0:
            raise ValueError("off %r cannot be negative"%off);
        if _length == -1:
            _length = self._mr.length - _off;
        if _length + _off > self._mr.length:
            raise ValueError("Length is too long %u > %u"%(_length + _off,
                                                           self._mr.length));
        return sge(addr=<uintptr_t>(self._mr.addr + _off),
                   lkey=self._mr.lkey,
                   length=_length);

    def __str__(self):
        return "mr:%X:%s"%(self._mr.handle,self._pd);
    def __repr__(self):
        return "MR(%r,0x%x,0x%x,%u,lkey=0x%x,rkey=0x%x)"%(
            self._pd,self._mr.handle,self.addr,self.length,
            self.lkey,self.rkey);

cdef class QP:
    """Queue pair, this is a context manager."""
    cdef object __weakref__
    cdef PD _pd
    cdef CQ _scq
    cdef CQ _rcq
    cdef SRQ _srq
    cdef c.ibv_qp *_qp
    cdef c.ibv_qp_cap _cap
    cdef int _qp_type
    cdef list _groups

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

        memset(&cinit,0,sizeof(cinit));

        if not isinstance(init.send_cq, CQ):
            raise TypeError("send_cq must be a cq")
        if not isinstance(init.recv_cq, CQ):
            raise TypeError("recv_cq must be a cq")
        if not isinstance(init.cap, qp_cap):
            raise TypeError("cap must be a qp_cap")
        if init.srq is not None and not isinstance(init.srq, SRQ):
            raise TypeError("srq must be a SRQ")

        self._scq = init.send_cq
        self._rcq = init.recv_cq

        cinit.send_cq = self._scq._cq
        cinit.recv_cq = self._rcq._cq
        if init.srq is not None:
            self._srq = init.srq
            cinit.srq = self._srq._srq
        cinit.cap.max_send_wr = init.cap.max_send_wr
        cinit.cap.max_recv_wr = init.cap.max_recv_wr
        cinit.cap.max_send_sge = init.cap.max_send_sge
        cinit.cap.max_recv_sge = init.cap.max_recv_sge
        cinit.cap.max_inline_data = init.cap.max_inline_data
        cinit.qp_type = init.qp_type
        cinit.sq_sig_all = init.sq_sig_all
        cinit.qp_context = <void *>self

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
            while self._groups:
                g = self._groups[0];
                self.detach_mcast(rdma.path.IBPath(None,DGID=g[0],DLID=g[1]));
            rc = c.ibv_destroy_qp(self._qp)
            if rc != 0:
                raise rdma.SysError(errno,"ibv_destroy_qp",
                                    "Failed to destroy queue pair")
            self._qp = NULL;
            self._pd = None;
            self._scq = None;
            self._rcq = None;
            self._srq = None;

    def modify(self,attr,int mask):
        """When modifying a QP the value *attr.ah_attr* may be a
        :class:`rdma.ibverbs.ah_attr` or :class:`rdma.path.IBPath`."""
        cdef c.ibv_qp_attr cattr
        cdef int rc
        cdef int cmask

        memset(&cattr,0,sizeof(cattr));

        cmask = mask
        if debug:
            print 'modify qp, attr = %s mask = 0x%x' % (str(attr), cmask)
        if not isinstance(mask, int):
            raise TypeError("mask must be an int")
        if not isinstance(attr, qp_attr):
            raise TypeError("attr must be a qp_attr")
        cattr.qp_state = attr.qp_state
        cattr.cur_qp_state = attr.cur_qp_state
        cattr.en_sqd_async_notify = attr.en_sqd_async_notify
        cattr.qp_access_flags = attr.qp_access_flags
        cattr.pkey_index = attr.pkey_index
        cattr.port_num = attr.port_num
        cattr.qkey = attr.qkey

        if cmask & c.IBV_QP_AV:
            to_ah_attr(&cattr.ah_attr, attr.ah_attr)

        cattr.path_mtu = attr.path_mtu
        cattr.timeout = attr.timeout
        cattr.retry_cnt = attr.retry_cnt
        cattr.rnr_retry = attr.rnr_retry
        cattr.rq_psn = attr.rq_psn
        cattr.max_rd_atomic = attr.max_rd_atomic

        if cmask & c.IBV_QP_ALT_PATH:
            to_ah_attr(&cattr.alt_ah_attr, attr.alt_ah_attr)
            cattr.alt_pkey_index = attr.alt_pkey_index
            cattr.alt_port_num = attr.alt_port_num
            cattr.alt_timeout = attr.alt_timeout

        cattr.min_rnr_timer = attr.min_rnr_timer
        cattr.sq_psn = attr.sq_psn
        cattr.max_dest_rd_atomic = attr.max_dest_rd_atomic
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

    def post_send(self, arg):
        """*wrlist* may be a single :class:`rdma.ibverbs.send_wr` or
        a list of them."""
        cdef list sglist, wrlist
        cdef unsigned char *mem
        cdef c.ibv_send_wr dummy_wr
        cdef c.ibv_send_wr *cwr
        cdef c.ibv_send_wr *cbad_wr
        cdef c.ibv_sge dummy_sge
        cdef c.ibv_sge *csge
        cdef c.ibv_ah dummy_ah
        cdef c.ibv_ah *cah
        cdef int i, j, n, rc,
        cdef int wr_id
        cdef AH ah
        cdef int num_sge

        wrlist = _post_check(arg, send_wr, self._cap.max_send_sge, &num_sge)

        n = len(wrlist)
        mem = <unsigned char *>calloc(1,sizeof(dummy_wr)*n + sizeof(dummy_sge)*num_sge);
        if mem == NULL:
            raise MemoryError()
        try:
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
                if isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
                    cwr.num_sge = len(wr.sg_list)
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
                    if not isinstance(wr.ah,AH):
                        raise TypeError("AH must be a AH")
                    ah = wr.ah;
                    cwr.wr.ud.ah = ah._ah
                    cwr.wr.ud.remote_qpn = wr.remote_qpn
                    cwr.wr.ud.remote_qkey = wr.remote_qkey

                cwr.send_flags = wr.send_flags
                cwr.imm_data = wr.imm_data
                cwr = cwr + 1;

            rc = c.ibv_post_send(self._qp, <c.ibv_send_wr *>mem, &cbad_wr)
            if rc != 0:
                cwr = <c.ibv_send_wr *>(mem);
                for 0 <= i < n:
                    if cwr+i == cbad_wr:
                        break;
                raise WRError(rc,"ibv_post_send","Failed to post work request",n);
        finally:
            free(mem)

    def post_recv(self, arg):
        """*wrlist* may be a single :class:`rdma.ibverbs.recv_wr` or
        a list of them."""
        cdef list wrlist
        cdef unsigned char *mem
        cdef c.ibv_recv_wr dummy_wr
        cdef c.ibv_recv_wr *cwr
        cdef c.ibv_recv_wr *cbad_wr
        cdef c.ibv_sge dummy_sge
        cdef c.ibv_sge *csge
        cdef int i, j, n, rc
        cdef int wr_id
        cdef int num_sge

        # NOTE: A copy of this is in SRQ.post_recv
        wrlist = _post_check(arg, recv_wr, self._cap.max_recv_sge, &num_sge)

        n = len(wrlist)
        mem = <unsigned char *>calloc(1,sizeof(dummy_wr)*n + sizeof(dummy_sge)*num_sge);
        if mem == NULL:
            raise MemoryError()
        try:
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
                if isinstance(wr.sg_list, list) or isinstance(wr.sg_list, tuple):
                    cwr.num_sge = len(wr.sg_list)
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
                cwr = cwr + 1;

            rc = c.ibv_post_recv(self._qp, <c.ibv_recv_wr *>mem, &cbad_wr)
            if rc != 0:
                cwr = <c.ibv_recv_wr *>(mem);
                for 0 <= i < n:
                    if cwr+i == cbad_wr:
                        break;
                raise WRError(rc,"ibv_post_recv","Failed to post work request",n);
        finally:
            free(mem)

    def query(self,int mask):
        """Return information about the QP. *mask* selects which fields
        to return.

        :rtype: tuple(:class:`rdma.ibverbs.qp_attr`,:class:`rdma.ibverbs.qp_init_attr`)"""

        cdef c.ibv_qp_attr cattr
        cdef c.ibv_qp_init_attr cinit
        cdef int rc

        rc = c.ibv_query_qp(self._qp, &cattr, mask, &cinit)
        if rc != 0:
            raise rdma.SysError(rc,"ibv_query_qp",
                                "Failed to query queue pair")

        cap = qp_cap(max_send_wr=cattr.cap.max_send_wr,
                     max_recv_wr=cattr.cap.max_recv_wr,
                     max_send_sge=cattr.cap.max_send_sge,
                     max_recv_sge=cattr.cap.max_recv_sge,
                     max_inline_data=cattr.cap.max_inline_data);
        attr = qp_attr(qp_state=cattr.qp_state,
                       cur_qp_state=cattr.cur_qp_state,
                       path_mtu=cattr.path_mtu,
                       path_mig_state=cattr.path_mig_state,
                       qkey=cattr.qkey,
                       rq_psn=cattr.rq_psn,
                       sq_psn=cattr.sq_psn,
                       dest_qp_num=cattr.dest_qp_num,
                       qp_access_flags=cattr.qp_access_flags,
                       cap=cap,
                       ah_attr=from_ah_attr(&cattr.ah_attr),
                       alt_ah_attr=from_ah_attr(&cattr.alt_ah_attr),
                       pkey_index=cattr.pkey_index,
                       alt_pkey_index=cattr.alt_pkey_index,
                       en_sqd_async_notify=cattr.en_sqd_async_notify,
                       sq_draining=cattr.sq_draining,
                       max_rd_atomic=cattr.max_rd_atomic,
                       max_dest_rd_atomic=cattr.max_dest_rd_atomic,
                       min_rnr_timer=cattr.min_rnr_timer,
                       port_num=cattr.port_num,
                       timeout=cattr.timeout,
                       retry_cnt=cattr.retry_cnt,
                       rnr_retry=cattr.rnr_retry,
                       alt_port_num=cattr.alt_port_num,
                       alt_timeout=cattr.alt_timeout);
        icap = qp_cap(max_send_wr=cinit.cap.max_send_wr,
                     max_recv_wr=cinit.cap.max_recv_wr,
                     max_send_sge=cinit.cap.max_send_sge,
                     max_recv_sge=cinit.cap.max_recv_sge,
                     max_inline_data=cinit.cap.max_inline_data);
        init = qp_init_attr(send_cq=self._scq,
                            recv_cq=self._rcq,
                            cap=icap,
                            qp_type=cinit.qp_type,
                            sq_sig_all=cinit.sq_sig_all);
        return (attr, init)

    def attach_mcast(self,path):
        """Attach this QP to receive the multicast group described by
        *path.DGID* and *path.DLID*."""
        cdef int rc
        cdef void *dgid
        cdef Py_ssize_t length
        if PyObject_AsReadBuffer(path.DGID, <const_void_ptr_ptr>&dgid,
                                 &length) != 0 or length != 16:
            raise TypeError("Expected buffer")
        rc = c.ibv_attach_mcast(self._qp,<c.ibv_gid *>dgid,path.DLID);
        if rc != 0:
            raise rdma.SysError(rc,"ibv_attach_mcast",
                                "Failed to attach to %r"%(path));
        if self._groups is None:
            self._groups = [];
        # Relying on verbs to fail on double add
        self._groups.append((path.DGID,path.DLID))

    def detach_mcast(self,path):
        """Detach this QP from the multicast group described by
        *path.DGID* and *path.DLID*."""
        cdef int rc
        cdef void *dgid
        cdef Py_ssize_t length
        cdef object gid
        if PyObject_AsReadBuffer(path.DGID, <const_void_ptr_ptr>&dgid,
                                 &length) != 0 or length != 16:
            raise TypeError("Expected buffer")
        rc = c.ibv_detach_mcast(self._qp,<c.ibv_gid *>dgid,path.DLID);
        if rc != 0:
            raise rdma.SysError(rc,"ibv_detach_mcast",
                                "Failed to detach to %r"%(path));
        # Relying on verbs to fail on double remove
        self._groups.remove((path.DGID,path.DLID))

    def modify_to_init(self,path,int qp_access_flags=0):
        """Modify the QP to the INIT state."""
        if self._qp_type == c.IBV_QPT_UD:
            attr = qp_attr(qp_state=c.IBV_QPS_INIT,
                           pkey_index=path.pkey_index,
                           port_num=path.end_port.port_id,
                           qkey=path.qkey);
        else:
            attr = qp_attr(qp_state=c.IBV_QPS_INIT,
                           pkey_index=path.pkey_index,
                           port_num=path.end_port.port_id,
                           qp_access_flags=qp_access_flags);
        self.modify(attr,attr.MASK)

    def modify_to_rtr(self,path):
        """Modify the QP to the RTR state."""
        if self._qp_type == c.IBV_QPT_UD:
            attr = qp_attr(qp_state=c.IBV_QPS_RTR);
        elif self._qp_type == c.IBV_QPT_UC:
            attr = qp_attr(qp_state=c.IBV_QPS_RTR,
                           path_mtu=path.MTU,
                           dest_qp_num=path.dqpn,
                           rq_psn=path.dqpsn,
                           ah_attr=path)
        else:
            attr = qp_attr(qp_state=c.IBV_QPS_RTR,
                           path_mtu=path.MTU,
                           dest_qp_num=path.dqpn,
                           rq_psn=path.dqpsn,
                           max_dest_rd_atomic=path.drdatomic,
                           # Hmm, where does this come from?
                           min_rnr_timer=path.min_rnr_timer,
                           ah_attr=path)
        self.modify(attr,attr.MASK)

    def modify_to_rts(self,path):
        """Modify the QP to the RTS state."""
        if self._qp_type == c.IBV_QPT_UD or self._qp_type == c.IBV_QPT_UC:
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
        self.modify(attr,attr.MASK)

    def establish(self,path,int qp_access_flags=0):
        """Perform :meth:`modify_to_init`, :meth:`modify_to_rtr` and
        :meth`modify_to_rts`.  This function is most useful for UD QPs which
        do not require any external sequencing."""
        self.modify_to_init(path,qp_access_flags);
        self.modify_to_rtr(path);
        self.modify_to_rts(path);

    def __str__(self):
        return "qp:%u:%s"%(self._qp.qp_num,self._pd);
    def __repr__(self):
        return "QP(%r,0x%x,%u,qp_type=%s)"%(
            self._pd,self._qp.handle,self._qp.qp_num,
            IBA.const_str("IBV_QPT_",self._qp.qp_type,True,
                          sys.modules["rdma.ibverbs"]));
