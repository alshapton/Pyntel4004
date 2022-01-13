.. _constant_data:

Constant Data
=============

.. include:: ../../global.rst

Eight-bit data values can be assembled into ROM or 
program RAM locations by writing a blank code field and 
an operand field beginning with a positive number. If the 
operand is greater than 8 bits, it will be truncated on the left.

Example:

Assume that a label VAL has been equated to 14, and the label LOC appears
on an instruction assembled at location 0x034B

::

                                                            Assembled Data

            LDM     0           / Statement for context     
        C1,         0 + VAL                                     0x0E
        C2,         4095                                        0xFF
        C3,         0 + LOC                                     0x4B


The following are invalid data statements 

::


            LDM     0           / Statement for context     
        C4,         ABC         / Does not begin with a number 
        C5,         -18         / Number is not positive