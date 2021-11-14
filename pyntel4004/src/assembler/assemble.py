# Import i4004 processor

from hardware.processor import Processor
from hardware.suboperation import split_address8

# Assembler imports
from assembler.asm_supporting import assemble_isz, assemble_2, \
    assemble_fim, assemble_jcn, do_error, get_bits, \
    match_label, pass0, print_ln, \
    work_with_a_line_of_asm, write_program_to_file

from shared.shared import get_opcodeinfo

###############################################################################
#  _ _  _    ___   ___  _  _                                _     _           #
# (_) || |  / _ \ / _ \| || |     /\                       | |   | |          #
#  _| || |_| | | | | | | || |_   /  \   __ __  __ _ __ ___ | |__ | | ___ _ _  #
# | |__   _| | | | | | |__   _| / /\ \ / _/ _|/ _\ '_ ` _ \| '_ \| |/ _ \ '_| #
# | |  | | | |_| | |_| |  | |  / ____ \\_ \_ \  _/ | | | | | |_) | |  __/ |   #
# |_|  |_|  \___/ \___/   |_| /_/    \_\__/__/\__|_| |_| |_|_.__/|_|\___|_|   #
#                                                                             #
###############################################################################


def asm_comment(label, count, line):
    """
    Output the assembled comment.

    Parameters
    ----------
    label: str, mandatory
        Any label on this line

    count: int, mandatory
        Current assembly program line

    line: str, mandatory
        Line of program code.

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
    print_ln('', label, ' ', ' ', ' ', ' ', ' ', ' ', ' ',  ' ',
             ' ', str(count), line, ' ', '', '', '',)


def assemble_1(opcodeinfo, label, TPS, address, count):
    """
    Output the assembled operator (no operand(s)).

    Parameters
    ----------
    opcodeinfo: str, mandatory
        JSON string containing the information about the opcode

    label: str, mandatory
        Any label on this line

    TPS: List, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    count: int, mandatory
        Current assembly program line

    Returns
    -------
    TPS: List
        Assembled code

    address: int
        Current address of memory for assembly

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    address_left, address_right = split_address8(address)
    # Only operator, no operand
    bit1, bit2 = get_bits(opcodeinfo)
    TPS[address] = opcodeinfo['opcode']
    print_ln(address, label, address_left,
             address_right, bit1, bit2, '', '',
             TPS[address], '', '', str(count),
             opcodeinfo['opcode'], '', '', '', '')
    address = address + opcodeinfo['words']
    return TPS, address


def assemble_3(chip, x, _LABELS, TPS, address, address_left,
               address_right, label, count):
    """
    Assemble code with 3 components.

    Parameters
    ----------
    chip: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: List, mandatory
        Line of program code (split into component parts).

    _LABELS: List, mandatory
        List for containing labels

    TPS: List, mandatory
        Assembled code

    address: int, mandatory
        Current address of memory for assembly

    address_left, address_right: str, mandatory
        Binary representation of 2 4-bit words representing "address"

    label: str, mandatory
        Any label on this line

    count: int, mandatory
        Current assembly program line

    Returns
    -------
    address: int
        Current address of memory for assembly

    TPS: List, mandatory
        Assembled code

    _LABELS: List, Mandatory
        List for containing labels

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    # Operator and 2 operands
    if x[0] == 'jcn':
        address, TPS, _LABELS = assemble_jcn(chip, x, _LABELS, TPS,
                                             address, address_left,
                                             address_right, label,
                                             count)
    if x[0][:3] == 'fim':
        address, TPS, _LABELS = assemble_fim(chip, x, _LABELS, TPS,
                                             address, label, count)
    if x[0] == 'isz':
        address, TPS, _LABELS = assemble_isz(chip, x, x[1], _LABELS, TPS,
                                             address, address_left,
                                             address_right, label, count)
    if x[0] not in ('jcn', 'fim', 'isz'):
        TPS, address = asm_others(chip, x, x[0], TPS, address, label)

    return address, TPS, _LABELS


def asm_label(TPS, address, x, count, label):
    """
    Output the assembled label.

    Parameters
    ----------
    TPS: List, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    x: List, mandatory
        Line of program code (split into component parts).

    count: int, mandatory
        Current assembly program line

    label: str, mandatory
        Any label on this line

    Returns
    -------
    TPS: List, mandatory
        Assembled code

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    TPS[address] = int(x[1])
    print_ln('', '',  '', '', '', '', '', '', '', '', '',
             str(count), label, str(x[1]), '', '', '',)
    return TPS


