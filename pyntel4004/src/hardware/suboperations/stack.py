"""Stack methods."""
# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

from hardware.exceptions import ValueOutOfRangeForStack  # noqa


def read_all_stack(self) -> list:
    """
    Return the complete stack.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    STACK
        The stack as a list

    """
    return self.STACK


def read_from_stack(self) -> int:
    """
    Read from the stack.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    value
        the 12-bit number read from the stack

    Raises
    ------
    N/A

    Notes
    -----
    The stack pointer begins at 2, and then moves toward 0

        First Read             Second Read          Third Read
        +------------+       +------------+        +------------+
        |     d      | <--SP |      d     |        |      d     |
        |     b      |       |      b     |        |      b     | <---SP
        |     c      |       |      c     | <--SP  |      c     |
        +------------+       +------------+        +------------+

    """
    if self.STACK_POINTER == 2:
        self.STACK_POINTER = 0
    else:
        self.STACK_POINTER = self.STACK_POINTER + 1
    value = self.STACK[self.STACK_POINTER]

    return value


def read_stack_pointer(self) -> int:
    """
    Return the value of the stack pointer.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    STACK_POINTER
        The value of the stack pointer used to determine where in the stack
        return addresses to  subroutines (for example) are

    """
    return self.STACK_POINTER


def write_to_stack(self, value: int) -> bool:
    """
    Write to the stack.

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
    The stack pointer begins at 2, and then moves toward 0

      After 2 writes         After 3 writes         After 3 writes
      +------------+         +------------+        +------------+
      |     a      |         |      a     | <--SP  |      d     |
      |     b      |         |      b     |        |      b     | <---SP
      |            | <--SP   |      c     |        |      c     |
      +------------+         +------------+        +------------+

    After 3 writes, address "a" is lost

    """
    if (value < 0 or value > 4095):
        raise ValueOutOfRangeForStack(' Value: ' + str(value))

    self.STACK[self.STACK_POINTER] = value
    self.STACK_POINTER = self.STACK_POINTER - 1
    if self.STACK_POINTER == -1:
        self.STACK_POINTER = 2
    return True
