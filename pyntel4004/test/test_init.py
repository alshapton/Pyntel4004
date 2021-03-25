# Using pytest
# Test the initialisation of an instance of an i4004(processor)

import sys
sys.path.insert(1, '../src')

from src.i4004 import processor  # noqa

def test_init_accumulator():
    assert(chip.read_accumulator() == 0)


def test_init_acbr():
    assert(chip.ACBR == 0)


def test_init_current_ram_bank():
    assert(chip.read_current_ram_bank() == 0)


def test_init_program_counter():
    assert(chip.PROGRAM_COUNTER == 0)


def test_init_stack_pointer():
    assert(chip.STACK_POINTER == 2)


def test_init_stack():
    assert(sum(chip.read_all_stack()) == 0)


def test_init_command_registers():
    assert(sum(chip.read_all_command_registers()) == 0)


def test_init_registers():
    assert(sum(chip.read_all_registers()) == 0)


def test_init_dram():
    assert(sum(chip.read_all_pram()) == 0)


def test_init_ram():
    assert(sum(chip.read_all_ram()) == 0)


def test_init_rom():
    assert(sum(chip.read_all_rom()) == 0)


def test_init_characteristic_4_bit_value_max():
    assert(chip.MAX_4_BITS == 15)


def test_init_carry_bit():
    assert(chip.read_carry() == 0)


'''
    assert(sum(chip.read_all_ram()) == 0)
    assert(sum(chip.read_all_rom()) == 0)
    assert(sum(chip.read_all_registers()) == 0)

'''

chip = processor()

