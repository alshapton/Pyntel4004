.. _hardware-machine-tcs:

TCS
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Transmit Carry and Subtract
   * - Function
     - The accumulator is set to 9 if the carry/link is 0. |br|
       The accumulator is set to 10 if the carry/link is a 1. |br|
       The carry/link is set to 0.
   * - Syntax
     - TCS
   * - Assembled
     -
   * - Binary
     - 11111001
   * - Decimal
     - 249
   * - Hexadecimal
     - 0xF9
   * - Symbolic
     - .. image:: images/tcs-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Carry bit is reset
   * - Implemented
     - tcs_

.. rubric:: Detailed Description


If the carry bit = 0, the accumulator is set to 9. |br|
If the carry bit = 1, the accumulator is set to 10. |br|

In either case, the carry bit is then reset.

The opcode for this instruction does not contain any additional data:

.. image:: images/tcs.png
   :scale: 50%
   :align: center


This instruction is used when subtracting decimal numbers greater than 4 bits in length.
For an example of this, see :ref:`here <hardware-machine-refs-decsub>`

.. _tcs: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
