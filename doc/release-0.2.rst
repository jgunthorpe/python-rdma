Version 0.2
===========

`In progress`

Notable Bug Fixes:

- :attr:`rdma.devices.RDMADevice.node_desc` had a trailing \\n
- `ibverbs` tracks multicast joins in QPs so they can be undone during closing,
  fixs up a failure to clean up during exceptions in some cases.
- :class:`~rdma.sched.MADSchedule` could loose the RPC result if it got too busy.
- :func:`rdma.discovery.topo_SMP` did not strictly enforce BFS order and
  could overrun the hop limit.

Notable Features/Improvements:

- :func:`rdma.path.from_string` is a very general string to
  :class:`~rdma.path` parser. Includes support for parsing the :func:`repr`
  format of :class:`~rdma.path.IBPath`, which basically makes everything possible
  from the command line.
- :meth:`rdma.subnet.Subnet.advance_dr` is used to advance a DR path, and it
  understands how to deal with trying to DR from a non switch port.
- :attr:`rdma.subnet.Port.port_id`
- :func:`rdma.path.resolve_path` and :func:`rdma.path.get_mad_path` can be
  used with :class:`~rdma.sched.MADSchedule`, or synchronously.
- Support for acting as a GMP server, including vendor MADs and vendor
  MADs with OUIs. See :meth:`rdma.madtransactor.MADTransactor.parse_request`

ibtool:

- Better target address parsing using :func:`rdma.path.from_string`
- Add `set_nodedesc[.sh]`
- Add `ibtracert`
- Add `ibswportwatch`
- Add `iblinkinfo`
- Add `subnet_diff` (aka `ibdiscover.pl`)
- Single node fabric check functions: `ibchecknode`, `ibcheckportstate`,
  `ibcheckportwidth`, `ibcheckerrs`, and `ibdatacounts`
- Full topology check functions: `ibcheckstate`, `ibcheckwidth`, `ibchecknet`,
  `ibcheckerrors`, `ibclearcounters`, `ibclearerrors`, `ibdatacounters`, and
  `ibidsverify`.
- MAD server functions `vendstat`, `ibsysstat` and `ibping`
