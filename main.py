# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import time
import random

from communication.messages import CubeJoinedSignal, CubeDisconnectedSignal
from communication.mqtt_handler import MqttHandler
from testing.utils import Network

HOST_ADDRESS = "insert_server_address"
PORT = 0


def test_active_scenario(number_of_cubes: int,
                         min_gap_between_transmissions: int,
                         max_gap_between_transmissions: int):
    """
    Active scenaraio starts with empty network.
    At some point, cube will join the network.
    The cube may leave the network.
    Cube is periodically flipped.

    :param number_of_cubes: Max number of cubes that can join the network
    :param min_gap_between_transmissions: Minimal time-gap between transmissions
    :param max_gap_between_transmissions: Maximum time-gap between transmissions
    """
    network = Network(size=number_of_cubes)
    mqtt = MqttHandler(HOST_ADDRESS, PORT)

    while True:
        # Random join event
        cube_joined_probability = random.randint(1, 100)
        if cube_joined_probability > 50 and not network.full:
            new_cube_id = network.join()
            mqtt.publish(CubeJoinedSignal(new_cube_id))

        # Random exit event
        cube_disconnected_probability = random.randint(1, 100)
        if cube_disconnected_probability > 75 and not network.empty:
            cube_id = network.exit()
            mqtt.publish(CubeDisconnectedSignal(cube_id))

        # Random flip event


        time.sleep(random.randint(min_gap_between_transmissions, max_gap_between_transmissions))


if __name__ == "__main__":
    test_active_scenario(number_of_cubes=3, min_gap_between_transmissions=5, max_gap_between_transmissions=20)
