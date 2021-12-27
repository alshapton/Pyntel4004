.. _input_and_output:

Input and Output
================

.. include:: ../../global.rst

Programs communicate with the outside world via 4-bit input or output ports. |br| |br|
The operation of these ports is controlled by special I/O instructions described :ref:`here<io_and_ram_instructions>`.
These ports are physically located on the same devices which hold ROMs and DATA RAMs; therefore, 
they are referred to as ROM ports or RAM ports. These
are **totally** separate from the instruction or data locations provided in ROM or RAM, 
and should not be confused with them. |br|
The ports associated with RAMs may be used only for output.

Text © intel4004.com