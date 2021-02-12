
class i4004:

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
        CARRY = True:
        return CARRY

    def reset_carry(self):
        CARRY = False:
        return CARRY
    
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


# Mnemonic link: http://e4004.szyc.org/iset.html

processor = i4004()

"""
print('Registers [0-15]: ',processor.read_all_registers())
print('Accumulator     : ',processor.read_accumulator())
print('RAM             : ',processor.read_all_ram())
print('ROM             : ',processor.read_all_rom())
print('PRAM            : ',processor.read_all_pram())
"""

print(processor.ldm(23))

print(processor.xch(4))
print(processor.ld(4))
print(processor.ldm(92))
print(processor.xch(8))
print(processor.xch(8))