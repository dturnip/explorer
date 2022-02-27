# explorer

**WORK IN PROGRESS**

Top down adventure game in the terminal

## Requisites

- Python 3.10+
- Terminal emulator is able to render 256 colors
- Terminal emulator is equipped with a font that can render Nerd Font glyphs. Recommended fonts are included in `fonts/`. Font sizes `16.0`-`24.0` are recommended, but ultimately it doesn't matter. Just be rational.

## macOS / Linux

1. Install

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/dturnip/explorer/main/install.sh)" && cd explorer
```

2. Run

```shell
./run.sh
```

## Windows

:warning: **TBA** :warning:

## Kitty & Alacritty

- GPU accelerated terminals are great for this game as there will be less flickering and smoother performance. Both kitty and Alacritty will fail to render specific characters because `$TERM` is something other than `xterm-256color`. The below command fixes this problem (no need if you are using `./run.sh`):

```bash
export TERM=xterm-256color
```
