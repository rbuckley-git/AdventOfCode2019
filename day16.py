# https://adventofcode.com/
# 27/12/2019
# Day 16
#
import unittest

def parse_input(filename):
    with open( filename ) as fp:
        return [int(ch) for ch in fp.read().strip()]

def calc_pattern(input_length,i):
    pattern = [0] * (i+1) + [1] * (i+1) + [0] * (i+1) + [-1] * (i+1)
    while len(pattern) <= input_length:
        pattern += pattern

    return pattern[1:]

def process_phase(digits):
    output_digits = []
    for i in range(len(digits)):
        pattern = calc_pattern(len(digits),i)
        output = 0
        for k in range(len(digits)):
            output += digits[k] * pattern[k]
        output_digits.append(abs(output) % 10)
    return output_digits

class AdventTestCase(unittest.TestCase):
    def test_case1(self):
        digits = parse_input("16.test.1.input.txt")
        
        for i in range(4):
            digits = process_phase(digits)

        self.assertEqual("".join(map(str,digits)),"01029498")

    def test_case2(self):
        digits = parse_input("16.test.2.input.txt")
        
        for i in range(100):
            digits = process_phase(digits)
        final_output = "".join(map(str,digits))
        self.assertEqual(final_output[0:8],"24176176")

    def test_case3(self):
        digits = parse_input("16.test.3.input.txt")
        
        for i in range(100):
            digits = process_phase(digits)
        final_output = "".join(map(str,digits))
        self.assertEqual(final_output[0:8],"73745418")

    def test_case4(self):
        digits = parse_input("16.test.4.input.txt")
        digits = digits * 10000
        offset = int("".join(map(str,digits[0:7])))
        print("Offset:",offset)

        for i in range(100):
            digits = process_phase(digits)
        print(digits)
        output = "".join(map(str,digits[offset+1:offset+9]))
        self.assertEqual(output,"84462026")


if __name__ == '__main__':
    """
    digits = parse_input("16.input.txt")

    for i in range(100):
        digits = process_phase(digits)
        #print(digits)
    final_output = "".join(map(str,digits))
    print("Part 1:",final_output[0:8])
    """
    digits = parse_input("16.input.txt")
    digits = digits * 10000

    offset = int("".join(map(str,digits[0:7])))
    print("Offset:",offset)
    print("")
