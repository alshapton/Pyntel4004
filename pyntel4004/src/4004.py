# Import i4004 processor

from hardware.processor import Processor
import getopt
import sys

# Assembler imports

from assembler.assemble import assemble

# Executer imports
from executer.execute import execute
from executer.supporting import retrieve


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
    outputfile = 'default'
    pc = 0

    # Create new instance of a processor
    chip = Processor()

    RUN = False
    ASSEMBLE = False
    try:
        opts, args = getopt.getopt(argv, "i:o:r:x", ["ifile=", "ofile=", "s"])  # noqa
    except getopt.GetoptError:
        print('4004 -i <inputfile>\n -o <outputfile> -x')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('4004 -i <inputfile> -o <outputfile> -x')
            sys.exit()
        if opt in ("-o", "--ofile"):
            if arg == '':
                outputfile = inputfile
            else:
                outputfile = arg
        if opt in ("-i", "--ifile"):
            inputfile = arg
            ASSEMBLE = True
        if opt == "-x":
            RUN = True
        if opt == "-r":
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
    print(opts, args)
    if ASSEMBLE is True:
        result = assemble(inputfile, outputfile, chip)

    if RUN is True and result is True:
        print()
        print('EXECUTING PROGRAM: ')
        print()
        did_execute = execute(chip, 'rom', pc, True)
        if did_execute:
            print()
            acc = chip.read_accumulator()
            print('Accumulator : ' + str(acc) +
                  '  (0b ' + str(Processor.decimal_to_binary(4, acc)) + ')')
            print('Carry       :', chip.read_carry())
            print()


main(sys.argv[1:])
