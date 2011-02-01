#!/usr/bin/python
'''This module provides a list of IB devices scrapped from sysfs'''
from __future__ import with_statement;

import rdma;
import rdma.IBA as IBA;
import os,re,collections

SYS_INFINIBAND = "/sys/class/infiniband/";

def _conv_gid2guid(s):
    """Return the GUID portion of a GID string.

    :raises ValueError: If the string is invalid."""
    return IBA.GID(s).guid();
def _conv_hex(s):
    """Convert the content of a sysfs hex integer file to our representation.

    :raises ValueError: If the string is invalid."""
    return int(s,16);
def _conv_int_desc(s):
    """Convert the content of a sysfs file that has a format %u:%s, the %s is
    the descriptive name for the integer.

    :raises ValueError: If the string is invalid."""
    t = s.split(':');
    if len(t) != 2:
        raise ValueError("%r is not a valid major:minor"%(s));
    return (int(t[0]),t[1].strip());

class SysFSCache(object):
    '''Cache queries from sysfs attributes. This class is used to make
    the sysfs parsing demand load.'''
    def __init__(self,dir_):
        '''*dir_* is the directory the attributes reside in.'''
        self._dir = dir_;
        self._cache = {};

    def _cached_sysfs(self,name,convert = None):
        '''Read, cache and return the value from sysfs'''
        if self._cache.has_key(name):
            return self._cache[name];
        with open(self._dir + name) as F:
            s = F.read();
            if convert:
                s = convert(s);
            else:
                s = s.strip();
            self._cache[name] = s;
            return s;

class DemandList(collections.Iterable):
    """Present an ordered list interface with a non-integer index for
    a set of values that are demand created. The list indexes must be known
    in advance."""
    # FIXME: would like to use OrderedDict
    def __init__(self,path,conv,iconv = int):
        """The indexes are computed as::

             sorted(iconv(I) for I in os.listdir(path))

        *conv* is called to convert the contents of each file in *path*
        to the python representation."""
        self._path = path;
        self._conv = conv;
        self._data = {};
        self._okeys = tuple(sorted(iconv(I) for I in os.listdir(path)));
        for I in self._okeys:
            self._data[I] = None;

    def __len__(self): return len(self._data);
    def __iter__(self):
        """This class isn't a dictionary, it is an ordered list with maybe non
        integer indexes. So we are returning values not keys."""
        for I in self._okeys:
            yield self[I];
    def valuesiter(self): return self.__iter__();
    def keysiter(self): return self._okeys.__iter__();

    def first(self):
        """Return the first element of the list"""
        return self[self._okeys[0]];

    def __getitem__(self,idx):
        ret = self._data[idx];
        if ret is None:
            with open(self._path + "%s"%(idx)) as F:
                ret = self._conv(F.read());
                self._data[idx] = ret;
        return ret;

    def index(self,value):
        """Return the index idx such that ``obj[idx] == value``."""
        for k,v in self._data.iteritems():
            if v == value:
                return k;

        for I in self._okeys:
            if self[I] == value:
                return I;
        raise ValueError("DemandList.index(x): x not in list");

    def __repr__(self):
        return "{%s}"%(", ".join("%r: %r"%(k,self[k]) for k in self._okeys));

class DemandList2(DemandList):
    """Like :class:`DemandList` but *conv* is a function to call with the idx,
    not file content. This is useful for cases where the *path* argument to
    :meth:`__init__` points to a list of directories."""
    def __getitem__(self,idx):
        ret = self._data[idx];
        if ret is None:
            ret = self._conv(idx);
            self._data[idx] = ret;
        return ret;

