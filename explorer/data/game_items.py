from typing import Callable

from ..ctx import Delusion, Delusions, Healable, Rarity, Weapon, state

Weapons: dict[Rarity, dict[int, Callable[..., Weapon]]] = {
    Rarity.Common: {
        1: lambda: Weapon("Icicle", 19, Delusion(Delusions.Freeze), Rarity.Common),
        2: lambda: Weapon("Iron Sword", 24, Delusion(Delusions.Burn), Rarity.Common),
        3: lambda: Weapon("Rose Whip", 11, Delusion(Delusions.Plant), Rarity.Common),
        4: lambda: Weapon("Laser Cannon", 16, Delusion(Delusions.Mech), Rarity.Common),
        5: lambda: Weapon("Dark Gloop", 12, Delusion(Delusions.Corrupt), Rarity.Common),
        6: lambda: Weapon("Slingshot", 20, Delusion(Delusions.Stun), Rarity.Common),
        7: lambda: Weapon("Taser", 18, Delusion(Delusions.Zap), Rarity.Common),
        8: lambda: Weapon("Hungry Spirit", 13, Delusion(Delusions.Drain), Rarity.Common),
        9: lambda: Weapon("Jade Dagger", 23, Delusion(Delusions.Bleed), Rarity.Common),
    },
    Rarity.Rare: {
        1: lambda: Weapon("Frozen Stars", 22, Delusion(Delusions.Freeze), Rarity.Rare),
        2: lambda: Weapon("Fiery Desire", 27, Delusion(Delusions.Burn), Rarity.Rare),
        3: lambda: Weapon("Thorn Lasso", 13, Delusion(Delusions.Plant), Rarity.Rare),
        4: lambda: Weapon("Shield Buster", 17, Delusion(Delusions.Mech), Rarity.Rare),
        5: lambda: Weapon("Symbiotic Arm", 14, Delusion(Delusions.Corrupt), Rarity.Rare),
        6: lambda: Weapon("Rock Pillar", 23, Delusion(Delusions.Stun), Rarity.Rare),
        7: lambda: Weapon("Lightning Rod", 21, Delusion(Delusions.Zap), Rarity.Rare),
        8: lambda: Weapon("Wicked Blade", 18, Delusion(Delusions.Drain), Rarity.Rare),
        9: lambda: Weapon("Amethyst Sword", 25, Delusion(Delusions.Bleed), Rarity.Rare),
    },
    Rarity.Epic: {
        1: lambda: Weapon("Avalanche", 24, Delusion(Delusions.Freeze), Rarity.Epic),
        2: lambda: Weapon("Lava Fist", 29, Delusion(Delusions.Burn), Rarity.Epic),
        3: lambda: Weapon("The Stringless", 16, Delusion(Delusions.Plant), Rarity.Epic),
        4: lambda: Weapon("Fortified Mace", 21, Delusion(Delusions.Mech), Rarity.Epic),
        5: lambda: Weapon("Elusive Eye", 18, Delusion(Delusions.Corrupt), Rarity.Epic),
        6: lambda: Weapon("Judge Club", 25, Delusion(Delusions.Stun), Rarity.Epic),
        7: lambda: Weapon("Electric Glove", 23, Delusion(Delusions.Zap), Rarity.Epic),
        8: lambda: Weapon("Dark Axe", 22, Delusion(Delusions.Drain), Rarity.Epic),
        9: lambda: Weapon("Cruel Claws", 27, Delusion(Delusions.Bleed), Rarity.Epic),
    },
    Rarity.Mythic: {
        1: lambda: Weapon("The Frostbite", 29, Delusion(Delusions.Freeze), Rarity.Mythic),
        2: lambda: Weapon("Hellbringer", 37, Delusion(Delusions.Burn), Rarity.Mythic),
        3: lambda: Weapon("Lustre", 22, Delusion(Delusions.Plant), Rarity.Mythic),
        4: lambda: Weapon("Falcon Turret", 27, Delusion(Delusions.Mech), Rarity.Mythic),
        5: lambda: Weapon("Scimitar", 23, Delusion(Delusions.Corrupt), Rarity.Mythic),
        6: lambda: Weapon("Ancient Club", 30, Delusion(Delusions.Stun), Rarity.Mythic),
        7: lambda: Weapon("Thunder Staff", 27, Delusion(Delusions.Zap), Rarity.Mythic),
        8: lambda: Weapon("Soul Orb", 26, Delusion(Delusions.Drain), Rarity.Mythic),
        9: lambda: Weapon("Divine Wrath", 34, Delusion(Delusions.Bleed), Rarity.Mythic),
    },
}

Heals: dict[int, Callable[..., Healable]] = {
    1: lambda: Healable("Bandage", 15, Rarity.Common),
    2: lambda: Healable("Health Pot", 25, Rarity.Rare),
    3: lambda: Healable("Med Kit", 75, Rarity.Epic),
    4: lambda: Healable("Blessing", 100, Rarity.Mythic),
}
