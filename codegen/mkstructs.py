#!/usr/bin/python
# ./mkstructs.py -x iba_transport.xml -x iba_12.xml -x iba_13_4.xml -x iba_13_6.xml -x iba_14.xml -x iba_15.xml -x iba_16_1.xml -x iba_16_3.xml -x iba_16_4.xml  -o ../rdma/IBA_struct.py -t ../tests/iba_struct.py -r ../doc/iba_struct.inc
'''This script converts the XML descriptions of IB structures into python
   classes and associated codegen'''
from __future__ import with_statement;
import sys,optparse,re,os;
from xml.etree import ElementTree;
from contextlib import contextmanager;

# From IBA.py - including this by name creates a circular module dependency
# that is easier to break this way.
MAD_METHOD_GET = 0x01;
MAD_METHOD_SET = 0x02;
MAD_METHOD_SEND = 0x03;
MAD_METHOD_GET_RESP = 0x81;
MAD_METHOD_TRAP = 0x05;
MAD_METHOD_TRAP_REPRESS = 0x07;
MAD_METHOD_GET_TABLE = 0x12;
MAD_METHOD_GET_TRACE_TABLE = 0x13;
MAD_METHOD_GET_MULTI = 0x14;
MAD_METHOD_DELETE = 0x15;
MAD_METHOD_RESPONSE = 0x80;

methodMap = {};
prefix = ("Subn","CommMgt","Performance","BM","DevMgt","SubnAdm","SNMP");
for I in prefix:
    for J in ("Get","Set","Send","Trap","Delete"):
        methodMap[I+J] = "MAD_METHOD_%s"%(J.upper());
    methodMap[I+"GetTable"] = "MAD_METHOD_GET_TABLE";
    methodMap[I+"GetTraceTable"] = "MAD_METHOD_GET_TRACE_TABLE";
    methodMap[I+"GetMulti"] = "MAD_METHOD_GET_MULTI";

@contextmanager
def safeUpdateCtx(path):
    """Open a temporary file path.tmp, return it, then close it and rename it
    to path using safeUpdate as a context manager"""
    tmp = path + ".tmp";
    try:
        os.unlink(tmp);
    except: pass;

    f = file(tmp,"wt");
    yield f;
    f.close();
    os.rename(tmp,path);

def rst_tableize(lst,idx):
    width = max(len(I[idx]) for I in lst);
    line = "="*width;
    yield line;
    first = True;
    for I in lst:
        yield I[idx].ljust(width);
        if first:
            yield line;
            first = False;
    yield line;

class Type(object):
    """Hold a single typed field in the structure"""
    mutable = True;

    def __init__(self,xml):
        self.count = int(xml.get("count","1"));
        self.bits = int(xml.get("bits"));
        self.off = xml.get("off");
        g = re.match("^(\d+)\[(\d+)\]$",self.off);
        if g:
            g = g.groups();
            self.off = int(g[0])*8 + int(g[1]);
        else:
            self.off = int(self.off)*8;
        self.type = xml.get("type");
        if self.type == "HdrIPv6Addr" and self.bits == 128:
            self.type = "struct IBA.GID";
            self.mutable = False;
        if self.type is None and xml.text is not None and \
           self.bits == 64 and "GUID" in xml.text:
            self.type = "struct IBA.GUID";
            self.mutable = False;

    def lenBits(self):
        return self.bits*self.count;
    def isObject(self):
        return self.type and self.type.startswith('struct ');
    def initStr(self):
        base = "0";
        if self.isObject():
            base = self.type[7:] + "()";
        elif self.bits > 64:
            base = "bytearray(%u)"%(self.bits/8);
        if self.count != 1:
            if self.bits <= 8:
                return "bytearray(%u)"%(self.count);
            return "[%s]*%u"%(base,self.count);
        return base;
    def type_desc(self):
        base = ":class:`int`";
        if self.isObject():
            ty = self.type[7:]
            if ty.startswith("IBA."):
                base = ":class:`~rdma.%s`"%(self.type[7:]);
            else:
                base = ":class:`~rdma.IBA.%s`"%(self.type[7:]);
        elif self.bits > 64:
            base = ":class:`bytearray` (%u)"%(self.bits/8);
        if self.count != 1:
            if self.bits <= 8:
                base = ":class:`bytearray` (%u)"%(self.count);
            return "[%s]*%u"%(base,self.count);
        return base;

    def make_pack(self,name,idx=0):
        return "%s.pack_into(buffer,offset + %u)"%(name,self.off/8 + idx*self.bits/8);
    def make_unpack(self,name,idx=0):
        if self.mutable:
            return "%s.unpack_from(buffer,offset + %u)"%(name,self.off/8 + idx*self.bits/8)
        return "%s = %s(buffer[offset + %u:offset + %u],raw=True)"%\
               (name,self.type[7:],self.off/8 + idx*self.bits/8,
                self.off/8 + (idx+1)*self.bits/8);

    def isAligned(self):
        if self.bits >= 32:
            return self.bits % 32 == 0 and self.off % 32 == 0;
        return (self.bits == 8 or self.bits == 16) and \
               (self.off % self.bits) == 0;
    def getStruct(self):
        if self.isObject():
            return self.type[7:];
        return None;

