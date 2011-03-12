.. Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.

:mod:`rdma.devices` module
==========================

The Linux RDMA discovery module determines the devices in the system by
probing in sysfs. The objects returned all defer their sysfs operations
until necessary and then cache the results. This means that none of the
objects and properties track runtime changes to the sysfs files.
Depending on the application this is either OK or disastrous.

When using verbs, the integerated
:meth:`rdma.ibverbs.Context.handle_async_event` method will update the
:class:`rdma.devices.EndPort` in response to async events from the kernel
indicating that the cached data is out of date.

The :class:`rdma.devices.RDMADevice` and :class:`rdma.devices.EndPort` contain
properties that return the various IBA defined quantities.

.. note::
   Currently this really only correctly supports IB devices. Other
   technologies will probably need subclasses that include appropriate
   properties. eg iWarp devices do not have PKeys.

.. automodule:: rdma.devices
   :members:
   :undoc-members:
   :show-inheritance:
