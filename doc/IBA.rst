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
   This is based on Pythons :mod:`struct` module, which requires a :class:`bytes`
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
member of a `*Format` object. Here is the pretty print output for a
:class:`~rdma.IBA.SAFormat` containing a :class:`~rdma.IBA.SAPathRecord`::

 SAFormat
   0 01030201 baseVersion=1,mgmtClass=3,classVersion=2,method=1
   4 00000000 status=0,classSpecific=0
   8 00000000 transactionID=1
  12 00000001
  16 00350000 attributeID=53,reserved1=0
  20 00000000 attributeModifier=0
  24 00000000 RMPPVersion=0,RMPPType=0,RRespTime=0,RMPPFlags=0,RMPPStatus=0
  28 00000000 data1=0
  32 00000000 data2=0
  36 00000000 SMKey=0
  40 00000000
  44 00000000 attributeOffset=0,reserved2=0
  48 00000000 componentMask=2060
  52 0000080C
 SAPathRecord
  56 00000000 reserved1=0
  60 00000000 reserved2=0
  64 FE800000 DGID=GID('fe80::2:c903:0:1492')
  68 00000000
  72 0002C903
  76 00001492
  80 FE800000 SGID=GID('fe80::2:c903:0:1491')
  84 00000000
  88 0002C903
  92 00001491
  96 00000000 DLID=0,SLID=0
 100 00000000 rawTraffic=0,reserved3=0,flowLabel=0,hopLimit=0
 104 00800000 TClass=0,reversible=1,numbPath=0,PKey=0
 108 00000000 reserved4=0,SL=0,MTUSelector=0,MTU=0,rateSelector=0,rate=0
 112 00000000 packetLifeTimeSelector=0,packetLifeTime=0,preference=0,reserved5=0
 116 00000000 reserved6=0

Notice that the use of :class:`~rdma.IBA.SAPathRecord` for the payload is
automatically deduced based on the value of `attributeID`. The printer shows
the decimal byte offset and raw hex bytes in the left columns and shows a decode
of the attribute names corrisponding to that byte position in the right hand
area.

The pretty printer is invoked by calling the :meth:`~rdma.binstruct.BinStruct.printer`
method of the structure to print. This example shows how to produce an arbitary
MAD printer::

  IBA.get_fmt_payload(buf[1],buf[2],0)[0](buf).printer(sys.stdout);


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
   :members: BinFormat,ComponentMask,GID,GUID,ZERO_GID,ZERO_GUID,conv_ep_addr,conv_lid
   :undoc-members:
   :show-inheritance:

.. module_data:: rdma.IBA

:mod:`rmda.IBA` Binary Structures
---------------------------------

.. include:: iba_struct.inc
