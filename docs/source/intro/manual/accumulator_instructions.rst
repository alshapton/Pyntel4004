.. _accumulator_instructions:

Accumulator Instructions
========================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   ../../hardware/machine/clb
   ../../hardware/machine/clc
   ../../hardware/machine/iac
   ../../hardware/machine/cmc
   ../../hardware/machine/cma
   ../../hardware/machine/ral
   ../../hardware/machine/rar
   ../../hardware/machine/tcc
   ../../hardware/machine/dac
   ../../hardware/machine/tcs
   ../../hardware/machine/stc
   ../../hardware/machine/daa
   ../../hardware/machine/kbp


.. list-table:: 
   :header-rows: 1

   * - Code
     - Symbolic
     - Description
   * - :ref:`hardware-machine-clb`
     - .. image:: ../../hardware/machine/images/clb-sym.png
          :scale: 25%
     - Clear both the accumulator and carry.
   * - :ref:`hardware-machine-clc`
     - .. image:: ../../hardware/machine/images/clc-sym.png
          :scale: 25%
     - Clear carry.
   * - :ref:`hardware-machine-iac`
     - .. image:: ../../hardware/machine/images/iac-sym.png
          :scale: 25%
     - Increment accumulator.
   * - :ref:`hardware-machine-cmc`
     - .. image:: ../../hardware/machine/images/cmc-sym.png
          :scale: 25%
     - Complement carry.
   * - :ref:`hardware-machine-cma`
     - .. image:: ../../hardware/machine/images/cma-sym.png
          :scale: 25%
     - Complement each bit of the accumulator.
   * - :ref:`hardware-machine-ral`
     - .. image:: ../../hardware/machine/images/ral-sym.png
          :scale: 25%
     - Rotate accumulator left through carry.
   * - :ref:`hardware-machine-rar`
     - .. image:: ../../hardware/machine/images/rar-sym.png
          :scale: 25%
     - Rotate accumulator right through carry.
   * - :ref:`hardware-machine-tcc`
     - .. image:: ../../hardware/machine/images/tcc-sym.png
          :scale: 25%
     - Transmit the value of the carry to the accumulator then clear carry.
   * - :ref:`hardware-machine-dac`
     - .. image:: ../../hardware/machine/images/dac-sym.png
          :scale: 25%
     - Decrement accumulator.
   * - :ref:`hardware-machine-tcs`
     - .. image:: ../../hardware/machine/images/tcs-sym.png
          :scale: 25%
     - Adjust accumulator for decimal subtract.
   * - :ref:`hardware-machine-stc`
     - .. image:: ../../hardware/machine/images/stc-sym.png
          :scale: 25%
     - Set carry.
   * - :ref:`hardware-machine-daa`
     - .. image:: ../../hardware/machine/images/daa-sym.png
          :scale: 25%
     - Adjust accumulator for decimal add.
   * - :ref:`hardware-machine-kbp`
     - .. image:: ../../hardware/machine/images/kbp-sym.png
          :scale: 25%
     - Convert accumulator from 1 of n code to a binary value.
