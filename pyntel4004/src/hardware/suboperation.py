# Sub-operation methods

def set_carry(self):
    # Set the carry bit
    self.CARRY = 1
    return self.CARRY


def reset_carry(self):
    # Reset the carry bit
    self.CARRY = 0
    return self.CARRY


def increment_register(self, register: int):
    self.REGISTERS[register] = self.REGISTERS[register] + 1
    if (self.REGISTERS[register] > self.MAX_4_BITS):
        self.REGISTERS[register] = 0
    return None


def write_pin10(self, value: int):
    if (value == 0 or value == 1):
        self.PIN_10_SIGNAL_TEST = value
        return True
    else:
        return False

# Miscellaneous read/write operations


def read_complement_carry(self):
    # Return the complement of the carry bit
    return 1 if self.CARRY == 0 else 0


def write_to_stack(self, value: int):
    # Note that the stack pointer begins at 2, and then moves toward 0
    #
    #  After 2 writes         After 3 writes         After 3 writes
    #  +------------+         +------------+         +------------+
    #  |     a      |         |      a     |  <--SP  |      d     |
    #  |     b      |         |      b     |         |      b     |  <---SP
    #  |            |  <--SP  |      c     |         |      c     |
    #  +------------+         +------------+         +------------+
    #
    # Note that after 3 writes, address "a" is lost

    self.STACK[self.STACK_POINTER] = value
    self.STACK_POINTER = self.STACK_POINTER - 1
    if (self.STACK_POINTER == -1):
        self.STACK_POINTER = 2
    return None


def read_from_stack(self):
    # Note that the stack pointer begins at 2, and then moves toward 0
    #
    #    First Read             Second Read          Third Read
    #    +------------+        +------------+        +------------+
    #    |     d      |  <--SP |      d     |        |      d     |
    #    |     b      |        |      b     |        |      b     |  <---SP
    #    |     c      |        |      c     |  <--SP |      c     |
    #    +------------+        +------------+        +------------+
    #

    if (self.STACK_POINTER == 2):
        self.STACK_POINTER = 0
    else:
        self.STACK_POINTER = self.STACK_POINTER + 1
    value = self.STACK[self.STACK_POINTER]

    return value

# Utility operations


def ones_complement(self, value: str):
    # Perform a one's complement
    # i.e. invert all the bits
    binary = bin(value)[2:].zfill(4)
    ones = ''
    for x in range(4):
        if (binary[x] == '1'):
            ones = ones + '0'
        else:
            ones = ones + '1'
    return ones


def decimal_to_binary(self, decimal: int):
    # Convert decimal to binary
    binary = bin(decimal)[2:].zfill(4)
    return binary


def binary_to_decimal(self, binary: str):
    # Convert binary to decimal
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal
