#!/usr/bin/python
from __future__ import with_statement;

import rdma,rdma.tools;

SYS_INFINIBAND_VERBS = "/sys/class/infiniband_verbs/";

class UVerbs(rdma.tools.SysFSDevice):
    '''Handle to a uverbs kernel interface. This supports the context manager protocol.'''
    def __init__(self,parent):
        for I in parent._iterate_services_device(SYS_INFINIBAND_VERBS,"uverbs\d+"):
            rdma.tools.SysFSDevice.__init__(self,parent,I);
            break;
        else:
            raise rdma.RDMAError("Unable to open uverbs device for %s"%(repr(parent)));

    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self.parent,
                id(self));
