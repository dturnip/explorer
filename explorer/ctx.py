from recordclass import RecordClass  # type: ignore
from enum import Enum, auto

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

class Weapon:
    def __init__(self, name: str, atk: int) -> None:
        self.name = name
        self.atk = atk


class Delusion(Enum):
    bleed = auto()
    burn = auto()
    freeze = auto()


class Healable:
    def __init__(self, name: str, fx: int, desc: str) -> None:
        self.name = name
        self.fx = fx
        self.desc = desc


class Inventory(RecordClass):
    weapons: list[Weapon | None]
    delusions: list[Delusion | None]
    heals: list[Healable | None]
    items: list[str | None]
    money: int


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


player = Player(176, 61)
state = State
inventory = Inventory(
    weapons=[None] * 10,
    delusions=[None] * 3,
    heals=[None] * 5,
    items=[None] * 10,
    money=10,
)
