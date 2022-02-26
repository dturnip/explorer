from typing import Callable
from PIL import Image

from ..colors import Colors
from ..contexts.glob import GlobContext


class Tile:
    def __init__(self, char: str, barrier: bool, color: int, id: int) -> None:
        self.char = char
        self.barrier = barrier
        self.color = color
        self.id = id


PIXEL_TO_TILE: dict[tuple[int, int, int], Callable[..., Tile]] = {
    # Top left 90 intersection
    (240, 240, 240): lambda: Tile("┌", True, Colors.WALL, 10),
    # Top center T intersection
    (230, 230, 230): lambda: Tile("┬", True, Colors.WALL, 11),
    # Top right 90 intersection
    (220, 220, 220): lambda: Tile("┐", True, Colors.WALL, 12),
    # Middle left T intersection
    (210, 210, 210): lambda: Tile("├", True, Colors.WALL, 13),
    # Center four way intersection
    (25, 25, 25): lambda: Tile("┼", True, Colors.WALL, 14),
    # Middle right T intersection
    (200, 200, 200): lambda: Tile("┤", True, Colors.WALL, 15),
    # Bottom left 90 intersection
    (190, 190, 190): lambda: Tile("└", True, Colors.WALL, 16),
    # Bottom center T intersection
    (180, 180, 180): lambda: Tile("┴", True, Colors.WALL, 17),
    # Bottom right 90 intersection
    (170, 170, 170): lambda: Tile("┘", True, Colors.WALL, 18),
    # Horizontal wall
    (120, 120, 120): lambda: Tile("─", True, Colors.WALL, 19),
    # Vertical wall
    (100, 100, 100): lambda: Tile("│", True, Colors.WALL, 20),
    # Path
    (150, 150, 150): lambda: Tile(".", False, Colors.PATH, 21),
    # Enemy \uf5ac
    (255, 0, 0): lambda: Tile("", True, Colors.ENEMY, 22),
    # Chest \uf8d2
    (255, 0, 255): lambda: Tile("", False, Colors.CHEST, 23),
    # Money \uf155
    (255, 255, 0): lambda: Tile("", False, Colors.MONEY, 24),
    # Shop \uf07a
    (91, 192, 192): lambda: Tile("", False, Colors.SHOP, 25),
    # Heal \uf7df
    (0, 255, 0): lambda: Tile("", False, Colors.HEAL, 26),
    # Super \uf005
    (255, 120, 0): lambda: Tile("", False, Colors.SUPER, 27),
    # Healing Grass
    (0, 100, 0): lambda: Tile(" ", False, Colors.GRASS, 28),
    # Tree decoration
    (0, 150, 150): lambda: Tile("", True, Colors.TREE, 29),
    # Checkpoint
    (200, 125, 200): lambda: Tile("", False, Colors.CHECK, 30),
    # Gamble water
    (0, 0, 255): lambda: Tile(" ", False, Colors.WATER, 31),
    # Lock
    (255, 215, 0): lambda: Tile("", True, Colors.LOCK, 32),
    # Key
    (255, 180, 0): lambda: Tile("", False, Colors.KEY, 33),
    # Transparrent tile
    (255, 255, 255): lambda: Tile(" ", False, Colors.BLACK, 999),
}


def parse_image(m: Image.Image) -> list[list[Tile]]:
    G = GlobContext()
    width, height = m.size
    assert width == height == 256

    blank = (255, 255, 255)

    ret = []

    for _ in range(G.center_y):
        ret.append([PIXEL_TO_TILE[blank]() for _ in range(width + G.center_x * 2)])

    for x in range(width):
        ret.append([])

        for _ in range(G.center_x):
            ret[G.center_y + x].append(PIXEL_TO_TILE[blank]())

        for y in range(height):
            ret[G.center_y + x].append(PIXEL_TO_TILE[m.getpixel((y, x))[0:3]]())

        for _ in range(G.center_x):
            ret[G.center_y + x].append(PIXEL_TO_TILE[blank]())

    for _ in range(G.center_y):
        ret.append([PIXEL_TO_TILE[blank]() for _ in range(width + G.center_x * 2)])

    return ret
