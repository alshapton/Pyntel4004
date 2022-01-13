.. _instruction_summary:

Instruction Summary
===================

.. include:: ../../global.rst

.. toctree::
   :hidden:

   index_register_instructions
   index_register_to_accumulator_instructions
   accumulator_instructions
   immediate_instructions
   transfer_of_control_instructions
   subroutine_linkage_instructions
   nop_instructions
   memory_selection_instructions
   io_and_ram_instructions

This is a summary of 4004 instructions. |br|

Abbreviations used are as follows:

.. list-table:: 
   :header-rows: 1

   * - Abbreviation
     - Description
   * - A
     - Accumulator.
   * - A :subscript:`n`
     - Bit n in the accumulator, where n may have any value from 0 to 3.
   * - ADDR
     - A read-only memory or program random-access memory address.
   * - carry
     - The carry bit.
   * - PC
     - The 12-bit Program Counter.
   * - PCH
     - The high-order 4 bits of the Program Counter.
   * - PCL
     - The low-order 4 bits of the Program Counter.
   * - PCM
     - The middle 4 bits of the Program Counter.
   * - RAM
     - Random Access Memory.
   * - REG
     - Any index register from 0 to 15.
   * - R0
     - Index Register 0.
   * - R1
     - Index Register 1.
   * - ROM
     - Read Only Memory.
   * - RP
     - Any index register pair from 0P to 7P.
   * - STK
     - The address stack
   * - .. image:: images/complement-value.png
          :scale: 50%
     - The number obtained by complementing each bit of "value".
   * - X:Y
     - The value obtained by concatenating the values X and Y.
   * - [   ]
     - An optional field enclosed by brackets.     
   * - (   )
     - Contents of register or memory enclosed by parentheses.  
   * - .. image:: images/left-arrow.png
          :scale: 50%
     - Replace value on left hand side of arrow with value on right hand side.

.. list-table:: Instruction Summary
   :header-rows: 1

   * - Group
     - Definition
   * - :ref:`Index Register Instructions <index_register_instructions>`
     - Instructions which involve index registers or |br| register pairs.
   * - :ref:`Index Register to Accumulator Instructions <index_register_to_accumulator_instructions>`
     - Instructions which involve an operation between |br| an index register and the accumulator. |br| Instructions in this class occupy one byte.
   * - :ref:`Accumulator Instructions <accumulator_instructions>`
     - Instructions which operate only on the contents |br| of the accumulator and/or the carry bit. |br| Instructions in this class occupy one byte.
   * - :ref:`Immediate Instructions <immediate_instructions>`
     - Instructions which use data that is part of the |br| instruction itself.
   * - :ref:`Transfer Of Control Instructions <transfer_of_control_instructions>`
     - Instructions which alter the normal execution |br| sequence of instructions.
   * - :ref:`Subroutine Linkage Instructions <subroutine_linkage_instructions>`
     - Instructions which call and cause return from |br| subroutines. |br| They cause a transfer of program control and |br| use the address stack.
   * - :ref:`No-Operation Instruction <nop_instructions>`
     - This instruction occupies one byte.
   * - :ref:`Memory Selection Instructions <memory_selection_instructions>`
     - Instructions which specify DATA RAM data and |br| status characters, RAM output ports and ROM |br| input and output ports to be |br| operated on by I/O and RAM instructions
   * - :ref:`Input/Output and RAM Instructions <io_and_ram_instructions>`
     - Instructions which access DATA RAM |br| characters or perform input or output |br| operations. |br| One instruction, WPM, allows the programmer |br| to read or write 8-bit program RAM locations. |br| These instructions use addresses selected by |br| the DCL and SRC instructions.
 
