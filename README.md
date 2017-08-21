
Python-rdma is an open source project that provides an interface to the Linux
RDMA stack from the Python language.

t is an amalgamation of the functionality contained in the Open Fabrics
Alliance packages libibmad, libibumad, libibverbs, libibnetdisc and
infiniband-diags.

A new API was developed for this library that is designed to take advantage of
Python features and provides a very uniform, integrated design across all the
different aspects of IB and RDMA programming. It has a particular focus on
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

The module is written entirely in Python and only relies on external system
libraries to provide ibverbs functionality.

# Documentation

Review the [documentation](manual/).

Watch the [OFA 2011 presentation](https://youtu.be/eew3r9gQ7iU) and read the
slide [deck](ofa-2011-slides/).

# Release Announcement
