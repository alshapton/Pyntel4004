"""Assembler supporting functions."""

# Disable pylint's too-many-arguments and too-many-locals warnings,
# since there are functions in this module with large numbers of
# arguments, and large numbers of local variables.

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

from typing import Tuple, Any
from hardware.processor import Processor
from hardware.suboperations.utility import split_address8
from shared.shared import do_error, get_opcodeinfo, get_opcodeinfobyopcode  # noqa


def asm_comment(label: str, count: int, line: str) -> None:
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


def assemble_1(opcodeinfo: dict, label: str, tps: list,
               address: int, count: int) -> Tuple[list, str]:
    """
    Output the assembled operator (no operand(s)).

    Parameters
    ----------
    opcodeinfo: str, mandatory
        JSON string containing the information about the opcode

    label: str, mandatory
        Any label on this line

    tps: list, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    count: int, mandatory
        Current assembly program line

    Returns
    -------
    tps: list
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
    tps[address] = opcodeinfo['opcode']
    print_ln(address, label, address_left,
             address_right, bit1, bit2, '', '',
             tps[address], '', '', str(count),
             opcodeinfo['mnemonic'].replace('(', '').replace(')', ''),
             '', '', '', '')
    address = address + opcodeinfo['words']
    return tps, address


def assemble_3(chip: Processor, x: list, _labels: list, tps: list,
               address: int, address_left: str, address_right: str,
               label: str, count: int) -> Tuple[int, list, list]:
    """
    Assemble code with 3 components.

    Parameters
    ----------
    chip: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        Line of program code (split into component parts).

    _labels: list, mandatory
        List for containing labels

    tps: list, mandatory
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

    tps: list, mandatory
        Assembled code

    _labels: list, Mandatory
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
        address, tps, _labels = assemble_jcn(chip, x, _labels, tps,
                                             address, address_left,
                                             address_right, label,
                                             count)
    if x[0][:3] == 'fim':
        address, tps, _labels = assemble_fim(chip, x, _labels, tps,
                                             address, label, count)
    if x[0] == 'isz':
        address, tps, _labels = assemble_isz(chip, x, x[1], _labels, tps,
                                             address, address_left,
                                             address_right, label, count)
    if x[0] not in ('jcn', 'fim', 'isz'):
        tps, address = asm_others(chip, x, count, x[0], tps, address, label)

    return address, tps, _labels


def asm_label(tps: list, address: int, x: list,
              count: int, label: str) -> list:
    """
    Output the assembled label.

    Parameters
    ----------
    tps: list, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    x: list, mandatory
        Line of program code (split into component parts).

    count: int, mandatory
        Current assembly program line

    label: str, mandatory
        Any label on this line

    Returns
    -------
    tps: List, mandatory
        Assembled code

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    tps[address] = int(x[1])
    print_ln('', '',  '', '', '', '', '', '', '', '', '',
             str(count), label, str(x[1]), '', '', '',)
    return tps


def asm_end(tps: list, address: int, count: int, label: str) -> list:
    """
    Output the assembled "end" pseudo-opcode.

    Parameters
    ----------
    tps: list, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    count: int, mandatory
        Current assembly program line

    label: str, mandatory
        Any label on this line

    Returns
    -------
    tps: List
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
    tps[address] = 255
    return tps


def asm_org(label: str, count: int, x: list,
            opcode: str) -> Tuple[bool, str, int]:
    """
    Output the assembled "org" pseudo-opcode.

    Parameters
    ----------
    label: str, mandatory
        Any label on this line

    count: int, mandatory
        Current assembly program line

    x: list, mandatory
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


def asm_others(chip: Processor, x: list, count: int, opcode: str,
               tps: list, address: int, label: str) -> Tuple[list, int]:
    """
    Assemble othe instructions.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        Line of program code (split into component parts).

    count: int, mandatory
        Current assembly program line

    opcode: int, mandatory
       Value of the opcode for assembly

    tps: list, mandatory
        Assembled code

    address: int, mandatory
        address to assemble to

    label: str, mandatory
        Label of the current line (if any)

    Returns
    -------
    tps: list
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
    tps[address] = opcodeinfo['opcode']
    tps[address+1] = int(x[2])
    print_ln(address, label, address_left, address_right, bit1, bit2,
             val_left, val_right, str(tps[address]) + "," +
             str(tps[address + 1]), '', '', str(count), opcode, str(x[1]),
             str(x[2]), '', '')
    address = address + opcodeinfo['words']
    return tps, address


