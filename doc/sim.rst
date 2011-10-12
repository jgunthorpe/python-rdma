.. Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

************
IBSIM Module
************

Python RDMA has native support for communicating with the `ibsim` subnet
simulator. This support does not require any preload library or sysfs
emulation directory. The integrated module queries all information directly
from the simulator.

The usage of the simulator is straightforward::

 $ export IBSIM_SERVER_NAME=localhost
 $ ibtool ibstatus

 Infiniband device 'ibsim0' port 0 status:
         default gid:     fe80::20:0
         base lid:        0
         sm lid:          0
         state:           4: ACTIVE
         phys state:      5: Link UP
         rate:            4X (2.5 Gb/sec)

Currently the client only supports UDP connections so the simulator must
be started with '-r'::

 ibsim -r -s net-examples/net.2sw2path4hca

Limitations
===========

* verbs communication is not supported
* RMPP operations are not supported
* ibsim must be patched to fix bugs related to endianess handling and DR
  path processing.
