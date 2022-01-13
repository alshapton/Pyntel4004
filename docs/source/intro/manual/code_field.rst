.. _code_field:

Code Field
==========

.. include:: ../../global.rst



This field contains a code which identifies the machine operation 
(add, subtract, jump, etc.) to be performed: hence the term operation 
code or op-code. The instructions described in  Sections 3. 3 thru 3.11, 
are each identified by a mnemonic label which must appear in the code field. 
For example, since the "jump unconditionally" instruction is identified by the 
letters "JUN", these letters must appear in the code field to identify the 
instruction as "jump unconditionally".

There must be at least one space following the code field. Thus:

::
    
    LAB,    JUN     AWY

is legal, but

::
    
    LAB,    JUNAWY

is illegal.