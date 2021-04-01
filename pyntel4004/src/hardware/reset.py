# Initialisation methods

def init_ram(self):
    for _i in range(self.MEMORY_SIZE_RAM):
        self.RAM.append(0)


def init_command_registers(self):
    for _i in range(self.NO_COMMAND_REGISTERS):
        self.COMMAND_REGISTERS.append(0)


def init_registers(self):
    for _i in range(self.NO_REGISTERS):
        self.REGISTERS.append(0)


def init_stack(self):
    for _i in range(self.STACK_SIZE):
        self.STACK.append(0)


def init_rom(self):
    for _i in range(self.MEMORY_SIZE_ROM):
        self.ROM.append(0)


def init_dram(self):
    for _i in range(self.MEMORY_SIZE_PRAM):
        self.PRAM.append(0)


def init_wpm_counter(self):
    self.WPM_COUNTER = 'LEFT'
