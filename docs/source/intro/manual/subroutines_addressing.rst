.. _subroutines_addressing:

Subroutines and use of the Stack for Addressing
===============================================

.. include:: ../../global.rst


Before understanding the purpose or effectiveness of the stack,
it is necessary to understand the concept of a subroutine.


Consider a frequently used operation such as addition. 
|br|
The 4004 provides instructions to add one character of data to another, 
but what if there was a requirement to add numbers outside the range of 0 to 15 
(the range of one character)? Such addition will require a number of instructions 
to be executed in sequence. It is quite possible that this addition routine 
may be required many times within one program; to repeat the identical code every 
time it is needed is possible, but very wasteful of memory:


.. image:: /intro/manual/images/sub-stack-diag1.png
          :scale: 50%
          :align: center

A more efficient means of accessing the addition routine would be to store 
it once, and find a way of accessing it when needed:

 .. image:: /intro/manual/images/sub-stack-diag2.png
          :scale: 50%
          :align: center

A frequently accessed routine such as the addition above is called a subroutine,
and the 4004 provides instructions that call subroutines and return from subroutines.

When a subroutine is executed, the sequence of events may be depicted as follows:

 .. image:: /intro/manual/images/sub-stack-diag3.png
          :scale: 50%
          :align: center

|br|
The arrows indicate the execution sequence.

When the" Call" instruction is executed, the address of the "next" instruction is 
written to the stack (see Section 2.4), and the subroutine is executed. The last executed 
instruction of a subroutine will always be a special "Return Instruction", which reads an 
address from the stack into the program counter, and thus causes
program execution to continue at the "Next" instruction as illustrated below:

 .. image:: /intro/manual/images/sub-stack-diag4.png
          :scale: 50%
          :align: center

Since the stack provides three registers, subroutines may be nested up to three deep; 
for example, the addition subroutine could itself call some other subroutine and so on. 
An examination of the sequence of write and read stack operations will show that the 
return path will always be identical to the call path, even if the same subroutine 
is called at more than one level; however, an attempt to nest subroutines to a depth 
of more than 3 will cause the program to fail, since some addresses will have been overwritten.