def asm_org(label, count, x, opcode):
    """
    Output the assembled "org" pseudo-opcode.

    Parameters
    ----------
    label: str, mandatory
        Any label on this line

    count: int, mandatory
        Current assembly program line

    x: List, mandatory
        Line of program code (split into component parts).

    opcode: str, mandatory
        Opcode ('org' or '=')

    Returns
    -------
    True: Boolean, mandatory
          We have found an "org" instruction

    location: str
        'rom' or 'ram'

    address: int
        address inm rom/ram to assemble

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if opcode == 'org':
        print_ln('', label,  '', '', '', '', '', '', '',
                 '', '', str(count), opcode, str(x[1]),
                 '', '', '',)
        if x[1] in ('rom', 'ram'):
            location = x[1]
            address = 0
        else:
            location = 'ram'
            address = int(str(x[1]))
    if opcode == '=':
        print_ln('', label,  '', '', '', '', '', '', '',
                 '', '', str(count), opcode, str(x[2]),
                 '', '', '',)
        location, address = 0, 0
    return True, location, address


def asm_end(TPS, address, count, label):
    """
    Output the assembled "end" pseudo-opcode.

    Parameters
    ----------
    TPS: List, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    count: int, mandatory
        Current assembly program line

    label: str, mandatory
        Any label on this line

    Returns
    -------
    TPS: List, mandatory
        Assembled code

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    print_ln('', label, '', '', '', '', '',  '', '', '', '', str(count),
             'end', '', '', '', '')
    # pseudo-opcode (directive "end")
    TPS[address] = 255
    return TPS


def asm_pin(chip, value, label, count):
    """
    Manage the PIN10 (Signal pin).

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    value: int, mandatory
        value to write to the signal pin

    label: str, mandatory
        Any label on this line

    count: int, mandatory
        Current assembly program line

    Returns
    -------
    err: str/boolean
        False if no error
        Text if error

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    result = chip.write_pin10(int(value))
    if result is False:
        err = "FATAL: Pass 2:  Invalid value for " \
              + "TEST PIN 10 at line " + count
    else:
        print_ln('', label, '', '', '', '', '', '', '', '',
                 '', '', '', '', str(count), 'pin',
                 str(value))
        err = False
    return err


def asm_others(chip, x, count, opcode, TPS, address, label):
    """
    Pass 1 of the two-pass assembly process.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: List, mandatory
        Line of program code (split into component parts).

    count: int, mandatory
        Current assembly program line

    opcode: int, mandatory
       Value of the opcode for assembly

    TPS: List, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    label: str, mandatory
        Label of the current line (if any)

    Returns
    -------
    TPS: List
        Assembled code

    address: int
        the address to assemble to

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    d_type = ''
    if int(x[2]) <= 256:
        d_type = 'data8'
    val_left, val_right = split_address8(int(x[2]))
    address_left, address_right = split_address8(address)
    f_opcode = opcode + "(" + x[1] + "," + d_type + ")"
    opcodeinfo = get_opcodeinfo(chip, 'L', f_opcode)
    bit1, bit2 = get_bits(opcodeinfo)
    TPS[address] = opcodeinfo['opcode']
    TPS[address+1] = int(x[2])
    print_ln(address, label, address_left, address_right, bit1, bit2,
             val_left, val_right, str(TPS[address]) + "," +
             str(TPS[address + 1]), '', '', str(count), opcode, str(x[1]),
             str(x[2]), '', '')
    address = address + opcodeinfo['words']
    return TPS, address


