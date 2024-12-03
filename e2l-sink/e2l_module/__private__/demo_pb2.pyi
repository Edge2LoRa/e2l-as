from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ("client_id", "request_data")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    request_data: str
    def __init__(self, client_id: _Optional[int] = ..., request_data: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendStatistics(_message.Message):
    __slots__ = ("client_id", "message_data", "gw_1_received_frame_num", "gw_1_transmitted_frame_num", "gw_2_received_frame_num", "gw_2_transmitted_frame_num", "ns_received_frame_frame_num", "ns_transmitted_frame_frame_num", "module_received_frame_frame_num", "aggregation_function_result", "current_snapshot")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    GW_1_RECEIVED_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    GW_1_TRANSMITTED_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    GW_2_RECEIVED_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    GW_2_TRANSMITTED_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    NS_RECEIVED_FRAME_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    NS_TRANSMITTED_FRAME_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    MODULE_RECEIVED_FRAME_FRAME_NUM_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FUNCTION_RESULT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    message_data: str
    gw_1_received_frame_num: int
    gw_1_transmitted_frame_num: int
    gw_2_received_frame_num: int
    gw_2_transmitted_frame_num: int
    ns_received_frame_frame_num: int
    ns_transmitted_frame_frame_num: int
    module_received_frame_frame_num: int
    aggregation_function_result: int
    current_snapshot: int
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., gw_1_received_frame_num: _Optional[int] = ..., gw_1_transmitted_frame_num: _Optional[int] = ..., gw_2_received_frame_num: _Optional[int] = ..., gw_2_transmitted_frame_num: _Optional[int] = ..., ns_received_frame_frame_num: _Optional[int] = ..., ns_transmitted_frame_frame_num: _Optional[int] = ..., module_received_frame_frame_num: _Optional[int] = ..., aggregation_function_result: _Optional[int] = ..., current_snapshot: _Optional[int] = ...) -> None: ...

class Device_info(_message.Message):
    __slots__ = ("dev_id", "lat", "lon", "temperature", "humidity", "assigned_gw")
    DEV_ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_GW_FIELD_NUMBER: _ClassVar[int]
    dev_id: str
    lat: float
    lon: float
    temperature: float
    humidity: float
    assigned_gw: int
    def __init__(self, dev_id: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., temperature: _Optional[float] = ..., humidity: _Optional[float] = ..., assigned_gw: _Optional[int] = ...) -> None: ...

class Device_info_list(_message.Message):
    __slots__ = ("device_list",)
    DEVICE_LIST_FIELD_NUMBER: _ClassVar[int]
    device_list: _containers.RepeatedCompositeFieldContainer[Device_info]
    def __init__(self, device_list: _Optional[_Iterable[_Union[Device_info, _Mapping]]] = ...) -> None: ...

class Gateway_info(_message.Message):
    __slots__ = ("gw_id", "lat", "lon", "rx_frame", "tx_frame", "processed_frame", "memory", "cpu", "bandwidth_reduction", "coverage", "fwd_frames")
    GW_ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    RX_FRAME_FIELD_NUMBER: _ClassVar[int]
    TX_FRAME_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_FRAME_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_REDUCTION_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    FWD_FRAMES_FIELD_NUMBER: _ClassVar[int]
    gw_id: str
    lat: float
    lon: float
    rx_frame: int
    tx_frame: int
    processed_frame: int
    memory: float
    cpu: float
    bandwidth_reduction: int
    coverage: float
    fwd_frames: int
    def __init__(self, gw_id: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., rx_frame: _Optional[int] = ..., tx_frame: _Optional[int] = ..., processed_frame: _Optional[int] = ..., memory: _Optional[float] = ..., cpu: _Optional[float] = ..., bandwidth_reduction: _Optional[int] = ..., coverage: _Optional[float] = ..., fwd_frames: _Optional[int] = ...) -> None: ...

class Gateway_info_list(_message.Message):
    __slots__ = ("gateway_list",)
    GATEWAY_LIST_FIELD_NUMBER: _ClassVar[int]
    gateway_list: _containers.RepeatedCompositeFieldContainer[Gateway_info]
    def __init__(self, gateway_list: _Optional[_Iterable[_Union[Gateway_info, _Mapping]]] = ...) -> None: ...

