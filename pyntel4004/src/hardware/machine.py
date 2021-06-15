
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

from hardware.instructions.accumulator import clb, clc, cma, cmc, iac, \
     daa, dac, kbp, ral, rar, stc, tcc, tcs  # noqa
from hardware.instructions.idx import inc, fin  # noqa
from hardware.instructions.idxacc import add, ld, sub, xch # noqa
from hardware.instructions.immediate import fim, ldm # noqa
from hardware.instructions.memory_select import dcl, src # noqa
from hardware.instructions.nop import nop  # noqa

#
# Abbreviations used in the descriptions of each instruction's actions:
#
#        (    )	    the content of
#        -->	    is transferred to
#        ACC	    Accumulator (4-bit)
#        CY	        Carry/link Flip-Flop
#        ACBR	    Accumulator Buffer Register (4-bit)
#        RRRR	    Index register address
#        RPn	    Index register pair address
#        PL	        Low order program counter Field (4-bit)
#        PM	        Middle order program counter Field (4-bit)
#        PH	        High order program counter Field (4-bit)
#        ai	        Order i content of the accumulator
#        CMi	    Order i content of the command register
#        M	        RAM main character location
#        MSi	    RAM status character i
#        DB (T)	    Data bus content at time T
#        Stack	    The 3 registers in the address register
#                   other than the program counter
#
# Additional Abbreviations:
#        ~           Inverse (1's complement)
#        .           logical OR
#

# Operators

# One Word Machine Instructions


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

# 2-word Instructions


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
    self.PROGRAM_COUNTER = address - 1
    return self.PROGRAM_COUNTER


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
    address = self.COMMAND_REGISTER
    final_address = (crb * self.PAGE_SIZE) + address
    self.RAM[final_address] = value
    self.increment_pc(2)
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
    self.write_ram_status(0)
    self.increment_pc(1)
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
    self.write_ram_status(1)
    self.increment_pc(1)
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
    self.write_ram_status(2)
    self.increment_pc(1)
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
    self.write_ram_status(3)
    self.increment_pc(1)
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
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][0]
    self.increment_pc(1)
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
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][1]
    self.increment_pc(1)
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
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][2]
    self.increment_pc(1)
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
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][3]
    self.increment_pc(1)
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
    chip = int(bin(int(self.COMMAND_REGISTER))
               [2:].zfill(8)[:2], 2)
    self.RAM_PORT[crb][chip] = self.ACCUMULATOR
    self.increment_pc(1)
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
    rom = int(bin(int(self.COMMAND_REGISTER))[2:].zfill(8)[:4], 2)
    self.ROM_PORT[rom] = self.ACCUMULATOR
    self.increment_pc(1)
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
    from hardware.suboperation import flip_wpm_counter
    from hardware.reads import read_wpm_counter

    address = self.COMMAND_REGISTER

    # Get the value of the WPM Counter
    wpm_counter = read_wpm_counter(self)

    if self.ROM_PORT[14] == 1:
        # Write enabled, so store
        value = self.ACCUMULATOR
        if wpm_counter == 'LEFT':
            value = self.ACCUMULATOR << 4
            self.PRAM[address] = value
        if wpm_counter == 'RIGHT':
            value = self.ACCUMULATOR
            self.PRAM[address] = self.PRAM[address] + value

    if self.ROM_PORT[14] != 1:
        # read
        if wpm_counter == 'LEFT':
            self.ROM_PORT[14] = self.PRAM[address] >> 4 << 4
        if wpm_counter == 'RIGHT':
            value = self.ACCUMULATOR
            self.ROM_PORT[14] = self.PRAM[address] << 4 >> 4

    flip_wpm_counter(self)

    self.increment_pc(2)
    return True


