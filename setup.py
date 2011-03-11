#!/usr/bin/env python

import sys
import re
import os.path
from distutils import log
from distutils.core import setup
from distutils.core import Command
from distutils.extension import Extension

try:
    import Pyrex.Distutils
except ImportError:
    log.info("Pyrex is not installed -- using shippped Pyrex output");
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
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)
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

# From PyCA
class sphinx_build(Command):
    description = 'build documentation using Sphinx'
    user_options = [
      ('builder=', 'b', 'builder to use; default is html'),
      ('all', 'a', 'write all files; default is to only write new and changed files'),
      ('reload-env', 'E', "don't use a saved environment, always read all files"),
      ('out-dir=', 'o', 'path where output is stored (default: doc/<builder>)'),
      ('cache-dir=', 'd', 'path for the cached environment and doctree files (default: outdir/.doctrees)'),
      ('conf-dir=', 'c', 'path where configuration file (conf.py) is located (default: same as source-dir)'),
      ('set=', 'D', '<setting=value> override a setting in configuration'),
      ('no-color', 'N', 'do not do colored output'),
      ('pdb', 'P', 'run Pdb on exception'),
    ]
    boolean_options = ['all', 'reload-env', 'no-color', 'pdb']

    def initialize_options(self):
        self.sphinx_args = []
        self.builder = None
        self.all = False
        self.reload_env = False
        self.out_dir = None
        self.cache_dir = None
        self.conf_dir = None
        self.set = None
        self.no_color = False
        self.pdb = False
        self.build = None
        self.build_lib = None

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_lib', 'build_lib'));
        self.sphinx_args.append('sphinx-build')

        if self.builder is None:
            self.builder = 'html'
        self.sphinx_args.extend(['-b', self.builder])

        if self.all:
            self.sphinx_args.append('-a')
        if self.reload_env:
            self.sphinx_args.append('-E')
        if self.no_color or ('PS1' not in os.environ and 'PROMPT_COMMAND' not in os.environ):
            self.sphinx_args.append('-N')
        if not self.distribution.verbose:
            self.sphinx_args.append('-q')
        if self.pdb:
            self.sphinx_args.append('-P')

        if self.cache_dir is not None:
            self.sphinx_args.extend(['-d', self.cache_dir])
        if self.conf_dir is not None:
            self.sphinx_args.extend(['-c', self.conf_dir])
        if self.set is not None:
            self.sphinx_args.extend(['-D', self.set])

        self.source_dir = "doc";
        if self.out_dir is None:
            self.out_dir = os.path.join('doc', self.builder)

        self.sphinx_args.extend([self.source_dir, self.out_dir])

    def run(self):
        try:
            import sphinx
        except ImportError:
            log.info('Sphinx not installed -- skipping documentation. (%s)', sys.exc_info()[1])
            return

        if not os.path.exists(self.out_dir):
            if self.dry_run:
                self.announce('skipping creation of directory %s (dry run)' % self.out_dir)
            else:
                self.announce('creating directory %s' % self.out_dir)
                os.makedirs(self.out_dir)
        if self.dry_run:
            self.announce('skipping %s (dry run)' % ' '.join(self.sphinx_args))
        else:
            self.announce('running %s' % ' '.join(self.sphinx_args))
            opath = sys.path
            try:
                # We need to point Sphinx at the built library, including
                # the extension module so that autodoc works properly.
                sys.path.insert(0,self.build_lib)
                sphinx.main(self.sphinx_args)
            finally:
                sys.path = opath;

setup(name='rdma',
      version='0.1',
      description='RDMA functionality for python',
      ext_modules=[ibverbs_module],
      packages=['rdma','libibtool'],
      scripts=['ibtool'],
      cmdclass={'build_ext': build_ext,
                'docs': sphinx_build},
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
