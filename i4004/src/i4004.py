
class processor:

    MAX_4_BITS = 15
    
    ACCUMULATOR = 0

    RAM = []
    ROM = []
    REGISTERS = []
    PRAM = [[],[],[]]
    CARRY = False
    
    # Reset methods

    def init_ram(self):
        for _i in range(4096):
            self.RAM.append(0)

    def init_registers(self):
        for _i in range(15):
            self.REGISTERS.append(0)

    def init_rom(self):
        for _i in range(4096):
            self.ROM.append(0)

    def init_pram(self):
        self.PRAM = [[[0 for _j in range(7)] for _k in range(255)] for _l in range(3)]

    # Sub-operation methods

    def set_carry(self):
        self.CARRY = True
        return self.CARRY

    def reset_carry(self):
        self.CARRY = False
        return self.CARRY
    
    # Initialise processor

    def __init__(self):
        self.ACCUMULATOR = 0
        self.init_registers()
        self.init_pram()
        self.init_ram()
        self.init_rom()
        self.reset_carry()


    # Operators

    def nop(self, operand):
        """
        Name:           No Operation
        Function:       No operation performed.
        Syntax:         NOP
        Assembled:      0000 0000
        Symbolic:       Not applicable
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        return self

    def ldm(self, operand):
        """
        Name:           Load Accumulator Immediate
        Function:       The 4 bits of immediate data are loaded into the accumulator.
        Syntax:         LDM <value>
        Assembled:      1101 <DDDD>
        Symbolic:       DDDD --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.ACCUMULATOR = operand
        return self.ACCUMULATOR

    def ld(self, register):
        """
        Name:           Load index register to Accumulator
        Function:       The 4 bit content of the designated index register (RRRR) is loaded into accumulator.
                        The previous contents of the accumulator are lost.
        Syntax:         LD <value>
        Assembled:      1010 <RRRR>
        Symbolic:       (RRRR) --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.ACCUMULATOR = self.REGISTERS[register]
        return self.ACCUMULATOR


    def add(self, register):
        """
        Name:           Add index register to accumulator with carry
        Function:       The 4 bit content of the designated index register is added to the content of the accumulator with carry.
                        The result is stored in the accumulator. 
        Syntax:         ADD <register>
        Assembled:      1000 <RRRR>
        Symbolic:       (RRRR) + (ACC) + (CY) --> ACC, CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to 1 if a sum greater than MAX_4_BITS was generated to indicate a carry out; 
                        otherwise, the carry/link is set to 0. The 4 bit content of the index register is unaffected.
        """
        self.ACCUMULATOR = self.ACCUMULATOR + self.REGISTERS[register]
        # Check for carry bit set/reset when an overflow is detected
        # i.e. the result is more than a 4-bit number (MAX_4_BITS)
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY

    def sub(self, register):
        # TODO
        return self.ACCUMULATOR, self.CARRY

    def inc(self, register):
        """
        Name:           Increment index register
        Function:       The 4 bit content of the designated index register is incremented by 1. 
                        The index register is set to zero in case of overflow.
        Syntax:         INC <register>
        Assembled:      0110 <RRRR>
        Symbolic:       (RRRR) +1 --> RRRR
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.REGISTERS[register] = self.REGISTERS[register] + 1
        if (self.REGISTERS[register] > self.MAX_4_BITS ):
            self.REGISTERS[register] = 0
        return self.REGISTERS[register]


    def xch(self, register):
        """
        Name:           Exchange index register and accumulator
        Function:       The 4 bit content of designated index register is loaded into the accumulator.
                        The prior content of the accumulator is loaded into the designed register.
        Syntax:         XCH <register>
        Assembled:      1011 <RRRR>
        Symbolic:       (ACC) --> ACBR, (RRRR) --> ACC, (ACBR) --> RRRR
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        temporary_value = self.ACCUMULATOR
        self.ACCUMULATOR = self.REGISTERS[register]
        self.REGISTERS[register] = temporary_value
        return self.ACCUMULATOR, self.REGISTERS


    # Output Methods

    def read_all_registers(self):
        return(self.REGISTERS)

    def read_all_ram(self):
        return(self.RAM)

    def read_all_rom(self):
        return(self.ROM)

    def read_all_pram(self):
        return(self.PRAM)

    def read_accumulator(self):
        return(self.ACCUMULATOR)

    def read_carry(self):
        return(self.CARRY)

# Mnemonic link: http://e4004.szyc.org/iset.html

def run(program_name: str):
    program = open(program_name, 'r')

    print('Program Code')
    print()
    while True:
    
        line = program.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        line = line.strip()
        x = line.split(' ')
        if (len(line) > 0):
            print('     ', x[0], "  ",x[1])
            eval('processor.'+x[0]+'('+x[1]+')')
    program.close()
    print()
    return chip.read_accumulator()


chip = processor()
if not sum(chip.read_all_rom()):
    print('all zeroes')
else:
    print('non-zero')
    
"""
print('Registers [0-15]: ',chip.read_all_registers())
print('Accumulator     : ',chip.read_accumulator())
print('RAM             : ',chip.read_all_ram())
print('ROM             : ',chip.read_all_rom())
print('PRAM            : ',chip.read_all_pram())
"""


#print('Accumulator : ',run('addition.asm'))
#print(chip.read_carry())