The ``ibtool`` Program
**********************

``ibtool`` collects a number of pre-existing diagnostic utilities, rewritten
to use ``python-rdma`` under one program. The rewrites serve as both test cases
for the library and programming examples for proper library usage. In general
the programs strive to be close to the originals but there are many subtle
differences.

.. note::
  'libib' in the context of this document refers to the C/Bash/Perl/etc
  versions of the ibtools commands based on libib that are being cloned in
  this implementation.

Addressing
==========

``ibtool`` uses the functions in `python-rdma` for processing address
arguments, and removes much of the artificial specificity required by the
original tools.

End Port to Use
---------------

Most tools require an end port to operate on. The libib mechanism involves
specifying the device name and port number with two seperate arugments. This
is still supported but the port argument now accepts a full end port
specifier:

      =========== ===================
      Format      Example
      =========== ===================
      device      mlx4_0  (defaults to the first port)
      device/port mlx4_0/1
      Port GID    fe80::2:c903:0:1491
      Port GUID   0002:c903:0000:1491
      =========== ===================

So the device argument is not required, and its use discouraged. The device
argument will also accept a node GUID to reference the device.

As with the legacy tools the default end port is the first end port in the
system.

Target End Port Address
-----------------------

Most of the commands will operate on a remote port, this requires doing a MAD
RPC from the local end port to the remote. Commands accept a uniform format
for specifying the target end port

      =========== ===================
      Format      Example
      =========== ===================
      Port GID    fe80::2:c903:0:1491
      Port GUID   0002:c903:0000:1491
      LID         12 (decimal)
      DR Path     0,1  (the thing connected to port 1)
      =========== ===================

The directed route (DR) path option allows specifying a directed route path,
the value ``0,`` is the local end port, ``0,1`` is the thing connected to port
1 of the local end port, etc.

The formats for each type are unambiguous, so the prorgam simply determines
the correct entry automatically, legacy options specifying the type are
supported and the command fails if the provided argumen does not match.

When a directed route or LID is specified it is used as-is for sending SMPs.
If a GMP is required then the address is resolved to a full path using the SA.
Resolving a directed route to a GMP path is done using
a series of :class:`rdma.IBA.SALinkRecord` RPCs.


Error Handling
==============

The tool relies on python-rdma's exception system for end user error
reporting. This system provides a great level of detail for most user visible
errors. The -v option is used to increase the error diagnostic output,
up to including packet dumps for failing MADs.

Discovery
=========

Tools which require topology discovery use the :class:`rdma.subnet.Subnet`
information database, which has several different methods for collecting the
data, including DR, LID SMP and from the SA. Everything uses the parallel
MAD scheduler for loading the databases.

Currently the discovery has no error recovery, so it will blow up ungracefully
if MADs can't traverse links they are supposed to, or LIDs don't work.

Notable Differences
===================

Compared to the libib versions:

* The internal library relies less on DR queries to the local port to get
  information - instead this comes from sysfs. This makes MKey enforcement more
  usable.
* Greater consistency. All GIDs are printed and accepted in IPv6 format, GUIDs
  are printed and accepted in three colon GUID format (eg
  0002:c903:0000:1492), and unicast LIDs are printed in decimal format. LIDs
  are accepted as explicit hex (0x1a) or decimal arguments. Hex is uniformly
  lower case and when zero justified the number of zeros used is correct for
  the width of the type.
* The output of some commands is subtly different, ie commands that used to
  print inconsistent output (hex LIDs, hex GUIDs, etc) print in cannonical
  format
* Path record queries are always done for LID target end ports when using GMP,
  the correct SL to use is never assumed.
* A broader range of input is accepted for most arguments (ie GIDs, GUIDs, DR
  paths, etc) and the input argument type is unambigously determined by
  format.
* Debug output is quite different and dramatically better.
* Error output is different and dramatically better. More -v's provide more
  detail down to decoded packet dumps of the erroring MAD::

    E: RPC MAD_METHOD_GET(1) SMPFormatDirected(129.1) SMPPortInfo(21) timed out to 'DR Path (0, 1, 4)'

  vs::

    ibwarn: [2018] mad_rpc: _do_madrpc failed; dport (DR path slid 65535; dlid 65535; 0,1,4)
    ibaddr: iberror: failed: can't resolve requested address

