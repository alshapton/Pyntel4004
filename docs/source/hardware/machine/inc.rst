.. _hardware-machine-inc:

SRC
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Increment Register
   * - Function
     - Increments a specified register by 1.
   * - Syntax
     - INC(R)
   * - Assembled
     -
   * - Binary
     - 0110RRRR
   * - Decimal
     - 96, then incrementing by 1 until 111
   * - Hexadecimal
     - 0x60, then incrementing by 1 until 0x6F
   * - Symbolic
     - .. image:: images/inc-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - inc_

.. rubric:: Detailed Description

The address contained within the specified register pair designates either
a particular DATA RAM data character, a DATA RAM status character,
a RAM output port, or a ROM input/output port.
However, the address designates all of these simultaneously; it is up to
the programmer to then write the correct I/O or RAM instruction to access
the proper entity.

The disassembly of the instruction below shows how the register pair are
represented in the opcode.

.. image:: images/src.png
   :scale: 50%
   :align: center

The register specified in the lower 4 bits of the instruction is incremented by 1.
The carry bit will remain unchanged. If the register specified contains a value of 0b1111
and an INC instruction is applied, the register will contain a value of 0b0000, but
the carry bit will remain unchanged


.. rubric:: Example program

::

    / Example program
    / Loads the Accumulator with a value of 2
    / places that value in Register 6
    / increments Register 6
    / Register 6 contains a value of 3
            org    ram
            ld     2
            xch    6
            inc    6
            end



.. _inc: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
