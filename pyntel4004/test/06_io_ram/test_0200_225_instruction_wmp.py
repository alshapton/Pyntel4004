# Using pytest
# Test the WPM instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest


sys.path.insert(1, '../src')
sys.path.insert(1, '../test')

from hardware.processor import Processor  # noqa
from utils import encode_command_register  # noqa


def test_validate_wmp_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[225]
    known = {"opcode": 225, "mnemonic": "wmp()", "exe": 10.8, "bits": ["1110", '0001'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rambank", [1, 2, 3, 4, 5, 6, 7, 0])
@pytest.mark.parametrize("chip", [1, 2, 3, 0])
def test_wmp_scenario1(rambank, chip):
    """Test WMP instruction functionality."""
    import random

    chip_test = Processor()
    chip_base = Processor()

    value = random.randint(0, 15)  # Select a random value

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.CURRENT_RAM_BANK = rambank
    chip_test.set_accumulator(value)
    chip_test.COMMAND_REGISTER = \
        encode_command_register(chip, 0, 0, 'RAM_PORT')
    Processor.wmp(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.set_accumulator(value)
    chip_base.COMMAND_REGISTER = \
        encode_command_register(chip, 0, 0, 'RAM_PORT')
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank
    chip_base.RAM_PORT[rambank][chip] = chip_base.ACCUMULATOR

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
