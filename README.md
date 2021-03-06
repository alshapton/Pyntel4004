![Pyntel 4004 Logo](./images/pyntel4004.svg)
A Python software implementation of the Intel 4004 processor.

## General Information
- Two pass assembler using the original mnemonics, directives and comments syntax
- Monitor facility to step through code and examine registers, memory etc

## Design goals
- [ ] As much of the internals as possible should be carried out using binary arithmetic and operations.

- [ ] No external libraries to be used (i.e. pure Python).

- [ ] Build a fully-working i4004 opcode emulator.

- [ ] Build a fully-working assembler which generates correct op-codes.

- [ ] Construct a fully-working i4004 chip which can use the generated object code from the compiler (possibly using micro-python or circuit python on an Ardiuno Board).

## Example

##### Assembler Directives and other additions
Assembler directives are not part of the proogram itself, but can control things like starting address, and various environmental settings.

| Directive | Example | Meaning |
| :-:| :-:| :-|
| end | end | Indicating end of program, but not necessarily end of code |
| org | org 100 | Assemble and place object code commencing at address 100 |
| pin | pin 1 | Value of i4004's Pin 10 (test pin) |
|  / | / Author: ALS | A comment |
| label,| loop,| A label can be referred to in various control transfer statements. It MUST end in a comma (,)




![Assemble and Run](./images/assemble-run.png)

## Monitor Commands

| Command | Example | Meaning |
| :-:| :-:| :-|
| "Enter" | "Enter" | Execute the current instruction and move to the next |
|  acc   |   acc    | Show the current contents of the Accumulator |
|  carry |  carry    | Show the current contents of the Carry Bit |
|  off    |  off    | Continue to execute the program with no trace |
|   pc    |   pc    | Show the Program Counter |
| pin10   | pin10   | Show the status of PIN10 on the i4004 chip (test pin)
|    q    |    q    | Quit the monitor without executing any further commands |
|  ram   |   ram    | Show the complete contents of RAM |
|  reg *n*  |  reg 7  | Show content of a specified register |
|  regs   |  regs   | Show all 16 registers |
|  rom   |   rom    | Show the complete contents of ROM |
| stack   |  stack  | Show the stack and the location of the stack pointer |


### Credits:
- Intel 4004 Design Team
- Logo: [LouBeLou Print Shop](Www.psloubelou.com)

![Pyntel 4004 Logo](./images/Pyntel4001_chip.png)
