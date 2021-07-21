# Import i4004 processor

from hardware.processor import processor
import getopt
import json
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
    RUN = False
    try:
        opts, args = getopt.getopt(argv, "i:o:x", ["ifile=", "ofile="])  # noqa
    except getopt.GetoptError:
        print('assemble.py -i <inputfile>\n -o <outputfile> -x')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('assemble -i <inputfile> -o <outputfile> -x')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            if outputfile == '':
                outputfile = inputfile.replace('asm', 'obj')
            else:
                outputfile = arg
        elif opt == "-x":
            RUN = True

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


def reload(inputfile, chip):
    # Open the file
    f = open(inputfile, "r")

    # Load required data
    data = json.loads(f.read())

    # Close the file
    f.close()

    # Get data for memory load from JSON
    memory_space = data['location']
    location = 0
    pc = location

    # Place program in memory
    for i in data['memory']:
        if memory_space == 'rom':
            chip.ROM[location] = int(i, 16)
        else:
            chip.PRAM[location] = int(i, 16)
        location = location + 1

    return memory_space, pc


# Create new instance of a processor
chip = processor()
inputfile = ''
results = reload('example.4004.obj.obj', chip)

pc = results[1]
memory_space = results[0]

execute(chip, memory_space, pc, True)


# main(sys.argv[1:])
