# https://adventofcode.com/
# 4/12/2019
# Day 1
#
# Straightforward challenge.
#
import unittest

def calcFuelForMass( mass ):
    a = int(mass/3)
    a -= 2
    return a

# Calculation taking into account the additional mass the fuel will bring
#
def calcFuelIncludingFuelMass( mass ):
    f = calcFuelForMass( mass )
    fuelForFuel = f
    while True:
        fuelForFuel = calcFuelForMass( fuelForFuel )
        if (fuelForFuel < 0):
            break
        f += fuelForFuel

    return f

#
# test cases
#
class AdventTestCase(unittest.TestCase):
    def test_CalcFuel(self):
        self.assertEqual( calcFuelForMass( 12 ), 2 )
        self.assertEqual( calcFuelForMass( 14 ), 2 )
        self.assertEqual( calcFuelForMass( 1969 ), 654 )
        self.assertEqual( calcFuelForMass( 100756 ), 33583 )

    def test_CalcFuelIncludingFuelMass(self):
        self.assertEqual( calcFuelIncludingFuelMass( 12 ), 2 )
        self.assertEqual( calcFuelIncludingFuelMass( 14 ), 2 )
        self.assertEqual( calcFuelIncludingFuelMass( 1969 ), 966 )
        self.assertEqual( calcFuelIncludingFuelMass( 100756 ), 50346 )

if __name__ == '__main__':

    with open( '1.input.txt' ) as fp:
        sum1 = 0
        sum2 = 0
        for line in fp:
            sum1 += calcFuelForMass(int(line[:-1]))
            sum2 += calcFuelIncludingFuelMass(int(line[:-1]))

        print( "Part 1 total: ", sum1 )
        print( "Part 2 total: ", sum2 )
