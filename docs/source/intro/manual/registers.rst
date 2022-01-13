.. _registers:

Working (Index) Registers
=========================

.. include:: ../../global.rst

The 4004 provides the programmer with sixteen 4-bit registers. 

These may be referenced individually by the integers 0 through 15 ,
or as 8 register pairs by the even integers from 0 through 14. 

The register pairs may also be referenced by the symbols 0P through 7P. 

These correspondences are shown as follows:



.. list-table:: 
   :header-rows: 0

   * - .. centered:: Individual Registers
     - .. centered:: Register Pairs
   * - .. image:: images/registers-indiv.png
          :scale: 50%
          :align: center

     - .. image:: images/register-pairs.png
          :scale: 50%
          :align: center
   

Text © intel4004.com