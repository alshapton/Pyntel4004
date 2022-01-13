"""Construct opcode table for documentation."""

# Disable pylint's too-many-locals warnings,
# since there are large numbers of local variables.

# pylint: disable=too-many-locals

# Import system libraries

# Import system modules
import os
import sys
from typing import Any

sys.path.insert(1, '..' + os.sep + '..' + os.sep +
                'pyntel4004' + os.sep + 'src')

# Import i4004 processor
from hardware.processor import Processor  # noqa


def caps(line):
    """
    Capitalize a line of text

    Parameters
    ----------
    line: str, mandatory
        Line of text

    Returns
    -------
    str:    Capitalized line of text

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    return ' '.join(s[:1].upper() + s[1:] for s in line.split(' '))


def write_title(f: Any, label: str) -> None:
    """
    Write a title to a page (with label)

    Parameters
    ----------
    f   :  Any , mandatory
        The file handle to the open file

    title: str, mandatory
        Name of the calling function

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
    f.write('.. _' + label + ':\n')
    title = caps(label.replace('_', ' '))
    underline = ''
    underline = underline.ljust(len(title), '=')
    f.write('\n' + title + '\n' + underline + '\n')


def powers_of_two(directory: str) -> None:
    """
    Create the page for the powers of two.

    Parameters
    ----------
    directory: str, mandatory
        String containing the target directory for the file.

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

    doc_name = sys._getframe().f_code.co_name
    filename = directory + '/' + doc_name + doc_suffix
    with open(filename, "w") as f:
        write_title(f, doc_name)
        f.write('\n\n.. include:: ../../global.rst\n\n')

        f.write('.. list-table::\n')
        f.write('   :header-rows: 1\n\n')

        f.write('   * - 2 :superscript:`n`\n')
        f.write('     - n\n')
        f.write('     - 2 :superscript:`-n`\n')

        for i in range(64):

            # Positive powers
            pos_num = (2 ** i)
            pfmt = "{0:>20}"
            pos_output = pfmt.format(pos_num)
            pos = str([pos_output[max(i-3, 0):i]
                      for i in range(len(pos_output), 0, -3)][::-1]).\
                replace('[', '').replace(']', '').replace(',', '').\
                replace("'", "")

            # Negative powers
            nfmt = "{:." + str(i) + "f}"
            neg_num = (2 ** -i)
            prefix = '0.'
            if i == 0:
                prefix = '1.0'
            neg_output = nfmt.format(neg_num)[2:]
            neg = prefix + str([neg_output[i:i+3]
                                for i in range(0, len(neg_output), 3)]).\
                replace('[', '').replace(']', '').replace(',', '').\
                replace("'", "")
            f.write('   * - ' + pos + '\n')
            f.write('     - ' + str(i) + '\n')
            f.write('     - ' + neg + '\n')
    f.close()


def powers_of_sixteen(directory: str) -> None:
    """
    Create the page for the powers of 16.

    Parameters
    ----------
    directory: str, mandatory
        String containing the target directory for the file.

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

    doc_name = sys._getframe().f_code.co_name
    filename = directory + '/' + doc_name + doc_suffix
    powers = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 0]

    with open(filename, "w") as f:
        write_title(f, doc_name)
        f.write('\n\n.. include:: ../../global.rst\n\n')

        f.write('.. list-table::\n')
        f.write('   :header-rows: 1\n')
        f.write('   :widths: 20,10,70\n\n')

        f.write('   * - 16 :superscript:`n`\n')
        f.write('     - n\n')
        f.write('     - 16 :superscript:`-n`\n')

        for i in range(16):

            # Positive powers
            pos_num = (16 ** i)
            pfmt = "{0:>20}"
            pos_output = pfmt.format(pos_num)
            pos = str([pos_output[max(i-3, 0):i]
                      for i in range(len(pos_output), 0, -3)][::-1]).\
                replace('[', '').replace(']', '').replace(',', '').\
                replace("'", "")

            # Negative powers
            nfmt = "{:.63f}"
            neg_num = (16 ** -i) * (10 ** powers[i])
            neg_interim = nfmt.format(neg_num)
            neg_output = neg_interim
            neg = str([neg_output[i:i+5]
                      for i in range(0, len(neg_output), 5)]).\
                replace('[', '').replace(']', '').replace(',', '').\
                replace("'", "")
            neg = neg[:23] + ' x 10 :superscript:`' + \
                str(powers[i] * -1) + '`'
            f.write('   * - ' + pos + '\n')
            f.write('     - ' + str(i) + '\n')
            f.write('     - ' + neg + '\n')
    f.close()


def powers_of_10(directory: str) -> None:
    """
    Create the page for the powers of 10 in hex.

    Parameters
    ----------
    directory: str, mandatory
        String containing the target directory for the file.

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

    doc_name = sys._getframe().f_code.co_name
    filename = directory + '/' + doc_name + doc_suffix

    with open(filename, "w") as f:
        f.write('.. _' + doc_name + ':\n')
        title = caps(doc_name.replace('_', ' ') + ' :subscript:`16`')
        underline = ''
        underline = underline.ljust(len(doc_name)+16, '=')
        f.write('\n' + title + '\n' + underline + '\n')

        f.write('\n\n.. include:: ../../global.rst\n\n')

        f.write('.. list-table::\n')
        f.write('   :header-rows: 1\n')
        f.write('   :widths: 20,10,70\n\n')

        f.write('   * - 10 :superscript:`n`\n')
        f.write('     - n\n')
        f.write('     - 10 :superscript:`-n`\n')

        for i in range(20):

            # Positive powers
            pos_num = int((10 ** i))
            pos_output = hex(pos_num).replace("0x", '').upper()
            pos = str([pos_output[max(i-4, 0):i]
                      for i in range(len(pos_output), 0, -4)][::-1]).\
                replace('[', '').replace(']', '').replace(',', '').\
                replace("'", "")

            # Negative powers
            neg = ['1.0000 0000 0000 0000',
                   '0.1999 9999 9999 999A',
                   '0.28F5 C285 5C28 F5C3 x 16 :superscript:`-1`',
                   '0.4189 374B C6A7 EF9E x 16 :superscript:`-2`',
                   '0.68DB 8BAC 710c b296 x 16 :superscript:`-3`',
                   '0.A7C5 AC47 1B47 8423 x 16 :superscript:`-4`',
                   '0.10C6 F7A0 B5ED 9D37 x 16 :superscript:`-4`',
                   '0.1A07 F29A BCAF 4858 x 16 :superscript:`-5`',
                   '0.2AF3 1DC4 6118 73BF x 16 :superscript:`-6`',
                   '0.44B8 2FA0 9B5A 52CC x 16 :superscript:`-7`',
                   '0.6DF3 7F67 5EF6 EADF x 16 :superscript:`-8`',
                   '0.AFEB FF0B CB24 AAFF x 16 :superscript:`-9`',
                   '0.1197 9981 2DEA 1119 x 16 :superscript:`-9`',
                   '0.1C25 C268 4976 81C2 x 16 :superscript:`-10`',
                   '0.2D09 370D 4257 3604 x 16 :superscript:`-11`',
                   '0.480E BE7B 9D58 566D x 16 :superscript:`-12`',
                   '0.734A CASF 6226 F0AE x 16 :superscript:`-13`',
                   '0.B877 AA32 36A4 B449 x 16 :superscript:`-14`',
                   '0.1272 5DD1 D243 ABA1 x 16 :superscript:`-14`',
                   '0.1D83 C94F B6D2 AC35 x 16 :superscript:`-15`'
                   ]
            f.write('   * - ' + pos + '\n')
            f.write('     - ' + str(i) + '\n')
            f.write('     - ' + neg[i] + '\n')

    f.close()


def instruction_machine_codes(chip, directory: str) -> None:
    """
    Create the page for the machine code/opcode list

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    directory: str, mandatory
        String containing the target directory for the file.

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
    doc_name = sys._getframe().f_code.co_name
    filename = directory + '/' + doc_name + doc_suffix

    with open(filename, "w") as f:
        write_title(f, doc_name)
        f.write('\n\n.. include:: ../../global.rst')
        f.write('\nIn order to help the programmer examine memory ')
        f.write('when debugging programs, this list provides the assembly ')
        f.write('language instruction represented by each of the 256 ')
        f.write('possible instruction code bytes.\n')
        f.write('Where an instruction occupies two bytes, only the first ')
        f.write('(code) byte is given.')
        f.write('\n')
        f.write('\n')

        f.write('.. list-table:: Instruction Machine Codes\n')
        f.write('   :header-rows: 1\n\n')

        f.write('   * - Decimal\n')
        f.write('     - Octal\n')
        f.write('     - Hex\n')
        f.write('     - Mnemonic\n')
        f.write('     - Parameter\n')
        f.write('     - Comment\n')

        # Cycle through the instructions
        for i in chip.INSTRUCTIONS:
            opcode = i['opcode']
            comment = ''
            parameter = ''
            custom = False
            mnemonic = i['mnemonic'].replace('()', '').replace(',data8', '').replace(',address8', '').replace('address12)', '').upper()  # noqa
            m = mnemonic[:3]
            m2 = ''
            if mnemonic == '-':
                m = '---'
                custom = True
            if mnemonic[:3] == 'JMS' or mnemonic[:3] == 'JUN':
                comment = '|psi|'
                m2 = mnemonic[:3]
                custom = True
            if mnemonic[:3] == 'JCN':
                parameter = mnemonic.split('(')[1].replace(')', '')
                comment = 'CN=' + parameter
                m2 = mnemonic[:3]
                custom = True
            if mnemonic[:3] in ('WR0', 'WR1', 'WR2', 'WR3',
                                'RD0', 'RD1', 'RD2', 'RD3'):
                m2 = mnemonic[:2] + 'n'
                custom = True
            if mnemonic[:3] == 'LD ':
                m2 = 'ld'
                custom = True
            if custom is False:
                parameter = mnemonic.replace(')', '').replace('(', '').replace(mnemonic[:3], '')  # noqa
                m2 = m
            if opcode != 256:
                f.write('   * - ' + str(opcode) + '\n')
                f.write('     - ' + str(oct(opcode))[2:] + '\n')
                f.write('     - ' + hex(opcode)[2:].upper() + '\n')
                if m == '---':
                    f.write('     - Not Used \n')
                else:
                    f.write('     - ' + ':ref:`' + m.upper() +
                            ' <hardware-machine-' + m2.lower() + '>`\n')
                f.write('     - ' + parameter + '\n')
                f.write('     - ' + comment + '\n')
        f.write('\n|br|')
        f.write('\n\n |psi| Second hexadecimal ' +
                'digit is part of the jump address.')
        f.write('\n\n')
        f.close()


