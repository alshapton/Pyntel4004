# Using pytest
# Test the WPM instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')
sys.path.insert(2, '..' + os.sep + 'test')

import pickle  # noqa
import pytest  # noqa


from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import binary_to_decimal, \
    convert_to_absolute_address, \
    convert_decimal_to_n_bit_slices as c2n  # noqa
from utils import encode_command_register  # noqa


def test_validate_wpm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[227]
    known = {"opcode": 227, "mnemonic": "wpm()", "exe": 10.8, "bits": ["1110", "0011"], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rambank", [0, 7])
@pytest.mark.parametrize("chip", [2, 3])
@pytest.mark.parametrize("register", [1, 3])
@pytest.mark.parametrize("address", [2, 5, 3])
def test_wpm_scenario1_write(rambank, chip, register, address):
    """Test WPM instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    """
    This piece of code writes an 8-bit value (consisting of 2 4-bit values)
    from the accumulator in 2 chunks. The setting up of this code and the
    execution of several WPM statements is key to the testing, although much
    has to be set up around those instructions to stage the tests.

    1     FIM        0P    224
    2     SRC        0P          / Select ROM port 14.
    3     LDM        1
    4     WRR                    / Turn on write enable.
    5                            / Set up PRAM address.
    6                            /
    7     FIM        0P    0
    8     SRC        0P          / Select DATA RAM chip 0 register 0.
    9     RD1                    / Read middle 4 bits of address.
    10    XCH        10          / Save in register 10.
    11    RD2                    / Read lowest 4 bits of address.
    12    XCH        11          / Save in register 11.
    13    RD0                    / Read highest 4 bits of address.
    14    FIM        0P    240
    15    SRC        0P          / Select ROM port 15.
    16    WRR                    / Write high address.
    17    SRC        5P          / Write middle + low address (RP5)
    18                           /
    19    LD         2           / High 4 data bits to accumulator.
    20    WPM                    / Write to PRAM
    21    LD         3           / Low 4 data bits to accumulator.
    22    WPM                    / Write to PRAM

    23    FIM        0P    224
    24    SRC        0P          / Select ROM port 14.
    25    CLB
    26    WRR                    / Turn off write enable.
    """

    # Perform the instruction under test:
    # Preamble.....
    chip_test.PROGRAM_COUNTER = 0             # Set PC to be zero
    chip_test.CURRENT_RAM_BANK = rambank      # Set RAM BANK to be the supplied

    chip_base.PROGRAM_COUNTER = 0             # Set PC to be zero
    chip_base.CURRENT_RAM_BANK = rambank      # Set RAM BANK to be the supplied

    register_pair = 5
    reg_pair_first = (register_pair * 2)
    reg_pair_second = reg_pair_first + 1

    # Lines 1 - 4
    chip_test.ROM_PORT[14] = 1                # set the write enable flag

    # Line 7
    chip_test.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')

    address_to_write_to = convert_to_absolute_address(
        chip_test, rambank, chip, register, address)
    chunks = c2n(12, 4, address_to_write_to, 'b')

    # Lines 8 - 10    # Store middle bits in register "reg_pair_first"
    chip_test.STATUS_CHARACTERS[rambank][0][0][1] = \
        binary_to_decimal(str(chunks[1]))
    chip_test.REGISTERS[reg_pair_first] = \
        chip_test.STATUS_CHARACTERS[rambank][0][0][1]

    # Lines 11 - 12   # Store lower bits in register "reg_pair_second"
    chip_test.STATUS_CHARACTERS[rambank][0][0][2] = \
        binary_to_decimal(str(chunks[2]))
    chip_test.REGISTERS[reg_pair_second] = \
        chip_test.STATUS_CHARACTERS[rambank][0][0][2]

    # Lines 13 - 16    # Store higher bits in ROM PORT 15
    chip_test.STATUS_CHARACTERS[rambank][0][0][0] = \
        binary_to_decimal(str(chunks[0]))
    chip_test.ROM_PORT[15] = chip_test.STATUS_CHARACTERS[rambank][0][0][0]

    # Lines 17 - 18
    chip_test.COMMAND_REGISTER = Processor.read_registerpair(chip_test, 5)

    # Lines 19 - 20
    chip_test.set_accumulator(binary_to_decimal(str(chunks[0])))
    Processor.wpm(chip_test)

    # Lines 21 - 22
    chip_test.set_accumulator(binary_to_decimal(str(chunks[2])))
    Processor.wpm(chip_test)

    # Lines 23 - 26
    chip_test.set_accumulator(0)
    chip_test.reset_carry()
    chip_test.ROM_PORT[14] = 0

    # Simulate conditions at end of instruction in base chip
    # Lines 1 - 4
    chip_base.ROM_PORT[14] = 1              # set the write enable flag

    # Line 7
    chip_base.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')

    address_to_write_to = convert_to_absolute_address(
        chip_base, rambank, chip, register, address)
    chunks = c2n(12, 4, address_to_write_to, 'b')

    # Lines 8 - 10    # Store middle bits in register "reg_pair_first"
    chip_base.STATUS_CHARACTERS[rambank][0][0][1] = \
        binary_to_decimal(str(chunks[1]))
    chip_base.REGISTERS[reg_pair_first] = \
        chip_base.STATUS_CHARACTERS[rambank][0][0][1]

    # Lines 11 - 12   # Store lower bits in register "reg_pair_second"
    chip_base.STATUS_CHARACTERS[rambank][0][0][2] = \
        binary_to_decimal(str(chunks[2]))
    chip_base.REGISTERS[reg_pair_second] = \
        chip_base.STATUS_CHARACTERS[rambank][0][0][2]

    # Lines 13 - 16    # Store higher bits in ROM PORT 15
    chip_base.STATUS_CHARACTERS[rambank][0][0][0] = \
        binary_to_decimal(str(chunks[0]))
    chip_base.ROM_PORT[15] = chip_base.STATUS_CHARACTERS[rambank][0][0][0]

    # Lines 17 - 18
    chip_base.COMMAND_REGISTER = Processor.read_registerpair(chip_base, 5)

    # Lines 19 - 20
    chip_base.set_accumulator(binary_to_decimal(str(chunks[0])))
    chip_base.PRAM[address_to_write_to] = chip_base.ACCUMULATOR << 4
    chip_base.RAM[address_to_write_to] = chip_base.ACCUMULATOR << 4
    Processor.flip_wpm_counter(chip_base)
    chip_base.increment_pc(1)

    # Lines 21 - 22
    chip_base.set_accumulator(binary_to_decimal(str(chunks[2])))
    value = chip_base.ACCUMULATOR
    chip_base.PRAM[address_to_write_to] = \
        chip_base.PRAM[address_to_write_to] + value
    chip_base.RAM[address_to_write_to] = \
        chip_base.RAM[address_to_write_to] + value
    Processor.flip_wpm_counter(chip_base)
    chip_base.increment_pc(1)

    # Lines 23 - 26
    chip_base.set_accumulator(0)
    chip_base.reset_carry()
    chip_base.ROM_PORT[14] = 0

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("rambank", [0, 7])
@pytest.mark.parametrize("chip", [2, 3])
@pytest.mark.parametrize("register", [1, 3])
@pytest.mark.parametrize("address", [2, 5, 3])
def test_wpm_scenario1_read(rambank, chip, register, address):
    """Test WPM instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    """
    This piece of code reads an 8-bit value (consisting of 2 4-bit values)
    from the program ram in 2 chunks. The setting up of this code and the
    execution of several WPM statements is key to the testing, although much
    has to be set up around those instructions to stage the tests.

    1     FIM        0P    0
    2     SRC        0P          / Select DATA RAM chip 0 register 0.
    3     RD1                    / Read middle 4 bits of address.
    4     XCH        10          / Save in register 10.
    5     RD2                    / Read lowest 4 bits of address.
    6     XCH        11          / Save in register 11.
    7     RD0                    / Read highest 4 bits of address.
    8     FIM        0P    240
    9     SRC        0P          / Select ROM port 15.
    10    WRR                    / Write high address.
    11    SRC        5P          / Write middle + low address (RP5)

    12    WPM                    / PRAM data to ROM port 14.
    13    WPM                    / PRAM data to ROM port 15.

    14    FIM        0P    224
    15    SRC        0P          / Select ROM port 14.
    16    RDR                    / Read to accumulator
    17    XCH        2           / Save in register 2
    18    INC        0
    19    SRC        0P          / Select ROM port 15
    20    RDR                    / Read to accumulator
    21    XCH        3           / Save in register 2
    """
    # Perform the instruction under test:
    # Preamble.....
    chip_test.PROGRAM_COUNTER = 0             # Set PC to be zero
    chip_test.CURRENT_RAM_BANK = rambank      # Set RAM BANK to be the supplied

    chip_base.PROGRAM_COUNTER = 0             # Set PC to be zero
    chip_base.CURRENT_RAM_BANK = rambank      # Set RAM BANK to be the supplied

    register_pair = 5
    reg_pair_first = (register_pair * 2)
    reg_pair_second = reg_pair_first + 1

    # Lines 1 - 2
    chip_test.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')

    address_to_write_to = convert_to_absolute_address(
        chip_test, rambank, chip, register, address)
    chunks = c2n(12, 4, address_to_write_to, 'b')

    # Lines 3 - 4    # Store middle bits in register "reg_pair_first"
    chip_test.STATUS_CHARACTERS[rambank][0][0][1] = \
        binary_to_decimal(str(chunks[1]))
    chip_test.REGISTERS[reg_pair_first] = \
        chip_test.STATUS_CHARACTERS[rambank][0][0][1]

    # Lines 5 - 6   # Store lower bits in register "reg_pair_second"
    chip_test.STATUS_CHARACTERS[rambank][0][0][2] = \
        binary_to_decimal(str(chunks[2]))
    chip_test.REGISTERS[reg_pair_second] = \
        chip_test.STATUS_CHARACTERS[rambank][0][0][2]

    # Lines 7 - 10   # Store higher bits in ROM PORT 15
    chip_test.STATUS_CHARACTERS[rambank][0][0][0] = \
        binary_to_decimal(str(chunks[0]))
    chip_test.ROM_PORT[15] = chip_test.STATUS_CHARACTERS[rambank][0][0][0]

    # Line 11
    chip_test.COMMAND_REGISTER = Processor.read_registerpair(chip_test, 5)

    # Lines 12 - 13
    Processor.wpm(chip_test)
    Processor.wpm(chip_test)

    # Lines 14 - 16
    # Get the value from ROM port 14 to accumulator
    chip_test.set_accumulator(chip_test.ROM_PORT[14])

    # Line 17
    chip_test.REGISTERS[reg_pair_first] == chip_test.read_accumulator()

    # Lines 18 - 20
    # Get the value from ROM port 15 to accumulator
    chip_test.set_accumulator(chip_test.ROM_PORT[15])

    # Line 21
    chip_test.REGISTERS[reg_pair_second] == chip_test.read_accumulator()

    # Simulate conditions in base chip
    # Lines 1 - 2
    chip_base.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')

    address_to_write_to = convert_to_absolute_address(
        chip_base, rambank, chip, register, address)
    chunks = c2n(12, 4, address_to_write_to, 'b')

    # Lines 3 - 4    # Store middle bits in register "reg_pair_first"
    chip_base.STATUS_CHARACTERS[rambank][0][0][1] = \
        binary_to_decimal(str(chunks[1]))
    chip_base.REGISTERS[reg_pair_first] = \
        chip_base.STATUS_CHARACTERS[rambank][0][0][1]

    # Lines 5 - 6   # Store lower bits in register "reg_pair_second"
    chip_base.STATUS_CHARACTERS[rambank][0][0][2] = \
        binary_to_decimal(str(chunks[2]))
    chip_base.REGISTERS[reg_pair_second] = \
        chip_base.STATUS_CHARACTERS[rambank][0][0][2]

    # Lines 7 - 10   # Store higher bits in ROM PORT 15
    chip_base.STATUS_CHARACTERS[rambank][0][0][0] = \
        binary_to_decimal(str(chunks[0]))
    chip_base.ROM_PORT[15] = chip_base.STATUS_CHARACTERS[rambank][0][0][0]

    # Line 11
    chip_base.COMMAND_REGISTER = Processor.read_registerpair(chip_test, 5)

    # Lines 12 - 13
    chip_base.ROM_PORT[14] = chip_base.PRAM[address_to_write_to] >> 4 << 4
    Processor.flip_wpm_counter(chip_base)
    chip_base.increment_pc(1)
    chip_base.ROM_PORT[15] = chip_base.PRAM[address_to_write_to] << 4 >> 4
    Processor.flip_wpm_counter(chip_base)
    chip_base.increment_pc(1)

    # Lines 14 - 16
    # Get the value from ROM port 14 to accumulator
    chip_base.set_accumulator(chip_base.ROM_PORT[14])

    # Line 17
    chip_base.REGISTERS[reg_pair_first] == chip_base.read_accumulator()

    # Lines 18 - 20
    # Get the value from ROM port 15 to accumulator
    chip_base.set_accumulator(chip_base.ROM_PORT[15])

    # Line 21
    chip_base.REGISTERS[reg_pair_second] == chip_base.read_accumulator()

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
