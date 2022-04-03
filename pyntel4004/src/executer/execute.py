""" Module for running accembled code. """

# Import system modules
import os
import sys
from typing import Tuple
sys.path.insert(1, '..' + os.sep + 'src')

# Import i4004 processor
from hardware.processor import Processor  # noqa

# Import executer and shared functions
from executer.exe_supporting import deal_with_monitor_command, is_breakpoint  # noqa
from shared.shared import coredump, do_error, get_opcodeinfobyopcode, retrieve_program, \
    translate_mnemonic  # noqa

##############################################################################
#  _ _  _    ___   ___  _  _     ______                 _       _            #
# (_) || |  / _ \ / _ \| || |   |  ____|               | |     | |           #
#  _| || |_| | | | | | | || |_  | |__   _ __ ___  _   _| | __ _| |_ ___  _ _ #
# | |__   _| | | | | | |__   _| |  __| | '_ ` _ \| | | | |/ _` | __/ _ \| '_|#
# | |  | | | |_| | |_| |  | |   | |____| | | | | | |_| | | (_| | || (_) | |  #
# |_|  |_|  \___/ \___/   |_|   |______|_| |_| |_|\__,_|_|\__,_|\__\___/|_|  #
#                                                                            #
##############################################################################


def process_coredump(chip: Processor, ex) -> None:
    """
    Formulate the opcodes into mnemonics ready for execution.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    ex: Exception, mandatory
        Exception object to process

    Returns
    -------
    N/A

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    cls = str(type(ex))
    x = cls.replace('<class ', '').replace('>', ''). \
        replace("'", '').split('.')
    ex_type = x[len(x)-1]
    ex_args = str(ex.args).replace('(', '').replace(',)', '')
    message = ex_type + ': ' + ex_args + ' at location ' + \
        str(chip.PROGRAM_COUNTER)
    do_error(message)
    coredump(chip, 'core')


def process_instruction(chip: Processor, breakpoints: list, _tps: list,
                        monitor: bool, monitor_command: str, quiet: bool
                        ) -> Tuple[bool, str, bool, list, str, str]:
    """
    Process a single instruction.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    breakpoints : list, mandatory
        A list of the predetermined breakpoints

    _tps: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    monitor_command: str, mandatory
        Command given by the user.

    quiet: bool, mandatory
        Whether quiet mode is on or off.

    Returns
    -------
    result: bool
        Result of the function

    monitor_command: str
        Command given by the user.

    monitor: bool
        Whether or not the monitor is currently "on" or "off"

    breakpoints : list
        A list of the predetermined breakpoints

    exe: str
        pre-formatted exe mnemonic ready for processing

    opcode: str
        Opcode of the current instruction

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    classic_prompt = '>>> '
    breakout_prompt = 'B>> '
    prompt = classic_prompt
    result = None
    if is_breakpoint(breakpoints, chip.PROGRAM_COUNTER):
        monitor_command = 'none'
        monitor = True
        prompt = breakout_prompt

    opcode = _tps[chip.PROGRAM_COUNTER]
    if monitor is True:
        while monitor_command != '':
            if not quiet:
                monitor_command = input(prompt).lower()
            else:
                monitor_command = ''
            result, monitor, monitor_command, opcode = \
                deal_with_monitor_command(chip, monitor_command,
                                          breakpoints, monitor, opcode)
            if result is False:
                prompt = classic_prompt

            if result is None:
                break

    opcode = _tps[chip.PROGRAM_COUNTER]
    # pseudo-opcode (directive "end" - stop program)
    if opcode == 256:
        if not quiet:
            print('           end')
        result = None

    if chip.PROGRAM_COUNTER == 4096:
        result = False

    exe = get_opcodeinfobyopcode(chip, opcode)['mnemonic']
    if exe == '-':
        result = None

    return result, monitor_command, monitor, breakpoints, exe, opcode


def execute(chip: Processor, location: str, pc: int, monitor: bool,
            quiet: bool) -> bool:
    """
    Control the execution of a previously assembled program.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location : str, mandatory
        The location to which the program should be loaded

    pc : int, mandatory
        The program counter value to commence execution

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    quiet: bool, mandatory
        Whether or not quiet mode is on or off

    Returns
    -------
    True        in all instances

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
#    mccabe: MC0001 / execute is too complex (19) - start
#    mccabe: MC0001 / execute is too complex (13)
#    mccabe: MC0001 / execute is too complex (11)
#    mccabe: MC0001 / execute is too complex (5)

    breakpoints = []  # noqa
    chip.PROGRAM_COUNTER = pc
    opcode = 0
    _tps = retrieve_program(chip, location)
    while opcode != 256:  # pseudo-opcode (directive) for "end"
        monitor_command = 'none'
        if chip.PROGRAM_COUNTER != 4096:
            result, monitor_command, monitor, breakpoints, exe, opcode = \
                process_instruction(chip, breakpoints, _tps, monitor,
                                    monitor_command, quiet)
        else:
            opcode = 256

        if opcode == 256:
            break

        # Execute instruction
        exe = 'chip.' + translate_mnemonic(chip, _tps, exe, opcode,
                                           'E', 0, quiet)
        # Evaluate the command (some commands may change
        # the PROGRAM_COUNTER here)
        # Deliberately using eval here... skip checks in all code quality tools
        # skipcq: PYL-PYL-W0123
        try:
            eval(exe)  # noqa
        except Exception as ex:  # noqa
            process_coredump(chip, ex)
            return False
    return True
