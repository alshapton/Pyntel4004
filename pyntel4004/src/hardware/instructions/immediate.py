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
Commands:   FIM -   FETCH IMMEDIATE
            LDM -   LOAD ACCUMULATOR IMMEDIATE
"""


def fim(self, registerpair: int, value: int):
    """
    Name:           Fetched immediate from ROM
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


def ldm(self, operand: int):
    """
    Name:           Load Accumulator Immediate
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