def asm_pin(chip: Processor, value: int, label: str, count: int) -> Any:
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


def asm_pseudo(chip: Processor, opcode: int, label: str, count: int,
               x: list, tps: list, address: int, org_found: bool,
               location: str) -> Tuple[Any, bool, list, str, int]:
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

    x: list, mandatory
        Line of program code (split into component parts).

    tps: list, mandatory
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

    tps: list
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
        tps = asm_end(tps, address, count, label)
        err = False
    if opcode == 'pin':
        err = False
        err = asm_pin(chip, x[1], label, count)
    if opcode == '=':
        org_found, _unused1, _unused2 = asm_org(x[0], count, x, '=')
        err = False
    return err, org_found, tps, location, address


def asm_main(chip: Processor, x: list, _labels: list, address: int, tps: list,
             opcode: str, opcodeinfo: dict,
             label: str, count: int, org_found: bool, location: str) \
    -> Tuple[Processor, list, list, int, list,
             dict, str, int, Any, bool, str]:
    """
    Assemble the program (opcode components).

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _labels: list, mandatory
        List for containing labels

    address: int
        the address to assemble to

    tps: list, mandatory
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
    chip: Processor
        Instance of a processor to place the assembled code in.

    x: list
        The current line of code being assembled split into individual elements

    _labels: list
        List for containing labels

    address: int
        the address to assemble to

    tps: list
        Assembled code

    opcodeinfo: dict
        JSON string containing an opcode's information

    label: str
        If there is a label associated with this instruction, it will be here,
        "" otherwise.

    count: int
        Assembly line number (used for printing during assembly)

    err: Bool/Text depending on whether an error is raised,

    org_found: bool
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
            err, org_found, tps, location, address = \
                asm_pseudo(chip, opcode, label, count, x, tps,
                           address, org_found, location)
            if err:
                do_error(err)
                return False
        else:
            if org_found is True:
                chip, x, _labels, address, tps, opcodeinfo, label, \
                    count = assemble_opcodes(chip, x, _labels,
                                             address, tps, opcodeinfo,
                                             label, count)
            else:
                err = "FATAL: Pass 2: No 'org'" + \
                    " found at line: " + str(count + 1)
    else:
        err = "'FATAL: Pass 2:  Invalid mnemonic '" + \
            opcode + "' at line: " + str(count + 1)

    return chip, x, _labels, address, tps, opcodeinfo, label, count, err, \
        org_found, location


def assemble_opcodes(chip: Processor, x: list, _labels: list, address: int,
                     tps: list, opcodeinfo: dict, label: str, count: int) \
    -> Tuple[Processor, list, list,
             int, list, dict, str, int]:
    """
    Assemble the opcodes.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _labels: List, mandatory
        List for containing labels

    address: int
        the address to assemble to

    tps: List, mandatory
        Assembled code

    opcodeinfo: dict, mandatory
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

    _labels: list
        List for containing labels

    address: int
        the address to assemble to

    tps: list
        Assembled code

    opcodeinfo: dict, mandatory
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
        match_label(_labels, label, address)
        for _i in range(len([x])-1):
            x[_i] = x[_i + 1]
        x.pop(len([x])-1)
    opcode = x[0]

    address_left, address_right = split_address8(
        address)
    # Check for operand(s)
    if len(x) == 1:
        # Only operator, no operand
        tps, address = assemble_1(opcodeinfo, label, tps, address, count)  # noqa
    if len(x) == 2:
        # Operator & operand (generic)
        address, tps, _labels = assemble_2(chip, x, opcode, address, tps,
                                           _labels, address_left,
                                           address_right, label, count)
    if len(x) == 3:
        # Operator and 2 operands
        address, tps, _labels = assemble_3(chip, x, _labels, tps,
                                           address, address_left,
                                           address_right, label, count)
    return chip, x, _labels, address, tps, opcodeinfo, label, count


