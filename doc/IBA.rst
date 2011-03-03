InfiniBand Architecture (IBA) Definitions
=========================================

The majority of these definitions apply only to InfiniBand and are not
applicable to general RDMA devices. However, a few are used as part of the
kernel API for all device types (eg :data:`~rdma.IBA.NODE_CA`).

For ease of use it is recommended to import this module as::

    import rdma.IBA as IBA;

The module includes Python versions of the IBA defined binary structure. The
Python version is unpacked, accessing the IBA defined member names is simply
done by acessing the property name. The tables in the reference indicate
the valid member names, the bit position ``start_bit:end_bit (bit count)``
and a description of the Python type used for the attribute.

The class attributes starting with ``MAD_`` are metadata used by the RPC
functions in :class:`rdma.madtransactor.MADTransactor` to generate the correct
attribute ID, and validate that the RPC is valid.

All classes in this section are derived from :class:`rdma.binstruct.BinStruct`
and contain implementations of those methods. Use the
:meth:`~rdma.binstruct.BinStruct.pack_into` and
:meth:`~rdma.binstruct.BinStruct.unpack_from` methods to produce the
binary layout of the structure.

Constructors will also accept a bytes or another
:class:`~rdma.binstruct.BinStruct` instance::

   data = bytes('\0'*IBA.SMPFormat.MAD_LENGTH);
   hdr = IBA.MADHeader(data);
   sfmt = IBA.SMPFormat(hdr);
   dfmt = IBA.SMPFormatDirected(sfmt);

When referring to another :class:`~rdma.binstruct.BinStruct` instance the
new instance is unpacked using the original byte buffer that the first instance
was unpacked from. Changing the attributes has no effect.

.. NOTE::
   This is based on Python's :mod:`struct` module, which requires a :class:`bytes`
   object for unpack and a :class:`bytearray` for packing. This conversion
   is generally handled transparently..

Structures named ``*Format`` are generally a full MAD, and need to be 'casted'
to read the data::

   fmt = IBA.SMPFormat(data);
   pinf = IBA.SMPPortInfo(fmt.data);

Structure Pretty Printer
------------------------

All of the :class:`~rdma.binstruct.BinStruct` classes feature an automatic
pretty printer for the class content. The pretty printer understands some of
the structure of the data and properly pretty prints things like the data
member of a `*Format` object. Here is the `dump` pretty print output for a
:class:`~rdma.IBA.SAFormat` containing a :class:`~rdma.IBA.SAPathRecord`::

 SAFormat
   0 01030281 baseVersion=1,mgmtClass=3,classVersion=2,method=129
   4 00000000 status=0,classSpecific=0
   8 000028D6 transactionID=44902842023172
  12 C1F2BD04
  16 00350000 attributeID=53,reserved_144=0
  20 00000000 attributeModifier=0
  24 00000000 RMPPVersion=0,RMPPType=0,RRespTime=0,RMPPFlags=0,RMPPStatus=0
  28 00000000 data1=0
  32 00000000 data2=0
  36 00000000 SMKey=0
  40 00000000
  44 00080000 attributeOffset=8,reserved_368=0
  48 00000000 componentMask=2072
  52 00000818
    + data SAPathRecord
  56 00000000 serviceID=0
  60 00000000
  64 FE800000 DGID=GID('fe80::2:c903:0:1491')
  68 00000000
  72 0002C903
  76 00001491
  80 FE800000 SGID=GID('fe80::2:c903:0:1491')
  84 00000000
  88 0002C903
  92 00001491
  96 00050005 DLID=5,SLID=5
 100 00000000 rawTraffic=0,reserved_353=0,flowLabel=0,hopLimit=0
 104 0080FFFF TClass=0,reversible=1,numbPath=0,PKey=65535
 108 00008483 QOSClass=0,SL=0,MTUSelector=2,MTU=4,rateSelector=2,rate=3
 112 80000000 packetLifeTimeSelector=2,packetLifeTime=0,preference=0,reserved_464=0
 116 00000000 reserved_480=0

