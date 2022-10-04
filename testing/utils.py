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
        """
        :param size: Network size
        """
        self.network: List[Cube] = []
        self.size = size

    @property
    def full(self) -> bool:
        """ Indicates if network is full """
        return len(self.network) == self.size

    @property
    def empty(self) -> bool:
        """ Indicated if network is empty """
        return len(self.network) == 0

    @property
    def addresses(self) -> List[int]:
        """ Indicates all addresses """
        return [cube.id for cube in self.network]

    def join(self, cube_id: Optional[int] = None) -> int:
        """ Make new cube join network """
        assert cube_id not in self.addresses, "Specified address %d is already in use" % cube_id
        assert 0x00 < cube_id < 0xff, "Specified address %d is out of [%d; %d] range" % (cube_id, 0x00, 0xff)

        if cube_id is None:
            cube_id = self.get_unique_cube_id()
        self.network.append(Cube(cube_id))

        return cube_id

    def exit(self, cube_id: Optional[int] = None) -> int:
        """ Remove cube from the network """
        assert not self.empty, "Network is empty"

        if cube_id is None:
            cube_id = random.choice(self.network)
        assert cube_id in self.addresses, "Specified address %d is not in use" % cube_id

        self.network.remove(cube_id)

        return cube_id

    def get_unique_cube_id(self) -> int:
        assert not self.full and len(self.network) < 0xff, "Network is full"

        new_cube_id = random.randint(0x00, 0xff)
        while new_cube_id in self.network:
            new_cube_id = random.randint(0x00, 0xff)

        return new_cube_id

    def get_cube_by_id(self, target: int) -> Optional[Cube]:
        return next((cube for cube in self.network if cube.id == target), None)
