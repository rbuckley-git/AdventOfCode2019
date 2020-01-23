# https://adventofcode.com/
# 20/12/2019
# Day 20
#

import sys

start_position = None
end_position = None
grid = {}
portals = {}
answers = []
inner_portals = {}
outer_portals = {}

def reset():
    global grid
    global portals
    global answers
    global inner_portals
    global outer_portals

    grid = {}
    portals = {}
    answers = []
    inner_portals = {}
    outer_portals = {}

def parse_input(filename, part):
    global start_position
    global end_position
    global grid
    global portals
    global inner_portals
    global outer_portals

    width = 0
    height = 0

    letters = {}
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    gateways = {}
    with open( filename ) as fp:
        y = 0
        for line in fp.readlines():
            if len(line) > width:
                width = len(line)

            x = 0
            for ch in line:
                if ch == '.':
                    grid[(x,y)] = "."
                elif ch in alphabet:
                    letters[(x,y)] = ch
                x+=1
            y+=1
    height = y

    for (x,y) in letters:
        # part 2 requires knowledge of what gateways are in the inside and which are on the outside
        in_out = "IN"
        if y == 1 or y == height-1 or x == 0 or x == width-3:
            in_out = 'OUT'
        if (x,y-1) in letters and (x,y+1) in grid:                  # label above path
            gateways[(x,y+1)] = (in_out,letters[(x,y-1)] + letters[(x,y)])
        elif (x,y-1) in letters and (x,y-2) in grid:                # label below path
            gateways[(x,y-2)] = (in_out,letters[(x,y-1)] + letters[(x,y)])
        elif (x+1,y) in letters and (x+2,y) in grid:                # label to the left of path
            gateways[(x+2,y)] = (in_out,letters[(x,y)] + letters[(x+1,y)])
        elif (x+1,y) in letters and (x-1,y) in grid:                # label to the right of path
            gateways[(x-1,y)] = (in_out,letters[(x,y)] + letters[(x+1,y)])

    # find start and end positions
    for xy,v in gateways.items():
        if v[1] == "AA":
            start_position = xy
        elif v[1] == "ZZ":
            end_position = xy

    if part == 1:
        for xy1,v1 in gateways.items():
            if v1[1] in ["AA","ZZ"]:
                continue

            for xy2,v2 in gateways.items():
                if v1[1] == v2[1]:
                    if xy1 != xy2:
                        portals[xy1] = xy2
    else:
        for xy1,v1 in gateways.items():
            if v1[1] in ["AA","ZZ"]:
                continue

            for xy2,v2 in gateways.items():
                if v1[1] == v2[1]:
                    if xy1 != xy2:
                        if v1[0] == "OUT":
                            outer_portals[xy1] = (xy2,v1[1])
                        else:
                            inner_portals[xy1] = (xy2,v1[1])

        assert len(inner_portals) == len(outer_portals)

    # return

def get_position(pos,dir):
    if dir == "N":
        return (pos[0],pos[1]-1)
    if dir == "S":
        return (pos[0],pos[1]+1)
    if dir == "W":
        return (pos[0]-1,pos[1])
    if dir == "E":
        return (pos[0]+1,pos[1])

    raise Exception("Invalid direction")

def follow_path_part1(position,path = [],step = 1):
    global answers

    for xy,v in portals.items():
        #print("portal",xy,v)
        if position == xy:
            position = v
            ##print("warping to ",position)
            step+=1
            break

    path.append(position)
    directions = []
    for d in ["N","S","E","W"]:
        next_pos = get_position(position,d)
        if next_pos in grid and next_pos not in path:
            directions.append(d)
    
    #print(position,"dirs",directions)
    while directions:
        direction = directions.pop(0)
        new_pos = get_position(position,direction)
        follow_path_part1(new_pos,path,step+1)
        if new_pos == end_position:
            print("got to end",step)
            answers.append(step)

    path.pop(-1)

def follow_path_part2(position,used_portals = [],path = [],step = 1,level = 0):
    global answers
    warp = False

    if answers and step > max(answers):
        return

    if level > 50:
        print("aborting on level",level)
        return

    #print("used portals",used_portals)
    for xy,v in outer_portals.items():
        key = "-".join([v[1],str(level)])
        if position == xy and key not in used_portals:
            level-=1
            if level < 0:
                print("bad path",position,"through outer portal",v[1])
                return

            print("warping to ",position,"level",level,"through outer portal",v[1])
            position = v[0]
            #used_portals.append(key)
            step+=1
            path = []
            warp = True
            break

    if not warp:
        for xy,v in inner_portals.items():
            key = "-".join([v[1],str(level)])
            if position == xy and v[1] not in used_portals:
                level+=1
                print("warping to ",position,"level",level,"through inner portal",v[1])
                position = v[0]
                #used_portals.append(key)
                step+=1
                path = []
                break

    path.append(position)
    directions = []
    for d in ["N","S","E","W"]:
        next_pos = get_position(position,d)
        if next_pos in grid and next_pos not in path:
            directions.append(d)
    
    #print(position,"dirs",directions)
    while directions:
        direction = directions.pop(0)
        new_pos = get_position(position,direction)
        #print("push",new_pos,level)
        follow_path_part2(new_pos,used_portals,path,step+1,level)

        if new_pos == end_position and level == 0:
            print("got to end",step)
            answers.append(step)

    if path:
        path.pop(-1)    
    #print("pop",position,level,path)

if __name__ == '__main__':
    sys.setrecursionlimit(2000)

    parse_input("20.input.txt",1)
    follow_path_part1(start_position)
    print("Part 1: steps",min(answers))

    reset()
    parse_input("20.input.txt",2)
    print("start",start_position,"end",end_position)

    follow_path_part2(start_position)
    if answers:
        print("Part 1: steps",min(answers))
