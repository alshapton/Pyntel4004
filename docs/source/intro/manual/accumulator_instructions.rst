.. _accumulator_instructions:

Accumulator Instructions
========================


.. include:: ../../global.rst



.. toctree::
   :hidden:

   /hardware/machine/clb
   /hardware/machine/clc
   /hardware/machine/iac
   /hardware/machine/cmc
   /hardware/machine/cma
   /hardware/machine/ral
   /hardware/machine/rar
   /hardware/machine/tcc
   /hardware/machine/dac
   /hardware/machine/tcs
   /hardware/machine/stc
   /hardware/machine/daa
   /hardware/machine/kbp

Accumulator instructions  operate only on the contents of the accumulator and/or the carry bit.
Instructions in this class occupy one byte as follows:

.. image:: /intro/manual/images/acc-diag.png
          :scale: 50%
          :align: center

.. list-table::  
   :header-rows: 1

   * - Code
     - Description
   * - :ref:`hardware-machine-clb`
     - Clear both the accumulator and carry.
   * - :ref:`hardware-machine-clc`
     - Clear carry.
   * - :ref:`hardware-machine-iac`
     - Increment accumulator.
   * - :ref:`hardware-machine-cmc`
     - Complement carry.
   * - :ref:`hardware-machine-cma`
     - Complement each bit of the accumulator.
   * - :ref:`hardware-machine-ral`
     - Rotate accumulator left through carry.
   * - :ref:`hardware-machine-rar`
     - Rotate accumulator right through carry.
   * - :ref:`hardware-machine-tcc`
     - Transmit the value of the carry to the accumulator then clear carry.
   * - :ref:`hardware-machine-dac`
     - Decrement accumulator.
   * - :ref:`hardware-machine-tcs`
     - Adjust accumulator for decimal subtract.
   * - :ref:`hardware-machine-stc`
     - Set carry.
   * - :ref:`hardware-machine-daa`
     - Adjust accumulator for decimal add.
   * - :ref:`hardware-machine-kbp`
     - Convert accumulator from 1 of n code to a binary value.
