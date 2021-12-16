.. _hardware-machine-iac:

IAC
===

.. include:: ../../global.rst

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Increment accumulator
   * - Function
     - The content of the accumulator is incremented by 1.
   * - Syntax
     - IAC
   * - Assembled
     -
   * - Binary
     - 11110010
   * - Decimal
     - 242
   * - Hexadecimal
     - 0xF2
   * - Symbolic
     - .. image:: images/iac-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - No overflow sets the carry/link to 0; |br|
       Overflow sets the carry/link to a 1.
   * - Implemented
     - iac_

.. rubric:: Detailed Description

The contents of the accumulator are incremented by one. 
The carry bit is set if there is a carry out of the high order bit position,
and reset if there is no carry.

The opcode for this instruction does not contain any additional data:

.. image:: images/iac.png
   :scale: 50%
   :align: center

.. rubric:: Examples

Example 1

If the accumulator contains 9, then the IAC operation will be as follows:

::

     Accumulator   =   1 0 0 1
              +              1 
                      ---------
      Result      0    1 0 1 0
                Carry 


Example 2

If the accumulator contains 15, then the IAC operation will be as follows:

::

     Accumulator   =   1 1 1 1
              +              1 
                      ---------
      Result      1    0 0 0 0
                Carry 

.. _iac: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
