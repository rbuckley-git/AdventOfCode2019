# https://adventofcode.com/
# 10/12/2019
# Day 10
#
# That was hard. A bit of coding first thing, then at lunch and finished off at the end of the day.
# Learned about sorting of lists and some set manipulation. 
# High school trig came back to haunt.
# Some of the rounding on floats was just to make the debugging easier. There are probably easier ways of doing the trig logic but I brute forced it.
# Also used all the examples as good test data and made up more of myself.
#

import unittest
import math

# "." denotes no astorid. Load file and convert to array of coordinates
def load_map(filename):
    with open( filename ) as fp:
        map = []
        y = 0
        for line in fp.readlines():
            line = line.strip()
            for x in range(len(line)):
                if line[x] != ".":
                    map.append((x,y))
            y+=1
        return map

def build_observable(map, location):
    vectors = {}
    distances = {}
    unique_vectors = set()
    for a in map:
        if a == location:          # ignore self
            continue

        vector = (a[0]-location[0],a[1]-location[1])
        distance = abs(vector[0]) + abs(vector[1])
        b = max(abs(vector[0]),abs(vector[1]))
        vector = (round(vector[0]/b,4),round(vector[1]/b,4))  # calculate the normalised vector for this coordinate/location

        unique_vectors.add(vector)          # for use later, keep a track of unique vectors
        vectors[a] = vector                 # keep a track of what vectors are associated with what node
        distances[a] = distance             # whilst here, calculate and store distance from location against coordinate
    
    # observables is a set by vector with an array of distances
    observables = {}
    for uv in unique_vectors:
        for a,v in vectors.items():
            if uv == v:
                if v not in observables:
                    observables[v] = []
                observables[v].append([a,distances[a]])

    return observables

def build_vector_and_distance_map(map, location):
    vectors = {}
    distances = {}
    unique_vectors = set()
    for a in map:
        if a == location:          # ignore self
            continue

        vector = (a[0]-location[0],a[1]-location[1])
        distance = abs(vector[0]) + abs(vector[1])
        b = max(abs(vector[0]),abs(vector[1]))
        vector = (round(vector[0]/b,4),round(vector[1]/b,4))  # calculate the normalised vector for this coordinate/location

        unique_vectors.add(vector)          # for use later, keep a track of unique vectors
        vectors[a] = vector                 # keep a track of what vectors are associated with what node
        distances[a] = distance             # whilst here, calculate and store distance from location against coordinate
    
    return vectors,distances,unique_vectors

def count_observable(map,location):
    observables = build_observable(map,location)

    in_line_of_sight = len(observables)

    return in_line_of_sight

def best_location(map):
    best_location = (-1,-1)
    number_observable = 0
    for a in map:
        o = count_observable(map,a)
        if o > number_observable:
            number_observable = o
            best_location = a

    return best_location,number_observable

def get_rotation_for_vectors(vectors):
    rotational_positions = {}
    for v in vectors:
        x = v[0]
        y = v[1]
        angle = 999
        if x == 0 and y < 0:
            angle = 0
        elif x > 0 and y == 0:
            angle = 90
        elif x == 0 and y > 0:
            angle = 180
        elif x < 0 and y == 0:
            angle = 270

        if x != 0 and y != 0:
            if x > 0:           # Q1,Q2 - right quadrants
                angle = 90+math.degrees(math.atan(y/x))
            elif x < 0:         # Q3,Q4 - left half
                angle = 270+math.degrees(math.atan(y/x))

        rotational_positions[v] = round(angle,4)

    # sort our postions by rotation order so we can just loop round them in order
    return sorted(rotational_positions.items(), key = lambda kv:(kv[1], kv[0]))