class Struct(object):
    '''Holds the a single structure'''
    def __init__(self,xml,fn):
        self.filename = fn;
        self.name = xml.get("name");
        self.size = int(xml.get("bytes"));
        self.desc = "%s (section %s)"%(xml.get("desc"),xml.get("sect"));
        self.sect = tuple(I for I in xml.get("sect").split("."));

        self.mgmtClass = xml.get("mgmtClass");
        self.mgmtClassVersion = xml.get("mgmtClassVersion");
        self.methods = xml.get("methods");
        self.attributeID = xml.get("attributeID");

        self.is_format = (self.name.endswith("Format") or
                          self.name.endswith("FormatDirected"));

        self.inherits = {};
        self.mb = [];
        self.packCount = 0;
        self.reserved = 0;

        for I in xml.getiterator("mb"):
            self.mb.append((I.text or "",Type(I)));
        assert(sum((I[1].lenBits() for I in self.mb),0) <= self.size*8);

    def set_reserved(self):
        def to_reserved(s):
            if not s:
                self.reserved = self.reserved + 1;
                return "reserved%u"%(self.reserved);
            return s;

        self.reserved = 0;
        self.mb = [(to_reserved(name),ty) for name,ty in self.mb];
        self.mbGroup = self.groupMB();

    def make_inherit(self):
        """*Format structures inherit from the first element, but
        we optimize the codegen a little bit..."""
        if not self.is_format:
            return;

        first = self.mb[0];
        if not (first[0].endswith("Header") and first[1].isObject()):
            return;
        parent = structMap[first[1].getStruct()];

        # replace the contents of the top struct into our mb list
        self.mb = parent.mb + self.mb[1:];
        self.inherits[first[0]] = parent;

        # FIXME: I would like it if this was actually done with some
        # inheritance so that isinstance would work properly, but since we use
        # slots that seems like it would just cause confusion.  Certainly the
        # codegen of a single pack/unpack is very desirable.

        assert(sum((I[1].lenBits() for I in self.mb),0) <= self.size*8);
        self.make_inherit();

    def gen_component_mask(self,follow=True):
        """We have an automatic system for managing the component mask value
        used in SA queries. This generates the component mask bit offsets."""
        res = [];
        for name,mbt in sorted(self.mb,key=lambda x:x[1].off):
            struct = mbt.getStruct();
            if follow and struct is not None and struct in structMap:
                tmp = structMap[struct].gen_component_mask(False);
                res.extend("%s.%s"%(name,J) for J in tmp);
            else:
                res.append(name)
        return res;

    def groupMB(self):
        """Take the member list and group it into struct format characters. We
        try to have 1 format character for each member, but if that doesn't
        work out we group things that have to fit into a 8, 16 or 32 bit
        word."""

        groups = [];
        curGroup = [];
        off = 0;
        for I in self.mb:
            bits = I[1].lenBits();
            curGroup.append(I);

            if (off == 0 and (off + bits) % 32 == 0) or \
               (off + bits) % 32 == 0:
                if reduce(lambda a,b:a and b[1].isAligned(),curGroup,True):
                    for J in curGroup:
                        groups.append((J,));
                else:
                    groups.append(curGroup);
                curGroup = [];
                off = 0;
                continue;
            off = off + bits;
        assert(not curGroup);
        return groups;

    def bitsToFormat(self,bits):
        if bits == 8:
            return "B";
        if bits == 16:
            return "H";
        if bits == 32:
            return "L";
        if bits == 64:
            return "Q";
        assert(False);

    def formatSinglePack(self,bits,name,mbt):
        other = mbt.getStruct();
        if other:
            if mbt.count == 1:
                return (None,(mbt.make_pack(name),
                              mbt.make_unpack(name)),
                        mbt.lenBits());
            lst = [];
            for I in range(0,mbt.count):
                n = "%s[%u]"%(name,I);
                lst.append((None,(mbt.make_pack(n,I),
                                  mbt.make_unpack(n,I)),
                            mbt.lenBits()))
            return lst;
        if mbt.type == "HdrIPv6Addr":
            return ("[:16]",name,bits);
        if mbt.count == 1:
            if mbt.type is None and bits > 64:
                return ("[:%u]"%(bits/8),name,bits);
            return (self.bitsToFormat(bits),name,bits);
        if mbt.bits == 8:
            return ("[:%u]"%(bits/8),name,bits);
        if mbt.bits == 16 or mbt.bits == 32:
            res = []
            for I in range(0,mbt.count):
                res.append((self.bitsToFormat(mbt.bits),"%s[%u]"%(name,I),
                           mbt.bits));
            return res;

        # Must be a bit array
        assert(bits % 8 == 0)
        return (None,("rdma.binstruct.pack_array8(buffer,%u,%u,%u,%s)"%\
                      (mbt.off/8,mbt.bits,mbt.count,name),
                      "rdma.binstruct.unpack_array8(buffer,%u,%u,%u,%s)"%\
                      (mbt.off/8,mbt.bits,mbt.count,name)),
                bits);

    def structFormat(self,groups,prefix):
        res = [];
        for I in groups:
            bits = sum(J[1].lenBits() for J in I);
            assert(bits == 8 or bits == 16 or bits == 32 or bits % 32 == 0);
            if len(I) == 1:
                x = self.formatSinglePack(bits,prefix + I[0][0],I[0][1]);
                if isinstance(x,list):
                    res.extend(x);
                else:
                    res.append(x);
                continue;

            func = "_pack_%u_%u"%(self.packCount,bits);
            self.packCount = self.packCount + 1;

            pack = ["@property","def %s(self):"%(func)];
            unpack = ["@%s.setter"%(func),"def %s(self,value):"%(func)];
            tmp = [];
            off = bits;
            for J in I:
                off = off - J[1].bits;
                tmp.append("((%s%s & 0x%X) << %u)"%(prefix,J[0],(1 << J[1].bits)-1,off));
                unpack.append("    %s%s = (value >> %u) & 0x%X;"%(prefix,J[0],off,(1 << J[1].bits)-1));
            pack.append("    return %s"%(" | ".join(tmp)));
            self.funcs.append(pack);
            self.funcs.append(unpack);

            res.append((self.bitsToFormat(bits),"self.%s"%(func),bits));
        return res;

    def genFormats(self,fmts,pack,unpack):
        """Split into struct processing blocks and byte array assignment
        blocks"""
        off = 0;
        sfmts = [[]];
        sfmtsOff = [];
        fmtsOff = 0;
        for I in fmts:
            if I[0] is None:
                pack.append("    %s;"%(I[1][0]));
                unpack.append("    %s;"%(I[1][1]));
                off = off + I[2];
                continue;
            if I[0][0] == '[':
                assert off % 8 == 0 and I[2] % 8 == 0;
                pack.append("    buffer[offset + %u:offset + %u] = %s"%\
                            (off/8,off/8 + I[2]/8,I[1]));
                unpack.append("    %s = buffer[offset + %u:offset + %u]"%\
                              (I[1],off/8,off/8 + I[2]/8));
                off = off + I[2];
                continue;
            if fmtsOff != off and sfmts[-1]:
                sfmts.append([])

            if not sfmts[-1]:
                sfmtsOff.append(off);
            sfmts[-1].append(I);
            off = off + I[2];
            fmtsOff = off;

        for I,off in zip(sfmts,sfmtsOff):
            pack.append("    struct.pack_into('>%s',buffer,offset+%u,%s);"%\
                     ("".join(J[0] for J in I),
                      off/8,
                      ",".join(J[1] for J in I)));
            unpack.append("    (%s,) = struct.unpack_from('>%s',buffer,offset+%u);"%\
                          (",".join(J[1] for J in I),
                          "".join(J[0] for J in I),
                          off/8));

    def genPrinter(self):
        x = ["def printer(self,F,offset=0,header=True):",
             "    rdma.binstruct.BinStruct.printer(self,F,offset,header);"];
        groups = list(self.mbGroup);
        I = 0;
        while I < len(groups):
            bits = sum(J[1].lenBits() for J in groups[I]);
            if bits >= 32:
                I = I + 1;
                continue;
            groups[I] = groups[I] + groups[I+1];
            del groups[I+1];

        off = 0;
        for I in groups:
            bits = sum(J[1].lenBits() for J in I);
            assert bits % 32 == 0;
            if self.is_format and I[0][0] == "data":
                x.append('    self._format_data(F,%u,%u,offset);'%(off,off+bits));
            else:
                label = ','.join("%s=%%r"%(J[0]) for J in I);
                label2 = ','.join("self.%s"%(J[0]) for J in I);
                x.append('    label = "%s"%%(%s);'%(label,label2));
                x.append('    self.dump(F,%u,%u,label,offset);'%(off,off+bits));
            off = off + bits;
        if len(x) == 1:
            x.append('    return;');
        self.funcs.append(x);

    def get_properties(self):
        yield "MAD_LENGTH","%u"%(self.size);
        if self.mgmtClass:
            yield "MAD_CLASS","0x%x"%(int(self.mgmtClass,0));
            yield "MAD_CLASS_VERSION","0x%x"%(int(self.mgmtClassVersion,0));
        if self.attributeID:
            yield "MAD_ATTRIBUTE_ID","0x%x"%(int(self.attributeID,0));
        if self.methods:
            is_sa = False;
            for I in self.methods.split():
                if I.startswith("SubnAdm"):
                    is_sa = True;
                yield "MAD_%s"%(I.upper()),"0x%x # %s"%(globals()[methodMap[I]],
                                                        methodMap[I]);
            if is_sa:
                cm = self.gen_component_mask();
                if cm:
                    yield "COMPONENT_MASK","{%s}"%(", ".join("%r:%u"%(name,I) for I,name in enumerate(cm)));

    def asPython(self,F):
        self.funcs = [];

        if self.mb:
            x = ["def __init__(self,*args):"];
            for name,ty in self.mb:
                if (ty.isObject() and ty.mutable) or ty.count != 1:
                    x.append("    self.%s = %s;"%(name,ty.initStr()));
            if len(x) != 1:
                x.append("    rdma.binstruct.BinStruct.__init__(self,*args);");
                self.funcs.append(x);
            x = ["def zero(self):"];
            for name,ty in self.mb:
                x.append("    self.%s = %s;"%(name,ty.initStr()));
            self.funcs.append(x);

        pack = ["def pack_into(self,buffer,offset=0):"];
        unpack = ["def unpack_from(self,buffer,offset=0):",
                  "    self._buf = buffer[offset:];"];
        fmts = self.structFormat(self.mbGroup,"self.");
        if fmts:
            self.genFormats(fmts,pack,unpack);
        else:
            pack.append("    return None;");
            unpack.append("    return;");
        self.funcs.append(pack);
        self.funcs.append(unpack);

        self.genPrinter();

        self.slots = ','.join(repr(I[0]) for I in self.mb);
        if self.is_format:
            print >> F,"class %s(BinFormat):"%(self.name);
        else:
            print >> F,"class %s(rdma.binstruct.BinStruct):"%(self.name);
        print >> F,"    '''%s'''"%(self.desc);
        print >> F,"    __slots__ = (%s);"""%(self.slots);

        for name,value in self.get_properties():
            print >> F, "    %s = %s"%(name,value);

        for I in self.funcs:
            print >> F, "   ", "\n    ".join(I);
            print >> F

    def asRST(self,F):
        print >> F,".. class:: rdma.IBA.%s"%(self.name)
        print >> F,""
        if self.inherits:
            print >> F,"    An *aggregation* of: %s"%(", ".join(I.name for I in self.inherits.itervalues()))
            print >> F,""
        print >> F,"   ",self.desc
        print >> F,""
        for name,value in self.get_properties():
            print >> F, "    .. attribute:: %s = %s"%(name,value);
        print >> F,""

        rows = [("Member","Position","Type")];
        for name,ty in self.mb:
            rows.append((":attr:`%s`"%(name),
                         "%u:%u (%u)"%(ty.off,ty.off+ty.lenBits(),
                                       ty.bits),
                         ty.type_desc()));
        if rows:
            for I in zip(rst_tableize(rows,0),rst_tableize(rows,1),rst_tableize(rows,2)):
                print >> F,"   "," ".join(I)
            print >> F,""

