.. _hardware-machine-isz:

ISZ
===

.. include:: ../../global.rst

.. toctree::
   :hidden:

.. list-table::
   :widths: 25 75
   :header-rows: 0


   * - Name
     - Increment index register skip if zero
   * - Function
     - The content of the designated index register is incremented by 1. |br|
       The accumulator and carry/link are unaffected. If the result is zero, |br|
       the next instruction after ISZ is executed. |br|
       If the result is different from 0, program control is transferred |br|
       to the instruction located at the 8 bit address A2A2A2A2, A1A1A1A1 on |br|
       the same page (ROM) where the ISZ instruction is located.
       
   * - Syntax
     - ISZ(R, 8-bit address)
   * - Assembled
     -
   * - Binary
     - 0111R A2A2A2A2, A1A1A1A1
   * - Decimal
     - 112, then incrementing by 1 until 127 (1st word)
   * - Hexadecimal
     - 0x70, then incrementing by 1 until 0x7F (1st word)
   * - Symbolic
     - .. image:: images/isz-sym.png
          :scale: 50%
   * - Execution
     - 2 words, 8-bit code and an execution time of 10.8 |mu| sec
   * - Side-effects
     - Not Applicable
   * - Implemented
     - isz_

.. rubric:: Detailed Description

The index register specified by REG is incremented by one. 
If the result is 0000, program execution continues with the
next sequential instruction. 
If the result does not equal 0000 the 8 bits specified by
ADDR replace the lowest 8 bits of the program counter.
The highest 4 bits of the program counter are unchanged.
Therefore, program execution continues at the specified
address on the same page of memory in which the ISZ
instruction is located.

The carry bit is not affected

.. image:: images/isz.png
   :scale: 50%
   :align: center

NOTE:
If ISZ is located on words 254 and 255 of a ROM page, when ISZ |br|
is executed and the result is not zero, program control is transferred |br|
to the 8-bit address located on the next page in sequence and not |br|
on the same page where ISZ is located.
.. rubric:: Example program

::

    / Example program
            org    ram
            fim    0p  
    lp      xch    2
            isz    0   lp
            end


The FIM instruction loads registers 0 and 1 with O.
The XCH is then executed.
Program execution continues until the ISZ is reached.
Register 0 is incremented to contain 1, and since this
result is non-zero, program control is transferred back to location labelled "lp".
This process continues until register 0 = 1111. 
Then the ISZ increments register 0 producing a result of OOOO, and execution continues
with the instruction at after the ISZ (which is the END).


.. _src: https://github.com/alshapton/Pyntel4004/blob/5e9f4253d8a412f6a3ec8fca5e3acfc88e0861c3/pyntel4004/src/hardware/machine.py#L208
