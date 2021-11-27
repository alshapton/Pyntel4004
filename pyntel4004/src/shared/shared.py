"""Shared operations (between assembly, disassembly and execution."""


def determine_filetype(inputfile):
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
    bytes = file.read(12)[2:9]
    if bytes == b'program':
        filetype = 'OBJ'
    else:
        filetype = 'BIN'
    return filetype


def coredump(chip, filename):
    """
    Take the memory and write to a given filename.

    Parameters
    ----------
    chip : Processor
        The chip targetted for the coredump

    filename: str, mandatory
        The filename to write to

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
    filename = datetime.now().strftime("%d/%m/%Y-%H:%M:%S") + '.core'
    errordate = 'Date/Time:' + \
        datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n\n'
    with open(filename, "w", encoding='utf-8') as output:
        output.write('\n\n' + errordate)
        output.write('Processor Characteristics:\n\n')
        output.write('MAX_4_BITS :           ' + str(chip.MAX_4_BITS) +
                     '\t\t\t')
        output.write('PAGE_SIZE :            ' + str(chip.PAGE_SIZE) + '\n')
        output.write('STACK_SIZE :           ' + str(chip.STACK_SIZE) +
                     '\t\t\t')
        output.write('MSB :                  ' + str(chip.MSB) + '\n')

        output.write('MEMORY_SIZE_RAM :      ' + str(chip.MEMORY_SIZE_RAM) +
                     '\t\t\t')
        output.write('NO_REGISTERS :         ' + str(chip.NO_REGISTERS) + '\n')
        output.write('MEMORY_SIZE_ROM :      ' + str(chip.MEMORY_SIZE_ROM) +
                     '\t\t\t')
        output.write('NO_ROM_PORTS :         ' + str(chip.NO_REGISTERS) + '\n')
        output.write('MEMORY_SIZE_PRAM :     ' +
                     str(chip. MEMORY_SIZE_PRAM) + '\t\t\t')
        output.write('NO_CHIPS_PER_BANK :    ' +
                     str(chip.NO_CHIPS_PER_BANK) + '\n')
        output.write('RAM_BANK_SIZE :        ' + str(chip.RAM_BANK_SIZE) +
                     '\t\t\t')
        output.write('RAM_CHIP_SIZE :        ' + str(chip.RAM_CHIP_SIZE) +
                     '\n')
        output.write('RAM_REGISTER_SIZE :    ' +
                     str(chip.RAM_REGISTER_SIZE) + '\t\t\t')
        output.write('NO_COMMAND_REGISTERS : ' +
                     str(chip.NO_COMMAND_REGISTERS) + '\n')
        output.write('NO_STATUS_REGISTERS :  ' +
                     str(chip.NO_STATUS_REGISTERS) + '\t\t\t')
        output.write('NO_STATUS_CHARACTERS : ' +
                     str(chip.NO_STATUS_CHARACTERS) + '\n')
        output.write('\n\nProcessor Status:\n\n')
        output.write('PIN 10               : ' + str(chip.PIN_10_SIGNAL_TEST)
                     + '\n')
        output.write('Program Counter      : ' + str(chip.PROGRAM_COUNTER) +
                     '\n')
        stack = ''
        for i in chip.STACK:
            stack = stack + str(chip.STACK[i]) + ', '
        ln = len(stack)-2
        stack = stack[:ln]
        output.write('Stack/Pointer        : (' + stack + ') / ' +
                     (str(chip.STACK_POINTER)) + '\n')
        output.write('ACBR                 : ' + str(chip.ACBR) + '\n')
        output.write('Carry                : ' + str(chip.CARRY) + '\n')
        output.write('DRAM Bank            : ' + str(chip.CURRENT_DRAM_BANK) +
                     '\n')
        output.write('RAM Bank             : ' + str(chip.CURRENT_RAM_BANK) +
                     '\n')
        output.write('WPM Counter          : ' + str(chip.WPM_COUNTER) + '\n')
        output.write('\n\nRegisters:\n\n')
        r = 0
        for i in chip.REGISTERS:
            if r < 10:
                spaces = ' '
            else:
                spaces = ''
            output.write('[' + spaces + str(r) + ']\t')
            r = r + 1
        output.write('\n')
        spaces = '  '
        for i in chip.REGISTERS:
            output.write(spaces + str(i) + '\t\t')

        print('Core dump to: ' + filename)
        return True


def do_error(message: str):
    """
    Print an assembly/runtime error message.

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


def get_opcodeinfo(self, ls: str, mnemonic: str):
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
    opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    if ls.upper() == 'S':
        try:
            opcodeinfo = next((item for item in self.INSTRUCTIONS
                               if str(item["mnemonic"][:3]) == mnemonic),
                              {"opcode": -1, "mnemonic": "N/A"})
        except:  # noqa
            opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
        return opcodeinfo
    try:
        opcodeinfo = next((item for item in self.INSTRUCTIONS
                           if str(item["mnemonic"]) == mnemonic),
                          {"opcode": -1, "mnemonic": "N/A"})
    except:  # noqa
        opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    return opcodeinfo


def get_opcodeinfobyopcode(self, opcode: int):
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
    opcodeinfo = {"opcode": -1, "mnemonic": "-"}
    try:
        opcodeinfo = next((item for item in self.INSTRUCTIONS
                           if item['opcode'] == opcode),
                          {"opcode": -1, "mnemonic": "N/A"})
    except:  # noqa
        opcodeinfo = {"opcode": -1, "mnemonic": "-"}
    return opcodeinfo
