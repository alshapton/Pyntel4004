# Pyntel4004

![Pyntel 4004 Logo](https://github.com/alshapton/Pyntel4004/raw/4afcf04365d6169ca6c1a86a10d70997c7583da6/images/pyntel4004.svg)

[![Build Pipeline](https://github.com/alshapton/Pyntel4004/actions/workflows/build-pipeline.yml/badge.svg)](https://github.com/alshapton/Pyntel4004/actions/workflows/build-pipeline.yml)
[![Documentation Status](https://readthedocs.org/projects/pyntel4004/badge/?version=latest)](https://pyntel4004.readthedocs.io/en/latest/?badge=latest)
![GitHub](https://img.shields.io/github/license/alshapton/pyntel4004)
[![PyPI version](https://badge.fury.io/py/Pyntel4004.svg)](https://badge.fury.io/py/Pyntel4004)
![PyPI - Downloads](https://img.shields.io/pypi/dm/Pyntel4004)
[![Plant Tree](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=Plant%20Tree&query=%24.total&url=https%3A%2F%2Fpublic.offset.earth%2Fusers%2Ftreeware%2Ftrees)](https://plant.treeware.earth/alshapton/pyntel4004)

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg)](https://sonarcloud.io/summary/new_code?id=alshapton_Pyntel4004)

A Python software implementation of the Intel 4004 processor and the MCS-4 computer.

## General Information

-  Two pass assembler using the original mnemonics, directives and comments syntax
-  Disassembler
-  Monitor facility to step through code and examine registers, memory etc
-  Cross-assembler for Retroshield 4004 Arduino

## Requirements

* Python >= 3.8.2

<br>

## Installation Instructions
<br>

### PyPI

Pyntel4004 can be installed from PyPI by using the command:

```bash

    $ pip install Pyntel4004
```

### Source Code
Pyntel4004’s git repo is available on GitHub, which can be browsed [here](https://github.com/alshapton/pyntel4004) and cloned using:

```bash

    $ git clone https://github.com/alshapton/pyntel4004 pyntel4004
```

Verify the installation by running unit tests:
```bash

    $ cd pyntel4004/test
    $ pytest
```
## Questions, Answers and Issues

Please use the github discussion board for questions, to ensure the right people see them in a timely manner.

[Github Pyntel4004 Discussion Board](https://github.com/alshapton/Pyntel4004/discussions)

and the github issue tracker to raise any issues.

[Github Pyntel4004 Issues Board](https://github.com/alshapton/Pyntel4004/issues)

<br>

## Usage Instructions

To use this software implementation of the Intel 4004 from the command line, you should install the [Pyntel4004-cli](https://pypi.org/project/Pyntel4004-cli/) using
`
pip install pyntel4004-cli
`

The user instructions can be found [here](https://pyntel4004.readthedocs.io/en/latest/intro/usage.html
)

## Design goals

- As much of the internals as possible should be carried out using binary arithmetic and operations.
- No 3rd party libraries to be used (i.e. pure Python).
- Build a fully-working i4004 opcode emulator.
- Build a fully-working assembler which generates correct op-codes.
- Construct a fully-working software-based i4004 chip which can use the generated object code from the assembler.
- Enable code assembled with Pyntel4004 to be run on a real i4004 chipset
- Enable code assembled with Pyntel4004 to be run on a retroShield4004 for Arduino

## Status

22-MAY-2022     First release of configuration file support
20-MAR-2022:    Command Line functionality is now deprecated
02-MAR-2022:    Finalised split - Pyntel4004 is now the core library
21-FEB-2022:    Started to split into two - (chip, assembler, dissassembler) and CLI
04-FEB-2022:    Cross-assemble to retroShield4004 for Arduino, completing documentation
23-SEP-2021:    Publishing releases to [PyPi](https://pypi.org/project/Pyntel4004/)
<br>
10-SEP-2021:    Documentation building and hosted with [READTHEDOCS](https://pyntel4004.readthedocs.io/en/latest/)
<br>
12-JUN-2021:    Auto-build with GITHUB Actions implemented
<br>
18-MAY-2021:    Implementing full test suite
<br>
21-APR-2021:    Instruction Set functionally complete
                Entering Testing Phase

## Example

### Assembler Directives and other additions

Assembler directives are not part of the program itself, but can control things like starting address, and various environmental settings.

| Directive | Example | Meaning |
| :-:| :-:| :-|
| end | end | Indicating end of program, but not necessarily end of code |
| org | org 100 | Assemble and place object code commencing at address 100 |
| pin | pin 1 | Value of i4004's Pin 10 (test pin) |
|  / | / Author: ALS | A comment |
| label,| loop,| A label can be referred to in various control transfer statements. It MUST end in a comma (,)

![Assemble and Run](https://github.com/alshapton/Pyntel4004/raw/4afcf04365d6169ca6c1a86a10d70997c7583da6/images/assemble-run.png)

## Monitor Commands

| Command | Example | Meaning |
| :-:| :-:| :-|
| "Enter" | "Enter"  | Execute the current instruction and move to the next |
|  acc    |   acc     | Show the current contents of the Accumulator |
|   b *n* |   b 71    | Create a breakpoint at address *n* |
|  carry  |  carry    | Show the current contents of the Carry Bit |
|  crb    |  crb     | Show the currently selected RAM Bank |
|  off    |  off     | Continue to execute the program with no trace |
|   pc    |   pc     | Show the Program Counter |
| pin10   | pin10    | Show the status of PIN10 on the i4004 chip (test pin)
|    q    |    q     | Quit the monitor without executing any further commands |
|  ram   |   ram     | Show the complete contents of RAM |
|  reg *n*  |  reg 7 | Show content of a specified register |
|  regs   |  regs    | Show all 16 registers |
|  rom    |   rom     | Show the complete contents of ROM |
| stack   |  stack   | Show the stack and the location of the stack pointer |


## Licence

This package is [Treeware](https://treeware.earth). If you use it in production, then we ask that you [**buy the world a tree**](https://plant.treeware.earth/alshapton/Pyntel4004) to thank us for our work. By contributing to the Treeware forest you’ll be creating employment for local families and restoring wildlife habitats.

### Credits

-  Intel 4004 Design Team
-  Logo: [LouBeLou Print Shop](http://www.psloubelou.com)

![Pyntel 4004 Logo](https://github.com/alshapton/Pyntel4004/blob/4afcf04365d6169ca6c1a86a10d70997c7583da6/images/Pyntel4001_chip.png)


.. _Python: https://www.python.org
