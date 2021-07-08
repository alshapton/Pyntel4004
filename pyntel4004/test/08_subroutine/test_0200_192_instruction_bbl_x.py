# Using pytest
# Test the BBL instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.suboperation import decimal_to_binary, write_to_stack  # noqa
from hardware.exceptions import ValueOutOfRangeForStack  # noqa


@pytest.mark.parametrize("increment", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                       12, 13, 14, 15])
def test_validate_instruction(increment):
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[192 + increment]
    known = {"opcode": 192 + increment, "mnemonic": "bbl(" + str(increment) + ")", "exe": 10.8, "bits": ["1100", decimal_to_binary(4, increment)], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                   12, 13, 14, 15])
def test_bbl_scenario1(value):
    """Test BBL instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    '''
    chip_base is where I want the end conditions to be constructed by me
    chip_test is where I want the start conditions to be managed by me, and the
    bbl instruction to manipulate and be compared with chip_base

    location 300
    jms 400 (pc = 400) (1)
            (pc = 302) (3) - end

    location 400
    bbl value (pc = 400) (2)

    '''
    PC = 300

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 300
    chip_base.write_to_stack(chip_base.PROGRAM_COUNTER + 2)
    chip_base.PROGRAM_COUNTER = 302  # Return
    chip_base.ACCUMULATOR = value
    chip_base.STACK_POINTER = 2

    # Set up conditions in test chip
    chip_test.PROGRAM_COUNTER = 300
    chip_test.write_to_stack(chip_test.PROGRAM_COUNTER + 2)

    # Perform the instruction under test:
    # Return from a subroutine and load a value into the accumulator
    processor.bbl(chip_test, value)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.PROGRAM_COUNTER == PC + 2
    assert chip_test.STACK_POINTER == 2
    assert chip_test.STACK[chip_test.STACK_POINTER] == 302  # Return

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
