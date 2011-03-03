Verbs Interface
===============

verbs objects provide a wrapper around the OFA verbs interface from
`libibverbs`. The wrapper puts the verbs interface into an OOP methodology
and generally exposes most functionality to Python.

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

:class:`rdma.path.IBPath` and Verbs
-----------------------------------

The raw verbs interface for creating QPs and their associated connetions is
simplified to rely on the standard :class:`~rdma.path.IBPath` structure which
should be filled in with all the necessary parameters. The wrapper QP modify
methods :meth:`~rdma.ibverbs.QP.modify_to_init`,
:meth:`~rdma.ibverbs.QP.modify_to_rtr`, and
:meth:`~rdma.ibverbs.QP.modify_to_rts` can setup a QP without additional
information.

:class:`~rdma.path.IBPath` structures can also be used any place where an
:class:`~rdma.ibverbs.ah_attr` could be used, including for creating
:class:`~rdma.ibverbs.AH` instances and with :meth:`~rdma.ibverbs.QP.modify`.

As for MADs the are additional RC/RD specific fields in the
:class:`~rdma.path.IBPath` structure. These must be filled in as part of the
connection setup process.

The QP related path parameters are:

================  ==========================
Path Attribute    Usage
================  ==========================
min_rnr_timer     qp_attr.min_rnr_timer
packet_life_time  qp_attr.timeout
dack_resp_time    qp_attr.timeout
sack_resp_time
dqpsn             qp_attr.dest_qp_num
sqpsn
drdatomic         qp_attr.max_dest_rd_atomic
srdatomic         qp_attr.max_rd_atomic
================  ==========================

The library has built in support for correctly establishing IB connections
without using a CM. Side A would do this::

  qp = pd.qp(...);
  path = rdma.path.IBPath(end_port,SGID=end_port.gids[0]);
  rdma.path.fill_path(qp,path);
  path.reverse();
  send_to_side_b(pickle.pickle(path));
  path = pickle.unpickle(recv_from_side_b());
  path.reverse();
  path.end_port = end_port;

  qp.modify_to_init(self.path,ibv.IBV_ACCESS_REMOTE_WRITE);
  qp.modify_to_rtr(self.path);
  qp.modify_to_rts(self.path);

  # Synchronize transition to RTS
  send_to_side_b(True);
  recv_from_side_b();

Side B would do this::

  qp = pd.qp(...);
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

Notes
-----

Provides Python interface to libibverbs.  All of the symbols retain their
names, but there are some differences between C and Python use:

- constructors are used to initialize structures.  For example::

      init = ibv_qp_init_attr(send_cq=cq, recv_cq=cq)

  all of the parameters are optional, so it is still possible
  to do this::

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
  reaped::

    m = mmap(-1,length)
    mr1 = ibv_mr(m, IBV_LOCAL_WRITE)
    mr2 = ibv_mr('foo')

    wr = ibv_send_wr()
    wr.sg_list=(ibv_sge(addr=mr.addr,length=mr.length,lkey=mr.lkey),
                ibv_sge(addr=mr2.addr,length=mr2.length,lkey=mr2.key))
    ...
    rc = ibv_post_send(

- can use methods on verb objects, eg::

      qp.modify(attr, mask)

  is equivalent to::

      ibv_modify_qp(qp, attr, mask)

- structure objects maintain the attribute mask by monitoring
  field assignments made by the constructor and subsequent
  assignment statements::

       attr = ibv_qp_attr()
       attr.qp_state        = IBV_QPS_INIT
       attr.pkey_index      = 0
       attr.port_num        = port
       attr.qp_access_flags = IBV_ACCESS_REMOTE_WRITE
       ibv_modify_qp(qp, attr, attr.MASK)

  Remember to zero out MASK if the attr object is reused
  for another call.

.. automodule:: rdma.ibverbs
   :members:
   :undoc-members:
   :show-inheritance:
