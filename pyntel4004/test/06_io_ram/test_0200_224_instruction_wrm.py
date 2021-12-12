# Using pytest
# Test the WRM instructions of an instance of an i4004(processor)


# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')
sys.path.insert(2, '..' + os.sep + 'src')

<<<<<<< HEAD
from hardware.suboperation import convert_to_absolute_address, \
    encode_command_register
sys.path.insert(1, '../src')
=======
import pickle  # noqa
import pytest  # noqa
>>>>>>> 0.0.1-beta.2

from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import convert_to_absolute_address  # noqa
from utils import encode_command_register  # noqa


def test_validate_wrm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[224]
    known = {"opcode": 224, "mnemonic": "wrm()", "exe": 10.8, "bits": ["1110", '0000'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rambank", [0, 1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("chip", [0, 1, 2, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
@pytest.mark.parametrize("address", [7, 6, 5, 4, 3, 2, 1, 0])
def test_wrm_scenario1(rambank, chip, register, address):
    """Test WRM instruction functionality."""
    import random

    chip_test = Processor()
    chip_base = Processor()

    value = random.randint(0, 15)  # Select a random value

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.CURRENT_RAM_BANK = rambank
    absolute_address = convert_to_absolute_address(
        chip_test, rambank, chip, register, address)
    chip_test.set_accumulator(value)
    chip_test.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')
    Processor.wrm(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.RAM[absolute_address] = value
    chip_base.set_accumulator(value)
    chip_base.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
