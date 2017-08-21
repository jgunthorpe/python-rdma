.. Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

RDMA Path
=========

Several general objects are provides for storing paths. In RDMA a path is the
connection between two end ports. The path representation used in this library
holds the full connection description, including all the necessary header
fields. These fields will be used as necessary, depending on the context that
the path is used in.

.. note::
   For efficiency the path caches certain expensive information. In the
   current implementation the cache is imperfect and does not clear
   automatically. For this reason users should treat path records as write
   once. This is also good practice since a path may be held onto for a time
   when working with the parallel MAD scheduler or other cases.

IB Paths
--------
In the IBA a path is unidirectional, but it may have the special property of
being *reversible*. For reversible paths the return path is computed by
calling :meth:`rdma.path.IBPath.reverse`. Further, the path may be a 'forward'
or 'reverse' path relative to the associated :class:`rdma.devices.EndPort` -
the exact direction will depend on context - send paths are 'forward' while
receive paths are 'reverse'.

The attributes for a :class:`~rdma.path.IBPath` as associated with packet headers are:

================  ===========================
Path Attribute    Header Field
================  ===========================
SL                `rdma.IBA.HdrLRH.SL`
has_grh           `rdma.IBA.HdrLRH.LNH` [0]
DLID              `rdma.IBA.HdrLRH.DLID`
SLID              `rdma.IBA.HdrLRH.SLID`
traffic_class     `rdma.IBA.HdrGRH.TClass`
flow_label        `rdma.IBA.HdrGRH.flowLabel`
hop_limit         `rdma.IBA.HdrGRH.hopLmt`
SGID              `rdma.IBA.HdrGRH.SGID`
DGID              `rdma.IBA.HdrGRH.DGID`
pkey              `rdma.IBA.HdrBTH.PKey`
dqpn              `rdma.IBA.HdrBTH.destQP`
sqpsn             `rdma.IBA.HdrBTH.PSN`
qkey              `rdma.IBA.HdrDETH.QKey`
sqpn              `rdma.IBA.HdrDETH.srcQP`
min_rnr_timer     `rdma.IBA.HdrAETH.syndrome`
================  ===========================

The rule for this class is that it represents the packet headers in the context it is
used/created. Eg when sending a packet it represents the packet header to be sent. When
receiving a packet it represents the packet headers as received.

There are additional fields for use by verbs, review :ref:`ibverbs_path`.

To make the use of paths simpler in some common cases there are get/set
properties that access end port GID indexes, PKey indexes, and LID bits. When
used as a `setattr` the property will update the full version. When used as a
`getattr` the property will use the end port to compute the index. The
properties are able to cache the results of these searches. For example::

	# Use pkey index 0
	IBPath(end_port,pkey_index=0);
	IBPath(end_port,pkey=end_port.pkeys[0]);

	# Use the default PKEY
	IBPath(end_port,pkey=IBA.PKEY_DEFAULT);
	IBPath(end_port,end_port.pkeys.index(IBA.PKEY_DEFAULT));

Do the same things.

.. note::
   The usage of asymmetric paths hasn't been implemented yet. My feeling for this is
   that the path itself should be a reversible path and have additional attributes for
   the asymmetric paths. Depending on context the asymmetric attributes could then be
   used.

Directed route paths are supported through the :class:`rdma.path.IBDRPath`
subclass that includes additional information for use in the
:class:`rdma.IBA.SMPFormatDirected` MAD.

:mod:`rdma.path` module
-----------------------
.. automodule:: rdma.path
   :members:
   :undoc-members:
   :show-inheritance:
