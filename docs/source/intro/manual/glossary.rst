.. _glossary:

Glossary of Terms
=================

.. include:: ../../global.rst

.. list-table:: 
   :header-rows: 1

   * - Term
     - Definition
   * - Address
     - A 12 bit number assigned to a read-only-memory or |br|
       program random-access memory location corresponding |br|
       to its sequential position.
   * - Bit
     - The smallest unit of information which can be represented. |br|
       (A bit may be in one of two states, 0 or 1).
   * - Byte
     - A group of 8 contiguous bits occupying a single memory location.
   * - Character
     - A group of 4 contiguous bits of data.
   * - Instruction 
     - The smallest single operation that the computer can be |br|
       directed to execute.
   * - Object Program
     - A program which can be loaded directly into the computer's |br| 
       memory and which requires no alteration before execution. |br|
       An object program was usually on paper tape, and is produced |br| 
       by assembling a source program, however the Pyntel4004 Assembler |br| 
       can produce object code to be loaded into an emulator or directly |br| 
       on to a board simulating an MCS-4. |br| 
       Instructions are represented by binary machine code in an |br| 
       object program.
   * - Program
     - A sequence of instructions which are taken as a group to |br| 
       allow the computer to accomplish a desired task.
   * - Source Program
     - A program which is readable by a programmer but which must be |br| 
       transformed into object program format before it can be loaded |br| 
       into the computer and executed. |br|
       Instructions in an assembly language source program are represented |br| 
       by their assembly language mnemonic.
   * - System Program
     - A program written to help in the process of creating user programs.
   * - User Program
     - A program written by the user to make the computer |br| 
       perform any desired task.
   * - nnnb
     - nnn represents a number in binary format.
   * - 0xnn
     - nnn represents a number in hexadecimal format.

.. rubric:: Note

All numbers in this document are assumed to be decimal unless otherwise specified.


.. rubric:: Note

.. image:: images/byte.png
   :scale: 50%
   :align: left


A representation of a byte in memory. |br|
Bits which are fixed  are indicated by 0 or 1; bits vvhich may be either
0 or 1 in different circumstances are represented by letters; thus RP represents a
three-bit field which contains one of the eight possible combinations of zeroes and ones.

Text © intel4004.com


