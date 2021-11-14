from hardware.processor import Processor
from hardware.suboperation import split_address8
from shared.shared import do_error, get_opcodeinfo, \
    get_opcodeinfobyopcode


def add_label(_L, label: str):
    """
    Add a label to the label table (if it does not exist already).

    Parameters
    ----------
    _L : list, mandatory
        A list of the existing labels
    label: str, mandatory
        A candidate new label

    Returns
    -------
    -1          if the label already existed and was not added
    _L : list
                the list of labels with the new label appended

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    try:
        label_exists = next((item for item in _L
                            if str(item["label"]) == label), None)
    except:  # noqa
        pass
    if not label_exists:
        _L.append({'label': label, 'address': -1})
    else:
        return -1
    return _L


def decode_conditions(conditions: str):
    """
    Decode the conditions from a JCN mnemonic to a decimal value.

    Parameters
    ----------
    conditions: str, mandatory
        List of a maximum of 4 conditions

    Returns
    -------
    int_conditions: int
        Integer value of the conditions

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    int_conditions = 0

    if 'I' in conditions:
        int_conditions = 8
    if 'A' in conditions:
        int_conditions = int_conditions + 4
    if 'C' in conditions:
        int_conditions = int_conditions + 2
    if 'T' in conditions:
        int_conditions = int_conditions + 1

    return int_conditions


def get_bits(opcodeinfo):
    """
    Return an opcode 2x 4-bit nibbles.

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
    -----
    N/A

    """
    bit1 = opcodeinfo['bits'][0]
    bit2 = opcodeinfo['bits'][1]
    return bit1, bit2


def match_label(_L, label: str, address):
    """
    Given a label and an address, add it (if required) to the list of labels.

    Parameters
    ----------
    _L: list, mandatory
        A list of the known labels and their addresses

    label: str, mandatory
        The potential new label

    address: int, mandatory
        The address of the potential new label

    Returns
    -------
    label_address
        The integer address of the label

    Raises
    ------
    N/A

    Notes
    -----
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
    -----
    This will return -1 if the label is not found

    """
    label_address = -1
    for _i in _L:
        if _i['label'] == label + ',':
            label_address = _i['address']
    return label_address


def assemble_isz(chip: Processor, x, register, _LABELS, TPS,
                 address, a_l, a_r, label, count):
    """
    Function to correctly assemble the ISZ instruction.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    register: int, mandatory
        The register which will be compared in this instruction
    _LABELS: list, mandatory
        List of valid labels

    TPS: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    address: int, mandatory
        Address in memory to place the newly assembled instruction

    a_l, a_r: str, mandatory
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
    -----
    N/A

    """
    n_opcode = 112 + int(register)
    opcodeinfo = get_opcodeinfobyopcode(chip, n_opcode)
    bit1, bit2 = get_bits(opcodeinfo)
    label_address = get_label_addr(_LABELS, x[2])
    vl, vr = split_address8(int(label_address))
    TPS[address] = n_opcode
    TPS[address + 1] = label_address
    print_ln(address, label, a_l,
             a_r, bit1, bit2, vl,
             vr, str(TPS[address]) +
             "," + str(TPS[address + 1]), '',
             '', str(count), x[0], str(x[1]),
             str(x[2]), '', '')
    address = address + opcodeinfo['words']
    return address, TPS, _LABELS