def pass1(chip: Processor, program_name: str, _labels: list,
          tps: list, tfile: list) -> Tuple[Any, list, list, list, int]:
    """
    Pass 1 of the two-pass assembly process.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    program_name: str, mandatory
        Name of the assembly language program file.

    _labels: list, Mandatory
        List for containing labels

    tps: list, mandatory
        Assembled code

    tfile: list, mandatory
        Assembly language store


    Returns
    -------
    err:
        False if no error, error text if error

    _labels: list
        List for containing labels

    tfile: list
        Assembly language store

    tps: list
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
    err = False
    p_line = 0
    address = 0

    try:
        program = open(program_name, 'r',  encoding='utf-8')  # noqa
    except IOError:
        err = ('FATAL: Pass 1: File "' + program_name +
               '" does not exist.')
        return err,  _labels, tps, tfile, address
    else:
        print()
        print()
        print('Program Code:', program_name)
        print()

        while True:
            line = program.readline()
            # if line is empty, end of file is reached
            if (not line) or (line == '') or len(line) == 0:
                # Completed reading program into memory
                break
            err, tfile, p_line, address, _labels = \
                work_with_a_line_of_asm(chip, line, _labels,
                                        p_line, address, tfile)
            if err:
                break
        # Completed reading program into memory (or errored-out)
        program.close()
        return err,  _labels, tps, tfile, address


def wrap_up(chip: Processor, location: str, tps: list, _labels: list,
            object_file: str) -> Processor:
    """
    Pass 1 of the two-pass assembly process.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location: str, mandatory
        either 'ram' or 'rom'

    tps: list, mandatory
        Assembled code

    _labels: list, mandatory
        List for containing labels

    object_file: str, mandatory
        The filename to write to

    Returns
    -------
    chip : Processor
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
        chip.ROM = tps

    if location == 'ram':
        chip.PRAM = tps

    print()
    print('Labels:')
    print('Address   Label')
    for _i in range(len(_labels)):  # noqa
        print('{:>5}     {}'.format(_labels[_i]['address'], _labels[_i]['label']))  # noqa
    write_program_to_file(tps, object_file, location, _labels)
    return chip


def add_label(_lbls, label: str):
    """
    Add a label to the label table (if it does not exist already).

    Parameters
    ----------
    _lbls : list, mandatory
        A list of the existing labels

    label: str, mandatory
        A candidate new label

    Returns
    -------
    -1          if the label already existed and was not added
    _lbls : list
                the list of labels with the new label appended

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    try:
        label_exists = next((item for item in _lbls
                            if str(item["label"]) == label), None)
    except:  # noqa
        pass
    if not label_exists:
        _lbls.append({'label': label, 'address': -1})
    else:
        return -1
    return _lbls


def decode_conditions(conditions: str) -> int:
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


def get_bits(opcodeinfo: dict) -> Tuple[str, str]:
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


def match_label(_lbls: list, label: str, address: int) -> list:
    """
    Given a label and an address, add it (if required) to the list of labels.

    Parameters
    ----------
    _lbls: list, mandatory
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
    for _i in range(len(_lbls)):  # noqa
        if _lbls[_i]['label'] == label:
            _lbls[_i]['address'] = address
    return _lbls


