.. _or:

Logical OR
==========

.. include:: ../../global.rst



The OR function of two bits is given by the following truth table:


.. image:: /intro/manual/images/or-diag.png
          :scale: 50%
          :align: center


Since any bit ORed with a one produces a one, and any bit ORed with a zero 
remains unchanged, the OR function is often used to set groups of bits to one.
|br| |br|

The following subroutine produces the OR, bit by bit,of the two 4 bit quantities 
held in index registers 0 and 1. The result is placed in register 0 while register 
1 is set to 0. Index registers 2 and 3 are also used.

For example, if register 0 is set to 0100 and register 1 to  0011, register 0 will be replaced with 0111.

::

                        0 1 0 0
                AND     0 0 1 1
                        -------
                        0 1 1 1


The subroutine produces the OR of two bits by placing the bits in the leftmost 
position of the accumuiator and register 2, respectively, and zeroing the rightmost 
three bits of the accumulator and register 2. Register 2 is then added to the 
accumulator. If the resulting carry = 1, the OR of the two bits = 1. 
If the resulting carry = 0, the OR of the two bits is equal to the leftmost bit of the accumulator.

::

    OR,     FIM     1P  11      / Register 2 = 0, Register 3 = 11
    L1,     LDM     0           / Get bit of Register 0, Set accumulator = 0
            XCH     0           / Set Register 0 to accumulator; Register 0 = 0
            RAL                 / Move first 'OR' bit to carry
            XCH     0           / Save shifted data in Register 0, set accumulator = 0
            INC     3           / Done if Register 3 = 0
            XCH     3           / Register 3 to accumulator
            JCN     4   L2      / Return if accumulator = 0
            XCH     3           / Otherwise, restore accumulator and Register 3
            RAR                 / Bit of Register 0 is alone in the accumulator
            XCH     2           / Save first 'OR' bit in Register 2
            LDM     0           / Get bit in Register 1, set accumulator = 0
            XCH     1           / Get bit of Register 1
            RAL                 / Move leftmost bit to carry
            XCH     1           / Save shifted data in Register 1
            RAR                 / Move second 'OR' bit to carry
            ADD     2           / 'ADD' gives the 'OR' of the bits in carry
            JCN     2   L1      / Jump if carry = 1 because 'OR' = 1
            RAL                 / Otherwise, 'OR' leftmost bit of the accumulator,
                                / transmit to carry by RAL
            JUN     L1
    L2,     BBL     0           / Return to main program



