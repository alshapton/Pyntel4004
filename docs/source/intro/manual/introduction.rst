.. _introduction:

Introduction
============

.. include:: ../../global.rst


This document has been written to help the reader program the INTEL 4004 microcomputer 
in assembly language, and to show how it is economical and practical to do so. 

Accordingly, this manual assumes that the reader has a good understanding of logic, 
but may be unfamiliar with programming concepts.

For those readers vlho do understand programming concepts, several features of the 
INTEL 4004 microcomputer are described below. They include:

• 4 bit parallel CPU on a single chip.
• 46 instructions, including conditional branching, subroutine capability, and binary and decimal arithmetic modes.
• Direct addressing for 32,768 bits of read-only memory, 5120 bits of data random-access memory and 32768 bits of program random-access memory.
• Sixteen 4-bit index registers and a three 12-bit register stack.

INTEL 4004 microcomputer users will have widely differing programming needs. 
Some users may wish to write a few short programs, while other users may have 
extensive programming requirements.

For the user with limited programming needs,two system programs resident on the 
INTELLEC 4 (Intel's development system for the MCS-4microcomputer) are provided; 
they are an Assembler and a System Monitor. 

Use of the INTELLEC 4 and its system programs is described in the INTELLEC 4 
Operator's Manual.

For the user with extensive programming needs, cross assemblers are available 
which allow programs to be generated on a computer having a FORTRAN compiler 
whose word size is 32 bits or greater, limiting INTELLEC 4 use to final checkout 
of programs only.

