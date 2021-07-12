.. _usage:

Overview of Pyntel4004
======================


Pyntel4004 consists of two components:

- an Intel 4004 assembler
- an Intel 4004 emulator to run assembled code


.. rubric:: Hardware emulation

The Intel 4004 emulator mimics the hardware of an original Intel 4004 processor and its' support chips through software.

Each instruction in Pyntel4004 acts on a virtual processor in
the same way as the original hardware implementations of the
instructions would act upon the real hardware.

**The intention is to test the assembled code on a real Intel 4004 chip to verify this..**


.. rubric:: Usage

In order to use these tools, a source file must first be
prepared in i4004 assembly language.
::

    / Example program
        org    ram
        fim    2  254
        end

This file should then be assembled (ie converted from the
mnemonics into machine code) as follows:
::

    4004 -i program.asm -x

The **-i** option is mandatory and supplies the source file name.

The optional flag **-x** will start the program running in the correct memory space.
By default the monitor will start, to enable debugging. The monitor can be switched off
at any time.

The optional flag **-o <output file>** will store the assembled program in a named output file.

.. rubric:: TODO

- More detailed instructions - directory structure
- More background info
- Add ability to load pre-assembled code and run
- Add ability to turn the monitor off prior to running



