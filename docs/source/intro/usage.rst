.. _usage:

Overview of Pyntel4004
======================


Pyntel4004 consists of two components:

- an Intel 4004 assembler/disassembler
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

This file should then be assembled into 4004 machine code.

In order to do this, the CLI package should be installed:

::

pip install pyntel4004-CLI

The full instructions for Pyntel4004-CLI should be read, however, a basic summary is below:
### Basic Usage.

`4004 <command> <options> <arguments>`

`<command>`
- `asm`  Assemble the input file
- `dis`  Disassemble the input file
- `exe`  Execute the object file

`<options>`
- **-h**, **--help**: Show help.
- **-v**, **--version**:  Show the version and exit.

<br>
<br>

#### `asm` options.

- **-i**, **--input** `<input file>`: assembly language source file [required].
- **-o**, **--output** `<output file>`: object code output file.
- **-e**, **--exec**: execute the assembled program if successful assembly.

- **-q**, **--quiet**: Quiet mode on *
- **-m**, **--monitor**: Start monitor*

- **-h**, **--help**: Show help.

*Mutually exclusive parameters

<br>
<br>

#### `dis` options.

- **-o**, **--object** `<object file>`: object code or binary input file. [required]
- **-b**, **--byte**: number of bytes to disassemble (between 1 and 4096).

    *It is the user's responsibility to understand that if a byte count causes the disassembler to end up midway through a 2-byte instruction, that last instruction will not be disassembled correctly.*

- **-h**, **--help**: Show help.

<br>
<br>

#### `exe` options.

- **-o**, **--object** `<object file>`: object code or binary input file.[required].
- **-q**, **--quiet**: Quiet mode on

- **-h**, **--help**: Show help.