.. Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

Foreword
========

`python-rdma` is a project intended to bring IB and RDMA capabilities to the
Python language. The main focus is not on high performance communication but
rather on effective and *correct* use of the IB and RDMA protocol stacks.

Primarily `python-rdma` is well suited for areas where quick development is
much more important than high performance:

- IB management software development. This is a significant strength of the
  module, which incorporates nearly the complete set of management protocols
  from the IBA specification. Much of the common errors and complexity in
  management processing (eg byte order, bit slicing, etc) is eliminated
  through the extensive use of code generation and full structure unpacking.
  The sophisticated introspection system allows very flexible and
  comprehensive processing of IBA defined management structures.
- Test development. The simplicity and comprehensiveness of the library can
  greatly speed development of management and verbs protocol test
  suites. Several bugs were found and patched in the OFA stack just during the
  development of the library's internal test suite.
- Training and problem exploration. Although the interface is quite different
  from the C APIs the general concepts flow over, and the Python bindings can
  be used without burdensome explicit error handling.

I also feel it is an fairly comprehensive exploration of an alternative and
more integrated API design for IB and RDMA programming. Although several of
the constructs are very Python specific, much of the overall organization and
principles can carry over to other languages. I feel it would be very
interesting to attempt to port the general API to C++, where ease of use and
high performance could be combined.

This documentation set attempts to be a complete exploration of the
`python-rdma` module's capabilities and APIs, but it does assume the reader
has significant pre-existing knowledge of the InfiniBand Architecture (IBA)
and OFA RDMA Verbs programming and principles.

Comparison to the OFA C API
---------------------------

For reference the `python-rdma` module covers the same areas as the following
OFA code:

================ =====================================================
OFA Module       Python-rdma
================ =====================================================
libibmad         Near 100% coverage via :mod:`rdma.madtransactor` and
                 :mod:`rdma.IBA`
libibumad        100% coverage via :mod:`rdma.umad`
libibverbs       100% coverage via :mod:`rdma.ibverbs` (through Cython)
libibnetdisc     ~80% coverage. No support for switch chassis grouping.
librdmacm        Not covered
libibcm          Not covered
infiniband-diags 45 commands re-implemented, 2 un-implemented.
                 Review :ref:`ibtool`
ibutils          Good coverage of the internal APIs but no
                 coverage for the user tools.
perftest	 `rdma_bw` is implemented as an example.
================ =====================================================

Other than :mod:`rdma.ibverbs` all of the module is written in pure Python.
