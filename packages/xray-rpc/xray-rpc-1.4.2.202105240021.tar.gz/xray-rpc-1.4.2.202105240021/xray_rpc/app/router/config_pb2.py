# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/router/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from xray_rpc.common.net import port_pb2 as common_dot_net_dot_port__pb2
from xray_rpc.common.net import network_pb2 as common_dot_net_dot_network__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='app/router/config.proto',
  package='xray.app.router',
  syntax='proto3',
  serialized_options=b'\n\023com.xray.app.routerP\001Z$github.com/xtls/xray-core/app/router\252\002\017Xray.App.Router',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x61pp/router/config.proto\x12\x0fxray.app.router\x1a\x15\x63ommon/net/port.proto\x1a\x18\x63ommon/net/network.proto\"\x81\x02\n\x06\x44omain\x12*\n\x04type\x18\x01 \x01(\x0e\x32\x1c.xray.app.router.Domain.Type\x12\r\n\x05value\x18\x02 \x01(\t\x12\x34\n\tattribute\x18\x03 \x03(\x0b\x32!.xray.app.router.Domain.Attribute\x1aR\n\tAttribute\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x14\n\nbool_value\x18\x02 \x01(\x08H\x00\x12\x13\n\tint_value\x18\x03 \x01(\x03H\x00\x42\r\n\x0btyped_value\"2\n\x04Type\x12\t\n\x05Plain\x10\x00\x12\t\n\x05Regex\x10\x01\x12\n\n\x06\x44omain\x10\x02\x12\x08\n\x04\x46ull\x10\x03\"\"\n\x04\x43IDR\x12\n\n\x02ip\x18\x01 \x01(\x0c\x12\x0e\n\x06prefix\x18\x02 \x01(\r\"B\n\x05GeoIP\x12\x14\n\x0c\x63ountry_code\x18\x01 \x01(\t\x12#\n\x04\x63idr\x18\x02 \x03(\x0b\x32\x15.xray.app.router.CIDR\"2\n\tGeoIPList\x12%\n\x05\x65ntry\x18\x01 \x03(\x0b\x32\x16.xray.app.router.GeoIP\"H\n\x07GeoSite\x12\x14\n\x0c\x63ountry_code\x18\x01 \x01(\t\x12\'\n\x06\x64omain\x18\x02 \x03(\x0b\x32\x17.xray.app.router.Domain\"6\n\x0bGeoSiteList\x12\'\n\x05\x65ntry\x18\x01 \x03(\x0b\x32\x18.xray.app.router.GeoSite\"\xe4\x04\n\x0bRoutingRule\x12\r\n\x03tag\x18\x01 \x01(\tH\x00\x12\x17\n\rbalancing_tag\x18\x0c \x01(\tH\x00\x12\'\n\x06\x64omain\x18\x02 \x03(\x0b\x32\x17.xray.app.router.Domain\x12\'\n\x04\x63idr\x18\x03 \x03(\x0b\x32\x15.xray.app.router.CIDRB\x02\x18\x01\x12%\n\x05geoip\x18\n \x03(\x0b\x32\x16.xray.app.router.GeoIP\x12\x32\n\nport_range\x18\x04 \x01(\x0b\x32\x1a.xray.common.net.PortRangeB\x02\x18\x01\x12,\n\tport_list\x18\x0e \x01(\x0b\x32\x19.xray.common.net.PortList\x12\x36\n\x0cnetwork_list\x18\x05 \x01(\x0b\x32\x1c.xray.common.net.NetworkListB\x02\x18\x01\x12*\n\x08networks\x18\r \x03(\x0e\x32\x18.xray.common.net.Network\x12.\n\x0bsource_cidr\x18\x06 \x03(\x0b\x32\x15.xray.app.router.CIDRB\x02\x18\x01\x12,\n\x0csource_geoip\x18\x0b \x03(\x0b\x32\x16.xray.app.router.GeoIP\x12\x33\n\x10source_port_list\x18\x10 \x01(\x0b\x32\x19.xray.common.net.PortList\x12\x12\n\nuser_email\x18\x07 \x03(\t\x12\x13\n\x0binbound_tag\x18\x08 \x03(\t\x12\x10\n\x08protocol\x18\t \x03(\t\x12\x12\n\nattributes\x18\x0f \x01(\tB\x0c\n\ntarget_tag\"7\n\rBalancingRule\x12\x0b\n\x03tag\x18\x01 \x01(\t\x12\x19\n\x11outbound_selector\x18\x02 \x03(\t\"\xf6\x01\n\x06\x43onfig\x12?\n\x0f\x64omain_strategy\x18\x01 \x01(\x0e\x32&.xray.app.router.Config.DomainStrategy\x12*\n\x04rule\x18\x02 \x03(\x0b\x32\x1c.xray.app.router.RoutingRule\x12\x36\n\x0e\x62\x61lancing_rule\x18\x03 \x03(\x0b\x32\x1e.xray.app.router.BalancingRule\"G\n\x0e\x44omainStrategy\x12\x08\n\x04\x41sIs\x10\x00\x12\t\n\x05UseIp\x10\x01\x12\x10\n\x0cIpIfNonMatch\x10\x02\x12\x0e\n\nIpOnDemand\x10\x03\x42O\n\x13\x63om.xray.app.routerP\x01Z$github.com/xtls/xray-core/app/router\xaa\x02\x0fXray.App.Routerb\x06proto3'
  ,
  dependencies=[common_dot_net_dot_port__pb2.DESCRIPTOR,common_dot_net_dot_network__pb2.DESCRIPTOR,])



