# This software can be copied, modified and distributed freely.
# The origin must be mentioned in all copied, modified or distributed pieces:
# <link>
# 2022, GyroCube
import random
from typing import List, Optional


class Cube:
    """ The class describes cube """

    def __init__(self, _id: int):
        self.id = _id
        self.side = random.randint(1, 6)

    def flip(self, _id: int) -> None:
        self.id = _id
        self.side = random.randint(1, 6)


class Network:
    """ The class describes cube network """

    def __init__(self, size: int):
        self.network: List[Cube] = []
        self.size = size

    @property
    def full(self) -> bool:
        return len(self.network) == self.size

    @property
    def empty(self) -> bool:
        return len(self.network) == 0

    def join(self, cube_id: Optional[int] = None) -> int:
        """ Make new cube join network """
        assert cube_id not in self.network, "Specified address %d is already in use" % cube_id
        if cube_id is None:
            cube_id = self.get_unique_cube_id()
        self.network.append(cube_id)

        return cube_id

    def exit(self, cube_id: Optional[int] = None) -> int:
        """ Remove cube from the network """
        assert not self.empty, "Network is empty"

        if cube_id is None:
            cube_id = random.choice(self.network)
        assert cube_id in self.network, "Specified address %d is not in use" % cube_id

        self.network.remove(cube_id)

        return cube_id

    def get_unique_cube_id(self) -> int:
        assert not self.full and len(self.network) < 0xff, "Network is full"

        new_cube_id = random.randint(0x00, 0xff)
        while new_cube_id in self.network:
            new_cube_id = random.randint(0x00, 0xff)

        return new_cube_id
