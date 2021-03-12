class ValueTooLargeForRegister(Exception):
    """Raised when the value for a register is too large"""
    pass


class InvalidEndOfPage(Exception):
    """Raised when it is impossible to determine the end of a page """
    pass
