.. _is_format:

Instruction Set Format
======================

.. include:: ../global.rst

Machine instructions
--------------------
The Intel 4004 chip Machine Instructions consist of:

- 1 word instructions - 8 bits requiring 8 clock periods (instruction cycle)
- 2 word instructions - 16 bits requiring 16 clock periods (2 instruction cycles)

Each instruction is divided into two 4 bit fields. The upper 4 bits is the **OPR** field
containing the operation code. The lower 4 bits is the **OPA** field containing the modifier.

For 2 word instructions, the second word contains the address information or data.

The upper 4 bits (OPR) will always be fetched befor the lower 4 bits (OPA) during M :subscript:`1` and M :subscript:`2` times respectively.
   
.. image:: ./images/if-1.png
          :scale: 50%
          :align: center


.. image:: ./images/if-2.png
          :scale: 50%
          :align: center


Input/Output, RAM, and Accumulator Group instructions
-----------------------------------------------------
In these instructions (which are all 1 word),the OPR contains a 4 bit code which identifies either the I/O 
instruction or the accumulator group instruction, and the OPA contains a 4 bit code which identifies the
operation to be performed. The table below illustrates the contents of each 4 bit field:

.. image:: ./images/if-3.png
          :scale: 50%
          :align: center
