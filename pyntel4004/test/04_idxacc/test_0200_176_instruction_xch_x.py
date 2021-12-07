# Using pytest
# Test the xch instructions of an instance of an i4004(processor)

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
    op = chip_test.INSTRUCTIONS[176 + register]
    known = {"opcode": 176 + register, "mnemonic": "xch(" + str(register) + ")", "exe": 10.8, "bits": ["1011", decimal_to_binary(4, register)], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7,
                                      8, 9, 10, 11, 12, 13, 14, 15])
def test_scenario1(register):
    """Test XCH instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    rv = random.randint(0, 15)  # Select a random 4-bit value

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(14)
    chip_test.REGISTERS[register] = rv

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.set_accumulator(rv)
    chip_base.REGISTERS[register] = 14

    # Carry out the instruction under test
    # Perform an XCH operation
    Processor.xch(chip_test, register)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()
    assert chip_test.REGISTERS[register] == chip_base.REGISTERS[register]

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
