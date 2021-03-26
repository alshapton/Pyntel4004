###########################################################################
#                                                                         #
#            .-.                                                          #
#           (._.)        ,--.      .-.      .-.        ,--.               #
#            .-.        /   |    /    \   /    \      /   |               #
#            | |       / .' |   |  .-. ; |  .-. ;    / .' |               #
#            | |     / /  | |   | |  | | | |  | |   / / | |               #
#            | |    / /   | |   | |  | | | |  | |  / /  | |               #
#            | |   /  `--'  |-. | |  | | | |  | | /  `--' |-.             #
#            | |    `-----| |-' | '  | | | '  | | `-----| |-'             #
#            | |          | |   '  `-' / '  `-' /       | |               #
#           (___)        (___)   `.__,'   `.__,'       (___)              #
#                                                                         #
#     _           _                   _   _                        _      #
#    (_)_ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __    ___  ___| |_    #
#    | | '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \  / __|/ _ \ __|   #
#    | | | | \__ \ |_| |  | |_| | (__| |_| | (_) | | | | \__ \  __/ |_    #
#    |_|_| |_|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_| |___/\___|\__|   #
#                                                                         #
###########################################################################

from .exceptions import InvalidRamBank

"""
Abbreviations used in the descriptions of each instruction's actions:

        (    )	    the content of
        -->	        is transferred to
        ACC	        Accumulator (4-bit)
        CY	        Carry/link Flip-Flop
        ACBR	    Accumulator Buffer Register (4-bit)
        RRRR	    Index register address
        RRR	        Index register pair address
        PL	        Low order program counter Field (4-bit)
        PM	        Middle order program counter Field (4-bit)
        PH	        High order program counter Field (4-bit)
        ai	        Order i content of the accumulator
        CMi	        Order i content of the command register
        M	        RAM main character location
        MSi	        RAM status character i
        DB (T)	    Data bus content at time T
        Stack	    The 3 registers in the address register
                    other than the program counter

Additional Abbreviations:
        ~           Inverse (1's complement)
        .           logical OR
"""
# Operators

# One Word Machine Instructions




def ldm(self, operand: int):
    """
    Name:           Load Accumulator Immediate
    Function:       The 4 bits of immediate data are loaded into
                    the accumulator.
    Syntax:         LDM <value>
    Assembled:      1101 <DDDD>
    Symbolic:       DDDD --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.
    """
    
    self.ACCUMULATOR = operand
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def ld(self, register: int):
    """
    Name:           Load index register to Accumulator
    Function:       The 4 bit content of the designated index register
                    (RRRR) is loaded into accumulator.
                    The previous contents of the accumulator are lost.
    Syntax:         LD <value>
    Assembled:      1010 <RRRR>
    Symbolic:       (RRRR) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.
    """

    self.ACCUMULATOR = self.REGISTERS[register]
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def xch(self, register: int):

    '''
    Name:           Exchange index register and accumulator
    Function:       The 4 bit content of designated index register is
                    loaded into the accumulator. The prior content of the
                    accumulator is loaded into the designed register.
    Syntax:         XCH <register>
    Assembled:      1011 <RRRR>
    Symbolic:       (ACC) --> ACBR, (RRRR) --> ACC, (ACBR) --> RRRR
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.

    '''

    self.ACBR = self.ACCUMULATOR
    self.ACCUMULATOR = self.REGISTERS[register]
    self.insert_register(register, self.ACBR)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.REGISTERS


