# Import i4004 processor

from hardware.processor import processor
import getopt
import sys

# Assembler imports

from assembler.assemble import assemble

# Executer imports
from executer.execute import execute


def main(argv):
    """
    Control the assembly and execution of a named assembly language file.

    Parameters
    ----------
    argv: list of command line arguments

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
    inputfile = ''
    outputfile = ''
    RUN = True
    try:
        opts, args = getopt.getopt(argv, "hi:o:norun", ["ifile=", "ofile="])  # noqa
    except getopt.GetoptError:
        print('assemble.py -i <inputfile>\n -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('assemble -i <inputfile> -o <outputfile> -norun')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            if outputfile == '':
                outputfile = inputfile.replace('asm', 'obj')
            else:
                outputfile = arg
        elif opt == "-norun":
            RUN = False

    # Create new instance of a processor
    chip = processor()

    result = assemble(inputfile, outputfile, chip)
    if RUN is True and result is True:
        print()
        print('EXECUTING PROGRAM: ')
        print()
        execute(chip, 'rom', 0, True)
        print()
        acc = chip.read_accumulator()
        print('Accumulator : ' + str(acc) +
              '  (0b ' + str(processor.decimal_to_binary(4, acc)) + ')')
        print('Carry       :', chip.read_carry())
        print()


main(sys.argv[1:])
