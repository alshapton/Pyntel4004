# Import i4004 processor

from hardware.processor import processor

##############################################################################
#  _ _  _    ___   ___  _  _     ______                 _       _            #
# (_) || |  / _ \ / _ \| || |   |  ____|               | |     | |           #
#  _| || |_| | | | | | | || |_  | |__   _ __ ___  _   _| | __ _| |_ ___  _ _ #
# | |__   _| | | | | | |__   _| |  __| | '_ ` _ \| | | | |/ _` | __/ _ \| '_|#
# | |  | | | |_| | |_| |  | |   | |____| | | | | | |_| | | (_| | || (_) | |  #
# |_|  |_|  \___/ \___/   |_|   |______|_| |_| |_|\__,_|_|\__,_|\__\___/|_|  #
#                                                                            #
##############################################################################


def execute(chip, location, PC, monitor):
    _TPS = []
    if (location == 'rom'):
        _TPS = chip.ROM
    else:
        _TPS = chip.PRAM

    chip.PROGRAM_COUNTER = 0
    opcode = 0
    while opcode != 255:  # pseudo-opcode (directive) for "end"

        custom_opcode = False
        OPCODE = _TPS[chip.PROGRAM_COUNTER]
        if (OPCODE == 255):  # pseudo-opcode (directive "end" - stop program)
            print('           end')
            break
        opcodeinfo = next((item for item in chip.INSTRUCTIONS
                          if item['opcode'] == OPCODE), None)
        exe = opcodeinfo['mnemonic']
        print("exe=",exe)
        if (exe == '-'):
            break
        words = opcodeinfo['words']
        if (words == 2):
            next_word = str(_TPS[chip.PROGRAM_COUNTER+1])
            OPCODE3 = str(OPCODE) + ',' + next_word

        # Only mnemonic with 2 characters - fix
        if (exe[:3] == 'ld '):
            exe = exe[:2] + exe[3:]

        # Ensure that the correct arguments are passed to the operations
        if (exe[:3] == 'fim'):
            custom_opcode = True
            value = str(_TPS[chip.PROGRAM_COUNTER + 1])
            cop = exe.replace('data8', value)
            exe = exe.replace('p', '').replace('data8)', '') + value + ')'

        if (exe[:3] == 'isz'):
            # Remove opcode from 1st byte to get register
            register = bin(_TPS[chip.PROGRAM_COUNTER] & 15)[2:].zfill(8)[4:]
            address = str(_TPS[chip.PROGRAM_COUNTER + 1])
            exe = 'isz(' + str(int(register, 2)) + ',' + str(address) + ')'

        if (exe[:4] == 'jcn('):
            custom_opcode = True
            address = _TPS[chip.PROGRAM_COUNTER+1]
            conditions = (bin(_TPS[chip.PROGRAM_COUNTER])[2:].zfill(8)[4:])
            b10address = str(address)
            cop = exe.replace('address8', b10address)
            exe = exe[:4] + str(int(conditions, 2)) + ',' + b10address + ')'

        # if (exe[:4] in ('src(')):
        #    custom_opcode = True

        if (exe[:4] in ('jun(', 'jms(')):
            custom_opcode = True
            # Remove opcode from 1st byte
            hvalue = bin(_TPS[chip.PROGRAM_COUNTER] &
                         0xffff0000)[2:].zfill(8)[:4]
            lvalue = bin(_TPS[chip.PROGRAM_COUNTER+1])[2:].zfill(8)
            whole_value = str(int(hvalue + lvalue, 2))
            cop = exe.replace('address12', whole_value)
            exe = exe[:4] + whole_value + ')'

        if (custom_opcode):
            custom_opcode = False
            print('  {:>7}  {:<10}'.format(OPCODE, cop.replace('()', '')))
        else:
            print('  {:>7}  {:<10}'.format(OPCODE, exe.replace('()', '')))

        exe = 'chip.' + exe

        # Evaluate the command (some commands may change
        # the PROGRAM_COUNTER here)
        eval(exe)
        monitor_command = 'none'
        if (monitor):
            while (monitor_command != ''):
                monitor_command = input('>> ').lower()
                if (monitor_command == 'regs'):
                    print('0-> ' + str(chip.REGISTERS) + ' <-15')
                    continue
                if (monitor_command == 'stack'):
                    for _i in range(chip.STACK_SIZE-1, -1, -1):
                        if (_i == chip.STACK_POINTER):
                            pointer = '==>'
                        else:
                            pointer = '-->'
                        print("[ " + str(_i) + "] " + pointer + "[ " +
                              str(chip.STACK[_i]) + ' ]')
                if (monitor_command == 'pc'):
                    print('PC = ', chip.PROGRAM_COUNTER)
                if (monitor_command == 'carry'):
                    print('CARRY = ', chip.read_carry())
                if (monitor_command == 'ram'):
                    print('RAM = ', chip.RAM)
                if (monitor_command == 'pram'):
                    print('PRAM = ', chip.PRAM)
                if (monitor_command == 'rom'):
                    print('ROM = ', chip.ROM)
                if (monitor_command[:3] == 'reg'):
                    register = int(monitor_command[3:])
                    print('REG[' + monitor_command[3:].strip()+'] = ' +
                          str(chip.REGISTERS[register]))
                if (monitor_command == 'acc'):
                    print('ACC =', chip.read_accumulator())
                if (monitor_command == 'pin10'):
                    print('PIN10 = ', chip.read_pin10())
                if (monitor_command == 'crb'):
                    print('CURRENT RAM BANK = ', chip.read_current_ram_bank())
                if (monitor_command == 'off'):
                    monitor_command = ''
                    monitor = False
                if (monitor_command == 'q'):
                    monitor = False
                    opcode = 255
                    break

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


