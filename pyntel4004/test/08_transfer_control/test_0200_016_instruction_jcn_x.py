# Using pytest
# Test the JCN instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa

from hardware.suboperation import decimal_to_binary  # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                   11, 12, 13, 14, 15])
def test_validate_instruction(value):
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[16 + value]
    known = {"opcode": 16 + value, "mnemonic": "jcn(" + str(value) + ",address8)", "exe": 21.6, "bits": ["0001", decimal_to_binary(4,  value), "xxxx", "xxxx"], "words": 2}  # noqa
    assert op == known

#        Conditions to check            Values
# PCbef, INV, ACC, CARRY, PIN10, PCaft, ACC, CARRY, PIN10


@pytest.mark.parametrize("values", [[100, 0, 0, 0, 0, 102, 0, 0, 0], [100, 1, 0, 0, 0, 1234, 0, 0, 0],
                                    [100, 0, 0, 0, 1, 1234, 0, 0, 0], [
                                        100, 0, 0, 0, 1, 102, 0, 0, 1],  # Pin10
                                    [100, 1, 0, 0, 1, 102, 0, 0, 0], [
                                        100, 1, 0, 0, 1, 102, 0, 0, 1],  #  Pin10 + invert
                                    [100, 0, 0, 1, 0, 1234, 0, 1, 0], [
                                        100, 0, 0, 1, 0, 102, 0, 1, 0],  # Carry
                                    [100, 1, 0, 1, 0, 102, 0, 1, 0], [
                                        100, 1, 0, 1, 0, 1234, 0, 1, 0],  #  Carry + invert
                                    [100, 0, 1, 0, 0, 1234, 0, 0, 0], [
                                        100, 0, 1, 0, 0, 102, 12, 0, 0],  # Accumulator
                                    [100, 1, 1, 0, 0, 102, 0, 0, 0], [
                                        100, 1, 0, 1, 0, 1234, 12, 0, 0],  # Accumulator + invert
                                    [100, 0, 1, 1, 0, 1234, 13, 1, 0], [
                                        100, 0, 0, 1, 1, 102, 0, 1, 0],  # Combinations
                                    [100, 1, 1, 1, 0, 102, 13, 1, 0], [
                                        100, 1, 0, 1, 1, 1234, 0, 1, 0],  # Combinations + invert
                                    ])
def test_scenario1(values):
    """Test JCN instruction functionality."""

    chip_test = processor()
    chip_base = processor()

    PC = values[0]
    C1 = values[1]
    C2 = values[2]
    C3 = values[3]
    C4 = values[4]
    FA = values[5]

    ACCUMULATOR = values[6]
    CARRY_BIT = values[7]
    TEST_SIGNAL = values[8]

    CONDITION = int((C1 * 8) + (C2 * 4) + (C3 * 2) + C4)
    # Set both chips to initial status

    # Set accumulator value on both chips
    chip_test.set_accumulator(ACCUMULATOR)
    chip_base.set_accumulator(ACCUMULATOR)
    # Set carry bit on both chips
    if CARRY_BIT == 0:
        chip_test.reset_carry()
        chip_base.reset_carry()
    else:
        chip_test.set_carry()
        chip_base.set_carry()
    # Set test signal on both chips
    chip_test.write_pin10(TEST_SIGNAL)
    chip_base.write_pin10(TEST_SIGNAL)

    chip_test.PROGRAM_COUNTER = PC
    chip_base.PROGRAM_COUNTER = PC

    # Perform the instruction under test:
    processor.jcn(chip_test, CONDITION, FA)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = FA

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
    print(CONDITION, chip_base.PROGRAM_COUNTER, chip_test.PROGRAM_COUNTER)
