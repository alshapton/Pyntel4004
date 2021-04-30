# Using pytest
# Test the initialisation of an instance of an i4004(processor)

import sys
# import pytest
sys.path.insert(1, '../src')

from src.hardware.processor import processor  # noqa

# This needs to be extracted and placed soomewhere else


def freeze(o):
    if isinstance(o, dict):
        return frozenset({k: freeze(v) for k, v in o.items()}.items())

    if isinstance(o, list):
        return tuple([freeze(v) for v in o])

    return o


def make_hash(o):
    """
    makes a hash out of anything that contains only list,dict and hashable
    types including string and numeric types
    """
    return hash(freeze(o))


def test_validate_instruction():
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[0]
    known = {'opcode': 0, 'mnemonic': 'nop()', 'exe': 10.8, 'bits': ['0000', '0000'], 'words': 1} # noqa
    assert (make_hash(known) == make_hash(op))


def test_post_nop_chip():
    # Perform the instruction under test:
    processor.nop(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(1)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test
    assert (processor.make_hash(chip_base) == processor.make_hash(chip_test))


chip_base = processor()
chip_test = processor()
