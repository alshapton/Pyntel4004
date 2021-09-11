# Using pytest
# Test the ADM instructions of an instance of an i4004(processor)

from hardware.suboperation import insert_registerpair
import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.exceptions import InvalidRamBank  # noqa

'''
def test_validate_rdn_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[234]
    known = {"opcode": 234, "mnemonic": "rdr()", "exe": 10.8, "bits": ["1110", '1010'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[0, 15], [1, 14], [2, 13], [3, 12], [4, 11],
                                    [5, 10], [6, 9], [7, 8], [8, 7], [9 ,6],
                                    [10, 5], [11, 4], [12, 3], [13, 2], [14, 1],
                                    [15,0]]) 
def test_rdr_scenario1(values):
    """Test RDM instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    
    chip_test.set_accumulator(0)
    chip_test.COMMAND_REGISTER = values[0] << 4
    chip_test.ROM_PORT[values[0]] = values[1]
    processor.rdr(chip_test)
    
    # Simulate conditions at end of instruction in base chip
    chip_base.COMMAND_REGISTER = values[0] << 4
    chip_base.ROM_PORT[values[0]] = values[1]
    chip_base.set_accumulator(values[1])
    chip_base.increment_pc(1)
    
    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
'''
