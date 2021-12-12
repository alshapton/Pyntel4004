# Read Processor Methods


def read_all_registers(self):
    """
    Return the values of the Registers

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    REGISTERS
        The values of all the Registers
    """
    return self.REGISTERS


def read_all_command_registers(self):
    """
    Return the values of all of the Command Registers

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    COMMAND_REGISTERS
        The values of all the Command Registers
    """
    return self.COMMAND_REGISTERS


def read_all_ram(self):
    """
    Return the values of all the locations of RAM

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    RAM
        The values of all the locations of RAM
    """
    return self.RAM


def read_all_rom(self):
    """
    Return the values of all the locations of ROM

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ROM
        The values of all the locations of ROM
    """
    return self.ROM


def read_all_pram(self):
    """
    Return the values of all the locations of PRAM

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    PRAM
        The values of all the locations of PRAM
    """
    return self.PRAM


def read_all_stack(self):
    """
    Return the complete  stack

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    STACK
        The stack as a list
    """
    return self.STACK


def read_accumulator(self):
    """
    Return the value of the accumulator

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ACCUMULATOR
        The 4-bit value of the accumulator
    """
    return self.ACCUMULATOR


def read_all_rom_ports(self):
    """
    Return the values of all the ROM ports

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ROM_PORT
        The values of all the ROM ports
    """
    return self.ROM_PORT


def read_all_ram_ports(self):
    """
    Return the values of all the RAM ports

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    RAM_PORT
        The values of all the RAM ports
    """
    return self.RAM_PORT


def read_current_ram_bank(self):
    """
    Return the current RAM bank i.e. the one selected  by the SRC

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    CURRENT_RAM_BANK
        The current RAM bank value
    """
    return self.CURRENT_RAM_BANK


def read_carry(self):
    """
    Return the value of the carry flag

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    CARRY
        A 1 or a 0 (the value of the carry flag)
    """
    return self.CARRY


def read_pin10(self):
    """
    Return the value of PIN 10 on the i4004 chip (simulated test pin)

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    PIN_10_SIGNAL_TEST
        The value of the simulated test pin
    """
    return self.PIN_10_SIGNAL_TEST


def read_wpm_counter(self):
    """
    Return the value of the WPM counter ("LEFT" or "RIGHT") - internally
    keeps track of which 4-bits of a register will be transferred with the
    WPM instruction

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    WPM_COUNTER
        The value of the WPM counter
    """
    return self.WPM_COUNTER


def read_acbr(self):
    """
    Return the value of the ACBR interim property used for
    swapping out accumulator with register contents during
    an XCH instruction

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ACBR
        The value of the ACBR interim property
    """
    return self.ACBR


def read_program_counter(self):
    """
    Return the value of the program counter

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    PROGRAM_COUNTER
        The value of the program counter (current instruction)
    """
    return self.PROGRAM_COUNTER


def read_stack_pointer(self):
    """
    Return the value of the stack pointer

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    STACK_POINTER
        The value of the stack pointer used to determine where in the stack
        return addresses to  subroutines (for example) are
    """
    return self.STACK_POINTER


def read_all_status_characters(self):
    """
    Return the values of all the RAM status characters

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    STATUS_CHARACTERS
        The values of all the RAM status characters
    """
    return self.STATUS_CHARACTERS
