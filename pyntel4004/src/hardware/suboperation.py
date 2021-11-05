#  Sub-operation methods

from .exceptions import AddressOutOf8BitRange, \
    IncompatibleChunkBit, \
    InvalidBitValue, InvalidChunkValue, \
    InvalidCommandRegisterContent, InvalidCommandRegisterFormat, \
    InvalidPin10Value, InvalidRegister, \
    InvalidRegisterPair, NotABinaryNumber, \
    ProgramCounterOutOfBounds, ValueOutOfRangeForBits, \
    ValueOutOfRangeForStack, ValueTooLargeForAccumulator, \
    ValueTooLargeForRegister, ValueTooLargeForRegisterPair  # noqa


def rdx(self, character):
    """
    Name:           Read RAM status character X

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

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


def encode_command_register(chip, register, address, shape):
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


def decode_command_register(command_register, shape):
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


def convert_to_absolute_address(self, rambank, chip, register, address):
    """
    Convert a rambank, chip, register and address to an absolute 0 - 4095
    RAM adddress

    Parameters
    ----------
    self : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    rambank: integer, mandatory
        The currently selected RAM bank

    chip : integer, mandatory
        1 of 4 chips

    register : integer, mandatory
        1 of 4 registers

    address : integer, mandatory
        address within a page

    Returns
    -------
    absolute_address
        The address from 0 - 4095
    """
    absolute_address = (rambank * self.RAM_BANK_SIZE) + \
        (chip * self.RAM_CHIP_SIZE) + \
        (register * self.RAM_REGISTER_SIZE) + address
    return absolute_address


def split_address8(address):
    """
    Split a supplied decimal address into 2 4-bit words

    Parameters
    ----------
    address: int, mandatory
        An 8-bit address in decimal format

    Returns
    -------
    address_left: str
        left-most 4 bits

    address_right: str
        right-most 4 bits

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    if (address < 0) or (address > 255):
        raise AddressOutOf8BitRange('Address: ' + str(address))

    address_left = bin(address)[2:].zfill(8)[:4]
    address_right = bin(address)[2:].zfill(8)[4:]
    return address_left, address_right


def set_carry(self):
    """
    Set the carry bit

    Parameters
    ----------
    self: processor, mandatory
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
    self: processor, mandatory
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
    self: processor, mandatory
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
    self: processor, mandatory
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
    if (register < 0) or (register > 15):
        raise InvalidRegister('Register: ' + str(register))

    if value > 15:
        raise ValueTooLargeForRegister('Register: ' + str(register) + ',Value: ' + str(value))  # noqa
    self.REGISTERS[register] = value
    return value


def read_register(self, register: int):
    """
    Read a specific register

    Parameters
    ----------
    self: processor, mandatory
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
    if (register < 0) or (register > 15):
        raise InvalidRegister('Register:' + str(register))

    return self.REGISTERS[register]


def insert_registerpair(self, registerpair: int, value: int):
    """
    Insert a value into a specific register

    Parameters
    ----------
    self: processor, mandatory
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


def read_registerpair(self, registerpair: int):
    """
    Read a specific register pair

    Parameters
    ----------
    self: processor, mandatory
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
    self: processor, mandatory
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
    if self.PROGRAM_COUNTER + words > self.MEMORY_SIZE_RAM:
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
    self: processor, mandatory
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
    if pc + self.PAGE_SIZE > self.MEMORY_SIZE_RAM:
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' + str(pc + self.PAGE_SIZE))
    # Point the program counter to 1 page on
    pc = pc + self.PAGE_SIZE - 1
    return pc


