class processor:

    # Import processor internals
    import hardware.opcodes
    from hardware.reset import init_stack, init_command_registers, \
        init_ram, init_rom, init_dram, init_registers, init_wpm_counter

    from hardware.instructions.nop import nop
    from hardware.instructions.idx import inc, fin
    from hardware.instructions.accumulator import clb, clc, iac, cmc, \
        cma, ral, rar, tcc, dac, tcs, stc, daa, kbp

    from hardware.machine import ldm, ld, xch, add, sub, \
        bbl, jin, src, jun, jms, jcn, isz, fim, \
        dcl, wrm, wr0, wr1, wr2, wr3, wmp, wrr, rd0, rd1, \
        rd2, rd3, wpm
    from hardware.suboperation import set_carry, reset_carry,  \
        increment_register, write_pin10, read_complement_carry, \
        write_to_stack, read_from_stack, ones_complement, \
        decimal_to_binary, binary_to_decimal, insert_register, \
        is_end_of_page, inc_pc_by_page, insert_registerpair, \
        read_registerpair, read_register

    # Operations to read the processor components
    # Some used internally,
    from hardware.reads import read_all_registers, read_all_ram, \
        read_all_rom, read_all_pram, read_accumulator, \
        read_current_ram_bank, read_carry, read_pin10, read_all_stack, \
        read_all_command_registers

    # i4004 Processor characteristics
    MAX_4_BITS = 15             # Maximum value 4 bits can hold

    MEMORY_SIZE_RAM = 4096      # Number of 4-bit words in RAM
    MEMORY_SIZE_ROM = 4096      # Number of 4-bit words in ROM
    MEMORY_SIZE_PRAM = 4096     # Number of 4-bit words in PRAM
    PAGE_SIZE = 256             # Number of 4-bit words in a memory page
    STACK_SIZE = 3              # Number of 12-bit registers in the stack
    NO_REGISTERS = 16           # Number of registers
    NO_ROM_PORTS = 32           # Number of ROM output ports
    NO_CHIPS_PER_BANK = 4       # Number of memory chips per Data RAM Bank
    RAM_BANK_SIZE = 256         # Size in 4-bit addresses of a Data RAM Bank
    RAM_CHIP_SIZE = 64          # Size in 4-bit addresses of a single RAM chip
    RAM_REGISTER_SIZE = 16      # Number of 4-bit registers in a RAM chip
    NO_DRB = 8                  # Number of Data RAM Banks (0-7)
    NO_COMMAND_REGISTERS = 8    # Number of command registers
    NO_STATUS_REGISTERS = 4     # Number of Status registers per memory chip
    NO_STATUS_CHARACTERS = 4    # Number of Status chars per status register

    # Creation of processor internals

    ACCUMULATOR = 0         # Initialise the accumulator
    ACBR = 0                # Accumulator Buffer Register
    CARRY = 0               # Reset the carry bit
    COMMAND_REGISTERS = []  # Command Register (Select Data RAM Bank)
    CURRENT_DRAM_BANK = 0   # Current Data RAM Bank
    PROGRAM_COUNTER = 0     # Program Counter - 12-bit value

    # Set up RAM
    RAM = []                                # RAM
    RAM_PORT = [[0 for _bank in range(8)]   # RAM Ports
                for _chip in range(4)]
    # Set up ROM
    ROM = []                                # ROM
    ROM_PORT = [0 for _bank in range(16)]   # ROM ports

    PRAM = []               # Program RAM
    REGISTERS = []          # Registers (4-bit)
    STACK = []              # The stack - 3 x 12-bit registers
    STACK_POINTER = 2       # Stack Pointer

    # Set up RAM status characters
    STATUS_CHARACTERS = [[[[0 for _char in range(4)]
                         for _reg in range(4)]
                         for _chip in range(4)]
                         for _bank in range(8)]
    WPM_COUNTER = 'LEFT'    # WPM Counter (Left/Right flip)

    # Creation of processor simulated hardware

    # Pin 10 on the physical chip is the "test" pin
    # and can be read by the JCN instruction
    PIN_10_SIGNAL_TEST = 0

    # Instruction table
    INSTRUCTIONS = hardware.opcodes.instructions.opcodes

    # Initialise processor

    def __init__(self):
        # Initialise all the internals of the processor
        self.ACCUMULATOR = 0
        self.ACBR = 0
        self.CURRENT_RAM_BANK = 0
        self.PROGRAM_COUNTER == 0
        self.init_stack()
        self.init_command_registers()
        self.init_registers()
        self.init_dram()
        self.init_ram()
        self.init_rom()
        self.reset_carry()
        self.init_wpm_counter()

#  END OF PROCESSOR DEFINITION
