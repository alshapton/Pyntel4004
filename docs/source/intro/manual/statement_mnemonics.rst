.. _statement_mnemonics:

Statement Mnemonics
===================

.. include:: ../../global.rst

Assembly language instructions must adhere to a fixed set of rules as described here. |br|
An instruction has four separate and distinct parts or **FIELDS**.
|br|

|just|

.. list-table:: 
   :header-rows: 1

   * - Field
     - Name
     - Description
   * - 1
     - LABEL
     - It is the instruction location's label or name, and it is used to |br| reference the instruction.
   * - 2
     - CODE
     - It defines the operation that is to be performed by the instruction.
   * - 3
     - OPERAND
     -  It provides any address or data information needed by the |br| CODE field.
   * - 4
     - COMMENT
     - It is present for the programmer's convenience and is ignored by the |br| assembler. The programmer uses comment fields to describe the |br| operation and thus make the program more readable.


The assembler uses free fields; that is, any number of blanks may separate fields.

Some examples are shown below:

::

        CMI     CLB             / Clear accumulator and carry

        LAB,    INC     3       / Increment register 3

                JUN     CMI     / Jump to instruction labelled "CMI"

        FCH,    FIM     0P 255  / Load 0xFF (decimal 255) into register pair 0
