from os import get_terminal_size
from recordclass import RecordClass  # type: ignore
from math import floor
from typing import NamedTuple
from ..lib.singleton import singleton


class Data(RecordClass):
    class LevelData(RecordClass):
        level: int
        xp: int
        max_xp: int

    class HpData(RecordClass):
        hp: int
        max_hp: int

    level = LevelData(level=1, xp=0, max_xp=20)
    hp = HpData(hp=10, max_hp=10)


class Weapon:
    def __init__(self, name: str, atk: int) -> None:
        self.name = name
        self.atk = atk


class Inventory(RecordClass):
    weapons: list[str | None]
    delusions: list[str | None]
    heals: list[str | None]
    items: list[str | None]
    money: int


@singleton
class GameContext:
    _side_state = Data
    _inventory = Inventory(
        weapons=[None] * 10,
        delusions=[None] * 3,
        heals=[None] * 5,
        items=[None] * 10,
        money=0,
    )

    def __init__(self) -> None:
        w, h = get_terminal_size()

        if h % 2 == 0:
            h -= 1
        if w % 2 == 0:
            w -= 1

        self.__height = h
        self.__width = w

        self.__center_y = h // 2
        self.__center_x = w // 2

        self.__game_height = self.__height - 2 * floor(self.__height / 8)
        self.__game_width = self.__width - 2 * floor(self.__width / 8)

        self.__padding_height = (self.__height - self.__game_height) // 2

        # self.__padding_width = (self.__width - self.__game_width) // 2
        self.__padding_width = self.__width - self.__game_width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def center_y(self) -> int:
        return self.__center_y

    @property
    def center_x(self) -> int:
        return self.__center_x

    @property
    def game_height(self) -> int:
        return self.__game_height

    @property
    def game_width(self) -> int:
        return self.__game_width

    @property
    def padding_height(self) -> int:
        return self.__padding_height

    @property
    def padding_width(self) -> int:
        return self.__padding_width
