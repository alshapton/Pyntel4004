.. _hardware-machine-rdm:

RDM
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Read RAM character
   * - Function
     - The content of the previously selected RAM main memory character |br|
       is transferred to the accumulator. 
   * - Syntax
     - WRM
   * - Assembled
     -
   * - Binary
     - 11101001
   * - Decimal
     - 233
   * - Hexadecimal
     - 0xE9
   * - Symbolic
     - .. image:: images/rdm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - rdm_

.. rubric:: Detailed Description

The DATA RAM data character specified by the last SRC instruction is loaded into the accumulator.

The carry bit and the data character are not affected.

The opcode for this instruction does not contain any additional data:

.. image:: images/rdm.png
   :scale: 50%
   :align: center


.. rubric:: Example program

The example will read the contents of DATA RAM data character number 5 of register 0 of chip 0
of the currently selected DATA RAM bank into the accumulator.

::

  / Example program
          FIM   2P  5
          SRC   2P
          RDM


.. _rdm: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
