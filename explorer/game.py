import curses
from pathlib import Path
from PIL import Image

from .colors import Colors
from .contexts.pad import PadContext
from .contexts.glob import GlobContext
from .lib.parser import parse_image

G = GlobContext()


def render_border(stdscr: curses.window) -> None:
    stdscr.attron(Colors.OVERLAY)

    # fmt: off

    # Border corners
    stdscr.addstr(G.padding_height, G.padding_width, "╔")
    stdscr.addstr(G.padding_height, G.padding_width + G.game_width - 1, "╗")
    stdscr.addstr(G.padding_height + G.game_height - 1, G.padding_width, "╚")
    stdscr.addstr(G.padding_height + G.game_height - 1, G.padding_width + G.game_width - 1, "╝")

    # Border top, bottom
    stdscr.addstr(G.padding_height, G.padding_width + 1, "═" * (G.game_width - 2))
    stdscr.addstr(G.padding_height + G.game_height - 1, G.padding_width + 1, "═" * (G.game_width - 2))

    # Bottom left, right
    for y in range(G.game_height - 2):
        stdscr.addstr(G.padding_height + y + 1, G.padding_width, "║")
        stdscr.addstr(G.padding_height + y + 1, G.padding_width + G.game_width - 1, "║")

    # fmt: on

    stdscr.attroff(Colors.OVERLAY)


def render_player(stdscr: curses.window) -> None:
    stdscr.addstr(G.center_y, G.center_x, "", Colors.OVERLAY)


def update(stdscr: curses.window) -> None:

    stdscr.clear()
    render_border(stdscr)
    stdscr.refresh()
    PadContext().refresh()  # type: ignore

    # Requires Nerd Fonts compatible font
    render_player(stdscr)
    print(PadContext().y_offset, PadContext().x_offset)  # type: ignore


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
    curses.init_pair(2, 240, 16)
    curses.init_pair(3, 135, 16)
    curses.init_pair(4, 160, 16)
    curses.init_pair(5, 95, 16)
    curses.init_pair(6, 226, 16)
    curses.init_pair(7, 87, 16)
    curses.init_pair(8, 47, 16)
    curses.init_pair(9, 202, 16)
    curses.init_pair(10, 29, 29)
    curses.init_pair(11, 34, 16)
    curses.init_pair(12, 212, 16)
    curses.init_pair(13, 27, 27)
    curses.init_pair(14, 214, 16)
    curses.init_pair(15, 223, 16)

    curses.init_pair(99, 16, 16)

    Colors.WALL = curses.color_pair(1)  # white on black
    Colors.PATH = curses.color_pair(2)  # gray on black
    Colors.OVERLAY = curses.color_pair(3)  # purple on black
    Colors.ENEMY = curses.color_pair(4)  # red on black
    Colors.CHEST = curses.color_pair(5)  # pink-brown on black (UNCONFIRMED)
    Colors.MONEY = curses.color_pair(6)  # yellow on black
    Colors.SHOP = curses.color_pair(7)  # cyan on black (UNCONFIRMED)
    Colors.HEAL = curses.color_pair(8)  # light-green on black
    Colors.SUPER = curses.color_pair(9)  # orange on black
    Colors.GRASS = curses.color_pair(10)  # deep-gren on deep-gren (UNCONFIRMED)
    Colors.TREE = curses.color_pair(11)  # green on black
    Colors.CHECK = curses.color_pair(12)  # pink on black
    Colors.WATER = curses.color_pair(13)  # blue on blue (UNCONFIRMED)
    Colors.LOCK = curses.color_pair(14)  # gold on black
    Colors.KEY = curses.color_pair(15)  # tan-yellow on black

    Colors.BLACK = curses.color_pair(99)  # black on black

    spawn_y = 176 + G.padding_height
    spawn_x = 61 + G.padding_width

    pad_ctx = PadContext(
        curses.newpad(257 + G.center_y * 2, 257 + G.center_x * 2), spawn_y, spawn_x
    )

    game_map_path = Path(__file__).resolve().parents[1] / "krita" / "explorer_map.png"
    tile_matrix = parse_image(Image.open(game_map_path))

    for row in tile_matrix:
        for col in row:
            pad_ctx.pad.addch(col.char, col.color)
        pad_ctx.pad.addch("\n")

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
