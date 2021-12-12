###########################################################
#  _ _  _    ___   ___  _  _     _           _            #
# (_) || |  / _ \ / _ \| || |   (_)         | |           #
#  _| || |_| | | | | | | || |_   _ _ __   __| | _____  __ #
# | |__   _| | | | | | |__   _| | | '_ \ / _` |/ _ \ \/ / #
# | |  | | | |_| | |_| |  | |   | | | | | (_| |  __/>  <  #
# |_|  |_|  \___/ \___/   |_|   |_|_| |_|\__,_|\___/_/\_\ #
#                                                         #
###########################################################

"""
Commands in this module.

            INC -   INCREMENT REGISTER
            FIN -   FETCH INDIRECT


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


def fin(self, registerpair: int) -> Tuple[int, int]:
    """
    Name:           Fetch indirect from ROM.

    Function:       The 8 bit content of the 0 index register
                    pair (0000) (0001) is sent out as an address
                    in the same page where the FIN instruction is located.
                    The 8 bit word at that location is loaded into the
                    designated index register pair. The program counter
                    is unaffected; after FIN has been executed the next
                    instruction in sequence will be addressed. The content
                    of the 0 index register pair is unaltered unless
                    index register 0 was designated.
    Syntax:         FIN
    Assembled:      0011 RRRO
    Symbolic:       (PH) (0000) (0001) --> ROM address
                    (OPR) --> RRRO
                    (OPA) --> RRR1
    Execution:      1 word, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable
    Exceptions:     a) Although FIN is a 1-word instruction, its execution
                        requires two memory cycles (21.6 psec).
                    b) When FIN is located at address (PH) 1111 1111 data will
                        be fetched from the next page(ROM) in sequence and not
                        from the same page(ROM) where the FIN instruction is
                        located. That is, next address is
                        (PH + 1) (0000) (0001) and not (PH) (0000) (0001).
    """
    eop = self.is_end_of_page(self.PROGRAM_COUNTER, 1)
    if eop is True:
        page_shift = 1
    else:
        page_shift = 0
    value = self.RAM[(self.REGISTERS[1] + (self.REGISTERS[0] << 4)) +
                     (self.PAGE_SIZE * page_shift)]
    self.insert_registerpair(registerpair, value)
    self.increment_pc(1)
    return self.REGISTERS[registerpair], self.REGISTERS[registerpair+1]


def inc(self, register: int) -> int:
    """
    Name:           Increment index register.

    Function:       The 4 bit content of the designated index register is
                    incremented by 1.
                    The index register is set to zero in case of overflow.
    Syntax:         INC <register>
    Assembled:      0110 <RRRR>
    Symbolic:       (RRRR) +1 --> RRRR
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.
    """
    self.increment_register(register)
    self.increment_pc(1)
    return self.REGISTERS[register]
