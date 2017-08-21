=============
 Python RDMA
=============

This package contains the Python module `rdma` which provides a Python API for
the Linux RDMA stack. It is an amalgamation of the functionality contained in
the Open Fabrics Alliance packages `libibmad`, `libibumad`, `libibverbs`,
`libibnetdisc` and `infiniband-diags`.

A new API was developed for this library that is designed to take advantage of
Python features and provides a very uniform, integrated design across all
the different aspects of IB and RDMA programming. It has a particular focus on
ease of use and correct operation of the IB and RDMA protocol stacks.

The module is written entirely in Python and only relies on external
system libraries to provide ibverbs functionality.

Prebuilt documentation for the module can be reviewed `online
<https://jgunthorpe.github.io/python-rdma/manual/>`_, and the source
code is available on `GitHub <https://github.com/jgunthorpe/python-rdma>`_.

`python-rdma` is maintained by Obsidian Research Corp. and the main contact
for the package is Jason Gunthorpe <jgunthorpe@obsidianresearch.com>
