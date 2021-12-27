.. _index_register_instructions:

Index Register Instructions
===========================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   ../../hardware/machine/fin
   ../../hardware/machine/inc

The index register instructions involve index registers or register pairs. 
|
These instructions occupy one byte as follows:


.. list-table:: 
   :header-rows: 1

   * - FIN
     - INC
   * - .. image:: ../../hardware/machine/images/fin.png
          :scale: 50%
     - .. image:: ../../hardware/machine/images/inc.png
          :scale: 50%


.. list-table:: 
   :header-rows: 1

   * - Code
     - Symbolic
     - Description
   * - :ref:`hardware-machine-fin`
     - .. image:: ../../hardware/machine/images/fin-sym.png
          :scale: 25%
     - Load RP with 8 bits of ROM data addressed by register pair 0.
   * - :ref:`hardware-machine-inc`
     - .. image:: ../../hardware/machine/images/inc-sym.png
          :scale: 25%
     - Increment register REG.
