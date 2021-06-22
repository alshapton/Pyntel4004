# Using pytest
# Test the characteristics of an i4004(processor)

import sys
sys.path.insert(1, '../src')
from hardware.processor import processor  # noqa


def test_chip_properties_MAX_4_BITS():
    """Ensure the chip has been set with the correct value for a 4-bit word."""
    assert chip.MAX_4_BITS == 15


def test_chip_properties_MEMORY_SIZE_RAM():
    """Ensure the chip has been set with the correct memory size for RAM."""
    assert chip.MEMORY_SIZE_RAM == 4096


def test_chip_properties_MEMORY_SIZE_ROM():
    """Ensure the chip has been set with the correct memory size for ROM."""
    assert chip.MEMORY_SIZE_ROM == 4096


def test_chip_properties_MEMORY_SIZE_PRAM():
    """Ensure the chip has been set with the correct memory size for PRAM."""
    assert chip.MEMORY_SIZE_PRAM == 4096


def test_chip_properties_PAGE_SIZE():
    """Ensure the chip has been set with the correct page size."""
    assert chip.PAGE_SIZE == 256


def test_chip_properties_STACK_SIZE():
    """Ensure the chip has been set with the appropriate stack size."""
    assert chip.STACK_SIZE == 3


def test_chip_properties_NO_REGISTERS():
    """Ensure the chip has been set with the correct number of registers"""
    assert chip.NO_REGISTERS == 16


def test_chip_properties_NO_ROM_PORTS():
    """Ensure the chip has been set with the correct number of ROM ports."""
    assert chip.NO_ROM_PORTS == 32


def test_chip_properties_NO_CHIPS_PER_BANK():
    """Ensure the chip has been set with the right number of chips per bank."""
    assert chip.NO_CHIPS_PER_BANK == 4


def test_chip_properties_RAM_BANK_SIZE():
    """Ensure the chip has been set with the correct bank size."""
    assert chip.RAM_BANK_SIZE == 256


def test_chip_properties_RAM_CHIP_SIZE():
    """Ensure the chip has been set with the appropriate RAM chip size."""
    assert chip.RAM_CHIP_SIZE == 64


def test_chip_properties_RAM_REGISTER_SIZE():
    """Ensure the chip has been set with the correct RAM register size."""
    assert chip.RAM_REGISTER_SIZE == 16


def test_chip_properties_NO_DRB():
    """Ensure the chip has been set with the correct RAM banks."""
    assert chip.NO_DRB == 8


def test_chip_properties_NO_COMMAND_REGISTERS():
    """Ensure the chip has been set with the right number of command registers.""" # noqa
    assert chip.NO_COMMAND_REGISTERS == 8


def test_chip_properties_NO_STATUS_REGISTERS():
    """Ensure the chip has been set with the correct number of status registers.""" # noqa
    assert chip.NO_STATUS_REGISTERS == 4


def test_chip_properties_NO_STATUS_CHARACTERS():
    """Ensure the chip has been set with the correct number of status characters.""" # noqa
    assert chip.NO_STATUS_CHARACTERS == 4


def test_init_ram_without_read():
    """Ensure the RAM has been set up with all zeroes."""
    assert sum(chip.RAM) == 0


def test_init_MSB():
    """Ensure the chip has been set with the most significant bit value."""
    assert chip.MSB == 8


chip = processor()
