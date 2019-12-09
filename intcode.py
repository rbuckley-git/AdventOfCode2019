import unittest

class computer:
    def __init__(self, prog, input = None ):
        self.prog = prog.copy()
        self.prog_size = len(self.prog)
        self.prog.extend([0]*1000)
        self.pc = 0
        self.relative_base_offset = 0
        self.stopped = False
        self.debugging = False
        self.inputs = []
        if input != None:
            self.inputs.append(input)

    def set_phase(self, phase):
        self.inputs.insert(0, phase)

    def add_input(self, data):
        self.inputs.append(data)

    def set_debugging(self, debug):
        self.debugging = debug

    def get_op_and_mode(self, d ):
        op = d % 100
        # pad to 5 chars with "0" 
        d = str(d).zfill(5)
        return op, int(d[2]), int(d[1]), int(d[0])

    def get_program(self):
        return self.prog[0:self.prog_size]

    def get_relative_base_offset(self):
        return self.relative_base_offset

    def is_stopped(self):
        return self.stopped

    def get_param(self,mode):
        if mode == 0:
            addr = self.prog[self.pc]
            self.pc+=1
            if addr > len(self.prog):
                raise Exception("cannot address memory",addr)
            return self.prog[addr]

        if mode == 1:
            a = self.prog[self.pc]
            self.pc+=1
            return a

        if mode == 2: 
            a = self.prog[self.pc]
            if self.debugging:
                print("pc",self.pc,"base offset",self.relative_base_offset,"offset",a)
            self.pc+=1
            if self.relative_base_offset + a > len(self.prog):
                raise Exception("cannot address (relative) memory",addr)
            return self.prog[self.relative_base_offset + a]

        raise Exception("illegal addressing mode",mode)

    def set_param(self,mode,value):
        if mode == 0:
            addr = self.prog[self.pc]
            self.pc+=1
            self.prog[addr] = value
            return

        if mode == 1:
            self.prog[self.pc] = value
            self.pc+=1
            return

        if mode == 2: 
            rel_addr = self.prog[self.pc]
            self.pc+=1
            self.prog[self.relative_base_offset + rel_addr] = value
            return

        raise Exception("illegal addressing mode",mode)


    def run(self):
        while True:
            if self.debugging:
                print("pc",self.pc)
            op,mode1,mode2,mode3 = self.get_op_and_mode( self.prog[self.pc] )
            if self.debugging:
                print("decode opcode",self.prog[self.pc],":",op,mode1,mode2,mode3)
            self.pc+=1

            if ( op == 1 or op == 2 ):        # addition or multiplication
                a = self.get_param(mode1)
                b = self.get_param(mode2)
                c = 0

                if ( op == 1 ):
                    c = a + b
                    if self.debugging:
                        print("add",a,"with",b,"=",c)
                else:
                    c = a * b
                    if self.debugging:
                        print("multiply",a,"with",b,"=",c)

                self.set_param(mode3,c)

            elif ( op == 3):     # input
                if len(self.inputs) == 0:
                    raise Exception("program asking for input and none available")

                a = self.inputs.pop(0)
                
                if self.debugging:
                    print("using",a,"input",self.inputs)

                self.set_param(mode1,a)

            elif ( op == 4):     # output
                a = self.get_param(mode1)

                if self.debugging:
                    print("outputing",a)

                return a

            elif ( op == 5 or op == 6 ):     # jump if param 1 is non-zero (5) or jump if zero (6), move to location specified by second param

                a = self.get_param(mode1)
                b = self.get_param(mode2)

                if ( op == 5 ):
                    if ( a != 0 ):
                        self.pc = b
                elif ( op == 6 ):
                    if ( a == 0 ):
                        self.pc = b

            elif ( op == 7 or op == 8 ):     # less than store 1 in position param 3 if param 1 less than param 2, equal store 1 if param 1 = param 2

                a = self.get_param(mode1)
                b = self.get_param(mode2)
                
                s = 0
                if ( op == 7 ):
                    if ( a < b ):
                        s = 1
                else:
                    if ( a == b ):
                        s = 1

                self.set_param(mode3,s)

            elif ( op == 9):    # adjust relative base offset
                a = self.get_param(mode1)
                self.relative_base_offset += a
                if self.debugging:
                    print("adjust relative base offset by",a,"now",self.relative_base_offset )

            elif ( op == 99):    # exit
                self.stopped = True
                self.pc+=1
                return

            else:
                raise Exception("illegal opcode " + str(op))

class AdventTestCase(unittest.TestCase):
    def get_op_and_mode(self):
        ic = computer([3,0,0,99],0)
        self.assertEqual( ic.get_op_and_mode(),(3,0,0,0))
        ic = computer([103,0,0,99],0)
        self.assertEqual( ic.get_op_and_mode(),(3,1,0,0))
        ic = computer([12303,0,0,99],0)
        self.assertEqual( ic.get_op_and_mode(),(3,1,2,3))

    def test_add_basic(self):
        ic = computer([1,0,0,0,99])
        ic.run()
        self.assertEqual( ic.get_program(),[2,0,0,0,99])

    def test_multiple_basic(self):
        ic = computer([2,3,0,3,99])
        ic.run()
        self.assertEqual( ic.get_program(),[2,3,0,6,99])

        ic = computer([2,4,4,5,99,0])
        ic.run()
        self.assertEqual( ic.get_program(),[2,4,4,5,99,9801])

    def test_add_and_jump(self):
        ic = computer([1,1,1,4,99,5,6,0,99])
        ic.run()
        self.assertEqual( ic.get_program(), [30,1,1,4,2,5,6,0,99] )

    def test_output(self):
        ic = computer([4,00,99])
        self.assertEqual( ic.run(),4 )

    def test_input_output1(self):
        ic = computer([3,1,4,1,99],22)
        self.assertEqual( ic.run(), 22 )

    def test_abs_param1(self):
        ic = computer([103,0,4,1,99],22)
        self.assertEqual( ic.run(), 22 )

    def test_abs_param2(self):
        ic = computer([103,0,104,33,99],22)
        self.assertEqual( ic.run(), 33  )

    def test_abs_param3(self):
        ic = computer([1101,100,-1,4,0])
        self.assertEqual( ic.run(), None  )

    def test_illegal_opcode(self):
        ic = computer([1,0,0,1,55])
        self.assertRaises( Exception, ic.run )

        ic = computer([12,99])
        self.assertRaises( Exception, ic.run )

    def test_halt(self):
        ic = computer([1,0,0,0,99])
        ic.run()
        self.assertTrue( ic.is_stopped() )

    def test_input_output2(self):
        ic = computer([3,9,8,9,10,9,4,9,99,-1,8],8)
        self.assertEqual( ic.run(), 1 )
    
    def test_relative_base(self):
        prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        ic = computer(prog)
        output = []
        while not ic.is_stopped():
            d = ic.run()
            if d != None:
                output.append(d)
        self.assertListEqual(prog,output)

        # should output a 16 digit number
        prog = [1102,34915192,34915192,7,4,7,99,0]
        ic = computer(prog)
        d = str(ic.run())
        self.assertEqual(len(d),16)

        ic = computer([104,1125899906842624,99])
        self.assertEqual(ic.run(),1125899906842624)

if __name__ == '__main__':
    pass
