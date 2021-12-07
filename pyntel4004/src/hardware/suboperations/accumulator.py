"""Accumulator methods."""

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

# Import typing library
from typing import Tuple  # noqa

from hardware.exceptions import  ValueTooLargeForAccumulator  # noqa


def check_overflow(self) -> Tuple[int, int]:
    """
    Check if an overflow is detected.

    If the result is more than a 4-bit number(MAX_4_BITS),
    then an overflow is detected.

    If there is an overflow detected, set the carry bit,
    otherwise reset the carry bit.

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
    N/A

    """
    if self.ACCUMULATOR > self.MAX_4_BITS:
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS + 1
        self.set_carry()
    else:
        self.reset_carry()
    return self.ACCUMULATOR, self.CARRY


def read_acbr(self) -> int:
    """
    Return the value of the ACBR interim property.

    This is used for swapping out accumulator with
    register contents during an XCH instruction

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ACBR
        The value of the ACBR interim property

    """
    return self.ACBR


def read_accumulator(self) -> int:
    """
    Return the value of the accumulator.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    ACCUMULATOR
        The 4-bit value of the accumulator

    """
    return self.ACCUMULATOR


def set_accumulator(self, value: int) -> int:
    """
    Insert a value into the Accumulator.

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
    N/A

    """
    if value > self.MAX_4_BITS:
        raise ValueTooLargeForAccumulator(' Value: ' + str(value))
    self.ACCUMULATOR = value
    return value
