# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import unittest;
try:
    import cPickle as pickle
except ImportError:
    import pickle;
import rdma.IBA as IBA;
import rdma.binstruct;
import rdma.subnet;

class pickle_test(unittest.TestCase):
    def test_basic(self):
        "Check that all IBA structs can be pickled and unpickled"
        for I in IBA.__dict__.itervalues():
            if not isinstance(I,rdma.binstruct.BinStruct):
                continue;
            tmp = I()
            ret = pickle.dumps(I());
            tmp2 = pickle.loads(ret);
            self.assertEquals(tmp.__class__,tmp2.__class__);

    def test_subnet(self):
        "Pickling Subnet objects"
        sbn = rdma.subnet.Subnet();

        pinf = IBA.SMPPortInfo()
        for I in range(1,100):
            pinf.LID = I
            port = sbn.get_port_pinf(pinf,portIdx=0,LID=I);
            port.portGUID = IBA.GUID(0xDEADBEEF0000 | I);
            sbn.ports[port.portGUID] = port;

        ret = pickle.dumps(sbn);
        tmp2 = pickle.loads(ret);

        self.assertEquals(len(sbn.all_nodes),len(tmp2.all_nodes));
        self.assertEquals(sorted(sbn.nodes.keys()),sorted(tmp2.nodes.keys()));
        self.assertEquals(sorted(sbn.ports.keys()),sorted(tmp2.ports.keys()));

if __name__ == '__main__':
    unittest.main()