def add_label(_L, label: str):
    label_exists = next((item for item in _L
                        if str(item["label"]) == label), None)
    if not label_exists:
        _L.append({'label': label, 'address': -1})
    else:
        return (-1)
    return _L


def match_label(_L, label: str, address):
    for _i in range(len(_L)):
        if (_L[_i]['label'] == label):
            _L[_i]['address'] = address
    return _L


def get_label_addr(_L, label: str):
    label_address = -1
    for _i in _L:
        if (_i['label'] == label + ','):
            label_address = _i['address']
    return label_address


def get_bits(opcodeinfo):
    # Return an opcode 2x 4-bit nibbles
    bit1 = opcodeinfo['bits'][0]
    bit2 = opcodeinfo['bits'][1]
    return bit1, bit2


def do_error(message: str):
    # Print Assembly error
    print()
    print(message)
    return True


def get_opcodeinfo(ls: str, mnemonic: str):
    if (ls.upper() == 'S'):
        return next((item for item in chip.INSTRUCTIONS
                    if str(item["mnemonic"][:3]) == mnemonic), None)
    else:
        return next((item for item in chip.INSTRUCTIONS
                    if str(item["mnemonic"]) == mnemonic), None)


def assemble_isz(register, label, dest_label, _LABELS):
    n_opcode = 112 + int(register)
    opcodeinfo = next((item for item in chip.INSTRUCTIONS
                      if item["opcode"] == n_opcode), None)
    bit1, bit2 = get_bits(opcodeinfo)
    label_address = get_label_addr(_LABELS, dest_label)
    val_left = bin(int(label_address))[2:].zfill(8)[:4]
    val_right = bin(int(label_address))[2:].zfill(8)[4:]
    return n_opcode, label_address, opcodeinfo['words'], val_left, val_right, \
        bit1, bit2


def print_ln(f0, f1, f2, f3, f4, f5, f6, f7, f8,
             f9, f10, f11, f12, f13, f14, f15, f16):
    fmt = '{:>4} {:<10} {:>4} {:>4}  {:>4} {:>4} {:>4} '
    fmt = fmt + '{:>4} {:>7} {:<4} {:<4}{:<8}{:<3}'
    fmt = fmt + ' {:<3} {:<3} {} {}'
    print(fmt.format(f0, f1, f2, f3, f4, f5, f6, f7, f8,
                     f9, f10, f11, f12, f13, f14, f15, f16))


