# Import i4004 processor

from hardware.processor import processor
import ast
import getopt
import sys

# Assembler imports
from assembler.supporting import add_label

##############################################################################
#  _ _  _    ___   ___  _  _     ______                 _       _            #
# (_) || |  / _ \ / _ \| || |   |  ____|               | |     | |           #
#  _| || |_| | | | | | | || |_  | |__   _ __ ___  _   _| | __ _| |_ ___  _ _ #
# | |__   _| | | | | | |__   _| |  __| | '_ ` _ \| | | | |/ _` | __/ _ \| '_|#
# | |  | | | |_| | |_| |  | |   | |____| | | | | | |_| | | (_| | || (_) | |  #
# |_|  |_|  \___/ \___/   |_|   |______|_| |_| |_|\__,_|_|\__,_|\__\___/|_|  #
#                                                                            #
##############################################################################


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


def deal_with_monitor_command(chip: processor, monitor_command: str,
                              BREAKPOINTS, monitor: bool, opcode: str):
    """
    Take appropriate action depending on the command supplied.

    Parameters
    ----------
    chip : processor, mandatory
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


def execute(chip: processor, location: str, PC: int, monitor: bool):
    """
    Control the execution of a previously assembled program.

    Parameters
    ----------
    chip : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location : int, mandatory
        The location to which the program should be loaded

    PC : int, mandatory
        The program counter value commence execution

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    Returns
    -------
    True        in all instances

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    BREAKPOINTS = []
    _TPS = []
    if location == 'rom':
        _TPS = chip.ROM
    else:
        _TPS = chip.PRAM

    chip.PROGRAM_COUNTER = PC
    opcode = 0
    classic_prompt = '>>> '
    breakout_prompt = 'B>> '
    prompt = classic_prompt
    while opcode != 255:  # pseudo-opcode (directive) for "end"
        monitor_command = 'none'

        if is_breakpoint(BREAKPOINTS, chip.PROGRAM_COUNTER):
            monitor_command = 'none'
            monitor = True
            prompt = breakout_prompt
        if monitor is True:
            while monitor_command != '':
                monitor_command = input(prompt).lower()
                result, monitor, monitor_command, opcode = \
                    deal_with_monitor_command(chip, monitor_command,
                                              BREAKPOINTS, monitor, opcode)
                if result is False:
                    prompt = classic_prompt
                if result is None:
                    break
        custom_opcode = False
        OPCODE = _TPS[chip.PROGRAM_COUNTER]
        if OPCODE == 255:  # pseudo-opcode (directive "end" - stop program)
            print('           end')
            break
        try:
            opcodeinfo = next((item for item in chip.INSTRUCTIONS
                              if item['opcode'] == OPCODE), None)
        except:  # noqa
            opcodeinfo = {"opcode": -1, "mnemonic": "-"}
        exe = opcodeinfo['mnemonic']
        if exe == '-':
            break

        # Only mnemonic with 2 characters - fix
        if exe[:3] == 'ld ':
            exe = exe[:2] + exe[3:]

        # Ensure that the correct arguments are passed to the operations
        if exe[:3] == 'fim':
            custom_opcode = True
            value = str(_TPS[chip.PROGRAM_COUNTER + 1])
            cop = exe.replace('data8', value)
            exe = exe.replace('p', '').replace('data8)', '') + value + ')'

        if exe[:3] == 'isz':
            # Remove opcode from 1st byte to get register
            register = bin(_TPS[chip.PROGRAM_COUNTER] & 15)[2:].zfill(8)[4:]
            address = str(_TPS[chip.PROGRAM_COUNTER + 1])
            exe = 'isz(' + str(int(register, 2)) + ',' + str(address) + ')'

        if exe[:4] == 'jcn(':
            custom_opcode = True
            address = _TPS[chip.PROGRAM_COUNTER + 1]
            conditions = (bin(_TPS[chip.PROGRAM_COUNTER])[2:].zfill(8)[4:])
            b10address = str(address)
            cop = exe.replace('address8', b10address)
            exe = exe[:4] + str(int(conditions, 2)) + ',' + b10address + ')'

        # if (exe[:4] in ('src(')):
        #    custom_opcode = True

        if exe[:4] in ('jun(', 'jms('):
            custom_opcode = True
            # Remove opcode from 1st byte
            hvalue = bin(_TPS[chip.PROGRAM_COUNTER] &
                         0xffff0000)[2:].zfill(8)[:4]
            lvalue = bin(_TPS[chip.PROGRAM_COUNTER + 1])[2:].zfill(8)
            whole_value = str(int(hvalue + lvalue, 2))
            cop = exe.replace('address12', whole_value)
            exe = exe[:4] + whole_value + ')'

        if custom_opcode:
            custom_opcode = False
            print('  {:>7}  {:<10}'.format(OPCODE, cop.replace('()', '')))
        else:
            print('  {:>7}  {:<10}'.format(OPCODE, exe.replace('()', '')))

        exe = 'chip.' + exe

        # Evaluate the command (some commands may change
        # the PROGRAM_COUNTER here)
        ast.literal_eval(exe)
    return True

