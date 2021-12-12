##########################################################################
#                                                                        #
#  _ _ _   __   __  _ _                              _      _            #
# (_) | | /  \ /  \| | |   __ _ __ __ _  _ _ __ _  _| |__ _| |_ ___ _ _  #
# | |_  _| () | () |_  _| / _` / _/ _| || | '  \ || | / _` |  _/ _ \ '_| #
# |_| |_| \__/ \__/  |_|  \__,_\__\__|\_,_|_|_|_\_,_|_\__,_|\__\___/_|   #
#                                                                        #
##########################################################################

"""
Commands in this module.

            CLB -   CLEAR BOTH
            CLC -   CLEAR CARRY
            CMA -   COMPLEMENT ACCUMULATOR
            CMC -   COMPLEMENT CARRY
            DAA -   DECIMAL ADJUST ACCUMULATOR
            DAC -   DECREMENT ACCUMULATOR
            IAC -   INCREMENT ACCUMULATOR
            KBP -   KEYBOARD PROCESS
            RAL -   ROTATE ACCUMULATOR LEFT THROUGH CARRY
            RAR -   ROTATE ACCUMULATOR RIGHT THROUGH CARRY
            STC -   SET CARRY
            TCC -   TRANSMIT CARRY AND CLEAR
            TCS -   TRANSFER CARRY SUBTRACT


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
from typing import Tuple, Any


def clb(self: Any) -> Tuple[int, int]:
    """
    Name:           Clear Both.

    Function:       Set accumulator and carry/link to 0.
    Syntax:         CLB
    Assembled:      1111 0000
    Symbolic:       0 --> ACC, 0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    self.set_accumulator(0)
    self.reset_carry()
    self.increment_pc(1)
    return self.read_accumulator(), self.read_carry()


def clc(self: Any) -> int:
    """
    Name:           Clear Carry.

    Function:       Set carry/link to 0.
    Syntax:         CLC
    Assembled:      1111 0001
    Symbolic:       0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    self.reset_carry()
    self.increment_pc(1)
    return self.read_carry()


def cma(self: Any) -> int:
    """
    Name:           Complement Accumulator.

    Function:       The content of the accumulator is complemented.
                    The carry/link is unaffected.
    Syntax:         CMA
    Assembled:      1111 0100
    Symbolic:       ~a3 ~a2 ~a1 ~a0 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    from hardware.suboperations.utility import ones_complement  # noqa

    ones_acc = int(ones_complement(self.ACCUMULATOR, 4), 2)
    self.ACCUMULATOR = ones_acc
    self.increment_pc(1)
    return self.ACCUMULATOR


def cmc(self: Any) -> int:
    """
    Name:           Complement carry.

    Function:       The carry/link content is complemented.
    Syntax:         CLC
    Assembled:      1111 0011
    Symbolic:       ~(CY) --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    if self.CARRY == 1:
        self.reset_carry()
    else:
        self.set_carry()
    self.increment_pc(1)
    return self.CARRY


def daa(self: Any) -> Tuple[int, int]:
    """
    Name:           Decimal adjust accumulator.

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
    if (self.read_carry() == 1 or self.ACCUMULATOR > 9):
        self.ACCUMULATOR = self.ACCUMULATOR + 6
        if self.ACCUMULATOR > self.MAX_4_BITS:
            self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
            self.set_carry()
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def dac(self: Any) -> Tuple[int, int]:
    """
    Name:           Decrement accumulator.

    Function:       The content of the accumulator is decremented by 1.
    Syntax:         DAC
    Assembled:      1111 1000
    Symbolic:       (ACC) -1 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   A borrow sets the carry/link to 0;
                    No borrow sets the carry/link to a 1.
    """
    self.ACCUMULATOR = self.ACCUMULATOR + 15
    if self.ACCUMULATOR >= self.MAX_4_BITS:
        self.ACCUMULATOR = self.MSB
        self.set_carry()
    else:
        self.reset_carry()
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def iac(self: Any) -> Tuple[int, int]:
    """
    Name:           Increment accumulator.

    Function:       The content of the accumulator is incremented by 1.
    Syntax:         IAC
    Assembled:      1111 0010
    Symbolic:       (ACC) +1 --> ACC
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   No overflow sets the carry/link to 0;
                    overflow sets the carry/link to a 1.
    """
    self.ACCUMULATOR = self.ACCUMULATOR + 1
    if self.ACCUMULATOR == self.MAX_4_BITS + 1:
        self.ACCUMULATOR = 0
        self.set_carry()
    else:
        self.reset_carry()
    self.increment_pc(1)
    return self.read_accumulator(), self.read_carry()


