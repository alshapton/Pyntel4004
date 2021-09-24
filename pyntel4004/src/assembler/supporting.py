from hardware.processor import processor


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
