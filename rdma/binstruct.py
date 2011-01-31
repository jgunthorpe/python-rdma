#!/usr/bin/python
import rdma;
import abc;

# FIXME
def pack_array8(buf,offset,mlen,count,inp):
    return
    raise rdma.RDMAError("Not implemented");
def unpack_array8(buf,offset,mlen,count,inp):
    return
    raise rdma.RDMAError("Not implemented");

class BinStruct(object):
    '''Base class for all binary structure objects (MADs, etc)'''
    __metaclass__ = abc.ABCMeta;
    __slots__ = ('_buf');

    def __init__(self,buf = None,offset = 0):
        if buf != None:
            if isinstance(buf,BinStruct):
                buf = buf._buf;
            self.unpack_from(buf,offset);
        else:
            self._buf = None;
            self.zero();

    def printer(self,F,offset=0,header=True):
        """Pretty print the structure."""
        if header:
            print >> F, "%s"%(self.__class__.__name__);

    def dump(self,F,start_bits,end_bits,label,offset=0):
        """Display a single 'thing'. The display format is 'offest hexdword
        fmt' where fmt is the string version of the thing."""
        if self._buf is None:
            self._buf = bytearray(256);
            self.pack_into(self._buf);
            self._buf = bytes(self._buf);

        end_bits = end_bits/8;
        start_bits = start_bits/8;
        while start_bits < end_bits:
            print >> F, "% 3u %02X%02X%02X%02X %s"%\
                  (offset + start_bits,
                   ord(self._buf[start_bits]),ord(self._buf[start_bits+1]),
                   ord(self._buf[start_bits+2]),ord(self._buf[start_bits+3]),
                   label);
            label = '';
            start_bits = start_bits + 4;

    # 'pure virtual' functions
    def zero(self):
        """Set this instance back to the initial all zeros value."""
        return
    @abc.abstractmethod
    def unpack_from(self,buf,offset=0):
        """Expand the byte string buf starting at offset into this instance."""
        pass
    @abc.abstractmethod
    def pack_into(self,buf,offset=0):
        """Compact this instance into the byte array buf starting at offset."""
        pass
