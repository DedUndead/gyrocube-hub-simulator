# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import time
import random

from communication.messages import (
    CubeJoinedSignal,
    CubeDisconnectedSignal,
    CubeFlippedSignal,
    CubeConfigIndication,
)
from communication.mqtt_handler import MqttHandler
from testing.utils import Network


def test_single_message():
    """Template for sending single messages"""
    # See message constructors in communication.messages
    message = CubeFlippedSignal(cube_id=0xAA, old=1, new=5)

    MqttHandler.tx_single(HOST_ADDRESS, message)


def test_cube_flipping_scenarion(
    number_of_cubes: int,
    min_gap_between_transmissions: int,
    max_gap_between_transmissions: int,
):
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
        print("EVENT: CUBE FLIPPED")
        cube = random.choice(network.network)

        old_side = cube.side
        cube.flip()
        new_side = cube.side
        mqtt.publish(CubeFlippedSignal(cube.id, old_side, new_side))
        mqtt.publish(CubeConfigIndication(cube.id, cube.side, cube.config))

        time.sleep(
            random.randint(min_gap_between_transmissions, max_gap_between_transmissions)
        )


def test_active_scenario(
    number_of_cubes: int,
    min_gap_between_transmissions: int,
    max_gap_between_transmissions: int,
):
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
    mqtt = MqttHandler(HOST_ADDRESS, PORT, USERNAME, PASSWORD)

    while True:
        # Random join event
        # <- CubeJoined signal to /network
        # <- CubeConfigIndication signal to /config
        if random.randint(1, 100) > 50 and not network.full:
            print("EVENT: CUBE JOINED NETWORK")
            new_cube = network.join()
            mqtt.publish(CubeJoinedSignal(new_cube.id))
            mqtt.publish(
                CubeConfigIndication(new_cube.id, new_cube.side, new_cube.config)
            )

        # Random exit event
        # <- CubeDisconnected signal to /network
        elif random.randint(1, 100) > 75 and not network.empty:
            print("EVENT: CUBE EXITED NETWORK")
            cube_id = network.exit()
            mqtt.publish(CubeDisconnectedSignal(cube_id))

        # Random flip event
        # <- CubeFlipped signal to /cube
        # <- CubeConfigIndication signal to /config
        elif random.randint(1, 100) > 20 and not network.empty:
            print("EVENT: CUBE FLIPPED")
            cube = random.choice(network.network)

            old_side = cube.side
            cube.flip()
            new_side = cube.side
            mqtt.publish(CubeFlippedSignal(cube.id, old_side, new_side))
            mqtt.publish(CubeConfigIndication(cube.id, cube.side, cube.config))

        time.sleep(
            random.randint(min_gap_between_transmissions, max_gap_between_transmissions)
        )


if __name__ == "__main__":
    test_active_scenario(
        number_of_cubes=2,
        min_gap_between_transmissions=10,
        max_gap_between_transmissions=15,
    )
    # test_cube_flipping_scenarion(number_of_cubes=1, min_gap_between_transmissions=2, max_gap_between_transmissions=5)
