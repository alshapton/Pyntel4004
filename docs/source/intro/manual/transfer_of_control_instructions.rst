.. _transfer_of_control_instructions:

Transfer Of Control Instructions
================================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   ../../hardware/machine/jun
   ../../hardware/machine/jin
   ../../hardware/machine/jcn
   ../../hardware/machine/isz


.. list-table:: 
   :header-rows: 1

   * - Code
     - Symbolic
     - Description
   * - :ref:`hardware-machine-jun`
     - .. image:: ../../hardware/machine/images/jun-sym.png
          :scale: 25%
     - Jump to location ADDR.
   * - :ref:`hardware-machine-jin`
     - .. image:: ../../hardware/machine/images/jin-sym.png
          :scale: 25%
     - Jump to the address in register pair RP.
   * - :ref:`hardware-machine-jcn`
     - .. image:: ../../hardware/machine/images/jcn-sym.png
          :scale: 25%
     - Jump to ADDR if condition true.
   * - :ref:`hardware-machine-isz`
     - .. image:: ../../hardware/machine/images/isz-sym.png
          :scale: 25%
     - Increment REG. If zero, skip. If non zero, jump to ADDR
