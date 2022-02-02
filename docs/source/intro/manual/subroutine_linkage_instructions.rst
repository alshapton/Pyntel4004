.. _subroutine_linkage_instructions:

Subroutine Linkage Instructions
===============================


.. include:: ../../global.rst

.. toctree::
   :hidden:

   /hardware/machine/jms
   /hardware/machine/bbl

This section describes the commands which call and cause return from subroutines. |br|
They cause a transfer of program control and use the address stack XXXX(see Sections 2.4 and 2.7•7)XXX

.. list-table::  
   :header-rows: 1

   * - Code
     - Description
   * - :ref:`hardware-machine-jms`
     - Call subroutine and push return address onto stack.
   * - :ref:`hardware-machine-bbl`
     - Return from subroutine and load accumulator with immediate DATA.
