.. _floating_point:

Floating Point Numbers
======================

.. include:: ../../global.rst

|just|

The structure of DATA RAM chips is fully described in Section 2.3.3.

One use to which a 16-character DATA RAM register and its 4 status 
characters can be put is to store a 16 digit decimal floating point number.

Such a number can be represented in the form:


.. raw:: html

    <h1 align="center"> 
    
|plusmn| .DDDDDDDDDDDDDDDD * 10 |supplusminus| :superscript:`EE`  

|just|

The 16 data characters of a RAM register could then be used to store the digits 
of the number, two status characters could be used to hold the digits of the 
exponent, while the remaining two status characters would hold the signs of the 
number and its exponent.
|br|
If a value of **one** is chosen to represent minus and a value of **zero** is 
chosen to represent plus, status characters 0 and 1 hold the exponent digits, 
status character 2 holds the exponent sign and status character 3 holds 
the number's sign, then the number

.. raw:: html

    <h1 align="center"> 
    
|plusmn| .1234567890812489 * 10 :superscript:`-23`  

|just|

would appear in a RAM register as follows:

.. image:: /intro/manual/images/fp-diag.png
          :scale: 50%
          :align: center

