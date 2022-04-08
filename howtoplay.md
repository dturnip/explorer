# How to play

### :warning: Ensure you have followed instructions in `README.md` :warning:

## Keep in mind

- This is an unfinished game so there's a lot of features that are not implemented:
  - There is no game saving/loading
  - There is no shop feature yet, despite the visible tile
  - The key north west of spawn can't be picked up, and the gates in the southeast corner of the map can't be unlocked
  - The healing forest (dark green area) does not heal you
  - The gamble water (blue area) cannot be interacted with
  - So if you manage to defeat all enemies that exist on the current map and collect all loot, you beat the game

## Recommendations

- GPU Accelerated terminal emulator such as Alacritty. Trust me, it boosts performance by a lot!
- Large font size (but not too large)
- Playing in full screen

Sample Alacritty config in `~/.config/alacritty/alacritty.yml`:

```yaml
font:
  normal:
    family: JetbrainsMono Nerd Font
  size: 24.0
```

## Game State

There are two main states:

1. **_Normal state_**, ie when you an move, view the inventory etc
2. **_Prompt state_**, ie when you type commands

## Rarity

| Rarity | Colour |
| ------ | ------ |
| Common | Grey   |
| Rare   | Blue   |
| Epic   | Purple |
| Mythic | Orange |

## Interactive Tiles

- **_Brown Chest_**: Yields a common/rare/epic weapon and a random healable, with the exception of 2 free starter chests near spawn
- **_Green Heal_**: Yields a random healable
- **_Yellow Money_**: Yields $5, although it's useless at the moment because the **_cyan shops_** are not implemented
- **_Red Enemy_**: Stand in the center of the 3 to engage in a fight
- **_Orange Mythic_**: Yields a random mythic weapon

## Key Controls

When in **_normal state_**:
`w`: move up
`a`: move left
`s`: move down
`d`: move right

`e`/`E`: interact (player image will hint)
`i`/`I`: toggle inventory
`c`/`C`: toggle console log
`p`/`P`: toggle command prompt

`Q`: quit game

## Command Prompt

- Arrow keys don't work, but delete does
- This is designed for in game needs, so valid shell script will be invalid command

## Valid Commands

- There is a dev command `kill` which insta-kills the enemy

| Command       | Description                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------------------- |
| `equip <n>`   | Equips the weapon in the `n` weapon slot, toggle inventory to find `n`. Cannot use during a fight.               |
| `heal <n>`    | Consumes the healable in the `n` heals slot, toggle inventory to find `n`                                        |
| `replace <n>` | Replaces the newly found weapon with the weapon in weapon slot `n`. Can only be used when specifically prompted. |
| `discard`     | Discards the newly found weapon. Can only be used when specifically prompted.                                    |
| `attack`      | Performs an attack. Can only be used in the begin phase of a turn.                                               |
| `pass`        | Switches the turn to the opponent's begin phase.                                                                 |
| `abandon`     | Abandons a fight and restores the enemy to full health and full weapon ATK                                       |
| `showheals`   | Logs all heals in the inventory. Can only be used during a fight.                                                |

## Delusions

- Elements system just to make things more interesting
- Strong delusions perform 1.5x damage
- Strong diagram: `Freeze` -> `Burn` -> `Plant` -> `Mech` -> `Corrupt` -> `Stun` -> `Zap` -> `Freeze`
- `Drain` and `Bleed` are not strong or weak to anything
- Find in depth delusion info in `ctx.py` lines 80-168, including their effects

## Fights

- You can heal anytime on **_your turn_**
- The enemy will always attack in its begin phase
- If you pass in your begin phase, your end phase effect will not activate
- You always go first
- Three phases:
  - **_Begin_** – Can attack once
  - **_Counter_** – If the damage receiving entity is equipped with a delusion with a counter effect, it has a chance to activate
  - End – No attacking, `pass` to end the turn

## Features ~~Bugs that I were too lazy to fix~~

- If you are at max hp, switching delusions will keep you at max hp
- When typing commands in a fight, to avoid confusion, press `RETURN` until you see a prompt that says something similar to `[Phase Begin! Your Turn!]`. It doesn't make a difference to how the battle plays out, but it could make a difference in your strategy.c
