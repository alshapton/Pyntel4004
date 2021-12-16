.. _hardware-machine-rar:

RAR
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Rotate Accumulator right through Carry
   * - Function
     - The content of the accumulator and carry/link are rotated right.
   * - Syntax
     - RAR
   * - Assembled
     -
   * - Binary
     - 11110110
   * - Decimal
     - 246
   * - Hexadecimal
     - 0xF6
   * - Symbolic
     - .. image:: images/rar-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - As described
   * - Implemented
     - rar_

.. rubric:: Detailed Description

The contents of the accumulator are rotated one bit position to the right.

The low-order bit of the accumulator replaces the carry bit, while the carry bit
replaces the high-order bit of the accumulator.

.. image:: images/rar-diag.png
   :scale: 50%
   :align: center

The opcode for this instruction does not contain any additional data:

.. image:: images/rar.png
   :scale: 50%
   :align: center


.. _rar: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
