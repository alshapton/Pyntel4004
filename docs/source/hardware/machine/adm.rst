.. _hardware-machine-adm:

ADM
===

.. include:: ../../global.rst

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Addd DATA RAM to accumulator with carry
   * - Function
     - The content of the previously selected RAM main memory |br|
       character is added to the accumulator with carry.
   * - Syntax
     - ADM
   * - Assembled
     -
   * - Binary
     - 11101011
   * - Decimal
     - 235
   * - Hexadecimal
     - 0xEB
   * - Symbolic
     - .. image:: images/adm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - Depending on the result, the carry bit is reset or set.
   * - Implemented
     - adm_

.. rubric:: Detailed Description

The DATA RAM data character specified by the last SRC instruction, plus the
carry bit, are added to the accumulator.
The carry bit will be set if the result generates a carry, otherwise.
the data character is not affected.


The opcode for this instruction does not contain any additional data:

.. image:: images/adm.png
   :scale: 50%
   :align: center

.. rubric:: Example

In this example, the carry bit = 0, the accumulator contains a value of 10, and DATA
RAM character 0 of register 0 of chip 0 contains 7.
::

    / Example
            FIM   0P    0
            SRC   0P
            ADM

The `adm` operation above is carried out as follows:

::

        Accumulator   =   1 0 1 0
     Data Character   =   0 1 1 1    
     Carry            =         0  
                          -------
        Result      1     0 0 0 1  
                

The accumulator contains 1 and the carry bit is set.

.. _sbm: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