def rdr(self):
    """
    Name:           Read ROM Port
    Function:       The ROM port specified by the last SRC instruction is read.
                    When using the 4001 ROM,each of the 4 lines of the port may
                    be an input or an output line; the data on the input lines
                    is transferred to the corresponding bits of the
                    accumulator.
                    Any output lines cause either a 0 or a 1 to be transferred
                    to the corresponding bits of the accumulator.
                    Whether a 0 or a 1 is transferred is a function of the
                    hardware, not under control of the programmer. (See Note 3)
                    The Carry bit is unaffected.
    Syntax:         RDR
    Assembled:      1110 1010
    Symbolic:       (ROM input lines) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.

    Notes:  1       The i4001 chip has a 256-byte ROM (256 8-bit program
                    instructions), and one built-in 4-bit I/O port.
                    The MCS-4 has 16 i4001 ROM chips.

            2       On the INTELLEC 4, a ROM port may be used for either
                    input or output. If programs tested on the INTELLEC 4 are
                    to be run later with a 4001 ROM I must be careful not to
                    use one port for both functions.

            3       On the physical devices, if the leftmost I/O line is an
                    output line and the remaining I/O lines are input lines
                    containing 010B, the accumulator will contain either
                    1010B or O010B.
                    This software implementation of the i4004 will ALWAYS
                    return the values of the output lines as-is.
    """
    rom = self.COMMAND_REGISTER >> 4
    self.ACCUMULATOR = self.ROM_PORT[rom]
    self.increment_pc(1)
    return self.ACCUMULATOR


def rdm(self):
    """
    Name:           Read Data RAM data character
    Function:       The content of the previously selected RAM main memory
                    character is transferred to the accumulator
                    The carry/link is unaffected.
                    The 4-bit data in memory is unaffected.
    Syntax:         RDM
    Assembled:      1110 1001
    Symbolic:       (M) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    """
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))
               [2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    absolute_address = (crb * self.RAM_BANK_SIZE) + \
                       (chip * self.RAM_CHIP_SIZE) + \
                       (register * self.RAM_REGISTER_SIZE) + address
    self.ACCUMULATOR = self.RAM[absolute_address]
    self.increment_pc(1)
    return self.ACCUMULATOR


def adm(self, register: int):
    """
    Name:           Add from memory with carry
    Function:       The DATA RAM data character specified by the
                    last SRC instruction, plus the carry bit, are
                    added to the accumulator.
                    The data character is unaffected.
    Syntax:         ADM
    Assembled:      1110 1000
    Symbolic:       (M) + (ACC) + (CY) --> ACC, CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is set to 1 if a sum greater than
                    MAX_4_BITS was generated to indicate a carry out;
                    otherwise, the carry/link is set to 0.
    """
    from hardware.suboperation import check_overflow

    # Get value
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))
               [2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    absolute_address = (crb * self.RAM_BANK_SIZE) + \
                       (chip * self.RAM_CHIP_SIZE) + \
                       (register * self.RAM_REGISTER_SIZE) + address
    # Perform addition
    self.ACCUMULATOR = (self.ACCUMULATOR + self.RAM[absolute_address] +
                        self.read_carry())
    # Check for carry bit set/reset when an overflow is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    check_overflow(self)
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def sbm(self, register: int):
    """
    Name:           Subtract DATA RAM from memory with borrow
    Function:       The value of the DATA RAM character specified
                    by the last SRC instruction is subtracted from
                    the accumulator with borrow.
                    The data character is unaffected.
    Syntax:         SDM
    Assembled:      1110 1000
    Symbolic:       (M) + (ACC) + (CY) --> ACC, CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   This instruction sets the carry bit if the result
                    generates no borrow, and resets the carry bit if
                    the result generates a borrow.
    Notes:  1       A borrow from the previous subtraction is indicated
                    by the carry bit being equal to one at the beginning
                    of this instruction.

            2       No borrow from the previous subtraction is indicated
                    by the carry bit being equal to zero at the beginning
                    of this instruction.

            3       The subtract with borrow operation is actually
                    performed by complementing each bit of the data
                    character and adding the resulting value plus
                    the complement of the carry bit to the accumulator.

            4       When this instruction is used to subtract numbers
                    greater than 4 bits in lengthJ the carry bit must
                    be complemented by the program between each required
                    subtraction operation.
    """
    from hardware.suboperation import check_overflow

    # Get value
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTER
    chip = int(bin(int(address))
               [2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    absolute_address = (crb * self.RAM_BANK_SIZE) + \
                       (chip * self.RAM_CHIP_SIZE) + \
                       (register * self.RAM_REGISTER_SIZE) + address
    value = self.RAM[absolute_address]

    # Perform addition
    value_complement = int(self.ones_complement(value, 4), 2)
    carry_complement = self.read_complement_carry()

    self.ACCUMULATOR = (self.ACCUMULATOR + value_complement +
                        carry_complement)
    # Check for carry bit set/reset when an overflow is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    check_overflow(self)
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY
