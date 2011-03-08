Verbs Interface
===============

:mod:`rdma.ibverbs` implements a set of python extension objects and
functions that provide a wrapper around the OFA verbs interface from
`libibverbs`. The wrapper puts the verbs interface into an OOP methodology and
generally exposes most functionality to Python.

A basic example for getting a verbs instance and a protection domain is::

 import rdma
 import rdma.ibverbs as ibv

 end_port = rdma.get_end_port()
 with rdma.get_verbs(end_port) as ctx:
     pd = ctx.pd();

Verbs objects that have an underlying kernel allocation are all context
managers and have a :meth:`close` method, but the objects also keep track of
their own children. Ie closing a :class:`rdma.ibverbs.Context` will close all
:class:`rdma.ibverbs.PD` and :class:`rdma.ibverbs.CQ` objects created by it.
This makes resource clean up quite straightforward in most cases.

Like with :class:`file` objects users should be careful to call the
:meth:`close` method once the instance is no longer needed. Generally
focusing on the :class:`rdma.ibverbs.Context` and :class:`rdma.ibverbs.PD`
is sufficient due to the built in resource clean up.

The IB verbs structures (eg ibv_qp_attr) are mapped into Python objects, (eg
:class:`rdma.ibverbs.ibv_qp_attr`). As Python objects they work similary to the C
syntax with structure member assignment, but they can also be initialized with
a keyword argument list to the constructor. This can save a considerable number of lines.

There are effecient wraper functions that create
:class:`~rdma.ibverbs.qp_attr`, :class:`~rdma.ibverbs.ah_attr` and
:class:`~rdma.ibverbs.sge` objects with a reduced number of arguments.

Errors from verbs are raised as a :class:`rdma.SysError` which includes
the `libibverb` function that failed and the associated errno.

.. note::
   Despite the name 'ibverbs' the verbs interface is a generic interface
   that is supported by all RDMA devices. Different technologies have various
   limitations and support for anything but IB through this library is not
   completed.

.. _ibverbs_path:

Verbs and :class:`rdma.path.IBPath`
-----------------------------------

The raw verbs interface for creating QPs is simplified to rely on the standard
:class:`~rdma.path.IBPath` structure which should be filled in with all the
necessary parameters. The wrapper QP modify methods
:meth:`~rdma.ibverbs.QP.modify_to_init`,
:meth:`~rdma.ibverbs.QP.modify_to_rtr`, and
:meth:`~rdma.ibverbs.QP.modify_to_rts` can setup a QP without additional
information.

The attributes in an :class:`~rdma.path.IBPath` are used as follows when modifying
a QP:

================  ==========================
Path Attribute    Usage
================  ==========================
end_port.port_id  qp_attr.port_num
pkey              qp_attr.pkey_index
qkey              qp_attr.qkey
MTU		  qp_attr.path_mtu
retries		  qp_attr.retry_cnt
min_rnr_timer     qp_attr.min_rnr_timer
packet_life_time  qp_attr.timeout
dack_resp_time    qp_attr.timeout
sack_resp_time
dqpn              qp_attr.dest_qp_num
sqpn
dqpsn             qp_attr.rq_psn
sqpsn             qp_attr.sq_psn
drdatomic         qp_attr.max_dest_rd_atomic
srdatomic         qp_attr.max_rd_atomic
================  ==========================

:class:`~rdma.path.IBPath` structures can also be used any place where an
:class:`~rdma.ibverbs.ah_attr` could be used, including for creating
:class:`~rdma.ibverbs.AH` instances and with
:meth:`~rdma.ibverbs.QP.modify`. With this usage the
:class:`~rdma.path.IBPath` caches the created AH, so getting the AH for a path
the second time does not rebuild the AH. This means callers generally don't
have to worry about creating and maintaining AH's explicitly.

The attributes in an :class:`~rdma.path.IBPath` are used as follows when creating
an AH:

================  ==========================
Path Attribute    Usage
================  ==========================
has_grh		  ah_attr.is_global
DGID		  ah_attr.grh.dgid
SGID		  ah_attr.grh.sgid_index
flow_label	  ah_attr.grh.flow_label
hop_limit	  ah_attr.grh.hop_limit
traffic_class	  ah_attr.grh.traffic_class
DLID		  ah_attr.dlid
SLID		  ah_attr.SLID_bits
SL		  ah_attr.SL
rate		  ah_attr.static_rate
end_port.port_id  ah_attr.port_num
================  ==========================

