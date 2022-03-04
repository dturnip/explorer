from ..lib.singleton import singleton
from .game import GameContext

G = GameContext()


@singleton
class PlayerContext:
    def __init__(self, y: int = 176, x: int = 61) -> None:
        self.__y = y
        self.__x = x

        self.__rel_y = y + G.padding_height
        self.__rel_x = x + G.padding_width

        self.__map_y = y + G.center_y - 1
        self.__map_x = x + G.center_x - 1

    @property
    def y(self) -> int:
        return self.__y

    @property
    def x(self) -> int:
        return self.__x

    @y.setter
    def y(self, new_y) -> None:
        self.__y = new_y
        self.__rel_y = new_y + G.padding_height
        self.__map_y = new_y + G.center_y - 1

    @x.setter
    def x(self, new_x) -> None:
        self.__x = new_x
        self.__rel_x = new_x + G.padding_width
        self.__map_x = new_x + G.center_x - 1

    @property
    def rel_y(self) -> int:
        return self.__rel_y

    @property
    def rel_x(self) -> int:
        return self.__rel_x

    @property
    def map_y(self) -> int:
        return self.__map_y

    @property
    def map_x(self) -> int:
        return self.__map_x
