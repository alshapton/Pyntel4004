# Initialisation methods


def init_ram(self):
    """
    Initialise the RAM with zeroes in all locations

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.MEMORY_SIZE_RAM):
        self.RAM.append(0)


def init_command_registers(self):
    """
    Initialise the command registers with zeroes

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.NO_COMMAND_REGISTERS):
        self.COMMAND_REGISTERS.append(0)


def init_registers(self):
    """
    Initialise the registers with zeroes

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.NO_REGISTERS):
        self.REGISTERS.append(0)


def init_stack(self):
    """
    Initialise the stack

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.STACK_SIZE):
        self.STACK.append(0)


def init_rom(self):
    """
    Initialise the ROM with zeroes in all locations

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.MEMORY_SIZE_ROM):
        self.ROM.append(0)


def init_pram(self):
    """
    Initialise the PRAM with zeroes in all locations

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _i in range(self.MEMORY_SIZE_PRAM):
        self.PRAM.append(0)


def init_wpm_counter(self):
    """
    Initialise the WPM Counter

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Notes
    -----
    The WPM counter is required to allow WPM instructions to track which
    4-bit portion of an 8-bit byte is being transferred.
    """
    self.WPM_COUNTER = 'LEFT'
