import curses
from pathlib import Path
from PIL import Image
from typing import Protocol

from .globals import Colors, Globals as G
from .game import Game

# from .side import Side
from .lib.parser import parse_image, parse_command
from .ctx import (
    Delusion,
    Delusions,
    Log,
    Rarity,
    SideState,
    Weapon,
    Healable,
    inventory,
    player,
    Side,
)


class GameObject(Protocol):
    def render(self) -> None:
        """Renders the GameObject"""


class GameWrapper:
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
        key = self.stdscr.getch()
        side = self.get_side()
        if not side:
            return
        state = side.state

        match state:
            case SideState.prompt:
                match key:
                    case 10:  # RETURN
                        side.toggle_console()
                        command = side.prompt_buffer
                        side.prompt_buffer = ""

                        # Guard here so the console logger doesn't log blank lines
                        if not (command.isspace() or command == ""):
                            command_result = parse_command(command)
                            Log(parse_command(command).resolve)

                            if command_result.ok:
                                side.state = side.previous_state

                    case 127:  # DELETE
                        side.prompt_buffer = side.prompt_buffer[:-1]
                    case _:  # Any other key: echo it and add it to the command string buffer!
                        if len(side.prompt_buffer) < side.max_prompt_length:
                            side.prompt_buffer += chr(key)
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

        # match key:
        #     case 119:  # w
        #         (game := self.get_game()) and game.displace_up()
        #     case 97:  # a
        #         (game := self.get_game()) and game.displace_left()
        #     case 115:  # s
        #         (game := self.get_game()) and game.displace_down()
        #     case 100:  # d
        #         (game := self.get_game()) and game.displace_right()
        #     case 69 | 101:  # E or e
        #         # Interact with the tile
        #         (game := self.get_game()) and game.interact_tile()
        #     case 73 | 105:  # I or i
        #         (side := self.get_side()) and side.toggle_inventory()
        #     case 67 | 99:  # C or c
        #         (side := self.get_side()) and side.toggle_console()
        #     case 80 | 112:  # P or p
        #         (side := self.get_side()) and side.toggle_prompt()
        #     case 81:  # Q
        #         # Will get caught and break the loop
        #         raise Exception

    def render_border(self) -> None:
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
            case _:
                player_color = Colors.OVERLAY
                player_char = ""

        self.stdscr.addstr(G.center_y, G.center_x, player_char, player_color)

    def render(self) -> None:
        self.stdscr.clear()
        self.render_border()
        self.stdscr.refresh()
        for o in self.__objects:
            o.render()
        self.render_player()

    def run(self) -> None:
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

    game.render()
    game.run()

    # # Memory debugging
    # curr, peak = tracemalloc.get_traced_memory()
    # print(f"Current: {curr} bytes; Peak: {peak} bytes")
    # tracemalloc.stop()
    # while True:
    #     pass