###############################################################################
#  _ _  _    ___   ___  _  _                                _     _           #
# (_) || |  / _ \ / _ \| || |     /\                       | |   | |          #
#  _| || |_| | | | | | | || |_   /  \   __ __  __ _ __ ___ | |__ | | ___ _ _  #
# | |__   _| | | | | | |__   _| / /\ \ / _/ _|/ _\ '_ ` _ \| '_ \| |/ _ \ '_| #
# | |  | | | |_| | |_| |  | |  / ____ \\_ \_ \  _/ | | | | | |_) | |  __/ |   #
# |_|  |_|  \___/ \___/   |_| /_/    \_\__/__/\__|_| |_| |_|_.__/|_|\___|_|   #
#                                                                             #
###############################################################################


def match_label(_L, label: str, address):
    """
    Given a label and an address, add it (if required) to the list of labels.

    Parameters
    ----------
    _L : list, mandatory
        A list of the known labels and their addresses

    label: str, mandatory
        The potential new label

    label: int, mandatory
        The address of the potential new label

    Returns
    -------
    label_address
        The integer address of the label

    Raises
    ------
    N/A

    Notes
    ------
    This will return -1 if the label is not found

    """
    for _i in range(len(_L)):  # noqa
        if _L[_i]['label'] == label:
            _L[_i]['address'] = address
    return _L


def get_label_addr(_L, label: str):
    """
    Given a label, get the address for that label.

    Parameters
    ----------
    _L : list, mandatory
        A list of the known labels and their addresses
    label: str, mandatory
        The label whose address is required

    Returns
    -------
    label_address
        The integer address of the label

    Raises
    ------
    N/A

    Notes
    ------
    This will return -1 if the label is not found

    """
    label_address = -1
    for _i in _L:
        if _i['label'] == label + ',':
            label_address = _i['address']
    return label_address


def get_bits(opcodeinfo):
    """
    Return an opcode 2x 4-bit nibbles

    Parameters
    ----------
    opcodeinfo: str, mandatory
        JSON string containing the opcode info retrieved from the
        opcode table.

    Returns
    -------
    bit1, bit2
        2 strings containing 4 binary digits each

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    bit1 = opcodeinfo['bits'][0]
    bit2 = opcodeinfo['bits'][1]
    return bit1, bit2


def do_error(message: str):
    """
    Print an assembly error message

    Parameters
    ----------
    message: str, mandatory
        The error message to display

    Returns
    -------
    N/A

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    print()
    print(message)
    return True


