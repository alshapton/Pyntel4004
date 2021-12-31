.. _direct:

Direct Addressing
=================

.. include:: ../../global.rst



With direct addressing, as the name implies, an instruction provides an exact memory address. 
The following instruction provides an example of direct addressing:

.. code-block::

    Jump to location 3A2 

|just|

This instruction is represented by 4 hexadecimal digits in RQM or program RAM. 
The first digit is a 4, signifying a jump instruction, while the final 3 digits specify the address.

This instruction would appear in memory as follows:

.. image:: /intro/manual/images/direct-diag.png
          :scale: 50%
          :align: center