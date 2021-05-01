# Using pytest
# Test the initialisation of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from src.hardware.processor import processor            # noqa
from src.hardware.suboperation import insert_register , decimal_to_binary  # noqa

@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_validate_instruction(register):
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[96 + register]
    known = {"opcode": 96 + register, "mnemonic": "inc(" + str(register) + ")", "exe": 10.8, "bits": ["0110", decimal_to_binary(chip_test,int(register))], "words": 1} # noqa
    assert(op == known)

@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]) # noqa
def test_post_nop_chip(register):
    # Perform the instruction under test:
    # 3 increments of register "register"
    processor.inc(chip_test, register)
    processor.inc(chip_test, register)
    processor.inc(chip_test, register)

    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(3)
    insert_register(chip_test, register, 3)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


chip_base = processor()
chip_test = processor()
