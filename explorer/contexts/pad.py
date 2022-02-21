import curses

from curses import window

from ..lib.singleton import singleton


@singleton
class PadContext:
    """
    Context object for a curses pad, taking a reference to a pad
    """

    def __init__(self, pad: window, y_offset: int, x_offset: int) -> None:
        self.__pad = pad
        self.__y_offset = y_offset
        self.__x_offset = x_offset

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
        cy, cx = curses.LINES // 2, curses.COLS // 2

        self.__pad.refresh(
            self.__y_offset,
            self.__x_offset,
            cy // 3,
            cx // 3,
            cy // 3 * 2 + cy,
            cx // 3 * 2 + cx,
        )

        # print(self.__y_offset, self.__x_offset)

    def displace_up(self) -> None:
        if self.__y_offset > 0:
            self.__y_offset -= 1

    def displace_down(self) -> None:
        ## TODO: Mathematically calculate this, but this will do for now
        if self.__y_offset < 345:
            self.__y_offset += 1

    def displace_left(self) -> None:
        if self.__x_offset > 0:
            self.__x_offset -= 1

    def displace_right(self) -> None:
        if self.__x_offset < 345:
            self.__x_offset += 1
