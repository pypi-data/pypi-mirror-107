# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proxy/freedom/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from xray_rpc.common.protocol import server_spec_pb2 as common_dot_protocol_dot_server__spec__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proxy/freedom/config.proto',
  package='xray.proxy.freedom',
  syntax='proto3',
  serialized_options=b'\n\026com.xray.proxy.freedomP\001Z\'github.com/xtls/xray-core/proxy/freedom\252\002\022Xray.Proxy.Freedom',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1aproxy/freedom/config.proto\x12\x12xray.proxy.freedom\x1a!common/protocol/server_spec.proto\"K\n\x13\x44\x65stinationOverride\x12\x34\n\x06server\x18\x01 \x01(\x0b\x32$.xray.common.protocol.ServerEndpoint\"\xff\x01\n\x06\x43onfig\x12\x42\n\x0f\x64omain_strategy\x18\x01 \x01(\x0e\x32).xray.proxy.freedom.Config.DomainStrategy\x12\x13\n\x07timeout\x18\x02 \x01(\rB\x02\x18\x01\x12\x45\n\x14\x64\x65stination_override\x18\x03 \x01(\x0b\x32\'.xray.proxy.freedom.DestinationOverride\x12\x12\n\nuser_level\x18\x04 \x01(\r\"A\n\x0e\x44omainStrategy\x12\t\n\x05\x41S_IS\x10\x00\x12\n\n\x06USE_IP\x10\x01\x12\x0b\n\x07USE_IP4\x10\x02\x12\x0b\n\x07USE_IP6\x10\x03\x42X\n\x16\x63om.xray.proxy.freedomP\x01Z\'github.com/xtls/xray-core/proxy/freedom\xaa\x02\x12Xray.Proxy.Freedomb\x06proto3'
  ,
  dependencies=[common_dot_protocol_dot_server__spec__pb2.DESCRIPTOR,])



_CONFIG_DOMAINSTRATEGY = _descriptor.EnumDescriptor(
  name='DomainStrategy',
  full_name='xray.proxy.freedom.Config.DomainStrategy',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AS_IS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='USE_IP', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='USE_IP4', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='USE_IP6', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=353,
  serialized_end=418,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_DOMAINSTRATEGY)


_DESTINATIONOVERRIDE = _descriptor.Descriptor(
  name='DestinationOverride',
  full_name='xray.proxy.freedom.DestinationOverride',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='server', full_name='xray.proxy.freedom.DestinationOverride.server', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=85,
  serialized_end=160,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='xray.proxy.freedom.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain_strategy', full_name='xray.proxy.freedom.Config.domain_strategy', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='xray.proxy.freedom.Config.timeout', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='destination_override', full_name='xray.proxy.freedom.Config.destination_override', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_level', full_name='xray.proxy.freedom.Config.user_level', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONFIG_DOMAINSTRATEGY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=163,
  serialized_end=418,
)

_DESTINATIONOVERRIDE.fields_by_name['server'].message_type = common_dot_protocol_dot_server__spec__pb2._SERVERENDPOINT
_CONFIG.fields_by_name['domain_strategy'].enum_type = _CONFIG_DOMAINSTRATEGY
_CONFIG.fields_by_name['destination_override'].message_type = _DESTINATIONOVERRIDE
_CONFIG_DOMAINSTRATEGY.containing_type = _CONFIG
DESCRIPTOR.message_types_by_name['DestinationOverride'] = _DESTINATIONOVERRIDE
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DestinationOverride = _reflection.GeneratedProtocolMessageType('DestinationOverride', (_message.Message,), {
  'DESCRIPTOR' : _DESTINATIONOVERRIDE,
  '__module__' : 'proxy.freedom.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.proxy.freedom.DestinationOverride)
  })
_sym_db.RegisterMessage(DestinationOverride)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'proxy.freedom.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.proxy.freedom.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
_CONFIG.fields_by_name['timeout']._options = None
# @@protoc_insertion_point(module_scope)