Usage Examples
--------------

This is not intended to be a verbs primer. Generally the API follows that of
the normal OFA verbs (with `ibv\_` prefixes removed) , which in turn follows
the API documented by the IBA specification. Many helper functions are
provided to handle common situations in a standard way, generally these are
preferred.

UD QP Setup
^^^^^^^^^^^

Setting up a QP for UD communication is very simple. There are two major
cases, for communication with a single end port, and for communication with
multiple. The single case is::

 path = IBPath(end_port,dpqn=1,qkey=IBA.IB_DEFAULT_QP1_QKEY,DGID=...);
 with rdma.get_umad(path.end_port) as umad:
     rdma.path.resolve_path(umad,path,reversible=True);
 with ctx.pd() as pd:
     depth = 16;
     cq = pd.cq(2*depth);
     qp = pd.qp(ibv.IBV_QPT_UD,depth,cq,depth,cq)
     path.sqpn = qp.qp_num;
     # Post receive work requests to qp here
     qp.modify_to_init(path);
     qp.modify_to_rtr(path);
     qp.modify_to_rts(path);

     qp.post_send(ibv.send_wr(opcode=ibv.IBV_WR_SEND,
			      send_flags=ibv.IBV_SEND_SIGNALED,
			      ah=pd.ah(path),
			      remote_qpn=path.dpqn,
			      remote_qkey=path.qkey,
			      ...));

Notice that the path is used to configure the pkey and qkey values of the UD
QP during initialization, and is also used to create the AH for the send work
request.

The case for multiple destinations is very similar, however all destinations
must share the same PKey and QKey. For instance, assuming there is a list of
DGIDs::

 with rdma.get_umad(path.end_port) as umad:
     paths = [rdma.path.resolve_path(umad,IBPath(end_port,DGID=I,
                                                 qkey=IBA.IB_DEFAULT_QP1_QKEY),
                                     reversible=True,
                                     properties={'PKey': IBA.DEFAULT_PKEY})
              for I in destinations];

Will resolve all the DGIDs into paths with the same QKey and PKey. paths[-1]
can be used to setup the QP and all the paths can be used interchangeably
in work requests.

UD response path
^^^^^^^^^^^^^^^^

Constructing the reply path from a UD WC is very straightforward::

 wcs = cq.poll():
 for wc in wcs:
     request_path = ibv.WCPath(self.end_port,wc,
                               buf,0,
                               pkey=qp_pkey,
                               qkey=qp_qkey);
     reply_path = request_path.reverse();
     ah = pd.ah(reply_path);

`buf,0` is the buffer and offset of the memory posted in the recv
request. Remember that on UD QPs the first 40 bytes of the receive buffer are
reserved for a GRH, which is accessed by :func:`rdma.ibverbs.WCPath`.

No CM RC QP Setup
^^^^^^^^^^^^^^^^^

The library has built in support for correctly establishing IB connections
without using a CM by exchanging information over a side channel (eg a TCP
socket). Side A would do this::

  qp = pd.qp(ibv.IBV_QPT_RC,...);
  path = rdma.path.IBPath(end_port,SGID=end_port.gids[0]);
  rdma.path.fill_path(qp,path);
  path.reverse(for_reply=False);
  send_to_side_b(pickle.pickle(path));
  path = pickle.unpickle(recv_from_side_b());
  path.reverse(for_reply=False);
  path.end_port = end_port;

  qp.modify_to_init(self.path,ibv.IBV_ACCESS_REMOTE_WRITE);
  qp.modify_to_rtr(self.path);
  qp.modify_to_rts(self.path);

  # Synchronize transition to RTS
  send_to_side_b(True);
  recv_from_side_b();

Side B would do this::

  qp = pd.qp(ibv.IBV_QPT_RC,...);
  path = pickle.unpickle(recv_from_side_a());
  path.end_port = end_port;
  rdma.path.fill_path(qp,path);
  with rdma.get_umad(path.end_port) as umad:
     rdma.path.resolve_path(umad,path);
  send_to_sid_a(pickle.pickle(path));

  qp.modify_to_init(self.path,ibv.IBV_ACCESS_REMOTE_WRITE);
  qp.modify_to_rtr(self.path);
  qp.modify_to_rts(self.path);

  # Synchronize transition to RTS
  recv_from_side_a();
  send_to_side_a(True);

