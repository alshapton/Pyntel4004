.. _hardware-machine-cmc:

CMC
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Complement Carry
   * - Function
     - The carry/link content is complemented.
   * - Syntax
     - CMC
   * - Assembled
     -
   * - Binary
     - 11110011
   * - Decimal
     - 243
   * - Hexadecimal
     - 0xF3
   * - Symbolic
     - .. image:: images/cmc-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Carry bit is complemented
   * - Implemented
     - cmc_

.. rubric:: Detailed Description

The contents of the carry is complemented, i.e. if the carry bit is 1, it is set 
to zero. If it is zero, it is set to 1.

The opcode for this instruction does not contain any additional data:

.. image:: images/cmc.png
   :scale: 50%
   :align: center


.. _cmc: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
