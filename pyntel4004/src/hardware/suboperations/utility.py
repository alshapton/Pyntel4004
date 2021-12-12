"""Utility Operations."""
# Import typing library
from typing import Tuple

from hardware.exceptions import AddressOutOf8BitRange, \
    IncompatibleChunkBit, \
    InvalidBitValue, InvalidChunkValue, \
    NotABinaryNumber, ValueOutOfRangeForBits  # noqa


def binary_to_decimal(binary: str) -> int:
    """
    Converts a string value(which must be in binary form) to a decimal value.

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
    -----
    N/A

    """
    if len(binary) == 0:
        binary = '<empty>'
        raise NotABinaryNumber('"' + binary + '"')

    if len(binary.replace('0', '').replace('1', '')) != 0:
        raise NotABinaryNumber('"' + binary + '"')

    # Convert binary to decimal
    return int(binary, 2)


def convert_decimal_to_n_bit_slices(bits: int, chunk: int,
                                    decimal: int, result: str = 'b') -> str:
    """
    Converts a decimal to several binary or decimal values of specific lengths.

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
    -----
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


def convert_to_absolute_address(self, rambank: int, chip: int,
                                register: int, address: int) -> int:
    """
    Convert a rambank, chip, register and address to an absolute RAM address.

    Parameters
    ----------
    self : Processor, mandatory
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

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    absolute_address = (rambank * self.RAM_BANK_SIZE) + \
        (chip * self.RAM_CHIP_SIZE) + \
        (register * self.RAM_REGISTER_SIZE) + address
    return absolute_address


def decimal_to_binary(bits: int, decimal: int) -> str:
    """
    Converts a decimal value into a binary value of a specified bit length.

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
    -----
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


def ones_complement(value: str, bits: int) -> str:
    """
    Converts a decimal into a one's compliment value of a specified bit length.

    Parameters
    ----------
    value: str: mandatory
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
    -----
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (int(value) > ((2 ** bits) - 1)) or (int(value) < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(value) +
                                     ' Bits: ' + str(bits))

    # Perform a one's complement
    # i.e. invert all the bits

    binary = decimal_to_binary(bits, int(value))
    # binary = str(bin(value))[2:].zfill(bits)
    ones = ''
    for x in range(bits):
        if binary[x] == '1':
            ones = ones + '0'
        else:
            ones = ones + '1'
    return ones


def split_address8(address: int) -> Tuple[str, str]:
    """
    Split a supplied decimal address into 2 4-bit words.

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
    -----
    N/A

    """
    if (address < 0) or (address > 255):
        raise AddressOutOf8BitRange('Address: ' + str(address))

    address_left = bin(address)[2:].zfill(8)[:4]
    address_right = bin(address)[2:].zfill(8)[4:]
    return address_left, address_right
