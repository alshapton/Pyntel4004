# Using pytest
# Test the JUN instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.exceptions import ProgramCounterOutOfBounds  # noqa
from hardware.processor import processor  # noqa

from hardware.suboperation import decimal_to_binary, convert_decimal_to_n_bit_slices  # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7])
def test_validate_instruction(value):
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[49 + (value * 2)]
    known = {"opcode": 49 + (value * 2), "mnemonic": "jin(" + str(value) + ")", "exe": 10.8, "bits": ["0011", decimal_to_binary(4, (2 * value) + 1)], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[100, 4, 21, 21], [255, 4, 21, 276]])
def test_scenario1(values):
    """Test JIN instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    PCB = values[0]
    RP = values[1]
    REG = RP * 2
    RP_CONTENT = values[2]
    RPM = processor.convert_decimal_to_n_bit_slices(8, 4, RP_CONTENT, 'd')[1]  # noqa
    RPL = processor.convert_decimal_to_n_bit_slices(8, 4, RP_CONTENT, 'd')[0]  # noqa
    PCE = values[3]

    # Set chip to initial status
    chip_test.PROGRAM_COUNTER = PCB
    chip_test.REGISTERS[REG] = RPL
    chip_test.REGISTERS[REG + 1] = RPM

    # Perform the instruction under test:
    processor.jin(chip_test, RP)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = PCE
    chip_base.REGISTERS[REG] = RPL
    chip_base.REGISTERS[REG + 1] = RPM

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("values", [[4095, 4, 21, 4350], [4095, 4, 42, 4350]])
def test_scenario2(values):
    """Test JIN instruction failure."""
    chip_test = processor()

    PCB = values[0]
    RP = values[1]
    REG = RP * 2
    RP_CONTENT = values[2]
    RPM = processor.convert_decimal_to_n_bit_slices(8, 4, RP_CONTENT, 'd')[1]  # noqa
    RPL = processor.convert_decimal_to_n_bit_slices(8, 4, RP_CONTENT, 'd')[0]  # noqa
    PCE = values[3]

    # Simulate conditions at START of operation in base chip
    # chip should have not had any changes as the operations will fail

    chip_test.PROGRAM_COUNTER = PCB
    chip_test.REGISTERS[REG] = RPL
    chip_test.REGISTERS[REG + 1] = RPM
    # Simulate conditions at END of operation in test chip
    # chip should have not had any changes as the operations will fail
    # N/A

    # attempting to use an invalid address
    with pytest.raises(Exception) as e:
        assert processor.jin(chip_test, RP)

    assert str(e.value) == 'Program counter attempted to be set to ' + str(PCE)  # noqa
    assert e.type == ProgramCounterOutOfBounds
