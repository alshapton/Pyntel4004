#  Sub-operation methods

from .exceptions import ValueTooLargeForRegister, InvalidEndOfPage, \
    ProgramCounterOutOfBounds, InvalidPin10Value, NotABinaryNumber, \
    InvalidRegister, InvalidRegisterPair, ValueTooLargeForRegisterPair, \
    ValueTooLargeForAccumulator # noqa


def set_carry(self):
    """
    Set the carry bit

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.CARRY
        The carry bit

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    # Set the carry bit
    self.CARRY = 1
    return self.CARRY


def reset_carry(self):
    """
    Resets the carry bit

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.CARRY
        The carry bit

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    # Reset the carry bit
    self.CARRY = 0
    return self.CARRY


def read_complement_carry(self):
    """
    Reads the complement of the carry bit, but doesn't change the value

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
        The complement of the carry bit

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    return 1 if self.CARRY == 0 else 0


def insert_register(self, register: int, value: int):
    """
    Insert a value into a specific register

    Parameters
    ----------
    self : processor, mandatory
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
    ------
    N/A

    """
    if (register >= 0 and register <= 15):
        pass
    else:
        raise InvalidRegister('Register: ' + str(register))

    if (value > 15):
        raise ValueTooLargeForRegister('Register: ' + str(register) + ',Value: ' + str(value)) # noqa
    else:
        self.REGISTERS[register] = value
    return value


def read_register(self, register: int):
    """
    Read a specific register

    Parameters
    ----------
    self : processor, mandatory
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
    ------
    N/A

    """
    if (register >= 0 and register <= 15):
        pass
    else:
        raise InvalidRegister('Register:' + str(register))

    return self.REGISTERS[register]


def insert_registerpair(self, registerpair: int, value: int):
    """
    Insert a value into a specific register

    Parameters
    ----------
    self : processor, mandatory
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
    ------
    N/A

    """
    if (registerpair < 0 or registerpair > 7):
        raise InvalidRegisterPair('Register Pair: ' +
                                  str(registerpair))
    if (value > 256):
        raise ValueTooLargeForRegisterPair('Register Pair: ' +
                                           str(registerpair) +
                                           ',Value: ' +
                                           str(value))
    else:
        # Convert a register pair into a base register for insertion
        base_register = registerpair * 2
        self.insert_register(base_register, (value >> 4) & 15)   # Bit-shift right and remove low bits   # noqa
        self.insert_register(base_register + 1, value & 15)      # Remove low bits                       # noqa
    return value


def read_registerpair(self, registerpair: int):
    """
    Read a specific register pair

    Parameters
    ----------
    self : processor, mandatory
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
    ------
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


def increment_pc(self, words: int):
    """
    Increment the Program Counter by a specific number of words

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    words: int, mandatory
        The number of words to increment the Program Counter by

    Returns
    -------
    self.PROGRAM_COUNTER
        The new value of the Program Counter

    Raises
    ------
    ProgramCounterOutOfBounds

    Notes
    ------
    N/A

    """
    if (self.PROGRAM_COUNTER + words > self.MEMORY_SIZE_RAM):
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' +
                                        str(self.PROGRAM_COUNTER + words))
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + words
    return self.PROGRAM_COUNTER


def inc_pc_by_page(self, pc: int):
    """
    Retrieve the Program Counter's new value after being incremented
    by a page

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    pc: int, mandatory
        Current value of Program Counter

    Returns
    -------
    pc
        The new value of the Program Counter

    Raises
    ------
    ProgramCounterOutOfBounds

    Notes
    ------
    This function DOES NOT MODIFY the program counter, simply
    calculates the new  value of the counter. It is up to the
    calling  function to determine what to  do with the value.

    """
    if (pc + self.PAGE_SIZE > self.MEMORY_SIZE_RAM):
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' + str(pc + self.PAGE_SIZE))
    # Point the program counter to 1 page on
    pc = pc + self.PAGE_SIZE
    return pc


def is_end_of_page(self, address: int, word: int):
    """
    Determine if an instruction is located at the end of a memory page

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    address: int, mandatory
        Base address of the instruction

    word: int, mandatory
        Number of words in the instruction

    Returns
    -------
    True        if the instruction is at the end of the memory page
    False       if the instruction is not at the end of the memory page

    Raises
    ------
    InvalidEndOfPage

    Notes
    ------
    N/A

    """
    page = address // self.PAGE_SIZE
    location = address - (page * self.PAGE_SIZE)
    word = word - 1
    if ((location - word) == self.PAGE_SIZE - 1):
        return True
    else:
        return False
    raise InvalidEndOfPage('Address:' + str(address))
    return None


def increment_register(self, register: int):
    self.REGISTERS[register] = self.REGISTERS[register] + 1
    if (self.REGISTERS[register] > self.MAX_4_BITS):
        self.REGISTERS[register] = 0
    return None


