# Using pytest
# Test the ADM instruction of an instance of an i4004(processor)

from utils import is_same
from hardware.suboperation import insert_registerpair
import sys
import pickle
import pytest
sys.path.insert(1, '../src')
sys.path.append('../test')

from hardware.processor import processor  # noqa
from hardware.exceptions import InvalidRamBank  # noqa
from utils import is_same  # noqa


def test_validate_adm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[235]
    known = {"opcode": 235, "mnemonic": "adm()", "exe": 10.8, "bits": ["1110", '1000'], "words": 1}  # noqa
    assert op == known


<<<<<<< HEAD
@pytest.mark.parametrize("values", [[0, 1, 0, 7, 3], [1, 3, 1, 6, 4],
                                    [2, 3, 2, 5, 5], [3, 2, 3, 4, 6],
                                    [4, 3, 2, 3, 7], [5, 2, 1, 2, 2],
=======
@pytest.mark.parametrize("values", [[0, 1, 0, 7, 3], [1, 3, 1, 6, 4], [2, 3, 2, 5, 5],
                                    [3, 2, 3, 4, 6], [4, 3, 2, 3, 7], [
                                        5, 2, 1, 2, 2],
>>>>>>> test-opcode-235-adm
                                    [6, 0, 0, 1, 1], [7, 2, 2, 0, 0]])
def test_adm_scenario1(values):
    """Test ADM instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    rambank = values[0]
    chip = values[1]
    register = values[2]
    address = values[3]
    value = values[4]
    accumulator = 2

    cr = (chip * 64) + (register * 16) + address

    chip_test.CARRY = 0
    chip_test.COMMAND_REGISTER = cr

    chip_test.CURRENT_RAM_BANK = rambank
    absolute_address = (rambank * chip_test.RAM_BANK_SIZE) + \
        (chip * chip_test.RAM_CHIP_SIZE) + \
        (register * chip_test.RAM_REGISTER_SIZE) + address
    chip_test.RAM[absolute_address] = value
    chip_test.set_accumulator(accumulator)

    processor.adm(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.CARRY = 0
    chip_base.COMMAND_REGISTER = cr
    absolute_address = (rambank * chip_base.RAM_BANK_SIZE) + \
        (chip * chip_base.RAM_CHIP_SIZE) + \
        (register * chip_base.RAM_REGISTER_SIZE) + address
    chip_base.RAM[absolute_address] = value
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank
    chip_base.set_accumulator(value + accumulator)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
