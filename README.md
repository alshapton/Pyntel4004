![Pyntel 4004 Logo](./images/Pyntel4001_logo.png)
# Pyntel4004
A Python software implementation of the Intel 4004 processor.

## General Information
- Two pass assembler using the original mnemonics, directives and comments syntax

## Design ethos
- As much of the internals as possible should be carried out using binary arithmetic and operations
- No external libraries to be used (i.e. pure Python)
- Build a fully-working i4004 opcode emulator
- Build a fully-working assembler which generates correct op-codes
- Construct a fully-working i4004 chip which can use the generated object code from the compiler (possibly using micro-python or circuit python on an Ardiuno Board)

![Pyntel 4004 Logo](./images/Pyntel4001_chip.png)
