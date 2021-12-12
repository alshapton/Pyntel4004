##########################################################################
#                         _ _ _   __   __  _ _                            #
#                        (_) | | /  \ /  \| | |                           #
#                        | |_  _| () | () |_  _|                          #
#                        |_| |_| \__/ \__/  |_|                           #
#                          _                 _   _                        #
#                  ____  _| |__ _ _ ___ _  _| |_(_)_ _  ___               #
#                 (_-< || | '_ \ '_/ _ \ || |  _| | ' \/ -_)              #
#                 /__/\_,_|_.__/_| \___/\_,_|\__|_|_||_\___|              #
#                                                                         #
###########################################################################

"""
Commands in this module.

            BBL -   BRANCH BACK AND LOAD
            JMS -   JUMP TO SUBROUTINE


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

# Import typing library
from typing import Tuple

from hardware.exceptions import ValueOutOfRangeForStack


def bbl(self, accumulator: int) -> Tuple[int, int]:
    """
    Name:           Branch back and load data to the accumulator.

    Function:       The program counter (address stack) is pushed down one
                    level.
                    Program control transfers to the next instruction
                    following the last jump to subroutine (JMS)
                    instruction.
                    The 4 bits of data DDDD stored in the OPA portion of
                    the instruction are loaded to the accumulator.
                    BBL is used to return from subroutine to main program.
    Syntax:         BBL
    Assembled:      0110 DDDD
    Symbolic:       (Stack) --> PL, PM, PH
                    DDDD --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    address = self.read_from_stack()
    self.PROGRAM_COUNTER = address
    self.ACCUMULATOR = accumulator
    return self.PROGRAM_COUNTER, self.ACCUMULATOR


def jms(self, address: int) -> int:
    """
    Name:           Jump to Subroutine.

    Function:       The address of the next instruction in sequence following
                    JMS (return address) is saved in the push down stack.
                    Program control is transferred to the instruction located
                    at the 12 bit address (AAAA3,AAAA2,AAAA1). Execution of a
                    return instruction (BBL) will cause the saved address to
                    be pulled out of the stack, therefore, program control
                    is transferred to the next sequential instruction after
                    the last JMS.
                    The push down stack has 4 registers. One of them is used
                    as the program counter, therefore nesting of JMS can occur
                    up to 3 levels.
    Syntax:         JMS
    Assembled:      0101 AAAA3
                    AAAA2 AAAA1
    Symbolic:       AAAA1 --> PL,
                    AAAA2 --> PM,
                    AAAA3 --> PH
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable

    """
    # Add number of words so return address is correct
    self.write_to_stack(self.PROGRAM_COUNTER + 2)
    if 0 <= address <= 4095:
        self.PROGRAM_COUNTER = address - 1
        return self.PROGRAM_COUNTER
    raise ValueOutOfRangeForStack(' Value: ' + str(address))