def add(self, register: int):
    """
    Name:           Add index register to accumulator with carry
    Function:       The 4 bit content of the designated index register
                    is added to the content of the accumulator with carry.
                    The result is stored in the accumulator. (Note this
                    means the carry bit is also added)
    Syntax:         ADD <register>
    Assembled:      1000 <RRRR>
    Symbolic:       (RRRR) + (ACC) + (CY) --> ACC, CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is set to 1 if a sum greater than
                    MAX_4_BITS was generated to indicate a carry out;
                    otherwise, the carry/link is set to 0. The 4 bit
                    content of the index register is unaffected.
    """

    self.ACCUMULATOR = (self.ACCUMULATOR + self.REGISTERS[register] +
                        self.read_carry())
    # Check for carry bit set/reset when an overflow is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.MAX_4_BITS - self.MAX_4_BITS - 1
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def sub(self, register: int):
    """
    Name:           Subtract index register from accumulator with borrow
    Function:       The 4 bit content of the designated index register is
                    complemented (ones complement) and added to content of
                    the accumulator with borrow and the result is stored
                    in the accumulator.
    Syntax:         SUB <register>
    Assembled:      1001 <RRRR>
    Symbolic:       (ACC) + ~(RRRR) + (CY) --> ACC, CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   If a borrow is generated, the carry bit is set to 0,
                    otherwise, it is set to 1.
                    The 4 bit content of the index register is unaffected.
    """

    carry = self.read_complement_carry()
    self.ACCUMULATOR = (self.ACCUMULATOR +
                        self.binary_to_decimal(
                            self.ones_complement(self.REGISTERS[register]))
                        + carry)

    # Check for carry bit set/reset when borrow (overflow) is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def bbl(self, accumulator: int):
    """
    Name:           Branch back and load data to the accumulator
    Function:       The program counter (address stack) is pushed down one
                    level.
                    Program control transfers to the next instruction
                    following the last jump to subroutine (JMS)
                    instruction.
                    The 4 bits of data DDDD stored in the OPA portion of
                    the instruction are loaded to the accumulator.
                    BBL is used to return from subroutine to main program.
    Syntax:         BBL
    Assembled:      0110 DDDD
    Symbolic:       (Stack) --> PL, PM, PH
                    DDDD --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    address = self.read_from_stack()
    self.PROGRAM_COUNTER = address
    self.ACCUMULATOR = accumulator
    return self.PROGRAM_COUNTER, self.ACCUMULATOR


def jin(self):
    return None


def src(self, registerpair: int):
    """
    Name:           Send register control
    Function:       The 8 bit content of the designated index register pair
                    is sent to the RAM address register at X2 and X3.
                    A subsequent read, write, or I/O operation of the RAM will
                    utilize this address. Specifically, the first 2 bits of the
                    address designate a RAM chip; the second 2 bits designate
                    1 out of 4 registers within the chip;
                    the last 4 bits designate 1 out of 16 4-bit main memory
                    characters within the register.

                    This command is also used to designate a ROM for a
                    subsequent ROM I/O port operation. The first 4 bits
                    designate the ROM chip number to be selected. The address
                    in ROM or RAM is not cleared until the next SRC
                    instruction is executed.
                    The 8 bit content of the index register is unaffected.
    Syntax:         SRC
    Assembled:      0010 RRR1
    Symbolic:       (RRRO) --> DB (X2)
                    (RRR1) --> DB (X3)
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec..
    Side-effects:   Not Applicable
    """

    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    address = self.read_registerpair(registerpair)
    self.COMMAND_REGISTERS[self.read_current_ram_bank()] = address
    return None


def fin(self, registerpair: int):
    """
    Name:           Fetch indirect from ROM
    Function:       The 8 bit content of the 0 index register
                    pair (0000) (0001)
                    is sent out as an address in the same page
                    where the FIN instruction is located. The 8 bit
                    word at that location is loaded into the designated
                    index register pair. The program counter is unaffected;
                    after FIN has been executed the next instruction in
                    sequence will be addressed. The content of the 0 index
                    register pair is unaltered unless index register 0
                    was designated.
    Syntax:         FIN
    Assembled:      0011 RRRO
    Symbolic:       (PH) (0000) (0001) --> ROM address
                    (OPR) --> RRRO
                    (OPA) --> RRR1
    Execution:      1 word, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable
    Exceptions:     a) Although FIN is a 1-word instruction, its execution
                        requires two memory cycles (21.6 psec).
                    b) When FIN is located at address (PH) 1111 1111 data will
                        be fetched from the next page(ROM) in sequence and not
                        from the same page(ROM) where the FIN instruction is
                        located. That is, next address is
                        (PH + 1) (0000) (0001) and not (PH) (0000) (0001).
    """

    # EXCEPTION (b) - fin instruction is located at page boundary #
    eop = self.is_end_of_page(self.PROGRAM_COUNTER, 1)
    if (eop is True):
        page_shift = 1
    else:
        page_shift = 0
    value = self.RAM[(self.REGISTERS[1] + (self.REGISTERS[0] << 4)) +
                     (self.PAGE_SIZE * page_shift)]
    self.insert_registerpair(registerpair, value)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.REGISTERS[registerpair], self.REGISTERS[registerpair+1]

# 2-word Instructions


def jun(self, address: int):
    """
    Name:           Jump unconditional
    Function:       Program control is unconditionally
                    transferred to the instruction located
                    at the address AAAA3, AAAA2, AAAA1.
    Syntax:         JUN
    Assembled:      0100 AAAA3
                    AAAA2 AAAA1
    Symbolic:       AAAA1 --> PL,
                    AAAA2 --> PM,
                    AAAA3 --> PH
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable
    """
    self.PROGRAM_COUNTER = address
    return self.PROGRAM_COUNTER


def jms(self, address: int):
    """
    Name:           Jump to Subroutine
    Function:       The address of the next instruction in sequence following
                    JMS (return address) is saved in the push down stack.
                    Program control is transferred to the instruction located
                    at the 12 bit address (AAAA3,AAAA2,AAAA1). Execution of a
                    return instruction (BBL) will cause the saved address to
                    be pulled out of the stack, therefore, program control
                    is transferred to the next sequential instruction after
                    the last JMS.
                    The push down stack has 4 registers. One of them is used
                    as the program counter, therefore nesting of JMS can occur
                    up to 3 levels.
    Syntax:         JMS
    Assembled:      0101 AAAA3
                    AAAA2 AAAA1
    Symbolic:       AAAA1 --> PL,
                    AAAA2 --> PM,
                    AAAA3 --> PH
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable

    """
    # Add number of words so return address is correct
    self.write_to_stack(self.PROGRAM_COUNTER + 2)
    self.PROGRAM_COUNTER = address
    return self.PROGRAM_COUNTER


def jcn(self, conditions: int, address: int):
    """
    Name:           Jump conditional
    Function:       If the designated condition code is true, program control
                    is transferred to the instruction located at the 8 bit
                    address AAAA2, AAAA1 on the same page (ROM) where JCN is
                    located.
                    If the condition is not true the next instruction in
                    sequence after JCN is executed.
                    The condition bits are assigned as follows:
                    C1 = 0 Do not invert jump condition }
                    C1 = 1 Invert jump condition        }
                    C2 = 1 Jump if the accumulator content is zero
                    C3 = 1 Jump if the carry/link content is 1
                    C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
    Syntax:         JCN
    Assembled:      0001 C1C2C3C4
                    AAAA2 AAAA1
    Symbolic:       If C1C2C3C4 is true, A2A2A2A2 --> PM
                    A1A1A1A1 --> PL, PH unchanged
                    if C1C2C3C4 is false,
                    (PH) --> PH, (PM) --> PM, (PL + 2) --> PL
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Example:
    OPR     OPA
    ----    ----
    0001    0110  Jump if accumulator is zero or carry = 1

    Several conditions can be tested simultaneously.
    The logic equation describing the condition for a jump is give below:
    JUMP = ~C1 . ((ACC = 0) . C2 + (CY = 1) . C3 +
                ~TEST . C4) + C1 . ~((ACC = 0) . C2 +
                (CY = 1) . C3 + ~TEST . C4)

    Side-effects:   Not Applicable

    Info about signal/test pin 10 on intel4004
    https://tams.informatik.uni-hamburg.de/applets/hades/webdemos/80-mcs4/jmp/jmp_test.html

    Assembler:
            jcn     IACT    lbl

    I - Invert other conditions
    A - Accumulator = 0
    C - Carry Bit set (i.e. = 1)
    T - Test Signal on Intel4004 Pin 10 = 0

    Need to do "if JCN at end of page" code
    """

    i = int((conditions & 8) / 8)

    carry = self.read_carry()
    accumulator = self.read_accumulator()
    pin10 = self.read_pin10()
    if (i == 0):
        if (carry == 1) or (accumulator == 0) or (pin10 == 0):
            self.PROGRAM_COUNTER = address
    if (i == 1):
        if (carry == 1) or (accumulator != 0) or (pin10 == 1):
            self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 2

    return self.PROGRAM_COUNTER


def isz(self, register: int, address: int):
    """
    Name:           Increment index register skip if zero
    Function:       The content of the designated index register is
                    incremented by 1.
                    The accumulator and carry/link are unaffected.
                    If the result is zero, the next instruction after ISZ is
                    executed.
                    If the result is different from 0, program control is
                    transferred to the instruction located at the 8 bit
                    address AAAA2, AAAA1 on the same page (ROM) where the
                    ISZ instruction is located.
    Syntax:         ISZ
    Assembled:      0111 RRRR
                    AAAA2 AAAA1
    Symbolic:       (RRRR) + 1 --> RRRR,
                    if result = 0 (PH) --> PH, (PM) --> PM, (PL + 2) --> PL
                    if result <> 0  (PH) --> PH, AAAA2 --> PM, `AAAA1 --> PL
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable


    """
    self.increment_register(register)
    if (self.REGISTERS[register] == 0):
        self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 2
    else:
        self.PROGRAM_COUNTER = address

    return None


def fim(self, registerpair: int, value: int):
    """
    Name:           Fetched immediate from ROM
    Function:       The 2nd word represents 8-bits of data
                    which are loaded into the designated index register pair.
    Syntax:         FIM
    Assembled:      0010 RRR0
                    DDDD2  DDDD1
    Symbolic:       DDDD --> RRR0, DDDD1 --> RRR1
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable
    """

    self.insert_registerpair(registerpair, value)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 2
    return self.REGISTERS

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
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
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
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
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
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
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
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.CARRY


def cma(self):
    """
    Name:           Complement Accumulator
    Function:       The content of the accumulator is complemented.
                    The carry/link is unaffected.
    Syntax:         CMA
    Assembled:      1111 0100
    Symbolic:       ~a3 ~a2 ~a1 ~a0 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    self.ACCUMULATOR = self.ones_complement(self.ACCUMULATOR)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def iac(self):
    """
    Name:           Increment accumulator
    Function:       The content of the accumulator is incremented by 1.
    Syntax:         IAC
    Assembled:      1111 0010
    Symbolic:       (ACC) +1 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   No overflow sets the carry/link to 0;
                    overflow sets the carry/link to a 1.
    """

    self.ACCUMULATOR = self.ACCUMULATOR + 1
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def dac(self):
    """
    Name:           Decrement accumulator
    Function:       The content of the accumulator is decremented by 1.
    Syntax:         DAC
    Assembled:      1111 1000
    Symbolic:       (ACC) -1 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   A borrow sets the carry/link to 0;
                    No borrow sets the carry/link to a 1.
    """

    self.ACCUMULATOR = self.ACCUMULATOR + 15
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def ral(self):
    """
    Name:           Rotate left
    Function:       The content of the accumulator and carry/link
                    are rotated left.
    Syntax:         RAL
    Assembled:      1111 0101
    Symbolic:       C0 --> a0, a(i) --> a(i+1), a3 -->CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the highest significant
                    bit of the accumulator.
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
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
    # Add original carry bit
    self.ACCUMULATOR = self.ACCUMULATOR + C0
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def rar(self):
    """
    Name:           Rotate right
    Function:       The content of the accumulator and carry/link
                    are rotated right.
    Syntax:         RAR
    Assembled:      1111 0110
    Symbolic:       a0 --> CY, a(i) --> a(i-1), C0 -->a3
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the lowest significant
                    bit of the accumulator.
    """

    # Store Carry bit
    C0 = self.read_carry()
    # Set carry bit correctly
    if (self.ACCUMULATOR % 2 == 0):
        self.reset_carry()
    else:
        self.set_carry()
    # Shift right
    self.ACCUMULATOR = self.ACCUMULATOR // 2
    # Add carry to high-order bit of accumulator
    self.ACCUMULATOR = self.ACCUMULATOR + (C0 * self.MSB)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def tcc(self):
    """
    Name:           Transmit carry and clear
    Function:       The accumulator is cleared.
                    The least significant position of the accumulator
                    is set to the value of the carry/link.
    Syntax:         TCC
    Assembled:      1111 0111
    Symbolic:       0 --> ACC, (CY) --> a0, 0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the 0.
    """

    self.ACCUMULATOR = 0
    self.ACCUMULATOR = self.read_carry()
    self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def daa(self):
    """
    Name:           Decimal adjust accumulator
    Function:       The accumulator is incremented by 6 if
                    either the carry/link is 1 or if the accumulator
                    content is greater than 9.
    Syntax:         DAA
    Assembled:      1111 1011
    Symbolic:       (ACC) + (0000 or 0110) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is set to a 1 if the result generates
                    a carry, otherwise it is unaffected.
    """

    if (self.read_carry == 1 or self.ACCUMULATOR > 9):
        self.ACCUMULATOR = self.ACCUMULATOR + 6
        if (self.ACCUMULATOR > self.MAX_4_BITS):
            self.ACCUMULATOR = self.MAX_4_BITS - self.MAX_4_BITS
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
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

    if (self.read_carry() == 0):
        self.ACCUMULATOR = 9
    else:
        self.ACCUMULATOR = 10
    self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def kbp(self):
    """
    Name:           Keyboard process
    Function:       A code conversion is performed on the accumulator content,
                    from 1 out of n to binary code.
                    If the accumulator content has more than one bit on, the
                    accumulator will be set to 15.
                    (to indicate error) - conversion table below
    Syntax:         KBP
    Assembled:      1111 1100
    Symbolic:       (ACC) --> KBP, ROM --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is unaffected.


                    (ACC)           (ACC)
                    before          after
                        KBP	  	     KBP
                        0000	---->	0000
                        0001	---->	0001
                        0010	---->	0010
                        0100	---->	0011
                        1000	---->	0100
                        0011	---->	1111    Error
                        0101	---->	1111    Error
                        0110	---->	1111    Error
                        0111	---->	1111    Error
                        1001	---->	1111    Error
                        1010	---->	1111    Error
                        1011	---->	1111    Error
                        1100	---->	1111    Error
                        1101	---->	1111    Error
                        1110	---->	1111    Error
                        1111	---->	1111    Error
    """
    if (self.ACCUMULATOR == 0
        or self.ACCUMULATOR == 1
            or self.ACCUMULATOR == 2):
        return self.ACCUMULATOR

    if (self.ACCUMULATOR == 4):
        self.ACCUMULATOR = 3
        return self.ACCUMULATOR

    if (self.ACCUMULATOR == 8):
        self.ACCUMULATOR = 4
        return self.ACCUMULATOR

    # Error
    self.ACCUMULATOR = 15
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def dcl(self):
    """
    Name:           Designate command line
    Function:       The content of the three least significant accumulator
                    bits is transferred to the command control register
                    within the CPU. This instruction provides RAM bank
                    selection when multiple RAM banks are used.
                    (If no DCL instruction is sent out, RAM Bank number
                    zero is automatically selected after application of at
                    least one RESET). See below for RAM Bank selection table.
                    DCL remains latched until it is changed.
    Syntax:         DCL
    Assembled:      1111 1101
    Symbolic:       a0 --> CM0, a1 --> CM1, a2 --> CM2
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

                    The selection is made according to the following table.
                    (ACC)	CM-RAMi                     Enabled	Bank No.
                    -----	------------------------	------------
                    X000	CM-RAM0	                    Bank 0
                    X001	CM-RAM1	                    Bank 1
                    X010	CM-RAM2	                    Bank 2
                    X100	CM-RAM3	                    Bank 3
                    X011	CM-RAM1, CM-RAM1	        Bank 4
                    X101	CM-RAM1, CM-RAM3	        Bank 5
                    X110	CM-RAM2, CM-RAM3	        Bank 6
                    X111	CM-RAM1, CM-RAM2, CM-RAM3	Bank 7
    """

    ACC = self.ACCUMULATOR
    if (ACC > 7):
        raise InvalidRamBank('RAM bank : ' + str(ACC))

    self.CURRENT_RAM_BANK = ACC
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.CURRENT_RAM_BANK


def wrm(self):
    """
    Name:           Write accumulator into RAM character
    Function:       The accumulator content is written into the previously
                    selected RAM main memory character location.
                    The accumulator and carry/link are unaffected.
    Syntax:         WRM
    Assembled:      1110 0000
    Symbolic:       (ACC) --> M
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    
    value = self.ACCUMULATOR
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    final_address = (crb * self.PAGE_SIZE) + address
    self.RAM[final_address] = value
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.PROGRAM_COUNTER


def wr0(self):
    """
    Name:           Write accumulator into RAM status character 0
    Function:       The content of the accumulator is written into the
                    RAM status character 0 of the previously selected
                    RAM register.
                    The accumulator and the carry/link are unaffected.
    Syntax:         WR0
    Assembled:      1110 0100
    Symbolic:       (ACC) --> MS0
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    value = self.ACCUMULATOR
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.STATUS_CHARACTERS[crb][chip][register][0] = value
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.PROGRAM_COUNTER


def wr1(self):
    """
    Name:           Write accumulator into RAM status character 1
    Function:       The content of the accumulator is written into the
                    RAM status character 1 of the previously selected
                    RAM register.
                    The accumulator and the carry/link are unaffected.
    Syntax:         WR1
    Assembled:      1110 0101
    Symbolic:       (ACC) --> MS1
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    value = self.ACCUMULATOR
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.STATUS_CHARACTERS[crb][chip][register][1] = value
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.PROGRAM_COUNTER


def wr2(self):
    """
    Name:           Write accumulator into RAM status character 2
    Function:       The content of the accumulator is written into the
                    RAM status character 2 of the previously selected
                    RAM register.
                    The accumulator and the carry/link are unaffected.
    Syntax:         WR2
    Assembled:      1110 0110
    Symbolic:       (ACC) --> MS2
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    value = self.ACCUMULATOR
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.STATUS_CHARACTERS[crb][chip][register][2] = value
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.PROGRAM_COUNTER


def wr3(self):
    """
    Name:           Write accumulator into RAM status character 3
    Function:       The content of the accumulator is written into the
                    RAM status character 3 of the previously selected
                    RAM register.
                    The accumulator and the carry/link are unaffected.
    Syntax:         WR3
    Assembled:      1110 0111
    Symbolic:       (ACC) --> MS3
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    value = self.ACCUMULATOR
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.STATUS_CHARACTERS[crb][chip][register][3] = value
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.PROGRAM_COUNTER


def rd0(self):
    """
    Name:           Read RAM status character 0
    Function:       The 4-bits of status character 0 for the previously
                    selected RAM register are transferred to the
                    accumulator.
                    The carry/link and the status character are unaffected.
    Syntax:         RD0
    Assembled:      1110 1100
    Symbolic:       (MS0) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][0]
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def rd1(self):
    """
    Name:           Read RAM status character 1
    Function:       The 4-bits of status character 1 for the previously
                    selected RAM register are transferred to the
                    accumulator.
                    The carry/link and the status character are unaffected.
    Syntax:         RD1
    Assembled:      1110 1101
    Symbolic:       (MS1) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][1]
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def rd2(self):
    """
    Name:           Read RAM status character 2
    Function:       The 4-bits of status character 2 for the previously
                    selected RAM register are transferred to the
                    accumulator.
                    The carry/link and the status character are unaffected.
    Syntax:         RD2
    Assembled:      1110 1101
    Symbolic:       (MS2) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][2]
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def rd3(self):
    """
    Name:           Read RAM status character 3
    Function:       The 4-bits of status character 3 for the previously
                    selected RAM register are transferred to the
                    accumulator.
                    The carry/link and the status character are unaffected.
    Syntax:         RD3
    Assembled:      1110 1111
    Symbolic:       (MS3) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    Bits 1 + 2 = 1 of 4 DATA RAM CHIPS within the DATA RAM BANK previously
                 selected by a DCL instruction
    Bits 3 + 4 = 1 of 4 registers within the DATA RAM CHIP
    Bits 5-8   = Not relevant

    """

    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[self.read_current_ram_bank()]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][3]
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def wmp(self):
    """
    Name:           Write memory port
    Function:       The content of the accumulator is transferred to the
                    RAM output port of the previously selected RAM chip.
                    The data is available on the output pins until a new
                    WMP is executed on the same RAM chip.
                    The content of the ACC and the carry/link are unaffected.
    Syntax:         WMP
    Assembled:      1110 0001
    Symbolic:       (ACC) --> RAM output register
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The LSB bit of the accumulator appears on I/O 0, Pin 16,
                    of the 4002 RAM chip until it is changed.

    There is a 4-bit register on each DATA RAM Chip -  on the base MCS-4
    system (one i4004 CPU, 32 * i4002, and ? * i4001 ) - additionally, a i4003 shift register

    Therefore - 4 chips per bank, 8 banks = 32 addressable memory ports.

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)
    
    Bits 1 + 4 = The port associated with 1 of 4 DATA RAM
                 chips within the DATA RAM bank previously
                 selected by a DCL instruction
    Bits 3 - 8 = Not relevant
    """

    crb = self.read_current_ram_bank()
    chip = int(bin(int(self.COMMAND_REGISTERS[self.read_current_ram_bank()]))[2:].zfill(8)[:2], 2)
    self.RAM_PORT[crb][chip] = self.ACCUMULATOR
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def wrr(self):
    """
    Name:           Write ROM port
    Function:       The content of the accumulator is transferred to the ROM
                    output port of the previously selected ROM chip.
                    The data is available on the output pins until a new WRR
                    is executed on the same chip.
                    The content of the ACC and the carry/link are unaffected.
    Syntax:         WRR
    Assembled:      1110 0010
    Symbolic:       (ACC) --> ROM output lines
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The LSB bit of the accumulator appears on I/O 0, Pin 16,
                    of the 4001 ROM chip until it is changed.
    Notes:          No operation is performed on I/O lines coded as inputs.

    4 chips per bank, 8 banks = 32 addressable ROM ports.

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)

    Bits 1 - 4 = The ROM chip targetted
    Bits 5 - 8 = Not relevant
    """

    crb = self.read_current_ram_bank()
    rom = int(bin(int(self.COMMAND_REGISTERS[crb]))[2:].zfill(8)[:4], 2)
    self.ROM_PORT[rom] = self.ACCUMULATOR
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def wpm(self):
    """
    Name:           Write ROM port
    Function:       The content of the accumulator is transferred to the ROM
                    output port of the previously selected ROM chip.
                    The data is available on the output pins until a new WRR
                    is executed on the same chip.
                    The content of the ACC and the carry/link are unaffected.
    Syntax:         WRR
    Assembled:      1110 0010
    Symbolic:       (ACC) --> ROM output lines
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The LSB bit of the accumulator appears on I/O 0, Pin 16,
                    of the 4001 ROM chip until it is changed.
    Notes:          No operation is performed on I/O lines coded as inputs.

    
    """

    # TODO

    return True
