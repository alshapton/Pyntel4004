# Using pytest
# Test the INC instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from src.hardware.processor import processor # noqa
from src.hardware.suboperation import insert_register , decimal_to_binary  # noqa

@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])
def test_validate_instruction(registerpair):
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[48 + (registerpair * 2)]
    known = {"opcode": 48 + (registerpair * 2), "mnemonic": "fin(" + str(registerpair) + ")", "exe": 21.6, "bits": ["0011", decimal_to_binary(chip_test, 4, registerpair *2 )], "words": 1} # noqa
    assert(op == known)

@pytest.mark.parametrize("values", [[0, 123], [1, 234], [2,12], [3, 100], [4, 0], [5, 44], [6, 15], [7, 255] ]) # noqa
def test_scenario1(values):
    chip_test = processor()
    chip_base = processor()


    # Simulate conditions at end of instruction in base chip
    
    registerpair = values[0]
    valueofregisterpair0 = values[1]

    #split_num = [int(processor.decimal_to_binary[0:4]), int(str_num[4:])]
    chip_base.REGISTERS[0] =  0
    chip_base.REGISTERS[0] = 0
    

    # Perform the instruction under test:
    # Fetch indirect from
    processor.fin(chip_test, values[0])


    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    #assert (chip_test.read_program_counter() ==
    #        chip_base.read_program_counter())
    #assert (chip_test.read_register(0) ==
    #        chip_base.read_register(0))

    # Pickling each chip and comparing will show equality or not.
    #  assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))

"""

def test_scenario2():

    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    # Use register 0 to attempt to raise an exception
    for i in range(14):
        processor.inc(chip_test, 0)

    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(14)
    insert_register(chip_test, 0, 0)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert (chip_test.read_program_counter() ==
            chip_base.read_program_counter())
    assert (chip_test.read_register(0) == chip_base.read_register(0))

    # Pickling each chip and comparing will show complete equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))

"""