# Using pytest
# Test the initialisation of an instance of an i4004(processor)

import sys
# import pytest
sys.path.insert(1, '../src')

from src.hardware.processor import processor  # noqa


def test_base_chip():
    assert (hash(chip_base) == hash(chip_test))


def test_nop():
    processor.nop(chip_test)


def test_post_nop_chip():
    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(1)
    assert (hash(chip_base) == hash(chip_test))


chip_base = processor()
chip_test = processor()
