Version 0.1 Initial Release
===========================

`March 15, 2011`

I am pleased to announce the initial release of `python-rdma` a package to
provide a Python API for the Linux RDMA stack. This initial release is mainly
focused on IB specific management APIs, but the package also covers ibverbs.

A new API was developed for this library that is designed to take advantage of
Python features and provides a very uniform, integrated design across all
the different aspects of IB and RDMA programming. It has a particular focus on
ease of use and correct operation of the IB and RDMA protocol stacks.

Included is a re-implementation of a substantial portion of the
`infinband-diags` package. This re-implementation is functionally very similar
to `infiniband-diags` but also gains a number of new features:

- Uniform end port addressing. All commands support GID, port GUID, LID and DR
  path, even commands that are GMP based (like perfquery).
- Support for collecting information entirely from the SA via the `--sa`
  option.
- Consistently fetches path records for GMP communication (eg in perfquery) to
  support topologies with special requirements.
- Extensive MAD parallelization provides very good performance.
- All commands support a discovery cache file, which stores information in
  an efficient binary format.
- Much better debugging, including packet tracing down to full field decode.
- Minor new features to many tools, review section 8 of the manual for
  details.

The library itself is intended mainly for applications where quick development
is more important that the highest performance, such as:

- IB manamagent software development
- RDMA test development
- Training and problem exploration

Although already quite complete there are a few obvious areas that I hope
to have finished in the future:

- Integration of IB and RDMA CMs
- Support for RMPP when using verbs to issue GMPs - this will enable
  all diags to function in `--sa` mode without access to /dev/umad.
- Completion of missing `infinband-diags` commands

It is my hope this work will be of use to the wider InfiniBand community.

Extensive prebuilt documentation for the module can be reviewed `online
<http://www.obsidianresearch.com/python-rdma/doc/index.html>`_, and the source
code is available on `GitHub <http://github.com/jgunthorpe/python-rdma>`_.
