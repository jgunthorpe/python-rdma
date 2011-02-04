# Describe various IBA constants as strings
import rdma.IBA as IBA;

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

def description(value):
    """Decodes a fixed length string from a IBA MAD (such as
    :class:`rdma.IBA.SMPNodeDescription`) These strings are considered to be
    UTF-8 and null padding is removed."""
    for I in range(len(value)-1,-1,-1):
        if value[I] != chr(0):
                break;
    return value[:I].decode("UTF-8");