parser = optparse.OptionParser(usage="%prog")
parser.add_option('-x', '--xml', dest='xml', action="append")
parser.add_option('-o', '--struct-out', dest='struct_out')
parser.add_option('-t', '--test-out', dest='test_out')
parser.add_option('-r', '--rst-out', dest='rst_out')
(options, args) = parser.parse_args()

structs = [];
for I in options.xml:
    with open(I,'r') as F:
        doc = ElementTree.parse(F);
        for xml in doc.findall("struct"):
            if not xml.get("containerName"):
                structs.append(Struct(xml,I));
structMap = dict((I.name,I) for I in structs);
for I in structs:
    I.make_inherit();
for I in structs:
    I.set_reserved();

with safeUpdateCtx(options.struct_out) as F:
    print >> F, """import struct,rdma.binstruct;
class BinFormat(rdma.binstruct.BinStruct):
    '''Base class for all `*Format` type packet layouts.'''
    def _format_data(self,F,start_bits,end_bits,offset):
        attr = ATTR_TO_STRUCT.get((self.__class__,self.attributeID));
        if attr is None:
            return self.dump(F,start_bits,end_bits,'data',offset);
        attr(self,offset+start_bits/8).printer(F,offset+start_bits/8);
    def describe(self):
        '''Return a short description of the RPC described by this format.'''
        attr = ATTR_TO_STRUCT.get((self.__class__,self.attributeID));
        if attr is None:
            s = '??(%u)'%(self.attributeID);
        else:
            s = '%s(%u)'%(attr.__name__,self.attributeID);
        return '%s %s(%u.%u) %s'%(IBA.const_str('MAD_METHOD_',self.method,True),
                                  self.__class__.__name__,self.mgmtClass,
                                  self.classVersion,s);
        """;
    for I in structs:
        I.asPython(F);

    res = (I for I in structs if I.is_format);
    print >> F, "CLASS_TO_STRUCT = {%s};"%(",\n\t".join("(%u,%u):%s"%(
        int(I.mgmtClass,0),int(I.mgmtClassVersion,0),I.name) for I in res));

    res = []
    for I in structs:
        if I.is_format:
            for J in structs:
                if J.filename == I.filename and J.attributeID is not None:
                    res.append((I,J));
    print >> F, "ATTR_TO_STRUCT = {%s};"%(",\n\t".join("(%s,%u):%s"%(
        I[0].name,int(I[1].attributeID,0),I[1].name) for I in res));