* All commands support the `--sa` option which causes SMPs to be converted
  into SA record queries and sent to the SA. (see
  :class:`rdma.satransacator.SATransactor`) In `--sa` mode no SMPs are
  issued. Some commands have `SubnAdmGetTable` support when in `--sa` mode
  which makes them run faster. (Be warned, opensm has various bugs in its
  \*Record support)

Discovery:

* All the discovery shell scripts are native python and integrate properly with
  the command line system and support all the standard common options.
* The builtin discovery engine supports `--sa` which will rely entirely on SA
  Record queries for the data.
* All discovery using commands support the `--discovery` argument which can be
  LID, SMP or DR. DR exclusively uses directed route SMPs and can discover and
  unconfigured subnet. LID primarily uses LID routed SMP packets, except for a
  few DR SMPs to determine the connectivity. SA exclusively uses record data
  from the SA.
* Discovery data is stored in memory and re-used during the tool run,
  redundant queries are not issued.
* Everything is built on the parallel MAD scheduler
* The node name map file isn't implemented
* No chassis grouping functions are implemented
* Since no commands rely on frail text parsing, all node descriptions are
  supported in all tools, including putting " and other characters in them.

Specific commands:

* sminfo gets the LID using a `SMPPortInfo` RPC when using directed route.
* sminfo's has a --sminfo_smkey argument that is used for `SubnSet()` and `SubnGet()`
  RPCs. `SubnSet()` can send a 0 attribute modifier.
* `ibroute` uses the parallel MAD scheduler, displays LIDs in decimal and
  displays escaped node descriptions that are treated as UTF-8
* `ibroute` -M does not skip the last multicast LID.
* `ibroute` forgot how to limit by LID ranges
* `dump_lfts.sh` and `dump_mfts.sh` are internal commands that don't do
  duplicative work and are much faster.
* `ibhosts`, `ibswitches`, `ibrouters` and `ibnodes` display their output
  sorted by nodeGUID.
* smpquery sl2vl on a CA shows the CA port number not 0.
* perfquery supports directed route as an argument. The DR path is resolved
  to a LID path via a `SMPNodeInfo` RPC and a PR lookup to the SA
* perfquery uses the SA to get the `NodeInfo` (if needed) rather than using a
  SMP. It also uses the parallel MAD scheduler when looping over ports.
* 'perfquery -l' works like 'perfquery -a -l' instead of trying to request
  port 0 and often failing.
* perfquery gives a failure message if it is asked to loop over ports on
  a CA (which can't be done by simple port select)
* perfquery uses the `SMPNodeInfo.localPortNum` for the target as the default
  port number is none is given - this 'does the right thing' for CA ports
  and returns a result instead of an error for switch ports.
* perfquery will also handle `PMPortFlowCtlCounters`, `PMPortFlowCtlCounters`,
  `PMPortVLXmitFlowCtlUpdateErrors`, `PMPortVLXmitWaitCounters`,
  and `PMSwPortVLCongestion`
* `smpdump` has a `--decode` option to pretty print the MAD
* `smpdump` returns an error on timeout
* `smpdump` is joined by `decode_mad` which takes MADs in various formats
  and pretty prints them
* `saquery` supports all record types and supports all component masks via
  an enhanced syntax::

    saquery NR nodeInfo.portGUID=0017:77ff:feb6:2ca4

  This is done using python dynamic introspection and codegen of the component
  mask layout.
* The inconsistent names from saquery are less inconsistent but don't match
  100% what saquery produces.  The --int-names option uses the names described
  in this document.
* `saquery` forgot how to do --node-name-map
* `saquery` options that have an associated Selector don't set the selector.
* `saquery` is joined by `query` which can issue any Get type query for any
  supported attribute with any query content.
* `ibnetdiscover` prints the listing in a BFS order, not randomly.
* `ibfindnodesusing` only fetches subnet information actually used during
  output and supports more ways to specify the source switch.
* `ibfindnodesusing` learned the --all (show switches too) and -v (show
  LID and port GUID) options.
* `ibprintca/rt/switch` supports --sa which does limited SA queries to return
  the information instead of having to load a full topology.
* `ibprintca/rt/switch` displays the complete node stanza, instead of just a
  truncated version.
* `ibportstate` can work with CA ports if --sa is used
