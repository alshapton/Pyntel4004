.. _hardware-machine-wrr:

WRR
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Write ROM Port
   * - Function
     - Write to a specified ROM port
   * - Syntax
     - WRR
   * - Assembled
     -
   * - Binary
     - 11100010
   * - Decimal
     - 226
   * - Hexadecimal
     - 0xE2
   * - Symbolic
     - .. image:: images/wrr-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - wrr_

.. rubric:: Detailed Description

The content of the accumulator is transferred to the ROM output port of the previously selected ROM chip.
The data is available on the output pins until a new WRR is executed on the same chip.
The LSB bit of the accumulator appears on I/O 0, (pin 16), of the 4001.

No operation is performed on I/O lines coded as inputs.

The carry bit and the accumulator are unchanged.


The opcode for this instruction does not contain any additional data:

.. image:: images/wrr.png
   :scale: 50%
   :align: center


.. rubric:: Example Program

The example program will write the value 15 to the output port associated with the 
ROM chip 2.

::

  / Example program
        FIM        4P  64
        SRC        4P
        LDM        15
        WRR


.. _wrr: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
