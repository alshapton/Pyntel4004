.. _hardware-machine-kbp:

KBP
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Keyboard Process
   * - Function
     - If the accumulator contains OOOOB, it remains unchanged. |br|
       If one bit of the accumulator is set, the accumulator is set to |br|
       a number from 1 to 4 indicating which bit was set.
   * - Syntax
     - KBP
   * - Assembled
     -
   * - Binary
     - 11111100
   * - Decimal
     - 252
   * - Hexadecimal
     - 0xFC
   * - Symbolic
     - .. image:: images/kbp-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - kbp_

.. rubric:: Detailed Description

A code conversion is performed on the accumulator content, from 1 out of n to binary code.
If the accumulator content has more than one bit on, the accumulator will be set to 15 
(to indicate error). The carry/link is unaffected.

The conversion table is shown below:

.. list-table::
   :widths: 50 50
   :header-rows: 1


   * - Accumulator |br| before KBP
     - Accumulator |br| after KBP
   * - 0000
     - 0000
   * - 0001
     - 0001
   * - 0010
     - 0010
   * - 0100
     - 0011
   * - 1000
     - 0100
   * - 0011
     - 1111
   * - 0101
     - 1111
   * - 0110
     - 1111
   * - 0111
     - 1111
   * - 1001
     - 1111
   * - 1010
     - 1111
   * - 1011
     - 1111
   * - 1100
     - 1111
   * - 1101
     - 1111
   * - 1110
     - 1111
   * - 1111
     - 1111

The opcode for this instruction does not contain any additional data:

.. image:: images/kbp.png
   :scale: 50%
   :align: center


.. _kbp: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
