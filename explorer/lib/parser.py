from typing import Callable, Dict, Tuple
from PIL import Image
from explorer.game import Colors


class Tile:
    def __init__(self, char: str, barrier: bool, color: int, id: int) -> None:
        self.char = char
        self.barrier = barrier
        self.color = color
        self.id = id


PIXEL_TO_TILE: dict[tuple[int, int, int], Callable[..., Tile]] = {
    # Top left 90 intersection
    (0, 0, 0): lambda: Tile("┌", True, 0, 10),
    # Top center T intersection
    (0, 0, 0): lambda: Tile("┬", True, 0, 11),
    # Top right 90 intersection
    (0, 0, 0): lambda: Tile("┐", True, 0, 12),
    # Middle left T intersection
    (0, 0, 0): lambda: Tile("├", True, 0, 13),
    # Center four way intersection
    (0, 0, 0): lambda: Tile("┼", True, 0, 14),
    # Middle right T intersection
    (0, 0, 0): lambda: Tile("┤", True, 0, 15),
    # Bottom left 90 intersection
    (0, 0, 0): lambda: Tile("└", True, 0, 16),
    # Bottom center T intersection
    (0, 0, 0): lambda: Tile("┴", True, 0, 17),
    # Bottom right 90 intersection
    (0, 0, 0): lambda: Tile("┘", True, 0, 18),
    # Horizontal wall
    (0, 0, 0): lambda: Tile("─", True, 0, 19),
    # Vertical wall
    (0, 0, 0): lambda: Tile("│", True, 0, 20),
    # Path
    (0, 0, 0): lambda: Tile(".", False, 0, 21),
    # Enemy \uf5ac
    (0, 0, 0): lambda: Tile("", True, 0, 22),
    # Chest \uf8d2
    (0, 0, 0): lambda: Tile("", False, 0, 23),
    # Money \uf155
    (0, 0, 0): lambda: Tile("", False, 0, 24),
    # Shop \uf07a
    (0, 0, 0): lambda: Tile("", False, 0, 25),
    # Heal \uf7df
    (0, 0, 0): lambda: Tile("", False, 0, 26),
    # Super \uf005
    (0, 0, 0): lambda: Tile("", False, 0, 27),
    # Healing Grass
    (0, 0, 0): lambda: Tile(" ", False, 0, 28),
    # Tree decoration
    (0, 0, 0): lambda: Tile("", True, 0, 29),
    # Checkpoint
    (0, 0, 0): lambda: Tile("", False, 0, 30),
    # Indian water
    (0, 0, 0): lambda: Tile(" ", False, 0, 31),
    # Lock
    (0, 0, 0): lambda: Tile("", True, 0, 32),
    # Key
    (0, 0, 0): lambda: Tile("", False, 0, 33),
}
