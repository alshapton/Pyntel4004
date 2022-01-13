.. _hardware-machine-daa:

DAA
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Decimal Adjust Accumulator
   * - Function
     - If the contents of the accumulator are greater than 9, or if |br|
       the carry bit = 1, the accumulator is incremented by 6. |br|
       Otherwise, the accumulator is not affected.
   * - Syntax
     - DAA
   * - Assembled
     -
   * - Binary
     - 11111011
   * - Decimal
     - 251
   * - Hexadecimal
     - 0xFB
   * - Symbolic
     - .. image:: images/daa-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - As Described
   * - Implemented
     - daa_

.. rubric:: Detailed Description

If the contents of the accumulator are greater than 9, or if
the carry bit = 1, the accumulator is incremented by 6. 

Otherwise, the accumulator is not affected.

If the result of incrementing the accumulator produces a 
carry out of the high order bit position, the cary bit is set. 

Otherwise the carry bit is unaffected (**in particular it is not reset**).

.. rubric:: Notes

This instruction is used when adding decimal numbers. 
For an example of this see :ref:`Decimal Addition <hardware-machine-refs-decadd>`:

The opcode for this instruction does not contain any additional data:

.. image:: images/daa.png
   :scale: 50%
   :align: center


.. _daa: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
