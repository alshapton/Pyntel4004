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

pip install pyntel4004-cli

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

- **-i**, **--input** `<input file>`: assembly language source file.
- **-o**, **--output** `<output file>`: object code output file.
- **-e**, **--exec**: execute the assembled program if successful assembly.
- **-t**, **--type** `<extension>`: Type of output required. (multiple output types can be specified)
    - `bin` will deliver a binary file of machine code
    
    - `obj` will deliver an object module which can be loaded back into the disassembler for debugging

    - `h` will deliver a c-style header file that can be used in a RetroShield Arduino to run the code on a real 4004

    - `ALL` will deliver all of the above<details>New in 0.0.1-alpha.2<summary>Changelog</summary></details>
- **-c**, **--config** `<config file>`: use the specified config file<details>New in 0.0.1-alpha.2<summary>Changelog</summary></details>
- **-q**, **--quiet**: Quiet mode on *
- **-m**, **--monitor**: Start monitor*

- **-h**, **--help**: Show help.

*Mutually exclusive parameters

<br>
<br>

#### `dis` options.

- **-o**, **--object** `<object file>`: object code or binary input file.

- **-l**, **--labels**: show the label table (only available in .OBJ files)<details>New in 0.0.1-alpha.2<summary>Changelog</summary></details>
- **-c**, **--config** `<config file>`: use the specified config file<details>New in 0.0.1-alpha.2<summary>Changelog</summary></details>
- **-b**, **--byte**: number of bytes to disassemble (between 1 and 4096).
- **-h**, **--help**: Show help.

    *It is the user's responsibility to understand that if a byte count causes the disassembler to end up midway through a 2-byte instruction, that last instruction will not be disassembled correctly.*

<br>
<br>

#### `exe` options.

- **-o**, **--object** `<object file>`: object code or binary input file.
- **-c**, **--config** `<config file>`: use the specified config file<details>New in 0.0.1-alpha.2<summary>Changelog</summary></details>
- **-q**, **--quiet**: Quiet mode on

- **-h**, **--help**: Show help.

<br>
<br>

Error Messages
--------------

Error messages are displayed when there are issues with either the supplied command, or issues with the source code itself. The errors are raised as exceptions, with an exception type together with an information message

Errors
------

| Command  | Exception  | Options | Message  |
|---|---|----|--|
| asm  | BadParameter   | |Invalid Parameter Combination: --quiet and --monitor cannot be used together  |
| asm  | BadOptionUsage  | --type |Invalid output type specified | 
| asm | BadOptionUsage | --type |Cannot specify 'ALL' with any others|
|dis| BadOptionUsage| --inst | Instructions should be between 1 and 4096 |

Special Error Message

| Exception | Message |
|-----------|---------|
| CoreNotInstalled|  Pyntel4004 core is not installed - use pip install Pyntel4004


Configuration Files
-------------------
<details>New in 0.0.1-alpha.2<summary>Changelog</summary></details><br>
Pyntel4004-cli configuration files are specified using the [TOML](http://toml.io/) notation. This is a notation which favours humans over machines, so it is easy to understand and write the configuration you want.
<br>
<br>
Example Configuration File - example2.toml

```
# Configuration for Pyntel4004-cli.

title = "Configuration file for example2.asm"

[asm]
input = "example2.asm"
output = "example2"
type = ["BIN", "H"]
exec = true
monitor = true
quiet = true

[dis]
object = "examples/example2.obj"
inst = 6
labels = true

[exe]
object = "examples/example2.obj"
quiet = true
```

The configuration file has 4 sections:

This MUST be first

i)    The title - simply a description of what the configuration file is for. Note that any comments (lines starting with a ```#``` can be added anywhere for readability).

(in no particular order)

ii)  ```[asm]``` section containing directives for the assembly of a specific program source file

iii) ```[dis]``` section containing directives for the disassembly of a specific object module

iv)  ```[exe]``` section containing directives for the execution of a specific object module

The valid configuration tokens are shown in the example above - they mirror the options that can be specified on the command line. 

ANY of the configuration tokens can be overriden simply by specifying them on the command line.
