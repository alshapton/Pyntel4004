"""RAM methods."""
# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

from hardware.suboperations.other import decode_command_register  # noqa


def rdx(self, character) -> int:
    """
    Read RAM status character X.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the Processor containing the registers, accumulator etc

    character:
        RAM STATUS CHARACTER to read

    Returns
    -------
    self.ACCUMULATOR
        The value read from the specified RAM STATUS CHARACTER

    """
    crb = self.read_current_ram_bank()
    chip, register, _none = \
        decode_command_register(self.COMMAND_REGISTER, 'DATA_RAM_STATUS_CHAR')
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][character]
    self.increment_pc(1)
    return self.ACCUMULATOR


def read_all_ram(self) -> list:
    """
    Return the values of all the locations of RAM.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    RAM
        The values of all the locations of RAM

    """
    return self.RAM


def read_all_ram_ports(self) -> list:
    """
    Return the values of all the RAM ports.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    RAM_PORT
        The values of all the RAM ports

    """
    return self.RAM_PORT


def read_all_pram(self) -> list:
    """
    Return the values of all the locations of PRAM.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    PRAM
        The values of all the locations of PRAM

    """
    return self.PRAM


def read_all_status_characters(self) -> list:
    """
    Return the values of all the RAM status characters.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    STATUS_CHARACTERS
        The values of all the RAM status characters

    """
    return self.STATUS_CHARACTERS


def read_current_ram_bank(self) -> int:
    """
    Return the current RAM bank i.e. the one selected by the SRC.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    CURRENT_RAM_BANK
        The current RAM bank value

    """
    return self.CURRENT_RAM_BANK


def write_ram_status(self, char: int) -> bool:
    """
    Write to a RAM status character.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    char: int, mandatory
        specified status character

    Returns
    -------
    True
        if the value is set successfully

    Raises
    ------
    N/A

    Notes
    -----
    No error checking is done in this function
    All parameters cannot be out of range, since the functions to
    place them in various registers etc all have range checking built in .

    Eventually - there will be error checking here

    """
    value = self.read_accumulator()
    crb = self.read_current_ram_bank()

    chip, register, _none = \
        decode_command_register(self.COMMAND_REGISTER,
                                'DATA_RAM_STATUS_CHAR')
    self.STATUS_CHARACTERS[crb][chip][register][char] = value
    return True
