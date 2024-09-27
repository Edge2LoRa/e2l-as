import os
import base64
import time
from Crypto.PublicKey import ECC
import logging
import psutil
import grpc
from e2gw_rpc_client import (
    edge2gateway_pb2_grpc,
    EdPubInfo,
    E2LDeviceInfo,
    E2LDevicesInfoComplete,
    Device,
    ActiveFlag,
)
from .__private__ import (
    demo_pb2_grpc,
    SendStatistics,
    SendLogMessage,
    SendJoinUpdateMessage,
)
from mqtt_module import MQTTModule
import json
import hashlib
from threading import Thread, Lock
from pymongo import MongoClient
from datetime import datetime

log = logging.getLogger(__name__)

### LORAWAN PORTS
DEFAULT_APP_PORT = 2
DEFAULT_E2L_JOIN_PORT = 3
DEFAULT_E2L_APP_PORT = 4
DEFAULT_E2L_COMMAND_PORT = 5

# EDGE2LORA COMMAND
REJOIN_COMMAND = "REJOIN"

# LOG TYPE
LOG_GW1 = 1
LOG_GW2 = 2
LOG_ED = 3

# FRAME TYPES
EDGE_FRAME = 1
LEGACY_FRAME = 2
EDGE_FRAME_NOT_PROCESSING = 3
EDGE_FRAME_AGGREGATE = 4

# MONGO DB DOC TYPE
STATS_DOC_TYPE = "stats"
LOG_DOC_TYPE = "logs"
LOG_V2_DOC_TYPE = "logs_v2"
SYS_DOC_TYPE = "sys"
GW_FRAMES_STATS_DOC_TYPE = "gw_stats"

# DASHBOARD CONNECT TIMEOUT
DASHBOARD_TIMEOUT_SEC = 5


