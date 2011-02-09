# Describe various IBA constants as strings
import rdma.IBA as IBA;
import rdma.binstruct;

def mad_status(status):
    """Decode a MAD status into a string."""
    res = "";
    if status & IBA.MAD_STATUS_BUSY:
        res = res + "BUSY ";
    if status & IBA.MAD_STATUS_REDIRECT:
        res = res + "REDIECT ";
    code = (status >> 2) & 7;
    if code == 0:
        return res + "Ok";
    if code == 1:
        return res + "Bad version";
    if code == 2:
        return res + "Unsupported method";
    if code == 3:
        return res + "Unsupported method+attr";
    if code == 7:
        return res + "Invalid attr or modifier";
    return res + "??";

def node_type(value):
    """Decode a Node Type *value* into a string."""
    if value == IBA.NODE_CA:
        return "Channel Adaptor"
    if value == IBA.NODE_SWITCH:
        return "Switch"
    if value == IBA.NODE_ROUTER:
        return "Router"
    return "?? %u"%(value);

def description(value):
    """Decodes a fixed length string from a IBA MAD (such as
    :class:`rdma.IBA.SMPNodeDescription`) These strings are considered to be
    UTF-8 and null padding is removed."""
    for I in range(len(value)-1,-1,-1):
        if value[I] != chr(0):
                break;
    return value[:I].decode("UTF-8");

def _array_dump(F,a,buf,mbits,name,offset=0):
    """Dump an array beside the hex values. Each array member is printed
    beside the hex dword that it starts on."""
    cur_dword = 0;
    off = 0
    idx = 0;
    mb = [];
    max_idx = len(a);
    max_dword = (mbits*max_idx)//8;
    while cur_dword < max_dword:
        del mb[:]
        while off < cur_dword*8 + 32 and idx < max_idx:
            off = off + mbits;
            if idx == 0:
                mb.append("%s=[%u:%r"%(name,idx,a[idx]));
            elif idx+1 == max_idx:
                mb.append("%u:%r]"%(idx,a[idx]));
            else:
                mb.append("%u:%r"%(idx,a[idx]));
            idx = idx + 1;

        print >> F, "%3u %02X%02X%02X%02X %s"%\
              (offset + cur_dword,ord(buf[cur_dword]),ord(buf[cur_dword+1]),
               ord(buf[cur_dword+2]),ord(buf[cur_dword+3]),
               ", ".join(mb));
        cur_dword = cur_dword + 4;