def get_label_addr(_lbls: list, label: str) -> int:
    """
    Given a label, get the address for that label.

    Parameters
    ----------
    _lbls : list, mandatory
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
    for _i in _lbls:
        if _i['label'] == label + ',':
            label_address = _i['address']
    return label_address


def assemble_isz(chip: Processor, x: list, register: int, _lbls: list,
                 tps: list, address: int, a_l: str, a_r: str,
                 label: str, count: int) -> Tuple[int, list, list]:
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

    _lbls: list, mandatory
        List of valid labels

    tps: list, mandatory
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

    tps: list
        List representing the memory of the i4004 into which the newly
        assembled instruction has just been placed.

    _lbls: list
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
    label_address = get_label_addr(_lbls, x[2])
    vl, vr = split_address8(int(label_address))
    tps[address] = n_opcode
    tps[address + 1] = label_address
    print_ln(address, label, a_l,
             a_r, bit1, bit2, vl,
             vr, str(tps[address]) +
             "," + str(tps[address + 1]), '',
             '', str(count), x[0], str(x[1]),
             str(x[2]), '', '')
    address = address + opcodeinfo['words']
    return address, tps, _lbls


def assemble_fim(self: Processor, x: list, _labels: list,
                 tps: list, address: int, label: str,
                 count: int) -> Tuple[int, list, list]:
    """
    Function to assemble FIM instruction.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _labels: list, mandatory
        List of valid labels

    tps: list, mandatory
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

    tps: list
        List representing the memory of the i4004 into which the newly
        assembled instruction has just been placed.

    _labels: list
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
    tps[address] = opcodeinfo['opcode']
    tps[address + 1] = int(x[2])
    bit1, bit2 = get_bits(opcodeinfo)
    print_ln(address, label, '' '', '', bit1, bit2, '', '',
             str(tps[address]) + "," + str(tps[address + 1]),
             str(count), x[0], str(x[1]),
             str(x[2]), '', '', '', '')
    address = address + opcodeinfo['words']
    return address, tps, _labels


def assemble_jcn(self: Processor, x: list, _labels: list,
                 tps: list, address: int, address_left: str,
                 address_right: str, label: str,
                 count: int) -> Tuple[int, list, list]:
    """
    Function to assemble JCN instructions.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    x: list, mandatory
        The current line of code being assembled split into individual elements

    _labels: list, mandatory
        List of valid labels

    tps: list, mandatory
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

    tps: list
        List representing the memory of the i4004 into which the newly
        assembled instruction has just been placed.

    _labels: list
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
    label_addr = int(get_label_addr(_labels, dest_label))
    vl, vr = split_address8(label_addr)
    bit1, bit2 = get_bits(opcodeinfo)
    tps[address] = opcodeinfo['opcode']
    tps[address + 1] = label_addr
    print_ln(address, label, address_left, address_right, bit1, bit2,
             vl, vr, str(tps[address]) + "," + str(tps[address + 1]),
             '', '', str(count), x[0], str(x[1]), str(x[2]), '', '')
    address = address + opcodeinfo['words']
    return address, tps, _labels


def assemble_2(chip: Processor, x: list, opcode: str, address: int,
               tps: list, _labels: list, address_left: str,
               address_right: str, label: str, count: int) \
        -> Tuple[int, list, list]:
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

    tps: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    _labels: list, mandatory
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

    tps: list
        List representing the memory of the i4004 into which the newly
        assembled instruction has just been placed.

    _labels: list
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
    addx = get_label_addr(_labels, x[1])
    if addx == -1:
        addx = x[1]
    f_opcode = opcode + '(' + str(addx) + ')'

    if opcode in ('jun', 'jms'):
        # Special case for JUN and JMS
        if opcode == 'jun':
            decimal_code = 64
        if opcode == 'jms':
            decimal_code = 80
        f_opcode = opcode + '(address12)'
        opcodeinfo = get_opcodeinfo(chip, 'L', f_opcode)
        label_addr = get_label_addr(_labels, x[1])
        label_addr12 = str(bin(decimal_code)[2:].zfill(8)[:4]) + \
            str(bin(label_addr)[2:].zfill(12))
        bit1 = label_addr12[:8]
        bit2 = label_addr12[8:]
        tps[address] = int(str(bit1), 2)
        tps[address+1] = int(str(bit2), 2)
        print_ln(address, label, address_left, address_right, bit1[:4],
                 bit1[4:], bit2[:4], bit2[4:], str(tps[address]) + ',' +
                 str(tps[address + 1]), '', '', str(count), opcode, str(x[1]),
                 '', '', '')
        address = address + opcodeinfo['words']
    else:
        if opcode == 'src':
            register = x[1].lower().replace('p', '').replace('r', '')
            f_opcode = 'src(' + register + ')'
        opcodeinfo = get_opcodeinfo(chip, 'L', f_opcode)
        bit1, bit2 = get_bits(opcodeinfo)
        tps[address] = opcodeinfo['opcode']
        print_ln(address, label, address_left, address_right, bit1,
                 bit2, '', '', tps[address], '', '', str(count), opcode,
                 str(x[1]), '', '', '')
        address = address + opcodeinfo['words']
    return address, tps, _labels


def pass0(chip: Processor) -> Tuple[list, int, list, list]:
    """
    Initialise storage for assembly.

    Parameters
    ----------
    chip: Processor, mandatory
        Instance of a processor to place the assembled code in.

    Returns
    -------
    _labels: list
        List for containing labels

    tps_size: int
        Maximum size of program memory

    tps: list
        Program store

    tps_file: list
        Assembly language store

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    # Reset label table for this program
    _lbls = []

    # Maximum size of program memory
    tps_size = max([chip.MEMORY_SIZE_ROM,
                    chip.MEMORY_SIZE_PRAM,
                    chip.MEMORY_SIZE_RAM])

    # Reset temporary_program_store
    tps = []
    for _i in range(tps_size):
        tps.append(0)

    # Initialise assembly language line store to
    # twice the size of the potential program size.
    tfile = []
    for _i in range(tps_size * 2):
        tfile.append('')

    return _lbls, tps, tfile


