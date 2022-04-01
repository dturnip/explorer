from collections import deque
from curses import A_BOLD, window
from enum import Enum, auto
from getpass import getuser
from math import floor

from recordclass import RecordClass  # type: ignore

from .globals import Colors
from .globals import Globals as G
from .lib.singleton import singleton


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
    Drain:      75% chance || Heal me by what I strike
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
    def __init__(
        self, name: str, atk: int, delusion: Delusion, rarity: Rarity, level: int = 1
    ) -> None:
        self.name = name
        self.atk = atk
        self.delusion = delusion
        self.rarity = rarity
        self.level = level

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
    equipped_weapon: Weapon | None

    def add_weapon(self, weapon: Weapon) -> None:
        # By default, weapons is [None, None, None, None, None]

        ## FLAG!

        amount_of_weapons = len(list(filter(lambda weapon: weapon, self.weapons)))

        if amount_of_weapons < 5:
            self.weapons[amount_of_weapons] = weapon
            Log(f"Got {weapon.name}!")
            return

        side = Side()  # type: ignore
        side.previous_state = side.state
        side.temp_weapon = weapon
        state.check_xp()

        # All the math is to draw a responsive sized border around the message in the console
        Log(f"┏{'━' * (G.padding_width - 7)}┓")
        msg = f"┃ Got {weapon.name} [{weapon.delusion.get_symbol()} {weapon.atk} {str(weapon.rarity)[7:8]}]!"
        Log(f"{msg}{' ' * (G.padding_width - 6 - len(msg))}┃")
        Log(f"┃ Use `replace <n>` or `discard`!{' ' * (G.padding_width - 39)}┃")

        for i, w in enumerate(inventory.weapons):
            if w:
                msg = f"┃ {i+1}. {w.name} [{w.delusion.get_symbol()} {w.atk} {str(w.rarity)[7:8]}]"
                # Log(f"┃ {i+1}. {w.name} [{w.delusion.get_symbol()} {w.atk} {str(w.rarity)[7:8]}]")
                Log(f"{msg}{' ' * (G.padding_width - 6 - len(msg))}┃")

        Log(f"┗{'━' * (G.padding_width - 7)}┛")

        side.toggle_prompt()

    def add_heal(self, heal: Healable) -> None:
        amount_of_heals = len(list(filter(lambda heal: heal, self.heals)))

        if amount_of_heals < 5:
            self.heals[amount_of_heals] = heal
            Log(f"Got {heal.name}!")
            return

        del heal

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


LEVEL_META: dict[int, dict[str, int]] = {
    1: {"max_xp": 20, "base_max_hp": 50},
}

# The compound scaling is subject to change
for _ in range(9):
    LEVEL_META.update(
        {
            len(LEVEL_META)
            + 1: {
                "max_xp": int(round(LEVEL_META[len(LEVEL_META)]["max_xp"] * 1.8, -1)),
                "base_max_hp": int(round(LEVEL_META[len(LEVEL_META)]["base_max_hp"] * 1.5, -1)),
            }
        }
    )


class State(RecordClass):
    class LevelData(RecordClass):
        level: int
        xp: int
        max_xp: int

    class HpData(RecordClass):
        hp: int
        max_hp: int

    level = LevelData(level=1, xp=0, max_xp=LEVEL_META[1]["max_xp"])
    hp = HpData(hp=LEVEL_META[1]["base_max_hp"], max_hp=LEVEL_META[1]["base_max_hp"])

    def add_xp(self, xp: int) -> None:
        self.level.xp += xp
        self.check_xp()

    def check_xp(self) -> None:
        # Recursive function that updates hp, xp, weapon atk based on player level
        if self.level.level == 10:
            return

        if self.level.xp < self.level.max_xp:
            return

        self.level.level += 1
        self.level.max_xp = LEVEL_META[self.level.level]["max_xp"]

        self.hp.hp = LEVEL_META[self.level.level]["base_max_hp"]
        self.hp.max_hp = LEVEL_META[self.level.level]["base_max_hp"]

        for weapon in inventory.weapons:
            if weapon:
                if weapon.level > self.level.level:
                    raise Exception("Weapon level and player level are out of sync!")

                while weapon.level < self.level.level:
                    weapon.atk = floor(weapon.atk * 1.5)
                    weapon.level += 1

        temp_weapon = Side().temp_weapon  # type: ignore
        if temp_weapon:
            if temp_weapon.level > self.level.level:
                raise Exception("Temp Weapon level and player level are out of sync!")

            while temp_weapon.level < self.level.level:
                temp_weapon.atk = floor(temp_weapon.atk * 1.5)
                temp_weapon.level += 1

        self.check_xp()

    def update_max_hp(self) -> None:
        # An equipped weapon's delusion will change the player's hp capacity for game balance
        if inventory.equipped_weapon is None:
            return

        match inventory.equipped_weapon.delusion.type:
            case Delusions.Freeze:
                hp_multiplier = 1.1
            case Delusions.Burn:
                hp_multiplier = 0.75
            case Delusions.Plant:
                hp_multiplier = 1.5
            case Delusions.Mech:
                hp_multiplier = 1.35
            case Delusions.Corrupt:
                hp_multiplier = 0.8
            case Delusions.Stun:
                hp_multiplier = 1.05
            case Delusions.Zap:
                hp_multiplier = 1.1
            case Delusions.Drain:
                hp_multiplier = 1.0
            case Delusions.Bleed:
                hp_multiplier = 0.9

        if state.hp.hp == state.hp.max_hp:
            state.hp.max_hp = floor(
                round(LEVEL_META[self.level.level]["base_max_hp"]) * hp_multiplier
            )
            state.hp.hp = state.hp.max_hp
        else:
            state.hp.max_hp = floor(
                round(LEVEL_META[self.level.level]["base_max_hp"]) * hp_multiplier
            )


