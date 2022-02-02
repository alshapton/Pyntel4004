"""Assembler supporting functions."""

# Disable pylint's too-many-locals warnings,
# since there are large numbers of local variables.

# pylint: disable=too-many-locals

# Import system libraries
import getopt
import sys

# Import i4004 processor
from hardware.processor import Processor

# Assembler/disassembler imports
from assembler.assemble import assemble  # noqa
from disassembler.disassemble import disassemble  # noqa

# Executer imports
from executer.execute import execute  # noqa
from executer.exe_supporting import retrieve  # noqa


def main(argv: list) -> None:
    """
    Control the assembly,disasembly and execution of an assembly language file.

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

    inputfile = ''
    outputfile = 'default'
    pc = 0

    # Create new instance of a processor
    chip = Processor()

    run = False
    do_assemble = False
    do_disassemble = False
    """
    options:    -i / -ifile=    input file
                -o / -ofile=    output file
                -h              help
                -d              disassemble
                -x              execute
                -r              reload
    """
    helptxt = '4004 <options>\n'
    options = "options:    -i / -ifile=    input file \n \
            -o / -ofile=    output file \n \
            -h              help \n \
            -d              disassemble \n \
            -x              execute \n \
            -r              reload\n"

    try:
        opts, args = getopt.getopt(argv, "i:o:r:x:d")  # noqa
    except getopt.GetoptError:
        print(helptxt, options)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-d':
            reloadfile = str(args[0])
            do_disassemble = True
            run = False
        if opt == '-h':
            print(helptxt, options)
            sys.exit()
        if opt == "-o":
            if arg == '':
                outputfile = inputfile
            else:
                outputfile = arg
        if opt == "-i":
            inputfile = arg
            do_assemble = True
        if opt == "-x":
            run = True
        if opt == "-r":
            reloadfile = arg
            run = True
            result = retrieve(reloadfile, chip)
            pc = result[1]
            memory_space = result[0]
            print('Executing    : ' + arg)
            print('Memory space : ' + memory_space)
            print('From         : ' + str(pc))
            print()
            execute(chip, memory_space, pc, True)

    if do_assemble is True:
        result = assemble(inputfile, outputfile, chip)

    if do_disassemble is True:
        result = retrieve(reloadfile, chip)
        pc = result[1]
        memory_space = result[0]
        result = disassemble(chip, memory_space, 0)

    if run is True and result is True:
        print()
        print('EXECUTING PROGRAM: ')
        print()
        did_execute = execute(chip, 'rom', pc, True)
        if did_execute:
            print()
            acc = chip.read_accumulator()
            print('Accumulator : ' + str(acc) + '  (0b ' +
                  str(Processor.decimal_to_binary(4, acc)) + ')')
            print('Carry       :', chip.read_carry())
            print()


main(sys.argv[1:])
