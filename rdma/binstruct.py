# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
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
    '''Base class for all binary structure objects (MADs, etc). When pickled
    this class re-packs the structure and stores it as a `bytes` value. This
    reduces the storage overhead from pickling and allows the library to
    upgrade to different internal storage methods in future.'''
    __metaclass__ = abc.ABCMeta;
    __slots__ = ();

    def __init__(self,buf = None,offset = 0):
        """*buf* is either an instance of :class:`BinStruct` or a :class:`bytes`
        representing the data to unpack into the instance. *offset* is the
        starting offset in *buf* for unpacking. If no arguments are given then
        all attributes are set to 0."""
        if buf is not None:
            if isinstance(buf,BinStruct):
                buf = bytearray(buf.MAD_LENGTH);
                s.pack_into(buf);
            if isinstance(buf,bytearray):
                self.unpack_from(bytes(buf),offset);
            else:
                self.unpack_from(buf,offset);
        else:
            self.zero();

    def printer(self,F,offset=0,header=True,format="dump",**kwargs):
        """Pretty print the structure. *F* is the output file, *offset* is
        added to all printed offsets and *header* causes the display of the
        class type on the first line. *format* may be `dump` or `dotted`."""
        if header:
            print >> F, "%s"%(self.__class__.__name__);
        import rdma.IBA_describe;
        if format == "dotted":
            return rdma.IBA_describe.struct_dotted(F,self,**kwargs);
        return rdma.IBA_describe.struct_dump(F,self,offset=offset,**kwargs);

    def __reduce__(self):
        """When pickling, store in packed format. This gives us greater
        flexability across versions of the library and takes less space."""
        buf = bytearray(self.MAD_LENGTH);
        self.pack_into(buf);
        return (self.__class__,(bytes(buf),));

    # 'pure virtual' functions
    def zero(self):
        """Overridden in derived classes. Set this instance back to the
        initial all zeros value."""
        return
    @abc.abstractmethod
    def unpack_from(self,buf,offset=0):
        """Overridden in derived classes. Expand the :class:`bytes` *buf*
        starting at *offset* into this instance."""
        pass
    @abc.abstractmethod
    def pack_into(self,buf,offset=0):
        """Overridden in derived classes. Compact this instance into the
        :class:`bytearray` *buf* starting at *offset*."""
        pass

class BinFormat(BinStruct):
    '''Base class for all `*Format` type packet layouts.'''
    def describe(self):
        '''Return a short description of the RPC described by this format.'''
        import rdma.IBA as IBA
        attr = IBA.ATTR_TO_STRUCT.get((self.__class__,self.attributeID));
        return '%s %s(%u.%u) %s(%u)'%(IBA.const_str('MAD_METHOD_',self.method,True),
                                      self.__class__.__name__,
                                      self.mgmtClass,self.classVersion,
                                      '??' if attr is None else attr.__name__,
                                      self.attributeID);
