.. _data_ram:

Data RAM Addressing
======================

.. include:: ../../global.rst

To address a location in DATA RAM, the :ref:`DCL<hardware-machine-dcl>` and 
:ref:`SRC<hardware-machine-src>` instructions must be used as described 
:ref:`here<ram>`.

When the DCL has chosen a specific DATA RAM bank, the address of the specific character 
is held in a register pair accessed by the SRC instruction.