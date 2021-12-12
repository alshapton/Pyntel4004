.. _hardware-machine-ldm:

LDM
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Branch Back and Load
   * - Function
     - The 4 bits of immediate data encoded in the instruction are loaded |br|
       into the accumuator, then execution continues with the most recent address |br|
       on the stack.
       contents of the accumulator. The carry bit is not affected.
   * - Syntax
     - LDM(D)
   * - Assembled
     -
   * - Binary
     - 1100 DDDD
   * - Decimal
     - 208, then incrementing by 1 until 223 (1st word).
   * - Hexadecimal
     - 0xD0, then incrementing by 1 until 0xDF (1st word).
   * - Symbolic
     - .. image:: images/ldm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - ldm_

.. rubric:: Detailed Description

The 4 bits of immediate data are loaded into the accumulator.

The carry bit is not affected.

.. image:: images/ldm.png
   :scale: 50%
   :align: center


.. rubric:: Example Program

::

   / Example program
           ldm   0
           ldm   9
           ldm   15
           end     


The above program will first clear the accumulator (setting all 4 bits to 0), then load the value 9 into the accumulator, then finally, set all the accumulator's 4 bits by loading the value 15.

.. _bbl: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
