from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR: _ClassVar[Status]
    SUCCESS: _ClassVar[Status]
ERROR: Status
SUCCESS: Status

class TaskStatusRequest(_message.Message):
    __slots__ = ("task_uid",)
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    def __init__(self, task_uid: _Optional[str] = ...) -> None: ...

class TaskStartRequest(_message.Message):
    __slots__ = ("task_uid", "command")
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    command: str
    def __init__(self, task_uid: _Optional[str] = ..., command: _Optional[str] = ...) -> None: ...

class TaskDeleteRequest(_message.Message):
    __slots__ = ("task_uid",)
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    def __init__(self, task_uid: _Optional[str] = ...) -> None: ...

class TaskReloadRequest(_message.Message):
    __slots__ = ("task_uid",)
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    def __init__(self, task_uid: _Optional[str] = ...) -> None: ...

class TaskLogsOpenRequest(_message.Message):
    __slots__ = ("task_uid",)
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    def __init__(self, task_uid: _Optional[str] = ...) -> None: ...

class TaskLogsCloseRequest(_message.Message):
    __slots__ = ("task_uid",)
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    def __init__(self, task_uid: _Optional[str] = ...) -> None: ...

class PipRequest(_message.Message):
    __slots__ = ("package_name",)
    PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    package_name: str
    def __init__(self, package_name: _Optional[str] = ...) -> None: ...

class ExtendUpdateRequest(_message.Message):
    __slots__ = ("task_uid", "extend_info")
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    EXTEND_INFO_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    extend_info: str
    def __init__(self, task_uid: _Optional[str] = ..., extend_info: _Optional[str] = ...) -> None: ...

class ResultWriteRequest(_message.Message):
    __slots__ = ("task_uid", "result_data")
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    RESULT_DATA_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    result_data: bytes
    def __init__(self, task_uid: _Optional[str] = ..., result_data: _Optional[bytes] = ...) -> None: ...

class TaskResponse(_message.Message):
    __slots__ = ("status", "message", "result")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    status: Status
    message: str
    result: bytes
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., message: _Optional[str] = ..., result: _Optional[bytes] = ...) -> None: ...
