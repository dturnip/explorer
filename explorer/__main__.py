from curses import window
from curses import wrapper
from .app import main


def test_keys(stdscr: window) -> None:
    k = stdscr.getch()
    print(k)
    while True:
        pass


if __name__ == "__main__":
    wrapper(main)
    # wrapper(test_keys)
