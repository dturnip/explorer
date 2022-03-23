# from curses import window, A_BOLD
# from getpass import getuser
# from enum import Enum, auto
# from collections import deque
# from typing import Optional
# from .lib.singleton import singleton
# from .globals import Colors, Globals as G
# from .ctx import Delusion, Delusions, Healable, Rarity, Weapon, player, state, inventory
#
#
# class SideState(Enum):
#     default = auto()
#     inventory = auto()
#     console = auto()
#
#
# @singleton
# class Side:
#     def __init__(self, pad: window) -> None:
#         self.pad = pad
#         self.pad.bkgd(" ", Colors.WALL)
#
#         self.text: str = ""
#         self.state: SideState = SideState.default
#
#         self.log_buffer: deque[str] = deque()
#
#         # The height of the unboredered side pad, minus 2 ()
#         self.max_log_length = G.game_height - 2 - 2
#
#     def draw_stats(self) -> None:
#         draw = self.pad.addstr
#         user = getuser()
#         name = user if len(user) <= G.padding_width - 4 else user[: G.padding_width - 7] + "..."
#
#         self.pad.clear()
#
#         draw(f"{name}\n\n", A_BOLD)
#
#         draw("LEVEL: ", A_BOLD)
#         draw(f"{state.level.level} ({state.level.xp} / {state.level.max_xp} XP)\n")
#
#         draw("HP: ", A_BOLD)
#         draw(f"{state.hp.hp}", self.get_health_color())
#         draw(" / ")
#         draw(f"{state.hp.max_hp}\n", Colors.HP_HIGH)
#
#         draw("MONEY: ", A_BOLD)
#         draw(f"{inventory.money}\n")
#
#         draw(f"\n\nDEBUG(y, x): ", A_BOLD)
#         draw(f"({player.y}, {player.x})")
#
#     def draw_weapon(self, weapon: Weapon | None) -> None:
#
#         # TODO: Show a symbol indicating the currently equipped weapon
#
#         draw = self.pad.addstr
#
#         draw("- ")
#
#         if weapon is None:
#             draw("\n")
#             return
#
#         draw(f"{weapon.name} ", weapon.get_rarity_color())
#         draw("[")
#         draw(f"{weapon.delusion.get_symbol()} ", weapon.delusion.get_color())
#         draw(f"{weapon.atk}]\n")
#
#     def draw_heal(self, heal: Healable | None) -> None:
#         draw = self.pad.addstr
#
#         draw("- ")
#
#         if heal is None:
#             draw("\n")
#             return
#
#         draw(f"{heal.name} ", heal.get_rarity_color())
#         draw(f"[+{heal.amount}%]\n")
#
#     def draw_inventory(self) -> None:
#         draw = self.pad.addstr
#
#         self.pad.clear()
#
#         draw("~~~INVENTORY~~~\n\n")
#
#         draw("WEAPONS:\n", A_BOLD)
#
#         for weapon in inventory.weapons:
#             self.draw_weapon(weapon)
#
#         draw("\n")
#         draw("HEALS:\n", A_BOLD)
#
#         for heal in inventory.heals:
#             self.draw_heal(heal)
#
#     def draw_console(self) -> None:
#         draw = self.pad.addstr
#
#         self.pad.clear()
#
#         draw("~~~CONSOLE~~~\n\n")
#
#         for t in self.log_buffer:
#             draw(f"{t}\n")
#
#     def log(self, t: str) -> None:
#         if len(self.log_buffer) > self.max_log_length:
#             raise Exception("Log buffer length is over the max space")
#
#         if len(self.log_buffer) == self.max_log_length:
#             self.log_buffer.popleft()
#
#         self.log_buffer.append(t)
#
#     def toggle_inventory(self) -> None:
#         self.state = SideState.inventory if self.state != SideState.inventory else SideState.default
#
#     def toggle_console(self) -> None:
#         self.state = SideState.console if self.state != SideState.console else SideState.default
#
#     def render(self) -> None:
#         match self.state:
#             case SideState.default:
#                 self.draw_stats()
#             case SideState.inventory:
#                 self.draw_inventory()
#             case SideState.console:
#                 self.draw_console()
#
#         self.pad.refresh(
#             0,
#             0,
#             G.padding_height + 1,
#             2,
#             G.padding_height + G.game_height - 2,
#             G.padding_width - 3,
#         )
#
#     def get_health_color(_self) -> int:
#         c = state.hp.hp
#         m = state.hp.max_hp
#
#         low = m // 3
#         mid = low * 2
#
#         match (c <= low, c >= mid + 1):
#             case (True, False):
#                 return Colors.HP_LOW
#             case (False, False):
#                 return Colors.HP_MID
#             case (False, True):
#                 return Colors.HP_HIGH
#
#         # Never going to happen, but mypy just wants it because of explicit return types
#         return 0