with safeUpdateCtx(options.rst_out) as F:
    def is_sect_prefix(x,y):
        return x == y[:len(x)];
    sects = [(("12",),"Communication Management"),
             (("13","4"),"Generic MAD"),
             (("13","6"),"RMPP"),
             (("14",),"Subnet Management"),
             (("15",),"Subnet Administration"),
             (("16","1"),"Performance Management"),
             (("A13","6"),"Performance Management"),
             (("16","3"),"Device Management"),
             (("16","4"),"SNMP Tunneling")];
    lst = sorted(structs,key=lambda x:x.name);
    done = set();
    last = None;
    for I,name in sects:
        if name != last:
            header = "%s (%s)"%(name,".".join("%s"%(x) for x in I));
            print >> F, header;
            print >> F, "^"*len(header);
            print >> F
            last = name;
        for J in lst:
            if J not in done and is_sect_prefix(I,J.sect):
                J.asRST(F);
                done.add(J);

    header = "Miscellaneous IBA Structures";
    print >> F, header;
    print >> F, "^"*len(header);
    print >> F
    for J in lst:
        if J not in done:
                J.asRST(F);
with safeUpdateCtx(options.test_out) as F:
    print >> F,\
"""#!/usr/bin/python
import unittest,sys
import rdma.IBA as IBA;

class structs_test(unittest.TestCase):
    def test_component_mask(self):
        # See C15-0.1.27
        self.assertEqual(IBA.SAPortInfoRecord.COMPONENT_MASK["portInfo.capabilityMask"],7)
        self.assertEqual(IBA.SALinearForwardingTableRecord.COMPONENT_MASK["linearForwardingTable.portBlock"],3)

    def test_struct_packer(self):
        test = bytearray(512);
        testr = bytes(test);"""
    for I in structs:
        print >> F,'        assert(len(test) == 512);';
        print >> F,'        IBA.%s().pack_into(test);'%(I.name);
        print >> F,'        IBA.%s().unpack_from(testr);'%(I.name);
        print >> F,'        IBA.%s(testr);'%(I.name);
    print >> F, "    def test_struct_printer(self):";
    for I in structs:
        print >> F,'        IBA.%s().printer(sys.stdout);'%(I.name);
    print >> F,\
"""if __name__ == '__main__':
    unittest.main()""";
