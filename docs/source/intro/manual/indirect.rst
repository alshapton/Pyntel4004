.. _indirect:

Indirect Addressing
===================

.. include:: ../../global.rst


With indirect addressing, an instruction specifies a register pair which in turn holds 
an 8 bit value used for same page addressing (Section 2. 7.2). Suppose that registers
4 and 5 hold the 4-bit hexadecimal numbers 1 and B, respectively. Then the instruction:

.. code-block::

    Jump indirect to contents of register pair 4
    
|just|

This instruction would appear in memory as follows:

.. image:: /intro/manual/images/indirect-diag.png
          :scale: 50%
          :align: center

The 3 indicates a "jump indirect" instruction; the 5 indicates that the 
address indicated on this page is held in register pair 4. 
If register pair 4 had held the hex numbers 3 and C, a jump to location 0x23C would have occurred.