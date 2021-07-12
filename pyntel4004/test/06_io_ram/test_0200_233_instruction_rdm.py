# Using pytest
# Test the RDM instructions of an instance of an i4004(processor)

import sys
import pickle
import pytest
sys.path.insert(1, '../src')

from hardware.processor import processor  # noqa
from hardware.exceptions import InvalidRamBank  # noqa


def test_validate_rdm_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[233]
    known = {"opcode": 233, "mnemonic": "rdm()", "exe": 10.8, "bits": ["1110", '1001'], "words": 1}  # noqa
    assert op == known

'''
@pytest.mark.parametrize("rambank", [0, 1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("command_register", [2, 3])

@pytest.mark.parametrize("rambank", [0, 1, 2, 3, 4, 5, 6, 7])
def test_dcl_scenario1(rambank, command_register):
    """Test DCL instruction functionality."""
    chip_test = processor()
    chip_base = processor()

    # Perform the instruction under test:
    chip_test.set_accumulator(rambank)
    chip_test.dcl()

    # Simulate conditions at end of instruction in base chip
    chip_base.set_accumulator(rambank)
    chip_base.increment_pc(1)
    chip_base.CURRENT_RAM_BANK = rambank

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.CURRENT_RAM_BANK == chip_base.CURRENT_RAM_BANK

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("rambank", [8, 9])
def test_dcl_scenario2(rambank):
    """Test DCL instruction failure."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at START of operation in base chip
    # chip should have not had any changes as the operations will fail
    chip_base.set_accumulator(rambank)

    # Simulate conditions at END of operation in test chip
    # chip should have not had any changes as the operations will fail
    chip_test.set_accumulator(rambank)

    # attempting to use an invalid RAM Bank
    with pytest.raises(Exception) as e:
        assert processor.dcl(chip_test)
    assert str(e.value) == 'RAM bank : ' + str(rambank)
    assert e.type == InvalidRamBank

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
'''
