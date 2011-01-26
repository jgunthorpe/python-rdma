#!/usr/bin/python
'''This module provides a list of IB devices scrapped from sysfs'''
from __future__ import with_statement;

import rdma.IBA;
import os,stat,socket,re

SYS_INFINIBAND = "/sys/class/infiniband/";

def conv_gid(s):
    return socket.inet_pton(socket.AF_INET6,s);
def conv_guid(s):
    return s.strip();
def conv_hex(s):
    return int(s,16);
def conv_int_desc(s):
    t = s.split(':');
    return (int(t[0]),t[1].strip());

class SysFSCache(object):
    '''Cache queries from sysfs attributes. This class is used to make
    the sysfs parsing demand load.'''
    def __init__(self,dir):
        self._dir = dir;
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

class EndPort(SysFSCache):
    '''A RDMA end port. An end port can issue RDMA operations, has a port GID,
    etc. For an IB switch this will be port 0, for *CA it will be port 1 or
    higher.'''
    def __init__(self,parent,port_id):
        SysFSCache.__init__(self,parent._dir + "ports/%u/"%(port_id));
        self.parent = parent;
        self.port_id = port_id;

    def _iterate_services_device(self,dir,matcher):
        return self.parent._iterate_services_device(dir,matcher);
    def _iterate_services_end_port(self,dir,matcher):
        '''Iterate over all sysfs files that are associated with the
        device and with this end port.'''
        for I in self.parent._iterate_services_device(dir,matcher):
            try:
                with open(I + "/port") as F:
                    if int(F.read()) != self.port_id:
                        continue;
            except IOError:
                continue;
            yield I;

    def get_umad(self):
        '''Return a umad kernel interface associated with this device'''
        for I in self.parent._iterate_services(SYS_INFINIBAND_MAD,"umad\d+"):
            try:
                with open("%s%s/port"%(SYS_INFINIBAND_MAD,I)) as F:
                    if int(F.read()) != self.port_id:
                        continue;
                return UMad(self,SYS_INFINIBAND_MAD + I);
            except IOError:
                pass;
        raise RDMAError("Unable to open umad device for %s"%(repr(self)));

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
    @property
    def gids(self):
        if self._cache.has_key("gids"):
            return self._cache["gids"];
        res = {}
        for I in sorted(int(I) for I in os.listdir(self._dir + "gids/")):
            with open(self._dir + "gids/%u" %(I)) as F:
                s = F.read().strip();
                if s != "fe80:0000:0000:0000:0000:0000:0000:0000":
                    res[I] = conv_gid(s);
        self._cache["gids"] = res;
        return res;
    @property
    def pkeys(self):
        if self._cache.has_key("pkeys"):
            return self._cache["pkeys"];
        res = {}
        for I in sorted(int(I) for I in os.listdir(self._dir + "pkeys/")):
            with open(self._dir + "pkeys/%u" %(I)) as F:
                s = int(F.read(),16);
                if s != 0:
                    res[I] = s;
        self._cache["pkeys"] = res;
        return res;

    def __str__(self):
        return "%s/%u"%(self.parent,self.port_id);

    def __repr__(self):
        return "<%s.%s object for %s at 0x%x>"%\
               (self.__class__.__module__,
                self.__class__.__name__,
                self,
                id(self));

class RDMADevice(SysFSCache):
    NODE_CA = 1;

    def __init__(self,name):
        SysFSCache.__init__(self,SYS_INFINIBAND + name + "/");
        self.name = name;

        # FIXME: For switches this should just be 0, how does that represent
        # in Linux anyhow?
        self.end_ports = [EndPort(self,int(I))
                          for I in os.listdir(self._dir + "ports")];
        self.phys_port_cnt = len(self.end_ports);

    def _iterate_services_device(self,dir,matcher):
        '''Iterate over all sysfs files (ie umad, cm, etc) that are associated
        with this device. Use this to find the sysfs ID of slave kernel
        interface devices.'''
        m = re.compile(matcher);
        for I in os.listdir(dir):
            if not m.match(I):
                continue;
            try:
                with open("%s%s/ibdev"%(dir,I)) as F:
                    if F.read().strip() != self.name:
                        continue;
            except IOError:
                continue;
            yield dir + I;

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
