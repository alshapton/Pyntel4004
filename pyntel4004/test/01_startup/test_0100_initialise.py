# Using pytest
# Test the initialisation of an instance of an i4004(processor)
# Using the functions from the init.py module (via processor.py)
# Also testing the functions of the other.py module (via processor.py)

# Import system modules
import os
import sys

sys.path.insert(1, '..' + os.sep + 'src')

import pytest  # noqa


from hardware.processor import Processor  # noqa


@pytest.mark.withoutread
def test_init_ram_without_read():
    """Test RAM content directly."""
    assert sum(chip.RAM) == 0


@pytest.mark.withread
def test_init_ram_with_read():
    """Test RAM content with read function."""
    assert sum(chip.read_all_ram()) == 0


@pytest.mark.withoutread
def test_init_command_registers_without_read():
    """Test command register content directly."""
    assert sum(chip.COMMAND_REGISTERS) == 0


@pytest.mark.withread
def test_init_command_registers_with_read():
    """Test command register content with read function."""
    assert sum(chip.read_all_command_registers()) == 0


@pytest.mark.withoutread
def test_init_registers_without_read():
    """Test register content directly."""
    assert sum(chip.REGISTERS) == 0


@pytest.mark.withread
def test_init_registers_with_read():
    """Test register content with read function."""
    assert sum(chip.read_all_registers()) == 0


@pytest.mark.withoutread
def test_init_stack_without_read():
    """Test stack content directly."""
    assert sum(chip.STACK) == 0


@pytest.mark.withread
def test_init_stack_with_read():
    """Test content of the stack with read function."""
    assert sum(chip.read_all_stack()) == 0


@pytest.mark.withoutread
def test_init_rom_without_read():
    """Test ROM content directly."""
    assert sum(chip.ROM) == 0


@pytest.mark.withread
def test_init_rom_with_read():
    """Test ROM content with read function."""
    assert sum(chip.read_all_rom()) == 0


@pytest.mark.withoutread
def test_init_pram_without_read():
    """Test PRAM content directly."""
    assert sum(chip.PRAM) == 0


@pytest.mark.withread
def test_init_pram_with_read():
    """Test PRAM content with read function."""
    assert sum(chip.read_all_pram()) == 0


@pytest.mark.withoutread
def test_init_wpm_counter_without_read():
    """Test WPM counter directly."""
    assert chip.WPM_COUNTER == 'LEFT'


@pytest.mark.withread
def test_init_wpm_counter_with_read():
    """Test WPM counter with read function."""
    assert chip.read_wpm_counter() == 'LEFT'


@pytest.mark.withoutread
def test_init_accumulator_without_read():
    """Test ACCUMULATOR content directly."""
    assert chip.ACCUMULATOR == 0


@pytest.mark.withread
def test_init_accumulator_with_read():
    """Test accumulator with read function."""
    assert chip.read_accumulator() == 0


@pytest.mark.withoutread
def test_init_acbr_without_read():
    """Test ACBR content directly."""
    assert chip.ACBR == 0


@pytest.mark.withread
def test_init_acbr_with_read():
    """Test ACBR with read function."""
    assert chip.read_acbr() == 0


@pytest.mark.withoutread
def test_init_carry_bit_without_read():
    """Test CARRY flag content directly."""
    assert chip.CARRY == 0


@pytest.mark.withread
def test_init_carry_bit_with_read():
    """Test carry flag with read function."""
    assert chip.read_carry() == 0


@pytest.mark.withoutread
def test_init_current_ram_bank_without_read():
    """Test current RAM bank indicator directly."""
    assert chip.CURRENT_DRAM_BANK == 0


@pytest.mark.withread
def test_init_current_ram_bank_with_read():
    """Test current RAM bank indicator with read function."""
    assert chip.read_current_ram_bank() == 0


@pytest.mark.withoutread
def test_init_program_counter_without_read():
    """Test program counter content directly."""
    assert chip.PROGRAM_COUNTER == 0


@pytest.mark.withread
def test_init_program_counter_with_read():
    """Test program counter with read function."""
    assert chip.read_program_counter() == 0


@pytest.mark.withoutread
def test_init_stack_pointer_without_read():
    """Test stack pointer directly."""
    assert chip.STACK_POINTER == 2


@pytest.mark.withread
def test_init_stack_pointer_with_read():
    """Test stack pointer value with read function."""
    assert chip.read_stack_pointer() == 2


@pytest.mark.withoutread
def test_init_rom_ports_without_read():
    """Test ROM port content directly."""
    assert sum(chip.ROM_PORT) == 0


@pytest.mark.withread
def test_init_rom_ports_with_read():
    """Test ROM port content with read function."""
    assert sum(chip.read_all_rom_ports()) == 0


@pytest.mark.withoutread
def test_init_ram_ports_without_read():
    """Test RAM portcontent directly."""
    for i in range(chip.NO_CHIPS_PER_BANK):
        assert sum(chip.RAM_PORT[i]) == 0


@pytest.mark.withread
def test_init_ram_ports_with_read():
    """Test RAM port content with read function."""
    ram_ports = chip.read_all_ram_ports()
    for i in range(chip.NO_CHIPS_PER_BANK):
        assert sum(ram_ports[i]) == 0


@pytest.mark.withoutread
def test_init_status_characters_without_read():
    """Test RAM status characters directly."""
    for b in range(chip.NO_DRB):
        for c in range(chip.NO_CHIPS_PER_BANK):
            for r in range(chip.NO_STATUS_REGISTERS):
                assert sum(chip.STATUS_CHARACTERS[b][c][r]) == 0


@pytest.mark.withread
def test_init_status_characters_with_read():
    """Test RAM status characters with read function."""
    status_characters = chip.read_all_status_characters()
    for b in range(chip.NO_DRB):
        for c in range(chip.NO_CHIPS_PER_BANK):
            for r in range(chip.NO_STATUS_REGISTERS):
                assert sum(status_characters[b][c][r]) == 0


@pytest.mark.withoutread
def test_init_pin_10_without_read():
    """Test PIN 10 directly."""
    assert chip.PIN_10_SIGNAL_TEST == 0


@pytest.mark.withread
def test_init_pin_10_with_read():
    """Test PIN 10 with read function."""
    assert chip.read_pin10() == 0


def test_full_opcodes():
    """Test opcode count directly."""
    assert len(chip.INSTRUCTIONS) == 256


chip = Processor()
