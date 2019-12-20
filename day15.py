# https://adventofcode.com/
# 14/12/2019
# Day 14
#
# Tried a random approach to finding the tank which worked but could not find the entirety of the maze.
# Cam gave me some motivation to proceed and use a recursive approach, the trick being to ensure the intcode computer
# could be reset to the point before branching. Once an algorithm had been selected that would explore the entire grid,
# it came together. Part 2 was easy for a change. Good challenge. Probably some way of combining the maze exporation phase
# with the code to find the best path.

import intcode
import copy

prog = intcode.get_program("15.input.txt")
start = (0,0)
grid = {start:4}
loops = 0
debugging = False
path = []
steps_to_find = 0
tank = None

def render_grid(position = None):
    if len(grid) == 0:
        return

    maxx = max(x for x,y in grid)
    minx = min(x for x,y in grid)
    maxy = max(y for x,y in grid)
    miny = min(y for x,y in grid)

    print()
    for y in range(miny,maxy+1):
        chars = []
        for x in range(minx,maxx+1):
            if (x,y) == position:
                chars.append('X')
            elif (x,y) in grid:
                c = grid[(x,y)]
                if c == 1:     
                    chars.append('#')
                elif c == 2:   
                    chars.append(' ')
                elif c == 3:   
                    chars.append('O')
                elif c == 4:   
                    chars.append('S')
                elif c == 5:   
                    chars.append('o')
            else:
                chars.append(".")
        print("".join(chars))

    
def get_position(pos,dir):
    return tuple(map(sum,
                zip(pos,[None,(0,-1),(0,1),(-1,0),(1,0)][dir])))


def find_oxygen_tank(ic,position = start):
    global grid
    global debugging
    global loops
    global tank

    # find all directions that have not been explored
    directions = []
    for d in [1,3,2,4]:
        if get_position(position,d) not in grid:
            directions.append(d)

    while directions:
        while directions and not ic.is_stopped():
            loops+=1

            direction = directions.pop(0)

            if loops % 1000 == 0:
                render_grid(position)

            backup = copy.deepcopy(ic)              # back up our computer state
            ic.add_input(direction)

            resp = ic.run()
            if resp == None:
                continue

            new_pos = get_position(position,direction)
            moved = False
            if resp == 0:                   # wall
                grid[new_pos] = 1
            elif resp == 1:                 # empty space
                grid[new_pos] = 2
                moved = True
            else:                           # tank
                grid[new_pos] = 3
                render_grid(new_pos)
                moved = True
                print("found tank at",new_pos)

                tank = new_pos

            if moved:
                find_oxygen_tank(ic,new_pos)
                ic = copy.deepcopy(backup)              # restore state

    return

def find_path_to_oxygen_tank(ic,position = start):
    global grid
    global debugging
    global loops
    global path
    global steps_to_find

    # find all directions that have not been explored
    directions = []
    for d in [1,3,2,4]:
        if grid[get_position(position,d)] in [2,3]:
            directions.append(d)

    # for each direction, recurse into that position
    while directions and steps_to_find == 0:
        while directions and not ic.is_stopped():
            loops+=1

            direction = directions.pop(0)

            backup = copy.deepcopy(ic)              # back up our computer state
            ic.add_input(direction)

            resp = ic.run()
            if resp == None:
                continue

            new_pos = get_position(position,direction)
            moved = False
            if resp == 0:                   # wall
                grid[new_pos] = 1
            elif resp == 1:                 # empty space
                grid[new_pos] = 5
                moved = True
            else:                           # tank
                grid[new_pos] = 3
                render_grid(new_pos)
                moved = True
                path.append(position)
                print("found tank at",new_pos,"after",len(path),"steps")
                
                steps_to_find = len(path)
                ic.halt()
                break

            if moved:
                path.append(position)
                find_path_to_oxygen_tank(ic,new_pos)
                ic = copy.deepcopy(backup)              # restore state
                path.pop(-1)

    return

def find_time_to_flood_chamber(positions):
    global grid
    global debugging
    global loops

    stack = []
    while positions:
        p = positions.pop()

        # find all directions that contain space
        for d in [1,3,2,4]:
            if grid[get_position(p,d)] == 2:
                new_pos = get_position(p,d)
                grid[new_pos] = 5
                stack.append(new_pos)

    if stack:
        loops+=1
        find_time_to_flood_chamber(stack)
        
    return

if __name__ == '__main__':
    ic = intcode.computer(prog)

    find_oxygen_tank(ic)
    render_grid(None)
    
    ic = intcode.computer(prog)
    find_path_to_oxygen_tank(ic)
    print("Part 1:",steps_to_find,"steps to oxygen tank")

    # reset grid
    grid[start] = 2
    for p,v in grid.items():
        if v == 5:
            grid[p] = 2

    render_grid(None)
    loops = 0
    find_time_to_flood_chamber([tank])
    print("Part 2:",loops,"steps to flood with oxygen")
