#!/usr/bin/python

import os,os.path;

class RDMAError(Exception):
    '''General exception class for RDMA related errors.'''

class MADError(RDMAError):
    """Thrown when a MAD transaction returns with an error."""
    def __init__(self,req,rep,**kwargs):
        RDMAError.__init__(self);
        self.req = req;
        self.rep = rep;
        for k,v in kwargs.iteritems():
            self.__setattr__(k,v);

    def __str__(self):
        if "exc_info" in self.__dict__:
            return repr(self.exc_info);
        # FIXME: Decode what it was we asked for...
        import rdma.IBA;
        return "MAD error reply status 0x%x - %s"%(self.status,
                                                   rdma.IBA.mad_status_to_str(self.status));

class MADTimeoutError(MADError):
    '''Exception thrown when a MAD RPC times out.'''
    def __str__(self):
        if "exc_info" in self.__dict__:
            return repr(self.exc_info);
        return "MAD timed out";

def get_end_port(name=None):
    """Return a :class:`rdma.devices.EndPort` for the default end port if name
    is ``None``, or for the end port described by name.

    The end port string format is one of:
      =========== ===================
      Format      Example
      =========== ===================
      device      mlx4_0  (defaults to the first port)
      device/port mlx4_0/1
      Port GID    fe80::2:c903:0:1491
      Port GUID   0002:c903:0000:1491
      =========== ===================

    :rtype: :class:`rdma.devices.EndPort`
    :raises rdma.RDMAError: If no matching device is found or name is invalid."""
    devices = get_devices();
    if len(devices) == 0:
        raise RDMAError("No RDMA devices found.");
    if name is None:
        return devices.first().end_ports.first();

    # Try for a port GID
    import rdma.devices;
    import rdma.IBA;
    try:
        gid = IBA.GID(name);
    except ValueError:
        pass;
    else:
        return rdma.devices.find_port_gid(devices,gid)[0];

    # Port GUID
    try:
        guid = IBA.GUID(name);
    except ValueError:
        pass;
    else:
        return rdma.devices.find_port_guid(devices,guid);

    # Device name string
    return rdma.devices.find_port_name(devices,name);

def get_device(name=None):
    """Return a :class:`rdma.devices.Device` for the default device if name
    is ``None``, or for the device described by name.

    The device string format is one of:
      =========== ===================
      Format      Example
      =========== ===================
      device      mlx4_0
      Node GUID   0002:c903:0000:1491
      =========== ===================

    :rtype: :class:`rdma.devices.device`
    :raises rdma.RDMAError: If no matching device is found or name is invalid."""
    devices = get_devices();
    if len(devices) == 0:
        raise RDMAError("No RDMA devices found.");
    if name is None:
        return devices.first();

    # Port GUID
    import rdma.devices;
    import rdma.IBA;
    try:
        guid = IBA.GUID(name);
    except ValueError:
        pass;
    else:
        return rdma.devices.find_node_guid(devices,guid);

    # Device name string
    try:
        return devices[name];
    except KeyError:
        raise RDMAError("RDMA device %r not found."%(name));

_cached_devices = None;
def get_devices(refresh=False):
    '''Return a container of :class:`rdma.devices.RDMADevice` objects for all devices in the system.

    The return result is an object that looks like an ordered list of
    :class:`rdma.devices.RDMADevice` objects. However, indexing the list is
    done by device name not by index. If the length of the returned object is
    0 then no devices were detected. Programs are encouraged to use
    :func:`rdma.get_end_port`.

    :rtype: :class:`~.devices.DemandList` but this is an implementation detail.'''
    global _cached_devices;
    if _cached_devices is not None and not refresh:
        return _cached_devices;

    import rdma.devices;
    if not os.path.exists(rdma.devices.SYS_INFINIBAND):
        return ();

    _cached_devices = rdma.devices.DemandList2(
        rdma.devices.SYS_INFINIBAND,
        lambda x:rdma.devices.RDMADevice(x),
        lambda x:x);
    return _cached_devices;

def get_umad(port,**kwargs):
    '''Create a :class:`rdma.umad.UMAD` instance for the associated
    :class:`rdma.devices.EndPort`.'''
    import rdma.umad;
    return rdma.umad.UMAD(port,**kwargs);

def get_verbs(port,**kwargs):
    '''Create a :class:`rdma.uverbs.UVerbs` instance for the associated
    :class:`rdma.devices.RDMADevice`/:class:`rdma.devices.EndPort`.'''
    import rdma.uverbs;
    return rdma.uverbs.UVerbs(port,**kwargs);
