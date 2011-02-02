:mod:`rdma.path` module
=======================

Several general objects are provides for storing paths. In RDMA a path is the
connection between two end ports. The path represention used in this library
holds the full connection description, including all the necessary header
fields. These fields will be used as necessary, depending on the context that
the path is used in.

.. note::
   For efficiency the path caches certain expensive information. In the
   current implementation the cache is imperfect and does not clear
   automatically. For this reason users should treat path records as write
   once. This is also good practice since a path may be held onto for a time
   when working with the parallel MAD scheduler or other cases.

In the IBA a path is undirectional, but it may have the special property of
being *reversible*. For reversible paths the return path is computed by
calling :meth:`rdma.path.IBPath.reverse`. Further, the path may be a 'forward'
or 'reverse' path relative to the assoicated :class:`rdma.devices.EndPort` -
the exact direction will depend on context - send paths are 'forward' while
receive paths are 'reverse'.

Except for the special case of GMP and SMP MADs a pair of paths will be
required to establish communication.

.. automodule:: rdma.path
   :members:
   :undoc-members:
   :show-inheritance:
