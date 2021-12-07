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

"""
Commands in this module.

            DCL -   DESIGNATE COMMAND LINE
            SRC -   SEND REGISTER CONTROL


 Abbreviations used in the descriptions of each instruction's actions:

            (    )      the content of
            -->         is transferred to
            ACC	        Accumulator (4-bit)
            CY	        Carry/link Flip-Flop
            ACBR	    Accumulator Buffer Register (4-bit)
            RRRR	    Index register address
            RPn	        Index register pair address
            PL	        Low order program counter Field (4-bit)
            PM	        Middle order program counter Field (4-bit)
            PH	        High order program counter Field (4-bit)
            ai	        Order i content of the accumulator
            CMi	        Order i content of the command register
            M	        RAM main character location
            MSi	        RAM status character i
            DB (T)	    Data bus content at time T
            Stack	    The 3 registers in the address register
                        other than the program counter

    Additional Abbreviations:
            ~           Inverse (1's complement)
            .           logical OR


"""

from hardware.exceptions import InvalidRamBank, InvalidRegisterPair
from hardware.suboperations.utility import decimal_to_binary


def dcl(self) -> int:
    """
    Name:           Designate command line.

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
    if self.ACCUMULATOR > 7:
        raise InvalidRamBank('RAM bank : ' + str(self.ACCUMULATOR))

    self.CURRENT_RAM_BANK = self.ACCUMULATOR
    self.increment_pc(1)
    return self.CURRENT_RAM_BANK


def src(self, registerpair: int) -> int:
    """
    Name:           Send register control.

    Function:       The 8 bit content of the designated index register pair
                    is sent to the RAM address register at X2 and X3.
                    A subsequent read, write, or I/O operation of the RAM will
                    utilize this address. Specifically, the first 2 bits of the
                    address designate a RAM chip; the second 2 bits designate
                    1 out of 4 registers within the chip;
                    the last 4 bits designate 1 out of 16 4-bit main memory
                    characters within the register.

                    This command is also used to designate a ROM for a
                    subsequent ROM I/O port operation. The first 4 bits
                    designate the ROM chip number to be selected. The address
                    in ROM or RAM is not cleared until the next SRC
                    instruction is executed.
                    The 8 bit content of the index register is unaffected.
    Syntax:         SRC
    Assembled:      0010 RRR1
    Symbolic:       (RRRO) --> DB (X2)
                    (RRR1) --> DB (X3)
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec..
    Side-effects:   Not Applicable
    """
    if registerpair > 7:
        raise InvalidRegisterPair('Register pair : ' + str(registerpair))

    self.increment_pc(1)
    address = self.read_registerpair(registerpair)
    self.COMMAND_REGISTER = decimal_to_binary(8, address)
    return address
