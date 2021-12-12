# Using pytest
# Test the "empty" instructions of an instance of an i4004(processor)

import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pytest  # noqa

from hardware.processor import Processor  # noqa


@pytest.mark.parametrize("opcode", [1, 2, 3, 4, 5, 6, 7,
                                    8, 9, 10, 11, 12, 13, 14, 15, 254, 255])
def test_validate_instruction1_15(opcode):
    """Validate the instruction's opcode and characteristics."""
    chip_test = Processor()
    op = chip_test.INSTRUCTIONS[opcode]
    known = {"opcode": opcode, "mnemonic": "-", "words": 1}
    assert op == known


def test_validate_instruction256():
    """Validate the "fake" opcode and characteristics"""
    chip_test = Processor()
    op = chip_test.INSTRUCTIONS[256]
    known = {"opcode": 256, "mnemonic": "end", "exe": 0, "bits": ["1111", "1111"], "words": 0}  # noqa
    assert op == known
