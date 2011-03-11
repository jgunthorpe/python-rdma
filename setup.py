#!/usr/bin/env python

import sys
import re
import os.path
from distutils import log
from distutils.core import setup
from distutils.extension import Extension

try:
    import Pyrex.Distutils
except ImportError:
    # If we don't have Pyrex then just use the shipped .c file that is already built.
    ibverbs_module = Extension('rdma.ibverbs', ['rdma/ibverbs.c'],
                               libraries=['ibverbs']);
    from distutils.command.build_ext import build_ext
else:
    class build_ext(Pyrex.Distutils.build_ext):
        def build_extensions(self):
            self.codegen();
            Pyrex.Distutils.build_ext.build_extensions(self);

        def get_enums(self,F):
            s = []
            skip = True
            for I in F.readlines():
                if I[0] == '#':
                    skip = I.find("infiniband/verbs.h") == -1;
                else:
                    if not skip:
                        s.append(I)
            s = "".join(s);

            enum = {}
            for m in re.finditer(r'enum\s+(\w+)\s*{(.*?)}', s, re.DOTALL):
                name = m.group(1)
                constants = [c.partition('=')[0].strip() for c in m.group(2).split(',')]
                enum[name] = tuple(constants)

            return enum

        def write_enums_pxd(self,F,enums):
            print >> F, '\n\n'.join('\n'.join('%s = c.%s' % (c, c) for c in v)
                                    for e,v in sorted(enums.iteritems()))
        def write_enums_pxi(self,F,enums):
            sep = '\n' + ' '*8
            print >> F, '\n\n'.join('    enum %s:%s' % (e,sep) + sep.join(v)
                                    for e,v in sorted(enums.iteritems()));

        def codegen(self):
            verbs_h = os.path.join(self.build_temp,"verbs_h.c")
            verbs_h_o = verbs_h + ".out"
            with open(verbs_h,"wt") as F:
                F.write("#include <infiniband/verbs.h>")
            self.compiler.preprocess(verbs_h,verbs_h_o);

            with open(verbs_h_o) as F:
                enums = self.get_enums(F);
            with open("rdma/libibverbs_enums.pxd","wt") as F:
                print >> F, "cdef extern from 'infiniband/verbs.h':";
                self.write_enums_pxi(F,enums);
            with open("rdma/libibverbs_enums.pxi","wt") as F:
                self.write_enums_pxd(F,enums);

    ibverbs_module = Extension('rdma.ibverbs', ['rdma/ibverbs.pyx'],
                               libraries=['ibverbs'],
                               depends=['rdma/libibverbs.pxd',
                                        'rdma/libibverbs.pxi'])

setup(name='rdma',
      version='0.1',
      description='RDMA functionality for python',
      ext_modules=[ibverbs_module],
      packages=['rdma','libibtool'],
      scripts=['ibtool'],
      cmdclass={'build_ext': build_ext},
      platforms = "ALL",
      classifiers = [
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GPL',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
      ],)
