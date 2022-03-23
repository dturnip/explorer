from recordclass import RecordClass  # type: ignore
from enum import Enum, auto
from curses import window, A_BOLD
from getpass import getuser
from collections import deque
from typing import Optional
from .lib.singleton import singleton
from .globals import Colors, Globals as G


class Player:
    def __init__(self, y: int, x: int) -> None:
        self.__y = y
        self.__x = x

        self.rel_y = y + G.padding_height
        self.rel_x = x + G.padding_width
        self.map_y = y + G.center_y - 1
        self.map_x = x + G.center_x - 1

    @property
    def y(self) -> int:
        return self.__y

    @property
    def x(self) -> int:
        return self.__x

    @y.setter
    def y(self, y2) -> None:
        self.__y = y2
        self.rel_y = y2 + G.padding_height
        self.map_y = y2 + G.center_y - 1

    @x.setter
    def x(self, x2) -> None:
        self.__x = x2
        self.rel_x = x2 + G.padding_height
        self.map_x = x2 + G.center_x - 1


class Phase(Enum):
    begin = auto()
    counter = auto()
    end = auto()
    null = auto()


class Turn(Enum):
    player = auto()
    opponent = auto()
    null = auto()


class Delusions(Enum):
    Freeze = auto()
    Burn = auto()
    Plant = auto()
    Mech = auto()
    Corrupt = auto()
    Stun = auto()
    Zap = auto()
    Drain = auto()
    Bleed = auto()


meta = {
    Delusions.Freeze: {
        "strong": Delusions.Burn,
        "symbol": "",
        "phase": Phase.begin,
        "turn": Turn.player,
    },
    Delusions.Burn: {
        "strong": Delusions.Plant,
        "symbol": "",
        "phase": Phase.end,
        "turn": Turn.player,
    },
    Delusions.Plant: {
        "strong": Delusions.Mech,
        "symbol": "",
        "phase": Phase.begin,
        "turn": Turn.player,
    },
    Delusions.Mech: {
        "strong": Delusions.Corrupt,
        "symbol": "",
        "phase": Phase.counter,
        "turn": Turn.opponent,
    },
    Delusions.Corrupt: {
        "strong": Delusions.Stun,
        "symbol": "",
        "phase": Phase.counter,
        "turn": Turn.opponent,
    },
    Delusions.Stun: {
        "strong": Delusions.Zap,
        "symbol": "",
        "phase": Phase.end,
        "turn": Turn.player,
    },
    Delusions.Zap: {
        "strong": Delusions.Freeze,
        "symbol": "",
        "phase": Phase.begin,
        "turn": Turn.opponent,
    },
    Delusions.Drain: {
        "strong": None,
        "symbol": "",
        "phase": Phase.end,
        "turn": Turn.player,
    },
    Delusions.Bleed: {
        "strong": None,
        "symbol": "",
        "phase": Phase.end,
        "turn": Turn.player,
    },
}
#


class Delusion:
    """
    The player's weapon is equipped with a delusion.

    When an entity attacks an enemy with a delusion it is strong against, 150% damage is dealt
    Depending on the battle phase and turn, roll a chance to apply effects:
    ** If the percentage is a decimal value, take the ceil of it **

    Freeze:     50% chance || Take 5% out of their HP, Skip their turn
    Burn:       50% chance || Deal an extra 30% weapon damage
    Plant:      75% chance || Heal me by 10% of my max HP, increase my weapon ATK by 50% this turn
    Mech:       75% chance || Take half damage, increase my weapon ATK by 25% for the duration of the duel
    Corrupt:    50% chance || Make the enemy attack itself with half damage, negate effects
    Stun:       50% chance || Skip their turn
    Zap:        50% chance || Weaken their weapon ATK by 10%
    Drain:      75% chance || Heal me by 40% of what I strike
    Bleed:      50% chance || Reduce their HP by 10% of their max HP

    Base HP Stats for entities of delusions:

    Freeze:     83
    Burn:       64
    Plant:      96
    Mech:       90
    Corrupt:    69
    Stun:       85
    Zap:        80
    Drain:      78
    Bleed:      76

    Base ATK Stats for weapons of delusions (~common~rare~epic~mythic):

    Freeze:     Moderate    ~19~22~24~29
    Burn:       High        ~24~27~29~37
    Plant:      Low         ~11~13~16~22
    Mech:       Moderate    ~16~17~21~27
    Corrupt:    Low         ~12~14~18~23
    Stun:       Moderate    ~20~23~25~30
    Zap:        Moderate    ~18~21~23~27
    Drain:      Moderate    ~13~18~22~26
    Bleed:      High        ~23~25~27~34

    - When entities level up, their max HP becomes 110% of their current max HP
    - When entities level up, their current HP becomes max if it is currently max, otherwise it stays the same
    - When weapons level up, its ATK increases by 110% of its current ATK
    - Weapon level correlates exactly to the entity level
    """

    __slots__ = ("type", "phase")

    def __init__(self, type: Delusions) -> None:
        self.type: Delusions = type
        self.phase: Phase = self.get_phase()

    def get_phase(self) -> Phase:
        return meta[self.type]["phase"]

    def get_strong(self) -> Delusions:
        return meta[self.type]["strong"]

    def get_symbol(self) -> str:
        return meta[self.type]["symbol"]

    def get_color(self):
        # I was going to do something like this:
        # return meta[self.type]["color"]
        # But there's an issue with Recordclass so I have to do it like this:
        match self.type:
            case Delusions.Freeze:
                return Colors.FREEZE
            case Delusions.Burn:
                return Colors.BURN
            case Delusions.Plant:
                return Colors.PLANT
            case Delusions.Mech:
                return Colors.MECH
            case Delusions.Corrupt:
                return Colors.CORRUPT
            case Delusions.Stun:
                return Colors.STUN
            case Delusions.Zap:
                return Colors.ZAP
            case Delusions.Drain:
                return Colors.DRAIN
            case Delusions.Bleed:
                return Colors.BLEED


