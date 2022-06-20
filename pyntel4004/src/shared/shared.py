
"""Shared operations (between assembly, disassembly and execution."""

import os
import sys

sys.path.insert(1, '..' + os.sep + 'platforms')

# Import i4004 processor
from hardware.processor import Processor  # noqa
from hardware.suboperation import zfl  # noqa
from hardware.suboperations.utility import convert_to_absolute_address  # noqa

# Import exceptions
from hardware.exceptions import InvalidToken  # noqa

# Import typing library
from typing import Any, Tuple  # noqa


def output_core_item(filename: str, item: str) -> None:
    if filename == '':
        print(item, end='')  # Ensure that no newline is printed
    else:
        with open(filename, "a") as output:
            output.write(item)


def output_register(filename: str, chip: Processor,
                    tabs: str, rambank: int, ramchip: int,
                    register: int):
    output_core_item(filename, '\n\nRam Bank: ' + str(rambank) + '\n')
    output_core_item(filename, 'Ram Chip: ' + str(ramchip) + '\n')
    output_core_item(filename, 'Register: ' + str(register) + '\n')
    output_core_item(filename, 'Addr Value\n')

    for address in range(16):
        a = address - chip.PAGE_SIZE  # address realignment
        realaddress = convert_to_absolute_address(chip, rambank,
                                                  ramchip, register, a)
        output_core_item(filename, str(realaddress) + ':' +
                         tabs[:1] + str(chip.RAM[realaddress])
                         + '\n')

    output_core_item(filename, '\n')


def output_ramchip(filename: str, chip: Processor,
                   tabs: str, rambank: int, ramchip: int):
    output_core_item(filename, '\n\nRAM Bank: ' + str(rambank) + '\n')
    output_core_item(filename, 'RAM Chip: ' + str(ramchip) + '\n')
    for r in range(4):
        output_core_item(filename, 'Register: ' +
                         str(r) + '\t')
    output_core_item(filename, '\n')
    for _ in range(4):
        output_core_item(filename, 'Addr Value' + tabs[:1])

    output_core_item(filename, '\n')

    for address in range(16):
        a = address - chip.PAGE_SIZE  # address realignment

        for i in range(4):
            realaddress = \
                convert_to_absolute_address(chip, rambank,
                                            ramchip, (i + 16),
                                            a)
            output_core_item(filename, str(realaddress) + ':' +
                             tabs[:1] + str(chip.RAM[realaddress])
                             + tabs[:1])
        output_core_item(filename, '\n')
    output_core_item(filename, '\n')


def output_memory_bank(filename: str, chip: Processor,
                       tabs: str, rambank: int):
    for ramchip in range(4):
        output_ramchip(filename, chip,
                       tabs, rambank, ramchip)
    output_core_item(filename, '\n')


def output_all_memory(filename: str, chip: Processor,
                      tabs: str):
    for rambank in range(8):
        output_memory_bank(filename, chip,
                           tabs, rambank)
    output_core_item(filename, '\n')


def output_registers(filename: str, chip: Processor,
                     tabs: str) -> None:
    topline = '+-------'
    output_core_item(filename, '\n\nRegisters:\n\n')
    start = 0
    end = (int((chip.NO_REGISTERS/2)))
    r = 0
    for _ in range(0, 2):
        for i in range(start, end):
            output_core_item(filename, topline)
        output_core_item(filename, '+\n')

        for i in range(start, end):
            if r < 10:
                spaces = ' '
            else:
                spaces = ''
            output_core_item(filename, '| R ' + spaces + str(r) + '  ')
            r = r + 1

        output_core_item(filename, '|\n')
        for i in range(start, end):
            output_core_item(filename, topline)
        output_core_item(filename, '+\n')

        for i in range(start, end):
            if i == 1 or i == 8:
                spaces = '  '
            output_core_item(filename, '|' + spaces +
                             str(chip.REGISTERS[i]) + '    ')
        output_core_item(filename, '|\n')
        for i in range(start, end):
            output_core_item(filename, topline)
        output_core_item(filename, '+\n\n')
        start = end
        end = chip.NO_REGISTERS