def write_pin10(self, value: int):
    if (value == 0 or value == 1):
        self.PIN_10_SIGNAL_TEST = value
        return True
    else:
        raise InvalidPin10Value('PIN 10 attempted to be set to ' + str(value))


def write_ram_status(self, char: int):
    value = self.read_accumulator()
    crb = self.read_current_ram_bank()
    address = self.COMMAND_REGISTERS[crb]
    chip = int(bin(int(address))[2:].zfill(8)[:2], 2)
    register = int(bin(int(address))[2:].zfill(8)[2:4], 2)
    self.STATUS_CHARACTERS[crb][chip][register][char] = value
    return True

# Miscellaneous read/write operations


def write_to_stack(self, value: int):
    # Note that the stack pointer begins at 2, and then moves toward 0
    #
    #  After 2 writes         After 3 writes         After 3 writes
    #  +------------+         +------------+         +------------+
    #  |     a      |         |      a     |  <--SP  |      d     |
    #  |     b      |         |      b     |         |      b     |  <---SP
    #  |            |  <--SP  |      c     |         |      c     |
    #  +------------+         +------------+         +------------+
    #
    # Note that after 3 writes, address "a" is lost

    self.STACK[self.STACK_POINTER] = value
    self.STACK_POINTER = self.STACK_POINTER - 1
    if (self.STACK_POINTER == -1):
        self.STACK_POINTER = 2
    return None


def read_from_stack(self):
    # Note that the stack pointer begins at 2, and then moves toward 0
    #
    #    First Read             Second Read          Third Read
    #    +------------+        +------------+        +------------+
    #    |     d      |  <--SP |      d     |        |      d     |
    #    |     b      |        |      b     |        |      b     |  <---SP
    #    |     c      |        |      c     |  <--SP |      c     |
    #    +------------+        +------------+        +------------+
    #

    if (self.STACK_POINTER == 2):
        self.STACK_POINTER = 0
    else:
        self.STACK_POINTER = self.STACK_POINTER + 1
    value = self.STACK[self.STACK_POINTER]

    return value

# Utility operations


def ones_complement(self, value: str):
    # ones = str(~ int(value))[2:].zfill(4)   # Maybe simplify with this ?
    # Perform a one's complement
    # i.e. invert all the bits
    binary = bin(value)[2:].zfill(4)
    ones = ''
    for x in range(4):
        if (binary[x] == '1'):
            ones = ones + '0'
        else:
            ones = ones + '1'
    return ones


def decimal_to_binary(self, decimal: int):
    # Convert decimal to binary
    binary = bin(decimal)[2:].zfill(4)
    return binary


def binary_to_decimal(self, binary: str):
    """
    Converts a string value (which must be in binary form) to
    a decimal value

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    binary : str, mandatory
        a string which represents the binary value
    Returns
    -------
    The decimal value of the supplied binary value

    Raises
    ------
    NotABinaryNumber        : When a non-binary number is supplied

    Notes
    ------
    N/A

    """
    if len(binary.replace('0', '').replace('1', '') != 0):
        raise NotABinaryNumber('"' + binary + '"')

    # Convert binary to decimal
    return int(binary, 2)


def flip_wpm_counter(self):
    """
    Two WPM instructions must always appear in close succession; that is,
    each time one WPM instruction references a half byte of program RAM
    as indicated by an SRC address, another WPM must access the other half
    byte before the SRC address is altered.
    This internal counter keeps track of which half-byte is being accessed.
    If only one WPM occurs, this counter will be out of sync with the
    program and errors will occur.

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.WPM_COUNTER
        The flipped value of the WPM counter (either "LEFT" or "RIGHT")

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    if (self.WPM_COUNTER == 'LEFT'):
        self.WPM_COUNTER = 'RIGHT'
    else:
        self.WPM_COUNTER = 'LEFT'
    return self.WPM_COUNTER


def check_overflow(self):
    """
    Check for an overflow is detected
    i.e. the result is more than a 4-bit number (MAX_4_BITS)

    If there is an overflow detected, set the carry bit,
    otherwise reset the carry bit.

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.ACCUMULATOR
        The value of the accumulator after adjusting for overflow
    self.CARRY
        The carry bit

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """

    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS + 1
        self.set_carry()
    else:
        self.reset_carry()
    return self.ACCUMULATOR, self.CARRY


def set_accumulator(self, value: int):
    """
    Insert a value into the Accumulator

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    value: int, mandatory
        The value to insert

    Returns
    -------
    value
        The value of the accumulator

    Raises
    ------
    ValueTooLargeForAccumulator

    Notes
    ------
    N/A

    """

    if (value > self.MAX_4_BITS):
        raise ValueTooLargeForAccumulator(' Value: ' + str(value))
    else:
        self.ACCUMULATOR = value
    return value
