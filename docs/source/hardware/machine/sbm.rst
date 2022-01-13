.. _hardware-machine-sbm:

SBM
===

.. include:: ../../global.rst

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Subtract DATA RAM from memory with borrow
   * - Function
     - The content of the previously selected RAM character is subtracted |br|
       from the accumulator with borrow.
   * - Syntax
     - SBM
   * - Assembled
     -
   * - Binary
     - 11101000
   * - Decimal
     - 232
   * - Hexadecimal
     - 0xE8
   * - Symbolic
     - .. image:: images/sbm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - Depending on the result, the carry bit is reset or set.
   * - Implemented
     - sbm_

.. rubric:: Detailed Description

The value of the DATA RAM character specified by the last SRC instruction is subtracted
from the accumulator with borrow. The data character is unaffected. 
A borrow from the previous subtraction is indicated by the carry bit being equal to one 
at the beginning of this instruction. 
No borrow from the previous subtraction is indicated by the carry bit being equal to zero
at the beginning of this instruction.
This instruction sets the carry bit if the result generates no borrow, 
and resets the carry bit if the result generates a borrow.
The subtract with borrow operation is actually performed by complementing each bit of the 
data character and adding the resulting value plus the complement of the carry bit
to the accumulator.

.. rubric:: Notes

This instruction may be used to subtract numbers greater than 4 bits in length. 
The carry bit must be complemented by the program between each required subtraction operation. 
For an example of this, see :ref:`"Decimal Subtraction" <hardware-machine-refs-decsub>`:.

The opcode for this instruction does not contain any additional data:

.. image:: images/sbm.png
   :scale: 50%
   :align: center

.. rubric:: Example

In order to perform a normal subtraction, the carry bit should be zero. 

Assume the carry bit is 1, the accumulator contains 7, and the DATA RAM character 1 of
register 0 of chip 0 contains 5, the SBM will perform the following operation:

::

    / Example
            FIM   1P    1
            SRC   1P
            SBM

The `sbm` operation above is carried out as follows:

::

        Accumulator   =   0 1 1 1
  ~  Data Character   =   1 0 1 0    ( Character = 0 1 0 1)
  ~  Carry            =         0    ( carry = 1)
                          -------
        Result      0     0 0 0 1  
                Carry indicates a borrow

The accumulator contains 1 and the carry bit is reset.

.. _sbm: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
