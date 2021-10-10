# Using pytest
# Test the WRn instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.suboperation import encode_command_register  # noqa


def test_validate_wrNinstruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    # There are 4 wrN instructions.
    op = chip_test.INSTRUCTIONS[228]
    known = {"opcode": 228, "mnemonic": "wr0()", "exe": 10.8, "bits": ["1110", '0100'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[229]
    known = {"opcode": 229, "mnemonic": "wr1()", "exe": 10.8, "bits": ["1110", '0101'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[230]
    known = {"opcode": 230, "mnemonic": "wr2()", "exe": 10.8, "bits": ["1110", '0110'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[231]
    known = {"opcode": 231, "mnemonic": "wr3()", "exe": 10.8, "bits": ["1110", '0111'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rambank", [0, 1, 2, 3])
@pytest.mark.parametrize("chip", [0, 1, 2, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
@pytest.mark.parametrize("char", [0, 1, 2, 3])
def test_wrN_scenario1(rambank, chip, register, char):
    """Test instruction WRn"""
    from random import randint

    chip_test = processor()
    chip_base = processor()

    value = randint(0, 15)

    address = encode_command_register(chip, register, 0,
                                      'DATA_RAM_STATUS_CHAR')
    chip_test.CURRENT_RAM_BANK = rambank
    chip_test.COMMAND_REGISTER = address
    chip_test.set_accumulator(value)

    # Perform the instruction under test:
    if char == 0:
        processor.wr0(chip_test)
    if char == 1:
        processor.wr1(chip_test)
    if char == 2:
        processor.wr2(chip_test)
    if char == 3:
        processor.wr3(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.COMMAND_REGISTER = address
    chip_base.CURRENT_RAM_BANK = rambank
    chip_base.increment_pc(1)
    chip_base.set_accumulator(value)
    chip_base.STATUS_CHARACTERS[rambank][chip][register][char] = value

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
