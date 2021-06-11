.. _hardware-machine-jun:

JUN
===
.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Jump Unconditionally
   * - Function
     - Jump to any address within the memory space.
   * - Syntax
     - JUN (address)
   * - Assembled
     -
   * - Binary
     - 0010RAAAA AAAAAAAA
   * - Decimal
     - 64, then incrementing by 1 until 79 (1st word)
   * - Hexadecimal
     - 0x40, then incrementing by 2 until 0x4F (1st word)
   * - Symbolic
     - .. image:: images/jun-sym.png
          :scale: 50%
   * - Execution
     - 2 words 16-bit code and an execution time of 21.6 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - jun_


.. rubric:: Detailed Description

The 8 bits held in the register pair specified by RP are loaded into the
lower 8 bits of the program counter. The highest 4 bits of the program
counter are unchanged. Therefore program execution continues at this
address on the same page of memory in which the JIN instruction is loaded.

The carry bit, nor the contents of the register pair are not affected.

The disassembly of the instruction below shows how the register pair is
represented in the opcode.

.. image:: images/jun.png
  :scale: 50%
  :align: center


This instruction and the JMS instruction , use a 12-bit address, and can
reference any memory location. Their operation is not influenced by their
position within a page of memory, whereas some other instructions are.

Therefore, only a **JUN** or **JMS** instruction should be used to transfer control
from one page of memory to another.


.. rubric:: Example program snippet for illustration

::

     Arbitrary Memory
     Address   (Hex)

       0x360               jun LRG
       0x362         AD,   add 1



       0x370         LAC,  ldm 3
       0x371               jun AD



       0x3EO         LRG,  fim 0p, 4
       0x3E2               jun LAC
                           end


Normally, program instructions are executed sequentially.

A 12-bit register called the **program counter** holds the address of the
instruction to be executed. The JUN instruction replaces the program counter
contents, causing program execution to continue at that address.

Thus the execution sequence of the above example is as follows:

The **jun** instruction at 0x360 replaces the contents of the program counter with
0x3EO. The next instruction executed is the **fim** at location **LRG** which
loads register 0 with the value 0, and register 1 with the value 4.

The **jun** at 0x3E2 is then executed.
The program counter is set to 0x370, and the **ldm** at this address loads the
accumulator with the value 3.

The **jun** at 0x371 sets the program counter to 0x362, where the **add**
instruction adds the contents of register 1 plus the carry bit to the accumulator.

From here, normal program execution continues at location 0x363.


.. _jin: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
