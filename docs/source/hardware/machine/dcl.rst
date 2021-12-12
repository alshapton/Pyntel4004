.. _hardware-machine-dcl:

DCL
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Designate Command Line
   * - Function
     - Select a RAM bank
   * - Syntax
     - DCL
   * - Assembled
     -
   * - Binary
     - 11111101
   * - Decimal
     - 253
   * - Hexadecimal
     - 0xFD
   * - Symbolic
     - .. image:: images/dcl-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - dcl_

.. rubric:: Detailed Description

The content of the three least significant accumulator bits is transferred to the 
comand control register within the CPU. 
This instruction provides RAM bank selection when multiple RAM banks are used, since there could be up to 8 RAM banks.

(If no DCL instruction is sent out, RAM Bank number zero is automatically selected after 
application of at least one RESET). 

DCL remains latched until it is changed.

The opcode for this instruction does not contain any additional data:

.. image:: images/dcl.png
   :scale: 50%
   :align: center

The least significant 3 bits of the accumulator determine which RAM bank is selected (detailled in the
table below, along with the bits of the command register).


.. list-table::
   :widths: 15 15 15 15 15 15
   :header-rows: 1


   * - Accumulator |br| 
     - CM-RAM :subscript:`i` |br| enabled
     -
     -
     -
     - RAM |br| Bank
   * - 0x000
     - CM-RAM :subscript:`0`
     -
     -
     -
     - 0
   * - 0x001
     -
     - CM-RAM :subscript:`1`
     -
     -
     - 1
   * - 0x010
     -
     - 
     - CM-RAM :subscript:`2`
     -
     - 2
   * - 0x100
     -
     - 
     -
     - CM-RAM :subscript:`3`
     - 3
   * - 0x011
     -
     - CM-RAM :subscript:`1`
     - CM-RAM :subscript:`2`
     -
     - 4
   * - 0x101
     -
     - CM-RAM :subscript:`1`
     -
     - CM-RAM :subscript:`3`
     - 5
   * - 0x110
     -
     -
     - CM-RAM :subscript:`2`
     - CM-RAM :subscript:`3`
     - 6
   * - 0x111
     -
     - CM-RAM :subscript:`1`
     - CM-RAM :subscript:`2`
     - CM-RAM :subscript:`3`
     - 7


.. _dcl: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
