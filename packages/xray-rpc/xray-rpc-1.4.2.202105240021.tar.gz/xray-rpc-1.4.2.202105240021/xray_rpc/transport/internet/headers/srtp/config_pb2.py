# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/headers/srtp/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='transport/internet/headers/srtp/config.proto',
  package='xray.transport.internet.headers.srtp',
  syntax='proto3',
  serialized_options=b'\n(com.xray.transport.internet.headers.srtpP\001Z9github.com/xtls/xray-core/transport/internet/headers/srtp\252\002$Xray.Transport.Internet.Headers.Srtp',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n,transport/internet/headers/srtp/config.proto\x12$xray.transport.internet.headers.srtp\"w\n\x06\x43onfig\x12\x0f\n\x07version\x18\x01 \x01(\r\x12\x0f\n\x07padding\x18\x02 \x01(\x08\x12\x11\n\textension\x18\x03 \x01(\x08\x12\x12\n\ncsrc_count\x18\x04 \x01(\r\x12\x0e\n\x06marker\x18\x05 \x01(\x08\x12\x14\n\x0cpayload_type\x18\x06 \x01(\rB\x8e\x01\n(com.xray.transport.internet.headers.srtpP\x01Z9github.com/xtls/xray-core/transport/internet/headers/srtp\xaa\x02$Xray.Transport.Internet.Headers.Srtpb\x06proto3'
)




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='xray.transport.internet.headers.srtp.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='xray.transport.internet.headers.srtp.Config.version', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='padding', full_name='xray.transport.internet.headers.srtp.Config.padding', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extension', full_name='xray.transport.internet.headers.srtp.Config.extension', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='csrc_count', full_name='xray.transport.internet.headers.srtp.Config.csrc_count', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='marker', full_name='xray.transport.internet.headers.srtp.Config.marker', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload_type', full_name='xray.transport.internet.headers.srtp.Config.payload_type', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=86,
  serialized_end=205,
)

DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'transport.internet.headers.srtp.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.transport.internet.headers.srtp.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