def is_end_of_page(self, address: int, word: int):
    """
    Determine if an instruction is located at the end of a memory page

    Parameters
    ----------
    self: processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    address: int, mandatory
        Base address of the instruction

    word: int, mandatory
        Number of words in the instruction

    Returns
    -------
    True if the instruction is at the end of the memory page
    False if the instruction is not at the end of the memory page

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    page = address // self.PAGE_SIZE
    location = address - (page * self.PAGE_SIZE)
    word = word - 1
    return (location - word) == self.PAGE_SIZE - 1


def increment_register(self, register: int):
    """
    Increment the value in a register by 1

    Parameters
    ----------
    self: processor, mandatory
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
    ------
    N/A

    """
    if register < 0 or register > (self.NO_REGISTERS - 1):
        raise InvalidRegister('Register: ' + str(register))

    self.REGISTERS[register] = self.REGISTERS[register] + 1
    if self.REGISTERS[register] > self.MAX_4_BITS:
        self.REGISTERS[register] = 0
    return self.REGISTERS[register]


def write_pin10(self, value: int):
    """
    Write to pin 10 (reset pin)

    Parameters
    ----------
    self: processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    value: int, mandatory
        value for pin 10

    Returns
    -------
    True
        if the value is set successfully

    Raises
    ------
    InvalidPin10Value

    Notes
    ------
    N/A

    """
    if value in (0, 1):
        self.PIN_10_SIGNAL_TEST = value
        return True
    raise InvalidPin10Value('PIN 10 attempted to be set to ' + str(value))


def write_ram_status(self, char: int):
    """
    Write to a RAM status character

    Parameters
    ----------
    self: processor, mandatory
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

# Miscellaneous read/write operations


def write_to_stack(self, value: int):
    """
    Write to the stack

    Parameters
    ----------
    self: processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    value: int, mandatory
        value to write to the stack

    Returns
    -------
    True
        if the value is written to the stack successfully

    Raises
    ------
    ValueOutOfRangeForStack

    Notes
    ------
    The stack pointer begins at 2, and then moves toward 0

      After 2 writes         After 3 writes         After 3 writes
      +------------+ +------------+ +------------+
      |     a | |      a | <--SP | d |
      |     b | |      b | |      b | <---SP
      | | <--SP | c | |      c |
      +------------+ +------------+ +------------+

    After 3 writes, address "a" is lost
    """
    if (value < 0 or value > 4095):
        raise ValueOutOfRangeForStack(' Value: ' + str(value))

    self.STACK[self.STACK_POINTER] = value
    self.STACK_POINTER = self.STACK_POINTER - 1
    if self.STACK_POINTER == -1:
        self.STACK_POINTER = 2
    return True


def read_from_stack(self):
    """
    Read from the stack

    Parameters
    ----------
    self: processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    value
        the 12-bit number read from the stack

    Raises
    ------
    N/A

    Notes
    ------
    The stack pointer begins at 2, and then moves toward 0

        First Read             Second Read          Third Read
        +------------+ +------------+ +------------+
        |     d | <--SP | d | |      d |
        |     b | |      b | |      b | <---SP
        |     c | |      c | <--SP | c |
        +------------+ +------------+ +------------+

    """
    if self.STACK_POINTER == 2:
        self.STACK_POINTER = 0
    else:
        self.STACK_POINTER = self.STACK_POINTER + 1
    value = self.STACK[self.STACK_POINTER]

    return value

# Utility operations


