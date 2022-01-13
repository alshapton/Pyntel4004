.. _hardware-machine-cma:

CMA
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Complement Accumulator
   * - Function
     - Perform one's complement on the accumulator
   * - Syntax
     - CMA
   * - Assembled
     -
   * - Binary
     - 11110100
   * - Decimal
     - 244
   * - Hexadecimal
     - 0xF4
   * - Symbolic
     - .. image:: images/cma-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - N/A
   * - Implemented
     - cma_

.. rubric:: Detailed Description

The contents of the carry is complemented, i.e. if the carry bit is 1, it is set 
to zero. If it is zero, it is set to 1.

The opcode for this instruction does not contain any additional data:

.. image:: images/cma.png
   :scale: 50%
   :align: center


.. _cma: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
