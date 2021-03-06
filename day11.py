# https://adventofcode.com/
# 11/12/2019
# Day 11
#
# Straightforward once you can rely on an incode computer that did not need modification. Generated some test cases to handle the logic.

import unittest
import intcode

# assuming down and right is positive x and y
def move_position(start,direction):
    x = start[0]
    y = start[1]
    if direction == "<":
        return (x-1,y)
    if direction == "^":
        return (x,y-1)
    if direction == ">":
        return (x+1,y)
    if direction == "v":
        return (x,y+1)

    raise Exception("Invalid direction")

def change_direction_left(current_direction):
    directions = "^<v>"
    return directions[(directions.find(current_direction)+1) % 4]

def change_direction_right(current_direction):
    directions = "^>v<"
    return directions[(directions.find(current_direction)+1) % 4]

def change_direction(current_direction,turn):
    if turn == 0:       # turn left
        return change_direction_left(current_direction)
    if turn == 1:       # turn right
        return change_direction_right(current_direction)

    raise Exception("invalid turn instruction",turn)    


def emergency_hull_painting_robot(start_colour = 0):
    # to record the postions that have been painted
    positions_painted = set()
    # to record the current colour of each squart
    grid = {}
    # starting direction
    direction = "^"
    pos = (0,0)

    # 0 = black
    # 1 = white

    grid[(0,0)] = start_colour

    ic = intcode.computer( intcode.get_program("11.input.txt") )
    
    while not ic.is_stopped():
        colour = 0                  # default colour for a panel
        if pos in grid:             # lookup colour for panel if we have previously painted it
            colour = grid[pos]  

        ic.add_input(colour)

        colour = ic.run()
        if colour == None:
            continue

        turn = ic.run()
        if turn == None:
            continue

        positions_painted.add(pos)
        grid[pos] = colour

        direction = change_direction(direction,turn)
        pos = move_position(pos,direction)

    return len(positions_painted),grid

# max values need to have 1 added to cope with the zero index
def get_dimensions(grid):
    maxx = 0
    maxy = 0
    for cell in grid.keys():
        if cell[0] > maxx:
            maxx = cell[0]
        if cell[1] > maxy:
            maxy = cell[1]
    return maxx+1,maxy+1

def render_grid(grid):
    size_x,size_y = get_dimensions(grid)

    # initialise an empty canvas
    lines = []
    for y in range(size_y):
        line = []
        for x in range(size_x):
            line.append(" ")
        lines.append( line )

    # paint the canvas with the information from the grid
    for cell in grid.items():
        x = cell[0][0]
        y = cell[0][1]
        c = cell[1]

        if c==1:
            lines[y][x] = '#'

    # print out the canvas
    for y in range(size_y):
        print(" ".join(lines[y]))

class AdventTestCase(unittest.TestCase):
    def test_direction(self):
        self.assertEqual(move_position((0,0),"<"),(-1,0))
        self.assertEqual(move_position((5,5),">"),(6,5))
        self.assertEqual(move_position((-1,-1),"^"),(-1,-2))
        self.assertEqual(move_position((0,0),"v"),(0,1))
        self.assertRaises(Exception,move_position,[(0,0),"x"])

    def test_change_direction_left(self):
        self.assertEqual(change_direction_left("^"),"<")
        self.assertEqual(change_direction_left("<"),"v")
        self.assertEqual(change_direction_left("v"),">")
        self.assertEqual(change_direction_left(">"),"^")

    def test_change_direction_right(self):
        self.assertEqual(change_direction_right("^"),">")
        self.assertEqual(change_direction_right("<"),"^")
        self.assertEqual(change_direction_right("v"),"<")
        self.assertEqual(change_direction_right(">"),"v")

if __name__ == '__main__':
    panels,grid = emergency_hull_painting_robot()
    print("Part 1 - number of panels painted",panels)
    panels,grid = emergency_hull_painting_robot(1)
    print("Part 2 - number of panels painted",panels)
    render_grid(grid)
