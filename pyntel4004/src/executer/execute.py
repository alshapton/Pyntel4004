""" Module for running accembled code. """

# Import system modules
import sys
from typing import Tuple
sep = '/'  # Micropython
sys.path.insert(1, '..' + sep + 'src')  # Micropython

# Import platform detection
from platforms.platforms import get_current_platform  # noqa

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


def process_coredump(chip: Processor, ex: Exception) -> None:
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
    if opcode == 256:  # pseudo-opcode (directive "end" - stop program)
        if not quiet:
            print('           end')
        result = None

    exe = get_opcodeinfobyopcode(chip, opcode)['mnemonic']
    if exe == '-':
        result = None

    return result, monitor_command, monitor, breakpoints, exe, opcode


def dispatch0(operations: list, command: str):
    """
    Dispatch command line action to proper
    function with zero parameters
    """
    return operations[command]()


def dispatch1(operations: list, command: str, p1: int):
    """
    Dispatch command line action to proper
    function with 1 parameter
    """
    return operations[command](p1)


def dispatch2(operations: list, command: str, p1: int, p2: int):
    """
    Dispatch command line action to proper
    function with 2 parameters
    """
    return operations[command](p1, p2)


def execute(chip: Processor, location: str, pc: int, monitor: bool,
            quiet: bool, operations: list) -> bool:
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

    operations: list, mandatory
        List of functions i.e. instructions that are contained within the i4004

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

    platform = get_current_platform()
    breakpoints = []  # noqa
    chip.PROGRAM_COUNTER = pc
    opcode = 0
    const_chip = 'chip.'
    _tps = retrieve_program(chip, location)
    try:
        # pseudo-opcode (directive) for "end" or end of memory
        while opcode != 256 and chip.PROGRAM_COUNTER < 4096:
            monitor_command = 'none'
            result, monitor_command, monitor, breakpoints, exe, opcode = \
                process_instruction(chip, breakpoints, _tps, monitor,
                                    monitor_command, quiet)
            if opcode == 256:
                break

            if chip.PROGRAM_COUNTER == 4096:
                break
            # Execute instruction
            exe = const_chip + translate_mnemonic(chip, _tps, exe, opcode,
                                                  'E', 0, quiet)
            if platform == 'micropython':
                # Micropython
                command = exe.replace(const_chip, '')[:3]
                params = exe.replace(const_chip, '')[3:].\
                    replace('(', '').replace(')', '')
                splitparams = params.split(',')
                counter = 0
                p1 = None
                p2 = None
                for i in splitparams:
                    if counter == 0 and i is not None:
                        p1 = i
                    if counter == 1 and i is not None:
                        p2 = i
                    counter = counter + 1

                if splitparams == ['']:
                    _ = dispatch0(operations, command)
                elif p2 is None and p1 is not None:
                    _ = dispatch1(operations, command, int(p1))
                elif p2 is not None:
                    _ = dispatch2(operations, command, int(p1), int(p2))
            else:
                # Other pythons - e.g. cython
                # Evaluate the command (some commands may change
                # the PROGRAM_COUNTER here)
                # skipcq: PYL-PYL-W0123
                try:
                    eval(exe)  # noqa
                except Exception as ex:  # noqa
                    process_coredump(chip, ex)
                    return False
    except Exception as ex:
        process_coredump(chip, ex)
        return False
    return True
