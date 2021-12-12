.. _hardware-machine-stc:

STC
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Set Carry
   * - Function
     - Set the carry bit
   * - Syntax
     - STC
   * - Assembled
     -
   * - Binary
     - 11111010
   * - Decimal
     - 250
   * - Hexadecimal
     - 0xFA
   * - Symbolic
     - .. image:: images/stc-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Carry bit is set
   * - Implemented
     - stc_

.. rubric:: Detailed Description

The carry bit is set.

The opcode for this instruction does not contain any additional data:

.. image:: images/stc.png
   :scale: 50%
   :align: center


.. _stc: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
