# Using pytest
from src.processor.opcodes import opcodes
from src.i4004 import processor

def test_init():
    assert(chip.read_accumulator() == 0)
    assert(chip.MAX_4_BITS == 15)
    assert(chip.read_carry() is False)
    assert(sum(chip.read_all_ram()) == 0)
    assert(sum(chip.read_all_rom()) == 0)
    assert(sum(chip.read_all_registers()) == 0)

chip = processor()

