# Using pytest
# Test the WRR instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest


sys.path.insert(1, '../src')
sys.path.insert(2, '../test')
from hardware.processor import Processor  # noqa
from utils import encode_command_register  # noqa


def test_validate_wrr_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[226]
    known = {"opcode": 226, "mnemonic": "wrr()", "exe": 10.8, "bits": ["1110", '0010'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rom", [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                 10, 11, 12, 13, 14, 15, 0])
def test_wrr_scenario1(rom):
    """Test WRR instruction functionality."""
    import random

    chip_test = Processor()
    chip_base = Processor()

    value = random.randint(0, 15)  # Select a random value

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.set_accumulator(value)
    chip_test.COMMAND_REGISTER = \
        encode_command_register(rom, 0, 0, 'ROM_PORT')
    Processor.wrr(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.set_accumulator(value)
    chip_base.COMMAND_REGISTER = \
        encode_command_register(rom, 0, 0, 'ROM_PORT')
    chip_base.increment_pc(1)
    chip_base.ROM_PORT[rom] = chip_base.ACCUMULATOR

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
