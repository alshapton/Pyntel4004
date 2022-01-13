.. _rom:

Read-Only Memory (ROM)
======================

.. include:: ../../global.rst

Read-only memory (ROM) is used for storing program instructions and constant data which is 
never changed by the program. 

This is because the program can read locations in ROM, but can never alter (write) ROM locations.

ROM may be visualized as below; as a sequence of bytes, each of which may store 8 bits 
(two hexadecimal digits). 

Up to 4096 bytes of ROM may be present, and an individual byte is addressed by its sequential 
number between 0 and 4095.

ROM is further divided into pages, each of which contains 256 bytes. 

Thus: |br|
locations 0 through 255 comprise page 0 of ROM, |br|
locations 256 through 511 comprise page 1 and so on.


.. image:: images/rom-layout.png
           :scale: 50%
           :align: center


.. note:: Instruction Positioning

    As described :ref:`here<instruction_summary>`, certain instructions function differently when located
    in the last byte (or bytes) of a page than when located elsewhere.
