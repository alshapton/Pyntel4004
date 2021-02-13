# Using pytest and delayed-assert add-in
import delayed_assert
from i4004.src.i4004 import processor

def test_init():
    delayed_assert.expect(chip.read_accumulator() == 0)
    delayed_assert.expect(chip.MAX_4_BITS == 15)
    delayed_assert.expect(chip.read_carry() is False)
    delayed_assert.expect(sum(chip.read_all_ram()) == 0)
    delayed_assert.expect(sum(chip.read_all_rom()) == 0)
    delayed_assert.expect(sum(chip.read_all_registers()) == 0)
   
    
    # delayed_assert.expect(sum(chip.read_all_pram()) == 0) # Needs work
    
   
    delayed_assert.assert_expectations()


chip = processor()

