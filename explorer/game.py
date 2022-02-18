import curses
from types import SimpleNamespace

from contexts.pad import PadContext

# NOTES
# Parse pixel art in a matrix.
# Serialize/Deserialize matrix.
# 500 squared matrix
# Movement logic
# Collision logic
# State machine for player
# State machine for game state location


__Colors: dict[str, int] = {
    "WHITE_FG_BLACK_BG": 0,
    "BLACK_FG_WHITE_BG": 0,
    "PURPLE_FG_BLACK_BG": 0,
}

Colors = SimpleNamespace(**__Colors)


def render_border(stdscr: curses.window) -> None:
    cy, cx = curses.LINES // 2, curses.COLS // 2

    stdscr.attron(Colors.PURPLE_FG_BLACK_BG)

    stdscr.addstr(cy // 3 * 2 + cy + 1, cx // 3 - 1, "+")
    stdscr.addstr(cy // 3 - 1, cx // 3 - 1, "+")
    stdscr.addstr(cy // 3 * 2 + cy + 1, cx // 3 * 2 + cx + 1, "+")
    stdscr.addstr(cy // 3 - 1, cx // 3 * 2 + cx + 1, "+")

    stdscr.addstr(cy // 3 - 1, cx // 3, "-" * (cx // 3 * 2 + cx - cx // 3 + 1))
    stdscr.addstr(cy // 3 * 2 + cy + 1, cx // 3, "-" * (cx // 3 * 2 + cx - cx // 3 + 1))
    for i in range(cy // 3 * 2 + cy - cy // 3 + 1):
        stdscr.addstr(i + cy // 3, cx // 3 - 1, "|")
        stdscr.addstr(i + cy // 3, cx // 3 * 2 + cx + 1, "|")

    stdscr.attroff(Colors.PURPLE_FG_BLACK_BG)


def render_player(stdscr: curses.window) -> None:
    player_render_y = curses.LINES // 2 if (curses.LINES // 2) % 2 == 1 else curses.LINES // 2 - 1
    player_render_x = curses.COLS // 2 if (curses.COLS // 2) % 2 == 1 else curses.COLS // 2 - 1
    stdscr.addstr(player_render_y, player_render_x, "", Colors.PURPLE_FG_BLACK_BG)


def update(stdscr: curses.window) -> None:

    stdscr.clear()
    render_border(stdscr)
    stdscr.refresh()
    PadContext().refresh()  # type: ignore

    # Requires Nerd Fonts compatible font
    render_player(stdscr)


def listen(key: int) -> None:
    match key:
        case 119:  # w
            PadContext().displace_up()  # type: ignore
        case 97:  # a
            PadContext().displace_left()  # type: ignore
        case 115:  # s
            PadContext().displace_down()  # type: ignore
        case 100:  # d
            PadContext().displace_right()  # type: ignore
        case 81:  # Q
            raise Exception
        case _:
            pass


def main(stdscr: curses.window) -> None:
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 231, 16)
    curses.init_pair(2, 16, 231)
    curses.init_pair(3, 135, 16)

    Colors.WHITE_FG_BLACK_BG = curses.color_pair(1)
    Colors.BLACK_FG_WHITE_BG = curses.color_pair(2)
    Colors.PURPLE_FG_BLACK_BG = curses.color_pair(3)

    pad_ctx = PadContext(
        curses.newpad(1000, 1000),
        0,
        0,
    )

    pad_ctx.pad.bkgdset(" ", Colors.WHITE_FG_BLACK_BG)

    render_border(stdscr)

    stdscr.refresh()
    pad_ctx.refresh()

    render_player(stdscr)

    try:
        while True:
            listen(stdscr.getch())
            update(stdscr)
    except:
        pass
