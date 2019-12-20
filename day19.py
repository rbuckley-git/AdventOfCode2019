# https://adventofcode.com/
# 19/12/2019
# Day 19
#
# This had me puzzled for ages. Turned out to be an out by one error. 100 cells are contained in 99 coordinate changes. Algorithm was sound.
#

import intcode

prog = intcode.get_program("19.input.txt")
grid = {}

def render_grid():
    maxx = max(x for x,y in grid)
    maxy = max(y for x,y in grid)

    xstart = 0
    ystart = 0

    print()
    for y in range(ystart,maxy+1):
        chars = []
        for x in range(xstart,maxx+1):
            if (x,y) in grid:
                if grid[(x,y)] == 1:
                    chars.append( '#' )
                else:
                    chars.append('X')
            else:
                chars.append( '.' )
        
        print("".join(chars))

def is_being_pulled(x,y):
    ic = intcode.computer(prog)

    pulled = 0
    ic.add_input(x)
    ic.add_input(y)
    while not ic.is_stopped():
        output = ic.run()
        if output == None:
            continue

        if output == 1:
            pulled+=1

    return pulled

def is_square_pulled(top_right_corner,square_size):
    tr = top_right_corner
    tl = (tr[0]-square_size+1,tr[1])
    br = (tr[0],tr[1]+square_size-1)
    bl = (tr[0]-square_size+1,tr[1]+square_size-1)

    if not is_being_pulled(tl[0],tl[1]):
        return None
    if not is_being_pulled(br[0],br[1]):
        return None
    if not is_being_pulled(bl[0],bl[1]):
        return None

    grid[tr] = 2
    grid[tl] = 2
    grid[bl] = 2
    grid[br] = 2

    return tl

def calc_affected_points(grid_size):
    global grid
    pulled = 0
    for x in range(grid_size):
        for y in range(grid_size):
            if is_being_pulled(x,y):
                pulled += 1
                grid[(x,y)] = 1

    return pulled

def calc_santa_position(square_size):
    global grid

    # assume solution is greater than 500,500
    y = 30
    x1 = 10

    while not is_being_pulled(x1,y):
        x1+=1

    x2 = x1

    while is_being_pulled(x1,y):
        grid[(x1,y)] = 1
        x1+=1

    # cell before was being pulled
    x1-=1
    found = (0,0)
    while found == (0,0):
        y+=1    # next row

        # move on while there is traction
        while is_being_pulled(x1,y):
            grid[(x1,y)] = 1
            x1+=1
        x1-=1

        while not is_being_pulled(x2,y):
            x2+=1
        grid[(x2,y)] = 1

        tl = is_square_pulled((x1,y),square_size)
        if tl != None:
            return tl

    return found


if __name__ == '__main__':

    print("Part 1, affected points",calc_affected_points(50))

    render_grid()

    (x,y) = calc_santa_position(100)

    print("Part 2, answer",x*10000+y)

