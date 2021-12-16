.. _hardware-machine-rdn:

RDn
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Read Data from Ram Status Character
   * - Function
     - The 4-bits of status character n for the previously |br|
       selected  RAM register are transferred to the accumulator. 
   * - Syntax
     - RD0, RD1, RD2, RD3
   * - Assembled
     -
   * - Binary
     - 11101100, 11101101, 11101110, 11101111, 
   * - Decimal
     - 236, 237, 238, 239
   * - Hexadecimal
     - 0xEC, 0xED, 0xEE, 0xEF
   * - Symbolic
     - .. image:: images/rdn-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - rdn_

.. rubric:: Detailed Description

The DATA RAM status character whose number from 0 to 3 is specified by 
"n", associated with the DATA RAM register specified by the last SRC 
instruction, is loaded into the accumulator.

The carry bit and the status character are not affected.

The DATA RAM status character is encoded in the opcode as shown below:

.. image:: images/rdn.png
   :scale: 50%
   :align: center


.. rubric:: Example program

The example program will read the contents of DATA RAM status character 3 
of register 0 of chip 0 of the currently selected DATA RAM bank into the accumulator.

::

    / Example program
    FIM   2P  5
    SRC   2P
    RD3



.. _rdn: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