Notice that the use of :class:`~rdma.IBA.SAPathRecord` for the payload is
automatically deduced based on the value of `attributeID`. The printer shows
the decimal byte offset and raw hex bytes in the left columns and shows a decode
of the attribute names corrisponding to that byte position in the right hand
area.

The pretty printer is invoked by calling the :meth:`~rdma.binstruct.BinStruct.printer`
method of the structure to print. This example shows how to produce an arbitary
MAD printer::

  IBA.get_fmt_payload(buf[1],buf[2],0)[0](buf).printer(sys.stdout);

This is the dotted pretty print format::

 SAFormat
 baseVersion.....................1
 mgmtClass.......................3
 classVersion....................2
 method..........................146
 status..........................0
 classSpecific...................0
 transactionID...................44950782152048
 attributeID.....................53
 reserved_144....................0
 attributeModifier...............0
 RMPPVersion.....................1
 RMPPType........................1
 RRespTime.......................0
 RMPPFlags.......................7
 RMPPStatus......................0
 data1...........................1
 data2...........................84
 SMKey...........................0
 attributeOffset.................8
 reserved_368....................0
 componentMask...................12
 data.serviceID..................0
 data.DGID.......................GID('fe80::2:c903:0:1491')
 data.SGID.......................GID('fe80::2:c903:0:1491')
 data.DLID.......................5
 data.SLID.......................5
 data.rawTraffic.................0
 data.reserved_353...............0
 data.flowLabel..................0
 data.hopLimit...................0
 data.TClass.....................0
 data.reversible.................1
 data.numbPath...................0
 data.PKey.......................65535
 data.QOSClass...................0
 data.SL.........................0
 data.MTUSelector................2
 data.MTU........................4
 data.rateSelector...............2
 data.rate.......................3
 data.packetLifeTimeSelector.....2
 data.packetLifeTime.............0
 data.preference.................0
 data.reserved_464...............0
 data.reserved_480...............0

Component Mask Helper
---------------------

Subnet Administration Get RPCs have an annoying `ComponentMask` field which is
a bitfield indicating which subfields are relevant. Computing the correct
value for this can be quite difficult. The RPC generator computes the proper
values for all RPCs and stores them in the class variable
``COMPONENT_MASK``. The helper class :class:`rdma.IBA.ComponentMask` uses this
information to automate computing the `ComponentMask` value. For example::

        obj = IBA.SAPathRecord()
        cm = IBA.ComponentMask(obj);
	cm.DGID = IBA.GID("::1");
        cm.DLID = 2;
        assert(cm.component_mask == 20)

Passing a :class:`~rdma.IBA.ComponentMask` into the `SubnAdm*` RPC methods will
automatically correctly set the `ComponentMask` value of the MAD.

Word about Versions
-------------------

The library has some limited support for versioning the MAD Formats, but it is
not yet fully developed. The basic notion is that each version of a management
class will have a separate `Format` class and separate attribute classes.
The attribute class will be enhanced to contain the lowest format version it
applies to and the generic layer will instantiate the correct `Format` class.

Generally the message is that client programmers should ignore versions, and
the library will forever process todays current version with the current code.

Server side is a bit different, as the incoming MAD will be decoded according
to the version capability of the library, so some defensive code will
be required there.

:mod:`rdma.binstruct` IBA Structure Helpers
-------------------------------------------
.. automodule:: rdma.binstruct
   :members:
   :undoc-members:

:mod:`rdma.IBA_describe` Convert values descriptive strings
-----------------------------------------------------------
.. automodule:: rdma.IBA_describe
   :members:
   :undoc-members:

:mod:`rdma.IBA` InfiniBand Architecture (IBA) definitions
---------------------------------------------------------
.. automodule:: rdma.IBA
   :members: BinFormat,ComponentMask,GID,GUID,ZERO_GID,ZERO_GUID,conv_ep_addr,conv_lid,decode_link_width,lid_lmc_range,to_timer
   :undoc-members:
   :show-inheritance:

.. module_data:: rdma.IBA

:mod:`rmda.IBA` Binary Structures
---------------------------------

.. include:: iba_struct.inc
