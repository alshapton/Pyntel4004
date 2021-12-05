# Using pytest
# Test the JMS instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa

from hardware.processor import Processor  # noqa
from hardware.suboperation import decimal_to_binary, write_to_stack  # noqa
from hardware.exceptions import ValueOutOfRangeForStack  # noqa


@pytest.mark.parametrize("increment", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                       12, 13, 14, 15])
def test_validate_instruction(increment):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[80 + increment]
    known = {"opcode": 80 + increment, "mnemonic": "jms(address12)", "exe": 21.6, "bits": ["0101", decimal_to_binary(4, increment)], "words": 2}  # noqa
    assert op == known


@pytest.mark.parametrize("address12", [1024, 24, 99, 2095, 4090])
def test_jms_scenario1(address12):
    """Test JMS instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 300
    chip_base.write_to_stack(chip_base.PROGRAM_COUNTER + 2)
    chip_base.PROGRAM_COUNTER = address12 - 1

    # Set up conditions in test chip
    chip_test.PROGRAM_COUNTER = 300

    # Perform the instruction under test:
    # Jump to a subroutine
    Processor.jms(chip_test, address12)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.PROGRAM_COUNTER == address12 - 1
    assert chip_test.STACK_POINTER == 1
    assert chip_test.STACK[chip_test.STACK_POINTER + 1] == 302  # Return

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("address12", [-1, 4096])
def test_jms_scenario2(address12):
    """Test JMS instruction failure."""
    chip_test = Processor()

    # Simulate conditions at START of operation in base chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # Simulate conditions at END of operation in test chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # attempting to use an invalid value
    with pytest.raises(Exception) as e:
        assert Processor.jms(chip_test, address12)
    assert str(e.value) == ' Value: ' + str(address12)
    assert e.type == ValueOutOfRangeForStack
