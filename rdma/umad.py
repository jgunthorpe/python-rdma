# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
from __future__ import with_statement;

import rdma,rdma.tools,rdma.path,rdma.madtransactor;
import rdma.IBA as IBA;
import fcntl,struct,copy,errno,os,select;
from socket import htonl as cpu_to_be32;
from socket import htons as cpu_to_be16;

SYS_INFINIBAND_MAD = "/sys/class/infiniband_mad/";

class LazyIBPath(rdma.path.LazyIBPath):
    """Similar to :class:`rdma.path.IBPath` but the unpack of the UMAD AH is
    deferred until necessary since most of the time we do not care."""
    @staticmethod
    def _unpack_rcv(self):
        """Switch a UMAD AH back into an IBPath. Note this is only
        used for recv'd AH's where the meaning of the fields is altered.

        Our convention is that the path describes the packet headers as they
        existed on the wire, so this untwiddles things."""
        (sqpn,
         qkey,
         SLID,
         self.SL,
         DLID_bits,
         self.has_grh,
         DGID_index,
         self.hop_limit,
         self.traffic_class,
         self.SGID,
         flow_label,
         self.pkey_index) = \
         UMAD.ib_mad_addr_t.unpack(self._cached_umad_ah);
        self.sqpn = cpu_to_be32(sqpn);
        # FIXME: dqpn can be derived from agent_id
        self.qkey = cpu_to_be32(qkey);
        self.DLID = DLID_bits | self.end_port.lid;
        self.SLID = cpu_to_be16(SLID);
        if self.has_grh:
            self.SGID = IBA.GID(self.SGID,True);
            self.DGID = self.end_port.gids[DGID_index];
            self.flow_label = cpu_to_be32(flow_label);
        else:
            del self.SGID

