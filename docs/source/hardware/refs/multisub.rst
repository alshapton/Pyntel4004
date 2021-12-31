.. _hardware-machine-refs-multisub:

:orphan:

Multi-Digit Subtraction
=======================

.. include:: ../../global.rst

The carry bit may be used to add unsigned data quantities of arbitrary length.

.. rubric:: Consider the following subtraction of two 4-digit hexadecimal numbers:

::
 
                      5 4 B A
                      1 4 F 6 -
                      -------
                      3 F C 4


This subtraction may be performed by first setting the carry bit = 1. 
Then for each pair of digits, the program must complement the carry bit 
and perform the subtraction. By this process, the carry bit will adjust 
the differences, taking into account any borrows which may have occurred.
|br|
The process as applied to the above subtraction is as follows:

(1)   Set carry bit = 1
|br|
(2)   Complement carry bit (carry is now 0)
|br|
(3)   Subtract low order digits

::

                        A     1 0 1 0
                       ~6     1 0 0 1
                   ~carry           1
                              -------
                        1     0 1 0 0     =     0x04
                     carry 

|br|
(4)   Complement resulting carry bit (carry is now 0)
|br|
(5)   Subtract next digits

::

                        B     1 0 1 0
                       ~F     0 0 0 0
                   ~carry           1
                              -------
                        0     1 1 0 0     =     0x0C
                     carry 

|br|
(6)   Complement resulting carry bit (carry is now 1)
|br|
(7)   Subtract next digits

::

                        4     0 1 0 0
                       ~4     1 0 1 1
                   ~carry           0
                              -------
                        0     1 1 1 1     =     0x0F
                     carry 

|br|
(8)   Complement resulting carry bit (carry is now 1)
|br|
(9)   Subtract next digits

::

                        5     0 1 0 1
                       ~1     1 1 1 0
                   ~carry           0
                              -------
                        1     0 0 1 1     =     0x03
                     carry 


Thus, the correct result (0x3FC4) is obtained. 


The following subroutine will perform a sixteen digit subtraction, making these assumptions:


   * The two numbers to be subtracted are stored in DATA RAM chip 0, registers 0 and 1. 
   * Register 1 contains the subtrahend.
   * The numbers are stored with the least significant digit first (in character 0) .
   * The result will be stored least significant digit first in register 1 replacing the contents of register 1.
   * Index register 8 will count the number of digits (up to 16) which have been subtracted.


::

   SB,   FIM   2P    0     / REG PAIR 2P RAM CHIP 0 OF REG 0
         FIM   3P    16    / REG PAIR 3P RAM CHIP 0 OF REG 1 
         CLB               / SET CARRY = 0
         XCH   8           / SET DIGIT COUNTER = 0
         STC               / SET CARRY = 1
   SB1,  CMC               / COMPLEMENT CARRY BIT
         SRC   2P          / SELECT RAM REG 0
         RDM               / READ DIGIT TO ACCUMULATOR
         SRC   3P          / SELECT RAM REG 1
         SBM               / SUBTRACT DIGIT + CARRY FROM ACCUMULATOR
         WRM               / WRITE RESULT TO REG 1
         INC   5           / ADDRESS NEXT CHARACTER OF RAM REG 0
         INC   7           / ADDRESS NEXT CHARACTER OF RAM REG 1
         ISZ   8  SB1      / BRANCH IF DIGIT COUNTER < 16 (NON ZERO)
   OV,   BBL   0


When location "OV" is reached, RAM register 1 will contain the difference of the two 16 digit 
numbers arranged from low order digit to high order digit. 

.. note:: Carry Bit

      The carry bit from the previous subtraction is complemented by the **CMC** instruction each time through the loop.

