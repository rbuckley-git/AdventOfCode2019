# https://adventofcode.com/
# 10/12/2019
# Day 10
#
# Code refactored for part 2 of the challenge.
#

import unittest

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
        #print(map)
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
        vector = (vector[0]/b,vector[1]/b)  # calculate the normalised vector for this coordinate/location

        unique_vectors.add(vector)          # for use later, keep a track of unique vectors
        vectors[a] = vector                 # keep a track of what vectors are associated with what node
        distances[a] = distance             # whilst here, calculate and store distance from location against coordinate
    
    observables = {}
    for uv in unique_vectors:
        for a,v in vectors.items():
            if uv == v:
                if v not in observables:
                    observables[v] = []
                observables[v].append(distances[a])

    return observables,vectors

def count_observable(map,location):
    observables,vectors = build_observable(map,location)
    vectors = vectors   # remove warning

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

def find_nth_vaporized(map,location):
    observables,vectors = build_observable(map,location)

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

if __name__ == '__main__':
    map = load_map("10.input.txt")
    location,best = best_location(map)
    print("part 1 number of observable astorids",best,"from location",location)
