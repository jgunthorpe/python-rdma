Verbs Interface
===============

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
