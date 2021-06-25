# Using pytest
# Test the dac instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa


def test_validate_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[248]
    known = {"opcode": 248, "mnemonic": "dac()", "exe": 10.8, "bits": ["1111", '1000'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1],
                                    [6, 1], [7, 1], [8, 1], [9, 1], [10, 1],
                                    [11, 1], [12, 1], [13, 1], [14, 1], [15, 1], ])  # noqa
def test_scenario1(values):
    """Test DAC instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(values[0])

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    ACC = values[0] + 15

    if ACC > 8:
        chip_base.set_accumulator(8)
    else:
        chip_base.set_accumulator(ACC - 1)
    chip_base.increment_pc(1)
    chip_base.CARRY = values[1]

    # Carry out the instruction under test
    # Perform a DAC operation

    processor.dac(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()
    assert chip_test.read_carry() == chip_base.read_carry()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
