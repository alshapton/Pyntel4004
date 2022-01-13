.. _hardware-machine-ral:

RAL
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Rotate Accumulator left through Carry
   * - Function
     - The content of the accumulator and carry/link are rotated left.
   * - Syntax
     - RAL
   * - Assembled
     -
   * - Binary
     - 11110101
   * - Decimal
     - 245
   * - Hexadecimal
     - 0xF5
   * - Symbolic
     - .. image:: images/ral-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - As described
   * - Implemented
     - ral_

.. rubric:: Detailed Description

The contents of the accumulator are rotated one bit position to the left.

The high-order bit of the accumulator replaces the carry bit,
while the carry bit replaces the low-order bit of the accumulator as shown in the example below:

.. image:: images/ral-diag.png
   :scale: 50%
   :align: center

The opcode for this instruction does not contain any additional data:

.. image:: images/ral.png
   :scale: 50%
   :align: center


.. _ral: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