def assemble_2(x, opcode, address, TPS, _LABELS, address_left,
               address_right, label, count):
    # pad out for the only 2-character mnemonic
    if (opcode == 'ld'):
        opcode = 'ld '
    f_opcode = opcode + '(' + x[1] + ')'
    if (opcode in ('jun', 'jms')):
        # Special case for JUN and JMS
        if (opcode == 'jun'):
            decimal_code = 64
        if (opcode == 'jms'):
            decimal_code = 80
        f_opcode = opcode + '(address12)'
        opcodeinfo = get_opcodeinfo('L', f_opcode)
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
        if (opcode == 'src'):
            register = x[1].lower().replace('p', '').replace('r', '')
            f_opcode = 'src(' + register + ')'
            opcodeinfo = get_opcodeinfo('L', f_opcode)
            bit1, bit2 = get_bits(opcodeinfo)
            TPS[address] = opcodeinfo['opcode']
            print_ln(address, label, address_left, address_right, bit1,
                     bit2, '', '', TPS[address], '', '', str(count), opcode,
                     str(x[1]), '', '', '')
            address = address + opcodeinfo['words']
        else:
            opcodeinfo = get_opcodeinfo('L', f_opcode)
            bit1, bit2 = get_bits(opcodeinfo)
            TPS[address] = opcodeinfo['opcode']
            print_ln(address, label, address_left, address_right, bit1, bit2,
                     '', '', TPS[address], '', '', str(count), opcode,
                     str(x[1]), '', '', '')
            address = address + opcodeinfo['words']
    return address, TPS, _LABELS


def validate_inc(parts, line):
    if (len(parts) == 1):
        if (parts[0] == 'inc'):
            return do_error('No register value at line ' + str(line))
    if (len(parts) == 2):
        if ((parts[1] == 'inc') and (parts[0][-1])):
            return do_error('No register value at line ' + str(line))
        if ((parts[0] == 'inc') and ((int(parts[1]) > 15) or
           (int(parts[1]) < 0))):
            return do_error('Invalid register value (' + parts[1] +
                            ') at line ' + str(line))
    return False


