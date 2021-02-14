
class processor:

    # i4004 Processor characteristics
    MAX_4_BITS = 15         #    Maximum value 4 bits can hold
    
    MEMORY_SIZE_RAM = 4096      # Number of 4-bit words in RAM
    MEMORY_SIZE_ROM = 4096      # Number of 4-bit words in ROM
    MEMORY_SIZE_PRAM = 4096     # Number of 4-bit words in PRAM

    NO_REGISTERS = 16           # Number of registers

    # Creation of processor internals

    ACCUMULATOR = 0     # Initialise the accumulator
    ACBR = 0            # Accumulator Buffer Register
    CARRY = 0           # Reset the carry bit

    RAM = []            # RAM
    ROM = []            # ROM
    REGISTERS = []      # Reegisters
    PRAM = [[],[],[]]   # Program RAM

    
    # Reset methods

    def __init_ram(self):
        for _i in range(self.MEMORY_SIZE_RAM - 1):
            self.RAM.append(0)

    def __init_registers(self):
        for _i in range(self.NO_REGISTERS - 1):
            self.REGISTERS.append(0)

    def __init_rom(self):
        for _i in range(self.MEMORY_SIZE_ROM - 1):
            self.ROM.append(0)

    def __init_pram(self):
        self.PRAM = [[[0 for _j in range(7)] for _k in range(255)] for _l in range(3)]

    # Sub-operation methods

    def set_carry(self):
        # Set the carry bit
        self.CARRY = 1
        return self.CARRY

    def reset_carry(self):
        # Reset the carry bit
        self.CARRY = 0
        return self.CARRY

    # Miscellaneous read/write operations

    def read_complement_carry(self):
        # Return the complement of the carry bit
        return 1 if self.CARRY == 0 else 0

    # Utility operations 

    def ones_complement(self, value: str):
        # Perform a one's complement
        # i.e. invert all the bits
        binary = bin(value)[2:].zfill(4)
        ones = ''
        for x in range(4):
            if (binary[x] == '1'):
                ones = ones + '0'
            else:
                ones = ones + '1'   
        return ones

    def decimal_to_binary(self, decimal: int):
        # Convert decimal to binary
        binary = bin(decimal)[2:].zfill(4)
        return binary
    
    def binary_to_decimal(self, binary: str):
        # Convert binary to decinal
        decimal = 0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        return decimal

    # Initialise processor

    def __init__(self):
        # Initialise all the internals of the processor
        self.ACCUMULATOR = 0
        self.__init_registers()
        self.__init_pram()
        self.__init_ram()
        self.__init_rom()
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
                        The result is stored in the accumulator. (Note this means the carry bit is also added)
        Syntax:         ADD <register>
        Assembled:      1000 <RRRR>
        Symbolic:       (RRRR) + (ACC) + (CY) --> ACC, CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to 1 if a sum greater than MAX_4_BITS was generated to indicate a carry out; 
                        otherwise, the carry/link is set to 0. The 4 bit content of the index register is unaffected.
        """
        
        self.ACCUMULATOR = self.ACCUMULATOR + self.REGISTERS[register] + self.read_carry()
        # Check for carry bit set/reset when an overflow is detected
        # i.e. the result is more than a 4-bit number (MAX_4_BITS)
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def sub(self, register):
        """
        Name:           Subtract index register from accumulator with borrow    
        Function:       The 4 bit content of the designated index register is complemented (ones complement) and 
                        added to content of the accumulator with borrow and the result is stored in the accumulator.
        Syntax:         SUB <register>
        Assembled:      1001 <RRRR>
        Symbolic:       (ACC) + ~(RRRR) + (CY) --> ACC, CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   If a borrow is generated, the carry bit is set to 0; otherwise, it is set to 1.
                        The 4 bit content of the index register is unaffected.        
        """

        carry = self.read_complement_carry()
        self.ACCUMULATOR = self.ACCUMULATOR + self.binary_to_decimal(self.ones_complement(self.REGISTERS[register])) + carry

        # Check for carry bit set/reset when borrow (overflow) is detected
        # i.e. the result is more than a 4-bit number (MAX_4_BITS)
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS -1
            self.set_carry()
        else:
            self.reset_carry()
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

        self.ACBR = self.ACCUMULATOR
        self.ACCUMULATOR = self.REGISTERS[register]
        self.REGISTERS[register] = self.ACBR
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
            eval('chip.'+x[0]+'('+x[1]+')')
    program.close()
    print()
    return chip.read_accumulator()


chip = processor()

"""
print('Registers [0-15]: ',chip.read_all_registers())
print('Accumulator     : ',chip.read_accumulator())
print('RAM             : ',chip.read_all_ram())
print('ROM             : ',chip.read_all_rom())
print('PRAM            : ',chip.read_all_pram())
"""


#or x in range(16):
#    print("binary of ",x, " is ", chip.ones_complement(x), "    ", chip.binary_to_decimal(chip.ones_complement(x)))
print('Accumulator : ',run('addition.asm'))
print(chip.read_carry())