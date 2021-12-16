.. _hardware-machine-dac:

DAC
===

.. include:: ../../global.rst

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Decrement accumulator
   * - Function
     - The content of the accumulator is decremented by 1.
   * - Syntax
     - DAC
   * - Assembled
     -
   * - Binary
     - 11111000
   * - Decimal
     - 248
   * - Hexadecimal
     - 0xF8
   * - Symbolic
     - .. image:: images/dac-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - No borrow sets the carry/link to 1; |br|
       Borrow sets the carry/link to a 0.
   * - Implemented
     - iac_

.. rubric:: Detailed Description

The contents of the accumulator are decremented by one. 
The carry bit is set if there is no borrow out of the high-order bit position,
and reset if there is a borrow.

.. rubric:: Note

Subtracting a number is carried out using the complement of the number and adding.
Therefore subtracting 1 becomes adding -1.


The opcode for this instruction does not contain any additional data:

.. image:: images/iac.png
   :scale: 50%
   :align: center

.. rubric:: Examples

Example 1

If the accumulator contains 9, then the DAC operation will be as follows:

::

     Accumulator   =   1 0 0 1
         + (-1)        1 1 1 1 
                      ---------
      Result      1    1 0 0 0
                Carry (indicating no borrow)


Example 2

If the accumulator contains 0, then the DAC operation will be as follows:

::

     Accumulator   =   0 0 0 0
         + (-1)        1 1 1 1 
                      ---------
      Result      0    1 1 1 1 
                Carry (indicating a borrow)

.. _iac: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
