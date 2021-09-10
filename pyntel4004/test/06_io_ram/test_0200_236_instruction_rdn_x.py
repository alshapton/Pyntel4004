# Using pytest
# Test the RDn instructions of an instance of an i4004(processor)

from hardware.suboperation import insert_registerpair
import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.exceptions import InvalidRamBank  # noqa


def test_validate_rdN_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[236]
    known = {"opcode": 236, "mnemonic": "rd0()", "exe": 10.8, "bits": ["1110", '1100'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[237]
    known = {"opcode": 237, "mnemonic": "rd1()", "exe": 10.8, "bits": ["1110", '1101'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[238]
    known = {"opcode": 238, "mnemonic": "rd2()", "exe": 10.8, "bits": ["1110", '1110'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[239]
    known = {"opcode": 239, "mnemonic": "rd3()", "exe": 10.8, "bits": ["1110", '1111'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("chip", [0, 1, 2, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
def test_rdN_scenario1(chip, register):

    from random import seed
    from random import randint

    """Test RDM instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    value = randint(0, 15)

    address = (chip << 6) + (register << 4)
    chip_test.COMMAND_REGISTER = address
    chip_test.CURRENT_RAM_BANK = 0
    chip_test.STATUS_CHARACTERS[chip_test.CURRENT_RAM_BANK][chip][register][register] = value

    # Perform the instruction under test:
    if register == 0:
        processor.rd0(chip_test)
    if register == 1:
        processor.rd1(chip_test)
    if register == 2:
        processor.rd2(chip_test)
    if register == 3:
        processor.rd3(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.COMMAND_REGISTER = address
    chip_base.increment_pc(1)
    chip_base.set_accumulator(value)
    chip_base.STATUS_CHARACTERS[chip_test.CURRENT_RAM_BANK][chip][register][register] = value

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
