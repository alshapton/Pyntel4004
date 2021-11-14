# Import i4004 processor
import sys
sys.path.insert(1, '../src')

from hardware.processor import Processor  # noqa
from executer.exe_supporting import deal_with_monitor_command, is_breakpoint  # noqa
from shared.shared import coredump, do_error, get_opcodeinfobyopcode  # noqa

##############################################################################
#  _ _  _    ___   ___  _  _     ______                 _       _            #
# (_) || |  / _ \ / _ \| || |   |  ____|               | |     | |           #
#  _| || |_| | | | | | | || |_  | |__   _ __ ___  _   _| | __ _| |_ ___  _ _ #
# | |__   _| | | | | | |__   _| |  __| | '_ ` _ \| | | | |/ _` | __/ _ \| '_|#
# | |  | | | |_| | |_| |  | |   | |____| | | | | | |_| | | (_| | || (_) | |  #
# |_|  |_|  \___/ \___/   |_|   |______|_| |_| |_|\__,_|_|\__,_|\__\___/|_|  #
#                                                                            #
##############################################################################


def execute(chip: Processor, location: str, PC: int, monitor: bool):
    """
    Control the execution of a previously assembled program.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location : str, mandatory
        The location to which the program should be loaded

    PC : int, mandatory
        The program counter value to commence execution

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    Returns
    -------
    True        in all instances

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    breakpoints = []  # noqa
    _TPS = []
    if location == 'rom':
        _TPS = chip.ROM
    if location == 'ram':
        _TPS = chip.PRAM

    chip.PROGRAM_COUNTER = PC
    opcode = 0
    classic_prompt = '>>> '
    breakout_prompt = 'B>> '
    prompt = classic_prompt
    while opcode != 255:  # pseudo-opcode (directive) for "end"
        monitor_command = 'none'

        if is_breakpoint(breakpoints, chip.PROGRAM_COUNTER):
            monitor_command = 'none'
            monitor = True
            prompt = breakout_prompt
        if monitor is True:
            while monitor_command != '':
                monitor_command = input(prompt).lower()
                result, monitor, monitor_command, opcode = \
                    deal_with_monitor_command(chip, monitor_command,
                                              breakpoints, monitor, opcode)
                if result is False:
                    prompt = classic_prompt
                if result is None:
                    break
        custom_opcode = False
        OPCODE = _TPS[chip.PROGRAM_COUNTER]
        if OPCODE == 255:  # pseudo-opcode (directive "end" - stop program)
            print('           end')
            break
        opcodeinfo = get_opcodeinfobyopcode(chip, OPCODE)

        exe = opcodeinfo['mnemonic']
        if exe == '-':
            break

        # Only mnemonic with 2 characters - fix
        if exe[:3] == 'ld ':
            exe = exe[:2] + exe[3:]

        # Ensure that the correct arguments are passed to the operations
        if exe[:3] == 'fim':
            custom_opcode = True
            value = str(_TPS[chip.PROGRAM_COUNTER + 1])
            cop = exe.replace('data8', value)
            exe = exe.replace('p', '').replace('data8)', '') + value + ')'

        if exe[:3] == 'isz':
            # Remove opcode from 1st byte to get register
            register = bin(_TPS[chip.PROGRAM_COUNTER] & 15)[2:].zfill(8)[4:]
            address = str(_TPS[chip.PROGRAM_COUNTER + 1])
            exe = 'isz(' + str(int(register, 2)) + ',' + str(address) + ')'

        if exe[:4] == 'jcn(':
            custom_opcode = True
            address = _TPS[chip.PROGRAM_COUNTER + 1]
            conditions = (bin(_TPS[chip.PROGRAM_COUNTER])[2:].zfill(8)[4:])
            b10address = str(address)
            cop = exe.replace('address8', b10address)
            exe = exe[:4] + str(int(conditions, 2)) + ',' + b10address + ')'

        if exe[:4] in ('jun(', 'jms('):
            custom_opcode = True
            # Remove opcode from 1st byte
            hvalue = bin(_TPS[chip.PROGRAM_COUNTER] &
                         0xffff0000)[2:].zfill(8)[:4]
            lvalue = bin(_TPS[chip.PROGRAM_COUNTER + 1])[2:].zfill(8)
            whole_value = str(int(hvalue + lvalue, 2))
            cop = exe.replace('address12', whole_value)
            exe = exe[:4] + whole_value + ')'

        if custom_opcode:
            custom_opcode = False
            print('  {:>7}  {:<10}'.format(OPCODE, cop.replace('()', '')))
        else:
            print('  {:>7}  {:<10}'.format(OPCODE, exe.replace('()', '')))

        exe = 'chip.' + exe

        # Evaluate the command (some commands may change
        # the PROGRAM_COUNTER here)
        # Deliberately using eval here... skip checks in all code quality tools
        # skipcq: PYL-PYL-W0123
        try:
            eval(exe)  # noqa
        except Exception as ex:  # noqa
            cls = str(type(ex))
            x = cls.replace('<class ', '').replace('>', ''). \
                replace("'", '').split('.')
            ex_type = x[len(x)-1]
            ex_args = str(ex.args).replace('(', '').replace(',)', '')
            message = ex_type + ': ' + ex_args + ' at location ' + \
                str(chip.PROGRAM_COUNTER)
            do_error(message)
            coredump(chip, 'fred')
            return False
    return True
