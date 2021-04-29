# Using pytest
# Test the characteristics of an i4004(processor)

import sys
sys.path.insert(1, '../src')

from src.hardware.processor import processor  # noqa


def test_chip_properties_MAX_4_BITS():
    assert (chip.MAX_4_BITS == 15)


def test_chip_properties_MEMORY_SIZE_RAM():
    assert (chip.MEMORY_SIZE_RAM == 4096)


def test_chip_properties_MEMORY_SIZE_ROM():
    assert (chip.MEMORY_SIZE_ROM == 4096)


def test_chip_properties_MEMORY_SIZE_PRAM():
    assert (chip.MEMORY_SIZE_PRAM == 4096)


def test_chip_properties_PAGE_SIZE():
    assert (chip.PAGE_SIZE == 256)


def test_chip_properties_STACK_SIZE():
    assert (chip.STACK_SIZE == 3)


def test_chip_properties_NO_REGISTERS():
    assert (chip.NO_REGISTERS == 16)


def test_chip_properties_NO_ROM_PORTS():
    assert (chip.NO_ROM_PORTS == 32)


def test_chip_properties_NO_CHIPS_PER_BANK():
    assert (chip.NO_CHIPS_PER_BANK == 4)


def test_chip_properties_RAM_BANK_SIZE():
    assert (chip.RAM_BANK_SIZE == 256)


def test_chip_properties_RAM_CHIP_SIZE():
    assert (chip.RAM_CHIP_SIZE == 64)


def test_chip_properties_RAM_REGISTER_SIZE():
    assert (chip.RAM_REGISTER_SIZE == 16)


def test_chip_properties_NO_DRB():
    assert (chip.NO_DRB == 8)


def test_chip_properties_NO_COMMAND_REGISTERS():
    assert (chip.NO_COMMAND_REGISTERS == 8)


def test_chip_properties_NO_STATUS_REGISTERS():
    assert (chip.NO_STATUS_REGISTERS == 4)


def test_chip_properties_NO_STATUS_CHARACTERS():
    assert (chip.NO_STATUS_CHARACTERS == 4)


def test_init_ram_without_read():
    assert(sum(chip.RAM) == 0)


chip = processor()
