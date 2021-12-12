.. _hardware-machine-wpm:

WPM
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
     - Read/Write half a byte to Program RAM from accumulator.
   * - Syntax
     - WPM
   * - Assembled
     -
   * - Binary
     - 11100011
   * - Decimal
     - 227
   * - Hexadecimal
     - 0xE3
   * - Symbolic
     - .. image:: images/wpm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - wpm_

.. rubric:: Detailed Description

This is a special instruction which may be used to write the contents of the accumulator
into a half byte of program RAM,or read the contents of a half byte of program RAM into a 
ROM input port where it can be accessed by a program.

The carry bit is not affected.

The opcode for this instruction does not contain any additional data:

.. image:: images/wpm.png
   :scale: 50%
   :align: center

.. rubric:: Notes


Two WPM instructions must always appear in close succession; that is, 
each time one WPM instruction references a half byte of program RAM as 
indicated by an SRC address, another WPM must access the other half byte 
before the SRC address is altered. 
An internal counter keeps track of which half-byte is being accessed. 
If only one WPM occurs, this ounter will be out of sync with the program
and errors will occur. 
In this situation a RESET pulse must be used to re-initialize the machine.

A WPM instruction requires an SRC address to access program RAM.
**Whenever a WPM is executed, the DATA RAM which happens to correspond to 
this SRC address will also be written.**
If data needed later in the program is being held in such DATA RAM, 
the programmer must save it elsewhere before executing the WPM instruction.



.. rubric:: Storing Data Into Program RAM

A program must perform the following actions in order to store eight bits of data into a 
program RAM location:

(1) The value 1 must be written to ROM port number 14. 
    This is a "write enable" signal, permitting the store operation to work.

(2) The highest 4 bits of the program RAM address to be accessed must be written to ROM port number 15.

(3) The lowest 8 bits of the program RAM address to be accessed must be sent out by an SRC instruction.

(4) The higher 4 bits of data to be written must be loaded into the accumulator and written with the 
    first WPM; the lower 4 bits of data must then be loaded into the accumulator and written with
    the second WPM.

(5) The value 0 must be written to ROM port number 14, clearing the "write enable".


.. rubric:: Reading Data From Program RAM

A program must perform the following actions in order to read eight bits of data from a
program RAM location:

(1) The highest 4 bits of the program RAM address to be accessed must be written to ROM port 15.

(2) The lowest 8 bits of the program RAM address to be accessed must be sent out by an SRC instruction.

(3) Two WPM instructions in succession must be executed. The first reads the leftmost 4 bits of the 
    program RAM location into ROM port 14; the second reads the rightmost 4 bits of the program RAM 
    location into ROM port 15.



.. rubric:: Example program - TO DO

.. image:: images/wpm-diag.png
   :scale: 50%
   :align: center

::

  / Example program
          FIM   0P  180
          SRC   0P
          LDM   15
          WRM


.. _wpm: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