class FightState:
    def __init__(self) -> None:
        self.turn: Turn = Turn.null
        self.phase: Phase = Phase.null


player = Player(176, 61)
state = State()
fight_state = FightState()
inventory = Inventory(
    weapons=[None] * 5,
    heals=[None] * 5,
    items=[],
    _money=10,
    equipped_weapon=None,
)

##### EVERYTHING TO DO WITH THE SIDE #####


class SideState(Enum):
    default = auto()
    inventory = auto()
    console = auto()
    prompt = auto()


@singleton
class Side:
    def __init__(self, pad: window, stdscr: window) -> None:
        self.pad = pad
        self.pad.bkgd(" ", Colors.WALL)

        self.text: str = ""
        self.state: SideState = SideState.default
        self.previous_state: SideState = SideState.default

        self.log_buffer: deque[str] = deque()
        self.prompt_buffer: str = ""

        self.max_log_length: int = G.game_height - 2 - 7 - 8
        self.max_prompt_length: int = G.padding_width - 4 - 18

        self.stdscr = stdscr

        self.temp_weapon: Weapon | None = None

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

        current_weapon = inventory.equipped_weapon

        draw("\n")
        draw("ATK: ", A_BOLD)
        draw(f"{current_weapon.atk if current_weapon else 'NA'}\n")
        draw("WEAPON: ", A_BOLD)
        draw(f"{current_weapon.name if current_weapon else 'NA'}\n")
        draw("DELUSION: ", A_BOLD)
        draw(
            f"{str(current_weapon.delusion.type)[10:] + ' ' + current_weapon.delusion.get_symbol() if current_weapon else 'NA'}\n",
            current_weapon.delusion.get_color() if current_weapon else 0,
        )

        draw(f"\n\nPlayer Y: ", A_BOLD)
        draw(f"{player.y}")
        draw(f"\nPlayer X: ", A_BOLD)
        draw(f"{player.x}")

    def draw_weapon(self, weapon: Weapon | None) -> None:
        draw = self.pad.addstr

        if weapon is None:
            draw("-\n")
            return

        position = inventory.weapons.index(weapon) + 1

        if weapon == inventory.equipped_weapon:
            draw(f"{position}> ", Colors.HEAL)
        else:
            draw(f"{position}. ")

        draw(f"{weapon.name} ", weapon.get_rarity_color())
        draw("[")
        draw(f"{weapon.delusion.get_symbol()} ", weapon.delusion.get_color())
        draw(f"{weapon.atk}]\n")

    def draw_heal(self, heal: Healable | None) -> None:
        draw = self.pad.addstr

        if heal is None:
            draw("-\n")
            return

        position = inventory.heals.index(heal) + 1
        draw(f"{position}. ")

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

    def draw_console_stats(self) -> None:
        draw = self.pad.addstr

        draw("YOU━━━━━━\n")
        draw("HP: ", A_BOLD)
        draw(f"{state.hp.hp}", self.get_health_color())
        draw(" / ")
        draw(f"{state.hp.max_hp}\n", Colors.HP_HIGH)
        draw("ATK/DEL: ", A_BOLD)
        current_weapon = inventory.equipped_weapon
        draw(f"{current_weapon.atk if current_weapon else 'NA'}")
        draw(" / ")
        draw(
            f"{str(current_weapon.delusion.type)[10:] + ' ' + current_weapon.delusion.get_symbol() if current_weapon else 'NA'}\n",
            current_weapon.delusion.get_color() if current_weapon else 0,
        )
        draw(f"\n{'Enemy Name'}━━━━━━\n")
        draw("HP: ", A_BOLD)
        draw(f"Hp")
        draw(" / ")
        draw(f"Max\n", Colors.HP_HIGH)
        draw("ATK/DEL: ", A_BOLD)
        draw(f"ATK")
        draw(" / ")
        draw(f"DEL\n\n")
        draw("~~~~~~\n")

    def draw_console(self, prompt: bool) -> None:
        draw = self.pad.addstr

        self.pad.clear()

        if not prompt:
            draw("~~~CONSOLE/LOG~~~\n\n")

            self.draw_console_stats()

            for t in self.log_buffer:
                draw(f"{t}\n")
        else:
            draw("~~~CONSOLE/PROMPT~~~\n\n")

            self.draw_console_stats()

            for t in self.log_buffer:
                draw(f"{t}\n")

            extra_lines = self.max_log_length - len(self.log_buffer)
            for _ in range(extra_lines + 2):
                draw(f"\n")

            draw("COMMAND:\n", Colors.HEAL)
            draw(self.prompt_buffer, Colors.HEAL)

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

    def toggle_prompt(self) -> None:
        # Can only toggle the prompt whne in console mode
        self.state = SideState.prompt

    def render(self) -> None:
        state.check_xp()
        state.update_max_hp()

        match self.state:
            case SideState.default:
                self.draw_stats()
            case SideState.inventory:
                self.draw_inventory()
            case SideState.console:
                self.draw_console(prompt=False)
            case SideState.prompt:
                self.draw_console(prompt=True)

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
