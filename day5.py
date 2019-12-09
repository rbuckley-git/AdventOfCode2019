# https://adventofcode.com/
# 6/12/2019
# Day 5
#
# More for the intcode computer
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
    program = get_program( '5.input.txt' )

    ic = intcode.computer(program,1)
    while not ic.is_stopped():
        output = ic.run()
        if output != None:
            print("part 1 output",output)

    ic = intcode.computer(program,5)
    while not ic.is_stopped():
        output = ic.run()
        if output != None:
            print("part 2 output",output)
