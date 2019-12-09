# https://adventofcode.com/
# 6/12/2019
# Day 3
#
# This was quite a brain teaser. For ages, I was looking for a clever way of finding the intersect of two line segments.
# Eventually, solving the challange was more important to me than finding an elegant way so I brute forced it.
# Initial code took about 30 minutes to calculate. This is now instant using the set approach and I have not reversed
# this into part 2. Spent too long on this whole challage so far.
#
import unittest

def path_to_vector_array( instructions ):
    p = []
    xy = (0,0)
    p.append(xy)
    for path in instructions.split(","):
        x = 0
        y = 0
        dir = path[0]
        dist = int(path[1:])
        if ( dir == 'R' ):
            x = 1
        elif ( dir == 'L' ):
            x = -1
        elif ( dir == 'U' ):
            y = 1            
        elif ( dir == 'D' ):
            y = -1

        for i in range(0,dist):
            xy = ( xy[0] + x, xy[1] + y)
            p.append(xy)

    return p 

def calc_min_cross_distance( wire1, wire2 ):
    w1 = path_to_vector_array( wire1 )
    w2 = path_to_vector_array( wire2 )

    # this is new code base on comments by MJ and that there must be a better way
    intersects = list(set(w1) & set(w2))
    # not interested in origin as a result
    intersects.remove((0,0))

    # this was my brute force attempt at solving this, it gave the right answer but took ages
    """
    intersects = []
    for l1 in w1:
        for l2 in w2:
            if ( l2 == l1 and l2 != (0,0) ):
                intersects.append(l2)
    """
    distances = []
    for i in intersects:
        distances.append( abs(i[0]) + abs(i[1]) )

    return min(distances)

def calc_min_combined_steps( wire1, wire2 ):
    w1 = path_to_vector_array( wire1 )
    w2 = path_to_vector_array( wire2 )

    intersects = []
    i = len(w1) * len(w2)

    # not bothered refactoring this code, it takes ages to complete but got the right answer
    i1 = 0
    for l1 in w1:
        i2 = 0
        for l2 in w2:
            if ( l2 == l1 and l2 != (0,0) ):
                intersects.append(i1+i2)
            i-=1
            if ( i > 0 ) and ( i % 10000000 == 0):
                print(i) 
            i2+=1
        i1+=1

    return min( intersects )

#
# test cases
#
class AdventTestCase(unittest.TestCase):
    def test_min_cross_distance(self):
        self.assertEqual( calc_min_cross_distance("R10,U10","U10,R10"),20)
        self.assertEqual( calc_min_cross_distance("R10,U10,R10,U10","U10,R10,U10,R10"),20)
        self.assertEqual( calc_min_cross_distance("R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83"),159)
        self.assertEqual( calc_min_cross_distance("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),135)
    
    def test_min_combined_steps(self):
        self.assertEqual( calc_min_combined_steps("R8,U5,L5","U7,R6,D4"),30)
        self.assertEqual( calc_min_combined_steps("R8,U5,L5,D3","U7,R6,D4,L4"),30)
        self.assertEqual( calc_min_combined_steps("R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83"),610)
        self.assertEqual( calc_min_combined_steps("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),410)
    

if __name__ == '__main__':
    with open( "3.input.txt" ) as fp:
        path1 = fp.readline().strip()
        path2 = fp.readline().strip()

        print("part 1 min distance:",calc_min_cross_distance(path1,path2))
        print("part 2 min combined steps:",calc_min_combined_steps(path1,path2))

