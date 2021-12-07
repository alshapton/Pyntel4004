"""Register methods."""
# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

from hardware.exceptions import  InvalidRegister, InvalidRegisterPair, \
    ValueTooLargeForRegister, ValueTooLargeForRegisterPair  # noqa


def increment_register(self, register: int) -> int:
    """
    Increment the value in a register by 1.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    register: int, mandatory
        register to increment

    Returns
    -------
    self.REGISTERS[register]
        value of the register post increment

    Raises
    ------
    InvalidRegister

    Notes
    -----
    N/A

    """
    if register < 0 or register > (self.NO_REGISTERS - 1):
        raise InvalidRegister('Register: ' + str(register))

    self.REGISTERS[register] = self.REGISTERS[register] + 1
    if self.REGISTERS[register] > self.MAX_4_BITS:
        self.REGISTERS[register] = 0
    return self.REGISTERS[register]


def insert_register(self, register: int, value: int) -> int:
    """
    Insert a value into a specific register.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    register: int, mandatory
        The number of the register to use

    value: int, mandatory
        The value to insert

    Returns
    -------
    value
        The value of the register

    Raises
    ------
    InvalidRegister
    ValueTooLargeForRegister

    Notes
    -----
    N/A

    """
    if (register < 0) or (register > 15):
        raise InvalidRegister('Register: ' + str(register))

    if value > 15:
        raise ValueTooLargeForRegister('Register: ' + str(register) + ',Value: ' + str(value))  # noqa
    self.REGISTERS[register] = value
    return value


def insert_registerpair(self, registerpair: int, value: int) -> int:
    """
    Insert a value into a specific register.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    registerpair: int, mandatory
        The number of the register to insert

    value: int, mandatory
        The value to insert

    Returns
    -------
    value
        The value of the register pair

    Raises
    ------
    InvalidRegisterPair
    ValueTooLargeForRegisterPair

    Notes
    -----
    N/A

    """
    if 0 < registerpair > 7:
        raise InvalidRegisterPair('Register Pair: ' +
                                  str(registerpair))
    if value > 256:
        raise ValueTooLargeForRegisterPair('Register Pair: ' +
                                           str(registerpair) +
                                           ',Value: ' +
                                           str(value))
    # Convert a register pair into a base register for insertion
    base_register = registerpair * 2
    self.insert_register(base_register, (value >> 4) & 15)   # Bit-shift right and remove low bits   # noqa
    self.insert_register(base_register + 1, value & 15)      # Remove low bits                       # noqa
    return value


def read_all_registers(self) -> list:
    """
    Return the values of the Registers.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    REGISTERS
        The values of all the Registers

    """
    return self.REGISTERS


def read_register(self, register: int) -> int:
    """
    Read a specific register.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    register: int, mandatory
        The number of the register to read

    Returns
    -------
    self.REGISTERS[register]
        The value of the requested register

    Raises
    ------
    InvalidRegister

    Notes
    -----
    N/A

    """
    if (register < 0) or (register > 15):
        raise InvalidRegister('Register:' + str(register))

    return self.REGISTERS[register]


def read_registerpair(self, registerpair: int) -> int:
    """
    Read a specific register pair.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    registerpair: int, mandatory
        The number of the register pair to read

    Returns
    -------
    value
        The value of the requested register pair

    Raises
    ------
    InvalidRegister

    Notes
    -----
    N/A

    """
    if (registerpair < 0 or registerpair > 7):
        raise InvalidRegisterPair('Register Pair: ' +
                                  str(registerpair))
    # Convert a register pair into a base register for insertion
    base_register = registerpair * 2

    hi = self.read_register(base_register)       # High 4-bits
    lo = self.read_register(base_register + 1)   # Low 4-bits
    return (hi << 4) + lo   # Bit-shift left high value and add low value
