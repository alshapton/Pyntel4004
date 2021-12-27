.. _subroutine_linkage_instructions:

Subroutine Linkage Instructions
===============================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   ../../hardware/machine/jms
   ../../hardware/machine/bbl


.. list-table:: 
   :header-rows: 1

   * - Code
     - Symbolic
     - Description
   * - :ref:`hardware-machine-jms`
     - .. image:: ../../hardware/machine/images/jms-sym.png
          :scale: 25%
     - Call subroutine and push return address onto stack.
   * - :ref:`hardware-machine-bbl`
     - .. image:: ../../hardware/machine/images/bbl-sym.png
          :scale: 25%
     - Return from subroutine and load accumulator with immediate DATA.
