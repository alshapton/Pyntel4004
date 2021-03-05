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
    self.PRAM = [[[0 for _j in range(7)]
                 for _k in range(255)]
                 for _l in range(3)]
