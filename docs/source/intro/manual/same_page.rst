.. _same_page:

Same Page Addressing
====================

.. include:: ../../global.rst

Some instructions supply two hexadecimal digits which replace the lowest 8 bits of the 
program counter, addressing a ROM or program RAM location on the same page as the 
instruction being executed.
|br|

.. note:: 

    (Two addresses are on the same page if the highest order hexadecimal digit of their addresses are equal. 
    See Section 2.3.1)

The following instruction provides an example of same page addressing: 

.. code-block::

    Jump on condition 2 to location 0F of this page 

|just|


This instruction would appear in memory as follows:

.. image:: /intro/manual/images/same-page-diag.png
          :scale: 50%
          :align: center

The identical instruction encoding 0x120F, if located at location 0x501, would cause a jump to memory address 0x50F.