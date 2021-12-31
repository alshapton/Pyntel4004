.. _xor:

Logical XOR
===========

.. include:: ../../global.rst



The XOR function of two bits is given by the following truth table:


.. image:: /intro/manual/images/xor-diag.png
          :scale: 50%
          :align: center


Since the exclusive OR of two equal bits produces a zero and the exclusive 
OR of two unequal bits produces a one, the exclusive OR function can be used to 
test two quantities for equality. 
If the quantities differ in any bit position, a one will be produced in the result.
|br| |br|


The following subroutine produces the exclusive - OR of the two 4-bit quantities 
held in index registers 0 and 1. The result is placed in register 0, while register 1 is set to 0. 
Index registers 2 and 3 are also used. 

For example if register 0 = 0011 and register 1 = 0010, register 0 will be replaced with 0001.

::

                        0 0 1 1
                AND     0 0 1 0
                        -------
                        0 0 0 1



The subroutine produces the XOR of two bits by placing the bits in the leftmost position 
of the accumulator and register 2, respectively, and zeroing the rightmost three bIts of 
the accumulator and register 2. Register 2 is then added to the accumulator. 
The XOR of the two bits is then equal to the leftmost bit of the accumulator.

::

    XOR,    FIM     1P  11      / Register 2 = 0, Register 3 = 11
    L1,     LDM     0           / Get bit of Register 0, Set accumulator = 0
            XCH     0           / Set Register 0 to accumulator; Register 0 = 0
            RAL                 / Move first 'XOR' bit to carry
            XCH     0           / Save shifted data in Register 0, set accumulator = 0
            INC     3           / Done if Register 3 = 0
            XCH     3           / Register 3 to accumulator
            JCN     4   L2      / Return if accumulator = 0
            XCH     3           / Otherwise, restore accumulator and Register 3
            RAR                 / Bit of Register 0 is alone in the accumulator
            XCH     2           / Save first 'XOR' bit in Register 2
            LDM     0           / Get bit in Register 1, set accumulator = 0
            XCH     1           
            RAL                 / Move leftmost bit to carry
            XCH     1           / Save shifted data in Register 1
            RAR                 / Move second 'XOR' bit to carry
            ADD     2           / 'ADD' gives the 'XOR' of the bits in carry
            RAL                 / Otherwise, 'XOR' leftmost bit of the accumulator,
                                / transmit to carry by RAL
            JUN     L1          
    L2,     BBL     0           / Return to main program



