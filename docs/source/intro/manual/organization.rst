.. _organization:

Computer Organization
=====================

.. include:: ../../global.rst


This section provides the programmer with a functional overview of the 4004 computer. 
Information is presented in this section at a level that provides a programmer with necessary 
background in order to write efficient programs.

To the programmer, the computer is represented as consisting of the following parts:


(1) Sixteen working registers which serve as temporary storage for data, and provide the means for 
    addressing memory. |br| |br|

(2) The accumulator in which data is processed. |br| |br|

(3) Memories which may hold program instructions or data (or sometimes both), and which must 
    be addressed location by location in order to access stored information. |br| |br|

(4) The stack which is a device used to facilitate execution of subroutines, as described 
    later in this section. |br| |br| *******

(5) Input/Output which is the interface between a program and the outside world. |br| |br|

Text © intel4004.com