def get_opcodeinfo(chip: processor, ls: str, mnemonic: str):
    """
    Given a mnemonic, retrieve information about the mnemonic from
    the opcode table

    Parameters
    ----------
    chip : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    ls: str, mandatory
        's' or 'S' indicating whether the mnemonic contains the full mnemonic
        or not - e.g.    nop   as a mnemonic would be found if ls = 'S' or 's'
                         nop() as a mnemonic would be found if ls != 'S' or 's'

    mnemonic: str, mandatory
        The mnemonic to locate

    Returns
    -------
    opcodeinfo
        The information about the mnemonic required in JSON form,
        or

           {"opcode": -1, "mnemonic": "N/A"}

        if the mnemonic is not found.

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    if ls.upper() == 'S':
        try:
            opcodeinfo = next((item for item in chip.INSTRUCTIONS
                               if str(item["mnemonic"][:3]) == mnemonic), None)
        except:  # noqa
            opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
        return opcodeinfo
    try:
        opcodeinfo = next((item for item in chip.INSTRUCTIONS
                           if str(item["mnemonic"]) == mnemonic), None)
    except:  # noqa
        opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    return opcodeinfo


def assemble_isz(chip: processor, register, dest_label, _LABELS):
    """
    Function to correctly assemble the ISZ instruction.

    Parameters
    ----------
    chip : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    register: int, mandatory
        The register which will be compared in this instruction

    dest_label: str, mandatory
        The label to jump to if the conditions are met

    _LABELS: list, mandatory
        List of valid labels

    Returns
    -------
    n_opcode: int
        Decimal representation of the opcode (changes depending on conditions)

    label_address: int
        Address of the label in memory

    opcodeinfo['words']: int
        Length of the instruction in words

    val_left,val_right: str
        2 4-bit binary values - MSB and LSB of the memory address to jump to
        within this page.

    bit1, bit2: str
        2 4-bit binary values representing the two words of the opcode

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    n_opcode = 112 + int(register)
    try:
        opcodeinfo = next((item for item in chip.INSTRUCTIONS
                          if item["opcode"] == n_opcode), None)
    except:  # noqa
        opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    bit1, bit2 = get_bits(opcodeinfo)
    label_address = get_label_addr(_LABELS, dest_label)
    val_left = bin(int(label_address))[2:].zfill(8)[:4]
    val_right = bin(int(label_address))[2:].zfill(8)[4:]
    return n_opcode, label_address, opcodeinfo['words'], val_left, val_right, \
        bit1, bit2


def print_ln(f0, f1, f2, f3, f4, f5, f6, f7, f8,
             f9, f10, f11, f12, f13, f14, f15, f16):
    """
    Given a set of items, print them to the screen in a standard, columnar
    fashion.

    Parameters
    ----------
    f0 ....... f16 : str, all optional
        Parameters to print

    Returns
    -------
    N/A

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    fmt = '{:>4} {:<10} {:>4} {:>4}  {:>4} {:>4} {:>4} '
    fmt = fmt + '{:>4} {:>7} {:<4} {:<4}{:<8}{:<3}'
    fmt = fmt + ' {:<3} {:<3} {} {}'
    print(fmt.format(f0, f1, f2, f3, f4, f5, f6, f7, f8,
                     f9, f10, f11, f12, f13, f14, f15, f16))


def assemble_2(chip: processor, x, opcode, address, TPS, _LABELS, address_left,
               address_right, label, count):
    """
    Function to assemble specific instructions.

    Parameters
    ----------
    chip : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    opcode: str, mandatory
        The textual opcode (LD, LDM etc..)

    address: int, mandatory
        Address in memory to place the newly assembled instruction

    TPS: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    _LABELS: list, mandatory
        List of valid labels

    address_left, address_right: str, mandatory
        Binary representation of 2 4-bit words representing "address"

    label: str, mandatory
        If there is a label associated with this instruction, it will be here,
        "" otherwise.

    count: int, mandatory
        Assembly line number (used for printing during assembly)

    Returns
    -------
    address: int
        After the instruction has been assembled, the incoming address
        is incremented by the number of words in the assembled instruction.

    TPS: list
        List representing the memory of the i4004 into which the newly
        assembled instruction has just been placed.

    _LABELS: list
        Addresses of the labels (pass through only)

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    # pad out for the only 2-character mnemonic
    if opcode == 'ld':
        opcode = 'ld '
    f_opcode = opcode + '(' + x[1] + ')'
    if opcode in ('jun', 'jms'):
        # Special case for JUN and JMS
        if opcode == 'jun':
            decimal_code = 64
        if opcode == 'jms':
            decimal_code = 80
        f_opcode = opcode + '(address12)'
        opcodeinfo = get_opcodeinfo(chip, 'L', f_opcode)
        label_addr = get_label_addr(_LABELS, x[1])
        label_addr12 = str(bin(decimal_code)[2:].zfill(8)[:4]) + \
            str(bin(label_addr)[2:].zfill(12))
        bit1 = label_addr12[:8]
        bit2 = label_addr12[8:]
        TPS[address] = int(str(bit1), 2)
        TPS[address+1] = int(str(bit2), 2)
        print_ln(address, label, address_left, address_right, bit1[:4],
                 bit1[4:], bit2[:4], bit2[4:], str(TPS[address]) + ',' +
                 str(TPS[address + 1]), str(count), opcode, str(x[1]),
                 '', '', '', '', '')
        address = address + opcodeinfo['words']
    else:
        if opcode == 'src':
            register = x[1].lower().replace('p', '').replace('r', '')
            f_opcode = 'src(' + register + ')'
            opcodeinfo = get_opcodeinfo(chip, 'L', f_opcode)
            bit1, bit2 = get_bits(opcodeinfo)
            TPS[address] = opcodeinfo['opcode']
            print_ln(address, label, address_left, address_right, bit1,
                     bit2, '', '', TPS[address], '', '', str(count), opcode,
                     str(x[1]), '', '', '')
            address = address + opcodeinfo['words']
        else:
            opcodeinfo = get_opcodeinfo(chip, 'L', f_opcode)
            bit1, bit2 = get_bits(opcodeinfo)
            TPS[address] = opcodeinfo['opcode']
            print_ln(address, label, address_left, address_right, bit1, bit2,
                     '', '', TPS[address], '', '', str(count), opcode,
                     str(x[1]), '', '', '')
            address = address + opcodeinfo['words']
    return address, TPS, _LABELS