_DOMAIN_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='xray.app.router.Domain.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Plain', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Regex', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Domain', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Full', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=301,
  serialized_end=351,
)
_sym_db.RegisterEnumDescriptor(_DOMAIN_TYPE)

_CONFIG_DOMAINSTRATEGY = _descriptor.EnumDescriptor(
  name='DomainStrategy',
  full_name='xray.app.router.Config.DomainStrategy',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AsIs', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UseIp', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IpIfNonMatch', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IpOnDemand', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1487,
  serialized_end=1558,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_DOMAINSTRATEGY)


_DOMAIN_ATTRIBUTE = _descriptor.Descriptor(
  name='Attribute',
  full_name='xray.app.router.Domain.Attribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='xray.app.router.Domain.Attribute.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='xray.app.router.Domain.Attribute.bool_value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='xray.app.router.Domain.Attribute.int_value', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
    _descriptor.OneofDescriptor(
      name='typed_value', full_name='xray.app.router.Domain.Attribute.typed_value',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=217,
  serialized_end=299,
)

_DOMAIN = _descriptor.Descriptor(
  name='Domain',
  full_name='xray.app.router.Domain',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='xray.app.router.Domain.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='xray.app.router.Domain.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attribute', full_name='xray.app.router.Domain.attribute', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DOMAIN_ATTRIBUTE, ],
  enum_types=[
    _DOMAIN_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=351,
)


_CIDR = _descriptor.Descriptor(
  name='CIDR',
  full_name='xray.app.router.CIDR',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='xray.app.router.CIDR.ip', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='prefix', full_name='xray.app.router.CIDR.prefix', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=353,
  serialized_end=387,
)


_GEOIP = _descriptor.Descriptor(
  name='GeoIP',
  full_name='xray.app.router.GeoIP',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='country_code', full_name='xray.app.router.GeoIP.country_code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cidr', full_name='xray.app.router.GeoIP.cidr', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=389,
  serialized_end=455,
)


_GEOIPLIST = _descriptor.Descriptor(
  name='GeoIPList',
  full_name='xray.app.router.GeoIPList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entry', full_name='xray.app.router.GeoIPList.entry', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=457,
  serialized_end=507,
)


_GEOSITE = _descriptor.Descriptor(
  name='GeoSite',
  full_name='xray.app.router.GeoSite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='country_code', full_name='xray.app.router.GeoSite.country_code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain', full_name='xray.app.router.GeoSite.domain', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=509,
  serialized_end=581,
)


_GEOSITELIST = _descriptor.Descriptor(
  name='GeoSiteList',
  full_name='xray.app.router.GeoSiteList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entry', full_name='xray.app.router.GeoSiteList.entry', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=583,
  serialized_end=637,
)


_ROUTINGRULE = _descriptor.Descriptor(
  name='RoutingRule',
  full_name='xray.app.router.RoutingRule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='xray.app.router.RoutingRule.tag', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='balancing_tag', full_name='xray.app.router.RoutingRule.balancing_tag', index=1,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain', full_name='xray.app.router.RoutingRule.domain', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cidr', full_name='xray.app.router.RoutingRule.cidr', index=3,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='geoip', full_name='xray.app.router.RoutingRule.geoip', index=4,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port_range', full_name='xray.app.router.RoutingRule.port_range', index=5,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port_list', full_name='xray.app.router.RoutingRule.port_list', index=6,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='network_list', full_name='xray.app.router.RoutingRule.network_list', index=7,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='networks', full_name='xray.app.router.RoutingRule.networks', index=8,
      number=13, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_cidr', full_name='xray.app.router.RoutingRule.source_cidr', index=9,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_geoip', full_name='xray.app.router.RoutingRule.source_geoip', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_port_list', full_name='xray.app.router.RoutingRule.source_port_list', index=11,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_email', full_name='xray.app.router.RoutingRule.user_email', index=12,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inbound_tag', full_name='xray.app.router.RoutingRule.inbound_tag', index=13,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='xray.app.router.RoutingRule.protocol', index=14,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attributes', full_name='xray.app.router.RoutingRule.attributes', index=15,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
    _descriptor.OneofDescriptor(
      name='target_tag', full_name='xray.app.router.RoutingRule.target_tag',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=640,
  serialized_end=1252,
)


_BALANCINGRULE = _descriptor.Descriptor(
  name='BalancingRule',
  full_name='xray.app.router.BalancingRule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='xray.app.router.BalancingRule.tag', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='outbound_selector', full_name='xray.app.router.BalancingRule.outbound_selector', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1254,
  serialized_end=1309,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='xray.app.router.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain_strategy', full_name='xray.app.router.Config.domain_strategy', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rule', full_name='xray.app.router.Config.rule', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='balancing_rule', full_name='xray.app.router.Config.balancing_rule', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1312,
  serialized_end=1558,
)

_DOMAIN_ATTRIBUTE.containing_type = _DOMAIN
_DOMAIN_ATTRIBUTE.oneofs_by_name['typed_value'].fields.append(
  _DOMAIN_ATTRIBUTE.fields_by_name['bool_value'])
_DOMAIN_ATTRIBUTE.fields_by_name['bool_value'].containing_oneof = _DOMAIN_ATTRIBUTE.oneofs_by_name['typed_value']
_DOMAIN_ATTRIBUTE.oneofs_by_name['typed_value'].fields.append(
  _DOMAIN_ATTRIBUTE.fields_by_name['int_value'])
_DOMAIN_ATTRIBUTE.fields_by_name['int_value'].containing_oneof = _DOMAIN_ATTRIBUTE.oneofs_by_name['typed_value']
_DOMAIN.fields_by_name['type'].enum_type = _DOMAIN_TYPE
_DOMAIN.fields_by_name['attribute'].message_type = _DOMAIN_ATTRIBUTE
_DOMAIN_TYPE.containing_type = _DOMAIN
_GEOIP.fields_by_name['cidr'].message_type = _CIDR
_GEOIPLIST.fields_by_name['entry'].message_type = _GEOIP
_GEOSITE.fields_by_name['domain'].message_type = _DOMAIN
_GEOSITELIST.fields_by_name['entry'].message_type = _GEOSITE
_ROUTINGRULE.fields_by_name['domain'].message_type = _DOMAIN
_ROUTINGRULE.fields_by_name['cidr'].message_type = _CIDR
_ROUTINGRULE.fields_by_name['geoip'].message_type = _GEOIP
_ROUTINGRULE.fields_by_name['port_range'].message_type = common_dot_net_dot_port__pb2._PORTRANGE
_ROUTINGRULE.fields_by_name['port_list'].message_type = common_dot_net_dot_port__pb2._PORTLIST
_ROUTINGRULE.fields_by_name['network_list'].message_type = common_dot_net_dot_network__pb2._NETWORKLIST
_ROUTINGRULE.fields_by_name['networks'].enum_type = common_dot_net_dot_network__pb2._NETWORK
_ROUTINGRULE.fields_by_name['source_cidr'].message_type = _CIDR
_ROUTINGRULE.fields_by_name['source_geoip'].message_type = _GEOIP
_ROUTINGRULE.fields_by_name['source_port_list'].message_type = common_dot_net_dot_port__pb2._PORTLIST
_ROUTINGRULE.oneofs_by_name['target_tag'].fields.append(
  _ROUTINGRULE.fields_by_name['tag'])
_ROUTINGRULE.fields_by_name['tag'].containing_oneof = _ROUTINGRULE.oneofs_by_name['target_tag']
_ROUTINGRULE.oneofs_by_name['target_tag'].fields.append(
  _ROUTINGRULE.fields_by_name['balancing_tag'])
_ROUTINGRULE.fields_by_name['balancing_tag'].containing_oneof = _ROUTINGRULE.oneofs_by_name['target_tag']
_CONFIG.fields_by_name['domain_strategy'].enum_type = _CONFIG_DOMAINSTRATEGY
_CONFIG.fields_by_name['rule'].message_type = _ROUTINGRULE
_CONFIG.fields_by_name['balancing_rule'].message_type = _BALANCINGRULE
_CONFIG_DOMAINSTRATEGY.containing_type = _CONFIG
DESCRIPTOR.message_types_by_name['Domain'] = _DOMAIN
DESCRIPTOR.message_types_by_name['CIDR'] = _CIDR
DESCRIPTOR.message_types_by_name['GeoIP'] = _GEOIP
DESCRIPTOR.message_types_by_name['GeoIPList'] = _GEOIPLIST
DESCRIPTOR.message_types_by_name['GeoSite'] = _GEOSITE
DESCRIPTOR.message_types_by_name['GeoSiteList'] = _GEOSITELIST
DESCRIPTOR.message_types_by_name['RoutingRule'] = _ROUTINGRULE
DESCRIPTOR.message_types_by_name['BalancingRule'] = _BALANCINGRULE
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Domain = _reflection.GeneratedProtocolMessageType('Domain', (_message.Message,), {

  'Attribute' : _reflection.GeneratedProtocolMessageType('Attribute', (_message.Message,), {
    'DESCRIPTOR' : _DOMAIN_ATTRIBUTE,
    '__module__' : 'app.router.config_pb2'
    # @@protoc_insertion_point(class_scope:xray.app.router.Domain.Attribute)
    })
  ,
  'DESCRIPTOR' : _DOMAIN,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.Domain)
  })
_sym_db.RegisterMessage(Domain)
_sym_db.RegisterMessage(Domain.Attribute)

CIDR = _reflection.GeneratedProtocolMessageType('CIDR', (_message.Message,), {
  'DESCRIPTOR' : _CIDR,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.CIDR)
  })
_sym_db.RegisterMessage(CIDR)

GeoIP = _reflection.GeneratedProtocolMessageType('GeoIP', (_message.Message,), {
  'DESCRIPTOR' : _GEOIP,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.GeoIP)
  })
