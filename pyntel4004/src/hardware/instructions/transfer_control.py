##########################################################################
#                         _ _ _   __   __  _ _                           #
#                        (_) | | /  \ /  \| | |                          #
#                        | |_  _| () | () |_  _|                         #
#                        |_| |_| \__/ \__/  |_|                          #
#       _                     __                      _           _      #
#      | |_ _ _ __ _ _ _  ___/ _|___ _ _   __ ___ _ _| |_ _ _ ___| |     #
#      |  _| '_/ _` | ' \(_-<  _/ -_) '_| / _/ _ \ ' \  _| '_/ _ \ |     #
#       \__|_| \__,_|_||_/__/_| \___|_|   \__\___/_||_\__|_| \___/_|     #
#                                                                        #
##########################################################################

"""
    Commands:   JUN -   JUMP UNCONDITIONALLY
                JIN -   JUMP INDIRECT
                JCN -   JUMP ON CONDITION
                ISZ -   INCREMENT AND SKIP IF ZERO
"""


def jun(self, address: int):
    """
    Name:           Jump unconditional
    Function:       Program control is unconditionally
                    transferred to the instruction located
                    at the address AAAA3, AAAA2, AAAA1.
    Syntax:         JUN
    Assembled:      0100 AAAA3
                    AAAA2 AAAA1
    Symbolic:       AAAA1 --> PL,
                    AAAA2 --> PM,
                    AAAA3 --> PH
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable
    """
    from hardware.exceptions import ProgramCounterOutOfBounds

    if (address >= self.MEMORY_SIZE_RAM or address < 0):
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' +
                                        str(address))
    self.PROGRAM_COUNTER = address
    return self.PROGRAM_COUNTER


def jin(self, registerpair: int):
    """
    Name:           Jump Indirect
    Function:       The 8 bit content of the designated index register pair
                    is loaded into the low order 8 positions of the program
                    counter.
                    Program control is transferred to the instruction at
                    that address on the same page (same ROM) where the JIN
                    instruction is located.
                    The 8 bit content of the index register is unaffected.
    Syntax:         JIN
    Assembled:      0011 RRR1
    Symbolic:       (RRRO) --> PM
                    (RRR1) --> PL
                    PH unchanged
    Execution:      1 words, 16-bit code and an execution time of 10.8 usec.
    """
    from hardware.exceptions import ProgramCounterOutOfBounds

    address = self.read_registerpair(registerpair)
    PCB = self.PROGRAM_COUNTER

    # Increment PROGRAM_COUNTER by a page if the instruction is at
    # the last position in a page.
    if self.is_end_of_page(self.PROGRAM_COUNTER, 1) is True:
        self.PROGRAM_COUNTER = self.inc_pc_by_page(self.PROGRAM_COUNTER - 1)
        self.PROGRAM_COUNTER = self.PROGRAM_COUNTER - 12
        address = address - 1

    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER >> 8
    self.PROGRAM_COUNTER = (self.PROGRAM_COUNTER << 8) + address

    if self.PROGRAM_COUNTER >= self.MEMORY_SIZE_RAM:
        E_PC = self.PROGRAM_COUNTER
        self.PROGRAM_COUNTER = PCB
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' +
                                        str(E_PC))

    return self.PROGRAM_COUNTER


def jcn(self, conditions: int, address: int):
    """
    Name:           Jump conditional
    Function:       If the designated condition code is true, program control
                    is transferred to the instruction located at the 8 bit
                    address AAAA2, AAAA1 on the same page (ROM) where JCN is
                    located.
                    If the condition is not true the next instruction in
                    sequence after JCN is executed.
                    The condition bits are assigned as follows:
                    C1 = 0 Do not invert jump condition }
                    C1 = 1 Invert jump condition        }
                    C2 = 1 Jump if the accumulator content is zero
                    C3 = 1 Jump if the carry/link content is 1
                    C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
    Syntax:         JCN
    Assembled:      0001 C1C2C3C4
                    AAAA2 AAAA1
    Symbolic:       If C1C2C3C4 is true, A2A2A2A2 --> PM
                    A1A1A1A1 --> PL, PH unchanged
                    if C1C2C3C4 is false,
                    (PH) --> PH, (PM) --> PM, (PL + 2) --> PL
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Example:
    OPR     OPA
    ----    ----
    0001    0110  Jump if accumulator is zero or carry = 1

    Several conditions can be tested simultaneously.
    The logic equation describing the condition for a jump is give below:
    JUMP = ~C1 . ((ACC = 0) . C2 + (CY = 1) . C3 +
                ~TEST . C4) + C1 . ~((ACC = 0) . C2 +
                (CY = 1) . C3 + ~TEST . C4)

    Side-effects:   Not Applicable

    Info about signal/test pin 10 on intel4004
    https://tams.informatik.uni-hamburg.de/applets/hades/webdemos/80-mcs4/jmp/jmp_test.html

    Assembler:
            jcn     IACT    lbl

    I - Invert other conditions
    A - Accumulator = 0
    C - Carry Bit set (i.e. = 1)
    T - Test Signal on Intel4004 Pin 10 = 0

    Need to do "if JCN at end of page" code
    """
    i = int((conditions & 8) / 8)

    carry = self.read_carry()
    accumulator = self.read_accumulator()
    pin10 = self.read_pin10()
    if i == 0:
        if (carry == 1) or (accumulator == 0) or (pin10 == 0):
            self.PROGRAM_COUNTER = address
    else:
        if (carry == 1) or (accumulator != 0) or (pin10 == 1):
            self.increment_pc(2)
    return self.PROGRAM_COUNTER


def isz(self, register: int, address: int):
    """
    Name:           Increment index register skip if zero
    Function:       The content of the designated index register is
                    incremented by 1.
                    The accumulator and carry/link are unaffected.
                    If the result is zero, the next instruction after ISZ is
                    executed.
                    If the result is different from 0, program control is
                    transferred to the instruction located at the 8 bit
                    address AAAA2, AAAA1 on the same page (ROM) where the
                    ISZ instruction is located.
    Syntax:         ISZ
    Assembled:      0111 RRRR
                    AAAA2 AAAA1
    Symbolic:       (RRRR) + 1 --> RRRR,
                    if result = 0 (PH) --> PH, (PM) --> PM, (PL + 2) --> PL
                    if result <> 0  (PH) --> PH, AAAA2 --> PM, `AAAA1 --> PL
    Execution:      2 words, 16-bit code and an execution time of 21.6 usec.
    Side-effects:   Not Applicable


    """
    self.increment_register(register)
    if self.REGISTERS[register] == 0:
        self.increment_pc(2)
    else:
        self.PROGRAM_COUNTER = address
    return self.PROGRAM_COUNTER