class E2LoRaModule:
    """
    This class is handle the Edge2LoRa Protocol.
    """

    def __init__(self, dashboard_rpc_endpoint, experiment_id):
        # Generate ephimeral ecc private/public key pair
        self.ephimeral_private_key = ECC.generate(curve="P-256")
        self.ephimeral_public_key = self.ephimeral_private_key.public_key()
        self.ephimeral_public_key_bytes_compressed = (
            self.ephimeral_public_key.export_key(format="SEC1")
        )
        # Init active directory
        self.active_directory = {"e2gws": {}, "e2eds": {}}
        # Statistics collection utils
        self.statistics = {
            "dm": {"rx_legacy_frames": 0, "rx_e2l_frames": 0},
            "gateways": {},
            "devices": {},
            "ns": {"tx": 0, "rx": 0},
            "aggregation_result": 0,
        }
        self.e2gw_ids = []
        self.e2ed_ids = []
        self.ed_ids = []
        self.legacy_not_duplicates = {}
        self.legacy_dropped = 0
        self.legacy_not_duplicates_lock = Lock()
        # Setup experiment
        self.last_stats = None
        self.default_sleep_seconds = 5
        self.experiment_id = None
        self.db_client = None
        self.db = None
        self.collection = None
        self.dashboard_rpc_stub = None
        if experiment_id is not None:
            self.experiment_id = experiment_id
            mongo_host = os.getenv("MONGO_HOST", "localhost")
            mongo_port = os.getenv("MONGO_PORT", 27017)
            if isinstance(mongo_port, str) and mongo_port.isnumeric():
                mongo_port = int(mongo_port)
            self.db_client = MongoClient(mongo_host, mongo_port)
            db_name = os.getenv("MONGO_DB_NAME", "experiments_db")
            self.db = self.db_client[db_name]
            if experiment_id not in self.db.list_collection_names():
                self.db.create_collection(experiment_id)
                self.collection = self.db[experiment_id]
            else:
                # raise exception
                raise Exception(
                    "Experiment ID already exists, please change the experiment ID."
                )
        else:
            try:
                channel = grpc.insecure_channel(dashboard_rpc_endpoint)
                grpc.channel_ready_future(channel).result(timeout=DASHBOARD_TIMEOUT_SEC)
                self.dashboard_rpc_stub = demo_pb2_grpc.GRPCDemoStub(channel)
            except:
                log.info("DASHBOARD RPC ENDPOINT NOT AVAILABLE.")
                self.dashboard_rpc_stub = None
        #############################
        #   INIT TTS MQTT CLIENT    #
        #############################
        log.debug("Connecting to TTS MQTT broker...")
        self.tts_mqtt_client = MQTTModule(
            username=os.getenv("TTS_MQTT_USERNAME"),
            password=os.getenv("TTS_MQTT_PASSWORD"),
            host=os.getenv("TTS_MQTT_HOST"),
            port=int(os.getenv("TTS_MQTT_PORT")),
        )
        log.debug("Connected to TTS MQTT broker")
        #############################
        #   INIT E2L MQTT CLIENT    #
        #############################
        log.debug("Connecting to E2L MQTT broker...")
        time.sleep(DASHBOARD_TIMEOUT_SEC)
        self.e2l_mqtt_client = MQTTModule(
            username=os.getenv("E2L_MQTT_USERNAME"),
            password=os.getenv("E2L_MQTT_PASSWORD"),
            host=os.getenv("E2L_MQTT_HOST"),
            port=int(os.getenv("E2L_MQTT_PORT")),
        )
        self.input_process_topic = os.getenv("E2L_MQTT_AGGR_INPUT_TOPIC")
        self.control_base_topic = os.getenv("E2L_MQTT_CONTROL_BASE_TOPIC")
        log.debug("Connected to E2L MQTT broker")
        # Aggregation Utils
        self.ed_1_gw_selection = None
        self.ed_2_gw_selection = None
        self.ed_3_gw_selection = None
        # Load Device JSON
        split_devices = os.getenv("SPLIT_DEVICES")
        if split_devices is None or not split_devices.isnumeric():
            raise ("SPLIT_DEVICES SHOULD BE AN INTEGER")
        self.split_devices = int(split_devices)
        if self.split_devices < 0:
            self.split_devices = 0
        gw_number = os.getenv("GW_NUMBER")
        if gw_number is None or not gw_number.isnumeric():
            raise ("GW_NUMBER SHOULD BE AN INTEGER")
        self.gw_number = int(gw_number)
        if self.gw_number < 0:
            self.gw_number = 0
        self._load_device_json()
        # MOBILITY
        self.mobility = os.getenv("ENABLE_MOBILITY", "0") == "1"
        # GW shit mode
        gw_shut_enabled = os.getenv("GW_SHUT", "0")
        self.gw_shut_enabled = True if gw_shut_enabled == "1" else False
        if self.gw_shut_enabled:
            self.gw_shut_done = False
            device_number = os.getenv("DEVICE_NUMBER", "0")
            packet_number = os.getenv("PACKET_NUMBER", "0")
            packet_divisor = os.getenv("PACKET_DIVISOR", "4")
            if (
                packet_number.isnumeric()
                and device_number.isnumeric()
                and packet_divisor.isnumeric()
            ):
                packet_number = int(packet_number)
                device_number = int(device_number)
                packet_divisor = int(packet_divisor)
                if packet_number <= 0 or device_number <= 0:
                    self.gw_shut_enabled = False
                else:
                    self.gw_shut_packet_limit = int(
                        (packet_number * device_number) / packet_divisor
                    )
            else:
                self.gw_shut_enabled = False

    """
        @brief this function return the current date and time in ISOString.
        @return ISOString (str)
        @note "YYYY-mm-ddTHH:MM:SS.ffffffZ"
    """

    def _get_now_isostring(self):
        # get current daste time in ISOString format
        return f'{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")}Z'

    """
        @brief this function load the device info from a JSON file.
        @param None
        @return None
        @note the file shall be in the same format as the The Things Stack device bulk import JSON file
    """

    def _load_device_json(self):
        filename = os.getenv("DEVICE_LIST_FILE")
        if filename is None:
            return
        device_list = []
        with open(filename, "r") as file:
            device_list = json.load(file)
        for device in device_list:
            dev_id = device.get("ids", {}).get("dev_id")
            dev_eui = device.get("ids", {}).get("dev_eui")
            dev_addr = device.get("session", {}).get("dev_addr")
            edgeSEncKey = (
                device.get("session", {})
                .get("keys", {})
                .get("app_s_key", {})
                .get("key")
            )
            edgeSIntKey = (
                device.get("session", {})
                .get("keys", {})
                .get("f_nwk_s_int_key", {})
                .get("key")
            )
            if self.statistics.get("devices").get(dev_eui) is None:
                self.statistics["devices"][dev_eui] = {
                    "dev_addr": dev_addr,
                    "legacy_frames": 0,
                    "edge_frames": 0,
                }
            else:
                self.statistics["devices"][dev_eui]["dev_addr"] = dev_addr

            if dev_eui not in self.ed_ids:
                self.e2ed_ids.append(dev_eui)

            dev_obj = {
                "dev_id": dev_id,
                "dev_eui": dev_eui,
                "dev_addr": dev_addr,
                "e2gw": None,
                "edgeSIntKey": edgeSIntKey,
                "edgeSEncKey": edgeSEncKey,
            }
            self.active_directory["e2eds"][dev_eui] = dev_obj

    """
        @brief this function send log to the dashboard
        @param type: log type <LOG_GW1|LOG_GW2|LOG_ED>
        @param message: log message
    """

    def _send_log(self, type, message):
        if self.collection is not None:
            log_obj = {
                "_id": self._get_now_isostring(),
                "type": LOG_DOC_TYPE,
                "key_agreement_log_message_node_id": type,
                "key_agreement_message_log": message,
                "key_agreement_process_time": 0,
            }
            self.collection.insert_one(log_obj)
            return
        elif self.dashboard_rpc_stub is not None:
            request = SendLogMessage(
                client_id=1,
                message_data="",
                key_agreement_log_message_node_id=type,
                key_agreement_message_log=message,
                key_agreement_process_time=0,
            )
            log.debug(f"Sending log to dashboard: {type}\t{message}")
            response = self.dashboard_rpc_stub.SimpleMethodsLogMessage(request)
        else:
            pass

    """
        @brief this function push a log document in the MongoDB collection
        @param log_obj: dict to be pushed into the DB
        @return 0 if success, -1 if error
    """

    def _push_log_to_db(self, log_obj):
        if self.collection is None:
            return -1
        timetag_dm = int(round(time.time() * 1000))
        log_obj["_id"] = self._get_now_isostring()
        log_obj["timetag_dm"] = timetag_dm
        log_obj["type"] = LOG_V2_DOC_TYPE
        log.debug(f"PUSHING AGGREGATE INFO IN DB: {log_obj}")
        self.collection.insert_one(log_obj)
        return 0

    """
        @brief  This function collect the stats
        @return The updated dict containing the stats
    """

    def _get_db_stats(self):
        gw_1_info = {}
        gw_2_info = {}
        if len(self.e2gw_ids) > 0:
            gw_1_info = self.statistics["gateways"][self.e2gw_ids[0]]
        if len(self.e2gw_ids) > 1:
            gw_2_info = self.statistics["gateways"][self.e2gw_ids[1]]
        ns_info = self.statistics.get("ns", {})
        dm_info = self.statistics.get("dm", {})
        new_stats_data = {
            "gw_1_received_frame_num": gw_1_info.get("rx", 0),
            "gw_1_transmitted_frame_num": gw_1_info.get("tx", 0),
            "gw_2_received_frame_num": gw_2_info.get("rx", 0),
            "gw_2_transmitted_frame_num": gw_2_info.get("tx", 0),
            "ns_received_frame_num": ns_info.get("rx", 0),
            "ns_transmitted_frame_num": ns_info.get("tx", 0),
            "ns_dropped_legacy_frames": self.legacy_dropped,
            "dm_received_frame_num": dm_info.get("rx_legacy_frames", 0)
            + dm_info.get("rx_e2l_frames", 0),
            "dm_received_legacy_frame_num": dm_info.get("rx_legacy_frames", 0),
            "dm_received_e2l_frame_num": dm_info.get("rx_e2l_frames", 0),
            "aggregation_function_result": self.statistics.get("aggregation_result", 0),
        }
        stats_data = None
        if self.last_stats is not None:
            stats_data = {
                "gw_1_received_frame_num": new_stats_data.get(
                    "gw_1_received_frame_num", 0
                )
                - self.last_stats.get("gw_1_received_frame_num", 0),
                "gw_1_transmitted_frame_num": new_stats_data.get(
                    "gw_1_transmitted_frame_num", 0
                )
                - self.last_stats.get("gw_1_transmitted_frame_num", 0),
                "gw_2_received_frame_num": new_stats_data.get(
                    "gw_2_received_frame_num", 0
                )
                - self.last_stats.get("gw_2_received_frame_num", 0),
                "gw_2_transmitted_frame_num": new_stats_data.get(
                    "gw_2_transmitted_frame_num", 0
                )
                - self.last_stats.get("gw_2_transmitted_frame_num", 0),
                "ns_received_frame_num": new_stats_data.get("ns_received_frame_num", 0)
                - self.last_stats.get("ns_received_frame_num", 0),
                "ns_transmitted_frame_num": new_stats_data.get(
                    "ns_transmitted_frame_num", 0
                )
                - self.last_stats.get("ns_transmitted_frame_num", 0),
                "ns_dropped_legacy_frames": new_stats_data.get(
                    "ns_dropped_legacy_frames", 0
                )
                - self.last_stats.get("ns_dropped_legacy_frames", 0),
                "dm_received_frame_num": new_stats_data.get("dm_received_frame_num", 0)
                - self.last_stats.get("dm_received_frame_num", 0),
                "dm_received_legacy_frame_num": new_stats_data.get(
                    "dm_received_legacy_frame_num", 0
                )
                - self.last_stats.get("dm_received_legacy_frame_num", 0),
                "dm_received_e2l_frame_num": new_stats_data.get(
                    "dm_received_e2l_frame_num", 0
                )
                - self.last_stats.get("dm_received_e2l_frame_num", 0),
                "aggregation_function_result": self.statistics.get(
                    "aggregation_result", 0
                ),
            }
        else:
            stats_data = new_stats_data
        self.last_stats = new_stats_data
        return stats_data

    """
        @brief  This function collect the stats and return a SendStatistics object
        @return The updated SendStatistics object
    """

    def _get_stats(self):
        for i in range(1):
            gw_1_info = {}
            gw_2_info = {}
            if len(self.e2gw_ids) > 0:
                gw_1_info = self.statistics["gateways"][self.e2gw_ids[0]]
            if len(self.e2gw_ids) > 1:
                gw_2_info = self.statistics["gateways"][self.e2gw_ids[1]]
            ns_info = self.statistics.get("ns", {})
            dm_info = self.statistics.get("dm", {})
            request = SendStatistics(
                client_id=1,
                message_data="",
                gw_1_received_frame_num=gw_1_info.get("rx", 0),
                gw_1_transmitted_frame_num=gw_1_info.get("tx", 0),
                gw_2_received_frame_num=gw_2_info.get("rx", 0),
                gw_2_transmitted_frame_num=gw_2_info.get("tx", 0),
                ns_received_frame_frame_num=ns_info.get("rx", 0),
                ns_transmitted_frame_frame_num=ns_info.get("tx", 0),
                module_received_frame_frame_num=dm_info.get("rx_legacy_frames", 0)
                + dm_info.get("rx_e2l_frames", 0),
                aggregation_function_result=self.statistics.get(
                    "aggregation_result", 0
                ),
            )
            yield request
            # time.sleep(5)

    """
        @brief This function updated the paramenters according to the settings of the dashboard.
                It can trigger a change in the aggregation function and window size of the gateways, or
                change the E2GW for the E2EDs.
        @param ed_1_gw_selection: the gateway index to be used for the first E2ED
        @param ed_2_gw_selection: the gateway index to be used for the second E2ED
        @param ed_3_gw_selection: the gateway index to be used for the third E2ED
        @param aggregation_function: the aggregation function to be used for the gateways
        @param window_size: the window size to be used for the gateways
        @return None
    """

    def _update_params(self, ed_1_gw_selection, ed_2_gw_selection, ed_3_gw_selection):

        rejoin_command_base64 = base64.b64encode(REJOIN_COMMAND.encode("utf-8")).decode(
            "utf-8"
        )

        # UPDATE ED 1 GW SELECTION
        if ed_1_gw_selection is not None and len(self.e2gw_ids) >= ed_1_gw_selection:
            self.ed_1_gw_selection = ed_1_gw_selection
            if len(self.e2ed_ids) > 0:
                dev_eui = self.e2ed_ids[0]
                new_e2gw_id = self.e2gw_ids[self.ed_1_gw_selection - 1]
                e2ed_info = self.active_directory["e2eds"].get(dev_eui)
                if e2ed_info is not None:
                    e2ed_addr = e2ed_info.get("dev_addr")
                    old_e2gw_id = e2ed_info.get("e2gw")
                    if new_e2gw_id != old_e2gw_id:
                        self.active_directory["e2eds"][dev_eui]["e2gw"] = new_e2gw_id
                        dev_id = e2ed_info.get("dev_id")
                        self._send_downlink_frame(
                            base64_message=rejoin_command_base64,
                            dev_id=dev_id,
                            lorawan_port=DEFAULT_E2L_COMMAND_PORT,
                            priority="HIGHEST",
                        )
                        old_gw_info = self.active_directory["e2gws"].get(old_e2gw_id)
                        if old_gw_info is not None:
                            old_e2gw_stub = old_gw_info.get("e2gw_stub")
                            if old_e2gw_stub is not None:
                                e2ed_data = old_e2gw_stub.remove_e2device(
                                    E2LDeviceInfo(
                                        dev_eui=dev_eui,
                                        dev_addr=e2ed_info.get("dev_addr"),
                                    )
                                )
                                if e2ed_data.status_code == 0:
                                    log_message = f"Removed E2ED {e2ed_addr} from E2GW"
                                    self.handle_edge_data(
                                        gw_id=old_e2gw_id,
                                        dev_eui=dev_eui,
                                        dev_addr=e2ed_addr,
                                        aggregated_data=e2ed_data.aggregated_data,
                                        delta_time=0,
                                        gw_log_message=log_message,
                                    )

        # UPDATE ED 2 GW SELECTION
        if ed_2_gw_selection is not None and len(self.e2gw_ids) >= ed_2_gw_selection:
            self.ed_2_gw_selection = ed_2_gw_selection
            if len(self.e2ed_ids) > 1:
                dev_eui = self.e2ed_ids[1]
                new_e2gw_id = self.e2gw_ids[self.ed_2_gw_selection - 1]
                e2ed_info = self.active_directory["e2eds"].get(dev_eui)
                if e2ed_info is not None:
                    e2ed_addr = e2ed_info.get("dev_addr")
                    old_e2gw_id = e2ed_info.get("e2gw")
                    if new_e2gw_id != old_e2gw_id:
                        self.active_directory["e2eds"][dev_eui]["e2gw"] = new_e2gw_id
                        dev_id = e2ed_info.get("dev_id")
                        self._send_downlink_frame(
                            base64_message=rejoin_command_base64,
                            dev_id=dev_id,
                            lorawan_port=DEFAULT_E2L_COMMAND_PORT,
                            priority="HIGHEST",
                        )
                        old_gw_info = self.active_directory["e2gws"].get(old_e2gw_id)
                        if old_gw_info is not None:
                            old_e2gw_stub = old_gw_info.get("e2gw_stub")
                            if old_e2gw_stub is not None:
                                e2ed_data = old_e2gw_stub.remove_e2device(
                                    E2LDeviceInfo(
                                        dev_eui=dev_eui,
                                        dev_addr=e2ed_info.get("dev_addr"),
                                    )
                                )
                                if e2ed_data.status_code == 0:
                                    log_message = f"Removed E2ED {e2ed_addr} from E2GW"
                                    self.handle_edge_data(
                                        gw_id=old_e2gw_id,
                                        dev_eui=dev_eui,
                                        dev_addr=e2ed_addr,
                                        aggregated_data=e2ed_data.aggregated_data,
                                        delta_time=0,
                                        gw_log_message=log_message,
                                    )

        # UPDATE ED 3 GW SELECTION
        if ed_3_gw_selection is not None and len(self.e2gw_ids) >= ed_3_gw_selection:
            self.ed_3_gw_selection = ed_3_gw_selection
            if len(self.e2ed_ids) > 2:
                dev_eui = self.e2ed_ids[2]
                new_e2gw_id = self.e2gw_ids[self.ed_3_gw_selection - 1]
                e2ed_info = self.active_directory["e2eds"].get(dev_eui)
                if e2ed_info is not None:
                    e2ed_addr = e2ed_info.get("dev_addr")
                    old_e2gw_id = e2ed_info.get("e2gw")
                    if new_e2gw_id != old_e2gw_id:
                        self.active_directory["e2eds"][dev_eui]["e2gw"] = new_e2gw_id
                        dev_id = e2ed_info.get("dev_id")
                        self._send_downlink_frame(
                            base64_message=rejoin_command_base64,
                            dev_id=dev_id,
                            lorawan_port=DEFAULT_E2L_COMMAND_PORT,
                            priority="HIGHEST",
                        )
                        old_gw_info = self.active_directory["e2gws"].get(old_e2gw_id)
                        if old_gw_info is not None:
                            old_e2gw_stub = old_gw_info.get("e2gw_stub")
                            if old_e2gw_stub is not None:
                                e2ed_data = old_e2gw_stub.remove_e2device(
                                    E2LDeviceInfo(
                                        dev_eui=dev_eui,
                                        dev_addr=e2ed_addr,
                                    )
                                )
                                if (
                                    e2ed_data.status_code == 0
                                    and e2ed_data.aggregated_data_num > 0
                                ):
                                    log_message = f"Removed E2ED {e2ed_addr} from E2GW"
                                    self.handle_edge_data(
                                        gw_id=old_e2gw_id,
                                        dev_eui=dev_eui,
                                        dev_addr=e2ed_addr,
                                        aggregated_data=e2ed_data.aggregated_data,
                                        delta_time=0,
                                        gw_log_message=log_message,
                                    )

    """
        @brief  This function is used to periodically push the stats to the DB.
        @return None
    """

    def _update_db(self):
        while True:
            time.sleep(self.default_sleep_seconds)
            stats_obj = self._get_db_stats()
            stats_obj["_id"] = self._get_now_isostring()
            stats_obj["type"] = STATS_DOC_TYPE
            log.debug("Pushing new stats obj to DB...")
            self.collection.insert_one(stats_obj)
            log.debug("Stats pushed to DB.")

    """
        @brief  This function is used to periodically send the stats to the dashboard, and get the new settings.
        @return None
    """

    def _update_dashboard(self):
        while True:
            log.debug("Sending statistics to dashboard")
            response = self.dashboard_rpc_stub.ClientStreamingMethodStatistics(
                self._get_stats()
            )
            log.debug(f"Received commands from dashboard:\n{response}")
            ed_1_gw_selection = response.ed_1_gw_selection
            ed_2_gw_selection = response.ed_2_gw_selection
            ed_3_gw_selection = response.ed_3_gw_selection
            self._update_params(ed_1_gw_selection, ed_2_gw_selection, ed_3_gw_selection)
            time.sleep(self.default_sleep_seconds)

    """
        @brief  This function is used to periodically send the resources stats of the DM to the DB.
        @return None
    """

    def _monitor_resource(self):
        while True:
            mem_info = psutil.virtual_memory()
            memory_usage = mem_info.used
            memory_available = mem_info.available
            cpu_usage = psutil.cpu_percent()
            dm_sys_stats = {
                "_id": self._get_now_isostring(),
                "gw_id": "DM",
                "memory_usage": memory_usage,
                "memory_available": memory_available,
                "cpu_usage": cpu_usage,
                "data_received": 0,
                "data_transmitted": 0,
                "type": SYS_DOC_TYPE,
            }
            log.debug("Pushing sys stats in DB")
            self.collection.insert_one(dm_sys_stats)
            time.sleep(1)

    """
        @brief this function shut the GW2 and performa the handover of the e2ed to GW1
        @return 0 if success, -1 if failed.
    """

    def _shut_gw(self):
        if len(self.e2ed_ids) < 2:
            return -1
        # GET STUB OF GW TO SHUT
        shut_gw_id = self.e2gw_ids[1]
        shut_gw_info = self.active_directory["e2gws"].get(shut_gw_id, {})
        shut_gw_stub = shut_gw_info.get("e2gw_stub")
        if shut_gw_stub is None:
            return -1
        self.gw_shut_done = True
        # GET STUB OF GW TO PERFORM HANDOVER
        handover_gw_id = self.e2gw_ids[0]
        handover_gw_info = self.active_directory["e2gws"].get(handover_gw_id, {})
        handover_gw_stub = handover_gw_info.get("e2gw_stub")
        if handover_gw_stub is None:
            return -1

        # SHUT GW
        shut_gw_stub.set_active(ActiveFlag(is_active=False))
        device_list = []
        for dev_index in range(len(self.e2ed_ids)):
            dev_eui = self.e2ed_ids[dev_index]
            if (
                self.active_directory["e2eds"].get(dev_eui, {}).get("e2gw", "")
                == shut_gw_id
            ):
                self.active_directory["e2eds"][dev_eui]["e2gw"] = handover_gw_id
                edge_s_enc_key = self.active_directory["e2eds"][dev_eui]["edgeSEncKey"]
                edge_s_int_key = self.active_directory["e2eds"][dev_eui]["edgeSIntKey"]
                edge_s_enc_key_bytes = bytes.fromhex(edge_s_enc_key)
                edge_s_int_key_bytes = bytes.fromhex(edge_s_int_key)
                device_list.append(
                    Device(
                        dev_eui=dev_eui,
                        dev_addr=self.active_directory["e2eds"][dev_eui]["dev_addr"],
                        edge_s_enc_key=edge_s_enc_key_bytes,
                        edge_s_int_key=edge_s_int_key_bytes,
                    )
                )
        handover_gw_stub.add_devices(E2LDevicesInfoComplete(device_list=device_list))

        return 0

    """
        @brief  This function is used to send a downlink frame to a ED.
        @param   base64_message: The frame payload to be sent encoded in base64.
        @param   dev_id: The device ID of the ED as in TTS.
        @param   lorawan_port: The port of the ED. (default: 3)
        @param   priority: The priority of the frame. (default: HIGHEST)
        @return   0 is success, < 0 if failure.
    """

    def _send_downlink_frame(
        self, base64_message, dev_id, lorawan_port=3, priority="HIGHEST"
    ):
        downlink_frame = {
            "downlinks": [
                {
                    "f_port": lorawan_port,
                    "frm_payload": base64_message,
                    "priority": priority,
                }
            ]
        }
        downlink_frame_str = json.dumps(downlink_frame)

        base_topic = os.getenv("MQTT_BASE_TOPIC")
        topic = f"{base_topic}{dev_id}/down/replace"

        res = self.tts_mqtt_client.publish_to_topic(
            topic=topic, message=downlink_frame_str
        )

        return 0

    """
        @brief  This funciont handle new public key info received by a GW.
                It initialize a RPC client for each GW.
        @param gw_rpc_endpoint_address: The IP address of the Gateway.
        @param gw_rpc_endpoint_port: The port of the Gateway.
        @param gw_pub_key_bytes: The E2GW Public Key.
        @return 0 is success, < 0 if failure.
        @error code
            -1: Error 
    """

    def handle_gw_pub_info(
        self, gw_rpc_endpoint_address, gw_rpc_endpoint_port, gw_pub_key_compressed
    ):
        # Retireve Info
        gw_pub_key = ECC.import_key(gw_pub_key_compressed, curve_name="P-256")
        g_as_gw_point = gw_pub_key.pointQ * self.ephimeral_private_key.d
        g_as_gw = ECC.construct(
            curve="P-256", point_x=g_as_gw_point.x, point_y=g_as_gw_point.y
        )

        # Init RPC Client
        log.debug(
            f"Init RPC Client for GW {gw_rpc_endpoint_address}:{gw_rpc_endpoint_port}"
        )
        channel = grpc.insecure_channel(
            f"{gw_rpc_endpoint_address}:{gw_rpc_endpoint_port}"
        )
        stub = edge2gateway_pb2_grpc.Edge2GatewayStub(channel)

        self.active_directory["e2gws"][gw_rpc_endpoint_address] = {
            "gw_rpc_endpoint_address": gw_rpc_endpoint_address,
            "gw_rpc_endpoint_port": gw_rpc_endpoint_port,
            "gw_pub_key": gw_pub_key,
            "g_as_gw": g_as_gw,
            "e2gw_stub": stub,
        }
        if self.statistics.get("gateways").get(gw_rpc_endpoint_address) is None:
            self.statistics["gateways"][gw_rpc_endpoint_address] = {"rx": 0, "tx": 0}
        log_type = None
        log_message = ""
        if gw_rpc_endpoint_address not in self.e2gw_ids:
            self.e2gw_ids.append(gw_rpc_endpoint_address)
            log_message = f"Added GW info in DM active directory"
        else:
            log_message = f"Updated GW info in DM active directory"
        # SEND LOG
        index = self.e2gw_ids.index(gw_rpc_endpoint_address)
        log_type = None
        if index == 0:
            log_type = LOG_GW1
        elif index == 1:
            log_type = LOG_GW2
        else:
            log_type = None
        if log_type is not None:
            self._send_log(type=log_type, message=log_message)

        # Check the preloaded devices
        for dev_index in range(len(self.e2ed_ids)):
            # Create Device info
            dev_eui = self.e2ed_ids[dev_index]
            if self.active_directory["e2eds"].get(dev_eui) is None:
                continue
            dev_info = self.active_directory["e2eds"].get(dev_eui)
            edge_s_enc_key = dev_info.get("edgeSEncKey")
            edge_s_int_key = dev_info.get("edgeSIntKey")
            if edge_s_enc_key is None or edge_s_int_key is None:
                continue

            # Check if GW is already assigned.
            assigned_gw = dev_info.get("e2gw")
            if assigned_gw is None:
                gw_index = 0
                if self.split_devices > 0 and self.gw_number > 0:
                    gw_index = int((dev_index / self.split_devices) % self.gw_number)
                if gw_index >= len(self.e2gw_ids):
                    continue
                assigned_gw = self.e2gw_ids[gw_index]
                dev_info["e2gw"] = assigned_gw
            # SEND DEVICE INFO
            unassigned_device_info = {
                "dev_eui": dev_eui,
                "dev_addr": self.active_directory["e2eds"][dev_eui]["dev_addr"],
                "assigned_gw": assigned_gw,
            }
            assigned_device_info = {
                "dev_eui": dev_eui,
                "dev_addr": self.active_directory["e2eds"][dev_eui]["dev_addr"],
                "edge_s_enc_key": edge_s_enc_key,
                "edge_s_int_key": edge_s_int_key,
            }
            for gw_id in self.active_directory["e2gws"].keys():
                log.debug(f"Sending {dev_eui} info to {gw_id}")
                if gw_id == assigned_gw:
                    self.e2l_mqtt_client.publish_to_topic(
                        topic=f"{gw_id}/{self.control_base_topic}/add_assigned_device",
                        message=json.dumps(assigned_device_info),
                    )
                else:
                    self.e2l_mqtt_client.publish_to_topic(
                        topic=f"{gw_id}/{self.control_base_topic}/add_unassigned_device",
                        message=json.dumps(unassigned_device_info),
                    )

        return 0

    """
        @brief  This function handle new join request received by a ED.
        @param dev_eui: The Dev EUI.
        @param dev_addr: The Dev Addr.
    """

    def handle_otaa_join_request(self, dev_id, dev_eui, dev_addr):
        # SEND LOG
        # if len(self.e2ed_ids) < 1 or (dev_eui in self.e2ed_ids and self.e2ed_ids.index(dev_eui) == 0):
        self._send_log(
            type=LOG_ED, message=f"Dev {dev_eui} OTAA Activated. (Addr: {dev_addr})"
        )

        if self.statistics.get("devices").get(dev_eui) is None:
            self.statistics["devices"][dev_eui] = {
                "dev_addr": dev_addr,
                "legacy_frames": 0,
                "edge_frames": 0,
            }
        else:
            self.statistics["devices"][dev_eui]["dev_addr"] = dev_addr

        if dev_eui not in self.ed_ids:
            self.e2ed_ids.append(dev_eui)
        return 0

    """
        @brief  This function handle new public key info received by a ED.
                It complete the process of key agreement for the server.
        @param dev_eui: The Dev EUI.
        @param dev_addr: The Dev Addr.
        @param dev_pub_key_compressed: The Compressed Dev Public Key.
        @return 0 is success, < 0 if failure.
        @error code:
            -1: Error 
    """

    def handle_edge_join_request(
        self, dev_id, dev_eui, dev_addr, dev_pub_key_compressed_base_64
    ):
        # SEND LOG
        # if len(self.e2ed_ids) < 1 or (dev_eui in self.e2ed_ids and self.e2ed_ids.index(dev_eui) == 0):
        self._send_log(type=LOG_ED, message=f"Starting Edge Join (Dev: {dev_addr})")

        dev_obj = None
        e2gw = None
        # Check if ED is already registered
        if self.active_directory["e2eds"].get(dev_eui) is None:
            # Assign E2GW to E2ED and store informations
            selected_e2gw = 1
            if dev_eui in self.e2ed_ids:
                ed_index = self.e2ed_ids.index(dev_eui)
                if ed_index == 0:
                    selected_e2gw = self.ed_1_gw_selection
                elif ed_index == 1:
                    selected_e2gw = self.ed_2_gw_selection
                elif ed_index == 2:
                    selected_e2gw = self.ed_3_gw_selection
                else:
                    pass
            else:
                ed_next_index = len(self.e2ed_ids)
                if ed_next_index == 0:
                    selected_e2gw = self.ed_1_gw_selection
                elif ed_next_index == 1:
                    selected_e2gw = self.ed_2_gw_selection
                elif ed_next_index == 2:
                    selected_e2gw = self.ed_3_gw_selection
                else:
                    pass

            if len(self.e2gw_ids) > 0:
                if len(self.e2gw_ids) < selected_e2gw:
                    e2gw = self.active_directory["e2gws"].get(self.e2gw_ids[0])
                else:
                    e2gw = self.active_directory["e2gws"].get(
                        self.e2gw_ids[selected_e2gw - 1]
                    )
            if e2gw is None:
                log.error("No E2GW found")
                return -1
            dev_obj = {
                "dev_id": dev_id,
                "dev_eui": dev_eui,
                "dev_addr": dev_addr,
                "e2gw": e2gw.get("gw_rpc_endpoint_address"),
            }
        else:
            dev_obj = self.active_directory["e2eds"].get(dev_eui)
            e2gw = self.active_directory["e2gws"].get(dev_obj.get("e2gw"))
            log.debug(f"E2ED: {dev_eui} already registered")
            log.debug(f'E2GW: {dev_obj.get("e2gw")}')
            if e2gw is None:
                log.error("No E2GW found")
                return -1
        # SEND LOG
        # if len(self.e2ed_ids) < 1 or  (dev_eui in self.e2ed_ids and self.e2ed_ids.index(dev_eui) == 0):
        self._send_log(type=LOG_ED, message=f"Send EdgeJoinRequest (Dev: {dev_addr})")
        # Get g_as_gw
        g_as_gw = e2gw.get("g_as_gw")
        # Schedule downlink to ed with g_as_gw
        # encode g_as_gw in base64
        g_as_gw_exported = g_as_gw.export_key(format="SEC1")
        g_as_gw_base_64 = base64.b64encode(g_as_gw_exported).decode("utf-8")
        _downlink_frame = self._send_downlink_frame(
            base64_message=g_as_gw_base_64, dev_id=dev_id
        )
        # SEND LOG
        # if len(self.e2ed_ids) < 1 or  (dev_eui in self.e2ed_ids and self.e2ed_ids.index(dev_eui) == 0):
        self._send_log(
            type=LOG_ED, message=f"Received EdgeAcceptRequest (Dev: {dev_addr})"
        )

        # Generate g_as_ed
        # Decode base64
        dev_pub_key_compressed = base64.b64decode(dev_pub_key_compressed_base_64)
        dev_pub_key = ECC.import_key(dev_pub_key_compressed, curve_name="P-256")
        g_as_ed = dev_pub_key.pointQ * self.ephimeral_private_key.d
        g_as_ed_bytes = ECC.construct(
            curve="P-256", point_x=g_as_ed.x, point_y=g_as_ed.y
        ).export_key(format="SEC1")

        ### Send g_as_ed to e2gw
        e2gw_rpc_stub = e2gw.get("e2gw_stub")
        ed_pub_info = EdPubInfo(
            dev_eui=dev_eui,
            dev_addr=dev_addr,
            g_as_ed=g_as_ed_bytes,
            dev_public_key=dev_pub_key_compressed,
        )
        response = e2gw_rpc_stub.handle_ed_pub_info(ed_pub_info)
        g_gw_ed_bytes = response.g_gw_ed
        g_gw_ed = ECC.import_key(g_gw_ed_bytes, curve_name="P-256")
        edgeSKey_int = self.ephimeral_private_key.d * g_gw_ed.pointQ
        edgeSKey = edgeSKey_int.x.to_bytes()
        # SEND LOG
        index = self.e2gw_ids.index(e2gw.get("gw_rpc_endpoint_address"))
        log_type = None
        if index == 0:
            log_type = LOG_GW1
        elif index == 1:
            log_type = LOG_GW2
        else:
            log_type = None
        if log_type is not None:
            self._send_log(
                type=log_type, message=f"Received Device {dev_addr} Public Info"
            )

        # Hash edgeSKey
        edgeSIntKey = b"\x00" + edgeSKey
        edgeSEncKey = b"\x01" + edgeSKey
        edgeSIntKey = hashlib.sha256(edgeSIntKey).digest()[:16]
        edgeSEncKey = hashlib.sha256(edgeSEncKey).digest()[:16]
        log.info(f"edgeSIntKey: {[x for x in edgeSIntKey]}")
        log.info(f"edgeSEncKey: {[x for x in edgeSEncKey]}")

        # Store device info
        dev_obj["edgeSIntKey"] = edgeSIntKey
        dev_obj["edgeSEncKey"] = edgeSEncKey
        self.active_directory["e2eds"][dev_eui] = dev_obj
        if dev_eui not in self.e2ed_ids:
            self.e2ed_ids.append(dev_eui)

        # SEND LOG
        # if self.e2ed_ids.index(dev_eui) == 0:
        self._send_log(
            type=LOG_ED,
            message=f'Edge Join Completed (Dev: {dev_addr}, GW: {self.e2gw_ids.index(e2gw.get("gw_rpc_endpoint_address"))+1})',
        )
        if log_type is not None:
            self._send_log(
                type=log_type, message=f"Edge Join Completed (Dev: {dev_addr})"
            )

        # UPDATE DASHBOARD NETWORK TOPOLOGY
        if self.dashboard_rpc_stub is not None:
            join_update_message = SendJoinUpdateMessage(
                client_id=1,
                message_data="",
                ed_id=self.e2ed_ids.index(dev_eui) + 1,
                gw_id=self.e2gw_ids.index(e2gw.get("gw_rpc_endpoint_address")) + 1,
            )
            ret = self.dashboard_rpc_stub.SimpleMethodsJoinUpdateMessage(
                join_update_message
            )

        return 0

    """
        @brief  This function handle new edge frame received by an ED, passing by the legacy route.
        @param dev_id: The Dev ID as in TTS.
        @param dev_eui: The Dev EUI.
        @param dev_addr: The Dev Addr.
        @param frame_payload: The Frame Payload.
        @return 0 is success, < 0 if failure.
    """

    def handle_edge_data_from_legacy(self, dev_id, dev_eui, dev_addr, frame_payload):
        return 0

    """
        @brief  This function handle new legacy frame received by an ED, passing by the legacy route.
        @param dev_id: The Dev ID as in TTS.
        @param dev_eui: The Dev EUI.
        @param dev_addr: The Dev Addr.
        @param frame_payload: The Frame Payload.
        @return 0 is success, < 0 if failure.
    """

    def handle_legacy_data(
        self,
        dev_id,
        dev_eui,
        dev_addr,
        fcnt,
        rx_timestamp,
        frame_payload_base64,
        payload,
    ):
        # decode frame_payload_base64
        frame_payload = base64.b64decode(frame_payload_base64).decode("utf-8")
        log.debug(
            f"Received Legacy Frame from Legacy Route. Data: {frame_payload}. Dev: {dev_addr}."
        )
        self.statistics["dm"]["rx_legacy_frames"] = (
            self.statistics["dm"].get("rx_legacy_frames", 0) + 1
        )
        # self.statistics["ns"]["rx"] = self.statistics["ns"].get("rx", 0) + 1
        self.statistics["ns"]["tx"] = self.statistics["ns"].get("tx", 0) + 1

        up_msg = payload.get("uplink_message")
        uplink_message = payload.get("uplink_message")
        fcnt = uplink_message.get("f_cnt")
        rx_metadata = uplink_message.get("rx_metadata")[0]
        gw_info = rx_metadata.get("gateway_ids", {})
        gtw_id = gw_info.get("eui", "")
        rx_timestamp = rx_metadata.get("timestamp")
        rx_time = rx_timestamp.get("time", "")
        gtw_rssi = rx_metadata.get("rssi", 0)
        gtw_snr = rx_metadata.get("snr", 0.0)
        gtw_channel = rx_metadata.get("channel_index", 0)

        settings = uplink_message.get("settings", {})
        frequency_str = settings.get("frequency", "0.0")
        # convert frequency_str from Hz to MHz
        frequency = float(frequency_str) / 1_000_000.0

        data_rate = settings.get("data_rate", {}).get("lora", {})
        bandwidth = data_rate.get("bandwidth", 0.0) / 1_000.0
        spreading_factor = data_rate.get("spreading_factor", 0)
        data_rate_str = f"SF{spreading_factor}BW{int(bandwidth)}"

        coding_rate = settings.get("coding_rate", "")
        mqtt_payload = {
            "dev_eui": dev_eui,
            "dev_addr": dev_addr,
            "fcnt": fcnt,
            "timestamp": rx_time,
            "frequency": frequency,
            "data_rate": data_rate_str,
            "coding_rate": coding_rate,
            "gtw_id": gtw_id,
            "gtw_channel": gtw_channel,
            "gtw_rssi": gtw_rssi,
            "gtw_snr": gtw_snr,
            "payload": frame_payload_base64,
        }
        self.e2l_mqtt_client.publish_to_topic(
            topic=self.input_process_topic, message=json.dumps(mqtt_payload)
        )

        timestamp = rx_timestamp
        if frame_payload.isnumeric():
            timestamp = int(frame_payload)
        log_obj = {
            "module_id": "DM",
            "log_message": f"Legacy frame from {dev_addr}",
            "frame_type": LEGACY_FRAME,
            "fcnt": fcnt,
            "timetag": timestamp,
        }
        self._push_log_to_db(
            log_obj=log_obj,
        )
        return 0

    def _handle_mobility(self, payload):
        rx_process_gws = payload.get("rx_process_gw")
        dev_addrs = payload.get("devaddrs")

        devices_info = {}
        for index in range(len(dev_addrs)):
            dev_addr = dev_addrs[index]
            if devices_info.get(dev_addr) is None:
                devices_info[dev_addr] = {"total_packets": 0, "rx_gws": {}}
            device_info = devices_info[dev_addr]
            rx_process_gw = rx_process_gws[index]
            rx_gw = rx_process_gw[0]
            if device_info["rx_gws"].get(rx_gw) is None:
                device_info["rx_gws"][rx_gw] = 0
            device_info["rx_gws"][rx_gw] += 1
            device_info["total_packets"] += 1

        for dev_addr in devices_info.keys():
            # Retrieve Device OBJ
            # dev_obj = {
            #     "dev_id": dev_id,
            #     "dev_eui": dev_eui,
            #     "dev_addr": dev_addr,
            #     "e2gw": None,
            #     "edgeSIntKey": edgeSIntKey,
            #     "edgeSEncKey": edgeSEncKey,
            # }
            # self.active_directory["e2eds"][dev_eui] = dev_obj
            dev_obj = None
            for dev_obj_iter in self.active_directory["e2eds"].values():
                if dev_obj_iter.get("dev_addr") == dev_addr:
                    dev_obj = dev_obj_iter
                    break
            if dev_obj is None:
                continue

            # CHECK MOST USED GW
            device_info = devices_info[dev_addr]
            total_packets = device_info["total_packets"]
            rx_gws = device_info["rx_gws"]
            new_gw = None
            for gw in rx_gws.keys():
                if rx_gws[gw] / total_packets >= (1.0 / float(self.gw_number)):
                    new_gw = gw
                    break

            if dev_obj["e2gw"] == new_gw:
                continue

            # UPDATE ACTIVE DIRECTORY
            dev_obj["e2gw"] = new_gw

            dev_eui = dev_obj.get("dev_eui")
            dev_addr = dev_obj.get("dev_addr")
            assigned_gw = new_gw
            edge_s_int_key = dev_obj.get("edgeSIntKey")
            edge_s_enc_key = dev_obj.get("edgeSEncKey")
            # SEND DEVICE INFO
            unassigned_device_info = {
                "dev_eui": dev_eui,
                "dev_addr": dev_addr,
                "assigned_gw": assigned_gw,
            }
            assigned_device_info = {
                "dev_eui": dev_eui,
                "dev_addr": dev_addr,
                "edge_s_enc_key": edge_s_enc_key,
                "edge_s_int_key": edge_s_int_key,
            }
            for gw_id in self.active_directory["e2gws"].keys():
                log.debug(f"Sending {dev_eui} info to {gw_id}")
                if gw_id == assigned_gw:
                    self.e2l_mqtt_client.publish_to_topic(
                        topic=f"{gw_id}/{self.control_base_topic}/add_assigned_device",
                        message=json.dumps(assigned_device_info),
                    )
                else:
                    self.e2l_mqtt_client.publish_to_topic(
                        topic=f"{gw_id}/{self.control_base_topic}/add_unassigned_device",
                        message=json.dumps(unassigned_device_info),
                    )

        return 0

    """
        @brief  This function handle new edge frame received by an ED, passing by the E2ED route.
        @param gw_id: The GW ID.
        @param dev_eui: The Dev EUI.
        @param dev_addr: The Dev Addr.
        @param aggregated_data: The Aggregated Data.
        @param delta_time: The Delta Time.
        @return 0 is success, < 0 if failure.
    """

    def handle_edge_data(
        self,
        payload,
        gw_log_message=None,
    ):
        dev_addr = payload.get("dev_addr")
        gw_id = payload.get("gw_id")
        dev_eui = payload.get("dev_eui")
        aggregated_data = payload.get("aggregated_data")
        log.debug(
            f"Received Edge Frame from E2ED. Dev Addr: {dev_addr}. E2GW: {gw_id}."
        )

        # PUSH LOG
        payload["module_id"] = "DM"
        payload["log_message"] = f"Received Aggregate Frame from {dev_addr}"
        payload["frame_type"] = EDGE_FRAME_AGGREGATE
        payload["type"] = LOG_V2_DOC_TYPE
        self._push_log_to_db(log_obj=payload)

        # CHECK MOBILITY
        if self.mobility:
            self._handle_mobility(payload=payload)

        self.statistics["dm"]["rx_e2l_frames"] = (
            self.statistics["dm"].get("rx_e2l_frames", 0) + 1
        )
        if gw_id not in self.e2gw_ids:
            return -1
        self.statistics["gateways"][gw_id]["tx"] = (
            self.statistics["gateways"][gw_id].get("tx", 0) + 1
        )

        # SEND LOG
        if self.dashboard_rpc_stub is not None and dev_eui is not None:
            if dev_eui in self.e2ed_ids and self.e2ed_ids.index(dev_eui) == 0:
                self.statistics["aggregation_result"] = aggregated_data
            self._send_log(
                type=LOG_ED, message=f"E2L Frame Received by DM (Dev: {dev_addr})"
            )

        if gw_log_message is not None:
            index = self.e2gw_ids.index(gw_id)
            log_type = None
            if index == 0:
                log_type = LOG_GW1
            elif index == 1:
                log_type = LOG_GW2
            else:
                log_type = None
            if log_type is not None:
                self._send_log(type=log_type, message=gw_log_message)

        return 0

    """
        @brief  Thid function start a thread to handle the dashboard update loop.
        @return None.
    """

    def start_dashboard_update_loop(self):
        if self.collection is not None:
            self.db_update_loop = Thread(target=self._update_db)
            self.db_update_loop.start()
            return
        elif self.dashboard_rpc_stub is not None:
            self.dashboard_update_loop = Thread(target=self._update_dashboard)
            self.dashboard_update_loop.start()
        else:
            pass

    """
        @brief  This function start a thread to monitor the DM resources.
        @return None.
    """

    def start_resource_monitor_loop(self):
        if self.collection is not None:
            self.resource_monitor_loop = Thread(target=self._monitor_resource)
            self.resource_monitor_loop.start()
        return

    """
        @brief  This function handle the gateway log.
        @param gw_id: The gateway id.
        @param log_message: The log message.
        @return 0 is success, -1 if failure.
    """

    def handle_gw_log(self, gw_id, dev_addr, log_message, frame_type, fcnt, timetag):
        if gw_id not in self.e2gw_ids:
            return -1
        # SEND LOG
        index = self.e2gw_ids.index(gw_id)
        log_type = None
        if index == 0:
            log_type = LOG_GW1
        elif index == 1:
            log_type = LOG_GW2
        else:
            log_type = None
        if log_type is not None and self.collection is None:
            self._send_log(type=log_type, message=log_message)

        if log_type is None:
            return

        log_obj = {
            "module_id": gw_id,
            "log_message": log_message,
            "frame_type": frame_type,
            "fcnt": fcnt,
            "timetag": timetag,
        }
        self._push_log_to_db(log_obj=log_obj)

        return 0

    """
        @brief  This function handle the system log from the GWs.
        @param gw_id: The gateway id.
        @param memory_usage: The memory usage.
        @param memory_available: The memory available.
        @param cpu_usage: The cpu usage.
        @param data_received: The data received.
        @param data_transmitted: The data transmitted.
        @return 0 is success, -1 if failure.
    """

    def handle_sys_log(
        self,
        gw_id,
        memory_usage,
        memory_available,
        cpu_usage,
        data_received,
        data_transmitted,
    ):
        gw_sys_stats = {
            "_id": self._get_now_isostring(),
            "gw_id": gw_id,
            "memory_usage": memory_usage,
            "memory_available": memory_available,
            "cpu_usage": cpu_usage,
            "data_received": data_received,
            "data_transmitted": data_transmitted,
            "type": SYS_DOC_TYPE,
        }
        if self.collection is not None and gw_id in self.e2gw_ids:
            log.debug("Pushing sys stats in DB")
            self.collection.insert_one(gw_sys_stats)
        self._update_params(None, None, None)
        return 0

    """
        @brief  This function handle the gateway frames stats.
        @param gw_id: The gateway id.
        @param legacy_frames: The legacy frames counter.
        @param legacy_fcnts: The legacy frame fcnts.
        @param edge_frames: The edge frames counter.
        @param edge_fcnts: The edge frame fcnts.
        @param edge_not_processed_frames: The edge not processed frames counter.
        @param edge_not_processed_fcnts: The edge not processed frame fcnts.
        @return 0 is success, -1 if failure.
    """

    def handle_gw_frames_stats(
        self,
        gw_id,
        legacy_frames,
        legacy_fcnts,
        edge_frames,
        edge_fcnts,
        edge_not_processed_frames,
        edge_not_processed_fcnts,
    ):
        if self.collection is None:
            return -1
        gw_frames_stats = {
            "_id": self._get_now_isostring(),
            "gw_id": gw_id,
            "legacy_frames": legacy_frames,
            "legacy_fcnts": legacy_fcnts,
            "edge_frames": edge_frames,
            "edge_fcnts": edge_fcnts,
            "edge_not_processed_frames": edge_not_processed_frames,
            "edge_not_processed_fcnts": edge_not_processed_fcnts,
            "type": GW_FRAMES_STATS_DOC_TYPE,
        }
        log.debug("Pushing frames stats in DB")
        self.collection.insert_one(gw_frames_stats)

        # UPDATE SINK STATS
        self.statistics["gateways"][gw_id]["rx"] = (
            self.statistics["gateways"][gw_id].get("rx", 0)
            + edge_frames
            + edge_not_processed_frames
            + legacy_frames
        )

        self.statistics["gateways"][gw_id]["tx"] = (
            self.statistics["gateways"][gw_id].get("tx", 0) + legacy_frames
        )

        # CHECK IF GW TO SHUT
        index = self.e2gw_ids.index(gw_id)
        if (
            index is not None
            and index == 1
            and self.gw_shut_enabled
            and not self.gw_shut_done
            and self.statistics["gateways"][gw_id]["rx"] >= self.gw_shut_packet_limit
        ):
            shut_thread = Thread(target=self._shut_gw)
            shut_thread.start()

    """
        @brief: This function is called when a new message is received from the
                MQTT broker.
        @param client: The client object.
        @param userdata: The user data.
        @param message: The message.
        @return: None.
    """

    def _tts_subscribe_callback(self, client, userdata, message):
        log.debug("######### Received message from TTS")
        topic = message.topic
        payload_str = message.payload.decode("utf-8")
        payload = json.loads(payload_str)
        end_devices_infos = payload.get("end_device_ids")
        dev_id = end_devices_infos.get("device_id")
        dev_eui = end_devices_infos.get("dev_eui")
        dev_addr = end_devices_infos.get("dev_addr")
        if "/join" in topic:
            ret = self.handle_otaa_join_request(
                dev_id=dev_id, dev_eui=dev_eui, dev_addr=dev_addr
            )
            return ret
        up_msg = payload.get("uplink_message")
        up_port = up_msg.get("f_port")
        uplink_message = payload.get("uplink_message")
        fcnt = uplink_message.get("f_cnt")
        rx_metadata = uplink_message.get("rx_metadata")[0]
        rx_timestamp = rx_metadata.get("timestamp")
        frame_payload = uplink_message.get("frm_payload")
        ret = 0
        if up_port == DEFAULT_APP_PORT:
            log.debug("Received Legacy Frame")
            return self.handle_legacy_data(
                dev_id, dev_eui, dev_addr, fcnt, rx_timestamp, frame_payload, payload
            )
        elif up_port == DEFAULT_E2L_JOIN_PORT:
            log.debug("Received Edge Join Frame")
            ret = self.handle_edge_join_request(
                dev_id=dev_id,
                dev_eui=dev_eui,
                dev_addr=dev_addr,
                dev_pub_key_compressed_base_64=frame_payload,
            )
        elif up_port == DEFAULT_E2L_APP_PORT:
            log.debug("Received Edge Frame")
            ret = self.handle_edge_data_from_legacy(
                dev_id, dev_eui, dev_addr, frame_payload
            )
        else:
            log.warning(f"Unknown frame port: {up_port}")

        if ret < 0:
            log.error(f"Error handling frame: {ret}")

        return ret

    """
        @brief  This function init the tts mqtt client object.
        @return None.
    """

    def _init_tts_mqtt_client(self):
        # SUBSCRIBE TO UPLINK MESSAGE TOPIC
        uplink_topic = os.getenv("TTS_MQTT_UPLINK_TOPIC")
        log.debug(f"Subscribing to TTS MQTT topic {uplink_topic}...")
        self.tts_mqtt_client.subscribe_to_topic(
            topic=uplink_topic, callback=self._tts_subscribe_callback
        )
        log.debug(f"Subscribed to E2L MQTT topic {uplink_topic}")

        # SUBSCRIBE TO JOIN MESSAGE TOPIC
        join_topic = os.getenv("TTS_MQTT_OTAA_TOPIC")
        log.debug(f"Subscribing to TTS MQTT topic {join_topic}...")
        self.tts_mqtt_client.subscribe_to_topic(
            topic=join_topic, callback=self._tts_subscribe_callback
        )
        log.debug(f"Subscribed to TTS MQTT topic {join_topic}")

    """
        @brief  This function wait for messages from the TTS MQTT broker.
        @return None.
        @note   This function is blocking and should never return.
    """

    def _tts_mqtt_client_wait_for_message(self):
        log.info("Waiting for messages from TTS MQTT broker...")
        self.tts_mqtt_client.wait_for_message()

    def _e2l_subscribe_callback(self, client, userdata, message):
        """
        {
            'devaddr': '0036D012',
            'aggregated_data': {'avg_rssi': -33.0, 'avg_snr': 9.2},
            'fcnts': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
            'timestamps': [1714138009, 1714138010, 1714138010, 1714138011, 1714138011, 1714138011, 1714138012, 1714138013, 1714138013, 1714138013, 1714138014, 1714138014, 1714138014, 1714138014, 1714138014, 1714138015, 1714138015],
            'timestamp_pub': 1714138021072
        }

        def handle_edge_data(
            self,
            gw_id,
            dev_eui,
            dev_addr,
            aggregated_data,
            fcnts,
            dev_addrs,
            timetag,
            gw_log_message=None,
        ):
        """
        payload = json.loads(message.payload)
        topic = message.topic
        gw_id = topic.split("/")[0]
        # dev_addr = payload.get("devaddr")
        # dev_addrs = payload.get("devaddrs")
        # if dev_addrs is None or len(dev_addrs) == 0:
        #     for dev_eui_it, dev_info in self.active_directory["e2eds"].items():
        #         if dev_info["dev_addr"] == dev_addr:
        #             dev_eui = dev_eui_it
        #             break
        # else:
        #      dev_eui = None

        payload["gw_id"] = gw_id
        # payload["dev_eui"] = dev_eui

        log.debug(f"Received edge data from {gw_id}")# with dev_addr {dev_addr}")
        log.debug(f"PAYLOAD: {payload}")

        self.handle_edge_data(
            payload=payload,
            gw_log_message=None,
        )

    """
        @brief  This function init the e2l mqtt client object.
        @return None.
    """

    def _init_e2l_mqtt_client(self):
        # SUBSCRIBE TO AGGREGATE MESSAGE TOPIC
        aggr_topic = os.getenv("E2L_MQTT_AGGR_OUTPUT_TOPIC")
        log.debug(f"Subscribing to E2L MQTT topic {aggr_topic}...")
        self.e2l_mqtt_client.subscribe_to_topic(
            topic=aggr_topic, callback=self._e2l_subscribe_callback
        )
        log.debug(f"Subscribed to E2L MQTT topic {aggr_topic}")

    """
        @brief  This function wait for messages from the E2L MQTT broker.
        @return None.
        @note   This function is blocking and should never return.
    """

    def _e2l_mqtt_client_wait_for_message(self):
        log.info("Waiting for messages from E2L MQTT broker...")
        self.e2l_mqtt_client.wait_for_message()

    def mqtt_clients_init(self):
        self._init_tts_mqtt_client()
        self._init_e2l_mqtt_client()

    def mqtt_clients_wait_for_message(self):
        tts_thread = Thread(target=self._tts_mqtt_client_wait_for_message)
        e2l_thread = Thread(target=self._e2l_mqtt_client_wait_for_message)
        tts_thread.start()
        e2l_thread.start()
        tts_thread.join()
        e2l_thread.join()
