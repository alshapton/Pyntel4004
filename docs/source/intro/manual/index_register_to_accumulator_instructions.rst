.. _index_register_to_accumulator_instructions:

Index Register To Accumulator Instructions
==========================================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   ../../hardware/machine/add
   ../../hardware/machine/sub
   ../../hardware/machine/ld
   ../../hardware/machine/xch


.. list-table:: 
   :header-rows: 1

   * - Code
     - Symbolic
     - Description
   * - :ref:`hardware-machine-add`
     - .. image:: ../../hardware/machine/images/add-sym.png
          :scale: 25%
     - Add REG plus carry bit to the accumulator.
   * - :ref:`hardware-machine-sub`
     - .. image:: ../../hardware/machine/images/sub-sym.png
          :scale: 25%
     - Subtract REG from accumulator with borrow.
   * - :ref:`hardware-machine-ld`
     - .. image:: ../../hardware/machine/images/ld-sym.png
          :scale: 25%
     - Load accumulator from REG.
   * - :ref:`hardware-machine-xch`
     - .. image:: ../../hardware/machine/images/xch-sym.png
          :scale: 25%
     - Exchange the contents of accumulator and REG.
