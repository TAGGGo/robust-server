# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: amazon_ups.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='amazon_ups.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x10\x61mazon_ups.proto\">\n\tException\x12\x0b\n\x03\x65rr\x18\x01 \x02(\t\x12\x14\n\x0coriginseqnum\x18\x02 \x02(\x05\x12\x0e\n\x06seqnum\x18\x03 \x02(\x05\"-\n\tWarehouse\x12\n\n\x02id\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\"9\n\x07Product\x12\n\n\x02id\x18\x01 \x02(\x03\x12\x13\n\x0b\x64\x65scription\x18\x02 \x02(\t\x12\r\n\x05\x63ount\x18\x03 \x02(\x05\"t\n\tATruckReq\x12\x16\n\x02wh\x18\x01 \x02(\x0b\x32\n.Warehouse\x12\x12\n\nupsaccount\x18\x02 \x01(\t\x12\x11\n\tpackageid\x18\x03 \x02(\x03\x12\x18\n\x06things\x18\x04 \x03(\x0b\x32\x08.Product\x12\x0e\n\x06seqnum\x18\x05 \x02(\x05\"a\n\x0b\x41\x44\x65liverReq\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0f\n\x07truckid\x18\x02 \x02(\x05\x12\x0e\n\x06\x64\x65st_x\x18\x03 \x02(\x05\x12\x0e\n\x06\x64\x65st_y\x18\x04 \x02(\x05\x12\x0e\n\x06seqnum\x18\x05 \x02(\x05\"0\n\x0bUDeliverRsp\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x02 \x02(\x05\"@\n\nUTruckSent\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x11\n\tpackageid\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x05\"C\n\rUTruckArrived\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x11\n\tpackageid\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x05\"-\n\nU2AWorldId\x12\x0f\n\x07worldid\x18\x01 \x02(\x05\x12\x0e\n\x06seqnum\x18\x02 \x02(\x05\"o\n\x04\x41Msg\x12\x1c\n\x08truckreq\x18\x01 \x03(\x0b\x32\n.ATruckReq\x12 \n\ndeliverreq\x18\x02 \x03(\x0b\x32\x0c.ADeliverReq\x12\x0c\n\x04\x61\x63ks\x18\x03 \x03(\x05\x12\x19\n\x05\x65rror\x18\x04 \x03(\x0b\x32\n.Exception\"\xb4\x01\n\x04UMsg\x12\x1f\n\tdelivered\x18\x01 \x03(\x0b\x32\x0c.UDeliverRsp\x12\x1e\n\ttrucksent\x18\x02 \x03(\x0b\x32\x0b.UTruckSent\x12$\n\x0ctruckarrived\x18\x03 \x03(\x0b\x32\x0e.UTruckArrived\x12\x1c\n\x07worldid\x18\x04 \x03(\x0b\x32\x0b.U2AWorldId\x12\x0c\n\x04\x61\x63ks\x18\x05 \x03(\x05\x12\x19\n\x05\x65rror\x18\x06 \x03(\x0b\x32\n.Exception')
)




_EXCEPTION = _descriptor.Descriptor(
  name='Exception',
  full_name='Exception',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='err', full_name='Exception.err', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='originseqnum', full_name='Exception.originseqnum', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='Exception.seqnum', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=82,
)


_WAREHOUSE = _descriptor.Descriptor(
  name='Warehouse',
  full_name='Warehouse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Warehouse.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x', full_name='Warehouse.x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='Warehouse.y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=84,
  serialized_end=129,
)


_PRODUCT = _descriptor.Descriptor(
  name='Product',
  full_name='Product',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Product.id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='Product.description', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='Product.count', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=188,
)


_ATRUCKREQ = _descriptor.Descriptor(
  name='ATruckReq',
  full_name='ATruckReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='wh', full_name='ATruckReq.wh', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='upsaccount', full_name='ATruckReq.upsaccount', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='ATruckReq.packageid', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='things', full_name='ATruckReq.things', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='ATruckReq.seqnum', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=306,
)


_ADELIVERREQ = _descriptor.Descriptor(
  name='ADeliverReq',
  full_name='ADeliverReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='ADeliverReq.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='ADeliverReq.truckid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dest_x', full_name='ADeliverReq.dest_x', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dest_y', full_name='ADeliverReq.dest_y', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='ADeliverReq.seqnum', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=308,
  serialized_end=405,
)


_UDELIVERRSP = _descriptor.Descriptor(
  name='UDeliverRsp',
  full_name='UDeliverRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UDeliverRsp.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='UDeliverRsp.seqnum', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=407,
  serialized_end=455,
)


_UTRUCKSENT = _descriptor.Descriptor(
  name='UTruckSent',
  full_name='UTruckSent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='truckid', full_name='UTruckSent.truckid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UTruckSent.packageid', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='UTruckSent.seqnum', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=457,
  serialized_end=521,
)


_UTRUCKARRIVED = _descriptor.Descriptor(
  name='UTruckArrived',
  full_name='UTruckArrived',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='truckid', full_name='UTruckArrived.truckid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UTruckArrived.packageid', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='UTruckArrived.seqnum', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=523,
  serialized_end=590,
)


_U2AWORLDID = _descriptor.Descriptor(
  name='U2AWorldId',
  full_name='U2AWorldId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='worldid', full_name='U2AWorldId.worldid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='U2AWorldId.seqnum', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=592,
  serialized_end=637,
)


