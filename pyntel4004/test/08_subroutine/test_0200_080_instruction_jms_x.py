# Using pytest
# Test the JMS instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.suboperation import decimal_to_binary, write_to_stack  # noqa
from hardware.exceptions import ValueOutOfRangeForStack  # noqa


@pytest.mark.parametrize("increment", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                       12, 13, 14, 15])
def test_validate_instruction(increment):
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[80 + increment]
    known = {"opcode": 80 + increment, "mnemonic": "jms(address12)", "exe": 21.6, "bits": ["0101", decimal_to_binary(4, increment)], "words": 2}  # noqa
    assert op == known


@pytest.mark.parametrize("address12", [1024, 24, 99, 2095, 4090])
def test_scenario1(address12):
    """Test JMS instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 300
    chip_base.write_to_stack(chip_base.PROGRAM_COUNTER + 2)
    chip_base.PROGRAM_COUNTER = address12 - 1

    # Set up conditions in test chip
    chip_test.PROGRAM_COUNTER = 300

    # Perform the instruction under test:
    # Jump to a subroutine
    processor.jms(chip_test, address12)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.PROGRAM_COUNTER == address12 - 1
    assert chip_test.STACK_POINTER == 1
    assert chip_test.STACK[chip_test.STACK_POINTER + 1] == 302  # Return

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

'''
@pytest.mark.parametrize("values", [[1, 123, 23], [1, 234, 34],
                                    [2, 12, 5], [3, 100, 90], [4, 0, 12],
                                    [5, 44, 100], [6, 15, 48], [7, 255, 0]])
def test_scenario2(values):
    """Test JMS instruction functionality (scenario 2)."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 11
    chip_base.RAM[values[2]] = values[1]
    registervalue = convert_decimal_to_n_bit_slices(8, 4, values[1], 'd')  # noqa
    chip_base.REGISTERS[0] = registervalue[0]
    chip_base.REGISTERS[1] = registervalue[1]

    chip_test.PROGRAM_COUNTER = 10
    chip_test.RAM[values[2]] = values[1]
    chip_test.REGISTERS[0] = registervalue[0]
    chip_test.REGISTERS[1] = registervalue[1]

    # Perform the instruction under test:
    # Fetch indirect from
    left, right = processor.fin(chip_test, values[0])

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    left_r = chip_test.read_register(values[0])
    right_r = chip_test.read_register(values[0]+1)

    assert left == left_r
    assert right == right_r
    assert chip_test.PROGRAM_COUNTER == 11

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
'''


@pytest.mark.parametrize("address12", [-1, 4096])
def test_dcl_scenario2(address12):
    """Test JMS instruction failure."""
    chip_test = processor()

    # Simulate conditions at START of operation in base chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # Simulate conditions at END of operation in test chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # attempting to use an invalid value
    with pytest.raises(Exception) as e:
        assert processor.jms(chip_test, address12)
    assert str(e.value) == ' Value: ' + str(address12)
    assert e.type == ValueOutOfRangeForStack
