# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import unittest
import rdma
import rdma.IBA as IBA;
import rdma.path

class path_test(unittest.TestCase):
    def check_path(self,end_port,cls=rdma.path.IBPath,**kwargs):
        path = rdma.path.IBPath(end_port,**kwargs);
        npath = rdma.path.from_string(repr(path),end_port);
        self.assertEquals(path.__dict__,npath.__dict__)

    def check_path_str(self,end_port,s,cls=rdma.path.IBPath,**kwargs):
        path = cls(end_port,**kwargs);
        npath = rdma.path.from_string(s);
        self.assertEquals(path.__dict__,npath.__dict__)
        self.assertEquals(npath.__class__,cls);
        npath = rdma.path.from_string(repr(path),end_port);
        self.assertEquals(path.__dict__,npath.__dict__)

    def test_str_good(self):
        """Check good input to :func:`rdma.path.from_string`."""
        self.check_path(None,DGID=IBA.GID("fe80::1"));
        self.check_path(None,DGID=IBA.GID("fe80::1"),SL=10,pkey=0xff);
        self.check_path(None,DGID=IBA.GID("fe80::1"),SLID=0x12,DLID=15);

        self.check_path_str(None,"fe80::1",DGID=IBA.GID("fe80::1"));
        self.check_path_str(None,"0:0:0:1",DGID=IBA.GID("fe80::1"));
        self.check_path_str(None,"1",DLID=1);
        self.check_path_str(None,"0xff",DLID=0xff);
        self.check_path_str(None,"0,1",cls=rdma.path.IBDRPath,drPath="\0\1");
        self.check_path_str(None,"0,",cls=rdma.path.IBDRPath,drPath="\0");

        for I in rdma.get_devices():
            for J in I.end_ports:
                self.check_path_str(J,"fe80::1%%%s"%(J),DGID=IBA.GID("fe80::1"))
                for G in J.gids:
                    if int(G) >> 64 != IBA.GID_DEFAULT_PREFIX:
                        self.check_path_str(J,"%s"%(G),DGID=G);

    def test_str_bad(self):
        """Check bad input to :func:`rdma.path.from_string`."""
        from rdma.path import from_string;
        self.assertRaises(ValueError,from_string,"xx");
        self.assertRaises(ValueError,from_string,"0:0:0");
        self.assertRaises(ValueError,from_string,"fe80::/");
        self.assertRaises(ValueError,from_string,"fe80::1x");
        self.assertRaises(ValueError,from_string,"Moo()");
        self.assertRaises(ValueError,from_string,"IBPath()");
        self.assertRaises(ValueError,from_string,"IBPath(end_port=Moo)");
        self.assertRaises(ValueError,from_string,"IBPath(XX=1)");
        self.assertRaises(ValueError,from_string,"IBPath(DLID=1x)");
        self.assertRaises(ValueError,from_string,"IBPath(DLID=1 , x)");
        self.assertRaises(ValueError,from_string,"IBPath(DLID=1 , SLID=)");

if __name__ == '__main__':
    unittest.main()
