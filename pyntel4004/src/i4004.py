class processor:

    # Import processor internals
    import hardware.opcodes
    from hardware.reset import init_stack, init_command_registers, \
        init_ram, init_rom, init_dram, init_registers
    from hardware.machine import nop, ldm, ld, xch, add, sub, inc, \
        bbl, jin, src, fin, jun, jms, jcn, isz, fim, clb, clc, cmc, \
        stc, cma, iac, dac, ral, rar, tcc, daa, tcs, kbp, dcl
    from hardware.suboperation import set_carry, reset_carry,  \
        increment_register, write_pin10, read_complement_carry, \
        write_to_stack, read_from_stack, ones_complement, \
        decimal_to_binary, binary_to_decimal, insert_register

    # Operations to read the processor components
    # Some used internally,
    from hardware.reads import read_all_registers, read_all_ram, \
        read_all_rom, read_all_pram, read_accumulator, \
        read_current_ram_bank, read_carry, read_pin10

    # i4004 Processor characteristics
    MAX_4_BITS = 15             # Maximum value 4 bits can hold
    MSB = 8                     # Most significant bit value (4-bit)

    MEMORY_SIZE_RAM = 4096      # Number of 4-bit words in RAM
    MEMORY_SIZE_ROM = 4096      # Number of 4-bit words in ROM
    MEMORY_SIZE_DRAM = 4096     # Number of 4-bit words in PRAM
    PAGE_SIZE = 16              # Number of 8-bit words in a memory page
    STACK_SIZE = 3              # Number of 12-bit registers in the stack
    NO_REGISTERS = 16           # Number of registers
    NO_DRB = 8                  # Number of Data RAM Banks (0-7)
    NO_COMMAND_REGISTERS = 4    # Number of command registers

    # Creation of processor internals

    ACCUMULATOR = 0         # Initialise the accumulator
    ACBR = 0                # Accumulator Buffer Register
    CARRY = 0               # Reset the carry bit
    COMMAND_REGISTERS = []  # Command Register (Select Data RAM Bank)
    CURRENT_DRAM_BANK = 0   # Current Data RAM Bank
    PROGRAM_COUNTER = 0     # Program Counter - 12-bit value
    RAM = []                # RAM
    ROM = []                # ROM
    REGISTERS = []          # Registers
    PRAM = [[], [], []]     # Program RAM
    STACK = []              # The stack - 3 x 12-bit registers
    STACK_POINTER = 2       # Stack Pointer

    # Creation of processor simulated hardware

    # Pin 10 on the physical chip is the "test" pin
    # and can be read by the JCN instruction
    PIN_10_SIGNAL_TEST = 0

    # Instruction table
    INSTRUCTIONS = hardware.opcodes.instructions.opcodes

    # Initialise processor

    def __init__(self):
        # Initialise all the internals of the processor
        self.ACCUMULATOR = 0
        self.ACBR = 0
        self.CURRENT_RAM_BANK = 0
        self.PROGRAM_COUNTER == 0
        self.STACK_POINTER == 0
        self.init_stack()
        self.init_command_registers()
        self.init_registers()
        self.init_dram()
        self.init_ram()
        self.init_rom()
        self.reset_carry()

#  END OF PROCESSOR DEFINITION

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
        _TPS = chip.RAM
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
        words = opcodeinfo['words']
        if (words == 2):
            next_word = str(_TPS[chip.PROGRAM_COUNTER+1])
            OPCODE = str(OPCODE) + ',' + next_word

        # Only mnemonic with 2 characters - fix
        if (exe[:3] == 'ld '):
            exe = exe[:2] + exe[3:]

        # Ensure that the correct arguments are passed to the operations
        if (exe[:6] == 'fim(rp'):
            custom_opcode = True
            value = str(_TPS[chip.PROGRAM_COUNTER + 1])
            cop = exe.replace('data8', value)
            exe = exe.replace('rp', '').replace('data8)', '') + value + ')'

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
            print('  {:>7}  {:<10}'.format(OPCODE, cop))
        else:
            print('  {:>7}  {:<10}'.format(OPCODE, exe))

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


