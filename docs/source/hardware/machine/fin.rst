.. _hardware-machine-fin:


FIN
===
.. include:: ../../global.rst

.. toctree::
   :hidden:

TO COMPLETE

.. list-table:: 
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Fetch Indirect
   * - Function
     - 8 bits of immediate data are loaded into the register pair specified by RP.
   * - Syntax
     - FIM  RPp   Data
   * - Assembled
     -
   * - Binary
     - 0010RRR0 DDDDDDDD
   * - Decimal
     - 32, then incrementing by 2 until 46 (1st word)
   * - Hexadecimal
     - 0x20, then incrementing by 2 until 0x2E (1st word)
   * - Symbolic
     - .. image:: images/fim-sym.png
          :scale: 50%
   * - Execution
     - 2 words, 8-bit code and an execution time of 21.6 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - fin_

.. rubric:: Detailed Description

The 8 bits of immediate data (word 2) are loaded into the named register pair.
The register pairs are defined within the opcode as shown below:

.. image:: images/fim.png
   :scale: 50%
   :align: center

.. rubric:: Example program

::

    / Example program
            org    ram
            fim    2  254
            end

This will load the 8-bit decimal value 254 into the register pair 2 & 3.


After execution, register 2 will contain the upper 4 bits of the value 254,
with register 3 containing the lower 4 bits i.e. 15 and 14 respectively.


This is because decimal 254 is represented as 0xFE, so register 2 will contain 0xF (decimal 15),
while register 3 will contain 0xE (decimal 14).


.. _fin: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L389