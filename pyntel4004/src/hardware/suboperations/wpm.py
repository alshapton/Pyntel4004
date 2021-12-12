"""WPM methods."""


def read_wpm_counter(self) -> str:
    """
    Return the value of the WPM counter ("LEFT" or "RIGHT").

    Internally keeps track of which 4-bits of a register will
    be transferred with the WPM instruction

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    WPM_COUNTER
        The value of the WPM counter

    """
    return self.WPM_COUNTER


def flip_wpm_counter(self) -> str:
    """
    Flip the WPM counter.

    Two WPM instructions must always appear in close succession; that is,
    each time one WPM instruction references a half byte of program RAM
    as indicated by an SRC address, another WPM must access the other half
    byte before the SRC address is altered.
    This internal counter keeps track of which half-byte is being accessed.
    If only one WPM occurs, this counter will be out of sync with the
    program and errors will occur.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.WPM_COUNTER
        The flipped value of the WPM counter(either "LEFT" or "RIGHT")

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if self.WPM_COUNTER == 'LEFT':
        self.WPM_COUNTER = 'RIGHT'
    else:
        self.WPM_COUNTER = 'LEFT'
    return self.WPM_COUNTER
