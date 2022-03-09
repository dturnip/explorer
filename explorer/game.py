from curses import window
from .lib.parser import Tile
from .globals import Globals as G
from .ctx import player

# GameObject
class Game:
    def __init__(
        self, pad: window, game_map: list[list[Tile]], y_offset: int = 0, x_offset: int = 0
    ) -> None:
        self.pad = pad

        self.game_map = game_map
        self.y_offset = y_offset or player.rel_y
        self.x_offset = x_offset or player.rel_x

        for row in game_map:
            for col in row:
                self.pad.addch(col.char, col.color)
            self.pad.addch("\n")

        self.render()

    def render(self) -> None:
        self.pad.refresh(
            self.y_offset,
            self.x_offset,
            G.padding_height + 1,
            G.padding_width + 1,
            G.padding_height + G.game_height - 2,
            G.padding_width + G.game_width - 2,
        )

    def is_block(self, y, x) -> bool:
        match self.game_map[y][x].id:
            # Walls, enemies, locks
            # TODO: Make the player be able to stand of the enemy and interact with it, but not pass it
            case t if t in list(range(21)) + [22, 32]:
                return True
            case _:
                return False

    def displace_up(self) -> None:
        if self.y_offset - 1 > G.padding_height and not self.is_block(
            player.map_y - 1, player.map_x
        ):
            self.y_offset -= 1
            player.y -= 1

    def displace_down(self) -> None:
        if self.y_offset < 256 + G.padding_height and not self.is_block(
            player.map_y + 1, player.map_x
        ):
            self.y_offset += 1
            player.y += 1

    def displace_left(self) -> None:
        if self.x_offset - 1 > G.padding_width and not self.is_block(
            player.map_y, player.map_x - 1
        ):
            self.x_offset -= 1
            player.x -= 1

    def displace_right(self) -> None:
        if self.x_offset < 256 + G.padding_width and not self.is_block(
            player.map_y, player.map_x + 1
        ):
            self.x_offset += 1
            player.x += 1
