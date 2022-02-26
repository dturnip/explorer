# explorer

**THIS IS A BIG WORK IN PROGRESS**

A simple 2D top down command line game

## Requisites

- Python 3.10+
- macOS (Windows and Linux distros are not directly supported yet)
- Terminal emulator is one of: Terminal, iTerm2, kitty, Alacritty
- Terminal emulator equipped with `JetbrainsMono Nerd Font`, `Regular`, `16.0` (found in `fonts/`)

## Install & Run

### macOS

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

### Linux

:warning: **Currently not supported** :warning:

### Windows

:warning: **Currently not supported** :warning:

## Kitty & Alacritty

- GPU accelerated terminals are great for this game as there will be less flickering and smoother performance. Both terminals will fail to render specific characters because `$TERM` is something other than `xterm-256color`. Before running the module, run:

```bash
export TERM=xterm-256color
```
