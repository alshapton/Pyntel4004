# Using pytest
# Test the ral instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from src.hardware.processor import processor # noqa


def test_validate_instruction():
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[246]
    known = {"opcode": 246, "mnemonic": "rar()", "exe": 10.8, "bits": ["1111", '0110'], "words": 1} # noqa
    assert(op == known)

@pytest.mark.parametrize("values", [[6, 1, 11, 0], [6, 0, 3, 0],
                                    [15, 1, 15, 1], [15, 0, 7, 1]])
def test_scenario1(values):
    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(values[0])
    chip_test.CARRY = values[1]

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.set_accumulator(values[2])
    chip_base.CARRY = values[3]

    # Carry out the instruction under test
    # Perform a RAR operation

    processor.rar(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert (chip_test.read_program_counter() ==
            chip_base.read_program_counter())
    assert (chip_test.read_accumulator() ==
            chip_base.read_accumulator())
    assert (chip_test.read_carry() ==
            chip_base.read_carry())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))
