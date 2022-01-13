.. _data_statements:

Data Statements
===============

.. include:: ../../global.rst

Any 4 bit character in DATA RAM contains one of the 16 possible combinations of zeros and ones.
Arithmetic instructions assume that the DATA RAM characters upon which they operate are in a 
special format called "two's complement", and the operations performed on these bytes are called 
"two's complement arithmetic" •

.. rubric:: Two's Complement

When a character is interpreted as a signed two's complement number, the low order 3 bits 
supply the magnitude of the number, while the high order bit is interpreted as the sign of 
the number (**0 for positive numbers**, **1 for negative**).

The range of positive numbers that can be represented in signed two's complement notation is,
therefore, from 0 to 7:

.. list-table:: 
   :header-rows: 1

   * - Decimal
     - Binary
   * - 0
     - 0000
   * - 1
     - 0001
   * - 2
     - 0010
   * - 3
     - 0011
   * - 4
     - 0100
   * - 5
     - 0101
   * - 6
     - 0110
   * - 7
     - 0111


To change the sign of a number represented in two's complement, the following rules are applied:

    1. Invert each bit of the number (producing the so-called one's complement).

    2. Add one to the result, ignoring any carry out of the high order bit position.

Example 1:

Produce the two's complement representation of -6 . Following the rules above:

::

        + 6             =   0 1 1 0
    Invert each bit     =   1 0 0 1
    Add 1               =   1 0 1 0

Therefore, the two' s complement representation of -6 is the hexadecimal number '0x0A'. 
(Note that the sign bit is set, indicating a negative number.)


Example 2: 

To interpret the value 0x0C as a signed two's complement number:

    -   The high order bit is set, indicating that this is a negative number. 
    -   To obtain its value, again invert each bit and add one. 

**This is equivalent to subtracting one f:um the number and inverting each bit.**

::

          C             =   1 1 0 0
    Invert each bit     =   0 0 1 1
    Add 1               =   0 1 0 0

Thus, the value of 0x0C is - 4.


The range of negative numbers that can be represented in signed two's complement notation is,
therefore, from -1 to -8:

.. list-table:: 
   :header-rows: 1

   * - Decimal
     - Binary
   * - -1
     - 1111
   * - -2
     - 1110
   * - -3
     - 1101
   * - -4
     - 1100
   * - -5
     - 1011
   * - -6
     - 1010
   * - -7
     - 1001
   * - -8
     - 1000

To perform the subtraction 6 - 3, the following operations are performed:

::
    
    -   Take the two's complement of 3  =   1 1 0 1 
    -   Add the result to the minuend:
                                     6  =   0 1 1 0
                                + (-3)  =   1 1 0 1
                                            -------
                                            0 0 1 1 = 3 


When a data character is interpreted as an unsigned two's complement number, 
its value is considered positive and in the range 0 to 15.

.. list-table:: 
   :header-rows: 1

   * - Decimal
     - Binary
   * - 0
     - 0000
   * - 1
     - 0001
   * - 2
     - 0010
   * - 3
     - 0011
   * - 4
     - 0100
   * - 5
     - 0101
   * - 6
     - 0110
   * - 7
     - 0111
   * - 8
     - 1000
   * - 9
     - 1001
   * - 10
     - 1010
   * - 11
     - 1011
   * - 12
     - 1100
   * - 13
     - 1101
   * - 14
     - 1110
   * - 15
     - 1111

Two's complement arithmetic is still valid. When performing an addition operation, 
the carry bit is set when the result is greater than 15. When performing subtraction, 
the carry bit is set when the result is positive. If the carry bit is reset, the 
result is negative and present in its two's complement form.

Example 1:

Subtract 3 from 10 using unsigned two's complement arithmetic.

::
    
    10  =   1 0 1 0 
    -3  =   1 1 0 1 
            -------
        1   0 1 1 1
    carry

    Since the carry bit is **set**, the result is correct and positive

Example 2:

Subtract 15 from 12 using unsigned two's complement arithmetic.

::
    
    12  =   1 1 0 0 
   -15  =   0 0 0 1
            -------
        0   1 1 0 1 = -3
    carry

    Since the carry bit is **reset**, the result is negative and in its two's compliment form.

-----

To summarise Two's complement, below is a number line showing all the 4-bit representations from +7 to -8.

.. list-table:: 
   :header-rows: 1

   * - Decimal
     - Binary
   * - 7
     - 0111
   * - 6
     - 0110
   * - 5
     - 0101
   * - 4
     - 0100
   * - 3
     - 0011
   * - 2
     - 0010
   * - 1
     - 0001
   * - 0
     - 0000
   * - -1
     - 1111
   * - -2
     - 1110
   * - -3
     - 1101
   * - -4
     - 1100
   * - -5
     - 1011
   * - -6
     - 1010
   * - -7
     - 1001
   * - -8
     - 1000


-----

**Why two's complement ?**

Using two's complement notation for negative numbers, any subtraction problem 
becomes a sequence of bit inversions and additions. Therefore, fewer circuits 
are needed to perform subtraction.