# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import json
from time import sleep
from typing import Optional

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from communication.messages import MqttUnknownMessageError, MqttTopic, MessageTag, MessageType, Message


def _on_connect(client, userdata, flags, rc):
    """ On connect callback """
    print("Connection to server %s established. Returned code: %d", ["was", "was not"][bool(rc)], rc)


def _on_subscribe(client, userdata, mid, granted_qos):
    """ On subscribe callback """
    print("Successfully subscribed.")


def _on_message(client, userdata, message):
    """ On message callback """
    print("RECEIVED:", message.payload)

    # Sanity check for a topic
    assert MqttTopic.has(message.topic)

    # Echo error if the message is not a JSON string
    try:
        parsed_msg = json.loads(message.payload)
    except json.decoder.JSONDecodeError:
        client.publish(MqttTopic.ERROR, MqttUnknownMessageError())
        return

    # Check if mandatory fields are present
    try:
        parsed_tag = parsed_msg["tag"]
        parsed_type = parsed_msg["mtype"]
    except KeyError:
        client.publish(MqttTopic.ERROR, MqttUnknownMessageError())
        return

    # Echo error if certain message is not expected
    if not MessageTag.has(parsed_tag) or parsed_type != MessageType.REQUEST:
        client.publish(MqttTopic.ERROR, MqttUnknownMessageError())
        return

    # TODO: Handle requests


def _on_publish(client, userdata, mid):
    pass


class MqttHandler:

    def __init__(self, host: str, port: int):
        self.client = mqtt.Client()

        self.client.on_connect = _on_connect
        self.client.on_message = _on_message
        self.client.on_subscribe = _on_subscribe
        self.client.on_publish = _on_publish

        self.client.connect(host, port)
        for topic in MqttTopic.values():
            print("Subscribing to topic", topic)
            self.client.subscribe(topic)

    def __del__(self):
        self.client.disconnect()

    def publish(self, msg: Message, topic: Optional[MqttTopic] = None) -> None:
        if topic is None:
            topic = msg.mtopic

        pub_info = self.client.publish(topic, str(msg))
        if pub_info.rc:
            print("Error when sensing the message. Return code %d", pub_info.rc)
        else:
            print("SENT:", msg)

    @classmethod
    def tx_single(cls, hostname, msg: Message, topic: Optional[MqttTopic] = None) -> None:
        """ Perform quick transmission without initializing the client

        :param hostname: MQTT broker server address
        :param msg: HUB-CLOUD message to be sent
        :param topic: Topic. If None provided, appropriate topic for message type is chosen
        """
        if topic is None:
            topic = msg.mtopic

        publish.single(topic, str(msg), hostname)
        print("SENT:", msg)
