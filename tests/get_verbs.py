# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import unittest
import rdma

class get_verbs_test(unittest.TestCase):
    def test_get(self):
        for I in rdma.get_devices():
            with rdma.get_verbs(I) as X:
                print X;
            for Q in I.end_ports:
                with rdma.get_verbs(Q) as X:
                    print X;

if __name__ == '__main__':
    unittest.main()
