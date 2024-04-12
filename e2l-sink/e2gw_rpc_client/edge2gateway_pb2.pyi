from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActiveFlag(_message.Message):
    __slots__ = ["is_active"]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    is_active: bool
    def __init__(self, is_active: bool = ...) -> None: ...

class EdPubInfo(_message.Message):
    __slots__ = ["dev_eui", "dev_addr", "g_as_ed", "dev_public_key"]
    DEV_EUI_FIELD_NUMBER: _ClassVar[int]
    DEV_ADDR_FIELD_NUMBER: _ClassVar[int]
    G_AS_ED_FIELD_NUMBER: _ClassVar[int]
    DEV_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    dev_eui: str
    dev_addr: str
    g_as_ed: bytes
    dev_public_key: bytes
    def __init__(self, dev_eui: _Optional[str] = ..., dev_addr: _Optional[str] = ..., g_as_ed: _Optional[bytes] = ..., dev_public_key: _Optional[bytes] = ...) -> None: ...

class GwInfo(_message.Message):
    __slots__ = ["status_code", "g_gw_ed"]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    G_GW_ED_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    g_gw_ed: bytes
    def __init__(self, status_code: _Optional[int] = ..., g_gw_ed: _Optional[bytes] = ...) -> None: ...

class AggregationParams(_message.Message):
    __slots__ = ["aggregation_function", "window_size"]
    AGGREGATION_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    WINDOW_SIZE_FIELD_NUMBER: _ClassVar[int]
    aggregation_function: int
    window_size: int
    def __init__(self, aggregation_function: _Optional[int] = ..., window_size: _Optional[int] = ...) -> None: ...

class GwResponse(_message.Message):
    __slots__ = ["status_code", "message"]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    message: str
    def __init__(self, status_code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class E2LDeviceInfo(_message.Message):
    __slots__ = ["dev_eui", "dev_addr"]
    DEV_EUI_FIELD_NUMBER: _ClassVar[int]
    DEV_ADDR_FIELD_NUMBER: _ClassVar[int]
    dev_eui: str
    dev_addr: str
    def __init__(self, dev_eui: _Optional[str] = ..., dev_addr: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["dev_eui", "dev_addr", "edge_s_enc_key", "edge_s_int_key"]
    DEV_EUI_FIELD_NUMBER: _ClassVar[int]
    DEV_ADDR_FIELD_NUMBER: _ClassVar[int]
    EDGE_S_ENC_KEY_FIELD_NUMBER: _ClassVar[int]
    EDGE_S_INT_KEY_FIELD_NUMBER: _ClassVar[int]
    dev_eui: str
    dev_addr: str
    edge_s_enc_key: bytes
    edge_s_int_key: bytes
    def __init__(self, dev_eui: _Optional[str] = ..., dev_addr: _Optional[str] = ..., edge_s_enc_key: _Optional[bytes] = ..., edge_s_int_key: _Optional[bytes] = ...) -> None: ...

class E2LDevicesInfoComplete(_message.Message):
    __slots__ = ["device_list"]
    DEVICE_LIST_FIELD_NUMBER: _ClassVar[int]
    device_list: _containers.RepeatedCompositeFieldContainer[Device]
    def __init__(self, device_list: _Optional[_Iterable[_Union[Device, _Mapping]]] = ...) -> None: ...

class E2LData(_message.Message):
    __slots__ = ["status_code", "dev_eui", "dev_addr", "aggregated_data", "aggregated_data_num", "timetag"]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    DEV_EUI_FIELD_NUMBER: _ClassVar[int]
    DEV_ADDR_FIELD_NUMBER: _ClassVar[int]
    AGGREGATED_DATA_FIELD_NUMBER: _ClassVar[int]
    AGGREGATED_DATA_NUM_FIELD_NUMBER: _ClassVar[int]
    TIMETAG_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    dev_eui: str
    dev_addr: str
    aggregated_data: int
    aggregated_data_num: int
    timetag: int
    def __init__(self, status_code: _Optional[int] = ..., dev_eui: _Optional[str] = ..., dev_addr: _Optional[str] = ..., aggregated_data: _Optional[int] = ..., aggregated_data_num: _Optional[int] = ..., timetag: _Optional[int] = ...) -> None: ...
