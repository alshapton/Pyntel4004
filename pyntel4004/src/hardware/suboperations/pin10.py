"""PIN 10 methods."""

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')


from hardware.exceptions import InvalidPin10Value  # noqa


def read_pin10(self) -> int:
    """
    Return the value of PIN 10 on the i4004 chip (simulated test pin).

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    PIN_10_SIGNAL_TEST
        The value of the simulated test pin

    """
    return self.PIN_10_SIGNAL_TEST


def write_pin10(self, value: int) -> bool:
    """
    Write to pin 10 (reset pin).

    Parameters
    ----------
    self: Processor, mandatory
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
    -----
    N/A

    """
    if value in (0, 1):
        self.PIN_10_SIGNAL_TEST = value
        return True
    raise InvalidPin10Value('PIN 10 attempted to be set to ' + str(value))
