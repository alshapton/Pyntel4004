.. _hardware-machine-wrm:

WRM
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Write accumulator into RAM character
   * - Function
     - The accumulator content is written into the previously selected RAM |br|
       main memory character location. The accumulator and carry/link are unaffected.
   * - Syntax
     - WRM
   * - Assembled
     -
   * - Binary
     - 11100000
   * - Decimal
     - 224
   * - Hexadecimal
     - 0xE0
   * - Symbolic
     - .. image:: images/wrm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - wrm_

.. rubric:: Detailed Description

The contents of the accumulator are written into the DATA RAM data character specified by the last SRC 
instruction.

The carry bit and the accumulator are not affected.

The opcode for this instruction does not contain any additional data:

.. image:: images/wrm.png
   :scale: 50%
   :align: center


.. rubric:: Example program

The example program will cause the DATA RAM data character number 4 of register 3 of chip 2 of
the DATA RAM bank selected by the last DCL instruction to contain 15 (1111b).

::

  / Example program
          FIM   0P  180
          SRC   0P
          LDM   15
          WRM


.. _wrm: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
