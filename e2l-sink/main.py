import os, sys
import logging
from dateutil.parser import isoparse
from concurrent import futures

import grpc
from rpc_module import edge2applicationserver_pb2_grpc
from rpc_module import Edge2LoRaApplicationServer

from mqtt_module import MQTTModule
import json

from e2l_module import (
    E2LoRaModule,
    DEFAULT_APP_PORT,
    DEFAULT_E2L_APP_PORT,
    DEFAULT_E2L_JOIN_PORT,
)

DEBUG = os.getenv("DEBUG", False)
DEBUG = True if DEBUG == "1" else False
if DEBUG:
    from dotenv import load_dotenv

    load_dotenv()
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

"""
    @brief: This function is used to check if the environment variables are set.
    @return: True if all environment variables are set, False otherwise.
    @rtype: bool
"""


def check_env_vars() -> bool:
    env_vars = [
        "MQTT_USERNAME",
        "MQTT_PASSWORD",
        "MQTT_HOST",
        "MQTT_PORT",
        "MQTT_BASE_TOPIC",
        "MQTT_UPLINK_TOPIC",
        "MQTT_OTAA_TOPIC",
        "DASHBOARD_RPC_HOST",
        "DASHBOARD_RPC_PORT",
        "RPC_SERVER_PORT",
    ]
    for var in env_vars:
        if os.getenv(var) is None:
            log.error(f"{var} not set")
            exit(1)
        if "_PORT" in var:
            if not os.getenv(var).isnumeric():
                log.error(f"{var} must be numeric")
                exit(1)
            if int(os.getenv(var)) < 0 or int(os.getenv(var)) > 65535:
                log.error(f"{var} must be between 0 and 65535")
                exit(1)
    return True


"""
    @brief: This function is called when a new message is received from the
            MQTT broker.
    @param client: The client object.
    @param userdata: The user data.
    @param message: The message.
    @return: None.
"""


def subscribe_callback(client, userdata, message):
    topic = message.topic
    payload_str = message.payload.decode("utf-8")
    payload = json.loads(payload_str)
    end_devices_infos = payload.get("end_device_ids")
    dev_id = end_devices_infos.get("device_id")
    dev_eui = end_devices_infos.get("dev_eui")
    dev_addr = end_devices_infos.get("dev_addr")
    if "/join" in topic:
        ret = client.e2l_module.handle_otaa_join_request(
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
        return client.e2l_module.handle_legacy_data(
            dev_id, dev_eui, dev_addr, fcnt, rx_timestamp, frame_payload
        )
    elif up_port == DEFAULT_E2L_JOIN_PORT:
        log.debug("Received Edge Join Frame")
        ret = client.e2l_module.handle_edge_join_request(
            dev_id=dev_id,
            dev_eui=dev_eui,
            dev_addr=dev_addr,
            dev_pub_key_compressed_base_64=frame_payload,
        )
    elif up_port == DEFAULT_E2L_APP_PORT:
        log.debug("Received Edge Frame")
        ret = client.e2l_module.handle_edge_data_from_legacy(
            dev_id, dev_eui, dev_addr, frame_payload
        )
    else:
        log.warning(f"Unknown frame port: {up_port}")

    if ret < 0:
        log.error(f"Error handling frame: {ret}")

    return ret


def edge_callback(data):
    log.debug(f"Received data: {data}")
    return data


if __name__ == "__main__":
    log.info("Starting...")
    #####################
    #   CHECK ENV VARS  #
    #####################
    check_env_vars()

    #####################
    #   GET LINE ARGS   #
    #####################
    experiment_id = None
    if len(sys.argv) > 1:
        experiment_id = sys.argv[1]

    #####################
    #   INIT E2L MODULE #
    #####################
    dashboard_rpc_endpoint = None
    if experiment_id is None:
        dashboard_rpc_endpoint = (
            f'{os.getenv("DASHBOARD_RPC_HOST")}:{os.getenv("DASHBOARD_RPC_PORT")}'
        )
    e2l_module = E2LoRaModule(
        dashboard_rpc_endpoint=dashboard_rpc_endpoint, experiment_id=experiment_id
    )
    e2l_module.start_dashboard_update_loop()
    e2l_module.start_resource_monitor_loop()

    #####################
    #   INIT RPC SERVER #
    #####################
    rpc_server_instance = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    e2l_server = Edge2LoRaApplicationServer(e2l_module=e2l_module)
    edge2applicationserver_pb2_grpc.add_Edge2ApplicationServerServicer_to_server(
        e2l_server, rpc_server_instance
    )
    rpc_server_instance.add_insecure_port(f'[::]:{os.getenv("RPC_SERVER_PORT")}')
    rpc_server_instance.start()
    log.info("Started RPC server")

    #########################
    #   INIT MQTT CLIENT    #
    #########################
    log.debug("Connecting to MQTT broker...")
    mqqt_client = MQTTModule(
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
        host=os.getenv("MQTT_HOST"),
        port=int(os.getenv("MQTT_PORT")),
        e2l_module=e2l_module,
    )
    log.debug("Connected to MQTT broker")

    # SUBSCRIBE TO TOPIC
    uplink_topic = os.getenv("MQTT_UPLINK_TOPIC")
    join_topic = os.getenv("MQTT_OTAA_TOPIC")
    log.debug(f"Subscribing to MQTT topic {uplink_topic}...")
    mqqt_client.subscribe_to_topic(topic=uplink_topic, callback=subscribe_callback)
    log.debug(f"Subscribed to MQTT topic {uplink_topic}")
    log.debug(f"Subscribing to MQTT topic {join_topic}...")
    mqqt_client.subscribe_to_topic(topic=join_topic, callback=subscribe_callback)
    log.debug(f"Subscribed to MQTT topic {join_topic}")

    # PASS MQTT CLIENT TO E2L MODULE
    e2l_module.set_mqtt_client(mqqt_client)

    log.info("Waiting for messages from MQTT broker...")
    mqqt_client.wait_for_message()

    log.warning("Done, should never reach this point!")
    sys.exit(0)