def kbp(self: Any) -> int:
    """
    Name:           Keyboard process.

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
                        KBP	  	        KBP
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
    acc = self.read_accumulator()
    self.increment_pc(1)
    if acc in (0, 1, 2):
        return acc

    if acc == 4:
        self.set_accumulator(3)
        return self.read_accumulator()

    if acc == 8:
        self.set_accumulator(4)
        return self.read_accumulator()

    # Error
    self.set_accumulator(15)
    return self.read_accumulator()


def ral(self: Any) -> Tuple[int, int]:
    """
    Name:           Rotate left.

    Function:       The content of the accumulator and carry/link
                    are rotated left.
    Syntax:         RAL
    Assembled:      1111 0101
    Symbolic:       C0 --> a0, a(i) --> a(i+1), a3 -->CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the highest significant
                    bit of the accumulator.
    """
    c0 = self.read_carry()
    # Shift left
    self.ACCUMULATOR = self.ACCUMULATOR * 2
    # Set carry bit correctly
    if self.ACCUMULATOR >= self.MAX_4_BITS:
        self.set_carry()
    else:
        self.reset_carry()
    # If necessary remove non-existent bit 5
    if self.ACCUMULATOR > self.MAX_4_BITS:
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
    # Add original carry bit
    self.ACCUMULATOR = self.ACCUMULATOR + c0
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def rar(self: Any) -> Tuple[int, int]:
    """
    Name:           Rotate right.

    Function:       The content of the accumulator and carry/link
                    are rotated right.
    Syntax:         RAR
    Assembled:      1111 0110
    Symbolic:       a0 --> CY, a(i) --> a(i-1), C0 -->a3
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be set to the lowest significant
                    bit of the accumulator.
    """
    c0 = self.read_carry()
    # Set carry bit correctly
    if self.ACCUMULATOR % 2 == 0:
        self.reset_carry()
    else:
        self.set_carry()
    # Shift right
    self.ACCUMULATOR = self.ACCUMULATOR // 2
    # Add carry to high-order bit of accumulator
    self.ACCUMULATOR = self.ACCUMULATOR + (c0 * self.MSB)
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def stc(self: Any) -> int:
    """
    Name:           Set Carry.

    Function:       Set carry/link to 1.
    Syntax:         STC
    Assembled:      1111 1010
    Symbolic:       1 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """
    self.set_carry()
    self.increment_pc(1)
    return self.read_carry()


def tcc(self: Any) -> Tuple[int, int]:
    """
    Name:           Transmit carry and clear.

    Function:       The accumulator is cleared.
                    The least significant position of the accumulator
                    is set to the value of the carry/link.
    Syntax:         TCC
    Assembled:      1111 0111
    Symbolic:       0 --> ACC, (CY) --> a0, 0 --> CY
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit will be reset..
    """
    self.set_accumulator(0)
    self.ACCUMULATOR = self.read_carry()
    self.reset_carry()
    self.increment_pc(1)
    return self.ACCUMULATOR, self.CARRY


def tcs(self: Any) -> Tuple[int, int]:
    """
    Name:           Transfer Carry Subtract.

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
    if self.read_carry() == 0:
        self.set_accumulator(9)
    else:
        self.set_accumulator(10)
    self.reset_carry()
    self.increment_pc(1)
    return self.read_accumulator(), self.read_carry()
