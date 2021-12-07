##########################################################################
#                         _ _ _   __   __  _ _                           #
#                        (_) | | /  \ /  \| | |                          #
#                        | |_  _| () | () |_  _|                         #
#                        |_| |_| \__/ \__/  |_|                          #
#                                                                        #
#                     ___ ___    ___    _   __  __                       #
#                    |_ _/ _ \  | _ \  /_\ |  \/  |                      #
#                     | | (_) | |   / / _ \| |\/| |                      #
#                    |___\___/  |_|_\/_/ \_\_|  |_|                      #
#                                                                        #
##########################################################################

"""
Commands in this module.

            RDM -   READ DATA RAM DATA CHARACTER
            RDn -   READ DATA RAM STATUS CHARACTER
            RDR -   READ DATA ROM PORT
            WRM -   WRITE DATA RAM CHARACTER
            WRn -   WRITE DATA RAM STATUS CHARACTER
            WMP -   WRITE RAM PORT
            WRR -   WRITE ROM PORT
            ADM -   ADD DATA RAM TO ACCUMULATOR WITH CARRY
            SBM -   SUBTRACT DATA RAM FROM ACCUMULATOR WITH BORROW
            WPM -   WRITE PROGRAM RAM


 Abbreviations used in the descriptions of each instruction's actions:

            (    )      the content of
            -->         is transferred to
            ACC	        Accumulator (4-bit)
            CY	        Carry/link Flip-Flop
            ACBR	    Accumulator Buffer Register (4-bit)
            RRRR	    Index register address
            RPn	        Index register pair address
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

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

# Import typing library
from typing import Tuple  # noqa

from hardware.suboperations.utility import convert_to_absolute_address, \
    decimal_to_binary, ones_complement  # noqa
from hardware.suboperations.other import decode_command_register  # noqa
from hardware.suboperations.accumulator import check_overflow  # noqa
from hardware.suboperations.ram import rdx  # noqa
from hardware.suboperations.wpm import flip_wpm_counter, read_wpm_counter  # noqa


def rdm(self) -> int:
    """
    Name:           Read Data RAM data character.

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
    chip, register, address = \
        decode_command_register(self.COMMAND_REGISTER, 'DATA_RAM_CHAR')
    absolute_address = convert_to_absolute_address(
        self, crb, chip, register, address)
    self.ACCUMULATOR = self.RAM[absolute_address]
    self.increment_pc(1)
    return self.ACCUMULATOR


def rd0(self) -> int:
    """
    Name:           Read RAM status character 0.

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
    return rdx(self, 0)


def rd1(self) -> int:
    """
    Name:           Read RAM status character 1.

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
    return rdx(self, 1)


def rd2(self) -> int:
    """
    Name:           Read RAM status character 2.

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
    return rdx(self, 2)


def rd3(self) -> int:
    """
    Name:           Read RAM status character 3.

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
    return rdx(self, 3)


def rdr(self) -> int:
    """
    Name:           Read ROM Port.

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
                    to be run later with a 4001 ROM the programmer must be
                    careful not to use one port for both functions.

            3       On the physical devices, if the leftmost I/O line is an
                    output line and the remaining I/O lines are input lines
                    containing 010B, the accumulator will contain either
                    1010B or 0010B.

    Implementation  This software implementation of the i4004 will ALWAYS
                    return the values of the output lines as-is.
    """
    rom, _unused1, _unused2 = \
        decode_command_register(self.COMMAND_REGISTER, 'ROM_PORT')
    self.ACCUMULATOR = self.ROM_PORT[rom]
    self.increment_pc(1)
    return self.ACCUMULATOR


def wrm(self) -> int:
    """
    Name:           Write accumulator into RAM character.

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
    chip, register, address = \
        decode_command_register(self.COMMAND_REGISTER, 'DATA_RAM_CHAR')
    absolute_address = convert_to_absolute_address(
        self, crb, chip, register, address)
    self.RAM[absolute_address] = value
    self.increment_pc(1)
    return self.PROGRAM_COUNTER


def wr0(self) -> int:
    """
    Name:           Write accumulator into RAM status character 0.

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


