.. _hardware-machine-refs-decadd:

:orphan:

Decimal Addition
================

.. include:: ../../global.rst

Each 4 bit data quantity may be treated as a decimal number as long as it represents
one of the decimal digits from 0 through 9, and does not contain any of the
bit patterns representing the hexadecimal digits A through F. 

In order to preserve this decimal interpretation when perfonning addition, 
the value 6 must be added to the accumulator whenever an addition produces a result 
between 10 and 15. This is because each 4 bit data quantity can hold 6 more combinations
of bits than there are decimal digits.

The DAA (decimal adjust accumulator) instruction is provided for this purpose. 
Also, to permit addition of multi-digit decimal numbers, the DAA adds 6 to the accumulator 
whenever the carry bit is set indicating a decimal carry from previous additions. 
The carry bit is unaffected unless the addition of 6 produces a carry,
in which case the carry bit is set.


.. rubric:: Example: Perform the decimal addition

::
 
                      4 6 9
                      3 2 9 +
                        ---
                      7 9 8


1       Clear the carry and add the lowest-order digits

::
        
                   9  =   1 0 0 1
                   9  =   1 0 0 1
              Carry   =         0
                        ---------
        Result            0 0 1 0
        Carry       1


2       Perform a DAA operation, which will add 6 to the accumulator. Since no carry is produced by this operation, the carry bit is left unaffected (i.e. 1)

::
        
         Accumulator  =   0 0 1 0
                   6  =   0 1 1 0
              Carry   =         0
                        ---------
        Result            1 0 0 0 = 8
        Carry       1               
        
        (since the DAA produced no carry, the bit is unaffected)


3       Add the next two digits

::
        
                   6  =   0 1 1 0
                   2  =   0 0 1 0
              Carry   =         1
                        ---------
        Result            1 0 0 1 = 9
        Carry       0


4      Perform a DAA operation. Since the accumulator is not greater than 9, and the carry is not set, then no action occurs.

5      Add the next two digits

::
        
                   4  =   0 1 0 0
                   3  =   0 0 1 1
              Carry   =         0
                        ---------
        Result            0 1 1 1 = 7
        Carry       0

6       Perform a DAA operation. Again, no action occurs. Thus, the correct result (798) is generated in three 4-bit data characters.


.. rubric:: Example Code (subroutine)

A subroutine which adds two 16 digit decimal numbers can be found :ref:`here <hardware-machine-refs-multiadd>`:
