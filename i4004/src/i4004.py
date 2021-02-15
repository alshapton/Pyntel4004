
class processor:

    # i4004 Processor characteristics
    MAX_4_BITS = 15         #    Maximum value 4 bits can hold
    MSB = 8                 #    Most significant bit value (4-bit)
    
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

    
    # Initialisation methods

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
        self.ACBR = 0
        self.__init_registers()
        self.__init_pram()
        self.__init_ram()
        self.__init_rom()
        self.reset_carry()

    """
                                  
                .-.                                              
               (._.)        ,--.      .-.      .-.        ,--.   
                .-.        /   |    /    \   /    \      /   |   
                | |       / .' |   |  .-. ; |  .-. ;    / .' |   
                | |      / / | |   | |  | | | |  | |   / / | |   
                | |     / /  | |   | |  | | | |  | |  / /  | |   
                | |    /  `--' |-. | |  | | | |  | | /  `--' |-. 
                | |    `-----| |-' | '  | | | '  | | `-----| |-' 
                | |          | |   '  `-' / '  `-' /       | |   
               (___)        (___)   `.__,'   `.__,'       (___)  
        
         _           _                   _   _                        _   
        (_)_ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __    ___  ___| |_ 
        | | '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \  / __|/ _ \ __|
        | | | | \__ \ |_| |  | |_| | (__| |_| | (_) | | | | \__ \  __/ |_ 
        |_|_| |_|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_| |___/\___|\__|
                                                                        
    
    """           
    # Operators

    # One Word Machine Instructions

    def nop(self):
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

    def ldm(self, operand:int):
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

    def ld(self, register:int):
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
   
    
    def xch(self, register:int):
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

  
    def add(self, register:int):
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
            self.ACCUMULATOR = self.MAX_4_BITS  - self.MAX_4_BITS - 1 
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def sub(self, register:int):
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
            self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def inc(self, register:int):
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
            self.REGISTERS[register] = self.MAX_4_BITS - self.REGISTERS[register]
        return self.REGISTERS[register]


    def bbl(self):
        return None


    def jin(self):
        return None


    def src(self):
        return None


    def fin(self):
        return None



   # Accumulator Group Instructions

    def clb(self):
        """
        Name:           Clear Both
        Function:       Set accumulator and carry/link to 0.
        Syntax:         CLB
        Assembled:      1111 0000
        Symbolic:       0 --> ACC, 0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.ACCUMULATOR = 0
        self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def clc(self):
        """
        Name:           Clear Carry
        Function:       Set carry/link to 0.
        Syntax:         CLC
        Assembled:      1111 0001
        Symbolic:       0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.reset_carry()
        return self.CARRY

    def cmc(self):
        """
        Name:           Complement carry
        Function:       The carry/link content is complemented.
        Syntax:         CLC
        Assembled:      1111 0011
        Symbolic:       ~(CY) --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        if (self.CARRY == 1):
            self.reset_carry()
        else:
            self.set_carry()
        return self.CARRY


    def stc(self):
        """
        Name:           Set Carry
        Function:       Set carry/link to 1.
        Syntax:         STC
        Assembled:      1111 1010
        Symbolic:       1 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.set_carry()
        return self.CARRY


    def cma(self):
        """
        Name:           Complement Accumulator
        Function:       The content of the accumulator is complemented. The carry/link is unaffected.
        Syntax:         CMA
        Assembled:      1111 0100
        Symbolic:       ~a3 ~a2 ~a1 ~a0 --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.ACCUMULATOR = self.ones_complement(self.ACCUMULATOR)
        return self.ACCUMULATOR


    def iac(self):
        """
        Name:           Increment accumulator
        Function:       The content of the accumulator is incremented by 1.
        Syntax:         IAC
        Assembled:      1111 0010
        Symbolic:       (ACC) +1 --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   No overflow sets the carry/link to 0; overflow sets the carry/link to a 1.
        """

        self.ACCUMULATOR = self.ACCUMULATOR + 1
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def dac(self):
        """
        Name:           Decrement accumulator
        Function:       The content of the accumulator is decremented by 1.
        Syntax:         DAC
        Assembled:      1111 1000
        Symbolic:       (ACC) -1 --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   A borrow sets the carry/link to 0; no borrow sets the carry/link to a 1.
        """

        self.ACCUMULATOR = self.ACCUMULATOR + 15
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def ral(self):
        """
        Name:           Rotate left
        Function:       The content of the accumulator and carry/link are rotated left.
        Syntax:         RAL
        Assembled:      1111 0101
        Symbolic:       C0 --> a0, a(i) --> a(i+1), a3 -->CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit will be set to the highest significant bit of the accumulator.
        """

        # Store Carry bit
        C0 = self.read_carry()
        # Shift left
        self.ACCUMULATOR = self.ACCUMULATOR * 2
        # Set carry bit correctly
        if (self.ACCUMULATOR >= self.MAX_4_BITS):
                self.set_carry()
        else:
            self.reset_carry()
        # If necessary remove non-existent bit 5
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
        # Add ooriginal carry bit
        self.ACCUMULATOR = self.ACCUMULATOR + C0
        return self.ACCUMULATOR, self.CARRY


    def rar(self):
        """
        Name:           Rotate right
        Function:       The content of the accumulator and carry/link are rotated right.
        Syntax:         RAR
        Assembled:      1111 0110
        Symbolic:       a0 --> CY, a(i) --> a(i-1), C0 -->a3
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit will be set to the lowest significant bit of the accumulator.
        """

        # Store Carry bit
        C0 = self.read_carry()
        # Set carry bit coorrectly
        if (self.ACCUMULATOR % 2 == 0):
            self.reset_carry()
        else:
            self.set_carry() 
        # Shift right
        self.ACCUMULATOR = self.ACCUMULATOR // 2 
        # Add carry to high-order bit of accumulator
        self.ACCUMULATOR = self.ACCUMULATOR + (C0 * self.MSB)
        return self.ACCUMULATOR, self.CARRY


    def tcc(self):
        """
        Name:           Transmit carry and clear
        Function:       The accumulator is cleared. 
                        The least significant position of the accumulator is set to the value of the carry/link.
        Syntax:         TCC
        Assembled:      111 0111
        Symbolic:       0 --> ACC, (CY) --> a0, 0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit will be set to the 0.
        """

        self.ACCUMULATOR = 0
        self.ACCUMULATOR = self.read_carry()
        self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def daa(self):
        """
        Name:           Decimal adjust accumulator
        Function:       The accumulator is incremented by 6 if 
                        either the carry/link is 1 or if the accumulator content is greater than 9.        
        Syntax:         DAA
        Assembled:      1111 1011
        Symbolic:       (ACC) + (0000 or 0110) --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to a 1 if the result generates a carry, otherwise it is unaffected.
        """

        if (self.read_carry == 1 or self.ACCUMULATOR > 9):
            self.ACCUMULATOR = self.ACCUMULATOR + 6
            if (self.ACCUMULATOR > self.MAX_4_BITS ):
                self.ACCUMULATOR = self.MAX_4_BITS  - self.MAX_4_BITS 
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY

    def tcs(self):
        """
        Name:           Transfer Carry Subtract
        Function:       The accumulator is set to 9 if the carry/link is 0.
                        The accumulator is set to 10 if the carry/link is a 1.    
        Syntax:         TCS
        Assembled:      1111 1001
        Symbolic:       1001 --> ACC if (CY) = 0
                        1010 --> ACC if (CY) = 1
                        0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to 0.
        """

        if (self.read_carry() == 0 ):
            self.ACCUMULATOR = 9
        else:
            self.ACCUMULATOR = 10
        self.reset_carry()
        return self.ACCUMULATOR, self.CARRY






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


# Valid Opcodes

OPCODES = ['NOP', 'JCN', 'FIM', 'SRC', 'FIN', 'JIN', 'JUN', 'JMS',
'INC', 'ISZ', 'ADD', 'SUB', 'LD', 'XCH', 'BBL', 'LDM', 'WRM',
'WMP', 'WRR', 'WR0', 'WR1', 'WR2', 'WR3', 'SBM', 'RDM', 'RDR',
'ADM', 'RD0', 'RD1', 'RD2', 'RD3', 'CLB', 'CLC', 'IAC', 'CMC',
'CMA', 'RAL', 'RAR', 'TCC', 'DAC', 'TCS', 'STC', 'DAA','KBP', 'DCL']

def run(program_name: str):
    program = open(program_name, 'r')

    print('Program Code')
    print()
    while True:
        count = 0
        line = program.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        line = line.strip()
        x = line.split()
        if (len(line) > 0):
            opcode = x[0]
            u_opcode = opcode.upper()
            if (opcode in ['org','end']) or ( u_opcode in OPCODES):
                if (opcode in ['org','end']):
                    pass
                else:
                    # Check for operand
                    if (len(x) == 2):
                        # Operator and operand
                        print('     ', opcode, "  ",x[1])
                        eval('chip.'+opcode+'('+x[1]+')')
                    else:
                        # Only operator
                        eval('chip.'+opcode+'()')
                        print('     ', opcode)
                        
            else:
                print()
                print("Invalid mnemonic '",opcode,"' at line: ", count)
                break
        count = count + 1
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
run('example.asm')
print('Accumulator : ',chip.read_accumulator())
print('              ', chip.decimal_to_binary(chip.read_accumulator()))
print('              ', chip.read_carry())

