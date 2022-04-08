"""Initialisation methods."""

def init_registers(self) -> None:
    """
    Initialise the registers with zeroes.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    """
    for _ in range(self.NO_REGISTERS):
        self.REGISTERS.append(0)
