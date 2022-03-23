import random
from curses import window

from .lib.parser import Tile
from .globals import Colors, Globals as G
from .ctx import Healable, Rarity, Weapon, player, inventory
from .data.game_items import Weapons, Heals

# GameObject
class Game:
    def __init__(
        self, pad: window, game_map: list[list[Tile]], y_offset: int = 0, x_offset: int = 0
    ) -> None:
        self.pad = pad

        self.game_map = game_map
        self.y_offset = y_offset or player.rel_y
        self.x_offset = x_offset or player.rel_x

        self.redraw()

        self.render()

    def redraw(self) -> None:
        self.pad.clear()
        for row in self.game_map:
            for col in row:
                self.pad.addch(col.char, col.color)
            self.pad.addch("\n")

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

    def remove_tile(self, y, x) -> None:
        self.game_map[y][x] = Tile(".", False, Colors.PATH, 21, "PATH")
        self.redraw()

    # def got(self, *args: Weapon | Healable) -> None:
    #     for item in args:
    #         Side().log(f"Got {item.name}!")  # type: ignore

    def interact_tile(self) -> None:
        y, x = player.map_y, player.map_x
        match self.game_map[y][x].id:
            case 23:  # CHEST
                # Big ass match clause for all the chests
                match (player.y, player.x):
                    case (176, 49):
                        idx = random.randint(1, 3)
                        rand_weapon = Weapons[Rarity.Common][idx]()
                        rand_heal = Heals[1]()
                        inventory.add_weapon(rand_weapon)
                        inventory.add_heal(rand_heal)
                        self.remove_tile(y, x)
                        # self.got(rand_weapon, rand_heal)
                    case (185, 43):
                        rarity = (Rarity.Common, Rarity.Rare)[random.randint(1, 2) == 1]
                        idx = random.randint(1, 9)
                        rand_weapon = Weapons[rarity][idx]()
                        rand_heal = Heals[1]()
                        rand_heal2 = Heals[2]()
                        inventory.add_weapon(rand_weapon)
                        inventory.add_heal(rand_heal)
                        inventory.add_heal(rand_heal2)
                        self.remove_tile(y, x)
                        # self.got(rand_weapon, rand_heal, rand_heal2)
                    case _:
                        # Not implemeneted for this chest yet!
                        pass
            case 24:  # MONEY
                inventory.money += 5
                self.game_map[y][x] = Tile(".", False, Colors.PATH, 21, "PATH")
                self.redraw()
                # Side().log(f"Got $5!")  # type: ignore
                # self.render()
            case _:
                pass

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
