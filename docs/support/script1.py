"""Construct opcode table for documentation."""

# Disable pylint's too-many-locals warnings,
# since there are large numbers of local variables.

# pylint: disable=too-many-locals

# Import system libraries

# Import system modules
import os
import struct
import sys
from typing import Any

sys.path.insert(1, '..' + os.sep + '..' + os.sep +
                'pyntel4004' + os.sep + 'src')

# Import i4004 processor
from hardware.processor import Processor  # noqa


def convert(num):
    # map for decimal to hexa, 0-9 are
    # straightforward, alphabets a-f used
    # for 10 to 15.
    m = dict.fromkeys(range(16), 0)

    digit = ord('0')
    c = ord('a')

    for i in range(16):
        if (i < 10):
            m[i] = chr(digit)
            digit += 1
        else:
            m[i] = chr(c)
            c += 1

    # string to be returned
    res = ""

    # check if num is 0 and directly return "0"
    if (not num):
        return "0"

    # if num>0, use normal technique as
    # discussed in other post
    if (num > 0):
        while (num):
            res = m[num % 16] + res
            num //= 16
    # if num<0, we need to use the elaborated
    # trick above, lets see this
    else:
        # store num in a u_int, size of u_it is greater,
        # it will be positive since msb is 0
        n = num + 2**32

        # use the same remainder technique.
        while (n):
            res = m[n % 16] + res
            n //= 16

    return res


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


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
    powers = [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
            nfmt = "{:.63f}"
            neg_num = float(((10 ** -i) * (16 ** powers[i])))
            #neg_num = -(10 ** i)
            print(neg_num)
            neg_output = float.hex((neg_num))
            #neg_interim = nfmt.format(neg_num)

            '''
            neg = str([neg_output[i:i+5]
                      for i in range(0, len(neg_output), 5)]).\
                replace('[', '').replace(']', '').replace(',', '').\
                replace("'", "")
            neg = neg[:23] + ' x 10 :superscript:`' + \
                str(powers[i] * -1) + '`'

            '''
            neg = neg_output
            f.write('   * - ' + pos + '\n')
            f.write('     - ' + str(i) + '\n')
            f.write('     - ' + neg + '  ' + str(i) +
                    ' ' + str(powers[i]) + '\n')

    f.close()


def instruction_machine_codes(chip, directory: str) -> None:
    """
    Create the page for the machine code/opcode list

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

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
    # Create new instance of a processor
    chip = Processor()

    instruction_machine_codes(chip, manual)
    powers_of_two(manual)
    powers_of_sixteen(manual)
    powers_of_10(manual)


manual = '..' + os.sep + 'source' + os.sep + 'intro' + os.sep + 'manual'
doc_suffix = '.rst'

main(sys.argv[1:])
