.. _subroutines:

Subroutines
===========

.. include:: ../../global.rst

Frequently, a group of instructions must be repeated many times in a program. |br|
The group may be written "n" times if it is needed at "n" different points in a program, but better economy 
can be obtained by using subroutines.
|br| |br| A subroutine is coded like any other group of assembly language statements, and
is referred to by its name, which is the label of the first instruction. 
|br| |br| The programmer references a subroutine by writing its name in the operand field of a JMS instruction. 
When the JMS is executed, the address of the next sequential instruction after the JMS is written to the address stack (see Section 2.4), and
program execution proceeds with the first instruction of the subroutine. 
|br| |br| When the subroutine has completed its work, a BBL instruction is executed, which loads
a value into the accumulator and causes an address to be read from the stack into the program counter, causing 
program execution to continue with the instruction following the JMS. Thus, one copy of a subroutine may be 
called from many different points in memory, preventing duplication of code. Note also that since the address 
stack and the JMS instruction use 12-bit addresses, calling programs and subroutines may be 
located anywhere in ROM or control program RAM (they need not be on the same page in memory).

.. rubric::  Example: 

Subroutine IN increments an 8 bit number passed in index register 0
and 1 and then returns to the instruction following the last JMS instruction executed.

::

    IN,     XCH     1   / Register 1 to accumulator
            IAC         / Increment value and produce carry 
            XCH     1   / Restore register 1
            JCN 10  NC  / Jump if Carry is zero
            INC     0   / Increment high order 4 bits
    NC,     BBL     0   / returns


Assume IN appears as follows:

.. image:: /intro/manual/images/sub-diag1.png
          :scale: 50%
          :align: center


When the first JMS is executed, address 3C2H is written to the address stack, and control 
is transferred to IN. Execution of the BBL statement will cause the address 3C2H to be read 
from the stack and placed in the program counter, causing execution to continue at 3C2H 
(since the JMS occupies two bytes).

.. image:: /intro/manual/images/sub-diag2.png
          :scale: 50%
          :align: center

|br|
When the second JMS is executed, address 403H is written to the stack, and control is again transferred to IN. 
This time, the BBL will cause execution to resume at 403H.
|br| |br|
Note that IN could have called another subroutine during its
execution, causing another address to be written to the stack. 
This can occur only up to three levels, however, since the stack can hold only three addresses.
Beyond this point, some addresses will be overwritten and BBLs will transfer program control to incorrect addresses.