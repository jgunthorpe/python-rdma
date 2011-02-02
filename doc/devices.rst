:mod:`rdma.devices` module
==========================

The Linux RDMA discovery module determines the devices in the system by
probing in sysfs. The objects returned all defer their sysfs operations
until necessary and the cache the results. This means that none of the
objects and properties track runtime changes to the sysfs files.
Depending on the application this is either OK or disastrous.

The :class:`RDMADevice` and :class:`EndPort` contain properties that return
the various IBA defined quantities.

FIXME: Not sure what properties are available for iWarp devices.

.. automodule:: rdma.devices
   :members:
   :undoc-members:
   :show-inheritance:
