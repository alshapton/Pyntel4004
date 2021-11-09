# Using pytest
# Test the kbp instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import Processor  # noqa


def test_validate_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[252]
    known = {"opcode": 252, "mnemonic": "kbp()", "exe": 10.8, "bits": ["1111", '1100'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 0], [1, 1], [2, 2], [3, 15], [4, 3],
                                    [5, 15], [6, 15], [7, 15], [8, 4],
                                    [9, 15], [10, 15], [11, 15], [12, 15],
                                    [13, 15], [15, 15], [15, 15]])
def test_scenario1(values):
    """Test KPB instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(values[0])

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.set_accumulator(values[1])

    # Carry out the instruction under test
    # Perform a kbp operation

    Processor.kbp(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
