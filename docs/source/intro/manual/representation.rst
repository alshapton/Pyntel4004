.. _representation:

Computer Program representation in Memory
=========================================

.. include:: ../../global.rst

|just|

A computer program consists of a sequence of instructions. 
Each instruction performs an elementary operation such as the movement of data,
an arithmetic operation on data, or a change in instruction execution sequence. 
Instructions are described in :ref:`groups<instruction_summary>` or :ref:`individually<intel_4004_opcodes>`.
|br| |br|
A program will be stored in Read-Only Memory or Program Random Access Memory. 
It will appear as a sequence of hexadecimal digits which represent the instructions 
of the program. The memory address of the instruction being executed
is recorded in a 12-bit register called the Program Counter, and thus it is possible
to track a program as it is being executed. After each instruction is executed, the 
program counter is advanced to the address of the next instruction. 
Program execution proceeds sequentially unless a transfer-of-control instruction 
(jump or skip) is executed, which causes the program counter to be set to a specified 
address. Execution then continues sequentially from this new address in memory.
|br| |br|
Upon examining the contents of a ROM or program RAM memory location,
there is no way of telling whether a byte contains an encoded instruction or constant data. 
For example, the hexadecimal code F2 has been selected to represent
the instruction IAC (increment accumulator). Thus, the hex value F2 stored in 
a memory byte could represent either the instruction IAC or the hex data value F2.

---------

It is up to the programmer to ensure that data is not misinterpreted as an 
instruction code, but this is simply done as follows:
|br| |br|
Every program has a starting memory address, which is the memory address of the location 
holding the first instruction to be executed. Just before the first instruction is executed,
the program counter will automatically be set to this address, and this procedure will be 
repeated for every instruction in the program. 4004 instructions may require 8 or 16 bits 
for their encoding; in each case the program counter is set to the corresponding address as 
shown in the diagram below.
|br| |br|
In order to avoid errors, the programmer must be sure that a byte of constant data 
does not follow an instruction when another instruction is expected. 
Referring to the diagram, an instruction is expected in location 0x13F, since instruction 
4 is to be executed after instruction 3. 
|br| |br|
If location 0x13F held constant data, the program would not execute correctly. 
Therefore, when writing a program, do not place constant data in between adjacent 
instructions that are to be executed consecutively.
|br| |br|
A class of instructions (referred to as transfer-of-control instructions) causes program 
execution to branch to an instruction other than the next sequential instruction. The
memory address specified by the transfer of control instruction must be the address
of another instruction; if it is the address of a memory location holding data, 
the program will not execute correctly. For example, referring to the diagram below, suppose 
instruction 2 specifies a jump to location 0x140 and instructions 3 and 4 were replaced 
by data. Then following execution of instruction 2, the program counter would be set to 
0x140 and the program would execute correctly. 
But if, in error, instruction 2 were to specify a jump to 0x13E, an error would result 
since this location now holds data. Even if instructions 3 and 4 were not altered, 
a jump to location 0x13E would cause an error, since this is not the first byte of the instruction.

---------

Upon reading Section 3, you will see that it is easy to avoid writing an assembly language 
program with jump instructions which have erroneous memory addresses. Information on this subject 
is given here rather to help the programmer who is debugging programs by entering hexadecimal 
codes directly into program RAM

.. note::

    Programs usually exist in ROM, and therefore cannot be altered in this manner.


.. image:: /intro/manual/images/represent-diag.png
          :scale: 50%
          :align: center

