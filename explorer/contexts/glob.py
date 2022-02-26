from os import get_terminal_size
from ..lib.singleton import singleton
from math import floor


@singleton
class GlobContext:
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
        self.__padding_width = (self.__width - self.__game_width) // 2

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
