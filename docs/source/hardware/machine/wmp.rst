.. _hardware-machine-wmp:

WMP
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Write RAM Port
   * - Function
     - Write to a specified RAM port
   * - Syntax
     - WMP
   * - Assembled
     -
   * - Binary
     - 11100001
   * - Decimal
     - 225
   * - Hexadecimal
     - 0xE1
   * - Symbolic
     - .. image:: images/wmp-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - wmp_

.. rubric:: Detailed Description

The contents of the accumulator are written to the output port associated with the DATA RAM
chip selected by the last SRC instruction. 
The data is available on the output pins until a new WMP is executed on the same RAM chip.
The LSB bit of the accumultor appears on O0, (Pin 16), of the 4002.

The carry bit and the accumulator are unchanged.

The opcode for this instruction does not contain any additional data:

.. image:: images/wmp.png
   :scale: 50%
   :align: center


.. rubric:: Example Program

The example program will write the value 6 to the output port associated with the 
DATA RAM chip 2 of the currently selected DATA RAM bank.

::

  / Example program
        FIM        3P  64
        SRC        3P
        LDM        6
        WMP

.. _wmp: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