def wr1(self) -> int:
    """
    Name:           Write accumulator into RAM status character 1.

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


def wr2(self) -> int:
    """
    Name:           Write accumulator into RAM status character 2.

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


def wr3(self) -> int:
    """
    Name:           Write accumulator into RAM status character 3.

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


def wmp(self) -> int:
    """
    Name:           Write memory port.

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

    Bits 1 - 2 = The port associated with 1 of 4 DATA RAM
                 chips within the DATA RAM bank previously
                 selected by a DCL instruction
    Bits 3 - 8 = Not relevant
    """
    crb = self.read_current_ram_bank()
    chip, _unused1, _unused2 = \
        decode_command_register(self.COMMAND_REGISTER, 'RAM_PORT')
    self.RAM_PORT[crb][chip] = self.ACCUMULATOR
    self.increment_pc(1)
    return self.ACCUMULATOR


def wrr(self) -> int:
    """
    Name:           Write ROM port.

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
    rom, _unused1, _unused2 = \
        decode_command_register(self.COMMAND_REGISTER, 'ROM_PORT')
    self.ROM_PORT[rom] = self.ACCUMULATOR
    self.increment_pc(1)
    return self.ACCUMULATOR


def adm(self) -> Tuple[int, int]:
    """
    Name:           Add from memory with carry.

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
    # Get value
    crb = self.read_current_ram_bank()
    chip, register, address = \
        decode_command_register(self.COMMAND_REGISTER, 'DATA_RAM_CHAR')
    absolute_address = convert_to_absolute_address(
        self, crb, chip, register, address)
    # Perform addition
    self.ACCUMULATOR = (self.ACCUMULATOR + self.RAM[absolute_address] +
                        self.read_carry())
    # Check for carry bit set/reset when an overflow is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    check_overflow(self)
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def sbm(self) -> Tuple[int, int]:
    """
    Name:           Subtract DATA RAM from memory with borrow.

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
    # Get value
    crb = self.read_current_ram_bank()
    chip, register, address = \
        decode_command_register(self.COMMAND_REGISTER, 'DATA_RAM_CHAR')
    absolute_address = convert_to_absolute_address(
        self, crb, chip, register, address)
    value = self.RAM[absolute_address]

    # Perform addition
    value_complement = int(ones_complement(value, 4), 2)
    carry_complement = self.read_complement_carry()
    self.ACCUMULATOR = (self.ACCUMULATOR + value_complement +
                        carry_complement)
    # Check for carry bit set/reset when an overflow is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    check_overflow(self)
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def wpm(self) -> Tuple[int, int]:
    """
    Name:           Write program RAM.

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
    chip, register, addr = decode_command_register(
        decimal_to_binary(8, self.COMMAND_REGISTER),
        'DATA_RAM_CHAR')
    rambank = self.read_current_ram_bank()
    address = convert_to_absolute_address(self, rambank, chip, register, addr)
    # Get the value of the WPM Counter
    wpm_counter = read_wpm_counter(self)

    # Writing
    if self.ROM_PORT[14] == 1:
        # Write enabled, so store
        value = self.ACCUMULATOR
        if wpm_counter == 'LEFT':
            print(wpm_counter)
            value = self.ACCUMULATOR << 4
            self.PRAM[address] = value
            self.RAM[address] = value
        if wpm_counter == 'RIGHT':
            value = self.ACCUMULATOR
            self.RAM[address] = self.RAM[address] + value
            self.PRAM[address] = self.PRAM[address] + value

    # Reading
    if self.ROM_PORT[14] != 1:
        # read
        if wpm_counter == 'LEFT':
            self.ROM_PORT[14] = self.PRAM[address] >> 4 << 4
        if wpm_counter == 'RIGHT':
            value = self.ACCUMULATOR
            self.ROM_PORT[15] = self.PRAM[address] << 4 >> 4

    flip_wpm_counter(self)

    self.increment_pc(1)

    return self.ROM_PORT[14], self.ROM_PORT[15]