def asm_pseudo(chip, opcode, label, count, x, TPS, address,
               org_found, location):
    """
    Assemble pseudo-opcodes.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    opcode: int, mandatory
       Value of the opcode for assembly

    label: str, mandatory
        Label of the current line (if any)

    count: int, mandatory
        Current assembly program line

    x: List, mandatory
        Line of program code (split into component parts).

    TPS: List, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    org_found: Boolean, mandatory
        Whether an "org" directive has been found

    location: str
        'rom' or 'ram'

    Returns
    -------
    err:
        False if no error, error text if error

    org_found: Boolean, mandatory
        Whether an "org" directive has been found

    TPS: List
        Assembled code

    location: str
        'rom' or 'ram'

    address: int
        the address to assemble to

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if opcode == 'org':
        org_found, location, address = asm_org(label, count, x, 'org')
        err = False
    if opcode == 'end':
        TPS = asm_end(TPS, address, count, label)
        err = False
    if opcode == 'pin':
        err = False
        err = asm_pin(chip, x[1], label, count)
    if opcode == '=':
        org_found, _unused1, _unused2 = asm_org(x[0], count, x, '=')
        err = False
    return err, org_found, TPS, location, address


def pass1(chip, program_name, _LABELS, TPS, TFILE):
    """
    Pass 1 of the two-pass assembly process.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    program_name: str, mandatory
        Name of the assembly language program file.

    _LABELS: List, Mandatory
        List for containing labels

    TPS: List, mandatory
        Assembled code

    TFILE: List, Mandatory
        Assembly language store


    Returns
    -------
    err:
        False if no error, error text if error

    _LABELS: List
        List for containing labels

    TFILE: List
        Assembly language store

    TPS: List
        Assembled code

    address: int
        the address to assemble to

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    try:
        program = open(program_name, 'r')
    except IOError:
        err = ('FATAL: Pass 1: File "' + program_name +
               '" does not exist.')
    else:
        print()
        print()
        print('Program Code:', program_name)
        print()
        err = False
        p_line = 0
        address = 0

        while True:
            line = program.readline()
            # if line is empty, end of file is reached
            if not line:
                break
            err, TFILE, p_line, address, _LABELS = \
                work_with_a_line_of_asm(chip, line, _LABELS,
                                        p_line, address, TFILE)
            if err:
                return err,  _LABELS, TPS, TFILE, address
        # Completed reading program into memory
        program.close()
        return err,  _LABELS, TPS, TFILE, address


def wrap_up(chip, location, TPS, _LABELS, object_file):
    """
    Pass 1 of the two-pass assembly process.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location: str, mandatory
        either 'ram' or 'rom'

    TPS: List, mandatory
        Assembled code

    _LABELS: List, mandatory
        List for containing labels

    object_file: str, mandatory
        The filename to write to

    Returns
    -------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    # Place assembled code into correct location
    if location == 'rom':
        chip.ROM = TPS

    if location == 'ram':
        chip.PRAM = TPS

    print()
    print('Labels:')
    print('Address   Label')
    for _i in range(len(_LABELS)):  # noqa
        print('{:>5}     {}'.format(_LABELS[_i]['address'],
              _LABELS[_i]['label']))
    write_program_to_file(TPS, object_file, location, _LABELS)
    return chip


def assemble_opcodes(chip, x, _LABELS, address, TPS, opcodeinfo, label, count):
    """
    Assemble the opcodes.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _LABELS: List, mandatory
        List for containing labels

    address: int
        the address to assemble to

    TPS: List, mandatory
        Assembled code

    opcodeinfo: str, mandatory
        JSON string containing an opcode's information

    label: str, mandatory
        If there is a label associated with this instruction, it will be here,
        "" otherwise.

    count: int, mandatory
        Assembly line number (used for printing during assembly)

    Returns
    -------
    chip: Processor, mandatory
        Instance of a processor to place the assembled code in.

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _LABELS: List
        List for containing labels

    address: int
        the address to assemble to

    TPS: List
        Assembled code

    opcodeinfo: str, mandatory
        JSON string containing an opcode's information

    label: str, mandatory
        If there is a label associated with this instruction, it will be here,
        "" otherwise.

    count: int, mandatory
        Assembly line number (used for printing during assembly)

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if x[0][-1] == ',':
        label = x[0]
        match_label(_LABELS, label, address)
        for _i in range(len([x])-1):
            x[_i] = x[_i + 1]
        x.pop(len([x])-1)
    opcode = x[0]

    address_left, address_right = split_address8(
        address)
    # Check for operand(s)
    if len(x) == 1:
        # Only operator, no operand
        TPS, address = assemble_1(opcodeinfo, label, TPS, address, count)  # noqa
    if len(x) == 2:
        # Operator & operand (generic)
        address, TPS, _LABELS = assemble_2(chip, x, opcode, address, TPS,
                                           _LABELS, address_left,
                                           address_right, label, count)
    if len(x) == 3:
        # Operator and 2 operands
        address, TPS, _LABELS = assemble_3(chip, x, _LABELS, TPS,
                                           address, address_left,
                                           address_right, label, count)
    return chip, x, _LABELS, address, TPS, opcodeinfo, label, count