def hexadecimal_arithmetic(directory: str) -> None:
    """
    Create the page for with the two tables for hex arithmetic.
    Parameters
    ----------
    directory: str, mandatory
        String containing the target directory for the file.

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

    doc_name = sys._getframe().f_code.co_name
    filename = directory + '/' + doc_name + doc_suffix

    with open(filename, "w") as f:
        write_title(f, doc_name)
        f.write('\n\n.. include:: ../../global.rst')
        f.write('\n\n')

        f.write('.. list-table:: Hexadecimal Addition\n')
        f.write('   :header-rows: 1\n\n')

        f.write('   * - 0\n')
        for i in range(1, 15):
            f.write('     - ' + hex(i)[2:].upper() + '\n')
        f.write('     - F\n')

        for i in range(1, 16):
            f.write('   * - ' + hex(i)[2:].upper() + '\n')
            for j in range(1, 16):
                f.write('     - ' + hex(i+j)[2:].upper().rjust(2, '0') + '\n')

        f.write('.. list-table:: Hexadecimal Multiplication\n')
        f.write('   :header-rows: 1\n\n')

        f.write('   * - 1\n')
        for i in range(2, 15):
            f.write('     - ' + hex(i)[2:].upper() + '\n')
        f.write('     - F\n')

        for i in range(2, 16):
            f.write('   * - ' + hex(i)[2:].upper() + '\n')
            for j in range(2, 16):
                f.write('     - ' + hex(i*j)[2:].upper().rjust(2, '0') + '\n')


def hexadecimal_decimal_integer_conversion(directory: str) -> None:
    """
    Create the page for the hex/dec conversion

    Parameters
    ----------
    directory: str, mandatory
        String containing the target directory for the file.

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
    doc_name = sys._getframe().f_code.co_name
    filename = directory + '/' + doc_name + doc_suffix

    with open(filename, "w") as f:
        write_title(f, doc_name)
        f.write('\n\n.. include:: ../../global.rst')
        f.write('\n\n')
        f.write('\nThe table below provldes for direct conversions ')
        f.write('between hexadecimal integers in the range O-FFF and decimal ')
        f.write('integers in the range 0-4095. \n\n')
        f.write('For conversion of larger integers, the table values ')
        f.write('may be added to the following figures:\n')

        f.write('\n.. csv-table:: ')
        f.write('\n   :header: "Hex", "Decimal", "Hex", "Decimal"')
        f.write('\n   :widths: 25, 25, 25, 25')
        f.write('\n')

        f.write('\n   "1 000","4 096","20 000","131 072"')
        f.write('\n   "2 000","8 192","30 000","196 608"')
        f.write('\n   "3 000","12 288","40 000","262 144"')
        f.write('\n   "4 000","16 384","50 000","327 680"')
        f.write('\n   "5 000","20 480","60 000","393 216"')
        f.write('\n   "6 000","24 576","70 000","458 752"')
        f.write('\n   "7 000","28 672","80 000","524 288"')
        f.write('\n   "8 000","32 768","90 000","589 824"')
        f.write('\n   "9 000","36 864","A0 000","655 360"')
        f.write('\n   "A 000","40 960","B0 000","720 896"')
        f.write('\n   "B 000","45 056","C0 000","786 432"')
        f.write('\n   "C 000","49 152","D0 000","851 968"')
        f.write('\n   "D 000","53 248","E0 000","917 504"')
        f.write('\n   "E 000","57 344","F0 000","983 040"')
        f.write('\n   "F 000","61 440","100 000","1 048 576"')
        f.write('\n   "10 000","65 536","200 000","2 097 152"')
        f.write('\n   "11 000","69 632","300 000","3 145 728"')
        f.write('\n   "12 000","73 728","400 000","4 194 304"')
        f.write('\n   "13 000","77 824","500 000","5 242 880"')
        f.write('\n   "14 000","81 920","600 000","6 291 456"')
        f.write('\n   "15 000","86 016","700 000","7 340 032"')
        f.write('\n   "16 000","90 112","800 000","8 388 608"')
        f.write('\n   "17 000","94 208","900 000","9 437 184"')
        f.write('\n   "18 000","98 304","A00 000","10 485 760"')
        f.write('\n   "19 000","102 400","B00 000","11 534 336"')
        f.write('\n   "1A 000","106 496","C00 000","12 582 912"')
        f.write('\n   "1B 000","110 592","D00 000","13 631 408"')
        f.write('\n   "1C 000","114 688","E00 000","14 680 064"')
        f.write('\n   "1D 000","118 784","F00 000","15 728 640"')
        f.write('\n   "1E 000","122 880","1 000 000","16 777 216"')
        f.write('\n   "1F 000","126 976","2 000 000","33 554 432"')
        f.write('\n\n\n')

        f.write('.. list-table:: You will need to horizontally scroll....\n')
        f.write('   :header-rows: 1\n\n')

        f.write('   * - \n')
        for i in range(15):
            f.write('     - ' + hex(i)[2:].upper() + '\n')
        f.write('     - F\n')

        dec = 0
        for i in range(0, 4096, 16):
            f.write('   * - ' + hex(i)[2:].upper().rjust(3, '0') + '\n')
            for j in range(16):
                f.write('     - ' + str(dec).rjust(3, '0') + '\n')
                dec = dec + 1


