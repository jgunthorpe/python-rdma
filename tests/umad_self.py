#!/usr/bin/python
import unittest
import rdma,rdma.path;
import rdma.IBA as IBA;
import sys

class umad_self_test(unittest.TestCase):
    umad = None;
    tid = 0;

    def setUp(self):
        if self.umad == None:
            self.end_port = rdma.get_rdma_devices().first().end_ports.first();
            self.umad = rdma.get_umad(self.end_port);
            self.qp0 = self.umad.register_client(IBA.MAD_SUBNET,1);
            self.local_path = rdma.path.IBDRPath(self.end_port,
                                                 umad_agent_id = self.qp0);

    def test_node_info(self):
        inf = IBA.SMPPortInfo();
        self.subnGet(inf,self.local_path);
        (tmp,path) = self.umad.recvfrom();
        
        pkt2 = IBA.SMPFormatDirected(tmp);
        inf2 = IBA.SMPPortInfo(pkt2.data);
        inf2.printer(sys.stdout);

    def subnGet(self,payload,path):
        if isinstance(path,rdma.path.IBDRPath):
            fmt = IBA.SMPFormatDirected();
            fmt.drSLID = path.drSLID;
            fmt.drDLID = path.drDLID;
            fmt.initialPath[:len(path.drPath)] = path.drPath;
            fmt.MADHeader.hopCount = len(path.drPath);
        else:
            fmt = IBA.SMPFormat();
        self.sendMad(fmt,payload,payload.MAD_SUBNGET,path,0);

    def sendMad(self,fmt,payload,method,path,qpn):
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
        self.umad.sendto(buf,path);

if __name__ == '__main__':
    unittest.main()
