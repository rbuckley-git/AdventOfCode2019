# https://adventofcode.com/
# 13/12/2019
# Day 13

import unittest
import intcode

# globals
grid = {}
ball = (0,0)
bat = (0,0)
block_count = 0
size_y = 0
size_x = 0

# max values need to have 1 added to cope with the zero index
def get_dimensions():
    global size_x
    global size_y

    for cell in grid:
        if cell[0] > size_x:
            size_x = cell[0]
        if cell[1] > size_y:
            size_y = cell[1]
    size_x+=1
    size_y+=1

def render_grid():
    global size_x
    global size_y

    if size_x == 0 and size_y == 0:
        get_dimensions()

    # initialise an empty canvas
    lines = []
    for y in range(size_y):
        line = []
        for x in range(size_x):
            line.append(".")
        lines.append( line )

    # paint the canvas with the information from the grid
    for cell in grid.items():
        x = cell[0][0]
        y = cell[0][1]
        c = cell[1]

        if c == 1:              # 1 is a wall tile. Walls are indestructible barriers.
            lines[y][x] = '1'
        elif c == 3:            # 3 is a horizontal paddle tile. The paddle is indestructible.
            lines[y][x] = '3'
        elif c == 2:            # 2 is a block tile. Blocks can be broken by the ball.
            lines[y][x] = '2'
        elif c == 4:            # 4 is a ball tile. The ball moves diagonally and bounces off objects.
            lines[y][x] = '4'

    # print out the canvas
    for y in range(size_y):
        print("".join(lines[y]))

def update_globals():
    global block_count
    global bat
    global ball

    blocks = 0
    for cell in grid.items():
        if cell[1] == 3:    # bat
            bat = cell[0]
        elif cell[1] == 4:  # ball
            ball = cell[0]
        elif cell[1] == 2:  # block
            blocks+=1
    block_count = blocks

def get_input():
    update_globals()
    #render_grid()
    #print("ball",ball,"bat",bat)

    # If the joystick is in the neutral position, provide 0.
    # If the joystick is tilted to the left, provide -1.
    # If the joystick is tilted to the right, provide 1.

    if ball[0] < bat[0]:
        move = -1
    elif ball[0] > bat[0]:
        move = 1
    else:
        move = 0
    #
    # use input() to step through this bit
    #
    return move

if __name__ == '__main__':
    prog = intcode.get_program("13.input.txt")
    ic = intcode.computer(prog)

    while not ic.is_stopped():
        x = ic.run()
        y = ic.run()
        c = ic.run()

        grid[(x,y)] = c

    # count blocks
    update_globals()
    print("Part 1 block count",block_count)

    grid = {}
    size_x = 0
    size_y = 0

    prog = intcode.get_program("13.input.txt")
    prog[0] = 2             # play for free
    ic = intcode.computer(prog)
    ic.set_input_handler(get_input)

    score = 0
    while not ic.is_stopped():
        x = ic.run()
        y = ic.run()
        c = ic.run()
        if x is None:
            continue

        if (x,y) == (-1,0):
            score = block_count
        else:
            grid[(x,y)] = c

    update_globals()
    render_grid()

    print("Part 2 score",score)
