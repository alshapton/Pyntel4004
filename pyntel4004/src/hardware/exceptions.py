class ValueTooLargeForRegister(Exception):
    """Raised when the value for a register is too large"""
    pass


class InvalidEndOfPage(Exception):
    """Raised when it is impossible to determine the end of a page """
    pass


class ProgramCounterOutOfBounds(Exception):
    """Raised when the program counter is forced beyond the end of memory """
    pass


class InvalidPin10Value(Exception):
    """Raised when the value of PIN 10 is attempted to be set to NOT 0 or 1 """
    pass


class InvalidRamBank(Exception):
    """Raised when the attempting to select a RAM bank > 7 """
    pass
