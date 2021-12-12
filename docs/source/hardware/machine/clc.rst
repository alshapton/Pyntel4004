.. _hardware-machine-clc:

CLC
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Clear Carry
   * - Function
     - Clear the carry bit
   * - Syntax
     - CLC
   * - Assembled
     -
   * - Binary
     - 11110001
   * - Decimal
     - 241
   * - Hexadecimal
     - 0xF1
   * - Symbolic
     - .. image:: images/clc-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Carry bit is reset
   * - Implemented
     - clc_

.. rubric:: Detailed Description

The carry bit is reset.

The opcode for this instruction does not contain any additional data:

.. image:: images/clc.png
   :scale: 50%
   :align: center


.. _clc: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
