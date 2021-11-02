# Import i4004 processor

from hardware.processor import processor
from hardware.suboperation import split_address8

# Assembler imports
from assembler.supporting import add_label, assemble_isz, assemble_2, \
    assemble_fim, assemble_jcn, do_error, get_bits, \
    match_label, print_ln, \
    validate_inc, write_program_to_file

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
                    label_content = parts[1]
                else:
                    label_content = address
                # An EQUATE statement (indicated by "=")
                if parts[1] == '=':
                    constant = True
                    label_content = parts[2]

                match_label(_LABELS, parts[0], label_content)
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
                if opcode not in ('org', '/', 'end', 'pin', '='):
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
                if (opcode in ['org', 'end', 'pin', '=']) or \
                   (opcode is not None):
                    if (opcode in ['org', 'end', 'pin', '=']):
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
                        if opcode == '=':
                            ORG_FOUND = True
                            print_ln('', x[0],  '', '', '', '', '', '', '',
                                     '', '', str(count), opcode, str(x[2]),
                                     '', '', '',)
                    else:
                        if ORG_FOUND is True:
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
                            # Operator & operand (generic)
                            if len(x) == 2:
                                print(x)
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
                                    address, TPS, _LABELS = \
                                        assemble_jcn(chip, x, _LABELS, TPS,
                                                     address, address_left,
                                                     address_right, label,
                                                     count)
                                if opcode[:3] == 'fim':
                                    address, TPS, _LABELS = \
                                        assemble_fim(chip, x, _LABELS, TPS,
                                                     address, address_left,
                                                     address_right, label,
                                                     count)
                                if opcode == 'isz':
                                    address, TPS, _LABELS = \
                                        assemble_isz(chip, x, _LABELS, TPS,
                                                     address, address_left,
                                                     address_right, label,
                                                     count)
                                if opcode not in ('jcn', 'fim', 'isz'):
                                    d_type = ''
                                    if int(x[2]) <= 256:
                                        d_type = 'data8'
                                    val_left, val_right = split_address8(
                                        int(x[2]))
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
