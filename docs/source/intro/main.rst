.. _main:

Intel 4004 Chip History
=======================


.. image:: images/intel4004chip.png
          :scale: 50%

.. toctree::
   :hidden:
   
   ../hardware/refs/decsub
   ../hardware/refs/decadd
   ../hardware/refs/multiadd

Background

In 1969 Busicom contracted Intel to design a set of chips to be used in a new high perfomance calculator.
Ted Hoff, Federico Faggin and Stan Mazor came up with a design that involved four different chips.
The CPU was eventually to be called a microprocessor.

Later Intel negotiated for a return of the rights for the chips, which had gone to Busicom in the original contract.


The 4000 Family (A.K.A. Busicom Chip Set / MCS-4 Chip Set)

The 4000 family consisted of four different chips:

 - a 2048-bit ROM with a 4-bit programmable input-output port (4001) 
 - a 4-registers x 20-locations x 4-bit RAM data memory with a 4-bit output port (4002)
 - an input-output expansion chip, consisting of a static shift register with serial input and serial and parallel output (4003)
 - a 4-bit CPU chip (4004)

All the chips were packaged in 16-pin, dual-in-line packages.
This package restriction was imposed by Intel’s management, who at the time
considered any package with more that 16 pins uneconomical, despite the fact
that 40-pin packages were widely used by other semiconductor companies.

This unfortunate choice considerably constrained the performance of the system.
Address and data had to be multiplexed onto the pins (one of the claims of
:download:`Patent number US3821785 <resources/US3821715.pdf>`), causing a major
penalty in the instruction cycle execution.

The instruction cycle of 10.8 microseconds could have been easily reduced to
4 microseconds by a more appropriate package choice.

The 4000-family was completed by March 1971, in production by June 1971 and
introduced to the general market in November 1971 with the name MCS-4.


Text © intel4004.com
