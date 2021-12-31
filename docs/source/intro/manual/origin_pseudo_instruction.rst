.. _origin:

Origin
======

.. include:: ../../global.rst

Two forms of the instruction are acceptable:

.. list-table:: 

   * - Form 1
     - Form 2
   * - .. image:: /intro/manual/images/origin-diag1.png
          :scale: 50%
          :align: center
     - .. image:: /intro/manual/images/origin-diag2.png
          :scale: 50%
          :align: center

As shown above, the equals sign may appear in the "label" or the "code" field.

.. rubric:: Description:

The assembler's location counter is set to the value of 'Exp'. 
The next machine instruction or data byte generated will be assembled at address 'Exp'.

.. rubric: Example: 

::

        Label   Code    Operand
        =       0
                JUN     LO
                =       512
        LO,     LDM     7


The JUN instruction will be assembled in locations 0 and 1 of ROM or program
RAM. |br| 
The location counter is then set to 512, causing the LDM instruction to be assembled at location 512, 
the first location on the second memory page. 
|br| The JUN will therefore cause a jump to location 512.

.. note:: The pseudo instruction also makes it possible to assemble constant data values into a program. |br| For a description of how to do this, !!!! see Section 3.2.2  !!!!

