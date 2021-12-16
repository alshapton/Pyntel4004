.. _hardware-machine-nop:

NOP
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - No Operation
   * - Function
     - No operation performed
   * - Syntax
     - NOP
   * - Assembled
     -
   * - Binary
     - 0000 0000
   * - Decimal
     - 0
   * - Hexadecimal
     - 0x00
   * - Symbolic
     - Not Applicable
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - nop_

.. rubric:: Description

No operation is performed.
The program counter is incremented by one and execution continues with the next sequential instruction.

.. rubric:: Example program

::

    / Example program
            org    ram
            nop
            end

The program does nothing, since the NOP operation is the only operator in the program.

.. rubric:: Notes


The NOP instruction is useful for padding out memory positions for those operators that function differently at the page boundary, such that they do not end at a page boundary.


.. _nop: https://github.com/alshapton/Pyntel4004/blob/4ed95ca321cd0e9f19a89ef0ebea2b0ebe52952c/pyntel4004/src/hardware/machine.py#L54
