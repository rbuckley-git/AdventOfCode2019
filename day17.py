# https://adventofcode.com/
# 18/12/2019
# Day 17
#

import intcode
import sys

grid = {}
intersects = {}
surrounding_cells = [(0, 0),(0, -1),  (-1, 0), (0, 1),  (1, 0)]
directions =                [ord('^'),ord('<'),ord('v'),ord('>')]

def render_grid():
    maxx = max(x for x,y in grid)
    maxy = max(y for x,y in grid)

    print()
    for y in range(0,maxy+1):
        chars = []
        for x in range(0,maxx+1):
            chars.append( chr(grid[(x,y)] ))
        
        print("".join(chars))

def find_intersects():
    intersects = []

    maxx = max(x for x,y in grid)
    maxy = max(y for x,y in grid)

    # can't have an intersect on an edge
    for y in range(1,maxy):
        for x in range(1,maxx):
            if (x,y) in grid:
                intersect = True
                for d in surrounding_cells:
                    test = tuple(map(sum,zip((x,y),d)))
                    if grid[test] != ord('#'):
                        intersect = False
                        break
                if intersect:
                    grid[(x,y)] = ord('X')
                    intersects.append((x,y))

    return intersects

def find_start():
    for k in grid:
        if grid[k] in directions:
            return k,chr(grid[k])

def find_turn(relative_position,current_orientation):
    #print("or",relative_position,current_orientation)

    options = {
        ((-1, 0),'<'): (None,'<'),
        (( 0,-1),'^'): (None,'^'),
        (( 0, 1),'v'): (None,'v'),
        (( 1, 0),'>'): (None,'>'),
        ((-1, 0),'^'): ('L','<'),     # to the left but currently pointing up so turn left
        ((-1, 0),'v'): ('R','<'),
        (( 1, 0),'^'): ('R','>'),
        (( 1, 0),'v'): ('L','>')
    }
    print("lookup",relative_position,current_orientation)
    return options[(relative_position,current_orientation)]

def find_next_move(pos,direction):
    # skip self
    i = directions.index(ord(direction))+1
    print("find next move",direction)
    while True:
        d = surrounding_cells[i]
        test = tuple( map( sum, zip( pos,d)))
        print("test for next move",i,d,test)
        if grid[test] == ord('#'):
            turn = find_turn(d,direction)
            return turn
        i+=1
        i = i % len(surrounding_cells)

def move(position,direction):
    i = directions.index(ord(direction))
    print("move",i,direction)
    print('   tuple',surrounding_cells[i+1])
    return tuple( map( sum, zip( position,surrounding_cells[i])))
    

def find_segment():
    position,direction = find_start()
    print("start",position,direction)
    n = 0
    for x in range(10):
        print(x,"position",direction,position)
        turn,dir = find_next_move(position,direction)
        if turn != None:
            print("   turning",turn)
            direction = dir
        else:
            position = move(position,direction)
            n+=1
        


# Part 1
prog = intcode.get_program("17.input.txt")
ic = intcode.computer(prog)
line = []
x = 0
y = 0
while not ic.is_stopped():
    output = ic.run()
    if output == None:
        continue

    if output == 10:            # new line
        x = 0
        y+=1
    else:
        grid[(x,y)] = output
        x+=1

intersects = find_intersects()
render_grid()

sum_of_alignment_params = 0
for (x,y) in intersects:
    sum_of_alignment_params += x*y

print("Part 1: Sum of alignment params",sum_of_alignment_params)

# Part 2

prog[0] = 2 # wake up
ic = intcode.computer(prog)

find_segment()