"""Carry methods."""


def read_carry(self) -> int:
    """
    Return the value of the carry flag.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    CARRY
        A 1 or a 0 (the value of the carry flag)

    """
    return self.CARRY


def read_complement_carry(self) -> int:
    """
    Reads the complement of the carry bit, but doesn't change the value.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
        The complement of the carry bit

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    return 1 if self.CARRY == 0 else 0


def reset_carry(self) -> int:
    """
    Resets the carry bit.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.CARRY
        The carry bit

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    # Reset the carry bit
    self.CARRY = 0
    return self.CARRY


def set_carry(self) -> int:
    """
    Set the carry bit.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.CARRY
        The carry bit

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    # Set the carry bit
    self.CARRY = 1
    return self.CARRY
