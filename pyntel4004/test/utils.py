
from hardware.processor import Processor

###############################################################################
# Only used during testing to construct a command register of varying formats #
###############################################################################


def encode_command_register(chip, register, address, shape):

    from hardware.suboperations.utility import decimal_to_binary  # noqa
    from hardware.exceptions import InvalidCommandRegisterFormat

    if shape not in ('DATA_RAM_CHAR', 'DATA_RAM_STATUS_CHAR',
                     'RAM_PORT', 'ROM_PORT'):
        raise InvalidCommandRegisterFormat('Shape: ' + shape)

    if shape == 'DATA_RAM_CHAR':
        i_chip = decimal_to_binary(2, chip)
        i_register = decimal_to_binary(2, register)
        i_address = decimal_to_binary(4, address)
        command_register = i_chip + i_register + i_address

    if shape == 'DATA_RAM_STATUS_CHAR':
        i_chip = decimal_to_binary(2, chip)
        i_register = decimal_to_binary(2, register)
        i_address = '0000'
        command_register = i_chip + i_register + i_address

    if shape == 'RAM_PORT':
        # Note that in this instance, "chip" refers to "port"
        i_chip = decimal_to_binary(2, chip)
        i_register = '000'
        i_address = '000'
        command_register = i_chip + i_register + i_address

    if shape == 'ROM_PORT':
        # Note that in this instance, "chip" refers to "port"
        i_chip = decimal_to_binary(4, chip)
        i_register = '00'
        i_address = '00'
        command_register = i_chip + i_register + i_address

    return command_register


def is_same(chip1: Processor, chip2: Processor, component: str):
    """Individual assertions that the two supplied chips are identical."""
    # Valid component values are:
    #
    # ''                ALL components
    # RAM               RAM
    # REGISTERS         Registers
    # COMMAND_REGISTER  Command Register

    if component != '':
        # skipcq: PYL-PYL-W0123
        print('chip1:  ' + str(eval(('chip1.' + component))))
        # skipcq: PYL-PYL-W0123
        print('chip2:  ' + str(eval(('chip2.' + component))))

    # Check RAM content
    if component == 'RAM':
        for i in range(4095):
            if chip1.RAM[i] != chip2.RAM[i]:
                print('RAM Location: ', i, '   ',
                      chip1.RAM[i], '    ', chip2.RAM[i])
            assert chip1.RAM[i] == chip2.RAM[i]

    # Check Registers content
    if component == 'REGISTERS':
        for i in range(15):
            if chip1.REGISTERS[i] != chip2.REGISTERS[i]:
                print('Register: ', i, '   ',
                      chip1.REGISTERS[i], '    ', chip2.REGISTERS[i])
            assert chip1.REGISTERS[i] == chip2.REGISTERS[i]

    # Check command registers
    assert chip1.COMMAND_REGISTERS == chip2.COMMAND_REGISTERS

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

    return True
