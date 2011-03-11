Installing
==========

`python-rdma` relies on the standard python :mod:`distutils` functionality for
building and includes a `setup.py` script. The following will be required to
build the module:

- `Python` 2.6 or later in the 2.x series. `Python` 3 is currently not
  supported.
- A working C compiler that distutils can find
- `infiniband/verbs.h` must be in the compiler search path
- The C compiler must be able to link against `libibverbs`
- `Python` C development support must be installed (eg `python-dev` on Debian)

The build process is simply::

 $ ./setup.py build
 [..]

Once built the library can be tested without installation by setting
`PYTHONPATH`::

 $ export PYTHONPATH=`pwd`/lib.*/
 $ ./ibtool help

To install into `/usr/local/` use `./setup.py install`.

If your system has IB libraries installed outside the system path, perform the
build similar to the following::

 $ ./setup.py build_ext -I /opt/ofa64-1.5.1/include -L /opt/ofa64-1.5.1/lib/ --rpath=/opt/ofa64-1.5.1/lib
 $ ./setup.py build

.. note::
 `Python` 2.6 packages are available for RHEL and related via the Fedora
 EPEL_. These packages perform a parallel install of `Python` and do not replace
 the system version. Eg
 http://download.fedora.redhat.com/pub/epel/5/x86_64/repoview/python26.html

.. _EPEL: http://fedoraproject.org/wiki/EPEL

For Development
---------------

The module ships with a few pre-built things, to do development work the
following will also be required:

- Pyrex >= 0.9.9
- Sphinx >= 0.6.6

To test the installation of the above tools do the following::

 $ rm rdma/ibverbs.c
 $ ./setup.py build docs

To ease development I recommend installing the following symlink::

 $ (cd rdma ; ln -s ../build/lib.*/rdma/ibverbs.so .)

After which running Python programs from the top of the source tree will
automatically have the correct PYTHONPATH and changes to the source itself
will immediately be picked up without having to run `./setup.py build`

However, be aware that changes to the `Pyrex` extension module will still
require running `./setup.py build_ext` to recompile.

The two required modules are easily configured in a private user directory as
follows::

 $ wget http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/Pyrex-0.9.9.tar.gz
 $ wget http://pypi.python.org/packages/2.6/S/Sphinx/Sphinx-1.0.7-py2.6.egg#md5=a547658740040dd87ef71fbf723e7962
 $ tar -xzf Pyrex-0.9.9.tar.gz
 $ ln -s Pyrex-0.9.9/Pyrex .
 $ unzip Sphinx-1.0.7-py2.6.egg
 $ export PYTHONPATH=`pwd`

Other approaches are possible as well.

Test Suite
~~~~~~~~~~

The library includes a test suite built with :mod:`unittest`. To run the test
suite the end port returned by :func:`rdma.get_end_port` must be connected to
a small fabric. Some ways of running the suite::

 $ ./run-tests.py                # Run everything
 $ ./run-tests.py tests.verbs    # Only run the verbs test.

