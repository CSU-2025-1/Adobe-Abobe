# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: auth.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'auth.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\"2\n\x0fRegisterRequest\x12\r\n\x05login\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"/\n\x0cLoginRequest\x12\r\n\x05login\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"$\n\x0cTokenRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\";\n\x0c\x41uthResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x15\n\rrefresh_token\x18\x02 \x01(\t\"2\n\x10ValidateResponse\x12\r\n\x05valid\x18\x01 \x01(\x08\x12\x0f\n\x07user_id\x18\x02 \x01(\t2\x94\x01\n\x0b\x41uthService\x12+\n\x08Register\x12\x10.RegisterRequest\x1a\r.AuthResponse\x12%\n\x05Login\x12\r.LoginRequest\x1a\r.AuthResponse\x12\x31\n\rValidateToken\x12\r.TokenRequest\x1a\x11.ValidateResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERREQUEST']._serialized_start=14
  _globals['_REGISTERREQUEST']._serialized_end=64
  _globals['_LOGINREQUEST']._serialized_start=66
  _globals['_LOGINREQUEST']._serialized_end=113
  _globals['_TOKENREQUEST']._serialized_start=115
  _globals['_TOKENREQUEST']._serialized_end=151
  _globals['_AUTHRESPONSE']._serialized_start=153
  _globals['_AUTHRESPONSE']._serialized_end=212
  _globals['_VALIDATERESPONSE']._serialized_start=214
  _globals['_VALIDATERESPONSE']._serialized_end=264
  _globals['_AUTHSERVICE']._serialized_start=267
  _globals['_AUTHSERVICE']._serialized_end=415
# @@protoc_insertion_point(module_scope)