class Rarity(Enum):
    Common = auto()
    Rare = auto()
    Epic = auto()
    Mythic = auto()


class Weapon:
    def __init__(self, name: str, atk: int, delusion: Delusion, rarity: Rarity) -> None:
        self.name = name
        self.atk = atk
        self.delusion = delusion
        self.rarity = rarity

    def get_rarity_color(self) -> int:
        match self.rarity:
            case Rarity.Common:
                return Colors.COMMON
            case Rarity.Rare:
                return Colors.RARE
            case Rarity.Epic:
                return Colors.EPIC
            case Rarity.Mythic:
                return Colors.MYTHIC


class Healable:
    # TODO: Rarity
    def __init__(self, name: str, amount: int, rarity: Rarity) -> None:
        self.name = name
        self.amount = amount
        self.rarity = rarity

    def get_rarity_color(self) -> int:
        match self.rarity:
            case Rarity.Common:
                return Colors.COMMON
            case Rarity.Rare:
                return Colors.RARE
            case Rarity.Epic:
                return Colors.EPIC
            case Rarity.Mythic:
                return Colors.MYTHIC


class Inventory(RecordClass):
    weapons: list[Weapon | None]
    heals: list[Healable | None]
    items: list[str | None]
    _money: int

    def add_weapon(self, weapon: Weapon) -> None:
        # By default, weapons is [None, None, None, None, None]

        amount_of_weapons = len(list(filter(lambda weapon: weapon, self.weapons)))

        if amount_of_weapons < 5:
            self.weapons[amount_of_weapons] = weapon
            Log(f"Got {weapon.name}!")
            return

        raise Exception("TODO: weapon discard/replacement prompt")

    def add_heal(self, heal: Healable) -> None:
        amount_of_heals = len(list(filter(lambda heal: heal, self.heals)))

        if amount_of_heals < 8:
            self.heals[amount_of_heals] = heal
            Log(f"Got {heal.name}!")
            return

        raise Exception("TODO: heals discard/replacement prompt")

    def add_item(self) -> None:
        pass

    @property
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, n: int) -> None:
        curr = self._money
        self._money = n
        Log(f"Money {curr} -> {n}")


class State(RecordClass):
    class LevelData(RecordClass):
        level: int
        xp: int
        max_xp: int

    class HpData(RecordClass):
        hp: int
        max_hp: int

    level = LevelData(level=1, xp=0, max_xp=20)
    hp = HpData(hp=10, max_hp=10)


class FightState:
    def __init__(self) -> None:
        self.turn: Turn = Turn.null
        self.phase: Phase = Phase.null


player = Player(176, 61)
state = State
fight_state = FightState()
inventory = Inventory(
    weapons=[None] * 5,
    heals=[None] * 8,
    items=[],
    _money=10,
)

##### EVERYTHING TO DO WITH THE SIDE #####


class SideState(Enum):
    default = auto()
    inventory = auto()
    console = auto()


@singleton
class Side:
    def __init__(self, pad: window) -> None:
        self.pad = pad
        self.pad.bkgd(" ", Colors.WALL)

        self.text: str = ""
        self.state: SideState = SideState.default

        self.log_buffer: deque[str] = deque()

        # The height of the unboredered side pad, minus 2 ()
        self.max_log_length = G.game_height - 2 - 2

    def draw_stats(self) -> None:
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

    def draw_weapon(self, weapon: Weapon | None) -> None:

        # TODO: Show a symbol indicating the currently equipped weapon

        draw = self.pad.addstr

        draw("- ")

        if weapon is None:
            draw("\n")
            return

        draw(f"{weapon.name} ", weapon.get_rarity_color())
        draw("[")
        draw(f"{weapon.delusion.get_symbol()} ", weapon.delusion.get_color())
        draw(f"{weapon.atk}]\n")

    def draw_heal(self, heal: Healable | None) -> None:
        draw = self.pad.addstr

        draw("- ")

        if heal is None:
            draw("\n")
            return

        draw(f"{heal.name} ", heal.get_rarity_color())
        draw(f"[+{heal.amount}%]\n")

    def draw_inventory(self) -> None:
        draw = self.pad.addstr

        self.pad.clear()

        draw("~~~INVENTORY~~~\n\n")

        draw("WEAPONS:\n", A_BOLD)

        for weapon in inventory.weapons:
            self.draw_weapon(weapon)

        draw("\n")
        draw("HEALS:\n", A_BOLD)

        for heal in inventory.heals:
            self.draw_heal(heal)

    def draw_console(self) -> None:
        draw = self.pad.addstr

        self.pad.clear()

        draw("~~~CONSOLE~~~\n\n")

        for t in self.log_buffer:
            draw(f"{t}\n")

    def log(self, t: str) -> None:
        if len(self.log_buffer) > self.max_log_length:
            raise Exception("Log buffer length is over the max space")

        if len(self.log_buffer) == self.max_log_length:
            self.log_buffer.popleft()

        self.log_buffer.append(t)

    def toggle_inventory(self) -> None:
        self.state = SideState.inventory if self.state != SideState.inventory else SideState.default

    def toggle_console(self) -> None:
        self.state = SideState.console if self.state != SideState.console else SideState.default

    def render(self) -> None:
        match self.state:
            case SideState.default:
                self.draw_stats()
            case SideState.inventory:
                self.draw_inventory()
            case SideState.console:
                self.draw_console()

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


def Log(s: str) -> None:
    Side().log(s)  # type: ignore
