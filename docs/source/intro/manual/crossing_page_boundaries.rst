.. _crossing_page_boundaries:

Crossing Page Boundaries
========================

.. include:: ../../global.rst

As described in Section 2,  programs are held in either ROM or program
RAM, both of which are divided into pages. |br|
Each page consists of 256 8 -bit locations. |br|
Addresses 0 through 255 comprise the first page,256-511 comprise the second page, and so on.
|br|

In general, it is good programming practice to **never allow program flow to cross a page boundary 
except by using a JUN or JMS instruction**. |br|

The following example will show why this is true. Suppose a program in memory appears as below:


.. image:: /intro/manual/images/crossing-diag1.png
          :scale: 50%
          :align: center

If the accumulator is non-zero when the JCN is executed, program control will be transferred to location 200, as the programmer intended.
|br| Suppose now that an error discovered in the program requires that a new instruction be inserted somewhere between locations 200 and 253. |br|
The program would now appear as follows:

.. image:: /intro/manual/images/crossing-diag2.png
          :scale: 50%
          :align: center

Since the JCN is now located in the last two locations of a page, it functions differently. |br|
Now if the accumulator is non-zero when the JCN is executed, program control will be erroneously transferred to location 456, causing invalid results.
Since both the JUN and JMS instructions use 12-bit addresses to directly address locations on any page of memory, only these instructions should be used to cross page boundaries.