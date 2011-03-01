#! /usr/bin/python

from collections import namedtuple

finfo = namedtuple('finfo', 'type mask')
def struct(name, fields):
    def init(self, **args):
        for k in args:
            if k not in self._finfo.keys():
                raise TypeError("%s() got an unexpected keyword argument '%s'" %
                                (name, k))
        mask = 0
        self.MASK = 0
        for k, f in self._finfo.items():
            if k in args:
                v = args[k]
                mask |= f.mask
            elif callable(f.type):
                v = f.type()
            else:
                v = f.type
            setattr(self, k, v)

        self.MASK = mask

    def sattr(self, k, v):
        if k != 'MASK' and k not in self._finfo.keys():
            raise AttributeError("'%s' object has no attribute '%s'" % (name, k))

        object.__setattr__(self, k, v)
        if k != 'MASK':
            f = self._finfo[k]
            object.__setattr__(self, 'MASK', self.MASK | f.mask)

    def pretty(self):
        L = []
        for k, f in self._finfo.items():
            s = "%s=%s" % (k, getattr(self, k))
            if self.MASK & f.mask:
                s += '*'
            L.append(s)
        return ','.join(L)

    d = {
        '_finfo': dict((f[0], finfo(f[1], f[2] if len(f) > 2 else 0))
                      for f in fields),
        '__init__': init,
        '__setattr__': sattr,
        '__str__': pretty
    }
    return type(name, (object,), d)
