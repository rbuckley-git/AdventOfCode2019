# https://adventofcode.com/
# 6/12/2019
# Day 4
#
# Straightforward challenge.
#
import unittest

def validatePasswordA( password ):
    # rule 1 - password must be 6 characters
    if ( len(password) != 6 ):
        return False
    
    # rule 2 - two adjacent digits are the same
    rule2 = False
    for i in range( len(password) - 1 ):
        if ( password[i] == password[i+1] ):
            rule2 = True

    if ( not rule2 ):
        return False

    # rule 3 - digits left to right increase or stay same
    x = 0
    for i in range( len(password) ):
        if ( int(password[i]) < x ):
            return False
        x = int(password[i])

    return True

def validatePasswordB( password ):
    if ( not validatePasswordA(password) ):
        return False

    repeats = {}
    c = 0
    for i in range( len(password) - 1 ):
        if ( password[i] == password[i+1] and c == 0):
            repeats[ password[i] ] = 1
            c+=1
        elif ( c > 0 ):
            c=0

    rule = False
    for ch in repeats:
        n = 0
        for i in range( len(password)):
            if ( password[i] == ch ):
                n+=1
        if ( n == 2 ):
            rule = True

    return rule

#
# test cases
#
class AdventTestCase(unittest.TestCase):
    def test_passwordTestA(self):
        self.assertTrue( validatePasswordA("123389") )
        self.assertTrue( validatePasswordA("111111") )
        self.assertTrue( validatePasswordA("333389") )
        self.assertFalse( validatePasswordA("223450") )
        self.assertFalse( validatePasswordA("123789") )
        self.assertFalse( validatePasswordA("13789") )
        self.assertFalse( validatePasswordA("003454") )

    def test_passwordTestB(self):
        self.assertTrue( validatePasswordB("112233") )
        self.assertTrue( validatePasswordB("111122") )
        self.assertFalse( validatePasswordB("123444") )
        self.assertFalse( validatePasswordB("123334") )
        self.assertFalse( validatePasswordB("155558") )
        self.assertTrue( validatePasswordB("556678") )


if __name__ == '__main__':

    correct = 0
    for i in range(206938,679128+1):
        if ( validatePasswordA(str(i)) ):
            correct+=1
    print("part 1 valid passwords:",correct)

    correct = 0
    for i in range(206938,679128+1):
        if ( validatePasswordB(str(i)) ):
            correct+=1
    print("part 2 valid passwords:",correct)
