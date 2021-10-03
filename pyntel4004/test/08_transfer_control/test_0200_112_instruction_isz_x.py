# Using pytest
# Test the ISZ instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.suboperation import decimal_to_binary  # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
def test_validate_instruction(value):
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[112 + value]
    known = {"opcode": 112 + value, "mnemonic": "isz(" + str(value) + ",address8)", "exe": 10.8, "bits": ["0111", decimal_to_binary(4,  value)], "words": 2}  # noqa
    assert op == known


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
@pytest.mark.parametrize("values", [[0, 'Y'], [2, 'Y'], [10, 'Y'], [15, 'N']])
def test_scenario1(values, register):
    """Test ISZ instruction functionality."""
    from hardware.processor import processor

    chip_test = processor()
    chip_base = processor()

    PC = 100
    PCaftjump = 150
    PCaftnojump = 102

    REGISTER = register
    VALUE = values[0]
    if values[1] == 'Y':
        PCaft = PCaftjump
    else:
        PCaft = PCaftnojump

    # Set both chips to initial status
    # Program Counter
    chip_test.PROGRAM_COUNTER = PC
    chip_base.PROGRAM_COUNTER = PC

    # Registers
    chip_test.insert_register(REGISTER, VALUE)
    chip_base.insert_register(REGISTER, VALUE)
    chip_base.increment_register(REGISTER)

    # Perform the instruction under test:
    processor.isz(chip_test, REGISTER, PCaftjump)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = PCaft

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
