# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
from communication.messages import Message, MessageType, MessageTag
from communication.mqtt_handler import MqttTopic

if __name__ == "__main__":
    print(Message(MessageType.SIGNAL, MqttTopic.ERROR, MessageTag.CUBE_HARDWARE_ERROR))
