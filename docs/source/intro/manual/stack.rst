.. _stack:

The Stack
=========

.. include:: ../../global.rst

The stack consists of three 12-bit registers used to hold addresses of program 
instructions. Since programs are always run in ROM or program RAM, the
stack registers will always refer to ROM locations or program RAM locations. |br|

Stack operations consist of writing an address to the stack, and reading an address from the stack. 
In order to understand these operations, it may be helpful to visualize the stack as three registers 
on the surface of a cylinder, as shown below:

     - .. image:: images/stack-diag.png
          :scale: 50%
          :align: center
   
Each stack register is adjacent to the other two stack registers. 
The 4004 keeps a pointer to the next stack register available.

Writing An Address To The Stack
-------------------------------

To perform a stack write operation; |br|

(1) The address is written into the register indicated by the pointer. |br|
(2) The pointer is advanced to the next sequential register.

Any register may be used to hold the first address written to the stack. 
More than three addresses may be written to the stack; however, this will cause a corresponding number of previously 
stored addresses to be overwritten and lost. This is illustrated below:

     .. image:: images/stack-write.png
        :scale: 50%
        :align: center

.. rubric:: Note:

Storing the fourth address (d) overwrites the first address stored (a).

|just|

Reading An Address From The Stack
---------------------------------

To perform a stack read operation; |br|

(1) The pointer is backed up one register. |br|
(2) The memory address indicated by the pointer is read.

The address read remains in the stack undisturbed.  |br|
Thus, if 4 addresses are written to the stack and then three reads are performed, the stack will appear as below:


     .. image:: images/stack-read.png
        :scale: 50%
        :align: center

The stack is used by programs as described in Section 2.7.7.


Text © intel4004.com