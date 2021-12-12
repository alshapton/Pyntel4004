.. _hardware-machine-clb:

CLB
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Clear Both
   * - Function
     - Clear both the accumulator and carry bit
   * - Syntax
     - CLB
   * - Assembled
     -
   * - Binary
     - 11110000
   * - Decimal
     - 240
   * - Hexadecimal
     - 0xF0
   * - Symbolic
     - .. image:: images/clb-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Carry bit and Accumulator are zeroed
   * - Implemented
     - clb_

.. rubric:: Detailed Description

The accumulator is set to 0 and the carry bit is reset.

The opcode for this instruction does not contain any additional data:

.. image:: images/clb.png
   :scale: 50%
   :align: center


.. _clb: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
