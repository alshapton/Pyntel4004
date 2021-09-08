# Using pytest
# Test the RDM instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.exceptions import InvalidRamBank  # noqa
from hardware.suboperation import  insert_registerpair 

def test_validate_rdm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[233]
    known = {"opcode": 233, "mnemonic": "rdm()", "exe": 10.8, "bits": ["1110", '1001'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 1, 0, 7, 3], [1, 3, 1, 6, 4], [2, 5, 2, 5, 5 ], \
                                   [3, 7, 3, 4, 6], [4, 3, 4, 3, 7], [5, 2, 5, 2, 2], \
                                   [6, 0, 6, 1, 1], [7, 4, 7, 0, 0]])
def test_rdm_scenario1(values):
    """Test RDM instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    rambank = values[0]
    chip = values[1]
    register = values[2]
    address = values[3]
    value = values[4]

    # Perform the instruction under test:
    chip_test.CURRENT_RAM_BANK = rambank
    absolute_address = (rambank * chip_test.RAM_BANK_SIZE) + \
                    (chip * chip_test.RAM_CHIP_SIZE) + \
                    (register * chip_test.RAM_REGISTER_SIZE) + address
    chip_test.RAM[absolute_address] = value
    chip_test.set_accumulator(0)
    chip_test.COMMAND_REGISTER = absolute_address
    processor.rdm(chip_test)
    
    # Simulate conditions at end of instruction in base chip
    chip_base.RAM[absolute_address] = value
    chip_base.COMMAND_REGISTER = absolute_address
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank


    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