def get_addr_for_label(_L, label: str):
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


def do_assembly_error(message: str):
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
    label_address = get_addr_for_label(_LABELS, dest_label)
    val_left = bin(int(label_address))[2:].zfill(8)[:4]
    val_right = bin(int(label_address))[2:].zfill(8)[4:]
    return n_opcode, label_address, opcodeinfo['words'], val_left, val_right, \
        bit1, bit2


def print_ln(f0, f1, f2, f3, f4, f5, f6, f7, f8,
             f9, f10, f11, f12, f13, f14, f15, f16):
    fmt = '{:>4} {:<10} {} {}  {} {} {} {} {:>7} {:>7} {:<4}{:<8}{:<3}'
    fmt = fmt + ' {:<3} {:<3} {} {}'
    print(fmt.format(f0, f1, f2, f3, f4, f5, f6, f7, f8,
                     f9, f10, f11, f12, f13, f14, f15, f16))


def assemble_2(x, opcode, address, TPS, _LABELS, address_left,
               address_right, label, count):
   
    # pad out for the only 2-character mnemonic
    if (opcode == 'ld'):
        opcode = 'ld '
    fullopcode = opcode + '(' + x[1] + ')'
    if (opcode in ('jun', 'jms')):
 
        # Special case for JUN and JMS
        if (opcode == 'jun'):
            decimal_code = 64
        if (opcode == 'jms'):
            decimal_code = 80
        fullopcode = opcode + '(address12)'
        opcodeinfo = get_opcodeinfo('L', fullopcode)
        dest_label = x[1]
        label_addr = get_addr_for_label(_LABELS, dest_label)
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
            register = x[1]
            fullopcode = 'src(' + register + ')'
            opcodeinfo = get_opcodeinfo('L', fullopcode)
            bit1, bit2 = get_bits(opcodeinfo)
            TPS[address] = opcodeinfo['opcode']
            print_ln(address, label, address_left, address_right, bit1, bit2, '',
                    '', '', '', '', str(count), opcode, str(x[1]), '', '', '')
            address = address + opcodeinfo['words']
        else:
            opcodeinfo = get_opcodeinfo('L', fullopcode)
            bit1, bit2 = get_bits(opcodeinfo)
            TPS[address] = opcodeinfo['opcode']
            print_ln(address, label, address_left, address_right, bit1, bit2, '',
                    '', '', '', '', str(count), opcode, str(x[1]), '', '', '')
            address = address + opcodeinfo['words']
    return address, TPS, _LABELS


