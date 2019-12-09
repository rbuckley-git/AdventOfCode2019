# https://adventofcode.com/
# 7/12/2019
# Day 7
#
# Good test of map knowledge etc
#
import unittest


# this is a function that can recurse through the map to return 1 for each level
# indent was used to assist debugging
def count_orbits_from_orbit_map( o, p, indent = "" ):
    i = 1
    for k in o.keys():
        if k == p:
            if o[k] != "COM":
                i += count_orbits_from_orbit_map(o,o[k],indent + " ")

    return i

def count_orbits( orbits ):
    o = {}
    for orbit in orbits:
        p1,p2 = orbit.split(")")
        o[p2] = p1

    count = 0
    # loop through the top level keys summing the counts from the recursive function
    for k in o.keys():
        count += count_orbits_from_orbit_map( o, k )

    return count

def find_orbit_path(o, p, indent = "" ):
    orbit = p + ","
    for k in o.keys():
        if k == p:
            if o[k] != "COM":
                orbit += find_orbit_path(o,o[k],indent + " ")

    return orbit


def count_transfers( orbits, origin, destination ):
    o = {}
    for orbit in orbits:
        p1,p2 = orbit.split(")")
        o[p2] = p1
    
    #print(o)

    t1 = find_orbit_path( o, o[origin] )
    t2 = find_orbit_path( o, o[destination] )

    # find longest, remove trailing , and split into array
    s1 = max(t1,t2)[:-1].split(",")
    s2 = min(t1,t2)[:-1].split(",")

    # remove common characters from the end
    for i in range(len(s1)):
        if ( s1[-1] != s2[-1] ):
            break
        s1.pop(-1)
        s2.pop(-1)

    # answer will be the sum of the two arrays
    return len(s1) + len(s2)

#
# test cases
#
class AdventTestCase(unittest.TestCase):
    def test_orbit(self):
        self.assertEqual( count_orbits(["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L"]),42)
        self.assertEqual( count_transfers(["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU","I)SAN"],"YOU","SAN"),4)
        self.assertEqual( count_transfers(["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","J)YOU","I)SAN"],"YOU","SAN"),3)



if __name__ == '__main__':

    fp = open( '6.input.txt' )
    total = 0
    data = []
    for line in fp:
        data.append(line[:-1])
    fp.close()

    total = count_orbits( data )
    print( "total orbits: ", total )
    transfers = count_transfers( data, "YOU", "SAN" )
    print( "total transfers: ", transfers )