_AMSG = _descriptor.Descriptor(
  name='AMsg',
  full_name='AMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='truckreq', full_name='AMsg.truckreq', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deliverreq', full_name='AMsg.deliverreq', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acks', full_name='AMsg.acks', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='AMsg.error', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=639,
  serialized_end=750,
)


_UMSG = _descriptor.Descriptor(
  name='UMsg',
  full_name='UMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='delivered', full_name='UMsg.delivered', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trucksent', full_name='UMsg.trucksent', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='truckarrived', full_name='UMsg.truckarrived', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='worldid', full_name='UMsg.worldid', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acks', full_name='UMsg.acks', index=4,
      number=5, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='UMsg.error', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=753,
  serialized_end=933,
)

_ATRUCKREQ.fields_by_name['wh'].message_type = _WAREHOUSE
_ATRUCKREQ.fields_by_name['things'].message_type = _PRODUCT
_AMSG.fields_by_name['truckreq'].message_type = _ATRUCKREQ
_AMSG.fields_by_name['deliverreq'].message_type = _ADELIVERREQ
_AMSG.fields_by_name['error'].message_type = _EXCEPTION
_UMSG.fields_by_name['delivered'].message_type = _UDELIVERRSP
_UMSG.fields_by_name['trucksent'].message_type = _UTRUCKSENT
_UMSG.fields_by_name['truckarrived'].message_type = _UTRUCKARRIVED
_UMSG.fields_by_name['worldid'].message_type = _U2AWORLDID
_UMSG.fields_by_name['error'].message_type = _EXCEPTION
DESCRIPTOR.message_types_by_name['Exception'] = _EXCEPTION
DESCRIPTOR.message_types_by_name['Warehouse'] = _WAREHOUSE
DESCRIPTOR.message_types_by_name['Product'] = _PRODUCT
DESCRIPTOR.message_types_by_name['ATruckReq'] = _ATRUCKREQ
DESCRIPTOR.message_types_by_name['ADeliverReq'] = _ADELIVERREQ
DESCRIPTOR.message_types_by_name['UDeliverRsp'] = _UDELIVERRSP
DESCRIPTOR.message_types_by_name['UTruckSent'] = _UTRUCKSENT
DESCRIPTOR.message_types_by_name['UTruckArrived'] = _UTRUCKARRIVED
DESCRIPTOR.message_types_by_name['U2AWorldId'] = _U2AWORLDID
DESCRIPTOR.message_types_by_name['AMsg'] = _AMSG
DESCRIPTOR.message_types_by_name['UMsg'] = _UMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Exception = _reflection.GeneratedProtocolMessageType('Exception', (_message.Message,), dict(
  DESCRIPTOR = _EXCEPTION,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:Exception)
  ))
_sym_db.RegisterMessage(Exception)

Warehouse = _reflection.GeneratedProtocolMessageType('Warehouse', (_message.Message,), dict(
  DESCRIPTOR = _WAREHOUSE,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:Warehouse)
  ))
_sym_db.RegisterMessage(Warehouse)

Product = _reflection.GeneratedProtocolMessageType('Product', (_message.Message,), dict(
  DESCRIPTOR = _PRODUCT,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:Product)
  ))
_sym_db.RegisterMessage(Product)

ATruckReq = _reflection.GeneratedProtocolMessageType('ATruckReq', (_message.Message,), dict(
  DESCRIPTOR = _ATRUCKREQ,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:ATruckReq)
  ))
_sym_db.RegisterMessage(ATruckReq)

ADeliverReq = _reflection.GeneratedProtocolMessageType('ADeliverReq', (_message.Message,), dict(
  DESCRIPTOR = _ADELIVERREQ,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:ADeliverReq)
  ))
_sym_db.RegisterMessage(ADeliverReq)

UDeliverRsp = _reflection.GeneratedProtocolMessageType('UDeliverRsp', (_message.Message,), dict(
  DESCRIPTOR = _UDELIVERRSP,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UDeliverRsp)
  ))
_sym_db.RegisterMessage(UDeliverRsp)

UTruckSent = _reflection.GeneratedProtocolMessageType('UTruckSent', (_message.Message,), dict(
  DESCRIPTOR = _UTRUCKSENT,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTruckSent)
  ))
_sym_db.RegisterMessage(UTruckSent)

UTruckArrived = _reflection.GeneratedProtocolMessageType('UTruckArrived', (_message.Message,), dict(
  DESCRIPTOR = _UTRUCKARRIVED,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTruckArrived)
  ))
_sym_db.RegisterMessage(UTruckArrived)

U2AWorldId = _reflection.GeneratedProtocolMessageType('U2AWorldId', (_message.Message,), dict(
  DESCRIPTOR = _U2AWORLDID,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:U2AWorldId)
  ))
_sym_db.RegisterMessage(U2AWorldId)

AMsg = _reflection.GeneratedProtocolMessageType('AMsg', (_message.Message,), dict(
  DESCRIPTOR = _AMSG,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:AMsg)
  ))
_sym_db.RegisterMessage(AMsg)

UMsg = _reflection.GeneratedProtocolMessageType('UMsg', (_message.Message,), dict(
  DESCRIPTOR = _UMSG,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UMsg)
  ))
_sym_db.RegisterMessage(UMsg)


# @@protoc_insertion_point(module_scope)