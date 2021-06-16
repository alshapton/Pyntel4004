# Using pytest
# Test the daa instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor # noqa


def test_validate_instruction():
    '''
    Ensure instruction's characteristics are valid
    '''
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[251]
    known = {"opcode": 251, "mnemonic": "daa()", "exe": 10.8, "bits": ["1111", '1011'], "words": 1} # noqa
    assert(op == known)

@pytest.mark.parametrize("values", [[1, 0, 6, 1], [1, 1, 7, 1],
                                    [1, 2, 8, 1], [1, 3, 9, 1],
                                    [1, 4, 10, 1], [1, 5, 11, 1],
                                    [1, 6, 12, 1], [1, 7, 13, 1],
                                    [1, 8, 14, 1], [1, 9, 15, 1],
                                    [1, 10, 0, 1], [1, 11, 1, 1],
                                    [1, 12, 2, 1], [1, 13, 3, 1],
                                    [1, 14, 4, 1], [1, 15, 5, 1],
                                    [0, 0, 0, 0], [0, 1, 1, 0],
                                    [0, 2, 2, 0], [0, 3, 3, 0],
                                    [0, 4, 4, 0], [0, 5, 5, 0],
                                    [0, 6, 6, 0], [0, 7, 7, 0],
                                    [0, 8, 8, 0], [0, 9, 9, 0],
                                    [0, 10, 0, 1], [0, 11, 1, 1],
                                    [0, 12, 2, 1], [0, 13, 3, 1],
                                    [0, 14, 4, 1], [0, 15, 5, 1]])
def test_scenario1(values):
    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(values[1])
    chip_test.CARRY = values[0]

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.set_accumulator(values[2])
    chip_base.CARRY = values[3]

    # Carry out the instruction under test
    # Perform a daa operation

    processor.daa(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert (chip_test.read_program_counter() ==
            chip_base.read_program_counter())
    assert (chip_test.read_carry() ==
            chip_base.read_carry())
    assert (chip_test.read_accumulator() ==
            chip_base.read_accumulator())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))