_sym_db.RegisterMessage(GeoIP)

GeoIPList = _reflection.GeneratedProtocolMessageType('GeoIPList', (_message.Message,), {
  'DESCRIPTOR' : _GEOIPLIST,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.GeoIPList)
  })
_sym_db.RegisterMessage(GeoIPList)

GeoSite = _reflection.GeneratedProtocolMessageType('GeoSite', (_message.Message,), {
  'DESCRIPTOR' : _GEOSITE,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.GeoSite)
  })
_sym_db.RegisterMessage(GeoSite)

GeoSiteList = _reflection.GeneratedProtocolMessageType('GeoSiteList', (_message.Message,), {
  'DESCRIPTOR' : _GEOSITELIST,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.GeoSiteList)
  })
_sym_db.RegisterMessage(GeoSiteList)

RoutingRule = _reflection.GeneratedProtocolMessageType('RoutingRule', (_message.Message,), {
  'DESCRIPTOR' : _ROUTINGRULE,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.RoutingRule)
  })
_sym_db.RegisterMessage(RoutingRule)

BalancingRule = _reflection.GeneratedProtocolMessageType('BalancingRule', (_message.Message,), {
  'DESCRIPTOR' : _BALANCINGRULE,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.BalancingRule)
  })
_sym_db.RegisterMessage(BalancingRule)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'app.router.config_pb2'
  # @@protoc_insertion_point(class_scope:xray.app.router.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
_ROUTINGRULE.fields_by_name['cidr']._options = None
_ROUTINGRULE.fields_by_name['port_range']._options = None
_ROUTINGRULE.fields_by_name['network_list']._options = None
_ROUTINGRULE.fields_by_name['source_cidr']._options = None
# @@protoc_insertion_point(module_scope)
