"""Initialisation methods."""


def init_ram(self) -> None:
    """
    Initialise the RAM with zeroes in all locations.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.MEMORY_SIZE_RAM):
        self.RAM.append(0)


def init_command_registers(self) -> None:
    """
    Initialise the command registers with zeroes.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.NO_COMMAND_REGISTERS):
        self.COMMAND_REGISTERS.append(0)


def init_registers(self) -> None:
    """
    Initialise the registers with zeroes.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.NO_REGISTERS):
        self.REGISTERS.append(0)


def init_stack(self) -> None:
    """
    Initialise the stack.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.STACK_SIZE):
        self.STACK.append(0)


def init_rom(self) -> None:
    """
    Initialise the ROM with zeroes in all locations.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.MEMORY_SIZE_ROM):
        self.ROM.append(0)


def init_pram(self) -> None:
    """
    Initialise the PRAM with zeroes in all locations.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.MEMORY_SIZE_PRAM):
        self.PRAM.append(0)


def init_wpm_counter(self) -> None:
    """
    Initialise the WPM Counter.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Notes
    -----
    The WPM counter is required to allow WPM instructions to track which
    4-bit portion of an 8-bit byte is being transferred.

    """
    self.WPM_COUNTER = 'LEFT'