def print_ln(f0: str, f1: str, f2: str, f3: str, f4: str, f5: str, f6: str,
             f7: str, f8: str, f9: str, f10: str, f11: str, f12: str,
             f13: str, f14: str, f15: str, f16: str) -> None:
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


def validate_inc(parts: list, line: str) -> bool:
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


def work_with_a_line_of_asm(chip: Processor, line: str,
                            _labels: list, p_line: int,
                            address: int, tfile: list) \
        -> Tuple[Any, list, int, int, list]:
    """
    Analyse a single line of code.

    Parameters
    ----------
    chip: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    line: str, mandatory
        line of assembly code read in from a file

    _labels: list, Mandatory
        List for containing labels

    p_line: int, mandatory
        numbered line of assembly language program

    address: int, Mandatory
        Current address of memory for assembly

    tfile: list, Mandatory
        Assembly language store

    Returns
    -------
    err:
        False if no error, error text if error

    tfile: list
        Assembly language store

    p_line: int
        numbered line of assembly language program

    address: int
        Current address of memory for assembly

    _labels: list
        List for containing labels

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    print(line)
    constant = False
    err = False
    # Work with a line of assembly code
    parts = line.split()
    if parts[0][len(parts[0])-1] == ',':
        # Found a label, now add it to the label table
        print(_labels, '    ', parts[0], '   ', address)
        if add_label(_labels, parts[0]) == -1:
            err = ('FATAL: Pass 1: Duplicate label: ' + parts[0] +
                   ' at line ' + str(p_line + 1))
            return err, tfile, p_line, 0, _labels
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

        match_label(_labels, parts[0], label_content)
        # Set opcode
        opcode = parts[1][:3]
        opcodeinfo = get_opcodeinfo(chip, 'S', opcode)
        address = address + opcodeinfo['words']
    else:
        # Set opcode
        opcode = parts[0][:3]
    if opcode[:3] == 'inc':
        err = validate_inc(parts, p_line + 1)
        return err, tfile, p_line, 0, _labels
    # Custom opcodes
    if parts[0][len(parts[0])-1] != ',':
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
    tfile[p_line] = line.strip()
    p_line = p_line + 1
    return err, tfile, p_line, address, _labels


def write_program_to_file(program, filename, memory_location, _labels) -> bool:
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

    _labels: list, mandatory
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
    from datetime import datetime  # noqa
    program_name = '"program":"' + filename + '"'
    m_location = '"location":"' + memory_location + '"'
    compdate = '"compile_date":"' + \
               datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '"'
    labels = '"labels":' + str(_labels).replace("'", '"')
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
    with open(filename + '.obj', "w", encoding='utf-8') as output:
        output.write(json_doc)
    with open(filename + '.bin', "w+b") as b:
        b.write(bytearray(program))
    return True
