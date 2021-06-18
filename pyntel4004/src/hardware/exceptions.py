class IncompatibleChunkBit(Exception):
    """
    Raised when it a bit value is not a multiple of the chunk value
    when attempting to convert from a decimal number to chunked numbers.
    """


class InvalidBitValue(Exception):
    """
    Raised when it a bit value of other than 4,8 or 12 is used to convert
    a decimal number to a binary number.
    """


class InvalidChunkValue(Exception):
    """
    Raised when it a chunk value of other than 4,8 or 12 is used to convert
    a binary number into chunk.
    """


class InvalidEndOfPage(Exception):
    """Raised when it is impossible to determine the end of a page."""


class InvalidPin10Value(Exception):
    """Raised when the value of PIN 10 is attempted to be set to NOT 0 or 1."""


class InvalidRamBank(Exception):
    """Raised when the attempting to select a RAM bank > 7."""


class InvalidRegister(Exception):
    """Raised when an invalid register is supplied."""


class InvalidRegisterPair(Exception):
    """Raised when an invalid register pair is supplied."""


class NotABinaryNumber(Exception):
    """Raised when a supplied binary number is NOT binary."""


class ProgramCounterOutOfBounds(Exception):
    """Raised when the program counter is forced beyond the end of memory."""


class ValueTooLargeForAccumulator(Exception):
    """Raised when the value for the Accumulator is too large."""


class ValueOutOfRangeForBits(Exception):
    """
    Raised when the value to be converted from decimal to binary
    is too large for the number of bits supplied.
    """


class ValueTooLargeForRegister(Exception):
    """Raised when the value for a register is too large."""


class ValueTooLargeForRegisterPair(Exception):
    """Raised when the value for a register pair is too large."""


class ValueOutOfRangeForStack(Exception):
    """Raised when the value for the Stack is out of Range."""
