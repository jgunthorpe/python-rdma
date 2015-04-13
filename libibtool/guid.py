# Copyright 2015 Obsidian Research Corp. GPLv2, see COPYING.
import sys;
from libibtool import *;
from libibtool.libibopts import *;
import rdma.IBA as IBA;

def set_guid(lid,guid,slot):
    rec = IBA.SAGUIDInfoRecord();
    rec_cm = IBA.ComponentMask(rec);
    rec_cm.blockNum = slot//8;
    rec_cm.LID = lid;
    # ComponentMask does not handle this array correctly
    idx = slot - rec.blockNum*8;
    rec.GUIDInfo.GUIDBlock[idx] = IBA.GUID(guid);
    rec_cm.component_mask = rec_cm.component_mask | (1<<(rec.COMPONENT_MASK['GUIDInfo.GUIDBlock'] + idx));
    return rec_cm;

def cmd_set_guid(argv,o):
    """Set an alias guid on the port through the SA
       Usage: %prog TARGET SLOT GUID

       This uses a SubnAdmSet(GUIDInfo) to program an alias GUID on the end port.
    """
    LibIBOpts.setup(o);
    (args,values) = o.parse_args(argv);
    lib = LibIBOpts(o,args,values,3,(tmpl_target,tmpl_int,tmpl_port_guid));

    if len(values) != 3:
        raise CmdError("Not enough arguments");

    with lib.get_umad_for_target(values[0],gmp=True) as umad:
        set_cm = set_guid(lib.path.DLID,values[2],values[1]);
        ret = umad.SubnAdmSet(set_cm,umad.end_port.sa_path);
        ret.printer(sys.stdout);
