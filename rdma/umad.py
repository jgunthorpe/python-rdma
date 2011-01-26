#!/usr/bin/python
from __future__ import with_statement;

import rdma,rdma.tools;
import rdma.IBA as IBA;
import fcntl,struct;
from socket import htonl as cpu_to_be32;
from socket import htons as cpu_to_be16;

SYS_INFINIBAND_MAD = "/sys/class/infiniband_mad/";

class UMad(rdma.tools.SysFSDevice):
    '''Handle to a umad kernel interface. This supports the context manager protocol.'''
    IB_IOCTL_MAGIC = 0x1b
    IB_USER_MAD_REGISTER_AGENT = rdma.tools._IOC(3,IB_IOCTL_MAGIC,1,28);
    IB_USER_MAD_UNREGISTER_AGENT = rdma.tools._IOC(1,IB_IOCTL_MAGIC,2,4);
    IB_USER_MAD_ENABLE_PKEY = rdma.tools._IOC(0,IB_IOCTL_MAGIC,3,0);

    def __init__(self,parent):
        for I in parent._iterate_services_end_port(SYS_INFINIBAND_MAD,"umad\d+"):
            rdma.tools.SysFSDevice.__init__(self,parent,I);
            break;
        else:
            raise rdma.RDMAError("Unable to open umad device for %s"%(repr(parent)));
        
        with open(SYS_INFINIBAND_MAD + "abi_version") as F:
            self.abi_version = int(F.read().strip());
        if self.abi_version < 5:
            raise RDMAError("UMAD ABI version is %u but we need at least 5."%(self.abi_version));
        if not self._ioctl_enable_pkey():
            raise RDMAError("UMAD ABI is not compatible, we need PKey support.");

        # typedef struct ib_user_mad {
        #  uint32_t agent_id;
        #  uint32_t status;
        #  uint32_t timeout_ms;
        #  uint32_t retries;
        #  uint32_t length;
        #  ib_mad_addr_t addr;
        #  uint8_t data[0];
        # } ib_user_mad_t;
        self.ib_user_mad_t = struct.Struct("=LLLLL44s");
        # typedef struct ib_mad_addr {
        #  uint32_t qpn; // network
        #  uint32_t qkey; // network
        #  uint16_t lid; // network
        #  uint8_t sl;
        #  uint8_t path_bits;
        #  uint8_t grh_present;
        #  uint8_t gid_index;
        #  uint8_t hop_limit;
        #  uint8_t traffic_class;
        #  uint8_t gid[16];
        #  uint32_t flow_label; // network
        #  uint16_t pkey_index;
        #  uint8_t reserved[6];
        # } ib_mad_addr_t;
        self.ib_mad_addr_t = struct.Struct("=LLHBBBBBB16sLH6x");
        self.ib_mad_addr_local_t = struct.Struct("=LLHBBxxxx16x4xH6x");

        self.sbuf = bytearray(4096);
        self.rbuf = bytearray(4096);

    def _ioctl_enable_pkey(self):
        return fcntl.ioctl(self.dev.fileno(),self.IB_USER_MAD_ENABLE_PKEY) == 0;
    def _ioctl_unregister_agent(self,agent_id):
        fcntl.ioctl(self.dev.fileno(),self.IB_USER_MAD_UNREGISTER_AGENT,
                    struct.pack("=I",agent_id));

    def _ioctl_register_agent(self,qpn,mgmt_class,mgmt_class_version,
                                oui,rmpp_version,method_mask):
        """Returns agent_id"""
        buf = struct.pack("=L4LBBB3BB",
                          0,
                          method_mask[0],method_mask[1],method_mask[2],method_mask[3],
                          qpn,
                          mgmt_class,
                          mgmt_class_version,
                          oui[0],oui[1],oui[2],
                          rmpp_version);
        buf = fcntl.ioctl(self.dev.fileno(),self.IB_USER_MAD_REGISTER_AGENT,
                          buf);
        return struct.unpack("=L",buf[:4])[0];

    def register_client(self,mgmt_class,mgmt_version):
        """This is the general entry point to start operating as a client.
        The class and version of outgoing MADs should be provided. agent_id is
        returned."""
        rmpp_version = 1 if mgmt_class == IBA.MAD_SUBNET_ADMIN else 0;
        qpn = 0 if (mgmt_class == IBA.MAD_SUBNET or
                    mgmt_class == IBA.MAD_SUBNET_DIRECTED) else 1;
        return self._ioctl_register_agent(qpn,mgmt_class,mgmt_version,
                                          (0x00,0x14,0x05),rmpp_version,
                                          [0]*4);

    def make_ah(self,dlid,qpn,sl=0,path_bits=0,grh=None,qkey=None,pkey=0):
        '''Construct an address handle for umad. The result from this
        is only valid for use with sendto.'''
        # NOTE: qkey is not used in the kernel currently (bug)
        if qkey == None:
            qkey = IBA.IB_DEFAULT_QP0_QKEY if qpn == 0 else IBA.IB_DEFAULT_QP1_QKEY;
        if grh:
            return self.ib_mad_addr_t.pack(cpu_to_be32(qpn),
                                           cpu_to_be32(qkey),
                                           cpu_to_be16(dlid),
                                           sl,path_bits,
                                           1,grh.gid_index,
                                           grh.hop_limit,grh.traffic_class,
                                           cpu_to_be32(grh.flow_label),
                                           pkey);
        return self.ib_mad_addr_local_t.pack(cpu_to_be32(qpn),
                                       cpu_to_be32(qkey),
                                       cpu_to_be16(dlid),
                                       sl,path_bits,pkey);

    # The kernel API is lame, don't use the timers. Send all MADs with 0
    # timeout and rely on our own code to match things up. It isn't clear that
    # agent_id is actually useful except to pick QP1 or QP0.
    def sendto(self,buf,addr,agent_id):
        '''Send a MAD packet'''
        self.ib_user_mad_t.pack_into(self.sbuf,0,
                                     agent_id,0,0,0,len(buf),addr);
        del self.sbuf[64:];
        self.sbuf.extend(buf);
        self.dev.write(self.sbuf);

    def recvfrom(self):
        '''Recv a MAD packet'''
        rc = self.dev.readinto(self.rbuf);
        (agent_id,status,timeout_ms,retries,length,addr) = self.ib_user_mad_t.unpack_from(bytes(self.rbuf),0);
        buf = bytes(self.rbuf[64:]);
        if status != 0:
            # With a 0 timeout this should never happen.
            raise RDMAError("umad send failure code=%d for %s"%(status,repr(buf)));
        return (buf,addr,agent_id);

    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self.parent,
                id(self));

