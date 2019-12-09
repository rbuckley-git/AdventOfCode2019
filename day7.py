# https://adventofcode.com/
# 7/12/2019
# Day 7
#
# This called for significant refactoring of the intcode computer into a separate class.
#
import unittest
import itertools
import intcode

def calc_max_truster_signal( program, phaseSeq ):
    data = 0
    for phase in phaseSeq:
        ic = intcode.computer( program.copy(), data )
        ic.set_phase(phase)
        data = ic.run()
        
    return data

def calc_max_truster_signal_feedback_loop( program, phaseSeq ):
    amps = []
    for i in range(5):
        amp = intcode.computer(program)
        amp.set_phase(phaseSeq[i])
        amps.append(amp)

    data = 0
    i = 0
    amp_five_output = 0
    while True:
        amp = amps[i % 5]
        amp.add_input(data)
        data = amp.run()

        if i == 4:
            amp_five_output = data

        if amp.is_stopped():
            return amp_five_output

        i+=1
        if i>4:
            i = 0

#
# test cases
#
class AdventTestCase(unittest.TestCase):
    def test_calc_max_truster_signal(self):
        self.assertEqual( calc_max_truster_signal( 
            [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], 
            [4,3,2,1,0] ), 43210 )
        self.assertEqual( calc_max_truster_signal( 
            [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], 
            [0,1,2,3,4] ), 54321 )
        self.assertEqual( calc_max_truster_signal( 
            [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,
            31,1,32,31,31,4,31,99,0,0,0], 
            [1,0,4,3,2] ), 65210 )
    
    def test_calc_max_truster_signal_feedback_loop(self):
        self.assertEqual( calc_max_truster_signal_feedback_loop( 
            [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], 
            [9,8,7,6,5] ), 139629729 )

        self.assertEqual( calc_max_truster_signal_feedback_loop( 
            [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], 
            [9,7,8,5,6] ), 18216 )

if __name__ == '__main__':
    program = intcode.get_program( '7.input.txt' )

    # calculate all permutations of this list 
    perms = list(itertools.permutations([0, 1, 2, 3, 4]))
    maxThrust = 0
    for x in perms:
        thrust = calc_max_truster_signal(program,x)
        if thrust > maxThrust:
            maxThrust = thrust

    print("part 1 max thrust",maxThrust)

    # calculate all permutations of this list 
    perms = list(itertools.permutations([5,6,7,8,9]))
    maxThrust = 0
    for x in perms:
        thrust = calc_max_truster_signal_feedback_loop(program,x)
        if thrust > maxThrust:
            maxThrust = thrust

    print("part 2 max thrust",maxThrust)

