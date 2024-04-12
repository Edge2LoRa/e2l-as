from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["client_id", "request_data"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    request_data: str
    def __init__(self, client_id: _Optional[int] = ..., request_data: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["server_id", "response_data"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendStatistics(_message.Message):
    __slots__ = ["client_id", "message_data", "gw_1_received_frame_num", "gw_1_transmitted_frame_num", "gw_2_received_frame_num", "gw_2_transmitted_frame_num", "ns_received_frame_frame_num", "ns_transmitted_frame_frame_num", "module_received_frame_frame_num", "aggregation_function_result"]
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
    def __init__(self, client_id: _Optional[int] = ..., message_data: _Optional[str] = ..., gw_1_received_frame_num: _Optional[int] = ..., gw_1_transmitted_frame_num: _Optional[int] = ..., gw_2_received_frame_num: _Optional[int] = ..., gw_2_transmitted_frame_num: _Optional[int] = ..., ns_received_frame_frame_num: _Optional[int] = ..., ns_transmitted_frame_frame_num: _Optional[int] = ..., module_received_frame_frame_num: _Optional[int] = ..., aggregation_function_result: _Optional[int] = ...) -> None: ...

class ReplyStatistics(_message.Message):
    __slots__ = ["server_id", "response_data", "ed_1_gw_selection", "ed_2_gw_selection", "ed_3_gw_selection", "start_key_agreement_process", "process_function", "process_window", "change_processing_configuraiton"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    ED_1_GW_SELECTION_FIELD_NUMBER: _ClassVar[int]
    ED_2_GW_SELECTION_FIELD_NUMBER: _ClassVar[int]
    ED_3_GW_SELECTION_FIELD_NUMBER: _ClassVar[int]
    START_KEY_AGREEMENT_PROCESS_FIELD_NUMBER: _ClassVar[int]
    PROCESS_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    PROCESS_WINDOW_FIELD_NUMBER: _ClassVar[int]
    CHANGE_PROCESSING_CONFIGURAITON_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    ed_1_gw_selection: int
    ed_2_gw_selection: int
    ed_3_gw_selection: int
    start_key_agreement_process: int
    process_function: str
    process_window: int
    change_processing_configuraiton: int
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ..., ed_1_gw_selection: _Optional[int] = ..., ed_2_gw_selection: _Optional[int] = ..., ed_3_gw_selection: _Optional[int] = ..., start_key_agreement_process: _Optional[int] = ..., process_function: _Optional[str] = ..., process_window: _Optional[int] = ..., change_processing_configuraiton: _Optional[int] = ...) -> None: ...

class SendLogMessage(_message.Message):
    __slots__ = ["client_id", "message_data", "key_agreement_log_message_node_id", "key_agreement_message_log", "key_agreement_process_time"]
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
    __slots__ = ["server_id", "response_data"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendJoinUpdateMessage(_message.Message):
    __slots__ = ["client_id", "message_data", "ed_id", "gw_id"]
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
    __slots__ = ["server_id", "response_data"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendLogED(_message.Message):
    __slots__ = ["client_id", "message_data", "ed_key_agreement_message_log", "key_agreement_process_time"]
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
    __slots__ = ["server_id", "response_data"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendLogGW(_message.Message):
    __slots__ = ["client_id", "message_data", "gw_1_agreement_message_log", "key_agreement_process_time"]
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
    __slots__ = ["server_id", "response_data"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...

class SendLogDM(_message.Message):
    __slots__ = ["client_id", "message_data", "module_key_agreement_message_log", "key_agreement_process_time"]
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
    __slots__ = ["server_id", "response_data"]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    response_data: str
    def __init__(self, server_id: _Optional[int] = ..., response_data: _Optional[str] = ...) -> None: ...