def assemble(program_name: str, chip):
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

    program = open(program_name, 'r')
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
        print(line)
        constant = False
        # if line is empty, end of file is reached
        if not line:
            break
        else:
            # Work with a line of assembly code
            parts = line.split()
            if (parts[0][-1] == ','):
                # Found a label, now add it to the label table
                if add_label(_LABELS, parts[0]) == -1:
                    ERR = ('FATAL: Pass 1: Duplicate label: ' + parts[0] +
                           ' at line ' + str(p_line + 1))
                    break
                # Attach value to a label
                if ('0' <= str(parts[1])[:1] <= '9'):
                    constant = True
                    match_label(_LABELS, parts[0], parts[1])
                else:
                    match_label(_LABELS, parts[0], address)
                # Set opcode
                opcode = parts[1][:3]
            else:
                # Set opcode
                opcode = parts[0][:3]
            if (opcode[:3] == 'inc'):
                ERR = validate_inc(parts, p_line + 1)
                if ERR:
                    break
            # Custom opcodes
            print(len(opcode))
            print(opcode)
            if not constant:
                if (opcode == 'ld()' or opcode[:2] == 'ld'):
                    opcode = 'ld '
                print(opcode)
                if not (opcode in ('org', '/', 'end', 'pin')):
                    print('opcode=', opcode)
                    opcodeinfo = get_opcodeinfo('S', opcode)
                    print(opcodeinfo)
                    address = address + opcodeinfo['words']
            TFILE[p_line] = line.strip()
            p_line = p_line + 1
    # Completed reading program into memory
    program.close()

    if ERR:
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
        if (len(line) == 0):
            break  # End of code

        x = line.split()
        label = ''

        # Check for initial comments
        if (line[0] == '/'):
            print_ln('', label, ' ', ' ', ' ', ' ', ' ', ' ', ' ',  ' ',
                     ' ', str(count), line, ' ', '', '', '',)
            pass
        else:
            if (len(line) > 0):
                if (x[0][-1] == ','):
                    label = x[0]
                    opcode = x[1]
                    # Check to see if we are assembling a label
                    if ('0' <= str(x[1])[:1] <= '9'):
                        TPS[address] = int(x[1])
                        print_ln('', '',  '', '', '', '', '', '', '', '', '',
                                 str(count), label, str(x[1]), '', '', '',)
                        break
                else:
                    opcode = x[0]
                opcodeinfo = get_opcodeinfo('S', opcode)
                if (opcode in ['org', 'end', 'pin']) or (opcode is not None):
                    if (opcode in ['org', 'end', 'pin']):
                        if (opcode == 'org'):
                            ORG_FOUND = True
                            print_ln('', label,  '', '', '', '', '', '', '',
                                     '', '', str(count), opcode, str(x[1]),
                                     '', '', '',)
                            if (x[1] == 'rom') or (x[1] == 'ram'):
                                location = x[1]
                                address = 0
                            else:
                                location = 'ram'
                                address = int(str(x[1]))
                        if (opcode == 'end'):
                            print_ln('', label, '', '', '', '', '',  '', '',
                                     '', '', str(count), opcode, '', '',
                                     '', '')
                            # pseudo-opcode (directive "end")
                            TPS[address] = 255
                            # break
                        if (opcode == 'pin'):
                            result = chip.write_pin10(int(x[1]))
                            if (result is False):
                                ERR = do_error(
                                    "FATAL: Pass 2:  Invalid value for "
                                    + "TEST PIN 10 at line " + count)
                            print_ln('', label, '', '', '', '', '', '', '', '',
                                     '', '', '', '', str(count), opcode,
                                     str(x[1]))
                        pass
                    else:
                        if (ORG_FOUND is True):
                            if (x[0][-1] == ','):
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
                            if (len(x) == 2):
                                address, TPS, _LABELS = \
                                 assemble_2(x, opcode, address, TPS,
                                            _LABELS, address_left,
                                            address_right, label,
                                            count)
                            if (len(x) == 1):
                                # Only operator, no operand
                                bit1, bit2 = get_bits(opcodeinfo)
                                TPS[address] = opcodeinfo['opcode']
                                print_ln(address, label, address_left,
                                         address_right, bit1, bit2, '', '',
                                         TPS[address], '', '', str(count),
                                         opcode, '', '', '', '')
                                address = address + opcodeinfo['words']
                            if (len(x) == 3):
                                opcode = x[0]
                                # Operator and 2 operands
                                if (opcode == 'jcn'):
                                    conditions = x[1].upper()
                                    dest_label = x[2]
                                    bin_conditions = 0
                                    if ('I' in conditions):
                                        bin_conditions = 8
                                    if ('A' in conditions):
                                        bin_conditions = bin_conditions + 4
                                    if ('C' in conditions):
                                        bin_conditions = bin_conditions + 2
                                    if ('T' in conditions):
                                        bin_conditions = bin_conditions + 1
                                    f_opcode = 'jcn(' + str(bin_conditions) \
                                        + ',address8)'
                                    opcodeinfo = get_opcodeinfo('L', f_opcode)
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
                                if (opcode[:3] == 'fim'):
                                    f_opcode = x[0] + '(' + x[1] + ',data8)'
                                    opcodeinfo = get_opcodeinfo('L', f_opcode)
                                    print(opcodeinfo)
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
                                if (opcode == 'isz'):
                                    n_opcode, label_addr, words, \
                                        addr_left, addr_right, \
                                        bit1, bit2 = \
                                        assemble_isz(x[1], label, x[2],
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
                                if (opcode not in ('jcn', 'fim', 'isz')):
                                    d_type = ''
                                    if (int(x[2]) <= 256):
                                        d_type = 'data8'
                                    val_left = bin(int(x[2]))[2:].zfill(8)[:4]
                                    val_right = bin(int(x[2]))[2:].zfill(8)[4:]
                                    f_opcode = opcode + "(" + \
                                        x[1] + "," + d_type + ")"
                                    opcodeinfo = get_opcodeinfo('L', f_opcode)
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
    if (location == 'rom'):
        chip.ROM = TPS

    if (location == 'ram'):
        chip.PRAM = TPS

    print('Labels:')
    print('Address   Label')
    for _i in range(len(_LABELS)):
        print('{:>5}     {}'.format(_LABELS[_i]['address'],
              _LABELS[_i]['label']))
    write_program_to_file(TPS, program_name)
    return True


def write_program_to_file(program, filename):
    with open(filename + '.obj', "w") as output:
        for location in program:
            output.write(str(hex(location)[2:]))
    return True


# Create new instance of a processor
chip = processor()

result = assemble('example.asm', chip)
if result:
    print()
    print('EXECUTING : ')
    print()
    execute(chip, 'rom', 0, True)
    print()
    acc = str(chip.read_accumulator())
    print('Accumulator : ' + acc +
          '  (0b ' + str(chip.decimal_to_binary(acc)) + ')')
    print('Carry       :', chip.read_carry())
    print()