def instruction_summary(directory: str) -> None:

    operations = [
        {"group": 'index_register_instructions',
         "instructions": ["fin", "inc"]},
        {"group": 'index_register_to_accumulator_instructions',
         "instructions": ["add", "sub", "ld", "xch"]},
        {"group": 'accumulator_instructions',
         "instructions": ["clb", "clc", "iac", "cmc", "cma",
                          "ral", "rar", "tcc", "dac", "tcs",
                          "stc", "daa", "kbp"]},
        {"group": 'immediate_instructions',
         "instructions": ["fim", "ldm"]},
        {"group": 'transfer_of_control_instructions',
         "instructions": ["jun", "jin", "jcn", "isz"]},
        {"group": 'subroutine_linkage_instructions',
         "instructions": ["jms", "bbl"]},
        {"group": 'memory_selection_instructions',
         "instructions": ["src", "dcl"]},
        {"group": 'io_and_ram_instructions',
         "instructions": ["wrm", "wmp", "wrr", "wpm",
                          "wrn", "rdm", "rdr", "rdn",
                          "adm", "sbm"]},
        {"group": 'nop_instructions', "instructions": ["nop"]}
    ]

    descriptions = [{"inst": "fin", "desc": "Load RP with 8 bits of ROM data addressed by register pair 0."},  # noqa
                    {"inst": "inc", "desc": "Increment register REG."},  # noqa
                    {"inst": "add", "desc": "Add REG plus carry bit to the accumulator."},  # noqa
                    {"inst": "sub", "desc": "Subtract REG from accumulator with borrow."},  # noqa
                    {"inst": "ld", "desc": "Load accumulator from REG."},  # noqa
                    {"inst": "xch", "desc": "Exchange the contents of accumulator and REG."},  # noqa
                    {"inst": "clb", "desc": "Clear both the accumulator and carry."},  # noqa
                    {"inst": "clc", "desc": "Clear carry."},  # noqa
                    {"inst": "iac", "desc": "Increment accumulator."},  # noqa
                    {"inst": "cmc", "desc": "Complement carry."},  # noqa
                    {"inst": "cma", "desc": "Complement each bit of the accumulator."},  # noqa
                    {"inst": "ral", "desc": "Rotate accumulator left through carry."},  # noqa
                    {"inst": "rar", "desc": "Rotate accumulator right through carry."},  # noqa
                    {"inst": "tcc", "desc": "Transmit the value of the carry to the accumulator then clear carry."},  # noqa
                    {"inst": "dac", "desc": "Decrement accumulator."},  # noqa
                    {"inst": "tcs", "desc": "Adjust accumulator for decimal subtract."},  # noqa
                    {"inst": "stc", "desc": "Set carry."},
                    {"inst": "daa", "desc": "Adjust accumulator for decimal add."},  # noqa
                    {"inst": "kbp", "desc": "Convert accumulator from 1 of n code to a binary value."},  # noqa
                    {"inst": "fim", "desc": "Load 8 bit immediate DATA into register pair RP."},  # noqa
                    {"inst": "ldm", "desc": "Load 4-bit immediate DATA into the accumulator."},  # noqa
                    {"inst": "jun", "desc": "Jump to location ADDR."},  # noqa
                    {"inst": "jin", "desc": "Jump to the address in register pair RP."},  # noqa
                    {"inst": "jcn", "desc": "Jump to ADDR if condition true."},  # noqa
                    {"inst": "isz", "desc": "Increment REG. If zero, skip. If non zero, jump to ADDR"},  # noqa
                    {"inst": "jms", "desc": "Call subroutine and push return address onto stack."},  # noqa
                    {"inst": "bbl", "desc": "Return from subroutine and load accumulator with immediate DATA."},  # noqa
                    {"inst": "nop", "desc": "No Operation"},  # noqa
                    {"inst": "src", "desc": "Contents of RP select a RAM or ROM address to be used by I/O and RAM instructions."},  # noqa
                    {"inst": "dcl", "desc": "Select a particular RAM bank."},  # noqa
                    {"inst": "wrm", "desc": "Write accumulator to RAM."},  # noqa
                    {"inst": "wmp", "desc": "Write accumulator to RAM output port"},  # noqa
                    {"inst": "wrr", "desc": "Write accumulator to ROM output port."},  # noqa
                    {"inst": "wpm", "desc": "Write accumulator to Program RAM."},  # noqa
                    {"inst": "wrn", "desc": "Write accumulator to RAM status char&cter n (n = 0, 1, 2 or 3)."},  # noqa
                    {"inst": "rdm", "desc": "Load accumulator from RAM."},  # noqa
                    {"inst": "rdr", "desc": "Load accumulator from ROM input port."},  # noqa
                    {"inst": "rdn", "desc": "Load accumulator from RAM status character n (n = 0, 1, 2 or 3) ."},  # noqa
                    {"inst": "adm", "desc": "Add RAM data plus carry to accumulator."},  # noqa
                    {"inst": "sbm", "desc": "Subtract RAM data from accumulator with borrow."}  # noqa
                     ]  # noqa

    for section in operations:
        doc_name = section["group"]
        filename = directory + os.sep + doc_name + doc_suffix
        fragment_file = '..' + os.sep + 'source' + os.sep + 'intro' + \
            os.sep + 'manual' + os.sep + 'fragments' + os.sep + \
            doc_name + frag_suffix
        with open(filename, "w") as f:
            write_title(f, doc_name)
            f.write('\n\n.. include:: ../../global.rst')
            f.write('\n\n')
            f.write('.. toctree::\n   :hidden:\n\n')
            for ins in section["instructions"]:
                f.write('   /hardware/machine/' + ins + '\n')
            # Include the fragment file
            try:
                fragment = open(fragment_file, 'r')
                while True:
                    # Get next line from file
                    line = fragment.readline()
                    # if line is empty
                    # end of file is reached
                    if not line:
                        break
                    if line[:8] != ':orphan:':
                        f.write(line)
                fragment.close()
            except FileNotFoundError:
                # if there is no fragment file, then no problem
                pass
            f.write('\n\n')
            f.write('.. list-table:: \n')
            f.write('   :header-rows: 1\n\n')
            f.write('   * - Code\n')
            f.write('     - Description\n')

            for instruction in section["instructions"]:

                description = next((x for x in descriptions
                                   if x["inst"] == instruction), None)
                f.write('   * - :ref:`hardware-machine-' + instruction + '`\n')
                f.write('     - ' + description["desc"] + '\n')
        f.close()


def main(argv: list) -> None:
    """
    Create documentation pages from information
    contained in the code, and other places.

    Parameters
    ----------
    argv: list, mandatory
        list of command line arguments

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

    print("Building automated pages.....")

    # Create new instance of a processor
    chip = Processor()

    instruction_machine_codes(chip, manual)
    powers_of_two(manual)
    powers_of_sixteen(manual)
    powers_of_10(manual)
    hexadecimal_decimal_integer_conversion(manual)
    hexadecimal_arithmetic(manual)
    instruction_summary(manual)


manual = '..' + os.sep + 'source' + os.sep + 'intro' + os.sep + 'manual'
doc_suffix = '.rst'
frag_suffix = '.frag'

main(sys.argv[1:])
