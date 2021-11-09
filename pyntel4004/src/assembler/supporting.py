from hardware.processor import Processor
from hardware.suboperation import split_address8
from shared.shared import do_error, get_opcodeinfo, \
     get_opcodeinfobyopcode


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
    ------
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
    ------
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
    ------
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
    ------
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
    ------
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
