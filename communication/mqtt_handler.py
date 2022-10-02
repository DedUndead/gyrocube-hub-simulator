# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import enum
import json
import paho.mqtt.client as mqtt

from communication.messages import MqttUnknownMessageError, MqttTopic, MessageTag, MessageType


def _on_connect(client, userdata, flags, rc):
    """ On connect callback """
    print("Connection to server %s established. Returned code: %d", ["was", "was not"][bool(rc)], rc)


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

    # Check if the tag is present
    try:
        parsed_tag = parsed_msg["tag"]
    except KeyError:
        client.publish(MqttTopic.ERROR, MqttUnknownMessageError())
        return

    # Echo certain message is not expected
    if not MessageTag.has(parsed_msg["tag"]) or parsed_msg["mtype"] != MessageType.REQUEST:
        client.publish(MqttTopic.ERROR, MqttUnknownMessageError())
        return


class MqttHandler:

    def __init__(self, client):
        self.client = mqtt.Client()
        self.client.on_connect

    def on_connect(self):
        pass
