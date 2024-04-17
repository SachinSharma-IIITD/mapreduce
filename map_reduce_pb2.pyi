from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class data_point(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class master_to_mapper_task_assign(_message.Message):
    __slots__ = ("start_index", "end_index", "k_clusters", "data_points", "M", "R", "k", "id")
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    END_INDEX_FIELD_NUMBER: _ClassVar[int]
    K_CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    start_index: int
    end_index: int
    k_clusters: _containers.RepeatedCompositeFieldContainer[data_point]
    data_points: _containers.RepeatedCompositeFieldContainer[data_point]
    M: int
    R: int
    k: int
    id: int
    def __init__(self, start_index: _Optional[int] = ..., end_index: _Optional[int] = ..., k_clusters: _Optional[_Iterable[_Union[data_point, _Mapping]]] = ..., data_points: _Optional[_Iterable[_Union[data_point, _Mapping]]] = ..., M: _Optional[int] = ..., R: _Optional[int] = ..., k: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class master_to_reducer_task_assign(_message.Message):
    __slots__ = ("partition_index", "mapper_port", "M", "R", "k", "id")
    PARTITION_INDEX_FIELD_NUMBER: _ClassVar[int]
    MAPPER_PORT_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    partition_index: int
    mapper_port: _containers.RepeatedScalarFieldContainer[int]
    M: int
    R: int
    k: int
    id: int
    def __init__(self, partition_index: _Optional[int] = ..., mapper_port: _Optional[_Iterable[int]] = ..., M: _Optional[int] = ..., R: _Optional[int] = ..., k: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class mapper_to_reducer_data_point(_message.Message):
    __slots__ = ("key", "value", "count")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    key: float
    value: data_point
    count: float
    def __init__(self, key: _Optional[float] = ..., value: _Optional[_Union[data_point, _Mapping]] = ..., count: _Optional[float] = ...) -> None: ...

class master_to_mapper_task_assign_response(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class master_to_reducer_task_assign_response(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class mapper_to_master_file_read_response(_message.Message):
    __slots__ = ("point",)
    POINT_FIELD_NUMBER: _ClassVar[int]
    point: str
    def __init__(self, point: _Optional[str] = ...) -> None: ...

class reducer_to_mapper_file_read(_message.Message):
    __slots__ = ("partition_index", "reducer_id")
    PARTITION_INDEX_FIELD_NUMBER: _ClassVar[int]
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    partition_index: int
    reducer_id: int
    def __init__(self, partition_index: _Optional[int] = ..., reducer_id: _Optional[int] = ...) -> None: ...

class reducer_to_mapper_file_read_response(_message.Message):
    __slots__ = ("data_points", "success")
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    data_points: _containers.RepeatedCompositeFieldContainer[mapper_to_reducer_data_point]
    success: bool
    def __init__(self, data_points: _Optional[_Iterable[_Union[mapper_to_reducer_data_point, _Mapping]]] = ..., success: bool = ...) -> None: ...

class is_alive_response(_message.Message):
    __slots__ = ("alive",)
    ALIVE_FIELD_NUMBER: _ClassVar[int]
    alive: bool
    def __init__(self, alive: bool = ...) -> None: ...
