.. _io_and_ram_instructions:

Io And Ram Instructions
=======================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   /hardware/machine/wrm
   /hardware/machine/wmp
   /hardware/machine/wrr
   /hardware/machine/wpm
   /hardware/machine/wrn
   /hardware/machine/rdm
   /hardware/machine/rdr
   /hardware/machine/rdn
   /hardware/machine/adm
   /hardware/machine/sbm


This section describes instructions which access DATA RAM characters or perform input or output operations. 
One instruction, :ref:`WPM<hardware-machine-wpm>`, allows the programmer to read or write 8-bit program RAM locations. 
These instructions use addresses selected by the :ref:`DCL<hardware-machine-dcl>` and :ref:`SRC<hardware-machine-src>` instructions.

Instructions in this class occupy one byte as follows:

.. image:: /intro/manual/images/io-ram-diag.png
          :scale: 50%
          :align: center

.. list-table:: 
   :header-rows: 1

   * - Code
     - Description
   * - :ref:`hardware-machine-wrm`
     - Write accumulator to RAM.
   * - :ref:`hardware-machine-wmp`
     - Write accumulator to RAM output port
   * - :ref:`hardware-machine-wrr`
     - Write accumulator to ROM output port.
   * - :ref:`hardware-machine-wpm`
     - Write accumulator to Program RAM.
   * - :ref:`hardware-machine-wrn`
     - Write accumulator to RAM status char&cter n (n = 0, 1, 2 or 3).
   * - :ref:`hardware-machine-rdm`
     - Load accumulator from RAM.
   * - :ref:`hardware-machine-rdr`
     - Load accumulator from ROM input port.
   * - :ref:`hardware-machine-rdn`
     - Load accumulator from RAM status character n (n = 0, 1, 2 or 3) .
   * - :ref:`hardware-machine-adm`
     - Add RAM data plus carry to accumulator.
   * - :ref:`hardware-machine-sbm`
     - Subtract RAM data from accumulator with borrow.
