.. _hardware-machine-wrn:

WRn
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Write Data Ram Status Character
   * - Function
     - The content of the accumulator is written into the |br|
       RAM status character n of the previously selected RAM register.
   * - Syntax
     - WR0, WR1, WR2, WR3
   * - Assembled
     -
   * - Binary
     - 11100100, 11100101, 11100110, 11100111, 
   * - Decimal
     - 228, 229, 230, 231
   * - Hexadecimal
     - 0xE4, 0xE5, 0xE6, 0xE7
   * - Symbolic
     - .. image:: images/wrn-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - wrn_

.. rubric:: Detailed Description

The contents of the DATA RAM status character whose number from 0 to 3 is
specified by n, associated with the DATA RAM register specified by tbe 
last SRC instruction, are replaced by the contents of the accumulator.

The carry bit and the accumulator are not affected.

The DATA RAM status character is encoded in the opcode as shown below:

.. image:: images/wrn.png
   :scale: 50%
   :align: center


.. rubric:: Example program

The example program will write the value 2 into status character 1 of DATA RAM 
register 0 of chip 0 of the currently selected DATA RAM bank.

::

    / Example program
    FIM   0P  0
    SRC   0P
    LDM   2
    WR1



.. _wrn: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
