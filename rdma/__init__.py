#!/usr/bin/python

import os,os.path;

class RDMAError(Exception):
    '''General exception class for RDMA related errors.'''

class MADError(RDMAError):
    """Thrown when a MAD transaction returns with an error."""
    def __init__(self,req,rep,**kwargs):
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

_cached_devices = None;
def get_rdma_devices(refresh = False):
    '''Return a container of RDMADevice objects for all devices in the system'''
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
    '''Create a umad instance for the associated EndPort'''
    import rdma.umad;
    return rdma.umad.UMAD(port,**kwargs);

def get_verbs(port,**kwargs):
    '''Create a UVerbs instance for the associated Device/EndPort'''
    import rdma.uverbs;
    return rdma.uverbs.UVerbs(port,**kwargs);
