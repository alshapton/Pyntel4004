.. _transfer_of_control_instructions:

Transfer Of Control Instructions
================================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   /hardware/machine/jun
   /hardware/machine/jin
   /hardware/machine/jcn
   /hardware/machine/isz

Instructions which alter the normal execution sequence of instructions.

.. list-table:: 
   :header-rows: 1

   * - Code
     - Description
   * - :ref:`hardware-machine-jun`
     - Jump to location ADDR.
   * - :ref:`hardware-machine-jin`
     - Jump to the address in register pair RP.
   * - :ref:`hardware-machine-jcn`
     - Jump to ADDR if condition true.
   * - :ref:`hardware-machine-isz`
     - Increment REG. If zero, skip. If non zero, jump to ADDR
