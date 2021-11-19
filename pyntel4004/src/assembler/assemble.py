"""Assembler main module."""

# Disable pylint's too-many-locals warning, since there
# are functions in this module with large numbers of locals.

# pylint: disable=too-many-locals


# Import i4004 processor
from hardware.processor import Processor

# Assembler imports
from assembler.asm_supporting import  asm_comment, asm_label, asm_main, do_error, pass0, pass1, wrap_up   # noqa
# Shared imports
from shared.shared import get_opcodeinfo  # noqa

###############################################################################
#  _ _  _    ___   ___  _  _                                _     _           #
# (_) || |  / _ \ / _ \| || |     /\                       | |   | |          #
#  _| || |_| | | | | | | || |_   /  \   __ __  __ _ __ ___ | |__ | | ___ _ _  #
# | |__   _| | | | | | |__   _| / /\ \ / _/ _|/ _\ '_ ` _ \| '_ \| |/ _ \ '_| #
# | |  | | | |_| | |_| |  | |  / ____ \\_ \_ \  _/ | | | | | |_) | |  __/ |   #
# |_|  |_|  \___/ \___/   |_| /_/    \_\__/__/\__|_| |_| |_|_.__/|_|\___|_|   #
#                                                                             #
###############################################################################


def assemble(program_name: str, object_file: str, chip: Processor):
    """
    Main two-pass assembler for i4004 code.

    Parameters
    ----------
    program_name: str, mandatory
        Name of the source file to load

    object_file: str, mandatory
        Name of the output file in which to place the object code

    chip: Processor, mandatory
        Instance of a processor to place the assembled code in.

    Returns
    -------
    True if the code assembles correctly
    False if there are errors in the code

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    #     mccabe: MC0001 / assemble is too complex (44) - start
    #     mccabe: MC0001 / assemble is too complex (35)
    #     mccabe: MC0001 / assemble is too complex (30)
    #     mccabe: MC0001 / assemble is too complex (25)
    #     mccabe: MC0001 / assemble is too complex (21)
    #     mccabe: MC0001 / assemble is too complex (18)
    #     mccabe: MC0001 / assemble is too complex (13)
    #     mccabe: MC0001 / assemble is too complex (10)

    # Pass 0 - Initialise label tables, program storage etc
    _labels, tps, tfile = pass0(chip)

    # Program Line Count
    count = 0

    # Pass 1
    err, _labels, tps, tfile, address = pass1(chip, program_name,
                                              _labels, tps, tfile)

    if err:
        do_error(err + "\nProgram Assembly halted @ Pass 1\n\n")
        return False

    # Pass 2
    print('Address  Label   Address        Assembled                    ' +
          '  Line     Op/Operand')
    print(' (Dec)            (Bin)           (Bin)          (Dec)')
    print('                            Word 1     Word 2')

    org_found = False
    location = ''

    while True:
        line = tfile[count].strip()
        if len(line) == 0:
            break  # End of code
        x = line.split()
        label = ''

        # Check for initial comments
        if line[0] == '/':
            asm_comment(label, count, line)
        else:
            if len(line) > 0:
                if x[0][-1] == ',':
                    label = x[0]
                    opcode = x[1]
                    # Check to see if we are assembling a label
                    if '0' <= str(x[1])[:1] <= '9':
                        tps = asm_label(tps, address, x, count, label)
                        break
                else:
                    opcode = x[0]

                opcodeinfo = get_opcodeinfo(chip, 'S', opcode)
                chip, x, _labels, address, tps, opcodeinfo, label, count, \
                    err, org_found, location = \
                    asm_main(chip, x, _labels, address, tps, opcode,
                             opcodeinfo, label, count, org_found,
                             location)
                if err:
                    do_error(err)
                    break

        count = count + 1

    if err:
        print("Program Assembly halted")
        return False

    # Wrap up assembly process and write to file if necessary
    chip = wrap_up(chip, location, tps, _labels, object_file)
    return True
