# https://adventofcode.com/
# 23/12/2019
# Day 21
#
# 
#

import intcode

prog = intcode.get_program("20.input.txt")


if __name__ == '__main__':

    ic = intcode.computer(prog)

    while not ic.is_stopped():
        output = ic.run()
        if output == None:
            continue
