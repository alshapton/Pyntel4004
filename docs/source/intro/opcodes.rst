.. _intel_4004_opcodes:

Intel 4004 Op-Codes
===================
.. toctree::
   :hidden:

   ../hardware/machine/add
   ../hardware/machine/bbl
   ../hardware/machine/clb
   ../hardware/machine/clc
   ../hardware/machine/cma
   ../hardware/machine/cmc
   ../hardware/machine/daa
   ../hardware/machine/dac
   ../hardware/machine/dcl
   ../hardware/machine/fim
   ../hardware/machine/fin
   ../hardware/machine/iac
   ../hardware/machine/inc
   ../hardware/machine/isz
   ../hardware/machine/jin
   ../hardware/machine/jms
   ../hardware/machine/jun
   ../hardware/machine/jcn
   ../hardware/machine/kbp
   ../hardware/machine/ld
   ../hardware/machine/ldm
   ../hardware/machine/nop
   ../hardware/machine/ral
   ../hardware/machine/rar
   ../hardware/machine/rdn
   ../hardware/machine/src
   ../hardware/machine/stc
   ../hardware/machine/sub
   ../hardware/machine/tcc
   ../hardware/machine/tcs
   ../hardware/machine/wmp
   ../hardware/machine/wpm
   ../hardware/machine/wrm
   ../hardware/machine/wrn
   ../hardware/machine/wrr
   ../hardware/machine/xch

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
     - :ref:`hardware-machine-inc`
     - 0110RRRR
     -
     - R
   * - Increment and Skip
     - :ref:`hardware-machine-isz`
     - 0111RRRR
     - AAAAAAAA
     - R, A
   * - Add
     - :ref:`hardware-machine-add`
     - 1000RRRR
     -
     - R
   * - Subtract
     - :ref:`hardware-machine-sub`
     - 1001RRRR
     -
     - R
   * - Load
     - :ref:`hardware-machine-ld`
     - 1010RRRR
     -
     - R
   * - Exchange
     - :ref:`hardware-machine-xch`
     - 1011RRRR
     -
     - R
   * - Branch Back and Load
     - :ref:`hardware-machine-bbl`
     - 1100DDDD
     -
     - D
   * - Load Immediate
     - :ref:`hardware-machine-ldm`
     - 1101DDDD
     -
     - D
   * - Write Main Memory
     - :ref:`hardware-machine-wrm`
     - 11100000
     -
     -
   * - Write RAM Port
     - :ref:`hardware-machine-wmp`
     - 11100001
     -
     -
   * - Write Program RAM
     - :ref:`hardware-machine-wpm`
     - 11100011
     -
     -
   * - Write ROM Port
     - :ref:`hardware-machine-wrr`
     - 11100010
     -
     -
   * - Write Status Char 0
     - :ref:`WR0 <hardware-machine-wrn>`
     - 11100100
     -
     -
   * - Write Status Char 1
     - :ref:`WR1 <hardware-machine-wrn>`
     - 11100101
     -
     -
   * - Write Status Char 2
     - :ref:`WR2 <hardware-machine-wrn>`
     - 11100110
     -
     -
   * - Write Status Char 3
     - :ref:`WR3 <hardware-machine-wrn>`
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
     - :ref:`RD0 <hardware-machine-rdn>`
     - 11101100
     -
     -
   * - Read Status Char 1
     - :ref:`RD1 <hardware-machine-rdn>`
     - 11101101
     -
     -
   * - Read Status Char 2
     - :ref:`RD2 <hardware-machine-rdn>`
     - 11101110
     -
     -
   * - Read Status Char 3
     - :ref:`RD3 <hardware-machine-rdn>`
     - 11101111
     -
     -
   * - Clear Both
     - :ref:`hardware-machine-clb`
     - 11110000
     -
     -
   * - Clear Carry
     - :ref:`hardware-machine-clc`
     - 11110001
     -
     -
   * - Increment Accumulator
     - :ref:`hardware-machine-iac`
     - 11110010
     -
     -
   * - Complement Carry
     - :ref:`hardware-machine-cmc`
     - 11110011
     -
     -
   * - Complement Accumulator
     - :ref:`hardware-machine-cma`
     - 11110100
     -
     -
   * - Rotate Left
     - :ref:`hardware-machine-ral`
     - 11110101
     -
     -
   * - Rotate Right
     - :ref:`hardware-machine-rar`
     - 11110110
     -
     -
   * - Transfer Carry and Clear
     - :ref:`hardware-machine-tcc`
     - 11110111
     -
     -
   * - Decrement Accumulator
     - :ref:`hardware-machine-dac`
     - 11111000
     -
     -
   * - Transfer Carry Subtract
     - :ref:`hardware-machine-tcs`
     - 11111001
     -
     -
   * - Set Carry
     - :ref:`hardware-machine-stc`
     - 11111010
     -
     -
   * - Decimal Adjust Accumulator
     - :ref:`hardware-machine-daa`
     - 11111011
     -
     -
   * - Keyboard Process
     - :ref:`hardware-machine-kbp`
     - 11111100
     -
     -
   * - Designate Command Line
     - :ref:`hardware-machine-dcl`
     - 11111101
     -
     -


.. note:: Modifiers

   - A =  Address
   - C =  Condition
   - D =  Data
   - R =  Register
   - RP = Register Pair
