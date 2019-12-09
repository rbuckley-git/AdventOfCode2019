# https://adventofcode.com/
# 4/12/2019
# Day 2
#
# This was the start of the intcode. Unit tests migrated to that module now. Code was originally basic and inline but worked. Refactoring came for day 7.
#
import unittest
import intcode

def get_program( filename ):

    with open( filename ) as fp:
        line = fp.readline()
        prog = []
        for d in line.strip().split(","):
            prog.append(int(d))
        return prog

if __name__ == '__main__':

    program = get_program( '2.input.txt' )
    program[1] = 12
    program[2] = 2
    ic = intcode.computer(program)
    ic.run()
    p = ic.get_program()

    print("part 1 output",p[0])

    running = True
    for a in range(100):
        for b in range(100):
            p = program
            p[1] = a
            p[2] = b
            ic = intcode.computer(p)
            ic.run()
            p = ic.get_program()
            answer = p[0]

            if ( answer == 19690720):
                r = 100*a+b
                print("part 2 answer",r)

                running = False
                break

        if not running:
            break
