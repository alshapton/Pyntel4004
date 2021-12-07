"""Program Counter methods."""

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

from hardware.exceptions import  ProgramCounterOutOfBounds  # noqa


def increment_pc(self, words: int) -> int:
    """
    Increment the Program Counter by a specific number of words.

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
    N/A

    """
    if self.PROGRAM_COUNTER + words > self.MEMORY_SIZE_RAM:
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' +
                                        str(self.PROGRAM_COUNTER + words))
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + words
    return self.PROGRAM_COUNTER


def inc_pc_by_page(self, pc: int) -> int:
    """
    Retrieve the pc's new value after being incremented by a page.

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
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


def is_end_of_page(self, address: int, word: int) -> bool:
    """
    Determine if an instruction is located at the end of a memory page.

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
    N/A

    """
    page = address // self.PAGE_SIZE
    location = address - (page * self.PAGE_SIZE)
    word = word - 1
    return (location - word) == self.PAGE_SIZE - 1


def read_program_counter(self) -> int:
    """
    Return the value of the program counter.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    PROGRAM_COUNTER
        The value of the program counter (current instruction)

    """
    return self.PROGRAM_COUNTER
