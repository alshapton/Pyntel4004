.. _io_and_ram_instructions:

Io And Ram Instructions
=======================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   ../../hardware/machine/wrm
   ../../hardware/machine/wmp
   ../../hardware/machine/wrr
   ../../hardware/machine/wpm
   ../../hardware/machine/wrn
   ../../hardware/machine/rdm
   ../../hardware/machine/rdr
   ../../hardware/machine/rdn
   ../../hardware/machine/adm
   ../../hardware/machine/sbm


.. list-table:: 
   :header-rows: 1

   * - Code
     - Symbolic
     - Description
   * - :ref:`hardware-machine-wrm`
     - .. image:: ../../hardware/machine/images/wrm-sym.png
          :scale: 25%
     - Write accumulator to RAM.
   * - :ref:`hardware-machine-wmp`
     - .. image:: ../../hardware/machine/images/wmp-sym.png
          :scale: 25%
     - Write accumulator to RAM output port
   * - :ref:`hardware-machine-wrr`
     - .. image:: ../../hardware/machine/images/wrr-sym.png
          :scale: 25%
     - Write accumulator to ROM output port.
   * - :ref:`hardware-machine-wpm`
     - .. image:: ../../hardware/machine/images/wpm-sym.png
          :scale: 25%
     - Write accumulator to Program RAM.
   * - :ref:`hardware-machine-wrn`
     - .. image:: ../../hardware/machine/images/wrn-sym.png
          :scale: 25%
     - Write accumulator to RAM status char&cter n (n = 0, 1, 2 or 3).
   * - :ref:`hardware-machine-rdm`
     - .. image:: ../../hardware/machine/images/rdm-sym.png
          :scale: 25%
     - Load accumulator from RAM.
   * - :ref:`hardware-machine-rdr`
     - .. image:: ../../hardware/machine/images/rdr-sym.png
          :scale: 25%
     - Load accumulator from ROM input port.
   * - :ref:`hardware-machine-rdn`
     - .. image:: ../../hardware/machine/images/rdn-sym.png
          :scale: 25%
     - Load accumulator from RAM status character n (n = 0, 1, 2 or 3) .
   * - :ref:`hardware-machine-adm`
     - .. image:: ../../hardware/machine/images/adm-sym.png
          :scale: 25%
     - Add RAM data plus carry to accumulator.
   * - :ref:`hardware-machine-sbm`
     - .. image:: ../../hardware/machine/images/sbm-sym.png
          :scale: 25%
     - Subtract RAM data from accumulator with borrow.
