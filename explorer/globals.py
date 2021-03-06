from os import get_terminal_size
from math import floor
from curses import init_pair, color_pair
from recordclass import RecordClass  # type: ignore


class Globals:
    w, h = get_terminal_size()

    if h % 2 == 0:
        h -= 1
    if w % 2 == 0:
        w -= 1

    height = h
    width = w
    center_y = height // 2
    center_x = width // 2
    game_height = height - 2 * floor(height / 8)
    game_width = floor((width - 2 * floor(width / 8)) * 7 / 8)

    # Map padding so the player can actually move to the edge of the map.
    # It's a weird curses thing
    padding_height = (height - game_height) // 2
    padding_width = width - game_width


class Colors(RecordClass):
    WALL: int
    PATH: int
    OVERLAY: int
    ENEMY: int
    CHEST: int
    MONEY: int
    SHOP: int
    HEAL: int
    SUPER: int
    GRASS: int
    TREE: int
    CHECK: int
    WATER: int
    LOCK: int
    KEY: int

    BLACK: int
    HP_LOW: int
    HP_MID: int
    HP_HIGH: int

    FREEZE: int
    BURN: int
    PLANT: int
    MECH: int
    CORRUPT: int
    STUN: int
    ZAP: int
    DRAIN: int
    BLEED: int

    COMMON: int
    RARE: int
    EPIC: int
    MYTHIC: int

    @staticmethod
    def setup_colors():
        init_pair(1, 231, 16)
        init_pair(2, 240, 16)
        init_pair(3, 135, 16)
        init_pair(4, 160, 16)
        init_pair(5, 95, 16)
        init_pair(6, 226, 16)
        init_pair(7, 87, 16)
        init_pair(8, 47, 16)
        init_pair(9, 202, 16)
        init_pair(10, 29, 29)
        init_pair(11, 34, 16)
        init_pair(12, 212, 16)
        init_pair(13, 27, 27)
        init_pair(14, 214, 16)
        init_pair(15, 223, 16)

        init_pair(99, 16, 16)
        init_pair(100, 196, 16)
        init_pair(101, 220, 16)
        init_pair(102, 46, 16)

        init_pair(200, 87, 16)
        init_pair(201, 202, 16)
        init_pair(202, 76, 16)
        init_pair(203, 245, 16)
        init_pair(204, 141, 16)
        init_pair(205, 130, 16)
        init_pair(206, 220, 16)
        init_pair(207, 90, 16)
        init_pair(208, 196, 16)

        init_pair(209, 248, 16)
        init_pair(210, 69, 16)
        init_pair(211, 177, 16)
        init_pair(212, 208, 16)

        Colors.WALL = color_pair(1)  # white on black
        Colors.PATH = color_pair(2)  # gray on black
        Colors.OVERLAY = color_pair(3)  # purple on black
        Colors.ENEMY = color_pair(4)  # red on black
        Colors.CHEST = color_pair(5)  # pink-brown on black (UNCONFIRMED)
        Colors.MONEY = color_pair(6)  # yellow on black
        Colors.SHOP = color_pair(7)  # cyan on black (UNCONFIRMED)
        Colors.HEAL = color_pair(8)  # light-green on black
        Colors.SUPER = color_pair(9)  # orange on black
        Colors.GRASS = color_pair(10)  # deep-gren on deep-gren (UNCONFIRMED)
        Colors.TREE = color_pair(11)  # green on black
        Colors.CHECK = color_pair(12)  # pink on black
        Colors.WATER = color_pair(13)  # blue on blue (UNCONFIRMED)
        Colors.LOCK = color_pair(14)  # gold on black
        Colors.KEY = color_pair(15)  # tan-yellow on black

        Colors.BLACK = color_pair(99)  # black on black
        Colors.HP_LOW = color_pair(100)  # red on black
        Colors.HP_MID = color_pair(101)  # yellow on black
        Colors.HP_HIGH = color_pair(102)  # green on black

        Colors.FREEZE = color_pair(200)
        Colors.BURN = color_pair(201)
        Colors.PLANT = color_pair(202)
        Colors.MECH = color_pair(203)
        Colors.CORRUPT = color_pair(204)
        Colors.STUN = color_pair(205)
        Colors.ZAP = color_pair(206)
        Colors.DRAIN = color_pair(207)
        Colors.BLEED = color_pair(208)

        Colors.COMMON = color_pair(209)  # common silver
        Colors.RARE = color_pair(210)  # rare blue
        Colors.EPIC = color_pair(211)  # epic purple
        Colors.MYTHIC = color_pair(212)  # legendary orange