class ReplyInfoGwList(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class ReplyInfoDevList(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class ReplyStatistics(_message.Message):
    __slots__ = ("server_id", "response_data", "ed_1_gw_selection", "ed_2_gw_selection", "ed_3_gw_selection", "start_key_agreement_process", "process_function", "process_window", "change_processing_configuraiton", "scenario", "assining_policy", "refreshing_table_rate", "refresh_rate", "current_snapshot_hour")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    ED_1_GW_SELECTION_FIELD_NUMBER: _ClassVar[int]
    ED_2_GW_SELECTION_FIELD_NUMBER: _ClassVar[int]
    ED_3_GW_SELECTION_FIELD_NUMBER: _ClassVar[int]
    START_KEY_AGREEMENT_PROCESS_FIELD_NUMBER: _ClassVar[int]
    PROCESS_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    PROCESS_WINDOW_FIELD_NUMBER: _ClassVar[int]
    CHANGE_PROCESSING_CONFIGURAITON_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_FIELD_NUMBER: _ClassVar[int]
    ASSINING_POLICY_FIELD_NUMBER: _ClassVar[int]
    REFRESHING_TABLE_RATE_FIELD_NUMBER: _ClassVar[int]
    REFRESH_RATE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SNAPSHOT_HOUR_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    ed_1_gw_selection: int
    ed_2_gw_selection: int
    ed_3_gw_selection: int
    start_key_agreement_process: int
    process_function: str
    process_window: int
    change_processing_configuraiton: int
    scenario: str
    assining_policy: str
    refreshing_table_rate: int
    refresh_rate: int
    current_snapshot_hour: int
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ..., ed_1_gw_selection: _Optional[int] = ..., ed_2_gw_selection: _Optional[int] = ..., ed_3_gw_selection: _Optional[int] = ..., start_key_agreement_process: _Optional[int] = ..., process_function: _Optional[str] = ..., process_window: _Optional[int] = ..., change_processing_configuraiton: _Optional[int] = ..., scenario: _Optional[str] = ..., assining_policy: _Optional[str] = ..., refreshing_table_rate: _Optional[int] = ..., refresh_rate: _Optional[int] = ..., current_snapshot_hour: _Optional[int] = ...) -> None: ...

class SendLogMessage(_message.Message):
    __slots__ = ("client_id", "message_data", "key_agreement_log_message_node_id", "key_agreement_message_log", "key_agreement_process_time")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    KEY_AGREEMENT_LOG_MESSAGE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_AGREEMENT_MESSAGE_LOG_FIELD_NUMBER: _ClassVar[int]
    KEY_AGREEMENT_PROCESS_TIME_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    message_data: str
    key_agreement_log_message_node_id: int
    key_agreement_message_log: str
    key_agreement_process_time: int
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., key_agreement_log_message_node_id: _Optional[int] = ..., key_agreement_message_log: _Optional[str] = ..., key_agreement_process_time: _Optional[int] = ...) -> None: ...

class ReplyLogMessage(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendJoinUpdateMessage(_message.Message):
    __slots__ = ("client_id", "message_data", "ed_id", "gw_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    ED_ID_FIELD_NUMBER: _ClassVar[int]
    GW_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    message_data: str
    ed_id: int
    gw_id: int
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., ed_id: _Optional[int] = ..., gw_id: _Optional[int] = ...) -> None: ...

class ReplyJoinUpdateMessage(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendLogED(_message.Message):
    __slots__ = ("client_id", "message_data", "ed_key_agreement_message_log", "key_agreement_process_time")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    ED_KEY_AGREEMENT_MESSAGE_LOG_FIELD_NUMBER: _ClassVar[int]
    KEY_AGREEMENT_PROCESS_TIME_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    message_data: str
    ed_key_agreement_message_log: str
    key_agreement_process_time: int
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., ed_key_agreement_message_log: _Optional[str] = ..., key_agreement_process_time: _Optional[int] = ...) -> None: ...

class ReplyLogED(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendLogGW(_message.Message):
    __slots__ = ("client_id", "message_data", "gw_1_agreement_message_log", "key_agreement_process_time")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    GW_1_AGREEMENT_MESSAGE_LOG_FIELD_NUMBER: _ClassVar[int]
    KEY_AGREEMENT_PROCESS_TIME_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    message_data: str
    gw_1_agreement_message_log: str
    key_agreement_process_time: int
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., gw_1_agreement_message_log: _Optional[str] = ..., key_agreement_process_time: _Optional[int] = ...) -> None: ...

class ReplyLogGW(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendLogDM(_message.Message):
    __slots__ = ("client_id", "message_data", "module_key_agreement_message_log", "key_agreement_process_time")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    MODULE_KEY_AGREEMENT_MESSAGE_LOG_FIELD_NUMBER: _ClassVar[int]
    KEY_AGREEMENT_PROCESS_TIME_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    message_data: str
    module_key_agreement_message_log: str
    key_agreement_process_time: int
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., module_key_agreement_message_log: _Optional[str] = ..., key_agreement_process_time: _Optional[int] = ...) -> None: ...

class ReplyLogDM(_message.Message):
    __slots__ = ("server_id", "response_data")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...
