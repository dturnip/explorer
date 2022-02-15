# TODO

## Always

- :warning: **Add unit tests to new library code**

## Priority

- [ ] :art: Create 256x256 game map & map metadata

- [ ] :sparkles: Add map parser and renderer; keep in mind these icons require a Nerd Fonts compatible font to render. Also, the `Color` column below is the raw image map, not what's rendered:

  | Tile  | RGB           | Color   | Icon | Hex  | Brief Description                                             |
  | ----- | ------------- | ------- | ---- | ---- | ------------------------------------------------------------- |
  | wall  | 25, 25, 25    | black   | N/A  | N/A  | Player can't travel through this tile                         |
  | path  | 150, 150, 150 | gray    | N/A  | N/A  | Player can travel through this tile                           |
  | enemy | 255, 0, 0     | red     |     | f5ac | Interactive tile prompting a fight scene, acts like a wall    |
  | chest | 255, 0, 255   | magenta |     | f8d2 | Interactive tile containing loot: weapons, money, items       |
  | money | 255, 255, 0   | yellow  |     | f155 | Interactive tile which adds money to the inventory            |
  | shop  | 0, 255, 255   | cyan    |     | f07a | Interactive tile to purchase assorted goods                   |
  | heal  | 0, 255, 0     | green   |     | f7df | Interactive tile which adds a healing item to the inventory   |
  | super | 255, 165, 0   | orange  |     | f005 | Interactive tile which adds a legendary item to the inventory |
  <!-- Getting flagged out, plan is to combine enemy with block into one entity -->
  <!--   | block | 0, 0, 255     | blue    |     | f5ac | Temporary wall, unblocked by defeating associated enemy       | -->
  <!--   | enemy | 255, 0, 0     | red     |     | f071 | Interactive tile to fight an enemy, drops loot on win         | -->

- [ ] :wrench: Fix `PadContext` behavior so that the pad offset will never be large enough to cease pad display

- [ ] :sparkles: Add `GameContext`

- [ ] :sparkles: Add `PlayerContext`

- [ ] :sparkles: Add collision logic with walls

- [ ] :lipstick: Change style of player (background color and char) when above an interactive tile

- [ ] :sparkles: Change state and behavior of player depending on what environment they are in

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
