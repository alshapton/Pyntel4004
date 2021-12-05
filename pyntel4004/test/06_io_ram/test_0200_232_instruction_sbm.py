# Using pytest
# Test the SBM instruction of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')
sys.path.insert(2, '..' + os.sep + 'test')

import pickle  # noqa
import pytest  # noqa

from hardware.processor import Processor  # noqa
from hardware.suboperation import convert_to_absolute_address, \
    ones_complement  # noqa
from utils import encode_command_register  # noqa


def test_validate_sbm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[232]
    known = {"opcode": 232, "mnemonic": "sbm()", "exe": 10.8, "bits": ["1110", "0110"], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rambank", [0, 1])
@pytest.mark.parametrize("chip", [0, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
@pytest.mark.parametrize("address", [0, 1, 2, 7])
@pytest.mark.parametrize("value", [0, 1, 6, 7])
@pytest.mark.parametrize("accumulator", [0, 1, 7])
@pytest.mark.parametrize("carry", [0, 1])
def test_adm_scenario1(rambank, chip, register, address, value,
                       accumulator, carry):
    """Test ADM instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    cr = encode_command_register(chip, register, address, 'DATA_RAM_CHAR')

    chip_test.CARRY = carry
    chip_test.COMMAND_REGISTER = cr

    chip_test.CURRENT_RAM_BANK = rambank
    absolute_address = convert_to_absolute_address(
        chip_test, rambank, chip, register, address)
    chip_test.RAM[absolute_address] = value
    chip_test.set_accumulator(accumulator)

    Processor.sbm(chip_test)

    # Simulate conditions at end of instruction in base chip

    chip_base.CARRY = carry
    chip_base.COMMAND_REGISTER = cr
    absolute_address = convert_to_absolute_address(
        chip_base, rambank, chip, register, address)
    chip_base.RAM[absolute_address] = value
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank
    chip_base.set_accumulator(accumulator)
    value_complement = int(ones_complement(value, 4), 2)
    carry_complement = chip_base.read_complement_carry()
    chip_base.ACCUMULATOR = (chip_base.ACCUMULATOR + value_complement +
                             carry_complement)
    Processor.check_overflow(chip_base)
    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
