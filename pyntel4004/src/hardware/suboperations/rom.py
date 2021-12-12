"""ROM methods."""


def read_all_rom(self) -> list:
    """
    Return the values of all the locations of ROM.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ROM
        The values of all the locations of ROM

    """
    return self.ROM


def read_all_rom_ports(self) -> list:
    """
    Return the values of all the ROM ports.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ROM_PORT
        The values of all the ROM ports

    """
    return self.ROM_PORT
