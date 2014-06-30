#!/usr/bin/python
import pygame
import copy
import random
from math import floor
import argparse

PAUSED = None
STEP_ONCE = None
DRAW_MODE = None


class Field(object):
    def __init__(self, field):
        super().__init__()
        self.field = field
        self.X = len(field[0])
        self.Y = len(field)

    def is_alive(self, x, y):
        return bool(self.field[y][x] == "#")

    def check_neighbors(self, x, y):
        numalive = 0
        for u in [(x-1) % self.X, x, (x+1) % self.X]:
            for v in [(y-1) % self.Y, y, (y+1) % self.Y]:
                if self.is_alive(u, v) and (u, v) != (x, y):
                    numalive += 1
        return numalive

    def update_field(self, new_field):
        self.field = new_field


def draw_field(Surface, surfsize, fieldclass, rectsize, rectcolor):
    # Draw the rectangles
    for y in range(surfsize):
        ycurs = y*rectsize
        for x in range(surfsize):
            xcurs = x*rectsize
            if fieldclass.field[y][x] == "#":
                pygame.draw.rect(Surface, rectcolor,
                                 [xcurs, ycurs, rectsize, rectsize])
                pygame.draw.rect(Surface, (100, 100, 100),
                                 [xcurs, ycurs, rectsize, rectsize], 1)


def draw_grid(Surface, surfsize, fieldclass, rectsize, rectcolor):
    for y in range(surfsize):
        ycurs = y*rectsize
        for x in range(surfsize):
            xcurs = x*rectsize
            if fieldclass.field[y][x] == "#":
                pygame.draw.rect(Surface, rectcolor,
                                 [xcurs, ycurs, rectsize, rectsize])
            pygame.draw.rect(Surface, (100, 100, 100),
                             [xcurs, ycurs, rectsize, rectsize], 1)


def event_handler(screen, BG_COLOR, RECT_COLOR, field_scale, the_field):
    global PAUSED
    global STEP_ONCE
    global DRAW_MODE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
            elif event.key == pygame.K_SPACE:
                PAUSED = not PAUSED
            elif event.key == pygame.K_RIGHT:
                STEP_ONCE = not STEP_ONCE
                PAUSED = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x = int(floor(x/10)*10)
            y = int(floor(y/10)*10)
            xind = int(x/field_scale)
            yind = int(y/field_scale)
            if the_field.field[yind][xind] == "#":
                pygame.draw.rect(screen, BG_COLOR,
                                 [x, y, field_scale, field_scale])
                the_field.field[yind][xind] = "."
                if DRAW_MODE:
                    pygame.draw.rect(screen, (100, 100, 100),
                                     [x, y, field_scale, field_scale], 1)
            else:
                pygame.draw.rect(screen, RECT_COLOR,
                                 [x, y, field_scale, field_scale])
                pygame.draw.rect(screen, (100, 100, 100),
                                 [x, y, field_scale, field_scale], 1)
                the_field.field[yind][xind] = "#"
            pygame.display.flip()
    return False


def main(size, speed):
    global PAUSED
    global STEP_ONCE
    global DRAW_MODE
    field_scale = 10
    screen = pygame.display.set_mode((field_scale * size, field_scale * size))
    pygame.display.set_caption("Conway's game of life")
    RECT_COLOR = (255, 255, 255)
    BG_COLOR = (0, 0, 0)
    screen.fill(BG_COLOR)
    if DRAW_MODE:
        PAUSED = True
        field = [["." for k in range(size)] for l in range(size)]
        the_field = Field(field)
        draw_grid(screen, size, the_field, field_scale, RECT_COLOR)
        DRAW_MODE = False
    else:
        PAUSED = False
        field = [[random.choice(["#"] + ["."]*5) for k in range(size)]
                 for l in range(size)]
        the_field = Field(field)
        draw_field(screen, size, the_field, field_scale, RECT_COLOR)
    pygame.display.flip()
    STEP_ONCE = False
    while True:
        quit = event_handler(screen, BG_COLOR, RECT_COLOR,
                             field_scale, the_field)
        if quit:
            return
        if PAUSED:
            pygame.display.set_caption("Conway's game of life *PAUSED*")
            continue
        else:
            pygame.display.set_caption("Conway's game of life")
        if STEP_ONCE:
            PAUSED = True
            STEP_ONCE = False
        cc_field = copy.deepcopy(the_field.field)
        for p in range(the_field.X):
            for q in range(the_field.Y):
                cnt = the_field.check_neighbors(p, q)
                if not the_field.is_alive(p, q) and cnt == 3:
                    cc_field[q][p] = "#"
                elif the_field.is_alive(p, q) and cnt not in [2, 3]:
                    cc_field[q][p] = "."
        the_field.update_field(cc_field)
        screen.fill(BG_COLOR)
        draw_field(screen, size, the_field, field_scale, RECT_COLOR)
        pygame.display.flip()
        pygame.time.wait(speed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simulation of Conway's "
                                                 "Game of Life written in "
                                                 "pygame.")
    parser.add_argument("-s", dest="SPEED",
                        help="specify time between ticks in ms (default: 20)",
                        action="store", type=int, default=20)
    parser.add_argument("-S", dest="N",
                        help="set the size of the window to "
                             "10*Nx10*N (default: 50)",
                        action="store", type=int, default=50)
    parser.add_argument("-d", dest="DRAW_MODE",
                        help="enable draw mode", action="store_true")
    args = parser.parse_args()
    DRAW_MODE = args.DRAW_MODE
    pygame.init()
    main(args.SIZE, args.SPEED)
    pygame.quit()
