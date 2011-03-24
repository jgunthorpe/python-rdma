import rdma.IBA as IBA;

class MlxFormat(IBA.VendFormat):
    MAD_CLASS = 10
    MAD_CLASS_VERSION = 1

class MlxClassPortInfo(IBA.MADClassPortInfo):
    MAD_VENDGET = 0x1 # MAD_METHOD_GET
    MAD_VENDSET = 0x2 # MAD_METHOD_SET
    FORMAT = MlxFormat;

class OFASysStatFormat(IBA.VendOUIFormat):
    MAD_CLASS = 0x33
    MAD_CLASS_VERSION = 1
    MAD_CLASS_OUI = 0x001405
    MAD_METHOD_MASK = (1<<IBA.MAD_METHOD_GET) | (1<<IBA.MAD_METHOD_SET);
    def zero(self):
        IBA.VendOUIFormat.zero(self);
        self.OUI = self.MAD_CLASS_OUI;

class OFASysStatClassPortInfo(IBA.MADClassPortInfo):
    MAD_VENDGET = 0x1 # MAD_METHOD_GET
    MAD_VENDSET = 0x2 # MAD_METHOD_SET
    FORMAT = OFASysStatFormat;

def install_vend():
    """Since the vendor MADs can collide we prefer to only setup the dumper
    if they are going to be used."""
    import libibtool.vend as vend;
    formats = set(I[0] for I in vend.ATTR_TO_STRUCT.iterkeys());
    for I in formats:
        vend.ATTR_TO_STRUCT[I,IBA.MADClassPortInfo.MAD_ATTRIBUTE_ID] = IBA.MADClassPortInfo;
        vend.CLASS_TO_STRUCT[I.MAD_CLASS | (getattr(I,"MAD_CLASS_OUI",0) << 8),
                             (IBA.MAD_BASE_VERSION << 8) | I.MAD_CLASS_VERSION] = I;
    IBA.MEMBER_FORMATS.update(vend.MEMBER_FORMATS);
    IBA.ATTR_TO_STRUCT.update(vend.ATTR_TO_STRUCT);
    IBA.CLASS_TO_STRUCT.update(vend.CLASS_TO_STRUCT);
