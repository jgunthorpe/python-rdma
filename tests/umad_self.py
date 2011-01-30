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
        inf = self.umad.SubnGet(IBA.SMPNodeInfo(),self.local_path);
        inf.printer(sys.stdout);
        ports = inf.numPorts;

        inf = self.umad.SubnGet(IBA.SMPPortInfo,self.local_path);
        inf.printer(sys.stdout);

        self.assertEqual(ports,len(self.end_port.parent.end_ports));
        for I in range(1,ports):
            inf = self.umad.SubnGet(IBA.SMPPortInfo,self.local_path,I);

        self.assertRaises(rdma.MADError,
                          self.umad.SubnGet,IBA.SMPPortInfo,
                          self.local_path,ports+1);

    def test_timeout(self):
        self.assertEqual(self.umad.recvfrom(100),None);

if __name__ == '__main__':
    unittest.main()
