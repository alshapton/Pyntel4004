.. _hardware-machine-refs-multiadd:

:orphan:

Multi-Digit Addition
====================

.. include:: ../../global.rst

The carry bit may be used to add unsigned data quantities of arbitrary length.

.. rubric:: Consider the following addition of two 4-digit hexadecimal numbers:

::
 
                      3 8 1 C
                      6 9 F 2 +
                      -------
                      A 2 0 E


This addition may be performed by setting the carry bit = 1, then adding the two 
low-order digits of the numbers, then adding the resulting carry to the two next 
higher order digits, and so on:


.. image:: images/multiadd-diag1.png
   :scale: 50%
   :align: center


The following subroutine will perform a sixteen digit addition, making these assumptions:

- The two numbers to be added are stored in DATA RAM chip 0, registers 0 and 1. 
- The numbers are stored with the least significant digit first (in character 0) .
- The result will be stored least significant digit first in register 1 replacing the contents of register 1.
- Index register 8 will count the number of digits (up to 16) which have been added.

::
        
                   9  =   1 0 0 1
                   9  =   1 0 0 1
              Carry   =         0
                        ---------
        Result            0 0 1 0
        Carry       1


::

   AD,   FIM   2P    0     / REG PAIR 2P RAM CHIP 0 OF REG 0
         FIM   3P    16    / REG PAIR 3P RAM CHIP 0 OF REG 1 
         CLB               / SET CARRY = 0
         XCH   8           / SET DIGIT COUNTER = 0
   AD1,  SRC   2P          / SELECT RAM REG 0
         RDM               / READ DIGIT TO ACCUMULATOR
         SRC               / SELECT RAM REG 1
         ADM               / ADD DIGIT + CARRY TO ACCUMULATOR
         WRM               / WRITE RESULT TO REG 1
         INC   5           / ADDRESS NEXT CHARACTER OF RAM REG 0
         INC   7           / ADDRESS NEXT CHARACTER OF RAM REG 1
         ISZ   8  AD1      / BRANCH IF DIGIT COUNTER < 16 (NON ZERO)
   OVR,  BBL   0


When location `OVR` is reached, RAM register 1 will contain the sum of the two 16 digit 
numbers arranged from low order digit to high order digit. 
The reason multi-digit numbers are arranged this way is that it is easier to add numbers
from low order to high order digit, and it is easier to increment addresses than to 
decrement them.

The first time through the program loop, index register pair 2 (index register 4 and 5)
contains 0 and index register pair 3 (index registers 6 and 7) contains 16, referencing 
the first data characters of DATA RAM registers 0 and 1, respectively.

On succeeding repititions of the loop, index registers 5 and 7 are incremented, 
referenecing sequential data characters, until all 16 digits have been added.

.. image:: images/multiadd-diag2.png
   :scale: 50%
   :align: center

A variant of the subroutine is below - this time for an arbitary number of 16 digit numbers.
The only difference is the addition of an DAA instruction. 

::

   AD,   FIM   2P    0     / REG PAIR 2P RAM CHIP 0 OF REG 0
         FIM   3P    16    / REG PAIR 3P RAM CHIP 0 OF REG 1 
         CLB               / SET CARRY=0
         XCH   8           / SET DIGIT COUNTER = 0
   AD1,  SRC   2P          / SELECT RAM REG 0
         RDM               / READ DIGIT TO ACCUMULATOR
         SRC               / SELECT RAM REG 1
         ADM               / ADD DIGIT + CARRY TO ACCUMULATOR
         DAA               / ADJUST FOR DECIMAL
         WRM               / WRITE RESULT TO REG 1
         INC   5           / ADDRESS NEXT CHARACTER OF RAM REG 0
         INC   7           / ADDRESS NEXT CHARACTER OF RAM REG 1
         ISZ   8  AD1      / BRANCH IF DIGIT COUNTER < 16 (NON ZERO)
   OVR,  BBL   0
