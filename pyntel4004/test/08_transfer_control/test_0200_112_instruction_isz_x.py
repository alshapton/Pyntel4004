# Using pytest
# Test the ISZ instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa


from hardware.processor import Processor  # noqa
from hardware.suboperation import decimal_to_binary  # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                   11, 12, 13, 14, 15])
def test_validate_instruction(value):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[112 + value]
    known = {"opcode": 112 + value, "mnemonic": "isz(" + str(value) + ",address8)", "exe": 10.8, "bits": ["0111", decimal_to_binary(4,  value)], "words": 2}  # noqa
    assert op == known


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                      11, 12, 13, 14, 15])
@pytest.mark.parametrize("values", [[0, 'Y'], [2, 'Y'], [10, 'Y'], [15, 'N']])
def test_scenario1(values, register):
    """Test ISZ instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    pc = 100
    pcaftjump = 150
    pcaftnojump = 102

    reg = register
    value = values[0]
    if values[1] == 'Y':
        pcaft = pcaftjump
    else:
        pcaft = pcaftnojump

    # Set both chips to initial status
    # Program Counter
    chip_test.PROGRAM_COUNTER = pc
    chip_base.PROGRAM_COUNTER = pc

    # Registers
    chip_test.insert_register(reg, value)
    chip_base.insert_register(reg, value)
    chip_base.increment_register(reg)

    # Perform the instruction under test:
    Processor.isz(chip_test, reg, pcaftjump)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = pcaft

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
