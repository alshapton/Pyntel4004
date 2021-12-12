# Using pytest
# Test the cmc instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa

from hardware.processor import Processor  # noqa


def test_validate_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[243]
    known = {"opcode": 243, "mnemonic": "cmc()", "exe": 10.8, "bits": ["1111", '0011'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 1], [1, 0]])
def test_scenario1(values):
    """Test CMC instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.CARRY = values[0]

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.CARRY = values[1]

    # Carry out the instruction under test
    # Perform a CMC operation

    Processor.cmc(chip_test)
    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_carry() == chip_base.read_carry()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
