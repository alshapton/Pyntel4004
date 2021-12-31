.. _and:

Logical AND
===========

.. include:: ../../global.rst



The AND function of two bits is given by the following truth table:


.. image:: /intro/manual/images/and-diag.png
          :scale: 50%
          :align: center

|just|
Since any bit ANDed with a zero produces a zero, and any bit ANDed with a one 
remains unchanged, the AND function is often used to zero groups of bits.
|br| |br| |just|
The following subroutine produces the AND, bit by bit, of the two 4-bit 
quantities held in index registers 0 and 1. 
The result is placed in register 0, while register 1 is set to 0. Index registers 2 and 3 are also used.
For example, if register 0 = 1110 and register 1 = 0011, register 0 will be replaced with 0010.

::

                        1 1 1 0
                AND     0 0 1 1
                        -------
                        0 0 1 0


The subroutine produces the AND of two bits by placing the bits in the leftmost 
position of the accumulator and register 2, respectively, and zeroing the right-most 
three bits of the accumulator and register 2. Register 2 is then added to the accumulator, 
and the resulting carry is equal to the AND of the two bits.

::

    AND,    FIM     1P  11      / Register 2 = 0, Register 3 = 11
    L1,     LDM     0           / Get bit of Register 0, Set accumulator = 0
            XCH     0           / Set Register 0 to accumulator; Register 0 = 0
            RAL                 / Move first 'AND' bit to carry
            XCH     0           / Save shifted data in Register 0, set accumulator = 0
            INC     3           / Done if Register 3 = 0
            XCH     3           / Register 3 to accumulator
            JCN     4   L2      / Return if accumulator = 0
            XCH     3           / Otherwise, restore accumulator and Register 3
            RAR                 / Bit of Register 0 is alone in the accumulator
            XCH     2           / Save first 'AND' bit in Register 2
            XCH     1           / Get bit of Register 1
            RAL                 / Move leftmost bit to carry
            XCH     1           / Save shifted data in Register 1
            RAR                 / Move second 'AND' bit to carry
            ADD     2           / 'ADD' gives the 'AND' of the bits in carry
            JUN     L1
    L2,     BBL     0           / Return to main program



