# Import i4004 processor

from hardware.processor import processor
import getopt
import sys

# Assembler imports

from assembler.assemble import assemble

# Executer imports
from executer.execute import execute, retrieve


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
    outputfile = 'default.obj'
    pc = 0

    # Create new instance of a processor
    chip = processor()

    RUN = False
    try:
        opts, args = getopt.getopt(argv, "i:o:r:x", ["ifile=", "ofile=", "s"])  # noqa
    except getopt.GetoptError:
        print('4004 -i <inputfile>\n -o <outputfile> -x')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('4004 -i <inputfile> -o <outputfile> -x')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            if outputfile == '':
                outputfile = inputfile.replace('asm', 'obj')
            else:
                outputfile = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            result = assemble(inputfile, outputfile, chip)
        elif opt == "-x":
            RUN = True
        elif opt == "-r":
            reloadfile = arg
            RUN = True
            result = retrieve(reloadfile, chip)
            pc = result[1]
            memory_space = result[0]
            print('Executing    : ' + arg)
            print('Memory space : ' + memory_space)
            print('From         : ' + str(pc))
            print()
            execute(chip, memory_space, pc, True)

    if RUN is True and result is True:
        print()
        print('EXECUTING PROGRAM: ')
        print()
        execute(chip, 'rom', pc, True)
        print()
        acc = chip.read_accumulator()
        print('Accumulator : ' + str(acc) +
              '  (0b ' + str(processor.decimal_to_binary(4, acc)) + ')')
        print('Carry       :', chip.read_carry())
        print()


main(sys.argv[1:])
