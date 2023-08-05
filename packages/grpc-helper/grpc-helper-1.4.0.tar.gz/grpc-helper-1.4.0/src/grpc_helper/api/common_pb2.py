# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_helper/api/common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="grpc_helper/api/common.proto",
    package="",
    syntax="proto3",
    serialized_options=b"\n\017grpc_helper.apiP\001",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x1cgrpc_helper/api/common.proto"?\n\x06Result\x12\x19\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x0b.ResultCode\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\r\n\x05stack\x18\x03 \x01(\t""\n\x0cResultStatus\x12\x12\n\x01r\x18\x01 \x01(\x0b\x32\x07.Result"\x07\n\x05\x45mpty"/\n\x06\x46ilter\x12\r\n\x05names\x18\x01 \x03(\t\x12\x16\n\x0eignore_unknown\x18\x02 \x01(\x08*\xea\x02\n\nResultCode\x12\x06\n\x02OK\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x12\x08\n\x04\x41RGS\x10\x02\x12\x13\n\x0f\x45RROR_PORT_BUSY\x10\n\x12\x1c\n\x18\x45RROR_API_CLIENT_TOO_OLD\x10\x0b\x12\x1c\n\x18\x45RROR_API_SERVER_TOO_OLD\x10\x0c\x12\r\n\tERROR_RPC\x10\r\x12\x1c\n\x18\x45RROR_PROXY_UNREGISTERED\x10\x0e\x12\x19\n\x15\x45RROR_STREAM_SHUTDOWN\x10\x0f\x12\x17\n\x13\x45RROR_PARAM_MISSING\x10\x14\x12\x17\n\x13\x45RROR_PARAM_INVALID\x10\x15\x12\x16\n\x12\x45RROR_ITEM_UNKNOWN\x10\x1e\x12\x17\n\x13\x45RROR_ITEM_CONFLICT\x10\x1f\x12\x17\n\x13\x45RROR_MODEL_INVALID\x10(\x12\x18\n\x14\x45RROR_REQUEST_FAILED\x10\x32\x12\x10\n\x0c\x45RROR_CUSTOM\x10\x64\x42\x13\n\x0fgrpc_helper.apiP\x01\x62\x06proto3',
)

_RESULTCODE = _descriptor.EnumDescriptor(
    name="ResultCode",
    full_name="ResultCode",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(name="OK", index=0, number=0, serialized_options=None, type=None, create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(name="ERROR", index=1, number=1, serialized_options=None, type=None, create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(name="ARGS", index=2, number=2, serialized_options=None, type=None, create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name="ERROR_PORT_BUSY", index=3, number=10, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_API_CLIENT_TOO_OLD", index=4, number=11, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_API_SERVER_TOO_OLD", index=5, number=12, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(name="ERROR_RPC", index=6, number=13, serialized_options=None, type=None, create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name="ERROR_PROXY_UNREGISTERED", index=7, number=14, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_STREAM_SHUTDOWN", index=8, number=15, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_PARAM_MISSING", index=9, number=20, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_PARAM_INVALID", index=10, number=21, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_ITEM_UNKNOWN", index=11, number=30, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_ITEM_CONFLICT", index=12, number=31, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_MODEL_INVALID", index=13, number=40, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_REQUEST_FAILED", index=14, number=50, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR_CUSTOM", index=15, number=100, serialized_options=None, type=None, create_key=_descriptor._internal_create_key
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=192,
    serialized_end=554,
)
_sym_db.RegisterEnumDescriptor(_RESULTCODE)

ResultCode = enum_type_wrapper.EnumTypeWrapper(_RESULTCODE)
OK = 0
ERROR = 1
ARGS = 2
ERROR_PORT_BUSY = 10
ERROR_API_CLIENT_TOO_OLD = 11
ERROR_API_SERVER_TOO_OLD = 12
ERROR_RPC = 13
ERROR_PROXY_UNREGISTERED = 14
ERROR_STREAM_SHUTDOWN = 15
ERROR_PARAM_MISSING = 20
ERROR_PARAM_INVALID = 21
ERROR_ITEM_UNKNOWN = 30
ERROR_ITEM_CONFLICT = 31
ERROR_MODEL_INVALID = 40
ERROR_REQUEST_FAILED = 50
ERROR_CUSTOM = 100


_RESULT = _descriptor.Descriptor(
    name="Result",
    full_name="Result",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="code",
            full_name="Result.code",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="msg",
            full_name="Result.msg",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="stack",
            full_name="Result.stack",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=32,
    serialized_end=95,
)


_RESULTSTATUS = _descriptor.Descriptor(
    name="ResultStatus",
    full_name="ResultStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="r",
            full_name="ResultStatus.r",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=97,
    serialized_end=131,
)


_EMPTY = _descriptor.Descriptor(
    name="Empty",
    full_name="Empty",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=133,
    serialized_end=140,
)


_FILTER = _descriptor.Descriptor(
    name="Filter",
    full_name="Filter",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="names",
            full_name="Filter.names",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="ignore_unknown",
            full_name="Filter.ignore_unknown",
            index=1,
            number=2,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=142,
    serialized_end=189,
)

_RESULT.fields_by_name["code"].enum_type = _RESULTCODE
_RESULTSTATUS.fields_by_name["r"].message_type = _RESULT
DESCRIPTOR.message_types_by_name["Result"] = _RESULT
DESCRIPTOR.message_types_by_name["ResultStatus"] = _RESULTSTATUS
DESCRIPTOR.message_types_by_name["Empty"] = _EMPTY
DESCRIPTOR.message_types_by_name["Filter"] = _FILTER
DESCRIPTOR.enum_types_by_name["ResultCode"] = _RESULTCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Result = _reflection.GeneratedProtocolMessageType(
    "Result",
    (_message.Message,),
    {
        "DESCRIPTOR": _RESULT,
        "__module__": "grpc_helper.api.common_pb2"
        # @@protoc_insertion_point(class_scope:Result)
    },
)
_sym_db.RegisterMessage(Result)

ResultStatus = _reflection.GeneratedProtocolMessageType(
    "ResultStatus",
    (_message.Message,),
    {
        "DESCRIPTOR": _RESULTSTATUS,
        "__module__": "grpc_helper.api.common_pb2"
        # @@protoc_insertion_point(class_scope:ResultStatus)
    },
)
_sym_db.RegisterMessage(ResultStatus)

Empty = _reflection.GeneratedProtocolMessageType(
    "Empty",
    (_message.Message,),
    {
        "DESCRIPTOR": _EMPTY,
        "__module__": "grpc_helper.api.common_pb2"
        # @@protoc_insertion_point(class_scope:Empty)
    },
)
_sym_db.RegisterMessage(Empty)

Filter = _reflection.GeneratedProtocolMessageType(
    "Filter",
    (_message.Message,),
    {
        "DESCRIPTOR": _FILTER,
        "__module__": "grpc_helper.api.common_pb2"
        # @@protoc_insertion_point(class_scope:Filter)
    },
)
_sym_db.RegisterMessage(Filter)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
