from copy import deepcopy
import requests
import logging

log = logging.getLogger(__name__)


class E2LBrokerApi(object):

    def __init__(
        self,
        broker_api_username,
        broker_api_password,
        broker_api_host,
        broker_api_port,
        broker_mqtt_username,
        broker_mqtt_password,
    ):
        log.warning(broker_api_username)
        log.warning(broker_api_password)
        url = f"http://{broker_api_host}:{broker_api_port}"
        self.broker_api_endpoint = f"{url}/api/v5"
        self.broker_api_username = broker_api_username
        self.broker_api_password = broker_api_password
        self.default_headers = {"Content-Type": "application/json"}
        self.base_egress_config = {
            "name": None,
            "type": "mqtt",
            "enable": True,
            "resource_opts": {
                "max_buffer_bytes": 104857600,
                "query_mode": "sync",
                "health_check_interval": "15s",
            },
            "server": None,
            "proto_ver": "v5",
            "bridge_mode": True,
            "username": broker_mqtt_username,
            "password": broker_mqtt_password,
            "ssl": {"enable": False},
            "egress": {
                "remote": {
                    "retain": "${retain}",
                    "payload": "${payload}",
                    "topic": "${topic}",
                    "qos": "${qos}",
                },
                "local": {"topic": None},
            },
        }

        pass

    def create_egress_bridge(self, bridge_name, server, topic):
        egress_config = deepcopy(self.base_egress_config)
        egress_config["name"] = bridge_name
        egress_config["server"] = server
        # egress_config["egress"]["remote"][
        #     "topic"
        # ] = f'{bridge_name}/{egress_config["egress"]["remote"]["topic"]}'
        egress_config["egress"]["local"]["topic"] = topic
        log.debug(f"Creating egress bridge: {egress_config}")
        response = requests.post(
            f"{self.broker_api_endpoint}/bridges",
            json=egress_config,
            auth=(self.broker_api_username, self.broker_api_password),
            headers=self.default_headers,
        )

        log.info(response.text)
