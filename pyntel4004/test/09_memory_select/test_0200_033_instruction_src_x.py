# Using pytest
# Test the INC instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor # noqa
from hardware.suboperation import insert_register , decimal_to_binary, \
        insert_registerpair  # noqa
from hardware.exceptions import InvalidRegisterPair # noqa


@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])
def test_validate_instruction(registerpair):
    ''' Ensure instruction's characteristics are valid '''
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[33 + (registerpair * 2)]
    known = {"opcode": 33 + (registerpair * 2), "mnemonic": "src(" + str(registerpair) + ")", "exe": 21.6, "bits": ["0010", decimal_to_binary(chip_test, 4, (registerpair  * 2) + 1)], "words": 1} # noqa
    assert(op == known)


@pytest.mark.parametrize("values", [[0, 240], [1, 91], [2, 245], [3, 102],
                                    [4, 30], [5, 164], [6, 196], [7, 231]])
def test_scenario1(values):
    chip_test = processor()
    chip_base = processor()

    registerpair = values[0]
    value = values[1]
    # Set up chip conditions prior to commencement of test
    insert_registerpair(chip_test, registerpair, value)
    chip_test.PROGRAM_COUNTER = 0

    # Perform the instruction under test:
    processor.src(chip_test, registerpair)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(1)
    insert_registerpair(chip_base, registerpair, value)
    chip_base.COMMAND_REGISTER = value

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert (chip_test.read_program_counter() ==
            chip_base.read_program_counter())
    assert (chip_test.COMMAND_REGISTER ==
            chip_base.COMMAND_REGISTER)

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


@pytest.mark.parametrize("registerpair", [8, 9])
def test_dcl_scenario2(registerpair):

    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at START of operation in base chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # Simulate conditions at END of operation in test chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # attempting to use an invalid Register Pair
    with pytest.raises(Exception) as e:
        assert (processor.src(chip_test, registerpair))
    assert (str(e.value) == 'Register pair : ' + str(registerpair))
    assert (e.type == InvalidRegisterPair)

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))
