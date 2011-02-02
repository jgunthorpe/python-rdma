***********
RDMA Module
***********

The RDMA grouping of functionality applies to general RDMA devices and is
not specific to the IBA.

Programs that use a single port should use :func:`rdma.get_end_port`
to find the port, passing in a command line argument to specify the port. The
library provides standardized parsing of an end port description. Users are
encouraged to use end port GIDs.

A list if RDMA devices is available through the :func:`rdma.get_rdma_devices`
call.

Related modules:

.. toctree::

   devices.rst
   path.rst
   tools.rst

:mod:`rdma` module
==================

The top level import for the rdma module provides the exception types used in
the package as well as the basic accessors for accessing the device list and
instantiating access classes.

.. automodule:: rdma
   :members:

