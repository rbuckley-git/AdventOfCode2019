# https://adventofcode.com/
# 12/12/2019
# Day 12
#
# Well that was tough (for me). First part was easy enough and code worked nicely to
# calculate the energy levels.
# Second part required some intuition and thinking. Both difficult when trying to bash
# this stuff out quickly. After leaving the brute force approach running over lunch I gave
# up and sought external influences. I therefore attribute the part 2 solution to the 
# cleverness of others with bigger brains.
# Once I discovered the concept of periods in x,y,z dimensions and the lcm formula, it was
# a case of plugging it into my code. The result is not pretty and involved hardwiring it
# for the number of planets and dimensions. Got the result though eventually. Started
# learning about lambda and map and zip and other cool stuff that I need to explore more.
#

import unittest
import math

# globals
map = []
vel = []

# parse the input file to get a coordinate map
def load_map(filename):
    global map
    global vel
    map = []
    vel = []
    with open( filename ) as fp:
        for line in fp.readlines():
            pos = []
            for moon in line.strip()[1:-1].split(","):
                pos.append(moon.split("=")[1])
            map.append(list((int(pos[0]),int(pos[1]),int(pos[2]))))
            vel.append(list((0,0,0)))

def print_map():
    for i in range(len(map)):
        print("pos=<x={:3d},y={:3d},z={:3d}> vel=<x={:3d},y={:3d},z={:3d}>".
            format(map[i][0],map[i][1],map[i][2],vel[i][0],vel[i][1],vel[i][2]))

def get_state(map,velocity):
    states = []
    for i in range(len(map)):
        states.append("<{},{},{}|{},{},{}>".
            format(map[i][0],map[i][1],map[i][2],vel[i][0],vel[i][1],vel[i][2]))

    return "".join(states)

def apply_gravity():
    for i in range(len(map)):
        for j in range(len(map)):
            for k in range(3):
                gravity = 0
                if map[i][k] > map[j][k]:
                    gravity=-1
                elif map[i][k] < map[j][k]:
                    gravity=1
                vel[i][k]+=gravity

def apply_velocity():
    for i in range(len(map)):
        pos = []
        for k in range(3):
            pos.append( map[i][k]+vel[i][k] )
        map[i] = ( pos )

def calc_energy():
    energy = 0
    for i in range(len(map)):
        pe = 0
        ke = 0
        for k in range(3):
            pe+=abs(map[i][k])
            ke+=abs(vel[i][k])
        energy += (pe * ke)

    return energy

class AdventTestCase(unittest.TestCase):
    def test_gravity1(self):
        load_map("12.test.1.input.txt")

        apply_gravity()
        apply_velocity()
    
        self.assertEqual(map[0],list((2,-1,1)))
        self.assertEqual(map[1],list((3,-7,-4)))
        self.assertEqual(map[2],list((1,-7,5)))
        self.assertEqual(map[3],list((2,2,0)))
    
    def test_gravity2(self):
        load_map("12.test.1.input.txt")

        for i in range(2):
            apply_gravity()
            apply_velocity()

        self.assertEqual(map[0],list((5,-3,-1)))
        self.assertEqual(map[1],list((1,-2,2)))
        self.assertEqual(map[2],list((1,-4,-1)))
        self.assertEqual(map[3],list((1,-4,2)))
    
    def test_gravity10(self):
        load_map("12.test.1.input.txt")

        for i in range(10):
            apply_gravity()
            apply_velocity()

        self.assertEqual(map[0],list((2,1,-3)))
        self.assertEqual(map[1],list((1,-8,0)))
        self.assertEqual(map[2],list((3,-6,1)))
        self.assertEqual(map[3],list((2,0,4,)))
    
    def test_energy10(self):
        load_map("12.test.1.input.txt")

        for i in range(10):
            apply_gravity()
            apply_velocity()

        self.assertEqual(calc_energy(),179)

if __name__ == '__main__':
    load_map("12.input.txt")
    
    for i in range(1000):
        apply_gravity()
        apply_velocity()

    print("part 1 total energy",calc_energy())
    
    load_map("12.input.txt")

    periods = []

    # look at all the x's then y's then z's
    for k in range(3):
        n = 0

        # use a set to record that we have seen this location and velocity before
        seen = set()

        while True:
            apply_gravity()
            apply_velocity()

            # build a key of elements within the same dimension
            key = str(map[0][k]) + "," + str(map[1][k]) + "," + str(map[2][k]) + "," + str(map[3][k])
            key += str(vel[0][k]) + "," + str(vel[1][k]) + "," + str(vel[2][k]) + "," + str(vel[3][k])
            if key in seen:
                print("xyz"[k],"period",n)
                periods.append(n)
                break
            seen.add(key)
            
            n+=1
            
    # obtain lowest common multiple
    a = periods[0] * periods[1] // math.gcd(periods[0],periods[1])
    a = a * periods[2] // math.gcd(a,periods[2])

    print("part 2 steps",a)

    