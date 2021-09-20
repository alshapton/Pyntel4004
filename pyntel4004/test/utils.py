
from hardware.processor import processor


def is_same(chip1: processor, chip2: processor,component: str):
    """Individual assertions that the two supplied chips are identical."""

    if (component != ''):
        print('chip1:  ' + str(eval(('chip1.' + component ))))
        print('chip2:  ' + str(eval(('chip2.' + component ))))

    # Check command registers
    assert chip1.COMMAND_REGISTERS == chip2.COMMAND_REGISTERS

    # Check RAM content
    assert chip1.RAM == chip2.RAM
    assert chip1.RAM_PORT == chip2.RAM_PORT

    # Check ROM content
    assert chip1.ROM == chip2.ROM
    assert chip1.ROM_PORT == chip2.ROM_PORT

    # Check PRAM, Registers and Stack
    assert chip1.PRAM == chip2.PRAM
    assert chip1.REGISTERS == chip2.REGISTERS
    assert chip1.STACK == chip2.STACK

    # Check Command Register
    assert chip1.COMMAND_REGISTER == chip2.COMMAND_REGISTER

    # Check RAM status characters
    assert chip1.STATUS_CHARACTERS == chip2.STATUS_CHARACTERS

    assert chip1.PIN_10_SIGNAL_TEST == chip2.PIN_10_SIGNAL_TEST

    # Check Internals
    assert chip1.ACCUMULATOR == chip2.ACCUMULATOR
    assert chip1.ACBR == chip2.ACBR
    assert chip1.STACK_POINTER == chip2.STACK_POINTER
    assert chip1.PROGRAM_COUNTER == chip2.PROGRAM_COUNTER
    assert chip1.CURRENT_DRAM_BANK == chip2.CURRENT_DRAM_BANK
    assert chip1.CURRENT_RAM_BANK == chip2.CURRENT_RAM_BANK
    assert chip1.CARRY == chip2.CARRY
    assert chip1.WPM_COUNTER == chip2.WPM_COUNTER