def output_cpu_status(filename: str, chip: Processor,
                      tabs: str) -> None:
    output_core_item(filename, '\n\nProcessor Status:\n\n')
    output_core_item(filename, 'PIN 10               : ' +
                     str(chip.PIN_10_SIGNAL_TEST) + '\n')
    output_core_item(filename, 'Program Counter      : ' +
                     str(chip.PROGRAM_COUNTER) + '\n')
    stack = ''
    for i in chip.STACK:
        stack = stack + str(chip.STACK[i]) + ', '
    ln = len(stack) - 2
    stack = stack[:ln]
    output_core_item(filename,
                     'Stack/Pointer        : (' + stack + ') / ' +
                     (str(chip.STACK_POINTER)) + '\n')
    output_core_item(filename, 'ACBR                 : ' +
                     str(chip.ACBR) + '\n')
    acc = chip.read_accumulator()
    output_core_item(filename, 'Accumulator          : ' + str(acc) + '\n')
    output_core_item(filename, 'Carry                : ' +
                     str(chip.CARRY) + '\n')
    output_core_item(filename, 'DRAM Bank            : ' +
                     str(chip.CURRENT_DRAM_BANK) + '\n')
    output_core_item(filename, 'RAM Bank             : ' +
                     str(chip.CURRENT_RAM_BANK) + '\n')
    output_core_item(filename, 'WPM Counter          : ' +
                     str(chip.WPM_COUNTER) + '\n')


def output_core_characteristics(filename: str, chip: Processor,
                                tabs: str) -> None:
    output_core_item(filename, 'Processor Characteristics:\n\n')
    output_core_item(filename, 'MAX_4_BITS :           ' +
                     str(chip.MAX_4_BITS) + tabs)
    output_core_item(filename, 'PAGE_SIZE :            ' +
                     str(chip.PAGE_SIZE) + '\n')
    output_core_item(filename, 'STACK_SIZE :           ' +
                     str(chip.STACK_SIZE) + tabs)
    output_core_item(filename, 'MSB :                  ' +
                     str(chip.MSB) + '\n')
    output_core_item(filename, 'MEMORY_SIZE_RAM :      ' +
                     str(chip.MEMORY_SIZE_RAM) + tabs)
    output_core_item(filename, 'NO_REGISTERS :         ' +
                     str(chip.NO_REGISTERS) + '\n')
    output_core_item(filename, 'MEMORY_SIZE_ROM :      ' +
                     str(chip.MEMORY_SIZE_ROM) + tabs)
    output_core_item(filename, 'NO_ROM_PORTS :         ' +
                     str(chip.NO_REGISTERS) + '\n')
    output_core_item(filename, 'MEMORY_SIZE_PRAM :     ' +
                     str(chip. MEMORY_SIZE_PRAM) + tabs)
    output_core_item(filename, 'NO_CHIPS_PER_BANK :    ' +
                     str(chip.NO_CHIPS_PER_BANK) + '\n')
    output_core_item(filename, 'RAM_BANK_SIZE :        ' +
                     str(chip.RAM_BANK_SIZE) + tabs)
    output_core_item(filename, 'RAM_CHIP_SIZE :        ' +
                     str(chip.RAM_CHIP_SIZE) + '\n')
    output_core_item(filename, 'RAM_REGISTER_SIZE :    ' +
                     str(chip.RAM_REGISTER_SIZE) + tabs)
    output_core_item(filename, 'NO_COMMAND_REGISTERS : ' +
                     str(chip.NO_COMMAND_REGISTERS) + '\n')
    output_core_item(filename, 'NO_STATUS_REGISTERS :  ' +
                     str(chip.NO_STATUS_REGISTERS) + tabs)
    output_core_item(filename, 'NO_STATUS_CHARACTERS : ' +
                     str(chip.NO_STATUS_CHARACTERS) + '\n')


