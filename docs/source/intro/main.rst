.. _main:

Intel 4004 Chip History
=======================


.. image:: images/intel4004chip.png
          :scale: 50%


Background

In 1969 Busicom contracted Intel to design a set of chips to be used in a new high perfomance calculator.
Ted Hoff, Federico Faggin and Stan Mazor came up with a design that involved four different chips.
The CPU was eventually to be called a microprocessor.

Later Intel negotiated for a return of the rights for the chips, which had gone to Busicom in the original contract.


The 4000 Family (A.K.A. Busicom Chip Set / MCS-4 Chip Set)

The 4000 family consisted of four different chips:

 - a 2048-bit ROM with a 4-bit programmable input-output port (:ref:`4001<4001>`) 
 - a 4-registers x 20-locations x 4-bit RAM data memory with a 4-bit output port (:ref:`4002<4002>`)
 - an input-output expansion chip, consisting of a static shift register with serial input and serial and parallel output (:ref:`4003<4003>`)
 - a 4-bit CPU chip (:ref:`4004<4004>`)


Other chips in the 4xxx family were:

 - an 8-bit address latch for access to standard memory chips, and one built-in 4-bit chip select and I/O port (4008)
 - a program and I/O access converter to standard memory and I/O chips (4009)

 
 - an 8192-bit( 1024 × 8) ROM w/ 4-bit I/O Ports (4208)
 - a general purpose Bye I/O port (4211))
 - a keyboard/display interface (4269)
 - a memory interface (combined functions of 4008 and 4009)(4289)
 - an 8k mask-programming ROM (4308)
 - a 16384-bit (2048 × 8) Static ROM (4316)
 - a 2048-bit (256 × 8) EPROM (4702)
 - a 5.185 MHz Clock Generator Crystal for 4004/4201A or 4040/4201A (4801)


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