def validate_inc(parts, line):
    """
    Validate the contents (i.e. the parameters) of an INC command

    Parameters
    ----------
    parts: list, mandatory
        List of the parts of the line separated into elements of a list

    line: str, mandatory
        The mnemonic to locate

    Returns
    -------
    False in all circumstances except when an error occurs,
    in which case that error is printed during assembly and the
    assembly process will cease.

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    if len(parts) == 1 and parts[0] == 'inc':
        return do_error('No register value at line ' + str(line))
    if len(parts) == 2:
        if ((parts[1] == 'inc') and (parts[0][-1])):
            return do_error('No register value at line ' + str(line))
        if ((parts[0] == 'inc') and ((int(parts[1]) > 15) or
           (int(parts[1]) < 0))):
            return do_error('Invalid register value (' + parts[1] +
                            ') at line ' + str(line))
    return False


def assemble(program_name: str, object_file: str, chip: processor):
    """
    Main two-pass assembler for i4004 code

    Parameters
    ----------
    program_name: str, mandatory
        Name of the source file to load

    object_file: str, mandatory
        Name of the output file in which to place the object code

    chip: processor, mandatory
        Instance of a processor to place the assembled code in.

    Returns
    -------
    True if the code assembles correctly
    False if there are errors in the code

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    # Reset label table for this program
    _LABELS = []

    # Maximum size of program memory
    TPS_SIZE = max([chip.MEMORY_SIZE_ROM,
                    chip.MEMORY_SIZE_PRAM, chip.MEMORY_SIZE_RAM])

    # Reset temporary_program_store
    TPS = []
    for _i in range(TPS_SIZE):
        TPS.append(0)

    # Initialise assembly language line store to
    # twice the size of the potential program size.
    TFILE = []
    for _i in range(TPS_SIZE * 2):
        TFILE.append('')

    # Pass 1

    try:
        program = open(program_name, 'r')
    except IOError:
        ERR = ('FATAL: Pass 1: File "' + program_name +
               '" does not exist.')
    else:
        print()
        print()
        print('Program Code:', program_name)
        print()
        ORG_FOUND = False
        location = ''
        count = 0
        ERR = False
        p_line = 0
        address = 0

        while True:
            line = program.readline()
            constant = False
            # if line is empty, end of file is reached
            if not line:
                break

            # Work with a line of assembly code
            parts = line.split()
            if parts[0][-1] == ',':
                # Found a label, now add it to the label table
                if add_label(_LABELS, parts[0]) == -1:
                    ERR = ('FATAL: Pass 1: Duplicate label: ' + parts[0] +
                           ' at line ' + str(p_line + 1))
                    break
                # Attach value to a label
                if '0' <= str(parts[1])[:1] <= '9':
                    constant = True
                    match_label(_LABELS, parts[0], parts[1])
                else:
                    match_label(_LABELS, parts[0], address)
                # Set opcode
                opcode = parts[1][:3]
            else:
                # Set opcode
                opcode = parts[0][:3]
            if opcode[:3] == 'inc':
                ERR = validate_inc(parts, p_line + 1)
                if ERR:
                    break
            # Custom opcodes
            if not constant:
                if (opcode == 'ld()' or opcode[:2] == 'ld'):
                    opcode = 'ld '
                if opcode not in ('org', '/', 'end', 'pin'):
                    opcodeinfo = get_opcodeinfo(chip, 'S', opcode)
                    address = address + opcodeinfo['words']
            TFILE[p_line] = line.strip()
            p_line = p_line + 1
        # Completed reading program into memory
        program.close()

    if ERR:
        print(ERR)
        print("Program Assembly halted @ Pass 1")
        print()
        return False

    # Pass 2
    print('Address  Label   Address        Assembled                    ' +
          '  Line     Op/Operand')
    print(' (Dec)            (Bin)           (Bin)          (Dec)')
    print('                            Word 1     Word 2')

    # Program Line Count
    count = 0
    while True:
        line = TFILE[count].strip()
        if len(line) == 0:
            break  # End of code

        x = line.split()
        label = ''

        # Check for initial comments
        if line[0] == '/':
            print_ln('', label, ' ', ' ', ' ', ' ', ' ', ' ', ' ',  ' ',
                     ' ', str(count), line, ' ', '', '', '',)
        else:
            if len(line) > 0:
                if x[0][-1] == ',':
                    label = x[0]
                    opcode = x[1]
                    # Check to see if we are assembling a label
                    if '0' <= str(x[1])[:1] <= '9':
                        TPS[address] = int(x[1])
                        print_ln('', '',  '', '', '', '', '', '', '', '', '',
                                 str(count), label, str(x[1]), '', '', '',)
                        break
                else:
                    opcode = x[0]
                opcodeinfo = get_opcodeinfo(chip, 'S', opcode)
                if (opcode in ['org', 'end', 'pin']) or (opcode is not None):
                    if (opcode in ['org', 'end', 'pin']):
                        if opcode == 'org':
                            ORG_FOUND = True
                            print_ln('', label,  '', '', '', '', '', '', '',
                                     '', '', str(count), opcode, str(x[1]),
                                     '', '', '',)
                            if x[1] in ('rom', 'ram'):
                                location = x[1]
                                address = 0
                            else:
                                location = 'ram'
                                address = int(str(x[1]))
                        if opcode == 'end':
                            print_ln('', label, '', '', '', '', '',  '', '',
                                     '', '', str(count), opcode, '', '',
                                     '', '')
                            # pseudo-opcode (directive "end")
                            TPS[address] = 255
                            # break
                        if opcode == 'pin':
                            result = chip.write_pin10(int(x[1]))
                            if result is False:
                                ERR = do_error(
                                    "FATAL: Pass 2:  Invalid value for "
                                    + "TEST PIN 10 at line " + count)
                            print_ln('', label, '', '', '', '', '', '', '', '',
                                     '', '', '', '', str(count), opcode,
                                     str(x[1]))
                    else:
                        if ORG_FOUND is True:
                            if x[0][-1] == ',':
                                label = x[0]
                                match_label(_LABELS, label, address)
                                for _i in range(len([x])-1):
                                    x[_i] = x[_i + 1]
                                x.pop(len([x])-1)
                            opcode = x[0]

                            address_left = bin(address)[2:].zfill(8)[:4]
                            address_right = bin(address)[2:].zfill(8)[4:]

                            # Check for operand(s)
                            # Operator & operand (generic)
                            if len(x) == 2:
                                address, TPS, _LABELS = \
                                    assemble_2(chip, x, opcode, address, TPS,
                                               _LABELS, address_left,
                                               address_right, label,
                                               count)
                            if len(x) == 1:
                                # Only operator, no operand
                                bit1, bit2 = get_bits(opcodeinfo)
                                TPS[address] = opcodeinfo['opcode']
                                print_ln(address, label, address_left,
                                         address_right, bit1, bit2, '', '',
                                         TPS[address], '', '', str(count),
                                         opcode, '', '', '', '')
                                address = address + opcodeinfo['words']
                            if len(x) == 3:
                                opcode = x[0]
                                # Operator and 2 operands
                                if opcode == 'jcn':
                                    conditions = x[1].upper()
                                    dest_label = x[2]
                                    bin_conditions = 0
                                    if 'I' in conditions:
                                        bin_conditions = 8
                                    if 'A' in conditions:
                                        bin_conditions = bin_conditions + 4
                                    if 'C' in conditions:
                                        bin_conditions = bin_conditions + 2
                                    if 'T' in conditions:
                                        bin_conditions = bin_conditions + 1
                                    f_opcode = 'jcn(' + str(bin_conditions) \
                                        + ',address8)'
                                    opcodeinfo = get_opcodeinfo(chip, 'L',
                                                                f_opcode)
                                    label_addr = get_label_addr(_LABELS,
                                                                dest_label)
                                    vl = bin(int(label_addr))[2:].zfill(8)[:4]
                                    vr = bin(int(label_addr))[2:].zfill(8)[4:]
                                    bit1, bit2 = get_bits(opcodeinfo)
                                    TPS[address] = opcodeinfo['opcode']
                                    TPS[address + 1] = label_addr
                                    print_ln(address, label, address_left,
                                             address_right, bit1, bit2,
                                             vl, vr, str(TPS[address]) + "," +
                                             str(TPS[address + 1]), '', '', '',
                                             str(count), opcode, str(x[1]),
                                             str(x[2]), '')
                                    address = address + opcodeinfo['words']
                                if opcode[:3] == 'fim':
                                    f_opcode = x[0] + '(' + x[1] + ',data8)'
                                    opcodeinfo = get_opcodeinfo(chip, 'L',
                                                                f_opcode)
                                    TPS[address] = opcodeinfo['opcode']
                                    TPS[address + 1] = int(x[2])
                                    bit1, bit2 = get_bits(opcodeinfo)
                                    print_ln(address, label, '' '',
                                             '', bit1, bit2, '',
                                             '',  str(TPS[address]) +
                                             "," + str(TPS[address + 1]),
                                             str(count), opcode, str(x[1]),
                                             str(x[2]), '', '', '', '')
                                    address = address + opcodeinfo['words']
                                if opcode == 'isz':
                                    n_opcode, label_addr, words, \
                                        addr_left, addr_right, \
                                        bit1, bit2 = \
                                        assemble_isz(chip, x[1], x[2],
                                                     _LABELS)
                                    TPS[address] = n_opcode
                                    TPS[address + 1] = label_addr
                                    print_ln(address, label, addr_left,
                                             addr_right, bit1, bit2, vl,
                                             vr, str(TPS[address]) +
                                             "," + str(TPS[address + 1]),
                                             str(count), opcode, str(x[1]),
                                             str(x[2]), '', '', '', '')
                                    address = address + words
                                if opcode not in ('jcn', 'fim', 'isz'):
                                    d_type = ''
                                    if int(x[2]) <= 256:
                                        d_type = 'data8'
                                    val_left = bin(int(x[2]))[2:].zfill(8)[:4]
                                    val_right = bin(int(x[2]))[2:].zfill(8)[4:]
                                    f_opcode = opcode + "(" + \
                                        x[1] + "," + d_type + ")"
                                    opcodeinfo = get_opcodeinfo(chip, 'L',
                                                                f_opcode)
                                    bit1, bit2 = get_bits(opcodeinfo)
                                    TPS[address] = opcodeinfo['opcode']
                                    TPS[address+1] = int(x[2])
                                    print_ln(address, label, address_left,
                                             address_right, bit1, bit2,
                                             val_left, val_right,
                                             str(TPS[address]) + "," +
                                             str(TPS[address + 1]), '', '',
                                             str(count), opcode, str(x[1]),
                                             str(x[2]), '', '')
                                    address = address + opcodeinfo['words']
                        else:
                            ERR = do_error("FATAL: Pass 2: No 'org'" +
                                           " found at line: " + str(count + 1))
                            break
                else:
                    ERR = do_error("'FATAL: Pass 2:  Invalid mnemonic '" +
                                   opcode + "' at line: " + str(count + 1))
                    break
        count = count + 1

    if ERR:
        print("Program Assembly halted")
        return False
    print()

    # Place assembled code into correct location
    if location == 'rom':
        chip.ROM = TPS

    if location == 'ram':
        chip.PRAM = TPS

    print('Labels:')
    print('Address   Label')
    for _i in range(len(_LABELS)):  # noqa
        print('{:>5}     {}'.format(_LABELS[_i]['address'],
              _LABELS[_i]['label']))
    write_program_to_file(TPS, object_file, location, _LABELS)
    return True