def coredump(chip: Processor, filename: str, outputs: str) -> bool:
    """
    Take the memory and write to a given filename.

    Parameters
    ----------
    chip : Processor
        The chip targetted for the 3p

    filename: str, mandatory
        The filename to write to

    outputs: str, mandatory
        List of resuts to display as a string. A core dump is ALWAYS "ALL"

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
    # Import platform-specific code
    from platforms.platforms import get_current_datetime  # noqa

    required = outputs.upper()
    if 'ALL' in required and required != "['ALL']":
        raise InvalidToken("Cannot specify 'ALL' with any others")

    tabs = '\t\t\t'
    errordate = 'Date/Time:' + get_current_datetime() + '\n\n'
    if len(filename) > 0:
        filename = filename + '.core'
        with open(filename, "w") as output:
            output.write('')

    # Heading
    output_core_item(filename, '\n\n' + errordate)

    lreq = required.replace('[', '').split(',')

    for req in lreq:
        # Processor Characteristics
        if 'ALL' in req or 'PC' in req:
            output_core_characteristics(filename, chip, tabs)

        # Processor Status
        if 'ALL' in req or 'PS' in req:
            output_cpu_status(filename, chip, tabs)

        # Registers
        if 'ALL' in req or 'REGS' in req:
            output_registers(filename, chip, tabs)

        # Memory
        if 'ALL' in req or 'ALLMEM' in req:
            output_core_item(filename, '\n')
            output_all_memory(filename, chip, tabs)

        # Indvidual Chip/Memory Bank/Memory Register
        if 'CHIP' in req:
            stripped = (req.replace('CHIP(', '').replace('[', '').
                        replace(']', '').replace(')', '').
                        replace("'", "").split(':'))
            items = len(stripped)
            if items == 1:
                output_memory_bank(filename, chip,
                                   tabs, int(stripped[0]))
            if items == 2:
                output_ramchip(filename, chip,
                               tabs, int(stripped[0]), int(stripped[1]))
            if items == 3:
                output_register(filename, chip,
                                tabs, int(stripped[0]),
                                int(stripped[1]),
                                int(stripped[2]))
    return True


def msg_exec() -> None:
    print()
    print('EXECUTING PROGRAM: ')


def msg_blank() -> None:
    print()


def msg_acc(chip: Processor) -> None:
    acc = chip.read_accumulator()
    print('Accumulator : ' + str(acc) + '  (0b ' +
          str(Processor.decimal_to_binary(4, acc)) + ')')


def msg_carry(chip: Processor) -> None:
    print('Carry       :', chip.read_carry())


def msg_asm() -> None:
    print('Address  Label   Address        Assembled            ' +
          '          Line     Op/Operand')
    print(' (Dec)            (Bin)           (Bin)          (Dec)')
    print('                            Word 1     Word 2')


def msg_prog(param0: str) -> None:
    print()
    print()
    print('Program Code:', param0)


def msg_labels(param0: str) -> None:
    print()
    if len(param0) > 0:
        print('Labels:')
        print('Address   Label')
        for _i in range(len(param0)):  # noqa
            print('{:>5}     {}'.format(param0[_i]['address'], param0[_i]['label']))  # noqa


def print_messages(quiet: bool, msgtype: str, chip: Processor,
                   param0: Any) -> None:
    if not quiet:
        if msgtype == 'EXEC':
            msg_exec()
        if msgtype == 'BLANK':
            msg_blank()
        if msgtype == 'ACC':
            msg_acc(chip)
        if msgtype == 'CARRY':
            msg_carry(chip)
        if msgtype == 'ASM':
            msg_asm()
        if msgtype == 'PROG':
            msg_prog(param0)
        if msgtype == 'LABELS':
            msg_labels(param0)
    return None


def determine_filetype(inputfile: str) -> str:
    """
    Determine the filetype of a specific input file.
    In the context of reloading a previously assembled file for
    execution or disassembly.
    Parameters
    ----------
    inputfile: str, mandatory
        The filename to examine
    Returns
    -------
    filetype: str
        OBJ if an object file complete with metadata
        BIN if a binary assembled file.
    Raises
    ------
    N/A
    Notes
    -----
    N/A
    """
    file = open(inputfile, "rb")
    bites = file.read(12)[2:9]
    if bites == b'program':
        filetype = 'OBJ'
    else:
        filetype = 'BIN'
    return filetype


def do_error(message: str):
    """
    Print an assembly/runtime error message

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
    -----
    N/A

    """
    print()
    print(message)
    return True


def get_opcodeinfo(self: Processor, ls: str, mnemonic: str) -> dict:
    """
    Given a mnemonic retrieve details about the it from the opcode table.

    Parameters
    ----------
    self : Processor, mandatory
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
    -----
    N/A

    """
    if ls.upper() == 'S':
        opcodeinfo = next((item for item in self.INSTRUCTIONS
                          if str(item["mnemonic"][:3]) == mnemonic),
                          {"opcode": -1, "mnemonic": "N/A"})
    else:
        opcodeinfo = next((item for item in self.INSTRUCTIONS
                          if str(item["mnemonic"]) == mnemonic),
                          {"opcode": -1, "mnemonic": "N/A"})
    return opcodeinfo


def get_opcodeinfobyopcode(self: Processor, opcode: int) -> dict:
    """
    Given an opcode, retrieve details about it from the opcode table.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    opcode: int, mandatory
        The opcode to locate

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
    -----
    N/A

    """
    opcodeinfo = next((item for item in self.INSTRUCTIONS
                      if item['opcode'] == opcode),
                      {"opcode": -1, "mnemonic": "N/A"})
    return opcodeinfo


def retrieve_program(chip: Processor, location: str) -> list:
    """
    Retrieve the assembled program from the specified location.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location : str, mandatory
        The location to which the program should be loaded

    Returns
    -------
    loc: list
        The program from the location specified

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if location == 'rom':
        loc = chip.ROM
    if location == 'ram':
        loc = chip.PRAM
    return loc