def ones_complement(value: str, bits: int):
    """
    Converts a decimal value into its one's compliment value
    of a specified bit length

    Parameters
    ----------
    value: int: mandatory
        decimal value to convert

    bits: int, mandatory
        number of bits required for the conversion

    Returns
    -------
    The one's compliment binary value of the supplied decimal value.

    Raises
    ------
    InvalidBitValue: When a bit value of not 4, 8 or 12 is specified
    ValueOutOfRangeForBits: If the value supplied is either negative or is
                             out of range of the number of bits requested

    Notes
    ------
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (value > ((2 ** bits) - 1)) or (value < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(value) +
                                     ' Bits: ' + str(bits))

    # Perform a one's complement
    # i.e. invert all the bits

    binary = bin(value)[2:].zfill(bits)
    ones = ''
    for x in range(bits):
        if binary[x] == '1':
            ones = ones + '0'
        else:
            ones = ones + '1'
    return ones


def convert_decimal_to_n_bit_slices(bits: int, chunk: int, decimal: int, result: str = 'b'):  # noqa
    """
    Converts a decimal value into several binary or decimal values of specific
    bit lengths

    Parameters
    ----------
    bits: int, mandatory
        number of bits of the source data

    chunk: int, mandatory
        number of bits required per chunk

    decimal: int: mandatory
        decimal value to convert

    result: str: mandatory
        'd' will generate a decimal output
        'b' will generate a binary output

    Returns
    -------
    The binary value of the supplied decimal value.

    Raises
    ------
    IncompatibleChunkBit: When the chunks do not fit exactly within the bits
    InvalidBitValue: When a bit value of not 4, 8 or 12 is specified
    InvalidChunkValue: When a chunk value of not 4, 8 or 12 is specified
    ValueOutOfRangeForBits: If the value supplied is either negative or is
                             out of range of the number of bits requested

    Notes
    ------
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (chunk not in [2, 4, 8, 12]):
        raise InvalidChunkValue(' Chunk: ' + str(chunk))

    if bits % chunk != 0:
        raise IncompatibleChunkBit(' Bits: ' + str(bits) +
                                   ' Chunk: ' + str(chunk))

    if (decimal > ((2 ** bits) - 1)) or (decimal < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(decimal) +
                                     ' Bits: ' + str(bits))

    binary = decimal_to_binary(bits, decimal)
    chunks = [binary[i:i+chunk] for i in range(0, len(binary), chunk)]
    if result != 'b':
        decimals = []
        for element in chunks:
            decimals.append(binary_to_decimal(element))
        chunks = decimals
    return chunks


def decimal_to_binary(bits: int, decimal: int):
    """
    Converts a decimal value into a binary value of a specified bit length

    Parameters
    ----------
    bits: int, mandatory
        number of bits required for the conversion

    decimal: int: mandatory
        decimal value to convert

    Returns
    -------
    The binary value of the supplied decimal value.

    Raises
    ------
    InvalidBitValue: When a bit value of not 4, 8 or 12 is specified
    ValueOutOfRangeForBits: If the value supplied is either negative or is
                             out of range of the number of bits requested

    Notes
    ------
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (decimal > ((2 ** bits) - 1)) or (decimal < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(decimal) +
                                     ' Bits: ' + str(bits))

    # Convert decimal to binary
    binary = bin(decimal)[2:].zfill(bits)
    return binary


def binary_to_decimal(binary: str):
    """
    Converts a string value(which must be in binary form) to
    a decimal value

    Parameters
    ----------
    binary: str, mandatory
        a string which represents the binary value

    Returns
    -------
    The decimal value of the supplied binary value

    Raises
    ------
    NotABinaryNumber: When a non-binary number is supplied

    Notes
    ------
    N/A

    """
    if len(binary) == 0:
        binary = '<empty>'
        raise NotABinaryNumber('"' + binary + '"')

    if len(binary.replace('0', '').replace('1', '')) != 0:
        raise NotABinaryNumber('"' + binary + '"')

    # Convert binary to decimal
    return int(binary, 2)


def flip_wpm_counter(self):
    """
    Two WPM instructions must always appear in close succession; that is ,
    each time one WPM instruction references a half byte of program RAM
    as indicated by an SRC address, another WPM must access the other half
    byte before the SRC address is altered.
    This internal counter keeps track of which half-byte is being accessed.
    If only one WPM occurs, this counter will be out of sync with the
    program and errors will occur.

    Parameters
    ----------
    self: processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.WPM_COUNTER
        The flipped value of the WPM counter(either "LEFT" or "RIGHT")

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    if self.WPM_COUNTER == 'LEFT':
        self.WPM_COUNTER = 'RIGHT'
    else:
        self.WPM_COUNTER = 'LEFT'
    return self.WPM_COUNTER


def check_overflow(self):
    """
    Check for an overflow is detected
    i.e. the result is more than a 4-bit number(MAX_4_BITS)

    If there is an overflow detected, set the carry bit,
    otherwise reset the carry bit.

    Parameters
    ----------
    self: processor, mandatory
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
    if self.ACCUMULATOR > self.MAX_4_BITS:
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
    self: processor, mandatory
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
    if value > self.MAX_4_BITS:
        raise ValueTooLargeForAccumulator(' Value: ' + str(value))
    self.ACCUMULATOR = value
    return value