def pass0(chip):
    """
    Initialise storage for assembly.

    Parameters
    ----------
    chip: Processor, mandatory
        Instance of a processor to place the assembled code in.

    Returns
    -------
    _LABELS: List
        List for containing labels

    TPS_SIZE: Integer
        Maximum size of program memory

    TPS: List
        Program store

    TPS_FILE: List
        Assembly language store

    Raises
    ------
    N/A

    Notes
    -----
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

    return _LABELS, TPS_SIZE, TPS, TFILE


def assemble_fim(self, x, _LABELS, TPS, address, label, count):
    """
    Function to assemble FIM instruction.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _LABELS: list, mandatory
        List of valid labels

    TPS: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    address: int, mandatory
        Current program counter address

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
    -----
    N/A

    """
    f_opcode = x[0] + '(' + x[1] + ',data8)'
    opcodeinfo = get_opcodeinfo(self, 'L', f_opcode)
    TPS[address] = opcodeinfo['opcode']
    TPS[address + 1] = int(x[2])
    bit1, bit2 = get_bits(opcodeinfo)
    print_ln(address, label, '' '', '', bit1, bit2, '', '',
             str(TPS[address]) + "," + str(TPS[address + 1]),
             str(count), x[0], str(x[1]),
             str(x[2]), '', '', '', '')
    address = address + opcodeinfo['words']
    return address, TPS, _LABELS


def assemble_jcn(self, x, _LABELS, TPS, address, address_left,
                 address_right, label, count):
    """
    Function to assemble JCN instructions.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _LABELS: list, mandatory
        List of valid labels

    TPS: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    address: int, mandatory
        Address in memory to place the newly assembled instruction

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
    -----
    N/A

    """
    conditions = x[1].upper()
    dest_label = x[2]
    if '0' <= conditions <= '9':
        bin_conditions = conditions
    else:
        bin_conditions = decode_conditions(conditions)
    f_opcode = 'jcn(' + str(bin_conditions) + ',address8)'
    opcodeinfo = get_opcodeinfo(self, 'L', f_opcode)
    label_addr = int(get_label_addr(_LABELS, dest_label))
    vl, vr = split_address8(label_addr)
    bit1, bit2 = get_bits(opcodeinfo)
    TPS[address] = opcodeinfo['opcode']
    TPS[address + 1] = label_addr
    print_ln(address, label, address_left, address_right, bit1, bit2,
             vl, vr, str(TPS[address]) + "," + str(TPS[address + 1]),
             '', '', '', str(count), x[0], str(x[1]), str(x[2]), '')
    address = address + opcodeinfo['words']
    return address, TPS, _LABELS


def assemble_2(chip: Processor, x, opcode, address, TPS, _LABELS, address_left,
               address_right, label, count):
    """
    Function to assemble specific instructions.

    Parameters
    ----------
    chip : Processor, mandatory
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
    -----
    N/A

    """
    # pad out for the only 2-character mnemonic
    if opcode == 'ld':
        opcode = 'ld '
    addx = get_label_addr(_LABELS, x[1])
    print(addx)
    if addx == -1:
        addx = x[1]
    f_opcode = opcode + '(' + str(addx) + ')'
    print(f_opcode)

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
    return address, TPS, _LABELS


def print_ln(f0, f1, f2, f3, f4, f5, f6, f7, f8,
             f9, f10, f11, f12, f13, f14, f15, f16):
    """
    Print a set of items to the screen in a standard, columnar fashion.

    Parameters
    ----------
    f0 : str, optional
        Parameter to print

    f1 : str, optional
        Parameter to print

    f2 : str, optional
        Parameter to print

    f3 : str, optional
        Parameter to print

    f4 : str, optional
        Parameter to print

    f5 : str, optional
        Parameter to print

    f6 : str, optional
        Parameter to print

    f7 : str, optional
        Parameter to print

    f8 : str, optional
        Parameter to print

    f9 : str, optional
        Parameter to print

    f10 : str, optional
        Parameter to print

    f11 : str, optional
        Parameter to print

    f12 : str, optional
        Parameter to print

    f13 : str, optional
        Parameter to print

    f14 : str, optional
        Parameter to print

    f15 : str, optional
        Parameter to print

    f16 : str, optional
        Parameter to print

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
    fmt = '{:>4} {:<10} {:>4} {:>4}  {:>4} {:>4} {:>4} '
    fmt = fmt + '{:>4} {:>7} {:<4} {:<4}{:<8}{:<3}'
    fmt = fmt + ' {:<3} {:<3} {} {}'
    print(fmt.format(f0, f1, f2, f3, f4, f5, f6, f7, f8,
                     f9, f10, f11, f12, f13, f14, f15, f16))


def validate_inc(parts, line):
    """
    Validate the contents (i.e. the parameters) of an INC command.

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
    -----
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


def work_with_a_line_of_asm(chip, line, _LABELS, p_line, address, TFILE):
    """
    Analyse a single line of code.

    Parameters
    ----------
    chip: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    line: str, mandatory
        line of assembly code read in from a file

    _LABELS: List, Mandatory
        List for containing labels

    p_line: int, mandatory
        numbered line of assembly language program

    address: int, Mandatory
        Current address of memory for assembly

    TFILE: List, Mandatory
        Assembly language store

    Returns
    -------
    err:
        False if no error, error text if error

    TFILE: List
        Assembly language store

    p_line: int
        numbered line of assembly language program

    address: int
        Current address of memory for assembly

    _LABELS: List, Mandatory
        List for containing labels

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    constant = False
    err = False
    # Work with a line of assembly code
    parts = line.split()
    if parts[0][-1] == ',':
        # Found a label, now add it to the label table
        if add_label(_LABELS, parts[0]) == -1:
            err = ('FATAL: Pass 1: Duplicate label: ' + parts[0] +
                   ' at line ' + str(p_line + 1))
            return err, TFILE, p_line, 0, _LABELS
        # Attach value to a label
        if '0' <= str(parts[1])[:1] <= '9':
            constant = True
            label_content = parts[1]
        else:
            label_content = address
        # An EQUATE statement (indicated by "=")
        if parts[1] == '=':
            constant = True
            label_content = int(parts[2])

        match_label(_LABELS, parts[0], label_content)
        # Set opcode
        opcode = parts[1][:3]
    else:
        # Set opcode
        opcode = parts[0][:3]
    if opcode[:3] == 'inc':
        err = validate_inc(parts, p_line + 1)
        return err, TFILE, p_line, 0, _LABELS
    # Custom opcodes
    if not constant:
        if (opcode == 'ld()' or opcode[:2] == 'ld'):
            opcode = 'ld '
        if opcode not in ('org', '/', 'end', 'pin', '='):
            opcodeinfo = get_opcodeinfo(chip, 'S', opcode)
            if opcodeinfo == {'opcode': -1, 'mnemonic': 'N/A'}:
                err = "FATAL: Pass 1:  Invalid mnemonic '" + \
                      opcode + "' at line: " + str(p_line + 1)
            else:
                address = address + opcodeinfo['words']
    TFILE[p_line] = line.strip()
    p_line = p_line + 1
    return err, TFILE, p_line, address, _LABELS


def write_program_to_file(program, filename, memory_location, _LABELS):
    """
    Take the assembled program and write to a given filename.

    Parameters
    ----------
    program: list, mandatory
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
    -----
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
        content = str(hex(location)[2:])
        memorycontent = memorycontent + '"' + content + '", '
    memory_content = memorycontent[:-2] + ']'

    json_doc = "{"
    json_doc = json_doc + program_name + ','
    json_doc = json_doc + compdate + ','
    json_doc = json_doc + m_location + ','
    json_doc = json_doc + memory_content + ','
    json_doc = json_doc + labels
    json_doc = json_doc + '}'
    with open(filename + '.obj', "w") as output:
        output.write(json_doc)
    with open(filename + '.bin', "w+b") as b:
        b.write(bytearray(program))
    return True
