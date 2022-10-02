# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import enum
import time
import copy


class MessageType(enum.IntEnum):
    REQUEST  = 0x00  # Request action
    RESPONSE = 0x01  # Response to request
    SIGNAL   = 0x02  # Message that requires no response, can be used as ACK


class MqttTopic(enum.Enum):
    CONFIG       = "/config"       # Configuration of the cubes
    MEASUREMENTS = "/measurement"  # Measurements related info
    CUBE_STATE   = "/cube"         # Updates from cubes
    NETWORK      = "/network"      # Network updates
    ERROR        = "/error"        # Errors

    @classmethod
    def has(cls, value):
        return value in cls._value2member_map_


class MessageTag(enum.IntEnum):
    """
    Message tags are used for messages within the same topic to differentiate them between each other
    Additionally, message tags are unique within HUB-CLOUD message definitions, so the receiver can
    only check for tag to identify message it received if necessary.
    """
    CUBE_JOINED            = 0x01
    CUBE_DISCONNECTED      = 0x02
    SENSOR_DATA            = 0x03
    SENSOR_DATA_PERIOD_REQ = 0x04
    SENSOR_DATA_PERIOD_RES = 0x05
    CUBE_FLIPPED           = 0x06
    CUBE_SIDE_CONFIG       = 0x07
    CUBE_UPDATE_CONFIG_REQ = 0x08
    CUBE_UPDATE_CONFIG_RES = 0x09

    # Error tags
    CUBE_HARDWARE_ERROR        = 0x0A
    HUB_HARDWARE_ERROR         = 0x0B
    MQTT_UNKNOWN_MESSAGE_ERROR = 0x0C

    @classmethod
    def has(cls, value):
        return value in cls._value2member_map_


class Message:
    """ Base message class

    Each message in HUB-CLOUD communication includes common fields:
        mtype     - type of the message
        tag       - uniqe message identifier
        timestamp - UNIX timestamp of the message
    Representation of the message is JSON string.
    NOTE: mtopic is a member that is excluded from JSON representation
    """

    def __init__(self, mtype: MessageType, mtopic: MqttTopic, tag: MessageTag):
        self.mtype = mtype.value
        self.tag = tag
        self.timestamp = time.time()

        self.mtopic = mtopic.value

    def __str__(self):
        """
        Exclude MQTT topic from representation of the class,
        since it is not   a part of the actual message
        """
        json = copy.deepcopy(self.__dict__)
        del json["mtopic"]

        return str(json)

    def __call__(self):
        return str(self)

    @classmethod
    def from_json(cls):
        pass


class CubeJoinedSignal(Message):
    """ Signal that new cube joined the network """
    def __init__(self, cube_id: int):
        self.cube_id = cube_id
        super().__init__(MessageType.SIGNAL, MqttTopic.NETWORK, MessageTag.CUBE_JOINED)


class CubeDisconnectedSignal(Message):
    """ Signal that the cube left the network """
    def __init__(self, cube_id: int):
        self.cube_id = cube_id
        super().__init__(MessageType.SIGNAL, MqttTopic.NETWORK, MessageTag.CUBE_DISCONNECTED)


class MeasurementsSignal(Message):
    """ Signal containing the measurements """
    def __init__(self, temp: int, humid: int):
        self.temp = temp
        self.humid = humid
        super().__init__(MessageType.SIGNAL, MqttTopic.MEASUREMENTS, MessageTag.SENSOR_DATA)


class MeasurementsPeriodResponse(Message):
    """ Response to measurements period request

    Measurement period request should arrive in form of:
        { tag: 0x04, period: <new_period_ms> }
    This exchange allows to set new period of sensor data flow
    """
    def __init__(self):
        super().__init__(MessageType.RESPONSE, MqttTopic.MEASUREMENTS, MessageTag.SENSOR_DATA_PERIOD_RES)


class CubeFlippedSignal(Message):
    """ Signal that the cube was flipped from side OLD to side NEW """
    def __init__(self, cube_id: int, old: int, new: int):
        self.cube_id = cube_id
        self.old_side = old
        self.new_side = new
        super().__init__(MessageType.SIGNAL, MqttTopic.CUBE_STATE, MessageTag.CUBE_FLIPPED)


class CubeConfigIndication(Message):
    """ Signal containing configuration of the specific side """
    def __init__(self, side_idx: int, cube_id: int):
        self.side_idx = side_idx
        self.cube_id = cube_id
        super().__init__(MessageType.SIGNAL, MqttTopic.CONFIG, MessageTag.CUBE_SIDE_CONFIG)


class CubeConfigUpdateResponse(Message):
    """ Response configuration change for a specific side

    Measurement period request should arrive in form of:
        { TBA }
    This exchange allows to set new period of sensor data flow
    """
    def __init__(self, cube_id: int):
        self.cube_id = cube_id
        super().__init__(MessageType.RESPONSE, MqttTopic.CONFIG, MessageTag.CUBE_UPDATE_CONFIG_RES)


class CubeHardwareError(Message):
    """ Signal that indicates cube hardware error """
    def __init__(self, cube_id: int):
        self.cube_id = cube_id
        super().__init__(MessageType.SIGNAL, MqttTopic.ERROR, MessageTag.CUBE_HARDWARE_ERROR)


class HubHardwareError(Message):
    """ Signal that indicates cube hardware error """
    def __init__(self, cube_id: int):
        self.cube_id = cube_id
        super().__init__(MessageType.SIGNAL, MqttTopic.ERROR, MessageTag.HUB_HARDWARE_ERROR)


class MqttUnknownMessageError(Message):
    """ Signal that indicates reception of unknown MQTT message """
    def __init__(self):
        super().__init__(MessageType.SIGNAL, MqttTopic.ERROR, MessageTag.MQTT_UNKNOWN_MESSAGE_ERROR)
