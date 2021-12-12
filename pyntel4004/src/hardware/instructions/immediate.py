##########################################################################
#                         _ _ _   __   __  _ _                           #
#                        (_) | | /  \ /  \| | |                          #
#                        | |_  _| () | () |_  _|                         #
#                        |_| |_| \__/ \__/  |_|                          #
#                   _                    _ _      _                      #
#                  (_)_ __  _ __  ___ __| (_)__ _| |_ ___                #
#                  | | '  \| '  \/ -_) _` | / _` |  _/ -_)               #
#                  |_|_|_|_|_|_|_\___\__,_|_\__,_|\__\___|               #
#                                                                        #
##########################################################################

"""
Commands in this module.

            FIM -   FETCH IMMEDIATE
            LDM -   LOAD ACCUMULATOR IMMEDIATE


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


def fim(self, registerpair: int, value: int) -> list:
    """
    Name:           Fetched immediate from ROM.

    Function:       The 2nd word represents 8-bits of data
                    which are loaded into the designated index register pair.
    Syntax:         FIM
    Assembled:      0010 RRR0
                    DDDD2  DDDD1
    Symbolic:       DDDD --> RRR0, DDDD1 --> RRR1
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable
    """
    self.insert_registerpair(registerpair, value)
    self.increment_pc(2)
    return self.REGISTERS


def ldm(self, operand: int) -> int:
    """
    Name:           Load Accumulator Immediate.

    Function:       The 4 bits of immediate data are loaded into
                    the accumulator.
    Syntax:         LDM <value>
    Assembled:      1101 <DDDD>
    Symbolic:       DDDD --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.
    """
    self.ACCUMULATOR = operand
    self.increment_pc(1)
    return self.ACCUMULATOR
