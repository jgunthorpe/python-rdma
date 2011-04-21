# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
import unittest,sys
import rdma.IBA as IBA;
import rdma.binstruct;

structs = set(I for I in IBA.__dict__.itervalues()
              if isinstance(I,type) and issubclass(I,rdma.binstruct.BinStruct));

class structs_test(unittest.TestCase):
    def test_component_mask(self):
        # See C15-0.1.27
        self.assertEqual(IBA.SAPortInfoRecord.COMPONENT_MASK["portInfo.capabilityMask"],7)
        self.assertEqual(IBA.SALinearForwardingTableRecord.COMPONENT_MASK["linearForwardingTable.portBlock"],3)

    def test_odd_size(self):
        fmt = IBA.SMPFormatDirected();
        drPath = bytes("0"*65);
        fmt.initialPath[:len(drPath)] = drPath;
        test = bytearray(fmt.MAD_LENGTH);
        fmt.pack_into(test);
        assert(len(test) == 257);

        fmt2 = IBA.SMPFormatDirected(test);
        fmt.printer(sys.stdout);
        fmt.printer(sys.stdout,format="dotted");
        fmt2.printer(sys.stdout);
        fmt2.printer(sys.stdout,format="dotted");

    def test_struct_packer(self):
        """Checking struct pack and unpack."""
        test = bytearray(512);
        testr = bytes(test);
        for I in structs:
            I().pack_into(test);
            assert(len(test) == 512);
            I().unpack_from(testr);
            I(testr);

    def test_struct_printer_dump(self):
        """Checking printer dump style"""
        for I in structs:
            I().printer(sys.stdout);

    def test_struct_printer_dotted(self):
        """Checking printer dotted style"""
        for I in structs:
            I().printer(sys.stdout,format="dotted");

if __name__ == '__main__':
    unittest.main()
