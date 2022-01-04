.. _operand_field:

Operand Field
=============

.. include:: ../../global.rst


This field contains information used in conjunction with the code field to 
define precisely the operation to be performed by the instruction. 
Depending upon the code field, the operand field may be absent or may 
consist of one item or two items separated by blanks.
|br|
There are five types of information [(a) through (e) below] that may be 
requested as items of an operand field, and the information may be 
specified in five ways [(1) through (5) below].
|br|

The five ways of specifying information are as follows:

.. rubric:: (1) A Decimal number

Example:

::
    
    ABC,    LDM     14      / Load accumulator with decimal 14 (1100b).


.. rubric:: (2) The current program counter. This is specified by the character `*`
    and is equal to the address of the first byte of the currrent instruction.

Example:

::
    
    GO,    LDM     *+6      / If the instruction above is being assembled at 
                            / location 213, it will cause program control to 
                            / be transferred to address 219.

.. rubric:: (3) Labels that have been assigned a decimal number by the assembler (:ref:`the equate instruction<equate>`). 

Example:

Suppose label VAL has been equated to the number 42, and ZER
has been equated to the number 0. Then the following instructions all load 
register pair zero with the hexadecimal value 2A (decimal 42):


::
    
    A1,     FIM  0      42
    A2,     FIM  ZER    42
    A3,     FIM  ZER    VAL

.. rubric:: (4) Labels that appear in the label field of another instruction.

Example:

::
    
    LP1,    JUN  LP2    / Jump to label LP2
            ---
            ---
            ---
    LP2,    CMA
    


.. rubric:: (5) Arithmetic expressions involving data types (1) to (4) above connected by the 
    operators `+` (addition) and `-` (subtraction). These operators treat their 
    arguments as 12-bit quantities, and generate 12-bit quantities as their result. 
    If a value is generated which exceeds the number of bits available for it in 
    an instruction, the value is truncated on the left.

For example, if VAL refers to hexadecimal address 0xFFE, the instruction:
::

    JUN VAL

is encoded as 0x4FFE; a 4-bit operation code and 12 bit value. 

However, the instruction:

::

    JUN VAL + 9

will be encoded as 0x4007, where the value 0x007 has been truncated on the left
to 12 bits (three hex digits) giving a value o 0x007.

---------

Using some or all of the above data specifications, the following five types 
of information may be requested:
|br|

.. rubric:: (a) A register to serve as the source or destination in a data operation. 
    Methods 1, 3, or 5 may be used to specify the register, but the specification must 
    finally evaluate to one of the decimal numbers 0 to 15.

Example:

::

        I1,     INC 4
        I2,     INC R4
        I3,     INC 16 - 12

Assuming `R4` has been equated to 4, then the above instructions will **ALL** increment
register 4.

.. rubric:: (b) A register pair to serve as the source or destination in a data operation.
    The specification must evaluate to one of the even decimal numbers from 0 through 14 
    (corresponding to register pair designators 0P through 7P).

Example:

::

        I1,     SRC 1P
        I2,     INC 2
        I3,     INC RG2

Assuming label `RG2` has been equated to 2, then the above instructions will **ALL** increment
register pair 2 (i.e. registers 2 and 3).

.. rubric:: (c) Immediate data, to be used directly as a data item.

Example:

::

        AC1,    DATA    / Load the value of DATA into the accumulator


The value of `DATA` could be one of the following forms:

::

        19
        12 + 72 -3
        VAL             / Where VAL has been equated to a number

.. rubric:: (d) A 12 bit address, or the label of another location in memory.

Example:

::

        HR, JUN     OVR / Jump to instruction at OVR.
            JUN     513 / Jump to hex address 201 (decimal 513).


.. rubric:: (e) A condition code for use by the JCN (jump on condition) instruction. 
    This must evaluate to a number from 0 to 15.

Example:

::

            JCN 4   LOC 
            JCN 2+2 LOC

The above instructions cause program control to be transferred to address LOC if condition 4 (accumulator zero) is true.