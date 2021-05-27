##########################################################################
#                         _ _ _   __   __  _ _                           #
#                        (_) | | /  \ /  \| | |                          #
#                        | |_  _| () | () |_  _|                         #
#                        |_| |_| \__/ \__/  |_|                          #
#                                                _        _              #
#         _ __  ___ _ __  ___ _ _ _  _   ___ ___| |___ __| |_            #
#        | '  \/ -_) '  \/ _ \ '_| || | (_-</ -_) / -_) _|  _|           #
#        |_|_|_\___|_|_|_\___/_|  \_, | /__/\___|_\___\__|\__|           #
#                                 |__/                                   #
##########################################################################


from src.hardware.exceptions import InvalidRamBank


def dcl(self):
    """
    Name:           Designate command line
    Function:       The content of the three least significant accumulator
                    bits is transferred to the command control register
                    within the CPU. This instruction provides RAM bank
                    selection when multiple RAM banks are used.
                    (If no DCL instruction is sent out, RAM Bank number
                    zero is automatically selected after application of at
                    least one RESET). See below for RAM Bank selection table.
                    DCL remains latched until it is changed.
    Syntax:         DCL
    Assembled:      1111 1101
    Symbolic:       a0 --> CM0, a1 --> CM1, a2 --> CM2
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable

                    The selection is made according to the following table.
                    (ACC)	CM-RAMi                     Enabled	Bank No.
                    -----	------------------------	------------
                    X000	CM-RAM0	                    Bank 0
                    X001	CM-RAM1	                    Bank 1
                    X010	CM-RAM2	                    Bank 2
                    X100	CM-RAM3	                    Bank 3
                    X011	CM-RAM1, CM-RAM1	        Bank 4
                    X101	CM-RAM1, CM-RAM3	        Bank 5
                    X110	CM-RAM2, CM-RAM3	        Bank 6
                    X111	CM-RAM1, CM-RAM2, CM-RAM3	Bank 7
    """

    ACC = self.ACCUMULATOR
    if (ACC > 7):
        raise InvalidRamBank('RAM bank : ' + str(ACC))

    self.CURRENT_RAM_BANK = ACC
    self.increment_pc(1)
    return self.CURRENT_RAM_BANK
