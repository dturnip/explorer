from math import floor
import random
from typing import Callable

from PIL import Image

from ..ctx import Delusions, Phase, Side, Turn, inventory, state, player, fight_state, Log
from ..globals import Colors
from ..globals import Globals as G


class Tile:
    """
    Tile objects that the game map is comprised of
    """

    # Memory optimize
    __slots__ = ("char", "barrier", "color", "id", "name")

    def __init__(self, char: str, barrier: bool, color: int, id: int, name: str) -> None:
        self.char = char
        self.barrier = barrier
        self.color = color
        self.id = id
        self.name = name


PIXEL_TO_TILE: dict[tuple[int, int, int], Callable[..., Tile]] = {
    # Top left 90 intersection
    (240, 240, 240): lambda: Tile("┌", True, Colors.WALL, 10, "TOPL"),
    # Top center T intersection
    (230, 230, 230): lambda: Tile("┬", True, Colors.WALL, 11, "TOPM"),
    # Top right 90 intersection
    (220, 220, 220): lambda: Tile("┐", True, Colors.WALL, 12, "TOPR"),
    # Middle left T intersection
    (210, 210, 210): lambda: Tile("├", True, Colors.WALL, 13, "MIDL"),
    # Center four way intersection
    (25, 25, 25): lambda: Tile("┼", True, Colors.WALL, 14, "MIDM"),
    # Middle right T intersection
    (200, 200, 200): lambda: Tile("┤", True, Colors.WALL, 15, "MIDR"),
    # Bottom left 90 intersection
    (190, 190, 190): lambda: Tile("└", True, Colors.WALL, 16, "BOTL"),
    # Bottom center T intersection
    (180, 180, 180): lambda: Tile("┴", True, Colors.WALL, 17, "BOTM"),
    # Bottom right 90 intersection
    (170, 170, 170): lambda: Tile("┘", True, Colors.WALL, 18, "BOTR"),
    # Horizontal wall
    (120, 120, 120): lambda: Tile("─", True, Colors.WALL, 19, "HWALL"),
    # Vertical wall
    (100, 100, 100): lambda: Tile("│", True, Colors.WALL, 20, "VWALL"),
    # Path
    (150, 150, 150): lambda: Tile(".", False, Colors.PATH, 21, "PATH"),
    # Enemy (icon not final)
    # (255, 0, 0): lambda: Tile("", True, Colors.ENEMY, 22, "ENEMY"),
    (255, 0, 0): lambda: Tile("", True, Colors.ENEMY, 22, "ENEMY"),
    # Chest
    (255, 0, 255): lambda: Tile("", False, Colors.CHEST, 23, "CHEST"),
    # Money
    (255, 255, 0): lambda: Tile("", False, Colors.MONEY, 24, "MONEY"),
    # Shop
    (91, 192, 192): lambda: Tile("", False, Colors.SHOP, 25, "SHOP"),
    # Heal
    (0, 255, 0): lambda: Tile("", False, Colors.HEAL, 26, "HEAL"),
    # Super
    (255, 120, 0): lambda: Tile("", False, Colors.SUPER, 27, "SUPER"),
    # Healing Grass
    (0, 100, 0): lambda: Tile(" ", False, Colors.GRASS, 28, "GRASS"),
    # Tree decoration
    (0, 150, 150): lambda: Tile("", True, Colors.TREE, 29, "TREE"),
    # Checkpoint
    (200, 125, 200): lambda: Tile("", False, Colors.CHECK, 30, "SPAWN"),
    # Gamble water
    (0, 0, 255): lambda: Tile(" ", False, Colors.WATER, 31, "WATER"),
    # Lock
    (255, 215, 0): lambda: Tile("", True, Colors.LOCK, 32, "LOCK"),
    # Key
    (255, 180, 0): lambda: Tile("", False, Colors.KEY, 33, "KEY"),
    # Attack path
    # Change this to Colors.PATH once it works
    (200, 0, 0): lambda: Tile(".", False, Colors.PATH, 34, "ATTACK"),
    # Transparrent tile
    (255, 255, 255): lambda: Tile(" ", False, Colors.BLACK, 999, "VOID"),
}


