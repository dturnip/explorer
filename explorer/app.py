import curses
import random
from math import floor
from pathlib import Path
from typing import Protocol

from PIL import Image

from explorer.data.game_items import Weapons

from .ctx import (
    Delusion,
    Delusions,
    Healable,
    Log,
    Phase,
    Rarity,
    Side,
    SideState,
    Turn,
    Weapon,
    inventory,
    player,
    state,
    fight_state,
)
from .game import Game
from .globals import Colors
from .globals import Globals as G

# from .side import Side
from .lib.parser import parse_command, parse_image


class GameObject(Protocol):
    def render(self) -> None:
        """Renders the GameObject"""


class GameWrapper:
    """Main Game object responsible for being the master"""

    def __init__(self, stdscr: curses.window) -> None:
        self.__objects: list[GameObject] = []
        self.stdscr = stdscr

    def initialize(self) -> None:
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        Colors.setup_colors()

        self.render()

    def add_object(self, o: GameObject) -> None:
        self.__objects.append(o)

    def get_game(self) -> Game | None:
        try:
            # type Game is compatible with protocol GameObject, so if this is successful, the type is Game
            game: Game = next(filter(lambda o: isinstance(o, Game), self.__objects))  # type: ignore
            return game
        except StopIteration:
            return None

    def get_side(self):
        try:
            # Doing it like this because the Singleton implementation for Side is a decorator using a wrapper class
            side: Side = next(filter(lambda o: o == Side._instance, self.__objects))  # type: ignore
            return side
        except StopIteration:
            return None

    def listen(self) -> None:
        """
        Acts upon keyboard input
        """
        key = self.stdscr.getch()
        side = self.get_side()
        if not side:
            return

        # Enjoy this beautiful mountain of indents

        # Acts differently depending on the side pad's state
        match side.state:
            # Text input mode
            case SideState.prompt:
                match key:
                    case 10:  # RETURN
                        side.toggle_console()
                        command = side.prompt_buffer
                        side.prompt_buffer = ""

                        if side.temp_weapon:
                            command_result = parse_command(command, replace=True)
                            Log(command_result.resolve)
                            side.render()

                            # Weapon replacement "loop"
                            if not command_result.ok:
                                side.toggle_prompt()

                        # Recursive battle imperative logic
                        elif side.enemy:
                            assert inventory.equipped_weapon

                            # Enemy defeated
                            if side.enemy.hp <= 0:
                                game = self.get_game()
                                assert game

                                # Remove all enemy tiles blocking the path
                                y, x = side.enemy.pos

                                connected_tiles = [
                                    (y, x),
                                    (y + 1, x),
                                    (y - 1, x),
                                    (y, x + 1),
                                    (y, x - 1),
                                ]

                                enemy_tiles = filter(
                                    lambda pair: game.game_map[pair[0]][pair[1]].id == 22,
                                    connected_tiles,
                                )

                                for tile in enemy_tiles:
                                    game.remove_tile(*tile)

                                Log("")
                                Log(f"Defeated {side.enemy.name}")
                                # Reset state and reward XP
                                side.enemy = None
                                inventory.equipped_weapon.atk = side.old_weapon_atk
                                side.old_weapon_atk = 0
                                state.level.xp += 10
                                game.render()
                                return

                            if state.hp.hp <= 0:
                                Log("")
                                Log("")
                                Log("You Lose! [Ctrl-C] to exit")
                                self.render()
                                while True:
                                    pass

                            # Begin effects
                            if fight_state.phase == Phase.begin:
                                match fight_state.turn:
                                    case Turn.player:
                                        Log("[Phase begin! Your Turn!]")
                                        Log("")
                                        if not fight_state.player_fxd:
                                            match inventory.equipped_weapon.delusion.type:
                                                case Delusions.Plant:

                                                    Log(f"~~~Your Plant Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.75:
                                                        heal_qty = floor(state.hp.max_hp * 10 / 100)
                                                        old_hp = state.hp.hp
                                                        state.hp.hp = (
                                                            x
                                                            if (x := old_hp + heal_qty)
                                                            <= state.hp.max_hp
                                                            else state.hp.max_hp
                                                        )
                                                        atk_bonus = floor(
                                                            side.old_weapon_atk * 10 / 100
                                                        )
                                                        inventory.equipped_weapon.atk += atk_bonus
                                                        Log(f"(YOU) +HP {state.hp.hp - old_hp}")
                                                        Log(f"(YOU) +ATK {atk_bonus}")
                                                    else:
                                                        Log("Did nothing")

                                                case Delusions.Zap:
                                                    Log(f"~~~Your Zap Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.75:
                                                        atk_wither = floor(
                                                            side.enemy.original_atk * 15 / 100
                                                        )
                                                        side.enemy.atk -= atk_wither
                                                        Log(f"(ENEMY) -ATK {atk_wither}")
                                                    else:
                                                        Log("Did nothing")
                                    case Turn.opponent:
                                        Log("[Phase begin! Enemy Turn!]")
                                        Log("")
                                        if not fight_state.opponent_fxd:
                                            match side.enemy.delusion.type:
                                                case Delusions.Plant:
                                                    Log(f"~~~Enemy Plant Ability~~~")
                                                    fight_state.opponent_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.75:
                                                        heal_qty = floor(
                                                            side.enemy.max_hp * 10 / 100
                                                        )
                                                        old_hp = side.enemy.hp
                                                        side.enemy.hp = (
                                                            x
                                                            if (x := old_hp + heal_qty)
                                                            <= side.enemy.max_hp
                                                            else side.enemy.max_hp
                                                        )
                                                        atk_bonus = floor(
                                                            side.enemy.original_atk * 10 / 100
                                                        )
                                                        side.enemy.atk += atk_bonus
                                                        Log(f"(ENEMY) +HP {side.enemy.hp - old_hp}")
                                                        Log(f"(ENEMY) +ATK {atk_bonus}")
                                                    else:
                                                        Log("Did nothing")

                                                case Delusions.Zap:
                                                    Log(f"~~~Enemy Zap Ability~~~")
                                                    fight_state.opponent_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.75:
                                                        atk_wither = floor(
                                                            side.old_weapon_atk * 15 / 100
                                                        )
                                                        inventory.equipped_weapon.atk -= atk_wither
                                                        Log(f"(YOU) -ATK {atk_wither}")
                                                    else:
                                                        Log("Did nothing")

                                        enemy_command = parse_command("attack", fight=True)
                                        Log(enemy_command.resolve)
                                        Log("")

                            # End effects
                            if fight_state.phase == Phase.end:
                                match fight_state.turn:
                                    case Turn.player:
                                        Log("[Phase End! Your Turn!]")
                                        Log("")
                                        if not fight_state.player_fxd:
                                            match inventory.equipped_weapon.delusion.type:
                                                case Delusions.Freeze:
                                                    Log("~~~Your Freeze Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.35:
                                                        hp_wither = floor(
                                                            side.enemy.max_hp * 5 / 100
                                                        )

                                                        side.enemy.hp -= hp_wither

                                                        fight_state.phase = Phase.begin
                                                        fight_state.turn = Turn.player
                                                        fight_state.player_fxd = False
                                                        fight_state.opponent_fxd = False

                                                        Log(f"(ENEMY) -HP {hp_wither}")
                                                        Log(f"Skipped Enemy Turn!")
                                                        side.toggle_prompt()
                                                    else:
                                                        Log("Did nothing")
                                                case Delusions.Burn:
                                                    Log("~~~Your Burn Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.5:
                                                        burn_dmg = floor(
                                                            inventory.equipped_weapon.atk * 25 / 100
                                                        )

                                                        side.enemy.hp -= burn_dmg

                                                        Log(f"(ENEMY) -HP {burn_dmg}")
                                                    else:
                                                        Log("Did nothing")
                                                case Delusions.Stun:
                                                    Log("~~~Your Stun Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.35:
                                                        fight_state.phase = Phase.begin
                                                        fight_state.turn = Turn.player
                                                        fight_state.player_fxd = False
                                                        fight_state.opponent_fxd = False

                                                        Log(f"Skipped Enemy Turn!")
                                                        side.toggle_prompt()
                                                    else:
                                                        Log("Did nothing")
                                                case Delusions.Drain:
                                                    Log("~~~Your Drain Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.75:
                                                        heal_qty = (
                                                            inventory.equipped_weapon.atk // 2
                                                        )
                                                        old_hp = state.hp.hp
                                                        state.hp.hp = (
                                                            x
                                                            if (x := old_hp + heal_qty)
                                                            <= state.hp.max_hp
                                                            else state.hp.max_hp
                                                        )

                                                        Log(f"(ENEMY) +HP {state.hp.hp - old_hp}")
                                                    else:
                                                        Log("Did nothing")

                                                case Delusions.Bleed:
                                                    Log("~~~Your Bleed Ability~~~")
                                                    fight_state.player_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.5:
                                                        hp_wither = floor(
                                                            side.enemy.max_hp * 10 / 100
                                                        )

                                                        side.enemy.hp -= hp_wither

                                                        Log(f"(ENEMY) -HP {hp_wither}")
                                                    else:
                                                        Log("Did nothing")

                                    case Turn.opponent:
                                        Log("")
                                        if not fight_state.opponent_fxd:
                                            match side.enemy.delusion.type:
                                                case Delusions.Freeze:
                                                    Log("~~~Enemy Freeze Ability~~~")
                                                    fight_state.opponent_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.35:
                                                        hp_wither = floor(state.hp.max_hp * 5 / 100)

                                                        state.hp.hp -= hp_wither

                                                        fight_state.phase = Phase.begin
                                                        fight_state.turn = Turn.opponent
                                                        fight_state.player_fxd = False
                                                        fight_state.opponent_fxd = False

                                                        Log(f"(YOU) -HP {hp_wither}")
                                                        Log("Skipped Your Turn!")
                                                        side.enemy.extra_turn = True
                                                        side.toggle_prompt()
                                                    else:
                                                        side.enemy.extra_turn = False
                                                        Log("Did nothing")
                                                case Delusions.Burn:
                                                    Log("~~~Enemy Burn Ability~~~")
                                                    fight_state.opponent_fxd = True

                                                    rng = random.random()
                                                    if rng <= 0.5:
                                                        burn_dmg = floor(side.enemy.atk * 25 / 100)

                                                        state.hp.hp -= burn_dmg

                                                        Log(f"(YOU) -HP {burn_dmg}")
                                                    else:
                                                        Log("Did nothing")
                                                case Delusions.Stun:
                                                    Log("~~~Enemy Stun Ability~~~")
                                                    fight_state.opponent_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.35:
                                                        fight_state.phase = Phase.begin
                                                        fight_state.turn = Turn.opponent
                                                        fight_state.player_fxd = False
                                                        fight_state.opponent_fxd = False

                                                        Log(f"Skipped Your Turn!")
                                                        side.enemy.extra_turn = True
                                                        side.toggle_prompt()
                                                    else:
                                                        side.enemy.extra_turn = False
                                                        Log("Did nothing")
                                                case Delusions.Drain:
                                                    Log("~~~Enemy Drain Ability~~~")
                                                    fight_state.opponent_fxd = True
                                                    rng = random.random()
                                                    if rng <= 0.75:
                                                        heal_qty = side.enemy.atk // 2

                                                        old_hp = side.enemy.hp
                                                        side.enemy.hp = (
                                                            x
                                                            if (x := old_hp + heal_qty)
                                                            <= side.enemy.max_hp
                                                            else side.enemy.max_hp
                                                        )

                                                        Log(f"(ENEMY) +HP {side.enemy.hp - old_hp}")
                                                    else:
                                                        Log("Did nothing")
                                                case Delusions.Bleed:
                                                    Log("~~~Enemy Bleed Ability~~~")
                                                    fight_state.opponent_fxd = True

                                                    rng = random.random()
                                                    if rng <= 0.5:
                                                        hp_wither = floor(
                                                            state.hp.max_hp * 10 / 100
                                                        )

                                                        state.hp.hp -= hp_wither

                                                        Log(f"(YOU) -HP {hp_wither}")
                                                    else:
                                                        Log("Did nothing")

                            # Command input
                            if fight_state.turn == Turn.player:
                                if not (command.isspace() or command == ""):
                                    # Dev cheat
                                    if command == "kill":
                                        side.enemy.hp = 0

                                    command_result = parse_command(command, fight=True)
                                    Log(command_result.resolve)
                                    side.render()
                            elif fight_state.turn == Turn.opponent and not side.enemy.extra_turn:
                                enemy_command = parse_command("pass", fight=True)
                                Log(enemy_command.resolve)
                                side.render()

                            # Recurse the function if the enemy is still alive
                            if side.enemy:
                                side.toggle_prompt()
                        else:
                            # Guard here so the console logger doesn't log blank lines
                            if not (command.isspace() or command == ""):
                                command_result = parse_command(command)
                                Log(command_result.resolve)

                                if command_result.ok:
                                    side.state = side.previous_state

                    case 127:  # DELETE
                        side.prompt_buffer = side.prompt_buffer[:-1]
                    case _:  # Any other key: echo it and add it to the command string buffer!
                        if len(side.prompt_buffer) < side.max_prompt_length:
                            side.prompt_buffer += chr(key)

            # All other side pad states: regular key flow
            case _:
                game = self.get_game()
                if not game:
                    return

                match key:
                    case 119:  # w
                        game.displace_up()
                    case 97:  # a
                        game.displace_left()
                    case 115:  # s
                        game.displace_down()
                    case 100:  # d
                        game.displace_right()
                    case 69 | 101:  # E or e
                        # Interact with the tile
                        game.interact_tile()
                    case 73 | 105:  # I or i
                        side.toggle_inventory()
                    case 67 | 99:  # C or c
                        side.toggle_console()
                    case 80 | 112:  # P or p
                        side.previous_state = side.state
                        side.toggle_prompt()
                    case 81:  # Q
                        # Will get caught and break the loop
                        raise Exception

    def render_border(self) -> None:
        """
        Math code that I don't understand anymore which renders the purple borders
        """
        draw = self.stdscr.addstr

        self.stdscr.attron(Colors.OVERLAY)
        # Main Border corners
        draw(G.padding_height, G.padding_width, "╔")
        draw(G.padding_height, G.padding_width + G.game_width - 1, "╗")
        draw(G.padding_height + G.game_height - 1, G.padding_width, "╚")
        draw(G.padding_height + G.game_height - 1, G.padding_width + G.game_width - 1, "╝")

        # Main Border top, bottom
        draw(G.padding_height, G.padding_width + 1, "═" * (G.game_width - 2))
        draw(G.padding_height + G.game_height - 1, G.padding_width + 1, "═" * (G.game_width - 2))

        # Main Border left, right
        for y in range(G.game_height - 2):
            draw(G.padding_height + y + 1, G.padding_width, "║")
            draw(G.padding_height + y + 1, G.padding_width + G.game_width - 1, "║")

        # Side Border corners
        draw(G.padding_height, 1, "╔")
        draw(G.padding_height, G.padding_width - 2, "╗")
        draw(G.padding_height + G.game_height - 1, 1, "╚")
        draw(G.padding_height + G.game_height - 1, G.padding_width - 2, "╝")

        # Side Border top, bottom
        draw(G.padding_height, 2, "═" * (G.padding_width - 4))
        draw(G.padding_height + G.game_height - 1, 2, "═" * (G.padding_width - 4))

        # Side Border left, right
        for y in range(G.game_height - 2):
            draw(G.padding_height + y + 1, 1, "║")
            draw(G.padding_height + y + 1, G.padding_width - 2, "║")

        # fmt: on
        self.stdscr.attroff(Colors.OVERLAY)

    def render_player(self) -> None:
        """
        Render player and player skin in the center of the screen
        """
        game = self.get_game()

        if not game:
            return

        player_color: int
        player_char: str
        match game.game_map[player.map_y][player.map_x].id:
            case 23:  # CHEST
                player_color = Colors.CHEST
                player_char = "E"
            case 24:  # MONEY
                player_color = Colors.MONEY
                player_char = "E"
            case 26:  # HEAL
                player_color = Colors.HEAL
                player_char = "E"
            case 27:  # MYTHIC
                player_color = Colors.SUPER
                player_char = "E"
            case 34:  # ATTACK
                enemy = game.check_enemy(player.map_y, player.map_x)
                if enemy.enemy:
                    player_color = Colors.ENEMY
                    player_char = "E"
                else:
                    player_color = Colors.OVERLAY
                    player_char = ""

            case _:
                player_color = Colors.OVERLAY
                player_char = ""

        self.stdscr.addstr(G.center_y, G.center_x, player_char, player_color)

    def render(self) -> None:
        """
        Calls the render method on all gameobjects
        """
        self.stdscr.clear()
        self.render_border()
        self.stdscr.refresh()
        for o in self.__objects:
            o.render()
        self.render_player()

    def run(self) -> None:
        # I'm keeping the try/except commented out because this game is probably error prone
        # try:
        while True:
            self.listen()
            self.render()

        # except:
        #     pass


def main(stdscr: curses.window):

    # # Memory debugging
    # import tracemalloc
    #
    # tracemalloc.start()

    game = GameWrapper(stdscr)
    game.initialize()
    game.add_object(
        Game(
            curses.newpad(257 + G.center_y * 2, 257 + G.center_x * 2),
            parse_image(
                Image.open(Path(__file__).resolve().parents[1] / "krita" / "explorer_map.png")
            ),
        ),
    )

    game.add_object(
        Side(
            curses.newpad(G.game_height - 1, G.padding_width - 4),
            stdscr,
        )
    )

    # Give you a free exclusive weapon
    hard_stick = Weapon("Potato", 10, Delusion(Delusions.Plant), Rarity.Common)
    inventory.add_weapon(hard_stick)
    inventory.equipped_weapon = hard_stick

    game.render()
    game.run()

    # # Memory debugging
    # curr, peak = tracemalloc.get_traced_memory()
    # print(f"Current: {curr} bytes; Peak: {peak} bytes")
    # tracemalloc.stop()
    # while True:
    #     pass
