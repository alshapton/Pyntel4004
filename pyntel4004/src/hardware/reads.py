# Read Processor Methods

def read_all_registers(self):
    return(self.REGISTERS)


def read_all_command_registers(self):
    return(self.COMMAND_REGISTERS)


def read_all_ram(self):
    return(self.RAM)


def read_all_rom(self):
    return(self.ROM)


def read_all_pram(self):
    return(self.PRAM)


def read_all_stack(self):
    return(self.STACK)


def read_accumulator(self):
    return(self.ACCUMULATOR)


def read_all_rom_ports(self):
    return(self.ROM_PORT)


def read_all_ram_ports(self):
    return(self.RAM_PORT)


def read_current_ram_bank(self):
    return(self.CURRENT_RAM_BANK)


def read_carry(self):
    return(self.CARRY)


def read_pin10(self):
    return(self.PIN_10_SIGNAL_TEST)


def read_wpm_counter(self):
    return(self.WPM_COUNTER)


def read_acbr(self):
    return(self.ACBR)


def read_program_counter(self):
    return(self.PROGRAM_COUNTER)


def read_stack_pointer(self):
    return(self.STACK_POINTER)


def read_all_status_characters(self):
    return(self.STATUS_CHARACTERS)
