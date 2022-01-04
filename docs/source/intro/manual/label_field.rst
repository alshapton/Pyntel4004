.. _label_field:

Label Field
===========

.. include:: ../../global.rst

This is an optional field.
If present, it must start with a letter of the alphabet. The remaining characters may be 
letters or decimal digits.
The label field must end with a comma, immediately following the last character of
the label. Labels may be any length, but should be unique in the first three characters; 
the assembler cannot always distinguish between labels whose first three characters are 
identical. If no label is present, at least one blank must begin the line.

Some examples of legal label field values are:

::
    
    CM0,
    NUL,
    EGO,

Some examples of illegal label field values are:

::
    
    4GE,        / Does not begin with a letter
    AGE         / Valid characters, but does not end with a comma  
    A/A,        / Contains invalid characters

The following label has more than 3 characters:

::
    
    STROB,

Whilst this is legal, care must be taken not to have more than one label
with the first 3 characters identical.

For example, the following labels are indistinguishable from one another and 
will result in unpredictable behaviour:

::

    LABEL,
    LAB2,
    LAB6
    LABEL29,


Since labels serve as instruction addresses, they cannot be duplicated. For example, the sequence:

::

    NOW,    JUN     NXT
            ---
            ---
            ---
    NXT,    INC     2
            ---
            ---
    NXT,    CLB

is ambiguous; the assembler cannot detennine which **NXT** address is referenced by the **JUN** instruction.