# https://adventofcode.com/
# 14/12/2019
# Day 14
#

import intcode
from random import randint
import random

start = (19,5)
position = start
direction = 1
grid = {}
loops = 0
size_y = 0
size_x = 0
tank = None

# max values need to have 1 added to cope with the zero index
def get_dimensions():
    size_x = 0
    size_y = 0

    for cell in grid:
        if cell[0] > size_x:
            size_x = cell[0]
        if cell[1] > size_y:
            size_y = cell[1]
    size_x+=1
    size_y+=1

    return (size_x,size_y)

def render_grid():
    size_x,size_y = get_dimensions()
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

        if c == 1:     
            lines[y][x] = '#'
        elif c == 2:   
            lines[y][x] = ' '
        elif c == 3:   
            lines[y][x] = 'O'
    
    lines[position[1]][position[0]] = 'X'    
    lines[start[1]][start[0]] = 'S'    

    # print out the canvas
    for y in range(size_y):
        print("".join(lines[y]))
    
def get_position(current_pos,direction):

    if direction == 1:
        return (current_pos[0],current_pos[1]-1)
    elif direction == 2:
        return (current_pos[0],current_pos[1]+1)
    elif direction == 3:
        return (current_pos[0]-1,current_pos[1])
    elif direction == 4:
        return (current_pos[0]+1,current_pos[1])
    
    raise Exception("Invalid direction",direction)

def get_input_strategy1():
    global direction
    global loops

    loops+=1
    
    if loops % 10000 == 0:
        render_grid()
        print("position",position,["north","south","west","east"][direction-1],loops)

    # change direction randomly
    #
    direction = randint(1,4)
            
    return direction

def get_input_strategy2():
    global direction
    global loops

    loops+=1
    
    if loops % 10000 == 0:
        render_grid()
        print("position",position,["north","south","west","east"][direction-1],loops)

    # favour direction that would fill in a blank
    #
    for i in range(4):
        direction = i+1
        new_pos = get_position(position,direction)
        if new_pos not in grid:
            return direction

    direction = randint(1,4)
    
    for i in range(4):
        direction = i+1
        new_pos = get_position(position,direction)
        if new_pos in grid and grid[new_pos] == 2:
            return direction


    return randint(1,4)


def find_tank(prog,strategy):
    global position
    global grid
    ic = intcode.computer(prog)
    ic.set_input_handler(strategy)
    history = []
    while not ic.is_stopped():
        if loops > 100000:
            print("aborting after",loops,"loops")
            break

        resp = ic.run()
        if resp == None:
            continue

        new_pos = get_position(position,direction)

        if resp == 0:
            grid[new_pos] = 1
        elif resp == 1:
            grid[new_pos] = 2
            position = new_pos
            history.append(position)
        else:
            position = new_pos
            grid[new_pos] = 3
            render_grid()
            print("found tank at",position,"after",loops)
            return position


if __name__ == '__main__':
    prog = intcode.get_program("15.input.txt")
    random.seed(0)

    tank = find_tank(prog,get_input_strategy1)

    print("************")

    for i in range(2):
        position = start
        loops = 0
        tank = find_tank(prog,get_input_strategy2)
    
    print("Part 1")
