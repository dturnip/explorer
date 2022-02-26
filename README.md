# explorer

**THIS IS A BIG WORK IN PROGRESS**

A simple 2D top down command line game

## Requisites

- Python 3.10+
- Terminal emulator able to render 256 colors
- Terminal emulator equipped with a font that can render Nerd Font glyphs. Recommended fonts included in `fonts/`. Font size `16.0` is recommended, but ultimately it doesn't matter.

## Install & Run

### macOS / Linux

1. Clone, setup environment and install dependencies:

```bash
git clone https://github.com/dturnip/explorer.git && \
cd explorer && \
python3 -m venv venv && source ./venv/bin/activate && \
pip install -r requirements.txt
```

2. Run as a python module

```bash
python3 -m explorer
```

### Windows

:warning: **TBA** :warning:

## Kitty & Alacritty

- GPU accelerated terminals are great for this game as there will be less flickering and smoother performance. Both terminals will fail to render specific characters because `$TERM` is something other than `xterm-256color`. Before running the module, run:

```bash
export TERM=xterm-256color
```