def asm_main(chip, x, _LABELS, address, TPS, opcode, opcodeinfo,\
             label, count, org_found, location):
    """
    Assemble the program (opcode components).

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _LABELS: List, mandatory
        List for containing labels

    address: int
        the address to assemble to

    TPS: List, mandatory
        Assembled code

    opcode: str, mandatory
        opcode of this line of assembly code

    opcodeinfo: str, mandatory
        JSON string containing an opcode's information

    label: str, mandatory
        If there is a label associated with this instruction, it will be here,
        "" otherwise.

    count: int, mandatory
        Assembly line number (used for printing during assembly)

    org_found: Boolean, mandatory
        Whether an "org" directive has been found

    location: str, mandatory
        'rom' or 'ram'

    Returns
    -------
    chip: Processor, mandatory
        Instance of a processor to place the assembled code in.

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _LABELS: List
        List for containing labels

    address: int
        the address to assemble to

    TPS: List
        Assembled code

    opcodeinfo: str
        JSON string containing an opcode's information

    label: str
        If there is a label associated with this instruction, it will be here,
        "" otherwise.

    count: int
        Assembly line number (used for printing during assembly)

    err: Bool/Text depending on whether an error is raised,

    org_found: Boolean
        Whether an "org" directive has been found

    location: str
        'rom' or 'ram'

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    err = False
    if (opcode in ['org', 'end', 'pin', '=']) or (opcode is not None):
        if (opcode in ['org', 'end', 'pin', '=']):
            err, org_found, TPS, location, address = \
                asm_pseudo(chip, opcode, label, count, x, TPS,
                           address, org_found, location)
            if err:
                do_error(err)
                return False
        else:
            if org_found is True:
                chip, x, _LABELS, address, TPS, opcodeinfo, label, \
                    count = assemble_opcodes(chip, x, _LABELS,
                                             address, TPS, opcodeinfo,
                                            label, count)
            else:
                err = "FATAL: Pass 2: No 'org'" + \
                    " found at line: " + str(count + 1)
    else:
        err = "'FATAL: Pass 2:  Invalid mnemonic '" + \
            opcode + "' at line: " + str(count + 1)

    return chip, x, _LABELS, address, TPS, opcodeinfo, label, count, err, \
        org_found, location


def assemble(program_name: str, object_file: str, chip: Processor):
    """
    Main two-pass assembler for i4004 code.

    Parameters
    ----------
    program_name: str, mandatory
        Name of the source file to load

    object_file: str, mandatory
        Name of the output file in which to place the object code

    chip: Processor, mandatory
        Instance of a processor to place the assembled code in.

    Returns
    -------
    True if the code assembles correctly
    False if there are errors in the code

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    #     mccabe: MC0001 / assemble is too complex (44) - start
    #     mccabe: MC0001 / assemble is too complex (35)
    #     mccabe: MC0001 / assemble is too complex (30)
    #     mccabe: MC0001 / assemble is too complex (25)
    #     mccabe: MC0001 / assemble is too complex (21)
    #     mccabe: MC0001 / assemble is too complex (18)
    #     mccabe: MC0001 / assemble is too complex (13)
    #     mccabe: MC0001 / assemble is too complex (10)

    # Pass 0 - Initialise label tables, program storage etc
    _LABELS, TPS_SIZE, TPS, TFILE = pass0(chip)

    # Program Line Count
    count = 0

    # Pass 1
    err, _LABELS, TPS, TFILE, address = pass1(chip, program_name,
                                              _LABELS, TPS, TFILE)

    if err:
        do_error(err + "\nProgram Assembly halted @ Pass 1\n\n")
        return False

    # Pass 2
    print('Address  Label   Address        Assembled                    ' +
          '  Line     Op/Operand')
    print(' (Dec)            (Bin)           (Bin)          (Dec)')
    print('                            Word 1     Word 2')

    org_found = False
    location = ''

    while True:
        line = TFILE[count].strip()
        if len(line) == 0:
            break  # End of code
        x = line.split()
        label = ''

        # Check for initial comments
        if line[0] == '/':
            asm_comment(label, count, line)
        else:
            if len(line) > 0:
                if x[0][-1] == ',':
                    label = x[0]
                    opcode = x[1]
                    # Check to see if we are assembling a label
                    if '0' <= str(x[1])[:1] <= '9':
                        TPS = asm_label(TPS, address, x, count, label)
                        break
                else:
                    opcode = x[0]

                opcodeinfo = get_opcodeinfo(chip, 'S', opcode)
                chip, x, _LABELS, address, TPS, opcodeinfo, label, count, \
                    err, org_found, location = \
                    asm_main(chip, x, _LABELS, address, TPS, opcode,
                             opcodeinfo, label, count, org_found,
                             location)
                if err:
                    do_error(err)
                    break

        count = count + 1

    if err:
        print("Program Assembly halted")
        return False

    # Wrap up assembly process and write to file if necessary
    chip = wrap_up(chip, location, TPS, _LABELS, object_file)
    return True
