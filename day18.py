# https://adventofcode.com/
# 23/12/2019
# Day 18
#

import sys
import unittest
import itertools

sys.setrecursionlimit(2000)

start_position = None
key_symbols = "abcdefghijklmnopqrstuvwxyz"
door_symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
surrounding_cells = [(0, 1),  (1, 0), (0, -1),  (-1, 0)]
keys_to_collect = 0
answers = set()
loops = 0
keys = []

def parse_input(filename):
    global start_position
    global keys_to_collect
    global answers
    global loops
    global keys

    keys_to_collect = 0
    loops = 0
    grid = {}
    answers = set()
    keys = []
    
    with open( filename ) as fp:
        y = 0
        for line in fp.readlines():
            x = 0
            line = line.strip()
            for ch in line:
                if ch == '@':
                    start_position = (x,y)
                    grid[(x,y)] = "@"
                else:
                    grid[(x,y)] = ch
                
                if ch in key_symbols:
                    keys_to_collect+=1
                    keys.append(ch)

                x+=1
            y+=1

    return grid

def render_grid(lgrid):
    maxx = max(x for x,y in lgrid)
    maxy = max(y for x,y in lgrid)

    print()
    for y in range(0,maxy+1):
        chars = []
        for x in range(0,maxx+1):
            if (x,y) in lgrid:
                chars.append( lgrid[(x,y)] )
            else:
                chars.append( "#" )
        
        print("".join(chars))

def move(position,direction):
    return tuple( map( sum, zip( position,direction)))

def follow(lgrid, position, keys_to_collect, keys = set(), start_direction = 0, path = [],loop = 0):
    global answers
    global loops

    if loops > 10000000:
        return

    loops+=1

    # don't process if the job is done
    if keys_to_collect == 0:
        return

    # ensure we can restore state from the recursion
    lgrid = lgrid.copy()
    keys = keys.copy()

    path.append(position)
    
    # collect a key
    if lgrid[position] in key_symbols:
        keys_to_collect-=1
        if loops%5000 == 0:
            print("found key",lgrid[position],"at",position,keys_to_collect,"remaining, ",loop,"steps",loops)
        if keys_to_collect == 0:
            answers.add(loop)

        keys.add(lgrid[position].upper())
        lgrid[position] = "."
        path = []

    # open a door if we have the key
    if lgrid[position] in door_symbols:
        door = lgrid[position]
        #print("found door",door)
        if door in keys:
            #print("   unlocking")
            keys.remove(door)
            lgrid[position] = "."
            #render_grid(lgrid)
        else:
            path = []
            return

    decisions = []
    for d in surrounding_cells:
        next_pos = move(position,d)
        if lgrid[next_pos] != "#" and next_pos not in path:
            decisions.append(d)
    
    for d in decisions:
        next_pos = move(position,d)
        follow(lgrid,next_pos,keys_to_collect,keys,start_direction,path,loop+1)

    if path:
        path.pop(-1)

def find_position_of_key(grid,key):
    for p in grid:
        if grid[p] == key:
            grid[p] = "."
            return p

def unlock_door(grid,key):
    door = key.upper()

    for p in grid:
        if grid[p] == door:
            grid[p] = "."

def find_key(grid,position,key,path,step = 0):
    path.append(position)
    #print(position,grid[position])
    if grid[position] == key:
        unlock_door(grid,key)
        return step

    if grid[position] != '#' and grid[position] not in door_symbols:
        step+=1

        for d in surrounding_cells:
            next_pos = move(position,d)
            if grid[next_pos] != "#" and next_pos not in path:
                s = find_key(grid,next_pos,key,path,step)
                if s != None:
                    return s

    path.pop(-1)
    return None

def compare_lists(list1,list2):
    if len(list1) != len(list2):
        return False
    for n in range(len(list1)):
        if list1[n] != list2[n]:
            return False

    return True


def find_steps(grid,position,strategy):
    total_steps = 0
    found_keys = 0

    for key in strategy:
        path = []
        s = find_key(grid,position,key,path)
        if s == None:
            return None

        total_steps+=s
        found_keys+=1
        position = find_position_of_key(grid,key)

    if found_keys == len(strategy):
        return total_steps

    return None

def best_steps(filename):
    grid = parse_input(filename)
    render_grid(grid)
    answers = set()
    n = 0
    for strategy in itertools.permutations(keys):
        s = find_steps(grid.copy(),start_position,strategy)
        n+=1
        if n % 1000 == 0:
            print(strategy)

        if s == None:
            continue

        print(strategy,s,"steps")
        answers.add(s)
        
    return min(answers)

class AdventTestCase(unittest.TestCase):
    """
    def test_case1(self):
        self.assertEqual(best_steps("18.test.1.input.txt"),86)

    def test_case2(self):
        self.assertEqual(best_steps("18.test.2.input.txt"),132)
    """
    def test_case3(self):
        self.assertEqual(best_steps("18.test.3.input.txt"),136)

if __name__ == '__main__':
    print(best_steps("18.input.txt"))
    