def custom_opcode_logic(custom_opcode: bool, cop: str, exe: str) \
                        -> Tuple[str, str]:
    op = ''
    if custom_opcode:
        custom_opcode = False
        exe = cop
        op = cop
    else:
        op = exe
    return exe, op


def translate_mnemonic(chip: Processor, _tps: list, exe: str,
                       opcode: str, task: str, words: int, quiet: bool) -> str:
    """
    Formulate the opcodes into mnemonics ready for execution.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    _tps: list, mandatory
        List representing the memory of the i4004 into which the
        newly assembled instructions will be placed.

    exe: str, mandatory
        pre-formatted exe mnemonic ready for processing

    opcode: str, mandatory
        Opcode of the current instruction

    task: str, mandatory
        'D' for Disassembly
        'E' for Execution

    words: int, optional (supply 0)
        The number of words an instruction uses

    quiet: bool, mandatory
        Whether quiet mode is on

    Returns
    -------
    exe: str
        A correctly formed, ready-for execution mnemonic

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    custom_opcode = False
    cop = ''

    # Only mnemonic with 2 characters - fix
    if exe[:3] == 'ld ':
        exe = exe[:2] + exe[3:]

    # Ensure that the correct arguments are passed to the operations
    if exe[:3] == 'fim':
        exe = exe.replace('p', '').replace('data8)', '') +\
            str(_tps[chip.PROGRAM_COUNTER + 1]) + ')'

    if exe[:3] == 'isz':
        # Remove opcode from 1st byte to get register
        first_byte = zfl(str(_tps[chip.PROGRAM_COUNTER] & 15), 4)
        exe = 'isz(' + str(int(first_byte, 2))
        exe = exe + ',' + str(_tps[chip.PROGRAM_COUNTER + 1]) + ')'

    if exe[:4] == 'jcn(':
        custom_opcode = True
        address = _tps[chip.PROGRAM_COUNTER + 1]
        conditions = zfl(str(bin(_tps[chip.PROGRAM_COUNTER])[2:], 8)[4:])
        b10address = str(address)
        cop = exe.replace('address8', b10address)
        exe = exe[:4] + str(int(conditions, 2)) + ',' + b10address + ')'

    if exe[:4] in ('jun(', 'jms('):
        custom_opcode = True
        # Remove opcode from 1st byte
        hvalue = zfl(bin(_tps[chip.PROGRAM_COUNTER] &
                     0xffff0000)[2:], 8)[:4]
        lvalue = zfl(bin(_tps[chip.PROGRAM_COUNTER + 1])[2:], 8)
        whole_value = str(int(hvalue + lvalue, 2))
        cop = exe.replace('address12', whole_value)
        exe = exe[:4] + whole_value + ')'

    if task == 'D':
        if exe[:4] in ('jun(', 'jms(', 'jcn('):
            opcode = str(_tps[chip.PROGRAM_COUNTER]) + ', ' + \
                str(_tps[chip.PROGRAM_COUNTER + 1])

        if exe[:3] == 'end':  # pseudo-opcode (directive "end" - stop program)
            custom_opcode = False
        exe, op = custom_opcode_logic(custom_opcode, cop, exe)
        if quiet is False:
            print('{:4}  {:>8}  {:<10}'.format(chip.PROGRAM_COUNTER, opcode, op.replace('()', '')))  # noqa

        chip.PROGRAM_COUNTER = chip.PROGRAM_COUNTER + words

    if task == 'E':
        exe, op = custom_opcode_logic(custom_opcode, cop, exe)
        if quiet is False:
            print('  {:>7}  {:<10}'.format(opcode, op.replace('()', '')))  # noqa

    return exe
