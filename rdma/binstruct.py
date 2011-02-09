#!/usr/bin/python
import rdma;
import abc;

# FIXME
def pack_array8(buf,offset,mlen,count,inp):
    return
    raise rdma.RDMAError("Not implemented");
def unpack_array8(buf,offset,mlen,count,inp):
    """Starting at *offset* in *buf* assign *count* entries each *mlen* bits
    wide to indexes in *inp*."""
    # Sigh, so much overhead..
    val = int(buf[offset:offset+(mlen*count)/8].encode("hex"),16);
    for I in range(count):
        inp[I] = (val >> ((count - 1 - I)*mlen)) & ((1 << mlen) - 1);
    return

class BinStruct(object):
    '''Base class for all binary structure objects (MADs, etc)'''
    __metaclass__ = abc.ABCMeta;
    __slots__ = ('_buf');

    def __init__(self,buf = None,offset = 0):
        """*buf* is either an instance of :class:`BinStruct` or a :class:`bytes`
        representing the data to unpack into the instance. *offset* is the
        starting offset in *buf* for unpacking. If no arguments are given then
        all attributes are set to 0."""
        if buf is not None:
            if isinstance(buf,BinStruct):
                buf = buf._buf;
            if isinstance(buf,bytearray):
                self.unpack_from(bytes(buf),offset);
            else:
                self.unpack_from(buf,offset);
        else:
            self._buf = None;
            self.zero();

    def printer(self,F,offset=0,header=True):
        """Pretty print the structure. *F* is the output file, *offset* is
        added to all printed offsets and *header* causes the display of the
        class type on the first line."""
        if header:
            print >> F, "%s"%(self.__class__.__name__);
        import rdma.IBA_describe;
        rdma.IBA_describe.struct_dump(F,self,offset=offset);

    # 'pure virtual' functions
    def zero(self):
        """Overridden in derived classes. Set this instance back to the
        initial all zeros value."""
        return
    @abc.abstractmethod
    def unpack_from(self,buf,offset=0):
        """Overriden in derived classes. Expand the :class:`bytes` *buf*
        starting at *offset* into this instance."""
        pass
    @abc.abstractmethod
    def pack_into(self,buf,offset=0):
        """Overriden in derived classes. Compact this instance into the
        :class:`bytearray` *buf* starting at *offset*."""
        pass
