"""Assembly process supporting functions."""

import json
from typing import Tuple

from hardware.processor import Processor
from shared.shared import determine_filetype


def reload(inputfile: str, chip: Processor) -> Tuple[str, int]:
    """
    Reload an already assembled program and execute it.

    Parameters
    ----------
    inputfile: str, mandatory
        filename of a .obj or a .bin file

    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    memory_space: str
        rom or ram (depending on the target memory space)

    pc:  int
        location to commence execution of the assembled program

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """

    filetype = determine_filetype(inputfile)

    location = 0
    pc = location
    if filetype == 'OBJ':
        print(' Filetype: Object module with label tables etc.\n')
        with open(inputfile, "r", encoding='utf-8') as programfile:
            data = json.load(programfile)

        # Get data for memory load
        memory_space = data['location']

        # Place program in memory
        for i in data['memory']:
            if memory_space == 'rom':
                chip.ROM[location] = int(i, 16)
            else:
                chip.PRAM[location] = int(i, 16)
            location = location + 1

    if filetype == 'BIN':
        print(' Filetype: Binary assembled machine code\n')
        location = 0
        memory_space = 'ram'
        programbytearray = bytearray()
        try:
            with open(inputfile, "rb") as f:
                byte = f.read(1)
                while byte:
                    programbytearray += byte
                    byte = f.read(1)
                    location = location + 1

        except IOError:
            print('Error While Opening the file!')

        # Place program in memory
        location = 0
        memory_space = 'ram'

        for i in programbytearray:
            chip.PRAM[location] = i
            location = location + 1

    return memory_space, pc


def is_breakpoint(breakpoints: list, pc: int) -> bool:
    """
    Determine if the current programme counter is at a breakpoint.

    Parameters
    ----------
    breakpoints : list, mandatory
        A list of the predetermined breakpoints

    pc: int, mandatory
        The current value of the program counter

    Returns
    -------
    True        if the current program counter is at a breakpoint
    False       if the current program counter is not at a breakpoint

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    for i in breakpoints:
        if str(i) == str(pc):
            return True
    return False


def print_stack(chip: Processor) -> None:
    """
    Print the stack values (along with the pointer).

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

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
    for _i in range(chip.STACK_SIZE-1, -1, -1):
        if _i == chip.STACK_POINTER:
            pointer = '==>'
        else:
            pointer = '-->'
        print("[ " + str(_i) + "] " + pointer + "[ " +
              str(chip.STACK[_i]) + ' ]')


def process_simple_monitor_command(chip: Processor, monitor_command: str,
                                   monitor: bool, opcode: str) \
        -> Tuple[bool, bool, str, str]:
    """
    Take appropriate action depending on the command supplied.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    monitor_command: str, mandatory
        Command given by the user.

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    opcode: str, mandatory
        Opcode of the current instruction

    Returns
    -------
    True/False: bool  if the code should continue with monitor on or off
    None              if the monitor should be disabled

    monitor: bool
        Whether or not the monitor is currently "on" or "off"

    monitor_command: str
        The command that was entered by the user

    opcode: str
        Opcode of the current instruction

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if monitor_command == 'stack':
        print_stack(chip)
    elif monitor_command == 'pc':
        print('PC = ', chip.PROGRAM_COUNTER)
    elif monitor_command == 'carry':
        print('CARRY = ', chip.read_carry())
    elif monitor_command == 'ram':
        print('RAM = ', chip.RAM)
    elif monitor_command == 'pram':
        print('PRAM = ', chip.PRAM)
    elif monitor_command == 'rom':
        print('ROM = ', chip.ROM)
    elif monitor_command == 'acc':
        print('ACC =', chip.read_accumulator())
    elif monitor_command == 'pin10':
        print('PIN10 = ', chip.read_pin10())
    elif monitor_command == 'crb':
        print('CURRENT RAM BANK = ', chip.read_current_ram_bank())
    return True, monitor, monitor_command, opcode


def deal_with_monitor_command(chip: Processor, monitor_command: str,
                              breakpoints, monitor: bool, opcode: str) \
        -> Tuple[bool, bool, str, str]:
    """
    Take appropriate action depending on the command supplied.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    monitor_command: str, mandatory
        Command given by the user.

    breakpoints : list, mandatory
        A list of the predetermined breakpoints

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    opcode: str, mandatory
        Opcode of the current instruction

    Returns
    -------
    True/False: bool  if the code should continue with monitor on or off
    None              if the monitor should be disabled

    monitor: bool
        Whether or not the monitor is currently "on" or "off"

    monitor_command: str
        The command that was entered by the user

    opcode: str,
        Opcode of the current instruction

    Raises
    ------
    N/A

    Notes
    -----
    Function will return a value of -1 if the monitor command is invalid.

    """
#   mccabe: MC0001 / deal_with_monitor_command is too complex (18) - start
#   mccabe: MC0001 / deal_with_monitor_command is too complex (16)
#   mccabe: MC0001 / deal_with_monitor_command is too complex (5)

    if monitor_command == '':
        return True, monitor, monitor_command, opcode
    if monitor_command == 'regs':
        print('0-> ' + str(chip.REGISTERS) + ' <-15')
        return True, monitor, monitor_command, opcode
    if monitor_command in (['stack', 'pc', 'carry', 'ram', 'pram',
                            'rom', 'acc', 'pin10', 'crb']):
        result, monitor, monitor_command, opcode = \
            process_simple_monitor_command(chip, monitor_command,
                                           monitor, opcode)
        return result, monitor, monitor_command, opcode
    if monitor_command[:3] == 'reg':
        register = int(monitor_command[3:])
        print('REG[' + monitor_command[3:].strip()+'] = ' +
              str(chip.REGISTERS[register]))
        return True, monitor, monitor_command, opcode
    if monitor_command[:1] == 'b':
        bp = monitor_command.split()[1]
        breakpoints.append(bp)
        print('Breakpoint set at address ' + bp)
        return True, monitor, monitor_command, opcode
    if monitor_command == 'off':
        return False, False, '', opcode
    if monitor_command == 'q':
        return None, False, monitor_command, 255

    return -1, '', '', 0


def retrieve(inputfile: str, chip: Processor) -> Tuple[str, int]:
    """
    Pass-thru function for the "reload" function.

    Parameters
    ----------
    inputfile: str, mandatory
        filename of a .obj file

    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    m: str
        rom or ram (depending on the target memory space)

    p: int
        location to commence execution of the assembled program

    Raises
    ------
    N/A

    Notes
    -----
    No added value in this function, simply a pass-thru.

    """
    m, p = reload(inputfile, chip)
    return m, p
