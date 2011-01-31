#!/usr/bin/python
'''This module provides a list of IB devices scrapped from sysfs'''
from __future__ import with_statement;

import os,socket,re,collections

SYS_INFINIBAND = "/sys/class/infiniband/";

def conv_gid(s):
    """Convert the content of a sysfs GID file to our representation."""
    return socket.inet_pton(socket.AF_INET6,s.strip());
def conv_guid(s):
    """Convert the content of a sysfs GUID file to our representation."""
    return s.strip();
def conv_hex(s):
    """Convert the content of a sysfs hex integer file to our representation."""
    return int(s,16);
def conv_int_desc(s):
    """Convert the content of a sysfs device major:minor file to our representation."""
    t = s.split(':');
    return (int(t[0]),t[1].strip());

class SysFSCache(object):
    '''Cache queries from sysfs attributes. This class is used to make
    the sysfs parsing demand load.'''
    def __init__(self,dir_):
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
    """Demand loading class for things like GID tables and PKey tables"""
    # FIXME: would like to use OrderedDict
    def __init__(self,path,conv,iconv = int):
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
        """Return the index idx such that obj[idx] == value"""
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
    """Like DemandList but conv is a function to call with the idx, not file
    content."""
    def __getitem__(self,idx):
        ret = self._data[idx];
        if ret is None:
            ret = self._conv(idx);
            self._data[idx] = ret;
        return ret;

class EndPort(SysFSCache):
    '''A RDMA end port. An end port can issue RDMA operations, has a port GID,
    etc. For an IB switch this will be port 0, for *CA it will be port 1 or
    higher.'''
    def __init__(self,parent,port_id):
        SysFSCache.__init__(self,parent._dir + "ports/%u/"%(port_id));
        self.parent = parent;
        self.port_id = port_id;
        self.pkeys = DemandList(self._dir + "pkeys/",conv_hex);
        self.gids = DemandList(self._dir + "gids/",conv_gid);

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
    def lid(self): return self._cached_sysfs("lid",conv_hex);
    @property
    def lmc(self): return self._cached_sysfs("lid_mask_count",int);
    @property
    def phys_state(self): return self._cached_sysfs("phys_state",conv_int_desc);
    @property
    def state(self): return self._cached_sysfs("state",conv_int_desc);
    @property
    def sm_lid(self): return self._cached_sysfs("sm_lid",conv_hex);
    @property
    def sm_sl(self): return self._cached_sysfs("sm_sl",int);

    # FIXME This must come from verbs :(
    @property
    def subnet_timeout(self): return 18;

    def pkey_index(self,pkey):
        # FIXME: We don't really need to read all the pkey entries to do
        # this, searching the directory
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
    def __init__(self,name):
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
    def node_type(self): return self._cached_sysfs("node_type",conv_int_desc);
    @property
    def node_guid(self): return self._cached_sysfs("node_guid",conv_guid);
    @property
    def node_desc(self): return self._cached_sysfs("node_desc");
    @property
    def fw_ver(self): return self._cached_sysfs("fw_ver");
    @property
    def sys_image_guid(self): return self._cached_sysfs("sys_image_guid",conv_guid);
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
