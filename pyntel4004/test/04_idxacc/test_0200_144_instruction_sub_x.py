# Using pytest
# Test the sub instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa
import random  # noqa

from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import decimal_to_binary  # noqa
from hardware.suboperations.registers import insert_register  # noqa


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7,
                                      8, 9, 10, 11, 12, 13, 14, 15])
def test_validate_instruction(register):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[144 + register]
    known = {"opcode": 144 + register, "mnemonic": "sub(" + str(register) + ")", "exe": 10.8, "bits": ["1001", Processor.decimal_to_binary(4, register)], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 6, 2, 4, 1], [1, 6, 2, 3, 1]])
def test_scenario1(values):
    """Test SUB instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    rr = random.randint(0, 15)  # Select a random register

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(values[1])
    chip_test.CARRY = values[0]
    chip_test.insert_register(rr, values[2])

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.CARRY = values[4]
    chip_base.set_accumulator(values[3])
    chip_base.insert_register(rr, values[2])

    # Carry out the instruction under test
    # Perform a SUB operation
    Processor.sub(chip_test, rr)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_carry() == chip_base.read_carry()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
