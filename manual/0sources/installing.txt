.. Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

Installing
==========

`python-rdma` relies on the standard Python :mod:`distutils` functionality for
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

 $ export PYTHONPATH=`pwd`/build/lib.*/
 $ ./ibtool help

To install into `/usr/local/` use `./setup.py install`.

.. note:: Due to how Python searches for libraries the *PYTHONPATH*
 environment variable is still required to run the executable scripts, such as
 the test suite, included in the package.

If your system has IB libraries installed outside the system path, you need to
create a setup.cfg similar to the following::

 [build_ext]
 include-dirs=/opt/ofa64-1.5.1/include
 library-dirs=/opt/ofa64-1.5.1/lib
 rpath=/opt/ofa64-1.5.1/lib

Prior to running `./setup.py build`.

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

- Cython >= 0.21
- Sphinx >= 0.6.6

To test the installation of the above tools do the following::

 $ rm rdma/ibverbs.c
 $ ./setup.py build docs

To ease development I recommend installing the following symlink::

 $ (cd rdma ; ln -s ../build/lib.*/rdma/ibverbs.so .)

After which running Python programs from the top of the source tree will
automatically have the correct PYTHONPATH and changes to the source itself
will immediately be picked up without having to run `./setup.py build`

However, be aware that changes to the extension module will still
require running `./setup.py build_ext` to recompile.

The two required modules are easily configured in a private user directory as
follows::

 $ pip install --user Cython
 $ pip install --user Sphinx

Other approaches are possible as well.

Test Suite
~~~~~~~~~~

The library includes a test suite built with :mod:`unittest`. To run the test
suite the end port returned by :func:`rdma.get_end_port` must be connected to
a small fabric. Some ways of running the suite::

 $ ./run-tests.py                # Run everything
 $ ./run-tests.py tests.verbs    # Only run the verbs test.

.. note::
 The test suite exercises functionality that is known to make OpenSM crash.
 As of this writing OpenSM GIT has been fixed but the latest release (3.3.9)
 does not include the fix.
