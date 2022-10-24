# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import json
from time import sleep
from typing import Optional

from paho import mqtt
import paho.mqtt.client as mqtt_client
import paho.mqtt.publish as publish

from communication.messages import (
    MqttUnknownMessageError,
    MqttTopic,
    MessageTag,
    MessageType,
    Message,
)


def _on_connect(client, userdata, flags, rc):
    """On connect callback"""
    print(
        "Connection to server %s established. Returned code: %d",
        ["was", "was not"][bool(rc)],
        rc,
    )


def _on_subscribe(client, userdata, mid, granted_qos):
    """On subscribe callback"""
    print("Successfully subscribed.")


def _on_message(client, userdata, message):
    """On message callback"""
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


def _on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


class MqttHandler:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.client = mqtt_client.Client(
            client_id="", userdata=None, protocol=mqtt_client.MQTTv5
        )
        self.client.on_connect = _on_connect

        for topic in MqttTopic.values():
            print("Subscribing to topic", topic)
            self.client.subscribe(topic)

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)

        self.client.on_message = _on_message
        self.client.on_subscribe = _on_subscribe
        self.client.on_publish = _on_publish

    def __del__(self):
        self.client.disconnect()

    def publish(self, msg: Message, topic: Optional[MqttTopic] = None) -> None:
        if topic is None:
            topic = msg.mtopic
        pub_info = self.client.publish(topic, str(msg), qos=0)
        if pub_info.rc:
            print(f"Error when sensing the message. Return code {pub_info.rc}")
        else:
            print("SENT:", msg)

    @classmethod
    def tx_single(
        cls, hostname, msg: Message, topic: Optional[MqttTopic] = None
    ) -> None:
        """Perform quick transmission without initializing the client

        :param hostname: MQTT broker server address
        :param msg: HUB-CLOUD message to be sent
        :param topic: Topic. If None provided, appropriate topic for message type is chosen
        """
        if topic is None:
            topic = msg.mtopic

        publish.single(topic, str(msg), hostname)
        print("SENT:", msg)