:func:`rdma.path.fill_path` sets up most of the the QP related path parameters
and :func:`rdma.path.resolve_path` gets the path record(s) from the SA.

This procedure implements the same process and information exchange that the
normal IB CM would do, including negotiating responder resources and having
the capability to setup asymmetric paths (unimplemented today).

WC Error handling
^^^^^^^^^^^^^^^^^

The class :class:`rdma.ibverbs.WCError` is an exception that can be thrown
when a WC error is detected. It formats the information in the WC and provides
a way for the catcher to determine the failed QP::

 wcs = cq.poll():
 for wc in wcs:
     if wc.status != ibv.IBV_WC_SUCCESS:
         raise ibv.WCError(wc,qp=qp);

Depending on the situation QP errors may not be recoverable so the whole QP
should be torn down.

Completion Channels
^^^^^^^^^^^^^^^^^^^

Additional helpers are provided to simplify completion channel processing,
suitable for single threaded applications. The basic usage for a completion
channel is::

        # To setup the completion channel
        cc = ctx.comp_channel();
        poll = select.poll();
        cc.register_poll(poll);
        cq = ctx.cq(2*depth,cc)
        cq.req_notify_cq();

        def get_wcs():
            while True:
                ret = poll.poll();
                for I in ret:
                    if cc.check_poll(I) is not None:
                        wcs = cq.poll();
                        if wcs is not None:
                            return wcs;

        wcs = get_wcs();

Obviously the methodology becomes more complex if additional things are polled
for. The basic idea is that :meth:`rdma.ibverbs.CompChannel.check_poll` takes
care of all the details and returns the CQ that has available work
completions.

Using :mod:`rdma.vtools` the above example can be further simplified::

	cc = ctx.comp_channel();
	cq = ctx.cq(2*depth,cc)
	poller = rdma.vtools.CQPoller(cq,cc);

	for wc in poller.iterwc(timeout=1):
	    print wc

Memory
^^^^^^

Memory registrations are made explicit, as with verbs everything that is passed
into a work request must have an associated memory registration. A MR object
can be created for anything that supports the python buffer protocol, and
writable MRs require a mutable python buffer. Some useful examples::

 s = "Hello";
 mr = pd.mr(s,ibv.IBV_ACCESS_REMOTE_READ);
 s = bytearray(256);
 mr = pd.mr(s,ibv.IBV_ACCESS_REMOTE_WRITE);
 s = mmap.mmap(-1,256);
 mr = pd.mr(s,ibv.IBV_ACCESS_REMOTE_WRITE);

SGEs are constructed through the MR::

     sge = mr.sge();
     sge = mr.sge(length=128,off=10);

A tool is provided for managing a finite pool of fixed size buffers. This construct
is very useful for applications using the SEND verb::

   pool = rdma.vtools.BufferPool(pd,count=100,size=1024);
   pool.post_recvs(qp,50);

   buf_idx = pool.pop();
   pool.copy_to("Hello message!",buf_idx);
   qp.post_send(ibv.send_wr(wr_id=buf_idx,
		            sg_list=pool.make_sge(buf_idx,pool.size),
                            opcode=ibv.IBV_WR_SEND,
                            send_flags=ibv.IBV_SEND_SIGNALED,
                            ah=pd.ah(path),
                            remote_qpn=path.dqpn,
                            remote_qkey=path.qkey);


:mod:`rdma.vtools` module
=========================

:mod:`rdma.vtools` provides various support functions to make verbs
programming easier.

.. automodule:: rdma.vtools
   :members:
   :undoc-members:
   :show-inheritance:

:mod:`rdma.ibverbs` module
==========================

.. note::
   Unfortuntely sphinx does not do a very good job auto documenting extension
   modules, and all the function arguments are stripped out. Until this is
   resolved the documentation after this point is incomplete.

.. automodule:: rdma.ibverbs
   :members:
   :undoc-members:
   :show-inheritance:
