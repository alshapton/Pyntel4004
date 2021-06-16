# Using pytest
# Test the clb instructions of an instance of an i4004(processor)

import sys
import pickle
sys.path.insert(1, '../src')

from hardware.processor import processor # noqa


def test_validate_instruction():
    ''' Ensure instruction's characteristics are valid '''
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[241]
    known = {"opcode": 241, "mnemonic": "clc()", "exe": 10.8, "bits": ["1111", '0001'], "words": 1} # noqa
    assert op == known


def test_scenario1():
    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(14)
    chip_test.set_carry()

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    chip_base.reset_carry()

    # Carry out the instruction under test
    # Perform a CLB operation
    processor.clb(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_carry() == chip_base.read_carry()
    assert chip_test.read_carry() == chip_base.read_carry()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