def write_program_to_file(program, filename, memory_location, _LABELS):
    """
    Take the assembled program and write to a given filename.

    Parameters
    ----------
    program : list, mandatory
        The compiled program
    filename: str, mandatory
        The filename to write to
    memory_location: str, mandatory
        Location in memory of the first word of the program
    _LABELS: list, mandatory
        Label table

    Returns
    -------
    True

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """

    from datetime import datetime

    program_name = '"program":"' + filename + '"'
    m_location = '"location":"' + memory_location + '"'
    compdate = '"compile_date":"' + \
               datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '"'
    labels = '"labels":' + str(_LABELS).replace("'", '"')
    memorycontent = '"memory":['
    for location in program:
        memorycontent = memorycontent + '"' + str(hex(location)[2:]) + '", '
    memory_content = memorycontent[:-2] + ']'
    json_doc = "{"
    json_doc = json_doc + program_name + ','
    json_doc = json_doc + compdate + ','
    json_doc = json_doc + m_location + ','
    json_doc = json_doc + memory_content + ','
    json_doc = json_doc + labels
    json_doc = json_doc + '}'
    print(json_doc)
    with open(filename + '.obj', "w") as output:
        output.write(json_doc)

    return True


def main(argv):
    """
    Control the assembly and execution of a named assembly language file.

    Parameters
    ----------
    argv: list of command line arguments

    Returns
    -------
    N/A

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    inputfile = ''
    outputfile = ''
    RUN = True
    try:
        opts, args = getopt.getopt(argv, "hi:o:norun", ["ifile=", "ofile="])  # noqa
    except getopt.GetoptError:
        print('assemble.py -i <inputfile>\n -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('assemble -i <inputfile> -o <outputfile> -norun')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            if outputfile == '':
                outputfile = inputfile.replace('asm', 'obj')
            else:
                outputfile = arg
        elif opt in ("-norun"):
            RUN = False

    # Create new instance of a processor
    chip = processor()

    result = assemble(inputfile, outputfile, chip)
    if RUN is True and result is True:
        print()
        print('EXECUTING PROGRAM: ')
        print()
        execute(chip, 'rom', 0, True)
        print()
        acc = chip.read_accumulator()
        print('Accumulator : ' + str(acc) +
              '  (0b ' + str(processor.decimal_to_binary(4, acc)) + ')')
        print('Carry       :', chip.read_carry())
        print()


main(sys.argv[1:])
