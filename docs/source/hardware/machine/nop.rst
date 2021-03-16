No Operation
************

.. list-table:: Information
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
     - `machine`_

Example program
***************
::

    / Example program
            org    ram
            nop
            end

The program does nothing, since the NOP operation is the only operator in the program.

Notes
******

The NOP instruction is useful for padding out memory positions for those operators that function differently at the page boundary, such that they do not end at a page boundary. 

.. |mu| replace:: :math:`{\mu}`
.. _machine: https://github.com/alshapton/Pyntel4004/blob/main/pyntel4004/src/hardware/machine.py
