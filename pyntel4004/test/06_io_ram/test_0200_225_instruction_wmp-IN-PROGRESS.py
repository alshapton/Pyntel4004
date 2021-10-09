# Using pytest
# Test the WPM instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest

from hardware.suboperation import decimal_to_binary, binary_to_decimal
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa


def test_validate_wmp_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[225]
    known = {"opcode": 225, "mnemonic": "wmp()", "exe": 10.8, "bits": ["1110", '0001'], "words": 1}  # noqa
    assert op == known


'''
@pytest.mark.parametrize("rambank", [0, 1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("chip", [0, 1, 2, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
@pytest.mark.parametrize("address", [7, 6, 5, 4, 3, 2, 1, 0])
def test_wrm_scenario1(rambank, chip, register, address):
    """Test WRM instruction functionality."""
    import random

    chip_test = processor()
    chip_base = processor()

    value = random.randint(0, 15)  # Select a random value

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0
    chip_test.CURRENT_RAM_BANK = rambank
    absolute_address = (rambank * chip_test.RAM_BANK_SIZE) + \
        (chip * chip_test.RAM_CHIP_SIZE) + \
        (register * chip_test.RAM_REGISTER_SIZE) + address
    chip_test.set_accumulator(value)
    b_chip = decimal_to_binary(2, chip)
    b_register = decimal_to_binary(2, register)
    b_address = decimal_to_binary(4, address)
    chip_test.COMMAND_REGISTER = binary_to_decimal(
        b_chip + b_register + b_address)

    processor.wrm(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.RAM[absolute_address] = value
    chip_base.set_accumulator(value)
    chip_base.COMMAND_REGISTER = binary_to_decimal(decimal_to_binary(2, chip) + \
                                                   decimal_to_binary(2, register) + decimal_to_binary(4, address))
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

'''