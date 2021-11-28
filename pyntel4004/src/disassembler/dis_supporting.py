"""Disassembly process supporting functions."""
# Import i4004 processor
from hardware.processor import Processor  # noqa

# Shared imports
from shared.shared import get_opcodeinfobyopcode  # noqa


def disassemble_instruction(chip, _tps, opcode):
    """
    Process a single instruction.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    _tps: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    opcode: str, mandatory
        Opcode of the current instruction

    Returns
    -------
    exe: str
        pre-formatted exe mnemonic ready for processing

    opcode: str
        Opcode of the current instruction

    words, int
        The number of words an instruction uses

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    opcode = _tps[chip.PROGRAM_COUNTER]
    oi = get_opcodeinfobyopcode(chip, opcode)
    words = (oi['words'])
    exe = get_opcodeinfobyopcode(chip, opcode)['mnemonic']
    return exe, opcode, words
