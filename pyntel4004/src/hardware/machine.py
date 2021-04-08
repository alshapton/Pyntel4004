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

from hardware.instructions.nop import nop  # noqa
from hardware.instructions.idx import inc, fin  # noqa
from hardware.instructions.accumulator import clb, clc, iac, cmc, \
     cma, ral, rar, tcc, dac, tcs, stc, daa, kbp  # noqa

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
    system (one i4004 CPU, 32 * i4002, and ? * i4001 ) - additionally, a i4003
    shift register.

    Therefore - 4 chips per bank, 8 banks = 32 addressable memory ports.

    An address set by the previous SRC instruction is interpreted as follows:

    (Bits in this order : 12345678)

    Bits 1 + 4 = The port associated with 1 of 4 DATA RAM
                 chips within the DATA RAM bank previously
                 selected by a DCL instruction
    Bits 3 - 8 = Not relevant
    """

    crb = self.read_current_ram_bank()
    chip = int(bin(int(self.COMMAND_REGISTERS[self.read_current_ram_bank()]))
               [2:].zfill(8)[:2], 2)
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
    Name:           Write program RAM
    Function:       This is a special instruction which may be used to write
                    the contents of the accumulator into a half byte of
                    program RAM, or read the contents of a half byte of program
                    RAM into a ROM input port where it can be accessed by a
                    program.
                    The Carry bit is unaffected.
    Syntax:         WPM
    Assembled:      1110 0011
    Symbolic:       (A) --> (PRAM)
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.

    Notes:  1       Two WPM instructions must always appear in close
                    succession; that is, each time one WPM instruction
                    references a half byte of program RAM as indicated by an
                    SRC address, another WPM must access the other half byte
                    before the SRC address is altered. An internal counter
                    keeps track of which half-byte is being accessed. If only
                    one WPM occurs, this counter will be out of sync with the
                    program and errors will occur. In this situation, a RESET
                    pulse must be used to re-initialize the machine.

            2       A WPM instruction requires an SRC address to access program
                    RAM. Whenever a WPM is executed, the DATA RAM which happens
                    to correspond to this SRC address will also be written.
                    If data needed later in the program is being held in such
                    a DATA RAM, the programmer must save it elsewhere before
                    executing the WPM instruction.


    """

    from suboperation import flip_wpm_counter
    from reads import read_wpm_counter

    # address = self.read_registerpair(registerpair)
    # self.COMMAND_REGISTERS[self.read_current_ram_bank()] = address

    # TODO
    if (self.ROM_PORT[14] == 1):
        # Write enabled
        pass

    if (self.ROM_PORT[14] == 0):
        # read
        pass

    # Get the value of the WPM Counter
    wpm_counter = read_wpm_counter()

    if (wpm_counter == 'LEFT'):
        pass
    if (wpm_counter == 'RIGHT'):
        pass
    if (wpm_counter not in ['LEFT', 'RIGHT']):
        pass  # raise error

    # Finally, flip the WPM Counter
    flip_wpm_counter()

    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return True
