import random
from curses import window

from .ctx import Delusion, Healable, Rarity, Weapon, inventory, player, state
from .data.game_items import Enemies, Heals, Weapons
from .globals import Colors
from .globals import Globals as G
from .lib.parser import Tile


class EnemyResult:
    def __init__(
        self,
        enemy: Tile | None = None,
        pos: tuple[int, int] | None = None,
        atk: int | None = None,
        hp: int | None = None,
        delusion: Delusion | None = None,
        name: str | None = None,
    ) -> None:
        self.enemy = enemy
        self.pos = pos
        self.atk = atk
        self.hp = hp
        self.delusion = delusion
        self.name = name


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
            case t if t in list(range(21)) + [22, 32]:
                return True
            case _:
                return False

    def check_enemy(self, y, x) -> EnemyResult:
        up = self.game_map[y - 1][x]
        down = self.game_map[y + 1][x]
        left = self.game_map[y][x - 1]
        right = self.game_map[y][x + 1]

        tiles = [up, down, left, right]
        ids = [up.id, down.id, left.id, right.id]

        try:
            enemy_idx = ids.index(22)
        except ValueError:
            return EnemyResult()

        enemy = tiles[enemy_idx]

        y = [self.game_map.index(r) for r in self.game_map if enemy in r][0]
        x = [r.index(enemy) for r in self.game_map if enemy in r][0]

        enemy_data = Enemies[(player.y, player.x)]
        atk, hp, delusion, name = enemy_data.values()

        return EnemyResult(enemy, (y, x), atk, hp, delusion, name)

    def remove_tile(self, y, x) -> None:
        self.game_map[y][x] = Tile(".", False, Colors.PATH, 21, "PATH")
        self.redraw()

    def handle_chest(self, y, x) -> None:
        self.remove_tile(y, x)
        state.add_xp(10)

    @staticmethod
    def random_heal() -> Healable:
        rng = random.random()
        # Chance for bandage: 60%
        # Chance for health pot: 25%
        # Chance for med kit: 12%
        # Chance for blessing: 3%
        if rng < 0.03:
            return Heals[4]()
        elif rng < 0.15:
            return Heals[3]()
        elif rng < 0.40:
            return Heals[2]()
        else:
            return Heals[1]()

    def interact_tile(self) -> None:
        y, x = player.map_y, player.map_x
        match self.game_map[y][x].id:
            case 23:  # CHEST
                # Big ass match clause for all the chests
                match (player.y, player.x):
                    case (176, 49):
                        self.handle_chest(y, x)
                        idx = random.randint(1, 3)
                        rand_weapon = Weapons[Rarity.Common][idx]()
                        rand_heal = Heals[1]()
                        inventory.add_weapon(rand_weapon)
                        inventory.add_heal(rand_heal)
                    case (185, 43):
                        self.handle_chest(y, x)
                        rarity = (Rarity.Common, Rarity.Rare)[random.randint(1, 2) == 1]
                        idx = random.randint(1, 9)
                        rand_weapon = Weapons[rarity][idx]()
                        rand_heal = Heals[1]()
                        rand_heal2 = Heals[2]()
                        inventory.add_weapon(rand_weapon)
                        inventory.add_heal(rand_heal)
                        inventory.add_heal(rand_heal2)
                    case _:
                        self.handle_chest(y, x)
                        rng = random.randint(1, 6)
                        rarity = (
                            Rarity.Common
                            if rng == 1 or rng == 2 or rng == 3
                            else Rarity.Rare
                            if rng == 4 or rng == 5
                            else Rarity.Epic
                        )
                        idx = random.randint(1, 9)
                        rand_weapon = Weapons[rarity][idx]()
                        rand_heal = self.random_heal()
                        inventory.add_weapon(rand_weapon)
                        inventory.add_heal(rand_heal)
            case 24:  # MONEY
                self.remove_tile(y, x)
                inventory.money += 5
            case 26:  # HEAL
                self.remove_tile(y, x)
                inventory.add_heal(self.random_heal())
            case 34:  # FIGHT
                if self.game_map[player.map_y][player.map_x].id != 34:
                    return

                enemy = self.check_enemy(player.map_y, player.map_x)
                if not enemy.enemy:
                    return

                # TODO Set the enemy into temp state, and enter fight state(ctx.py)
                self.remove_tile(enemy.pos[0], enemy.pos[1])
                state.hp.hp -= 30
                self.render()
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
