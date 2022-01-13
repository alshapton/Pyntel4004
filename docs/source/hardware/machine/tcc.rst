.. _hardware-machine-tcc:

TCC
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Transmit Carry and Clear
   * - Function
     - The accumulator is cleared. The least significant position of the accumulator |br|
       is set to the value of the carry/link. The carry/link is set to 0.
   * - Syntax
     - TCC
   * - Assembled
     -
   * - Binary
     - 11110111
   * - Decimal
     - 247
   * - Hexadecimal
     - 0xF7
   * - Symbolic
     - .. image:: images/tcc-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Carry bit is reset
   * - Implemented
     - tcc_

.. rubric:: Detailed Description


If the carry bit is zero, the accumulator is set to 0000.
If the carry bit is one, the accumulator is set to 0001. |br|

In either case, the carry bit is then reset.

The opcode for this instruction does not contain any additional data:

.. image:: images/tcc.png
   :scale: 50%
   :align: center


<<<<<<< HEAD
.. _stc: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
=======
.. _tcc: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
>>>>>>> release/0.0.1-beta.3
