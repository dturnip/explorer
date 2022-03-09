from typing import Optional
from recordclass import RecordClass  # type: ignore
from enum import Enum, auto
from .globals import Globals as G


class Player:
    def __init__(self, y: int, x: int) -> None:
        self.__y = y
        self.__x = x

        self.rel_y = y + G.padding_height
        self.rel_x = x + G.padding_width
        self.map_y = y + G.center_y - 1
        self.map_x = x + G.center_x - 1

    @property
    def y(self) -> int:
        return self.__y

    @property
    def x(self) -> int:
        return self.__x

    @y.setter
    def y(self, y2) -> None:
        self.__y = y2
        self.rel_y = y2 + G.padding_height
        self.map_y = y2 + G.center_y - 1

    @x.setter
    def x(self, x2) -> None:
        self.__x = x2
        self.rel_x = x2 + G.padding_height
        self.map_x = x2 + G.center_x - 1


class Weapon:
    def __init__(self, name: str, atk: int) -> None:
        self.name = name
        self.atk = atk


class Delusion(Enum):
    bleed = auto()
    burn = auto()
    freeze = auto()


class Healable:
    def __init__(self, name: str, fx: int, desc: str) -> None:
        self.name = name
        self.fx = fx
        self.desc = desc


class Inventory(RecordClass):
    weapons: list[Weapon | None]
    delusions: list[Delusion | None]
    heals: list[Healable | None]
    items: list[str | None]
    money: int


class State(RecordClass):
    class LevelData(RecordClass):
        level: int
        xp: int
        max_xp: int

    class HpData(RecordClass):
        hp: int
        max_hp: int

    level = LevelData(level=1, xp=0, max_xp=20)
    hp = HpData(hp=10, max_hp=10)


player = Player(176, 61)
state = State
inventory = Inventory(
    weapons=[None] * 10,
    delusions=[None] * 3,
    heals=[None] * 5,
    items=[None] * 10,
    money=10,
)
