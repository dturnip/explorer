from typing import Callable
from PIL import Image
from ..globals import Colors, Globals as G


class Tile:
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
    # Enemy \uf5ac
    (255, 0, 0): lambda: Tile("", True, Colors.ENEMY, 22, "ENEMY"),
    # Chest \uf8d2
    (255, 0, 255): lambda: Tile("", False, Colors.CHEST, 23, "CHEST"),
    # Money \uf155
    (255, 255, 0): lambda: Tile("", False, Colors.MONEY, 24, "MONEY"),
    # Shop \uf07a
    (91, 192, 192): lambda: Tile("", False, Colors.SHOP, 25, "SHOP"),
    # Heal \uf7df
    (0, 255, 0): lambda: Tile("", False, Colors.HEAL, 26, "HEAL"),
    # Super \uf005
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
