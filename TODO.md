# TODO

## Always

- :warning: **Add unit tests to new library code**

## Priority

- [ ] :art: Create 256x256 game map & map metadata

- [x] :sparkles: Add map parser and renderer; keep in mind these icons require a Nerd Fonts compatible font to render

- [x] :wrench: Fix player not being able to move to the side of the map by adding padding to the matrix of tiles

- [x] :wrench: Fix `PadContext` behavior so that the pad offset will never be large enough to cease pad display

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
