.. _intel_4004_opcodes:

Intel 4004 Op-Codes
===================
.. toctree::
   :hidden:

   ../hardware/machine/fim
   ../hardware/machine/fin
   ../hardware/machine/jin
   ../hardware/machine/jms
   ../hardware/machine/jun
   ../hardware/machine/jcn
   ../hardware/machine/src
   ../hardware/machine/nop

.. list-table:: Intel 4004 processor Op-Codes
   :header-rows: 1

   * - Instruction
     - Mnemonic
     - 1st byte
     - 2nd byte
     - Modifiers
   * - No Operation
     - :ref:`hardware-machine-nop`
     - 00000000
     -
     -
   * - Jump Conditional
     - :ref:`hardware-machine-jcn`
     - 0001CCCC
     - AAAAAAAA
     - C, A
   * - Fetch Immediate
     - :ref:`hardware-machine-fim`
     - 0010RRR0
     - DDDDDDDD
     - RP, D
   * - Send Register Control
     - :ref:`hardware-machine-src`
     - 0010RRR1
     -
     - RP
   * - Fetch Indirect
     - :ref:`hardware-machine-fin`
     - 0011RRR0
     -
     - RP
   * - Jump Indirect
     - :ref:`hardware-machine-jin`
     - 0011RRR1
     -
     - RP
   * - Jump Unconditional
     - :ref:`hardware-machine-jun`
     - 0100AAAA
     - AAAAAAAA
     - A
   * - Jump to Subroutine
     - :ref:`hardware-machine-src`
     - 0101AAAA
     - AAAAAAAA
     - A
   * - Increment
     - INC
     - 0110RRRR
     -
     - R
   * - Increment and Skip
     - ISZ
     - 0111RRRR
     - AAAAAAAA
     - R, A
   * - Add
     - ADD
     - 1000RRRR
     -
     - R
   * - Subtract
     - SUB
     - 1001RRRR
     -
     - R
   * - Load
     - LD
     - 1010RRRR
     -
     - R
   * - Exchange
     - XCH
     - 1011RRRR
     -
     - R
   * - Branch Back and Load
     - BBL
     - 1100DDDD
     -
     - D
   * - Load Immediate
     - LDM
     - 1101DDDD
     -
     - D
   * - Write Main Memory
     - WRM
     - 11100000
     -
     -
   * - Write RAM Port
     - WMP
     - 11100001
     -
     -
   * - Write ROM Port
     - WRR
     - 11100010
     -
     -
   * - Write Status Char 0
     - WR0
     - 11100100
     -
     -
   * - Write Status Char 1
     - WR1
     - 11100101
     -
     -
   * - Write Status Char 2
     - WR2
     - 11100110
     -
     -
   * - Write Status Char 3
     - WR3
     - 11100111
     -
     -
   * - Subtract Main Memory
     - SBM
     - 11101000
     -
     -
   * - Read Main Memory
     - RDM
     - 11101001
     -
     -
   * - Read ROM Port
     - RDR
     - 11101010
     -
     -
   * - Add Main Memory
     - ADM
     - 11101011
     -
     -
   * - Read Status Char 0
     - RD0
     - 11101100
     -
     -
   * - Read Status Char 1
     - RD1
     - 11101101
     -
     -
   * - Read Status Char 2
     - RD2
     - 11101110
     -
     -
   * - Read Status Char 3
     - RD3
     - 11101111
     -
     -
   * - Clear Both
     - CLB
     - 11110000
     -
     -
   * - Clear Carry
     - CLC
     - 11110001
     -
     -
   * - Increment Accumulator
     - IAC
     - 11110010
     -
     -
   * - Complement Carry
     - CMC
     - 11110011
     -
     -
   * - Complement
     - CMA
     - 11110100
     -
     -
   * - Rotate Left
     - RAL
     - 11110101
     -
     -
   * - Rotate Right
     - RAR
     - 11110110
     -
     -
   * - Transfer Carry and Clear
     - TCC
     - 11110111
     -
     -
   * - Decrement Accumulator
     - DAC
     - 11111000
     -
     -
   * - Transfer Carry Subtract
     - TCS
     - 11111001
     -
     -
   * - Set Carry
     - STC
     - 11111010
     -
     -
   * - Decimal Adjust Accumulator
     - DAA
     - 11111011
     -
     -
   * - Keyboard Process
     - KBP
     - 11111100
     -
     -
   * - Designate Command Line
     - DCL
     - 11111101
     -
     -


.. note:: Modifiers

   - A =  Address
   - C =  Condition
   - D =  Data
   - R =  Register
   - RP = Register Pair
