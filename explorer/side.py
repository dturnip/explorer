from curses import window, A_BOLD
from getpass import getuser
from .globals import Colors, Globals as G
from .ctx import player, state, inventory


class Side:
    def __init__(self, pad: window) -> None:
        self.pad = pad
        self.pad.bkgd(" ", Colors.WALL)

    def render(self) -> None:
        draw = self.pad.addstr
        user = getuser()
        name = user if len(user) <= G.padding_width - 4 else user[: G.padding_width - 7] + "..."

        self.pad.clear()

        draw(f"{name}\n\n", A_BOLD)

        draw("LEVEL: ", A_BOLD)
        draw(f"{state.level.level} ({state.level.xp} / {state.level.max_xp} XP)\n")

        draw("HP: ", A_BOLD)
        draw(f"{state.hp.hp}", self.get_health_color())
        draw(" / ")
        draw(f"{state.hp.max_hp}\n", Colors.HP_HIGH)

        draw("MONEY: ", A_BOLD)
        draw(f"{inventory.money}\n")

        draw(f"\n\nDEBUG(y, x): ", A_BOLD)
        draw(f"({player.y}, {player.x})")

        self.pad.refresh(
            0,
            0,
            G.padding_height + 1,
            2,
            G.padding_height + G.game_height - 2,
            G.padding_width - 3,
        )

    def get_health_color(_self) -> int:
        c = state.hp.hp
        m = state.hp.max_hp

        low = m // 3
        mid = low * 2

        match (c <= low, c >= mid + 1):
            case (True, False):
                return Colors.HP_LOW
            case (False, False):
                return Colors.HP_MID
            case (False, True):
                return Colors.HP_HIGH

        # Never going to happen, but mypy just wants it because of explicit return types
        return 0
