"""Disassembly process supporting functions."""
# Import i4004 processor
from hardware.processor import Processor  # noqa

# Shared imports
from shared.shared import get_opcodeinfobyopcode, retrieve_program  # noqa


def disassemble_mnemonic(chip: Processor, _tps, exe, opcode, words):
    """
    Formulate the opcodes into mnemonics ready for execution.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    exe: str, mandatory
        pre-formatted exe mnemonic ready for processing

    _tps: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    opcode: str, mandatory
        Opcode of the current instruction

    words: int, mandatory
        The number of words an instruction uses

    Returns
    -------
    exe: str
        A correctly formed, ready-for execution mnemonic

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    custom_opcode = False
    cop = ''

    # Only mnemonic with 2 characters - fix
    if exe[:3] == 'ld ':
        exe = exe[:2] + exe[3:]

    # Ensure that the correct arguments are passed to the operations
    if exe[:3] == 'fim':
        custom_opcode = True
        value = str(_tps[chip.PROGRAM_COUNTER + 1])
        cop = exe.replace('data8', value)
        exe = exe.replace('p', '').replace('data8)', '') + value + ')'

    if exe[:3] == 'isz':
        # Remove opcode from 1st byte to get register
        register = bin(_tps[chip.PROGRAM_COUNTER] & 15)[2:].zfill(8)[4:]
        address = str(_tps[chip.PROGRAM_COUNTER + 1])
        exe = 'isz(' + str(int(register, 2)) + ',' + str(address) + ')'

    if exe[:4] == 'jcn(':
        custom_opcode = True
        address = _tps[chip.PROGRAM_COUNTER + 1]
        conditions = (bin(_tps[chip.PROGRAM_COUNTER])[2:].zfill(8)[4:])
        b10address = str(address)
        cop = exe.replace('address8', b10address)
        exe = exe[:4] + str(int(conditions, 2)) + ',' + b10address + ')'
        opcode = str(_tps[chip.PROGRAM_COUNTER]) + ', ' \
            + str(_tps[chip.PROGRAM_COUNTER + 1])

    if exe[:4] in ('jun(', 'jms('):
        custom_opcode = True
        # Remove opcode from 1st byte
        hvalue = bin(_tps[chip.PROGRAM_COUNTER] &
                     0xffff0000)[2:].zfill(8)[:4]
        lvalue = bin(_tps[chip.PROGRAM_COUNTER + 1])[2:].zfill(8)
        whole_value = str(int(hvalue + lvalue, 2))
        cop = exe.replace('address12', whole_value)
        exe = exe[:4] + whole_value + ')'
        opcode = str(_tps[chip.PROGRAM_COUNTER]) + ', ' + \
            str(_tps[chip.PROGRAM_COUNTER + 1])

    if exe[:3] == 'end':  # pseudo-opcode (directive "end" - stop program)
        opcode = ''
        custom_opcode = False

    if custom_opcode:
        custom_opcode = False
        exe = cop
        print('{:4}  {:>8}  {:<10}'.format(chip.PROGRAM_COUNTER, opcode, cop.replace('()', '')))  # noqa
    else:
        print('{:4}  {:>8}  {:<10}'.format(chip.PROGRAM_COUNTER, opcode, exe.replace('()', '')))  # noqa

    chip.PROGRAM_COUNTER = chip.PROGRAM_COUNTER + words

    return exe


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
