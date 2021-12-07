"""Read Processor methods."""

# Import typing library
from typing import Tuple

from hardware.exceptions import InvalidCommandRegisterContent, InvalidCommandRegisterFormat  # noqa
from hardware.suboperations.utility import binary_to_decimal


def read_all_command_registers(self) -> list:
    """
    Return the values of all of the Command Registers.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    COMMAND_REGISTERS
        The values of all the Command Registers

    """
    return self.COMMAND_REGISTERS


def decode_command_register(command_register: str,
                            shape: str) -> Tuple[int, int, int]:
    """
    Convert the supplied CR into its component parts.

    Parameters
    ----------
    command_register : str, mandatory
        Content of the command register to convert

    shape:
        The shape/purpose of the command_register

    Returns
    -------
    chip: int
        The chip referred to

    register: int
        register

    address: int
        address referred to

    Raises
    ------
    InvalidCommandRegisterFormat

    """
    if shape not in ('DATA_RAM_CHAR', 'DATA_RAM_STATUS_CHAR',
                     'RAM_PORT', 'ROM_PORT'):
        raise InvalidCommandRegisterFormat('Shape: ' + shape)

    command_register = str(command_register)
    if shape == 'DATA_RAM_CHAR':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        chip = binary_to_decimal(command_register[:2])
        register = binary_to_decimal(command_register[2:4])
        address = binary_to_decimal(command_register[4:])

    if shape == 'DATA_RAM_STATUS_CHAR':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        chip = binary_to_decimal(command_register[:2])
        register = binary_to_decimal(command_register[2:4])
        address = '0'

    if shape == 'RAM_PORT':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        # Note that in this instance, "chip" refers to "port"
        chip = binary_to_decimal(command_register[:2])
        register = '0'
        address = '0'

    if shape == 'ROM_PORT':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        # Note that in this instance, "chip" refers to "port"
        chip = binary_to_decimal(command_register[:4])
        register = '0'
        address = '0'

    return int(chip), int(register), int(address)