def find_nth_vaporized(map,location,n,debug = False):
    vectors,distances,unique_vectors = build_vector_and_distance_map(map,location)
    rotational_positions = get_rotation_for_vectors(unique_vectors)

    if debug:
        print("rotational ",rotational_positions)

    vaporisation = 0
    while True:
        for i in rotational_positions:
            target_vector = i[0]
            if debug:
                print("vectors",vectors)
                print("key",i,"target vector",target_vector)

            target_positions = []
            for pos,vector in vectors.items():
                if vector == target_vector:
                    target_positions.append((pos,distances[pos]))
            target_positions = sorted(target_positions, key=lambda kv:kv[1])
            if debug:
                print("target_positions",target_positions)

            # do we have any target positions
            if len(target_positions) > 0:
                next_target,d = target_positions.pop(0)
                vectors.pop(next_target)
                if debug:
                    print("next target",next_target)
                vaporisation+=1
                if vaporisation == n:
                    return next_target

        # make sure we exit at some point
        if len(vectors) == 0:
            break

    return (0,0)

class AdventTestCase(unittest.TestCase):
    def test_count_observable(self):
        map = load_map("10.test.1.input.txt")
        self.assertEqual(count_observable(map,(3,4)),8)
        self.assertEqual(count_observable(map,(1,0)),7)
        self.assertEqual(count_observable(map,(4,0)),7)
        self.assertEqual(count_observable(map,(0,2)),6)
        self.assertEqual(count_observable(map,(1,2)),7)
        self.assertEqual(count_observable(map,(2,2)),7)
        self.assertEqual(count_observable(map,(3,2)),7)
        self.assertEqual(count_observable(map,(4,2)),5)
        self.assertEqual(count_observable(map,(4,3)),7)
        self.assertEqual(count_observable(map,(4,4)),7)

    def test_best_location_case1(self):
        map = load_map("10.test.1.input.txt")
        self.assertEqual(best_location(map),((3,4),8))

    def test_best_location_case2(self):
        map = load_map("10.test.2.input.txt")
        self.assertEqual(best_location(map),((5,8),33))

    def test_best_location_case3(self):
        map = load_map("10.test.3.input.txt")
        self.assertEqual(best_location(map),((1,2),35))

    def test_best_location_case4(self):
        map = load_map("10.test.4.input.txt")
        self.assertEqual(best_location(map),((6,3),41))

    def test_best_location_case5(self):
        map = load_map("10.test.5.input.txt")
        self.assertEqual(best_location(map),((11,13),210))

    def test_part2(self):
        map = [(0,0),(5,-5),(-2,2),(4,4),(5,5),(3,3)]
        self.assertEqual(find_nth_vaporized(map,(0,0),1),(5,-5))
        self.assertEqual(find_nth_vaporized(map,(0,0),2),(3,3))
        self.assertEqual(find_nth_vaporized(map,(0,0),3),(-2,2))
        self.assertEqual(find_nth_vaporized(map,(0,0),4),(4,4))
        self.assertEqual(find_nth_vaporized(map,(0,0),5),(5,5))

        map = [(0,0),(5,0)]
        self.assertEqual(find_nth_vaporized(map,(0,0),1),(5,0))

        map = [(0,0),(0,-5)]
        self.assertEqual(find_nth_vaporized(map,(0,0),1),(0,-5))

        map = load_map("10.test.5.input.txt")
        self.assertEqual(find_nth_vaporized(map,(11,13),1),(11,12))
        self.assertEqual(find_nth_vaporized(map,(11,13),2),(12,1))
        self.assertEqual(find_nth_vaporized(map,(11,13),3),(12,2))
        self.assertEqual(find_nth_vaporized(map,(11,13),10),(12,8))
        self.assertEqual(find_nth_vaporized(map,(11,13),20),(16,0))
        self.assertEqual(find_nth_vaporized(map,(11,13),50),(16,9))
        self.assertEqual(find_nth_vaporized(map,(11,13),100),(10,16))
        self.assertEqual(find_nth_vaporized(map,(11,13),199),(9,6))
        self.assertEqual(find_nth_vaporized(map,(11,13),200),(8,2))
        self.assertEqual(find_nth_vaporized(map,(11,13),201),(10,9))
        self.assertEqual(find_nth_vaporized(map,(11,13),299),(11,1))

if __name__ == '__main__':
    map = load_map("10.input.txt")
    location,best = best_location(map)
    print("part 1 number of observable astorids",best,"from location",location)

    xy = find_nth_vaporized(map,(11,11),200)
    print("part 2 200th astorid is",xy,"answer",xy[0]*100+xy[1])

