# Using pytest
# Test the JCN instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa


from hardware.processor import Processor  # noqa

from hardware.suboperation import decimal_to_binary  # noqa


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                   11, 12, 13, 14, 15])
def test_validate_instruction(value):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[16 + value]
    known = {"opcode": 16 + value, "mnemonic": "jcn(" + str(value) + ",address8)", "exe": 21.6, "bits": ["0001", decimal_to_binary(4,  value), "xxxx", "xxxx"], "words": 2}  # noqa
    assert op == known

#        Conditions to check            Values
# PCbef, INV, ACC, CARRY, PIN10, PCaft, ACC, CARRY, PIN10


@pytest.mark.parametrize("values", [[100, 0, 0, 0, 0, 102, 0, 0, 0],
                                    [100, 1, 0, 0, 0, 1234, 0, 0, 0],
                                    [100, 0, 0, 0, 1, 1234, 0, 0, 0],
                                    [100, 0, 0, 0, 1, 102, 0, 0, 1],  # Pin10
                                    [100, 1, 0, 0, 1, 102, 0, 0, 0],
                                    [100, 1, 0, 0, 1, 102, 0, 0, 1],  # InvP10
                                    [100, 0, 0, 1, 0, 1234, 0, 1, 0],
                                    [100, 0, 0, 1, 0, 102, 0, 1, 0],  # Carry
                                    [100, 1, 0, 1, 0, 102, 0, 1, 0],
                                    [100, 1, 0, 1, 0, 1234, 0, 1, 0],  # InvC'y
                                    [100, 0, 1, 0, 0, 1234, 0, 0, 0],
                                    [100, 0, 1, 0, 0, 102, 12, 0, 0],  # Acc
                                    [100, 1, 1, 0, 0, 102, 0, 0, 0],
                                    [100, 1, 0, 1, 0, 1234, 12, 0, 0],  # IvAcc
                                    [100, 0, 1, 1, 0, 1234, 13, 1, 0],
                                    [100, 0, 0, 1, 1, 102, 0, 1, 0],  # Cmb
                                    [100, 1, 1, 1, 0, 102, 13, 1, 0],
                                    [100, 1, 0, 1, 1, 1234, 0, 1, 0],  # InvCmb
                                    ])
def test_scenario1(values):
    """Test JCN instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    pc = values[0]
    c1 = values[1]
    c2 = values[2]
    c3 = values[3]
    c4 = values[4]
    fa = values[5]

    accumulator = values[6]
    carry_bit = values[7]
    test_signal = values[8]

    condition = int((c1 * 8) + (c2 * 4) + (c3 * 2) + c4)
    # Set both chips to initial status

    # Set accumulator value on both chips
    chip_test.set_accumulator(accumulator)
    chip_base.set_accumulator(accumulator)
    # Set carry bit on both chips
    if carry_bit == 0:
        chip_test.reset_carry()
        chip_base.reset_carry()
    else:
        chip_test.set_carry()
        chip_base.set_carry()
    # Set test signal on both chips
    chip_test.write_pin10(test_signal)
    chip_base.write_pin10(test_signal)

    chip_test.PROGRAM_COUNTER = pc
    chip_base.PROGRAM_COUNTER = pc

    # Perform the instruction under test:
    Processor.jcn(chip_test, condition, fa)

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = fa

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
