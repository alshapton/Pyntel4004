

#####################################################
#  _ _  _    ___   ___  _  _                        #
# (_) || |  / _ \ / _ \| || |                       #
#  _| || |_| | | | | | | || |_   _ __   ___  _ __   #
# | |__   _| | | | | | |__   _| | '_ \ / _ \| '_ \  #
# | |  | | | |_| | |_| |  | |   | | | | (_) | |_) | #
# |_|  |_|  \___/ \___/   |_|   |_| |_|\___/| .__/  #
#                                           | |     #
#                                           |_|     #
#                                                   #
#####################################################

"""
Commands in this module.

            NOP -   NO OPERATION

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


def nop(self) -> int:
    """
    Name:           No Operation.

    Function:       No operation performed.
    Syntax:         NOP
    Assembled:      0000 0000
    Symbolic:       Not applicable
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    self.increment_pc(1)
    return self.PROGRAM_COUNTER
