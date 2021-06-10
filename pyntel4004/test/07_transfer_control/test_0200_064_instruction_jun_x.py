# Using pytest
# Test the JUN instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.exceptions import ProgramCounterOutOfBounds # noqa
from hardware.processor import processor # noqa

from hardware.suboperation import decimal_to_binary # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                   10, 11, 12, 13, 14, 15])
def test_validate_instruction(value):
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[64 + value]
    known = {"opcode": 64 + value, "mnemonic": "jun(address12)", "exe": 21.6, "bits": ["0100", decimal_to_binary(chip_test, 4, value)], "words": 2} # noqa
    assert(op == known)


@pytest.mark.parametrize("address12", [0, 100, 99, 256, 512, 4095, 4094, 2048])
def test_scenario1(address12):
    chip_test = processor()
    chip_base = processor()

    # Set chip to initial status
    chip_test.PROGRAM_COUNTER = 0

    # Perform the instruction under test:
    processor.jun(chip_test, address12)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = address12

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert (chip_test.read_program_counter() ==
            chip_base.read_program_counter())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


@pytest.mark.parametrize("address12", [-1, 4096])
def test_scenario2(address12):

    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at START of operation in base chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # Simulate conditions at END of operation in test chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # attempting to use an invalid address
    with pytest.raises(Exception) as e:
        assert (processor.jun(chip_test, address12))
    assert (str(e.value) == 'Program counter attempted to be set to ' + str(address12)) # noqa
    assert (e.type == ProgramCounterOutOfBounds)

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))
