# https://adventofcode.com/
# 9/12/2019
# Day 9
#
# Gotcha here for me was the requirement to use more memory in the program as working space. Added this in to the computer
# class to avoid breaking all the test cases.
#

import intcode

def get_program( filename ):

    with open( filename ) as fp:
        line = fp.readline()
        prog = []
        for d in line.strip().split(","):
            prog.append(int(d))
        return prog

if __name__ == '__main__':

    program = get_program( '9.input.txt' )

    ic = intcode.computer(program,1)
    #ic.set_debugging(True)
    while not ic.is_stopped():
        output = ic.run()
        if output != None:
            print("part 1 output:",output)
    
    ic = intcode.computer(program,2)
    #ic.set_debugging(True)
    while not ic.is_stopped():
        output = ic.run()
        if output != None:
            print("part 2 output:",output)
                