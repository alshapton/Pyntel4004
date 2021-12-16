.. _hardware-machine-jms:

JMS
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Jump to Subroutine
   * - Function
     - Jump to a subroutine.
   * - Syntax
     - JMS (address)
   * - Assembled
     -
   * - Binary
     - 0101AAAA AAAAAAAA
   * - Decimal
     - 80, then incrementing by 1 until 95 (1st word)
   * - Hexadecimal
     - 0x50, then incrementing by 2 until 0x5F (1st word)
   * - Symbolic
     - .. image:: images/jun-sym.png
          :scale: 50%
   * - Execution
     - 2 words 16-bit code and an execution time of 21.6 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - jms_


.. rubric:: Detailed Description

The address of the instruction immediately following the JMS is written to
the address stack for later use by a BBL instruction.
Program execution continues at memory address ADDR, which may be on any page.

The carry bit is not affected.

The disassembly of the instruction below shows how the register pair is
represented in the opcode.

.. image:: images/jms.png
  :scale: 50%
  :align: center


This instruction and the JUN instruction , use a 12-bit address, and can
reference any memory location. Their operation is not influenced by their
position within a page of memory, whereas some other instructions are.

Therefore, only a **JUN** or **JMS** instruction should be used to transfer control
from one page of memory to another.

.. _jms_ref1:

.. rubric:: Example program snippet for illustration

::

          jms lab
          xch 0


  lab,    inc 1


          bbl 6

Normally, program instructions are executed sequentially.

A 12-bit register called the **program counter** holds the address of the
instruction to be executed. The JMS instruction replaces the program counter
contents, causing program execution to continue at that address, whilst also
placing the address of the next instruction on the stack.

Thus the execution sequence of the above example is as follows:

The **jms** instruction replaces the contents of the program counter with
the address of the label *lab*. The next instruction executed is **inc**.

Additional instructions are then executed, then the **bbl** instruction.

The **bbl** instruction then retrieves the topmost address from the stack (the
address of the **xch** instruction), sets the program counter to that address.

From here, normal program execution continues at that location.


.. _jms: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
