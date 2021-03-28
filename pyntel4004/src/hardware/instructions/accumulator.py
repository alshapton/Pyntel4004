##########################################################################
#                                                                        #
#  _ _ _   __   __  _ _                              _      _            #
# (_) | | /  \ /  \| | |   __ _ __ __ _  _ _ __ _  _| |__ _| |_ ___ _ _  #
# | |_  _| () | () |_  _| / _` / _/ _| || | '  \ || | / _` |  _/ _ \ '_| #
# |_| |_| \__/ \__/  |_|  \__,_\__\__|\_,_|_|_|_\_,_|_\__,_|\__\___/_|   #
#                                                                        #
##########################################################################


def clb(self):
    """
    Name:           Clear Both
    Function:       Set accumulator and carry/link to 0.
    Syntax:         CLB
    Assembled:      1111 0000
    Symbolic:       0 --> ACC, 0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    self.ACCUMULATOR = 0
    self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def clc(self):
    """
    Name:           Clear Carry
    Function:       Set carry/link to 0.
    Syntax:         CLC
    Assembled:      1111 0001
    Symbolic:       0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.CARRY


def iac(self):
    """
    Name:           Increment accumulator
    Function:       The content of the accumulator is incremented by 1.
    Syntax:         IAC
    Assembled:      1111 0010
    Symbolic:       (ACC) +1 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   No overflow sets the carry/link to 0;
                    overflow sets the carry/link to a 1.
    """

    self.ACCUMULATOR = self.ACCUMULATOR + 1
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def cmc(self):
    """
    Name:           Complement carry
    Function:       The carry/link content is complemented.
    Syntax:         CLC
    Assembled:      1111 0011
    Symbolic:       ~(CY) --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    if (self.CARRY == 1):
        self.reset_carry()
    else:
        self.set_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.CARRY


def cma(self):
    """
    Name:           Complement Accumulator
    Function:       The content of the accumulator is complemented.
                    The carry/link is unaffected.
    Syntax:         CMA
    Assembled:      1111 0100
    Symbolic:       ~a3 ~a2 ~a1 ~a0 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    self.ACCUMULATOR = self.ones_complement(self.ACCUMULATOR)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR


def ral(self):
    """
    Name:           Rotate left
    Function:       The content of the accumulator and carry/link
                    are rotated left.
    Syntax:         RAL
    Assembled:      1111 0101
    Symbolic:       C0 --> a0, a(i) --> a(i+1), a3 -->CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the highest significant
                    bit of the accumulator.
    """

    # Store Carry bit
    C0 = self.read_carry()
    # Shift left
    self.ACCUMULATOR = self.ACCUMULATOR * 2
    # Set carry bit correctly
    if (self.ACCUMULATOR >= self.MAX_4_BITS):
        self.set_carry()
    else:
        self.reset_carry()
    # If necessary remove non-existent bit 5
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
    # Add original carry bit
    self.ACCUMULATOR = self.ACCUMULATOR + C0
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def rar(self):
    """
    Name:           Rotate right
    Function:       The content of the accumulator and carry/link
                    are rotated right.
    Syntax:         RAR
    Assembled:      1111 0110
    Symbolic:       a0 --> CY, a(i) --> a(i-1), C0 -->a3
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the lowest significant
                    bit of the accumulator.
    """

    # Store Carry bit
    C0 = self.read_carry()
    # Set carry bit correctly
    if (self.ACCUMULATOR % 2 == 0):
        self.reset_carry()
    else:
        self.set_carry()
    # Shift right
    self.ACCUMULATOR = self.ACCUMULATOR // 2
    # Add carry to high-order bit of accumulator
    self.ACCUMULATOR = self.ACCUMULATOR + (C0 * self.MSB)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def tcc(self):
    """
    Name:           Transmit carry and clear
    Function:       The accumulator is cleared.
                    The least significant position of the accumulator
                    is set to the value of the carry/link.
    Syntax:         TCC
    Assembled:      1111 0111
    Symbolic:       0 --> ACC, (CY) --> a0, 0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the 0.
    """

    self.ACCUMULATOR = 0
    self.ACCUMULATOR = self.read_carry()
    self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def dac(self):
    """
    Name:           Decrement accumulator
    Function:       The content of the accumulator is decremented by 1.
    Syntax:         DAC
    Assembled:      1111 1000
    Symbolic:       (ACC) -1 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   A borrow sets the carry/link to 0;
                    No borrow sets the carry/link to a 1.
    """

    self.ACCUMULATOR = self.ACCUMULATOR + 15
    if (self.ACCUMULATOR > self.MAX_4_BITS):
        self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def tcs(self):
    """
    Name:           Transfer Carry Subtract
    Function:       The accumulator is set to 9 if the carry/link is 0.
                    The accumulator is set to 10 if the carry/link is a 1.
    Syntax:         TCS
    Assembled:      1111 1001
    Symbolic:       1001 --> ACC if (CY) = 0
                    1010 --> ACC if (CY) = 1
                    0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is set to 0.
    """

    if (self.read_carry() == 0):
        self.ACCUMULATOR = 9
    else:
        self.ACCUMULATOR = 10
    self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def stc(self):
    """
    Name:           Set Carry
    Function:       Set carry/link to 1.
    Syntax:         STC
    Assembled:      1111 1010
    Symbolic:       1 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    self.set_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.CARRY


def daa(self):
    """
    Name:           Decimal adjust accumulator
    Function:       The accumulator is incremented by 6 if
                    either the carry/link is 1 or if the accumulator
                    content is greater than 9.
    Syntax:         DAA
    Assembled:      1111 1011
    Symbolic:       (ACC) + (0000 or 0110) --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is set to a 1 if the result generates
                    a carry, otherwise it is unaffected.
    """

    if (self.read_carry == 1 or self.ACCUMULATOR > 9):
        self.ACCUMULATOR = self.ACCUMULATOR + 6
        if (self.ACCUMULATOR > self.MAX_4_BITS):
            self.ACCUMULATOR = self.MAX_4_BITS - self.MAX_4_BITS
        self.set_carry()
    else:
        self.reset_carry()
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR, self.CARRY


def kbp(self):
    """
    Name:           Keyboard process
    Function:       A code conversion is performed on the accumulator content,
                    from 1 out of n to binary code.
                    If the accumulator content has more than one bit on, the
                    accumulator will be set to 15.
                    (to indicate error) - conversion table below
    Syntax:         KBP
    Assembled:      1111 1100
    Symbolic:       (ACC) --> KBP, ROM --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry/link is unaffected.


                    (ACC)           (ACC)
                    before          after
                        KBP	  	     KBP
                        0000	---->	0000
                        0001	---->	0001
                        0010	---->	0010
                        0100	---->	0011
                        1000	---->	0100
                        0011	---->	1111    Error
                        0101	---->	1111    Error
                        0110	---->	1111    Error
                        0111	---->	1111    Error
                        1001	---->	1111    Error
                        1010	---->	1111    Error
                        1011	---->	1111    Error
                        1100	---->	1111    Error
                        1101	---->	1111    Error
                        1110	---->	1111    Error
                        1111	---->	1111    Error
    """
    if (self.ACCUMULATOR == 0
        or self.ACCUMULATOR == 1
            or self.ACCUMULATOR == 2):
        return self.ACCUMULATOR

    if (self.ACCUMULATOR == 4):
        self.ACCUMULATOR = 3
        return self.ACCUMULATOR

    if (self.ACCUMULATOR == 8):
        self.ACCUMULATOR = 4
        return self.ACCUMULATOR

    # Error
    self.ACCUMULATOR = 15
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.ACCUMULATOR
