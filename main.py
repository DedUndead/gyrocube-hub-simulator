# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import time
import random

from communication.messages import CubeJoinedSignal, CubeDisconnectedSignal, CubeFlippedSignal, CubeConfigIndication, \
    SideConfig
from communication.mqtt_handler import MqttHandler
from testing.utils import Network

HOST_ADDRESS = "insert_server_address"
PORT = 0


def test_cube_flipping_scenarion(number_of_cubes: int,
                                 min_gap_between_transmissions: int,
                                 max_gap_between_transmissions: int):
    """
    Cube flipping scenaraio starts with filled network of specified size.
    Cubes are periodically flipped.

    :param number_of_cubes: Number of cubes in the network
    :param min_gap_between_transmissions: Minimal time-gap between transmissions
    :param max_gap_between_transmissions: Maximum time-gap between transmissions
    """
    network = Network(size=number_of_cubes)
    mqtt = MqttHandler(HOST_ADDRESS, PORT)

    for _ in range(number_of_cubes):
        network.join()

    while True:
        cube = random.choice(network.network)

        old_side = cube.side
        cube.flip()
        new_side = cube.side
        mqtt.publish(CubeFlippedSignal(cube.id, old_side, new_side))
        mqtt.publish(CubeConfigIndication(cube.id, cube.side, cube.config))

        time.sleep(random.randint(min_gap_between_transmissions, max_gap_between_transmissions))


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
        # <- CubeJoined signal to /network
        # <- CubeConfigIndication signal to /config
        cube_joined_probability = random.randint(1, 100)
        if random.randint(1, 100) > 50 and not network.full:
            new_cube = network.join()
            mqtt.publish(CubeJoinedSignal(new_cube.id))
            mqtt.publish(CubeConfigIndication(new_cube.id, new_cube.side, new_cube.config))

        # Random exit event
        # <- CubeDisconnected signal to /network
        elif random.randint(1, 100) > 75 and not network.empty:
            cube_id = network.exit()
            mqtt.publish(CubeDisconnectedSignal(cube_id))

        # Random flip event
        # <- CubeFlipped signal to /cube
        # <- CubeConfigIndication signal to /config
        elif random.randint(1, 100) > 20 and not network.empty:
            cube = random.choice(network.network)

            old_side = cube.side
            cube.flip()
            new_side = cube.side
            mqtt.publish(CubeFlippedSignal(cube.id, old_side, new_side))
            mqtt.publish(CubeConfigIndication(cube.id, cube.side, cube.config))

        time.sleep(random.randint(min_gap_between_transmissions, max_gap_between_transmissions))


if __name__ == "__main__":
    #test_active_scenario(number_of_cubes=3, min_gap_between_transmissions=2, max_gap_between_transmissions=5)
    #test_cube_flipping_scenarion(number_of_cubes=1, min_gap_between_transmissions=2, max_gap_between_transmissions=5)
