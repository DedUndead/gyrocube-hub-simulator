# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import enum
import json
import paho.mqtt.client as mqtt

from communication.messages import MqttUnknownMessageError, MqttTopic


def _on_connect(client, userdata, flags, rc):
    """ On connect callback """
    print("Connection to server %s established. Returned code: %d", ["was", "was not"][bool(rc)], rc)


def on_message(client, userdata, message):
    """ On message callback """
    print("RECEIVED:", message.payload)

    if not MqttTopic.has(message.topic):
        client.publish(MqttTopic.ERROR, MqttUnknownMessageError())

    try


class MqttHandler:

    def __init__(self, client):
        self.client = mqtt.Client()
        self.client.on_connect

    def on_connect(self):
        pass
