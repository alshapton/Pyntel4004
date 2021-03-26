def inc(self, register: int):
    """
    Name:           Increment index register
    Function:       The 4 bit content of the designated index register is
                    incremented by 1.
                    The index register is set to zero in case of overflow.
    Syntax:         INC <register>
    Assembled:      0110 <RRRR>
    Symbolic:       (RRRR) +1 --> RRRR
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   The carry bit is not affected.
    """

    self.increment_register(register)
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.REGISTERS[register]