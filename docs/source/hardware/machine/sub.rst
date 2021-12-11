.. _hardware-machine-sub:

SUB
===

.. include:: ../../global.rst

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Subtract index register from accumulator with borrow
   * - Function
     - Subtract a value in an index register from the accumulator, |br|
       respecting the carry flag.
   * - Syntax
     - SUB R
   * - Assembled
     -
   * - Binary
     - 1001 R
   * - Decimal
     - 144, then incrementing by 1 until 159
   * - Hexadecimal
     - 0x90, then incrementing by 1 until 0x9F
   * - Symbolic
     - .. image:: images/sub-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - Depending on the result, the carry bit is reset or set.
   * - Implemented
     - sub_

.. rubric:: Detailed Description

The contents of index register R are subtracted with borrow from the accumulator. 
The result is kept in the accumulator; the contents of R are unchanged. 
A borrow from the previous subtraction is indicated by the carry bit being equal to one at
the beginning of this instruction. 
If the carry bit equals zero at the beginning of this instruction it is assumed that no 
borrow occurred from the previous subtraction.

This instruction sets the carry bit if there is no borrow out of the high order bit position, 
and resets the carry bit if there is a borrow.

The subtract with borrow operation is actually performed by complementing each bit of 
the contents of R and adding the resulting value plus the complement of the carry bit 
to the accumulator.

.. rubric:: Notes

This instruction may be used to subtract numbers greater than 4 bits in length. 
The carry bit must be complemented by the program between each required subtraction operation. 
For an example of this, see :ref:`"Decimal Subtraction" <hardware-machine-refs-decsub>`:.

The disassembly of the instruction below shows how the register is represented in the opcode:

.. image:: images/sub.png
   :scale: 50%
   :align: center

.. rubric:: Example programs

In order to perform a normal subtraction, the carry bit should be zero. 
If the accumulator contains 6, register 10 contains 2, and the carry bit is zero. 

This is the set-up for the operation `6 - 2`, giving the answer `4` in the accumulator.

::

    / Example program 1
            org    ram
            ldm    2
            xch    10
            ldm    6  
            clc
            sub    10
            end

The `sub` operation above is carried out as follows:

::

     Accumulator   =   0 1 1 0
  ~  Register 10   =   1 1 0 1    ( register 10 = 0 0 1 0)
  ~  Carry         =         1    ( carry = 0)
                      ---------
      Result      1     0 1 0 0  
                Carry indicates no borrow

The accumulator contains 4 and the carry bit is reset.

In this second example, if the accumulator contains 6, register 10 contains 2, and the carry bit is one:

::

    / Example program 2 
            org    ram
            ldm    2
            xch    10
            ldm    6  
            stc
            sub    10
            end

The `sub` operation above is carried out as follows:

::

     Accumulator   =   0 1 1 0
  ~  Register 10   =   1 1 0 1    ( register 10 = 0 0 1 0)
  ~  Carry         =         0    ( carry = 1)
                      ---------
      Result      1     0 0 1 1  
                Carry indicates no borrow

The accumulator contains 3 and the carry bit is reset.

.. _sub: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
