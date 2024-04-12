import paho.mqtt.client as mqtt
import logging 



class MQTTModule():

    def __init__(self, **kwargs) -> None:
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        host = kwargs.get('host', None)
        port = kwargs.get('port', None)
        client_id = kwargs.get('client_id', __name__)
        clean_session = kwargs.get('clean_session', True)
        e2l_module = kwargs.get('e2l_module', None)
        if username is None or password is None or host is None or port is None or e2l_module is None:
            raise Exception('Missing parameters')
        self.client = mqtt.Client(
            client_id =client_id,
            clean_session=clean_session,
            protocol = mqtt.MQTTv311
        )
        self.client.username_pw_set(username, password)
        self.client.connect(host, port, 60)
        # e2l Module
        self.e2l_module = e2l_module

    def _callback(self, client, userdata, message):
        self.callback(self, userdata, message)

    def enable_logger(self, enable = True):
        if enable:
            self.client.enable_logger(logging.getLogger(__name__))
        else:
            self.client.disable_logger()

    def subscribe_to_topic(self, topic: str, callback):
        self.client.subscribe(topic)
        self.callback = callback
        self.client.on_message = self._callback

    def wait_for_message(self):
        self.client.loop_forever()

    def publish_to_topic(self, topic, message):
        return self.client.publish(
            topic=topic, 
            payload=message
            )