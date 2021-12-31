.. _index_register_to_accumulator_instructions:

Index Register To Accumulator Instructions
==========================================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   /hardware/machine/add
   /hardware/machine/sub
   /hardware/machine/ld
   /hardware/machine/xch

This section describes instructions which involve an operation between an index register and the accumulator. 

Instructions in this class occupy one byte as follows:

.. image:: /intro/manual/images/idx-acc-diag.png
          :scale: 50%
          :align: center

.. list-table:: 
   :header-rows: 1

   * - Code
     - Description
   * - :ref:`hardware-machine-add`
     - Add REG plus carry bit to the accumulator.
   * - :ref:`hardware-machine-sub`
     - Subtract REG from accumulator with borrow.
   * - :ref:`hardware-machine-ld`
     - Load accumulator from REG.
   * - :ref:`hardware-machine-xch`
     - Exchange the contents of accumulator and REG.
