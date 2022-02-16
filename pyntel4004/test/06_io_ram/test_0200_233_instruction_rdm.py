# Using pytest
# Test the RDM instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')
sys.path.insert(2, '..' + os.sep + 'test')

import pickle  # noqa
import pytest  # noqa


from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import convert_to_absolute_address  # noqa
from utils import encode_command_register  # noqa


def test_validate_rdm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[233]
    known = {"opcode": 233, "mnemonic": "rdm()", "exe": 10.8, "bits": ["1110", '1001'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 1, 0, 7, 3], [1, 3, 1, 6, 4],
                                    [2, 1, 2, 5, 5], [3, 2, 0, 4, 6],
                                    [4, 3, 3, 3, 7], [5, 2, 1, 2, 2],
                                    [6, 0, 3, 1, 1], [7, 2, 2, 0, 0]])
def test_rdm_scenario1(values):
    """Test RDM instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    rambank = values[0]
    chip = values[1]
    register = values[2]
    address = values[3]
    value = values[4]

    # Perform the instruction under test:
    chip_test.CURRENT_RAM_BANK = rambank
    absolute_address = convert_to_absolute_address(
        chip_test, rambank, chip, register, address)
    chip_test.RAM[absolute_address] = value
    chip_test.set_accumulator(0)
    chip_test.COMMAND_REGISTER = \
        encode_command_register(chip, register, address, 'DATA_RAM_CHAR')
    chip_base.COMMAND_REGISTER = chip_test.COMMAND_REGISTER

    Processor.rdm(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.RAM[absolute_address] = value
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank
    chip_base.set_accumulator(value)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
