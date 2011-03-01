#! /usr/bin/python

from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext

ibverbs_module = Extension('rdma.ibverbs', ['rdma/ibverbs.pyx'],
                           libraries=['ibverbs'])

setup(name='rdma',
      version='0.1',
      description='RDMA functionality for python',
      ext_modules=[ibverbs_module],
      packages=['rdma','libibtool'],
      scripts=['ibtool'],
      cmdclass={'build_ext': build_ext})
