import curses

from curses import window

from lib.singleton import singleton


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

    def displace_up(self) -> None:
        if self.__y_offset > 0:
            self.__y_offset -= 1

    def displace_down(self) -> None:
        if self.__y_offset < self.__pad.getmaxyx()[0]:
            self.__y_offset += 1

    def displace_left(self) -> None:
        if self.__x_offset > 0:
            self.__x_offset -= 1

    def displace_right(self) -> None:
        if self.__x_offset < self.__pad.getmaxyx()[1]:
            self.__x_offset += 1