def struct_dump(F,s,offset=0,name_prefix=''):
    """Pretty print the structure *s*. *F* is the output file, *offset* is
    added to all printed offsets and name_prefix is used to prefix names
    when descending."""
    buf = None;
    if isinstance(s._buf,bytes):
        buf = s._buf;
    if isinstance(s._buf,bytearray):
        buf = bytes(s._buf);
    if buf is None:
        buf = bytearray(s.MAD_LENGTH);
        s.pack_into(buf);
        buf = bytes(buf);

    idx = 0;
    off = 0;
    mb = [];
    max_idx = len(s.MEMBERS);
    max_dword = len(buf);
    for nz_dword in range(max_dword-1,-1,-1):
        if buf[nz_dword] != '\0':
            break;
    cur_dword = 0;
    while cur_dword < max_dword:
        del mb[:]
        if (idx >= max_idx and cur_dword > nz_dword):
            break;
        while off < cur_dword*8 + 32 and idx < max_idx:
            name,mbits,count = s.MEMBERS[idx];
            bits = mbits*count;
            aligned = (off % 32) == 0 and (bits % 32) == 0;
            off = off + bits;
            idx = idx + 1;
            attr = getattr(s,name);

            if aligned and count == 1:
                # Special automagic decode of format data members based on
                # attribute ID.
                if name == "data" and isinstance(s,rdma.IBA.BinFormat):
                    nattr = IBA.ATTR_TO_STRUCT.get((s.__class__,s.attributeID));
                    if nattr != None:
                        if nattr.MAD_LENGTH <= max_dword - cur_dword:
                            attr = nattr(buf,cur_dword);

                # Recurse into children structs
                if isinstance(attr,rdma.binstruct.BinStruct):
                    print >> F,"   + %s%s %s"%(name_prefix,name,
                                               attr.__class__.__name__)
                    struct_dump(F,attr,cur_dword,
                                name_prefix="%s%s."%(name_prefix,name));
                    cur_dword = cur_dword + bits//8;
                    if cur_dword >= max_dword:
                        return
                    print >> F,"   - %s%s"%(name_prefix,name)
                    continue;

            # Handle aligned arrays by pretty printing the array
            if aligned and count != 1 and count == len(attr):
                # Handle arrays of structures
                if isinstance(attr[0],rdma.binstruct.BinStruct):
                    for I,v in enumerate(attr):
                        print >> F,"   + %s%s[%u] %s"%(
                            name_prefix,name,I,v.__class__.__name__);
                        struct_dump(F,v,cur_dword,
                                    name_prefix="%s%s[%u]."%(
                                        name_prefix,name,I));
                        cur_dword = cur_dword + bits//8;
                    if cur_dword >= max_dword:
                        return
                    print >> F,"   - %s%s"%(name_prefix,name)
                    continue;

                _array_dump(F,attr,buf,mbits,name,offset=cur_dword);
                cur_dword = cur_dword + bits//8;
                continue;

            if aligned:
                # Not much sense in printing bytes we can see in hex.
                if isinstance(attr,bytearray):
                    mb.append("%s=<%u bytes>"%(name,bits/8));
                    continue;
            mb.append("%s=%r"%(name,getattr(s,name)));

        if cur_dword >= max_dword:
            return

        print >> F, "%3u %02X%02X%02X%02X %s"%\
              (offset + cur_dword,ord(buf[cur_dword]),ord(buf[cur_dword+1]),
               ord(buf[cur_dword+2]),ord(buf[cur_dword+3]),
               ",".join(mb));
        cur_dword = cur_dword + 4;

def struct_dotted(F,s,name_prefix='',dump_list=False,skip_reserved=True):
    """This tries to emulate the libib structure print format. Members are
    printed one per line with values aligned on column 32."""
    for name,mbits,count in s.MEMBERS:
        if skip_reserved and name.startswith("reserved_"):
            continue;
        attr = getattr(s,name);
        cname = name[0].upper() + name[1:];

        # Special automagic decode of format data members based on
        # attribute ID.
        if name == "data" and isinstance(s,rdma.IBA.BinFormat):
            nattr = IBA.ATTR_TO_STRUCT.get((s.__class__,s.attributeID));
            if nattr != None:
                if nattr.MAD_LENGTH <= len(attr):
                    attr = nattr(attr);

        if isinstance(attr,rdma.binstruct.BinStruct):
            struct_dotted(F,attr,"%s%s."%(name_prefix,name));
            continue;

        fmt = "%r";
        if count != 1 and len(attr) == count:
            if isinstance(attr[0],rdma.binstruct.BinStruct):
                for I,v in enumerate(attr):
                    struct_dotted(F,v,"%s%s[%u]."%(name_prefix,name,I));
                continue;

            if mbits > 16 or dump_list:
                for I,v in enumerate(attr):
                    n = "%s%s[%u]."%(name_prefix,cname,I);
                    print >> F, ("%s%s"+fmt)%(n,"."*(32-len(n)),v);
                continue;
            else:
                attr = "[%s]"%(", ".join(("%u:"+fmt)%(I,v) for I,v in enumerate(attr)));
                fmt = "%s";

        n = "%s%s"%(name_prefix,cname);
        print >> F, ("%s%s"+fmt)%(n,"."*(32-len(n)),attr);
