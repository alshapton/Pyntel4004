.. _hardware-machine-ld:

LD
==

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Load index register to Accumulator
   * - Function
     - The 4 bit content of the designated index register (RRRR) is loaded into accumulator. |br|
       The previous contents of the accumulator are lost. |br|
       The 4 bit content of the index register and the carry/link bit are unaffected..
   * - Syntax
     - LD(R)
   * - Assembled
     -
   * - Binary
     - 1010 RRRR
   * - Decimal
     - 160, then incrementing by 1 until 175 (1st word).
   * - Hexadecimal
     - 0xA0, then incrementing by 1 until 0xAF (1st word).
   * - Symbolic
     - .. image:: images/ld-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - ld_

.. rubric:: Detailed Description

The contents of REG are stored into the accumulator, replacing the previous contents
of the accumulator. The contents of REG are unchanged. 

The carry bit and the accumulator are not affected.

.. image:: images/ld.png
   :scale: 50%
   :align: center


.. rubric:: Example program

The example program will load the contents of register 11 into the accumulator.

If register 11 contains the value 9 (1001b), then after this program is executed,
the accumulator will contain 9 also.

::

    / Example program
    LD    11
    END



.. _ld: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
