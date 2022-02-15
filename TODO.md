# TODO

## Always

- :warning: **Add unit tests to new library code**

## Priority

- [ ] :art: Create 256x256 game map

- [ ] :sparkles: Add map parser and renderer; keep in mind:
  
  | Tile  | RGB         | Color  |
  | ----- | ----------- | ------ |
  | wall  | 0, 0, 0     | black  |
  | chest | 255, 0, 255 | pink   |
  | gold  | 255, 255, 0 | yellow |
  | enemy | 255, 0, 0   | red    |

- [ ] :wrench: Fix `PadContext` behavior so that the pad offset will never be large enough to cease pad display

- [ ] :sparkles: Add `PlayerContext`

- [ ] :sparkles: Add collision logic with walls

- [ ] :lipstick: Change style of player (background color and char) when above an interactive tile

- [ ] :sparkles: Add inventory, money, health system to `GameContext`

- [ ] :sparkles: Create run CLI script to run the game

- [ ] :sparkles: Add game saving (from within the game) and game loading (from the CLI)

## After

- [ ] :art: Create ASCII enemies

- [ ] :sparkles: Add fighting scenes and logic

- [ ] :memo: Create tutorial markdown file

- [ ] :sparkles: Add Makefile

- [ ] :sparkles: Add Dockerfile

- [ ] :sparkles: Create unique encoder/decoder for save/load games
