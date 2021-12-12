.. _hardware-machine-bbl:

BBL
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Load Accumulator Immediate
   * - Function
     - The 4 bits of data, DDDD stored in the OPA field of the insruction word | br| 
       are loaded into the accumulator. The previous contents of the acummulator | br |
       are lost. The carry/link bit is unaffected.
   * - Syntax
     - LDM(D)
   * - Assembled
     -
   * - Binary
     - 1101 DDDD
   * - Decimal
     - 192, then incrementing by 1 until 207 (1st word).
   * - Hexadecimal
     - 0xC0, then incrementing by 1 until 0xCF (1st word).
   * - Symbolic
     - .. image:: images/ldm-sym.png
          :scale: 50%
   * - Execution
     - 1 word, 8-bit code and an execution time of 10.3 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - bbl_

.. rubric:: Detailed Description

The program counter (address stack) is pushed down one level. 
Program control transfers to the next instruction following the last jump to 
subroutine (:ref:`JMS <hardware-machine-jms>`) instruction. 

The 4 bits of data DDDD stored in the OPA portion of the instruction are loaded to the accumulator.

BBL is used to return from a subroutine to main program. The carry bit is not affected.

.. image:: images/bbl.png
   :scale: 50%
   :align: center


.. rubric:: Note

In the example :ref:`here <jms_ref1>`, the BBL instruction loads the value
6 into the accumulator. The address 013 is read into the program counter, and 
program execution proceeds with the XCH instruction.

.. _bbl: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
