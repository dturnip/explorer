from curses import window

from ..lib.parser import Tile

from ..lib.singleton import singleton
from .game import GameContext
from .player import PlayerContext

G = GameContext()
P = PlayerContext()


@singleton
class PadContext:
    """
    Context object for a curses pad, taking a reference to a pad
    """

    def __init__(
        self, pad: window, tilemap: list[list[Tile]], y_offset: int, x_offset: int
    ) -> None:
        self.__pad = pad
        self.__y_offset = y_offset
        self.__x_offset = x_offset
        self.map = tilemap

        for row in tilemap:
            for col in row:
                self.__pad.addch(col.char, col.color)
            self.__pad.addch("\n")

        self.refresh()

    @property
    def pad(self) -> window:
        return self.__pad

    @property
    def y_offset(self) -> int:
        return self.__y_offset

    @property
    def x_offset(self) -> int:
        return self.__x_offset

    @y_offset.setter
    def y_offset(self, new_y_offset) -> None:
        self.__y_offset = new_y_offset

    @x_offset.setter
    def x_offset(self, new_x_offset) -> None:
        self.__x_offset = new_x_offset

    def refresh(self) -> None:
        self.__pad.refresh(
            self.__y_offset,
            self.__x_offset,
            G.padding_height + 1,
            G.padding_width + 1,
            G.padding_height + G.game_height - 2,
            G.padding_width + G.game_width - 2,
        )

    def is_block(self, y, x) -> bool:
        match self.map[y][x].id:
            case t if t in list(range(21)) + [22, 32]:
                return True
            case _:
                return False

    def try_interact_tile(self, y, x) -> None:
        match self.map[y][x].id:
            case 21:  # PATH
                pass
            case 24:  # MONEY
                G._inventory.money += 1

    def displace_up(self) -> None:
        if self.__y_offset - 1 > G.padding_height and not self.is_block(P.map_y - 1, P.map_x):
            self.__y_offset -= 1
            P.y -= 1

    def displace_down(self) -> None:
        if self.__y_offset < 256 + G.padding_height and not self.is_block(P.map_y + 1, P.map_x):
            self.__y_offset += 1
            P.y += 1

    def displace_left(self) -> None:
        if self.__x_offset - 1 > G.padding_width and not self.is_block(P.map_y, P.map_x - 1):
            self.__x_offset -= 1
            P.x -= 1

    def displace_right(self) -> None:
        if self.__x_offset < 256 + G.padding_width and not self.is_block(P.map_y, P.map_x + 1):
            self.__x_offset += 1
            P.x += 1
