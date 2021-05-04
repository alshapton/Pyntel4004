# Using pytest
# Test the initialisation of an instance of an i4004(processor)

import sys
import pickle

import pytest

sys.path.insert(1, '../src')

import hardware.suboperation # noqa
from hardware.processor import processor  # noqa
from hardware.exceptions import ValueTooLargeForRegister, InvalidRegister # noqa


def test_suboperation_set_carry():
    chip_base = processor()
    chip_test = processor()

    # Perform the instruction under test:
    # setting carry
    processor.set_carry(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.CARRY = 1

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert (chip_test.read_program_counter() == chip_base.read_program_counter())
    assert (chip_test.read_carry() == chip_base.read_carry())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_reset_carry():
    chip_base = processor()
    chip_test = processor()

    # Perform the instruction under test:
    # resetting carry
    processor.reset_carry(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.CARRY = 0

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert (chip_test.read_program_counter() == chip_base.read_program_counter())
    assert (chip_test.read_carry() == chip_base.read_carry())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_suboperation_insert_register_scenario1(register):
    chip_base = processor()
    chip_test = processor()

    # Perform the instruction under test:
    # insert a value of 5 into each register
    processor.insert_register(chip_test, register, 5)

    # Simulate conditions at end of instruction in base chip
    chip_base.REGISTERS[register] = 5

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert (chip_test.read_program_counter() == chip_base.read_program_counter())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_insert_register_scenario2():
    chip_base = processor()
    chip_test = processor()

    # Perform the instruction under test:
    # attempting to insert a value larger than the register can hold
    with pytest.raises(Exception) as e:
        assert (processor.insert_register(chip_test, 3, 25))
    assert (str(e.value) == "Register: 3,Value: 25")
    assert (e.type == ValueTooLargeForRegister)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert(chip_test.read_register(3) == 0)

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_insert_register_scenario3():
    chip_base = processor()
    chip_test = processor()

    # Perform the instruction under test:
    # attempting to insert a value larger than the register can hold
    with pytest.raises(Exception) as e:
        assert (processor.insert_register(chip_test, 25, 3))
    assert (str(e.value) == "Register: 25")
    assert (e.type == InvalidRegister)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    
    # N/A - the operation will completely fail - the chip will be as it was
    # in the base state

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))

@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_suboperation_read_register_scenario1(register):
    chip_base = processor()
    chip_test = processor()

    # Perform the instruction under test:
    # insert a value of 5 into each register
    chip_test.REGISTERS[register] = 5

    # Simulate conditions at end of instruction in base chip

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert (chip_test.read_register(register) == 5)

