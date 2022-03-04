from curses import window, A_BOLD
from getpass import getuser

from explorer.contexts.pad import PadContext
from explorer.contexts.player import PlayerContext

from ..lib.singleton import singleton
from .game import GameContext
from ..colors import Colors

# C lib
from recordclass import RecordClass  # type: ignore

G = GameContext()


@singleton
class SideContext:
    def __init__(self, pad: window) -> None:
        self.__pad = pad

        self.__pad.bkgdset(" ", Colors.WALL)

    @property
    def pad(self) -> window:
        return self.__pad

    def refresh(self) -> None:

        r = self.pad.addstr
        s = G._side_state
        u = getuser()
        name = u if len(u) <= G.padding_width - 4 else u[: G.padding_width - 7] + "..."

        self.pad.clear()

        r(f"{name}\n\n", A_BOLD)

        r("LEVEL: ", A_BOLD)
        r(f"{s.level.level} ({s.level.xp} / {s.level.max_xp} XP)\n")

        r("HP: ", A_BOLD)
        r(f"{s.hp.hp}", self.get_health_color())
        r(" / ")
        r(f"{s.hp.max_hp}\n", Colors.HP_HIGH)

        r("MONEY: ", A_BOLD)
        r(f"{G._inventory.money}\n")

        r("\n\nDEBUG(y, x): ", A_BOLD)
        r(f"({PlayerContext().y}, {PlayerContext().x})")  # type: ignore

        self.pad.refresh(
            0,
            0,
            G.padding_height + 1,
            2,
            G.padding_height + G.game_height - 2,
            G.padding_width - 3,
        )

    def get_health_color(_self) -> int:
        c = G._side_state.hp.hp
        m = G._side_state.hp.max_hp

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
