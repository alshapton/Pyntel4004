.. _carry:

Carry Bit
=========

.. include:: ../../global.rst


To make programming easier, a carry bit is provided by the 4004 to reflect the results of 
data operations. The descriptions of :ref:`individual instructions<intel_4004_opcodes>` specify which 
instructions affect the carry bit and whether the execution of the instruction is dependent 
in any way on the prior status of the carry bit. 
|br|
|br|
The carry bit is "set" if 1 and  "reset" if 0.
|br|

Certain data operations can cause an overflow out of the high-order 3-bit.
For example, addition of two hexadecimal digits can give rise to an answer that does not fit in one digit:

::

                                    3 2 1 0     Bit number

                            A       1 0 1 0
                        +   7       0 1 1 1
                                    -------
                            1       0 0 0 1
                        carry 

An operation that results in a carry out of bit 3 will set the carry bit. |br|
An operation that could have resulted·in a carry out of bit 3 but did not will reset the carry bit.