.. Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

IB Subnet Database
==================

The library has a general storage database for holding information for an IB
subnet. Support is provided for partial population, eg the database can
sometimes store a :class:`~rdma.IBA.SMPPortInfo` without first having a
:class:`~rdma.IBA.SMPNodeInfo` and the like.

The design is careful to separate the notion of an `end port` compared
to an `arbitrary port`. Only switches can have `arbitrary ports`! Most
functions work with and return `end ports` which will always correspond
to switch port 0.


:mod:`rdma.subnet` Store IB Subnet Data
---------------------------------------
.. automodule:: rdma.subnet
   :members:
   :undoc-members:
   :show-inheritance:

:mod:`rdma.discovery` Retrieve IB Subnet Data
---------------------------------------------

Functions that end in `\_SA` collect information using SA
:meth:`~rdma.madtransactor.MADTransactor.SubnAdmGetTable` RPCs, while `\_SMP`
functions collect information using VL15
:meth:`~rdma.madtransactor.MADTransactor.SubnGet` RPCs. These are all helper
data collection functions to fill in a :class:`rdma.subnet.Subnet` instance.

`topo_` functions collect information on the subnet by walking it using directed route, while
`subnet_` functions collect information from LID routing.

Generally the :func:`rdma.discovery.load` function should be used as the entry
point for this module.

.. note::
   The functions have some assumption about the state of the
   :class:`rdma.subnet.Subnet` instance. Often they will not re-fetch
   data they already have. Some care must be taken to wipe out existing
   information before doing a discovery if the desire is to get new
   information.

.. automodule:: rdma.discovery
   :members:
   :undoc-members:
   :show-inheritance:
