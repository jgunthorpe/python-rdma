MAD RPC Processing
==================

The python-rdma package includes a simplified system for processing MAD
based RPCs defined in the InfiniBand Architecture. Most of the tedious
processing is taken care of automatically and the user sees only the
actual RPC payload they are interested in.

For example, this displays the :class:`~rdma.IBA.SMPPortInfo` for the local
port::

	end_port = rdma.get_end_port();
	path = rdma.path.IBDRPath(end_port);
	with rdma.get_umad(end_port) as umad:
	    pinf = umad.SubnGet(IBA.SMPPortInfo,path);
	    pinf.printer(sys.stdout);

:mod:`rdma.madtransactor` MAD RPC Mixin
---------------------------------------

:class:`~rdma.madtransactor.MADTransactor` provides the base set of methods for doing MAD
RPC. Derived classes uses this as a mixin to provide the basic API.

The user visible API is the IBA defined RPC names, eg
:meth:`~rdma.madtransactor.MADTransactor.SubnGet` which performs that named RPC.

Two modes of operation are possible, synchronous and asynchronous. In
synchronous mode the RPC API will return the decoded reply payload. In
asynchronous mode the RPC API will return the request message details. The
mode in use is determined by the derived class.

The API is quite simplified::

   # Return the SMPPortInfo for port 1
   pinf = mad.SubnGet(IBA.SMPPortInfo,path,1);
   print pinf.masterSMLID;

Under the covers the :class:`~rdma.madtransactor.MADTransactor` produces a
:class:`rdma.IBA.SMPFormat` or :class:`rdma.IBA.SMPFormatDirected` that
contains as a payload a zero :class:`rdma.IBA.SMPPortInfo`. The
``attributeID`` is set to ``IBA.SMPPortInfo.MAD_ATTRIBUTE_ID`` and
the argument is tested to ensure that ``SubnGet`` is a legal RPC.

When a valid reply is received the generic MAD header is processed and errors
are converted into exceptions. The payload is unpacked and a new
:class:`rdma.IBA.SMPPortInfo` is returned.

All RPC functions have a similar signature:

.. function:: RPC(payload,path,attributeModifier=0)

   :param payload: The RPC type to execute. If it is a class then the request payload is zero, otherwise the content of the instance is sent as the request.
   :type payload: :class:`rdma.binstruct.BinStruct` derived class adhering to the MAD protocol
   :param path: A reversible path specifying the target node.
   :type path: :class:`rdma.path.IBPath`
   :param attributeModifier: The value of the generic MAD :attr:`rdma.IBA.MADHeader.attributeModifier` field
   :type attributeModifier: :class:`int`
   :returns: If *payload* is class then an instance of that class, otherwise a new instance of *payload.__class__*.
   :raises rdma.MADError: If an error MAD is returned.
   :raises rdma.MADTimeoutError: If the MAD timed out.
   :raises AttributeError: If payload or path are invalid.

.. automodule:: rdma.madtransactor
   :members:
   :undoc-members:

:mod:`rdma.umad` Userspace MAD Interface
----------------------------------------

The userspace MAD interface is normally instantiated by :func:`rdma.get_umad`
which will select the appropriate implementation for the platform.

.. automodule:: rdma.umad
   :members:
   :undoc-members:
   :show-inheritance:

:mod:`rdma.sched` Parallel MAD Scheduler
----------------------------------------

:class:`~rdma.sched.MADSchedule` is a parallel MAD scheduling system built
using Python coroutines as the schedualing element. It provides for very
simplified programming of parallel MAD operations.

A simple use of the class to fetch :class:`rdma.IBA.SMPNodeInfo` for a list of
paths::

    def get_nodeinfo(sched,node):
        node.ninf = yield sched.SubGet(IBA.SMPNodeInfo,node.path);

    nodes = [..];
    sched = rdma.sched.MADSchedual(umad);
    sched.run(mqueue=(get_nodeinfo(sched,I) for I in nodes));

The scheduler will pull coroutines from the *mqueue* argument and runs them to
return MADs to send, bounding the total outstanding MAD count and returning
replies as the result of ``yield``.

Simplified, :class:`~rdma.sched.MADSchedule` manages a set of generators
and coroutines and schedules when each is running. Generators ``yield``
coroutines and coroutines ``yield`` MADs to execute. Generators are started
by calling :meth:`~rdma.sched.MADSchedule.mqueue`. Typically this
would be done using a generator expression as an argument, but this is not
required.

Coroutines are the functions that actually process the MADs. They are started
either by being yielded from a generator or via the
:meth:`~rdma.sched.MADSchedule.queue` call. The typical format of a coroutine
is::

    def get_nodeinfo(sched,node):
        node.ninf = yield sched.SubGet(IBA.SMPNodeInfo,node.path);

:class:`~rdma.sched.MADSchedule` implements the asynchronous interface for
:class:`~rdma.madtransactor.MADTransactor`, so the RPC functions return the
MAD to send. The coroutine yields these MADs back to the scheduler which
issues them on the network and waits for a reply. When a reply (or exception)
is returned for the MAD the ``yield`` statement will return that exactly as
though the synchronous interface to :class:`~rdma.madtransactor.MADTransactor`
was being used.

While a coroutine is yielded other coroutined can execute until
:attr:`rdma.sched.MADSchedule.max_outstanding` MADs are issued, at which point
the scheduler waits for MADs on the network to complete. As coroutines exit
queued generators are called to produce more coroutines until there is no more
work to do.

A coroutine may also ``yeild`` another coroutine. In this instance the
scheduler treats it as a function call and runs the returned coroutine to
completion before returning from ``yeild``. If the coroutine produces
an exception then it will pass through the ``yield`` statement as well.

This example shows how to perform directed route discovery of a network
using parallel MAD scheduling::

    def get_port_info(sched,path,port,follow):
        pinf = yield sched.SubnGet(IBA.SMPPortInfo,path,port);
        if follow and pinf.portState != IBA.PORT_STATE_DOWN:
            npath = rdma.path.IBDRPath(end_port,drPath=path.drPath + chr(port));
            yield get_node_info(sched,npath);

    def get_node_info(sched,path):
        ninf = yield sched.SubnGet(IBA.SMPNodeInfo,path);
        if ninf.nodeGUID in guids:
            return;
        guids[ninf.nodeGUID] = ninf;

        if ninf.nodeType == IBA.NODE_SWITCH:
            sched.mqueue(get_port_info(sched,path,I,True)
                         for I in range(1,ninf.numPorts+1));
            pinf = yield sched.SubnGet(IBA.SMPPortInfo,path,0);
        else:
            yield get_port_info(sched,path,ninf.localPortNum,
                                len(path.drPath) == 1);

    guids = {};
    with rdma.get_umad(endport) as umad:
        sched = rdma.sched.MADSchedule(umad);
        local_path = rdma.path.IBDRPath(end_port);
        sched.run(get_node_info(sched,local_path));

.. automodule:: rdma.sched
   :members:
   :undoc-members:
   :show-inheritance:

:mod:`rdma.satransactor` Automatic SubnGet to SubnAdmGet Conversion
-------------------------------------------------------------------

IBA provides two ways to get information about objects manages by a SMA - the
first is a `SubnGet` SMP RPC to the end port, the second is a `SubnAdmGet`
GMP RPC to the SA. These should return the same information and are generally
interchangeable.

This class provides an easy way for tools to access the information either
using `SubnGet` or using `SubnAdmGet` without really affecting the source
code.  The `SubnGet` is transparently recoded into a `SubnAdmGet` with the
proper query components set from the path and attribute ID and proper
unwrapping of the SA reply.

The class can wrapper both synchronous and asynchronous
:class:`~rdma.madtransactor.MADTransactor` instances. When wrappering a
synchronous instance the class can also automatically resolve a DR path to a
LID for use with the SA.

I highly recommend that all tools with the cabability to perform `SubnGet`
provide an option to use this class to rely on the SA. IBA defines operation
modes that would deny all `SubnGet` operations without a valid `MKey`.

Example::

	end_port = rdma.get_end_port();
	path = rdma.path.IBDRPath(end_port);
	with rdma.satransactor.SATransactor(rdma.get_umad(end_port)) as umad:
	    pinf = umad.SubnGet(IBA.SMPPortInfo,path);
	    pinf.printer(sys.stdout);

.. automodule:: rdma.satransactor
   :members:
   :undoc-members:
   :show-inheritance:
