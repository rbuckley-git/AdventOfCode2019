# https://adventofcode.com/
# 9/12/2019
# Day 9
#
# Gotcha here for me was the requirement to use more memory in the program as working space. Added this in to the computer
# class to avoid breaking all the test cases.
#
import unittest
import intcode




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
                