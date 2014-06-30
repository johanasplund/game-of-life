# Conway's Game of Life

A simple script written in python 3.4.1 simulating Conway's game of life using pygame.

## Usage

```
$ python cgol.py -h
usage: cgol.py [-h] [-s SPEED] [-S N] [-d]

A simulation of Conway's Game of Life written in pygame.

optional arguments:
  -h, --help  show this help message and exit
  -s SPEED    specify time between ticks in ms (default: 20)
  -S N        set the size of the window to 10*Nx10*N (default: 50)
  -d          enable draw mode
```

### Controls
- `space` to pause/unpause
- `right arrow` to step once
- `left click` on a cell to make it live/die

## TODO

- ~~Show a grid when in draw mode~~
- Enable the user to hold left click and hover over cells to toggle their states