def parse_image(m: Image.Image) -> list[list[Tile]]:
    """Parses an Image and returns a 2D array of Tiles with padding on all four edges"""
    w, h = m.size
    assert w == h == 256
    blank = (255, 255, 255)
    ret = []

    for _ in range(G.center_y):
        ret.append([PIXEL_TO_TILE[blank]() for _ in range(w + G.center_x * 2)])

    for x in range(w):
        ret.append([])

        for _ in range(G.center_x):
            ret[G.center_y + x].append(PIXEL_TO_TILE[blank]())
        for y in range(h):
            ret[G.center_y + x].append(PIXEL_TO_TILE[m.getpixel((y, x))[0:3]]())
        for _ in range(G.center_x):
            ret[G.center_y + x].append(PIXEL_TO_TILE[blank]())

    for _ in range(G.center_y):
        ret.append([PIXEL_TO_TILE[blank]() for _ in range(w + G.center_x * 2)])

    return ret


COMMANDS = {
    "equip",
    "replace",
    "discard",
    "attack",
    "pass",
    "heal",
    "abandon",
    "showheals",
}


class CommandResult:
    def __init__(self, resolve: str, ok: bool) -> None:
        self.resolve = resolve
        self.ok = ok


def parse_command(command: str, **kwargs) -> CommandResult:
    """
    Takes in a command, verifies it, and hence parses it. Returns a CommandResult
    """
    tokens = command.split()
    token_stream = iter(tokens)

    parsed_action: str = ""

    try:
        command_name = next(token_stream)
        side = Side()  # type: ignore

        if kwargs.get("replace"):
            if command_name not in ["replace", "discard"]:
                return CommandResult(f"Can only use `replace`/`discard` now", ok=False)

        if not command_name in COMMANDS:
            return CommandResult(f"{command_name}: invalid command", ok=False)

        if kwargs.get("fight"):
            match fight_state.phase:
                case Phase.begin:
                    if command_name not in ["heal", "attack", "pass", "abandon", "showheals"]:
                        return CommandResult("Can't use that in begin phase!", ok=False)
                case Phase.end:
                    if command_name not in ["heal", "pass", "abandon", "showheals"]:
                        return CommandResult("Can't use that in end phase!", ok=False)
                case _:
                    pass

        match command_name:
            case "equip":
                if len(tokens) != 2:
                    return CommandResult("Invalid arguments to `equip`", ok=False)

            case "heal":
                if len(tokens) != 2:
                    return CommandResult("Invalid arguments to `heal`", ok=False)

            case "replace":
                _ = kwargs["replace"]
                if len(tokens) != 2:
                    return CommandResult("Invalid arguments to `replace`", ok=False)

            case "discard":
                _ = kwargs["replace"]

                weapon = side.temp_weapon
                assert weapon
                side.temp_weapon = None
                parsed_action += f"Discarded {weapon.name}"
                del weapon

            case "showheals":
                _ = kwargs["fight"]

                # Filters out all None elements
                heals = list(filter(lambda heal: heal, inventory.heals))

                if len(heals) == 0:
                    return CommandResult("You have 0 heals", ok=True)

                Log("~~~YOUR HEALS~~~")
                for i, heal in enumerate(heals):
                    assert heal
                    Log(f"{i+1}. {heal.name} [+{heal.amount}%]")

                return CommandResult("", ok=True)

            case "attack":
                _ = kwargs["fight"]
                assert inventory.equipped_weapon
                assert side.enemy

                match fight_state.turn:
                    case Turn.player:
                        damage = inventory.equipped_weapon.atk

                        if (
                            inventory.equipped_weapon.delusion.get_strong()
                            == side.enemy.delusion.type
                        ):
                            damage = floor(damage * 1.5)

                        # Counter ability
                        match side.enemy.delusion.type:
                            case Delusions.Mech:
                                Log("~~~Enemy Mech Counter~~~")
                                rng = random.random()
                                if rng <= 0.75:
                                    damage //= 2
                                    charge = floor(side.enemy.original_atk * 10 / 100)
                                    side.enemy.atk += charge
                                    Log("Halved damage")
                                    Log(f"(ENEMY) +ATK {charge}")
                                else:
                                    Log("Did nothing")

                            case Delusions.Corrupt:
                                Log("~~~Enemy Corrupt Counter~~~")
                                rng = random.random()
                                if rng <= 0.5:
                                    mirror_damage = floor(damage / 2)
                                    damage = 0

                                    state.hp.hp -= mirror_damage
                                    Log("Corrupted damage")
                                    Log(f"(YOU) -HP {mirror_damage}")
                                else:
                                    Log("Did nothing")

                            case _:
                                pass

                        side.enemy.hp -= damage
                        Log("")
                        Log(f"You Dealt {damage} damage")

                    case Turn.opponent:
                        damage = side.enemy.atk

                        if (
                            side.enemy.delusion.get_strong()
                            == inventory.equipped_weapon.delusion.type
                        ):
                            damage = floor(damage * 1.5)

                        # Counter ability
                        match inventory.equipped_weapon.delusion.type:
                            case Delusions.Mech:
                                Log("~~~Your Mech Counter~~~")
                                rng = random.random()
                                if rng <= 0.75:
                                    damage //= 2
                                    charge = floor(side.old_weapon_atk * 10 / 100)
                                    inventory.equipped_weapon.atk += charge
                                    Log("Halved damage")
                                    Log(f"(YOU) +ATK {charge}")
                                else:
                                    Log("Did nothing")

                            case Delusions.Corrupt:
                                Log("~~~Your Corrupt Counter~~~")
                                rng = random.random()
                                if rng <= 0.5:
                                    mirror_damage = floor(damage / 2)
                                    damage = 0

                                    side.enemy.hp -= mirror_damage
                                    Log("Corrupted damage")
                                    Log(f"(ENEMY) -HP {mirror_damage}")
                                else:
                                    Log("Did nothing")

                        state.hp.hp -= damage
                        Log("")
                        Log(f"Enemy Dealt {damage} damage")

                fight_state.phase = Phase.end
                Log("")

            case "pass":
                _ = kwargs["fight"]

                if fight_state.turn == Turn.player:
                    fight_state.turn = Turn.opponent
                elif fight_state.turn == Turn.opponent:
                    fight_state.turn = Turn.player

                fight_state.player_fxd = False
                fight_state.opponent_fxd = False

                fight_state.phase = Phase.begin

                parsed_action += "Turn passed"

            case "abandon":
                _ = kwargs["fight"]
                assert inventory.equipped_weapon

                # Reset all this fight state
                side.enemy = None
                inventory.equipped_weapon.atk = side.old_weapon_atk
                side.old_weapon_atk = 0
                fight_state.turn = Turn.null
                fight_state.phase = Phase.null
                fight_state.player_fxd = False
                fight_state.opponent_fxd = False

                parsed_action += "Abandoned fight"

        arg = next(token_stream)
        val = int(arg)

        match command_name:
            case "equip":
                if val not in range(1, 6):
                    return CommandResult("Invalid arguments to `equip`", ok=False)

                target_weapon = inventory.weapons[val - 1]
                if target_weapon is None:
                    return CommandResult(f"Slot {val} is None", ok=False)

                # Valid command
                inventory.equipped_weapon = target_weapon
                parsed_action += f"Equipped {target_weapon.name}"

            case "replace":
                if val not in range(1, 6):
                    return CommandResult("Invalid arguments to `replace`", ok=False)

                target_weapon = inventory.weapons[val - 1]
                assert target_weapon

                weapon = side.temp_weapon
                assert weapon
                side.temp_weapon = None
                inventory.weapons[val - 1] = weapon
                inventory.equipped_weapon = weapon
                parsed_action += f"Replaced {{{val}}} with {weapon.name}"
            case "heal":
                if val not in range(1, 6):
                    return CommandResult("Invalid arguments to `heal`", ok=False)

                target_heal = inventory.heals[val - 1]
                if target_heal is None:
                    return CommandResult(f"Slow {val} is None", ok=False)

                inventory.heals[val - 1] = None

                heals = list(filter(lambda heal: heal, inventory.heals))
                inventory.heals = [None] * 5
                for heal in heals:
                    assert heal
                    inventory.add_heal(heal)

                heal_qty = floor(state.hp.max_hp * target_heal.amount / 100)
                old_hp = state.hp.hp
                state.hp.hp = (
                    # Ensure that you can't heal over max hp
                    x
                    if (x := old_hp + heal_qty) <= state.hp.max_hp
                    else state.hp.max_hp
                )
                parsed_action += f"Healed {state.hp.hp - old_hp}HP"

        next(token_stream)
        # This line will never be run, but my python LSP wants the function to return a CommandResult
        return CommandResult(f"Invalid arguments to `{command_name}`", ok=False)

    except KeyError:
        # If your LSP says this could be unbound, trust me it won't
        return CommandResult(f"Cannot use `{command_name}` now", ok=False)
    except ValueError:
        return CommandResult("Argument must be an integer", ok=False)
    except StopIteration:
        return CommandResult(parsed_action, ok=True)
