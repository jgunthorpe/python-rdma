# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
import unittest
import rdma

class get_devices_test(unittest.TestCase):
    def test_list(self):
        devs = rdma.get_devices()
        print devs;
        for I in devs:
            print "RDMA Device '%s'"%(I.name);
            for J in ['node_type', 'fw_ver','node_guid','node_desc','sys_image_guid','board_id','hw_ver']:
                print "    %s: %s"%(J,repr(getattr(I,J)))
            for Q in I.end_ports:
                print "    port: %u"%(Q.port_id);
                for J in ['lid','lmc','phys_state','state','sm_lid','sm_sl','gids','pkeys']:
                    print "        %s: %s"%(J,repr(getattr(Q,J)))

if __name__ == '__main__':
    unittest.main()
