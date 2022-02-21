import curses



def render_border(stdscr: curses.window) -> None:
    cy, cx = curses.LINES // 2, curses.COLS // 2

    stdscr.attron(Colors.OVERLAY)

    stdscr.addstr(cy // 3 * 2 + cy + 1, cx // 3 - 1, "+")
    stdscr.addstr(cy // 3 - 1, cx // 3 - 1, "+")
    stdscr.addstr(cy // 3 * 2 + cy + 1, cx // 3 * 2 + cx + 1, "+")
    stdscr.addstr(cy // 3 - 1, cx // 3 * 2 + cx + 1, "+")

    stdscr.addstr(cy // 3 - 1, cx // 3, "-" * (cx // 3 * 2 + cx - cx // 3 + 1))
    stdscr.addstr(cy // 3 * 2 + cy + 1, cx // 3, "-" * (cx // 3 * 2 + cx - cx // 3 + 1))
    for i in range(cy // 3 * 2 + cy - cy // 3 + 1):
        stdscr.addstr(i + cy // 3, cx // 3 - 1, "|")
        stdscr.addstr(i + cy // 3, cx // 3 * 2 + cx + 1, "|")

    stdscr.attroff(Colors.OVERLAY)


def render_player(stdscr: curses.window) -> None:
    player_render_y = curses.LINES // 2 if (curses.LINES // 2) % 2 == 1 else curses.LINES // 2 - 1
    player_render_x = curses.COLS // 2 if (curses.COLS // 2) % 2 == 1 else curses.COLS // 2 - 1
    stdscr.addstr(player_render_y, player_render_x, "", Colors.OVERLAY)


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

    pad_ctx = PadContext(
        curses.newpad(1000, 1000),
        0,
        0,
    )


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
