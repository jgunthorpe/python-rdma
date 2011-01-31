#!/usr/bin/python
import rdma;

# FIXME
def pack_array8(buffer,offset,mlen,count,inp):
    return
    raise rdma.RDMAError("Not implemented");
def unpack_array8(buffer,offset,mlen,count,inp):
    return
    raise rdma.RDMAError("Not implemented");

class BinStruct(object):
    '''Base class for all binary structure objects (MADs, etc)'''
    __slots__ = ('_buf');

    def __init__(self,buffer = None,offset = 0):
        if buffer != None:
            if isinstance(buffer,BinStruct):
                buffer = buffer._buf;
            self.unpack_from(buffer,offset);
        else:
            self._buf = None;
            self.zero();

    def printer(self,F,offset=0,header=True):
        if header:
            print >> F, "%s"%(self.__class__.__name__);

    def dump(self,F,startBits,endBits,label,offset=0):
        if self._buf is None:
            self._buf = bytearray(256);
            self.pack_into(self._buf);
            self._buf = bytes(self._buf);

        endBits = endBits/8;
        startBits = startBits/8;
        while startBits < endBits:
            print >> F, "% 3u %02X%02X%02X%02X %s"%\
                  (offset + startBits,
                   ord(self._buf[startBits]),ord(self._buf[startBits+1]),
                   ord(self._buf[startBits+2]),ord(self._buf[startBits+3]),
                   label);
            label = '';
            startBits = startBits + 4;

    # 'pure virtual' functions
    def zero(self): return;
    # def unpack_from(self,buffer,offset=0):
    # def pack_into(self,buffer,offset=0):
