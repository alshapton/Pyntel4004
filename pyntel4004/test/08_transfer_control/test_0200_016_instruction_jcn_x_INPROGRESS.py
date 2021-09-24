# Using pytest
# Test the JCN instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.exceptions import ProgramCounterOutOfBounds  # noqa
from hardware.processor import processor  # noqa

from hardware.suboperation import decimal_to_binary  # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
def test_validate_instruction(value):
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[16 + value]
    known = {"opcode": 16 + value, "mnemonic": "jcn(" + str(value) + ",address8)", "exe": 21.6, "bits": ["0001", decimal_to_binary(4,  value), "xxxx", "xxxx"], "words": 2}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[100, 0, 0, 0, 0, 1234]])
def test_scenario1(values):
    """Test JCN instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    PC = values[0]
    C1 = values[1]
    C2 = values[2]
    C3 = values[3]
    C4 = values[4]
    FA = values[5]

    CONDITION = int(C1 + C2 + C3 + C4)
    # Set chip to initial status
    chip_test.PROGRAM_COUNTER = PC
    print(CONDITION, chip_base.PROGRAM_COUNTER, chip_test.PROGRAM_COUNTER)

    # Perform the instruction under test:
    processor.jcn(chip_test, CONDITION, FA)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = FA

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
    print(CONDITION, chip_base.PROGRAM_COUNTER, chip_test.PROGRAM_COUNTER)


'''
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
'''
