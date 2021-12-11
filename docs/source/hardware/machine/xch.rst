.. _hardware-machine-xch:

XCH
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Exchange index register and accumulator
   * - Function
     - The contents of the register specified by REG are exchanged with the |br|
       contents of the accumulator. The carry bit is not affected.
   * - Syntax
     - XCH(R)
   * - Assembled
     -
   * - Binary
     - 1011 RRRR
   * - Decimal
     - 176, then incrementing by 1 until 191 (1st word).
   * - Hexadecimal
     - 0xB0, then incrementing by 1 until 0xBF (1st word).
   * - Symbolic
     - .. image:: images/xch-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - xch_

.. rubric:: Detailed Description

The contents of the register specified by REG are exchanged with the |br|
contents of the accumulator. The carry bit is not affected.

.. image:: images/xch.png
   :scale: 50%
   :align: center


.. rubric:: Example program

If the accumulator contains 1100 and register 0 contains 0011 then the instruction
XCH 0 will cause the accumulator to contain 0011 and register 0 to contain 1100.

::

    / Example program
    XCH   0
    END

.. rubric:: Note

ACBR is the **Accumulator Buffer Register (4-bit)**

.. _xch: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
