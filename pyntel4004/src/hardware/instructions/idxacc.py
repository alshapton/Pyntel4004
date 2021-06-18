#############################################################
#       _ _ _   __   __  _ _      _         _               #
#      (_) | | /  \ /  \| | |    (_)_ _  __| |_____ __      #
#      | |_  _| () | () |_  _|   | | ' \/ _` / -_) \ /      #
#  _   |_| |_| \__/ \__/  |_|    |_|_||_\__,_\___/_\_\      #
# | |_ ___    __ _ __ __ _  _ _ __ _  _| |__ _| |_ ___ _ _  #
# |  _/ _ \  / _` / _/ _| || | '  \ || | / _` |  _/ _ \ '_| #
#  \__\___/  \__,_\__\__|\_,_|_|_|_\_,_|_\__,_|\__\___/_|   #
#                                                           #
#############################################################

"""
Commands:   ADD -   ADD REGISTER TO ACCUMULATOR WITH CARRY
            SUB -   SUBTRACT REGISTER FROM ACCUMULATOR WITH BORROW
            LD  -   LOAD ACCUMULATOR
            XCH -   EXCHANGE REGISTER AND ACCUMULATOR
"""


def add(self, register: int):
    """
    Name:           Add index register to accumulator with carry
    Function:       The 4 bit content of the designated index register
                    is added to the content of the accumulator with carry.
                    The result is stored in the accumulator. (Note this
                    means the carry bit is also added)
    Syntax:         ADD <register>
    Assembled:      1000 <RRRR>
    Symbolic:       (RRRR) + (ACC) + (CY) --> ACC, CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is set to 1 if a sum greater than
                    MAX_4_BITS was generated to indicate a carry out;
                    otherwise, the carry/link is set to 0. The 4 bit
                    content of the index register is unaffected.
    """
    from hardware.suboperation import check_overflow

    self.ACCUMULATOR = (self.ACCUMULATOR + self.REGISTERS[register] +
                        self.read_carry())
    # Check for carry bit set/reset when an overflow is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    check_overflow(self)
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def sub(self, register: int):
    """
    Name:           Subtract index register from accumulator with borrow
    Function:       The 4 bit content of the designated index register is
                    complemented (ones complement) and added to content of
                    the accumulator with borrow and the result is stored
                    in the accumulator.
    Syntax:         SUB <register>
    Assembled:      1001 <RRRR>
    Symbolic:       (ACC) + ~(RRRR) + (CY) --> ACC, CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   If a borrow is generated, the carry bit is set to 0,
                    otherwise, it is set to 1.
                    The 4 bit content of the index register is unaffected.
    """
    carry = self.read_complement_carry()

    self.ACCUMULATOR = (self.ACCUMULATOR +
                        self.binary_to_decimal(
                            self.ones_complement(self.REGISTERS[register], 4))
                        + carry)
    # Check for carry bit set/reset when borrow (overflow) is detected
    # i.e. the result is more than a 4-bit number (MAX_4_BITS)
    if self.ACCUMULATOR > self.MAX_4_BITS:
        self.ACCUMULATOR = self.ACCUMULATOR - (self.MAX_4_BITS + 1)
        self.set_carry()
    else:
        self.reset_carry()
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def ld(self, register: int):
    """
    Name:           Load index register to Accumulator
    Function:       The 4 bit content of the designated index register
                    (RRRR) is loaded into accumulator.
                    The previous contents of the accumulator are lost.
    Syntax:         LD <value>
    Assembled:      1010 <RRRR>
    Symbolic:       (RRRR) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.
    """
    self.ACCUMULATOR = self.REGISTERS[register]
    self.increment_pc(1)
    return self.ACCUMULATOR


def xch(self, register: int):
    """
    Name:           Exchange index register and accumulator
    Function:       The 4 bit content of designated index register is
                    loaded into the accumulator. The prior content of the
                    accumulator is loaded into the designed register.
    Syntax:         XCH <register>
    Assembled:      1011 <RRRR>
    Symbolic:       (ACC) --> ACBR, (RRRR) --> ACC, (ACBR) --> RRRR
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.

    """
    self.ACBR = self.ACCUMULATOR
    self.ACCUMULATOR = self.REGISTERS[register]
    self.insert_register(register, self.ACBR)
    self.increment_pc(1)
    self.ACBR = 0
    return self.ACCUMULATOR, self.REGISTERS
