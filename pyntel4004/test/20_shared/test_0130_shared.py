# Using pytest
# Test the shared operations between assembler and executer

import sys

import pytest
from hardware.processor import Processor  # noqa
from shared.shared import get_opcodeinfo


sys.path.insert(1, '../src')

##############################################################################
#                      Test get_opcodeinfo                                   #
##############################################################################

@pytest.mark.parametrize("values", [[0, 'nop()', 10.8, '0000', '0000', 1], # noqa
                                    [33, 'src(0)', 21.6, '0010', '0001', 1], # noqa
                                    [235, 'adm()', 10.8, '1110', '1000', 1],
                                    [119, 'isz(7,address8)', 10.8, '0111', '0111', 2] # noqa
                                    ])
def test_suboperation_get_opcodeinfo_scenario1(values):
    """Tests for get_opcodeinfo function."""
    chip = Processor()

    opcode = values[0]
    mnemonic = values[1]
    exetime = values[2]
    bit1 = values[3]
    bit2 = values[4]
    words = values[5]

    opcode = '{"opcode": ' + str(opcode) + ', "mnemonic": "' + \
        mnemonic + '", "exe": ' + str(exetime) + ','
    opcode = opcode + ' "bits": ["' + bit1 + '", "' + \
        bit2 + '"], "words": ' + str(words) + '}'

    chip_opcode = str(get_opcodeinfo(chip, '',  mnemonic)).replace('\'', '"')
    assert chip_opcode == opcode


@pytest.mark.parametrize("mnemonic", ['amd()', 'adding', 'clock'])
def test_suboperation_get_opcodeinfo_scenario2(mnemonic):
    """Tests for get_opcodeinfo function."""
    chip = Processor()
    opcode = '{"opcode": -1, "mnemonic": "N/A"}'

    chip_opcode = str(get_opcodeinfo(chip, '',  mnemonic)).replace('\'', '"')
    assert chip_opcode == opcode
