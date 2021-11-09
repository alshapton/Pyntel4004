from hardware.processor import Processor
import json


def reload(inputfile, chip):
    """
    Reload an already assembled program and execute it

    Parameters
    ----------
    inputfile: str, mandatory
        filename of a .obj file

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
    ------
    N/A

    """
    with open(inputfile, "r") as programfile:
        data = json.loads(programfile)

    # Get data for memory load from JSON
    memory_space = data['location']
    location = 0
    pc = location

    # Place program in memory
    for i in data['memory']:
        if memory_space == 'rom':
            chip.ROM[location] = int(i, 16)
        else:
            chip.PRAM[location] = int(i, 16)
        location = location + 1

    return memory_space, pc


def is_breakpoint(BREAKPOINTS, PC):
    """
    Determine if the current programme counter is at a predetermined
    breakpoint.

    Parameters
    ----------
    BREAKPOINT : list, mandatory
        A list of the predetermined breakpoints
    PC: int, mandatory
        The current value of the program counter

    Returns
    -------
    True        if the current program counter is at a breakpoint
    False       if the current program counter is not at a breakpoint

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    for i in BREAKPOINTS:
        if str(i) == str(PC):
            return True
    return False


def deal_with_monitor_command(chip: Processor, monitor_command: str,
                              BREAKPOINTS, monitor: bool, opcode: str):
    """
    Take appropriate action depending on the command supplied.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    monitor_command: str, mandatory
        Command given by the user.

    BREAKPOINTS : list, mandatory
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
    ------
    Function will return a value of -1 if the monitor command is invalid.

    """
    if monitor_command == '':
        return True, monitor, monitor_command, opcode

    if monitor_command == 'regs':
        print('0-> ' + str(chip.REGISTERS) + ' <-15')
        return True, monitor, monitor_command, opcode
    if monitor_command == 'stack':
        for _i in range(chip.STACK_SIZE-1, -1, -1):
            if _i == chip.STACK_POINTER:
                pointer = '==>'
            else:
                pointer = '-->'
            print("[ " + str(_i) + "] " + pointer + "[ " +
                  str(chip.STACK[_i]) + ' ]')
        return True, monitor, monitor_command, opcode
    if monitor_command == 'pc':
        print('PC = ', chip.PROGRAM_COUNTER)
        return True, monitor, monitor_command, opcode
    if monitor_command == 'carry':
        print('CARRY = ', chip.read_carry())
        return True, monitor, monitor_command, opcode
    if monitor_command == 'ram':
        print('RAM = ', chip.RAM)
        return True, monitor, monitor_command, opcode
    if monitor_command == 'pram':
        print('PRAM = ', chip.PRAM)
        return True, monitor, monitor_command, opcode
    if monitor_command == 'rom':
        print('ROM = ', chip.ROM)
        return True, monitor, monitor_command, opcode
    if monitor_command[:3] == 'reg':
        register = int(monitor_command[3:])
        print('REG[' + monitor_command[3:].strip()+'] = ' +
              str(chip.REGISTERS[register]))
        return True, monitor, monitor_command, opcode
    if monitor_command == 'acc':
        print('ACC =', chip.read_accumulator())
        return True, monitor, monitor_command, opcode
    if monitor_command == 'pin10':
        print('PIN10 = ', chip.read_pin10())
        return True, monitor, monitor_command, opcode
    if monitor_command == 'crb':
        print('CURRENT RAM BANK = ', chip.read_current_ram_bank())
        return True, monitor, monitor_command, opcode
    if monitor_command[:1] == 'b':
        bp = monitor_command.split()[1]
        BREAKPOINTS.append(bp)
        print('Breakpoint set at address ' + bp)
        return True, monitor, monitor_command, opcode
    if monitor_command == 'off':
        monitor_command = ''
        monitor = False
        return False, monitor, monitor_command, opcode
    if monitor_command == 'q':
        monitor = False
        opcode = 255
        return None, monitor, monitor_command, opcode
    return -1


def retrieve(inputfile, chip):
    """
    Pass-thru function for the "reload" function

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
    ------
    No added value in this function, simply a pass-thru.

    """
    m, p = reload(inputfile, chip)
    return m, p
