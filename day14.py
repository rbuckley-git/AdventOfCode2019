# https://adventofcode.com/
# 14/12/2019
# Day 14
#

import unittest

formulas = {}
spare = {}

def load_formulas(filename):
    global spare
    spare = {}
    with open( filename ) as fp:
        for line in fp.readlines():
            ingredients = line.strip().replace("=>",",").split(",")
            parts = list(map(str.split,list(map(str.strip,ingredients))))
            key = parts[-1][1]
            quantity = int(parts[-1][0])

            temp = []
            for i in range(0,len(parts)-1):
                temp.append((parts[i][1],int(parts[i][0])))
            formulas[key] = (quantity,temp)
        

def print_formulas():
    for k,v in formulas.items():
        print(k,v)

"""
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

def calc_multiple(needed,produces):
    m=int(needed/produces)
    if needed%produces > 0:
        m = needed // produces + 1

    if m==0:
        m=1

    return m

def solve(ingredient, n, indent = 0):
    spaces = " " * indent

    print(spaces,"need",n,"of",ingredient)

    if ingredient == "ORE":
        return n

    if not ingredient in spare:
        spare[ingredient] = 0

    f = formulas[ingredient]

    ans = 0
    for (k,quantity_produced) in f[1]:
        produces = f[0]

        multiple = calc_multiple(n,produces)

        if spare[ingredient] >= n:
            print(spaces,"taking",n,"from spare leaving",spare[ingredient])
            spare[ingredient] -= n
            multiple = 0
            n = 0
        elif spare[ingredient] > 0:
            print(spaces,"taking",spare[ingredient],"from spare leaving zero")
            n -= spare[ingredient]
            spare[ingredient] = 0
            multiple = calc_multiple(n,produces)

        print(spaces,"producing",multiple,"in units of",produces,"to satisfy",n)
        ans += solve(k,quantity_produced * multiple,indent+2)

        if produces * multiple > n:
            print(spaces,"stash",(produces*multiple) - n,"of",ingredient)
            spare[ingredient] += (produces*multiple) - n

    print(spaces,"ans",ans,spare)

    return ans

class AdventTestCase(unittest.TestCase):
    def test_1(self):
        load_formulas("14.test.1.input.txt")
        print_formulas()
        self.assertEqual(solve('FUEL',1),31)

    def test_2(self):
        load_formulas("14.test.2.input.txt")
        print_formulas()
        self.assertEqual(solve('FUEL',1),165)

    def test_2(self):
        load_formulas("14.test.3.input.txt")
        print_formulas()
        self.assertEqual(solve('FUEL',1),13312)


if __name__ == '__main__':
    pass