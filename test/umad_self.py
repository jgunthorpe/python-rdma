#!/usr/bin/python
import unittest
import rdma
import rdma.IBA as IBA;
import sys

class umad_self_test(unittest.TestCase):
    umad = None;
    tid = 0;

    def setUp(self):
        if self.umad == None:
            self.umad = rdma.get_umad(rdma.get_rdma_devices()[0].end_ports[0]);
            self.qp0 = self.umad.register_client(IBA.MAD_SUBNET,1);
            self.local_addr = self.umad.make_ah(0xFFFF,0);

    def xtest_node_info(self):
        inf = IBA.SMPPortInfo();

        pkt = IBA.SMPFormatDirected();
        pkt.MADHeader.baseVersion = IBA.MAD_BASE_VERSION;
        pkt.MADHeader.mgmtClass = IBA.MAD_SUBNET_DIRECTED;
        pkt.MADHeader.classVersion = 1;
        pkt.MADHeader.method = IBA.MAD_METHOD_GET;
        pkt.MADHeader.transactionID = self.tid;
        self.tid = self.tid + 1;
        pkt.MADHeader.attributeID = 0x15;
        pkt.drSLID = 0xFFFF;
        pkt.drDLID = 0xFFFF;
        inf.pack_into(pkt.data);

        test = bytearray(256);
        pkt.pack_into(test);

        self.umad.sendto(test,self.local_addr,self.qp0);
        (tmp,addr,agent_id) = self.umad.recvfrom();

        pkt2 = IBA.SMPFormat(tmp);
        pkt2.printer(sys.stdout);
        pkt2 = IBA.SMPFormatDirected(pkt2);
        pkt2.printer(sys.stdout);
        inf2 = IBA.SMPPortInfo(pkt2.data);
        inf2.printer(sys.stdout);

    def test_node_info(self):
        inf = IBA.SMPPortInfo();
        self.subnGet(inf,self.local_addr);
        (tmp,addr,agent_id) = self.umad.recvfrom();
        pkt2 = IBA.SMPFormatDirected(tmp);
        inf2 = IBA.SMPPortInfo(pkt2.data);
        inf2.printer(sys.stdout);

    def subnGet(self,payload,addr):
        fmt = IBA.SMPFormatDirected();
        fmt.drSLID = 0xFFFF;
        fmt.drDLID = 0xFFFF;
        self.sendMad(fmt,payload,payload.MAD_SUBNGET,addr);

    def sendMad(self,fmt,payload,method,addr):
        fmt.MADHeader.baseVersion = IBA.MAD_BASE_VERSION;
        fmt.MADHeader.mgmtClass = fmt.MAD_CLASS;
        fmt.MADHeader.classVersion = fmt.MAD_CLASS_VERSION;
        fmt.MADHeader.method = method;
        fmt.MADHeader.attributeID = payload.MAD_ATTRIBUTE_ID;
        fmt.MADHeader.transactionID = self.tid;
        self.tid = self.tid + 1;
        payload.pack_into(fmt.data);

        buf = bytearray(fmt.MAD_LENGTH);
        fmt.pack_into(buf);
        self.umad.sendto(buf,self.local_addr,self.qp0);

if __name__ == '__main__':
    unittest.main()
