.. Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

***********
RDMA Module
***********

The RDMA grouping of functionality applies to general RDMA devices and is
not specific to the IBA.

Programs that use a single port should use :func:`rdma.get_end_port`
to find the port, passing in a command line argument to specify the port. The
library provides standardized parsing of an end port description. Users are
encouraged to use end port GIDs.

A list of RDMA devices is available through the :func:`rdma.get_devices`
call.

Related modules:

.. toctree::

   devices.rst
   path.rst
   tools.rst
   sim.rst

Exceptions
==========

The root exception for things thrown by this module is :exc:`rdma.RDMAError`.

Usage guidelines:

* :exc:`rdma.RDMAError` is thrown for general error conditions, like 'Device
  Not Found'. The single argument is a string containing the failure message.
  This are either system failure messages with no possible recovery, or sane
  context localized failures - ie :func:`~rdma.get_end_port` throws
  :exc:`rdma.RDMAError` if it cannot return a port.
* :exc:`rdma.MADError` is thrown for error conditions that arise from MAD
  RPC processing, including error status MADs and malformed replies.
* :exc:`rdma.MADTimeoutError` is thrown when a MAD RPC call times out.
* :exc:`rdma.MADClassError` is thrown when a MAD RPC call errors out with
  a class specific error.
* :exc:`rdma.SysError` for kernel syscalls that fail.
* :exc:`rdma.path.SAPathNotFoundError` when a path cannot be resolved due to the
  SA reporting it was not found.
* :exc:`rdma.ibverbs.WRError` when a verbs work request fails to post.
* :exc:`rdma.ibverbs.WCError` when a verbs work completion indicates an error.
* :exc:`rdma.ibverbs.AsyncError` when a error case verbs async event is received.

Python's exception processing is somewhat limited in how it deals with
complicated layering, for instance if a RPC is performed to resolve a path the
exception may appear as a simple timeout error. This is generally pretty
useless. The :exc:`rdma.MADError` class includes a mechanism to stack error
messages, the lowest layer puts a layer appropriate message and higher layers
stack their layer appropriate messages. To process this extra information any
application using the library should use a try block as follows::

 try:
    do_stuff();
 except rdma.MADError as err:
    err.dump_detailed(sys.stderr,"E:",level=level);

Where level is a verbosity level set by the user. The resulting dumps will
look something like this at level 1::

 E: Failed getting MAD path record for end port GID('fe80::2:c903:0:1492').
 E: +RPC MAD_METHOD_GET(1) SAFormat(3.2) SAPathRecord(53) got class specific error 3

Level 2 will include dumps of the request and reply packet that caused the
error.  Naturally raising the exception again will produce a traceback - which
is generally less interesting for network-related RPC errors.

:mod:`rdma` module
==================

The top level import for the rdma module provides the exception types used in
the package as well as the basic accessors for accessing the device list and
instantiating access classes.

.. automodule:: rdma
   :members:

