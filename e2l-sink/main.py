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
    logging.basicConfig(level=logging.DEBUG)
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
        "TTS_MQTT_USERNAME",
        "TTS_MQTT_PASSWORD",
        "TTS_MQTT_HOST",
        "TTS_MQTT_PORT",
        "TTS_MQTT_BASE_TOPIC",
        "TTS_MQTT_UPLINK_TOPIC",
        "TTS_MQTT_OTAA_TOPIC",
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
    #   INIT MQTT CLIENTS   #
    #########################
    e2l_module.mqtt_clients_init()
    e2l_module.mqtt_clients_wait_for_message()

    log.warning("Done, should never reach this point!")
    sys.exit(0)