def assemble(program_name: str, chip):
    # Reset label table for this program
    _LABELS = []

    # Maximum size of program memory
    TPS_SIZE = max([chip.MEMORY_SIZE_ROM,
                    chip.MEMORY_SIZE_RAM, chip.MEMORY_SIZE_RAM])

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
    print('Address  Label   Address        Assembled                    ' +
          'Line     Op/Operand')
    print(' (Dec)            (Bin)           (Bin)          (Dec)')
    print('                            Word 1      Word 2')
    ORG_FOUND = False
    location = ''
    count = 0
    ERR = False
    p_line = 0
    address = 0

    while True:
        line = program.readline()
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
                match_label(_LABELS, parts[0], address)
                # Set opcode
                opcode = parts[1][:3]
            else:
                # Set opcode
                opcode = parts[0][:3]
            # Custom opcodes
            if (opcode == 'ld()'):
                opcode = 'ld '
            if not (opcode in ('org', '/', 'end', 'pin')):
                opcodeinfo = get_opcodeinfo('S', opcode)
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
            print_ln('', label, '', '', '', '', '', '', '', '', '', '', '',
                     '', str(count), line, '')
            pass
        else:
            if (len(line) > 0):
                if (x[0][-1] == ','):
                    label = x[0]
                    opcode = x[1]
                else:
                    opcode = x[0]
                opcodeinfo = get_opcodeinfo('S', opcode)
                if (opcode in ['org', 'end', 'pin']) or (opcode is not None):
                    if (opcode in ['org', 'end', 'pin']):
                        if (opcode == 'org'):
                            ORG_FOUND = True
                            print_ln('', label,  '', '', '', '', '', '', '',
                                     '', '', '','','', str(count), opcode, str(x[1]))
                            if (x[1] == 'rom') or (x[1] == 'ram'):
                                location = x[1]
                                address = 0
                            else:
                                location = 'ram'
                                address = int(str(x[1]))
                        if (opcode == 'end'):
                            print_ln('', label, '', '', '', '', '',  '', '', '',
                                      '','','','',str(count), opcode, '')
                            # pseudo-opcode (directive "end")
                            TPS[address] = 255
                            # break
                        if (opcode == 'pin'):
                            result = chip.write_pin10(int(x[1]))
                            if (result is False):
                                ERR = do_assembly_error(
                                    "FATAL: Pass 2:  Invalid value for "
                                    + "TEST PIN 10 at line " + count)
                            print_ln('', label, '', '', '', '', '', '', '', '', '',
                                     '', '', '', str(count), opcode, str(x[1]))
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
                                print_ln(address, label, address_left, address_right, bit1, bit2, '','','',TPS[address],'',str(count), opcode, '','','', '')
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
                                    fullopcode = 'jcn(' + str(bin_conditions) + ',address8)'
                                    opcodeinfo = get_opcodeinfo('L', fullopcode)
                                    label_address = get_addr_for_label(_LABELS, dest_label)
                                    val_left = bin(int(label_address))[2:].zfill(8)[:4]
                                    val_right = bin(int(label_address))[2:].zfill(8)[4:]
                                    bit1, bit2 = get_bits(opcodeinfo)
                                    TPS[address] = opcodeinfo['opcode']
                                    TPS[address + 1] = label_address
                                    print_ln(address, label, address_left, address_right, bit1, bit2, val_left, val_right, str(TPS[address]) + "," + str(TPS[address + 1]), str(count), opcode, str(x[1]), str(x[2]),'','','', '')
                                    address = address + opcodeinfo['words']
                                if (opcode == 'isz'):
                                    n_opcode, label_addr, words, \
                                        addr_left, addr_right, \
                                        bit1, bit2 = \
                                        assemble_isz(x[1], label, x[2], _LABELS)
                                    TPS[address] = n_opcode
                                    TPS[address + 1] = label_address
                                    print_ln(address, label, addr_left, addr_right, bit1, bit2, val_left, val_right, str(TPS[address]) + "," + str(TPS[address + 1]), str(count), opcode, str(x[1]), str(x[2]),'','','', '')
                                    address = address + words
                                if (opcode not in ('jcn', 'isz')):
                                    d_type = ''
                                    if (int(x[2]) <= 256):
                                        d_type = 'data8'
                                    val_left = bin(int(x[2]))[2:].zfill(8)[:4]
                                    val_right = bin(int(x[2]))[2:].zfill(8)[4:]
                                    fullopcode = opcode + "(" + x[1] + "," + d_type + ")"
                                    opcodeinfo = get_opcodeinfo('L', fullopcode)
                                    bit1, bit2 = get_bits(opcodeinfo)
                                    TPS[address] = opcodeinfo['opcode']
                                    TPS[address+1] = int(x[2])
                                    print_ln(address, label, address_left, address_right, bit1, bit2, val_left, val_right, str(TPS[address]) + "," + str(TPS[address + 1]), str(count), opcode, str(x[1]), str(x[2]),'','','', '')
                                    address = address + opcodeinfo['words']
                        else:
                            ERR = do_assembly_error("FATAL: Pass 2:  No 'org' found at line: " + count + 1)
                            break
                else:
                    ERR = do_assembly_error("'FATAL: Pass 2:  Invalid mnemonic '" + opcode + "' at line: " + count + 1)
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
        chip.RAM = TPS

    print('Labels:')
    print('Address   Label')
    for _i in range(len(_LABELS)):
        print('{:>5}     {}'.format(_LABELS[_i]['address'], _LABELS[_i]['label']))
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
    print('Accumulator : ' + str(chip.read_accumulator()) + '  (0b ' + str(chip.decimal_to_binary(chip.read_accumulator())) + ')')
    print('Carry       :', chip.read_carry())
    print()
