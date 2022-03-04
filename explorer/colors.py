from recordclass import RecordClass  # type: ignore


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