class EndPort(SysFSCache):
    '''A RDMA end port. An end port can issue RDMA operations, has a port GID,
    LID, etc. For an IB switch this will be port 0, for a \*CA it will be port
    1 or higher.'''
    def __init__(self,parent,port_id):
        """*parent* is the owning :class:`RDMADevice` and port_id is the port
        ID number, 0 for switches and > 1 for \*CAs"""
        SysFSCache.__init__(self,parent._dir + "ports/%u/"%(port_id));
        self.parent = parent;
        self.port_id = port_id;
        self.pkeys = DemandList(self._dir + "pkeys/",_conv_hex);
        self.gids = DemandList(self._dir + "gids/",IBA.GID);

    def _iterate_services_device(self,dir_,matcher):
        return self.parent._iterate_services_device(dir_,matcher);
    def _iterate_services_end_port(self,dir_,matcher):
        '''Iterate over all sysfs files that are associated with the
        device and with this end port.'''
        for I in self.parent._iterate_services_device(dir_,matcher):
            try:
                with open(I + "/port") as F:
                    if int(F.read()) != self.port_id:
                        continue;
            except IOError:
                continue;
            yield I;

    @property
    def lid(self): return self._cached_sysfs("lid",_conv_hex);
    @property
    def lmc(self): return self._cached_sysfs("lid_mask_count",int);
    @property
    def phys_state(self): return self._cached_sysfs("phys_state",_conv_int_desc);
    @property
    def state(self): return self._cached_sysfs("state",_conv_int_desc);
    @property
    def sm_lid(self): return self._cached_sysfs("sm_lid",_conv_hex);
    @property
    def sm_sl(self): return self._cached_sysfs("sm_sl",int);
    @property
    def port_guid(self): return self._cached_sysfs("gids/0",_conv_gid2guid);

    # FIXME This must come from verbs :(
    @property
    def subnet_timeout(self): return 18;

    def pkey_index(self,pkey):
        """Return the ``pkey index`` for pkey value *pkey*."""
        return self.pkeys.index(pkey);

    def __str__(self):
        return "%s/%u"%(self.parent,self.port_id);

    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self,
                id(self));

class RDMADevice(SysFSCache):
    """A RDMA device. A device has at least one end port. The main significance of
    a RDMA device in the API is to indicate that multiple end ports can
    share a single protection domain."""
    def __init__(self,name):
        """*name* is the kernel's name for this device in sysfs."""
        SysFSCache.__init__(self,SYS_INFINIBAND + name + "/");
        self.name = name;

        self.end_ports = DemandList2(self._dir + "ports/",
                                     lambda x:EndPort(self,x));
        self.phys_port_cnt = len(self.end_ports);

    def _iterate_services_device(self,dir_,matcher):
        '''Iterate over all sysfs files (ie umad, cm, etc) that are associated
        with this device. Use this to find the sysfs ID of slave kernel
        interface devices.'''
        m = re.compile(matcher);
        for I in os.listdir(dir_):
            if not m.match(I):
                continue;
            try:
                with open("%s%s/ibdev"%(dir_,I)) as F:
                    if F.read().strip() != self.name:
                        continue;
            except IOError:
                continue;
            yield dir_ + I;

    @property
    def node_type(self): return self._cached_sysfs("node_type",_conv_int_desc);
    @property
    def node_guid(self): return self._cached_sysfs("node_guid",IBA.GUID);
    @property
    def node_desc(self): return self._cached_sysfs("node_desc");
    @property
    def fw_ver(self): return self._cached_sysfs("fw_ver");
    @property
    def sys_image_guid(self): return self._cached_sysfs("sys_image_guid",IBA.GUID);
    @property
    def board_id(self): return self._cached_sysfs("board_id");
    @property
    def hw_ver(self): return self._cached_sysfs("hw_rev");

    def __str__(self):
        return self.name;
    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self,
                id(self));

def find_port_gid(devices,gid):
    """Search the list *devices* for the end port with *gid*.

    :returns: (:class:`EndPort`,gid_index)
    :raises rdma.RDMAError: If no matching device is found."""
    for I in devices:
        for J in I.end_ports:
            try:
                return (J,J.gids.index(gid));
            except ValueError:
                continue;
    raise rdma.RDMAError("RDMA End port %r not found."%(gid));

def find_port_guid(devices,guid):
    """Search the list *devices* for the end port with *guid*.

    :rtype: :class:`EndPort`
    :raises rdma.RDMAError: If no matching device is found."""
    for I in devices:
        for J in I.end_ports:
            if J.port_guid == guid:
                return J;
    raise rdma.RDMAError("RDMA End port %r not found."%(guid));

def find_port_name(devices,name):
    """Search the list *devices* for the end port with *name* and *name* may
    be a device name in which case the first end port is returned, otherwise
    it may be device/port.

    :rtype: :class:`EndPort`
    :raises rdma.RDMAError: If no matching device is found."""
    parts = name.split('/');
    try:
        device = devices[parts[0]];
    except KeyError:
        raise rdma.RDMAError("RDMA device %r not found."%(name));

    if len(parts) == 1:
        return device.end_ports.first();
    if len(parts) != 2:
        raise rdma.RDMAError("Invalid end port specification %r"%(name));

    try:
        idx = int(parts[1]);
    except ValueError:
        raise rdma.RDMAError("Invalid end port specification %r"%(name));

    try:
        return device.end_ports[idx];
    except KeyError:
        raise rdma.RDMAError("RDMA device %r port %u not found."%(parts[0],idx));