class UMAD(rdma.tools.SysFSDevice,rdma.madtransactor.MADTransactor):
    '''Handle to a UMAD kernel interface. This class supports the context
    manager protocol.'''
    IB_IOCTL_MAGIC = 0x1b
    IB_USER_MAD_REGISTER_AGENT = rdma.tools._IOC(3,IB_IOCTL_MAGIC,1,28);
    IB_USER_MAD_UNREGISTER_AGENT = rdma.tools._IOC(1,IB_IOCTL_MAGIC,2,4);
    IB_USER_MAD_ENABLE_PKEY = rdma.tools._IOC(0,IB_IOCTL_MAGIC,3,0);

    # typedef struct ib_user_mad {
    #  uint32_t agent_id;
    #  uint32_t status;
    #  uint32_t timeout_ms;
    #  uint32_t retries;
    #  uint32_t length;
    #  ib_mad_addr_t addr;
    #  uint8_t data[0];
    # } ib_user_mad_t;
    ib_user_mad_t = struct.Struct("=LLLLL44s");
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
    ib_mad_addr_t = struct.Struct("=LLHBBBBBB16sLH6x");
    ib_mad_addr_local_t = struct.Struct("=LLHBBxxxx16x4xH6x");

    def __init__(self,parent):
        """*parent* is the owning :class:`rdma.devices.EndPort`."""
        rdma.madtransactor.MADTransactor.__init__(self);

        for I in parent._iterate_services_end_port(SYS_INFINIBAND_MAD,"umad\d+"):
            rdma.tools.SysFSDevice.__init__(self,parent,I);
            break;
        else:
            raise rdma.RDMAError("Unable to open umad device for %s"%(repr(parent)));

        with open(SYS_INFINIBAND_MAD + "abi_version") as F:
            self.abi_version = int(F.read().strip());
        if self.abi_version < 5:
            raise rdma.RDMAError("UMAD ABI version is %u but we need at least 5."%(self.abi_version));
        if not self._ioctl_enable_pkey():
            raise rdma.RDMAError("UMAD ABI is not compatible, we need PKey support.");

        self.sbuf = bytearray(320);

        fcntl.fcntl(self.dev.fileno(),fcntl.F_SETFL,
                    fcntl.fcntl(self.dev.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK);
        self._poll = select.poll();
        self._poll.register(self.dev.fileno(),select.POLLIN);

        self._agent_cache = {};

        self._tid = int(os.urandom(4).encode("hex"),16);
        self.end_port = parent;

    def _get_new_TID(self):
        self._tid = (self._tid + 1) % (1 << 32);
        return self._tid;

    def _ioctl_enable_pkey(self):
        return fcntl.ioctl(self.dev.fileno(),self.IB_USER_MAD_ENABLE_PKEY) == 0;
    def _ioctl_unregister_agent(self,agent_id):
        fcntl.ioctl(self.dev.fileno(),self.IB_USER_MAD_UNREGISTER_AGENT,
                    struct.pack("=I",agent_id));

    def _ioctl_register_agent(self,dqpn,mgmt_class,mgmt_class_version,
                                oui,rmpp_version,method_mask):
        """Returns agent_id"""
        buf = struct.pack("=L4LBBB3BB",
                          0,
                          method_mask[0],method_mask[1],method_mask[2],method_mask[3],
                          dqpn,
                          mgmt_class,
                          mgmt_class_version,
                          oui[0],oui[1],oui[2],
                          rmpp_version);
        buf = fcntl.ioctl(self.dev.fileno(),self.IB_USER_MAD_REGISTER_AGENT,
                          buf);
        return struct.unpack("=L",buf[:4])[0];

    def register_client(self,mgmt_class,class_version):
        """Manually register a MAD agent. This is done automatically for
        sending MADs, this API is mainly intended to enable listening
        for unsolicited messages."""
        try:
            return self._agent_cache[mgmt_class,class_version];
        except KeyError:
            rmpp_version = 1 if mgmt_class == IBA.MAD_SUBNET_ADMIN else 0;
            qpn = 0 if (mgmt_class == IBA.MAD_SUBNET or
                        mgmt_class == IBA.MAD_SUBNET_DIRECTED) else 1;
            ret = self._ioctl_register_agent(qpn,mgmt_class,class_version,
                                             (0x00,0x14,0x05),rmpp_version,
                                             [0]*4);
            self._agent_cache[mgmt_class,class_version] = ret;
            return ret;

    def _cache_make_ah(self,path):
        """Construct the address handle for UMAD and cache it in the path
        class"""
        assert(path.end_port == self.parent);
        # The kernel seems to have no way to explicitly set a permissive
        # SLID.. I wonder what it does?
        if path.SLID == IBA.LID_PERMISSIVE:
            slid_bits = 0;
        else:
            slid_bits = path.SLID_bits;
        if path.has_grh:
            res = self.ib_mad_addr_t.pack(cpu_to_be32(path.dqpn),
                                          cpu_to_be32(path.qkey),
                                          cpu_to_be16(path.DLID),
                                          path.SL,
                                          slid_bits,
                                          1,
                                          path.SGID_index,
                                          path.hop_limit,
                                          path.traffic_class,
                                          path.DGID,
                                          cpu_to_be32(path.flow_label),
                                          path.pkey_index);
        else:
            res = self.ib_mad_addr_local_t.pack(cpu_to_be32(path.dqpn),
                                                cpu_to_be32(path.qkey),
                                                cpu_to_be16(path.DLID),
                                                path.SL,
                                                slid_bits,
                                                path.pkey_index);
        path._cached_umad_ah = res;
        return res;

    # The kernel API is lame, you'd think setting a 0 timeout would be fine to
    # disable the state tracking, but it insists on tracking TIDs so that
    # doesn't work. Bascially this sucks. Using the kernel timers doesn't fit
    # well for us. There is no way to cancel MADs once submitted, basically it
    # is a huge pain. Plus this API ensures that userspace can OOM the
    # kernel. Weee. Bad Design. Let me send packets. Enforce some TID bits
    # outgoing and route matching TID bits on reply and leave the rest to me.

    # FIXME: This is really roughly connected to our timers - the idea
    # is to keep the kernel listening up until before our timer expires then
    # have the kerne let go so our retry isn't blocked. This leaves a small
    # window where packets are ignored, I suppose I should fixup the callers
    # to allow delegated timeout processing, but grrr......
    def sendto(self,buf,path,agent_id=None):
        '''Send a MAD packet. *buf* is the raw MAD to send, starting with the first
        byte of :class:`rdma.IBA.MADHeader`. *path* is the destination.'''
        try:
            addr = path._cached_umad_ah;
        except AttributeError:
            addr = self._cache_make_ah(path);

        if agent_id is None:
            agent_id = path.umad_agent_id;
        self.ib_user_mad_t.pack_into(self.sbuf,0,
                                     agent_id,0,
                                     max(500,int(path.mad_timeout*1000)-500),0,
                                     len(buf),
                                     addr);
        del self.sbuf[64:];
        self.sbuf.extend(buf);
        self.dev.write(self.sbuf);

    def recvfrom(self,wakeat):
        '''Receive a MAD packet. If the value of
        :func:`rdma.tools.clock_monotonic()` exceeds *wakeat* then :class:`None`
        is returned.

        :returns: tuple(buf,path)'''
        buf = bytearray(320);
        first = True;
        while True:
            timeout = wakeat - rdma.tools.clock_monotonic();
            try:
                rc = self.dev.readinto(buf);
            except IOError as err:
                if err.errno == errno.ENOSPC:
                    # Hmm.. Must be RMPP.. Resize the buffer accordingly.
                    rmpp_data2 = struct.unpack_from(">L",bytes(buf),32);
                    buf = bytearray(min(len(buf)*2,rmpp_data2));
                    continue;
                raise;

            if rc is None:
                if not first:
                    raise IOError(errno.EAGAIN,"Invalid read after poll");
                if timeout <= 0 or not self._poll.poll(timeout*1000):
                    return None;
                first = False;
                continue;

            path = rdma.path.IBPath(self.parent);
            (path.umad_agent_id,status,timeout_ms,retries,length,
             path._cached_umad_ah) = self.ib_user_mad_t.unpack_from(bytes(buf),0);
            path.__class__ = LazyIBPath;

            if status != 0:
                if status == errno.ETIMEDOUT:
                    first = True;
                    continue;
                raise rdma.RDMAError("umad send failure code=%d for %s"%(status,repr(buf)));
            return (buf[64:rc],path);

    def _gen_error(self,buf,path):
        """Sadly the kernel can return EINVAL if it could not process the MAD,
        eg if you ask for PortInfo of the local CA with an invalid attributeID
        the Mellanox driver will return EINVAL rather than construct an error
        MAD. I consider this to be a bug in the kernel, but we fix it here
        by constructing an error MAD."""
        buf = copy.copy(buf);
        rmatch = self._get_reply_match_key(buf);
        buf[3] = rmatch[1];
        buf[4] = 0;
        buf[5] = IBA.MAD_STATUS_INVALID_ATTR_OR_MODIFIER; # Guessing.
        path = path.copy();
        path.reverse();
        return (buf,path);

    def _execute(self,buf,path,sendOnly = False):
        """Send the fully formed MAD in buf to path and copy the reply
        into buf. Return path of the reply. This is a synchronous method, all
        MADs received during this call are discarded until the reply is seen."""
        if path.umad_agent_id is None:
            if isinstance(buf,bytearray):
                agent_id = self.register_client(buf[1],buf[2]);
            else:
                agent_id = self.register_client(ord(buf[1]),ord(buf[2]));
        else:
            agent_id = None;
        try:
            self.sendto(buf,path,agent_id);
        except IOError as err:
            if err.errno == errno.EINVAL:
                return self._gen_error(buf,path);
            raise

        if sendOnly:
            return None;

        rmatch = self._get_reply_match_key(buf);
        expire = path.mad_timeout + rdma.tools.clock_monotonic();
        retries = path.retries;
        while True:
            ret = self.recvfrom(expire);
            if ret is None:
                if retries == 0:
                    return None;
                retries = retries - 1;
                self._execute(buf,path,True);

                expire = path.mad_timeout + rdma.tools.clock_monotonic();
                continue;
            elif rmatch == self._get_match_key(ret[0]):
                return ret;
            else:
                if self.trace_func is not None:
                    self.trace_func(self,rdma.madtransactor.TRACE_UNEXPECTED,
                                    path=path,ret=ret);
    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self.parent,
                id(self));

