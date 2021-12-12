"""Definition of an i4004 processor."""


class Processor:

    """Functionality and chracteristics of an i4004 processor."""

    #  pylint: disable=import-outside-toplevel
    # Turn off import-outside-toplevel warning for this class
    from hardware import opcodes

    # Import opcode mechanics
    from hardware.instructions.accumulator import clb, clc, cma, cmc, \
        daa, dac, iac, kbp, ral, rar, stc, tcc, tcs
    from hardware.instructions.idx import fin, inc
    from hardware.instructions.idxacc import add, ld, sub, xch
    from hardware.instructions.immediate import fim, ldm
    from hardware.instructions.io_ram import adm, rdm, rdr, rd0, rd1, rd2, \
        rd3, sbm, wmp, wpm, wrm, wrr, wr0, wr1, wr2, wr3
    from hardware.instructions.memory_select import dcl, src
    from hardware.instructions.nop import nop
    from hardware.instructions.subroutine import bbl, jms
    from hardware.instructions.transfer_control import isz, jcn, jin, jun

    from hardware.suboperations.other import decode_command_register, \
        read_all_command_registers
    from hardware.suboperations.utility import binary_to_decimal, \
        convert_decimal_to_n_bit_slices, convert_to_absolute_address, \
        decimal_to_binary, ones_complement, split_address8

    # Import suboperations
    from hardware.suboperations.accumulator import check_overflow, \
        read_acbr, read_accumulator, set_accumulator
    from hardware.suboperations.carry import read_carry, \
        read_complement_carry, reset_carry, set_carry
    from hardware.suboperations.init import init_command_registers, \
        init_pram, init_ram, init_registers, init_rom, init_stack, \
        init_wpm_counter
    from hardware.suboperations.pc import inc_pc_by_page, increment_pc, \
        is_end_of_page, read_program_counter
    from hardware.suboperations.pin10 import read_pin10, write_pin10
    from hardware.suboperations.ram import rdx, read_all_pram, read_all_ram, \
        read_all_ram_ports, read_all_status_characters, \
        read_current_ram_bank, write_ram_status
    from hardware.suboperations.registers import increment_register, \
        insert_register, insert_registerpair, read_all_registers, \
        read_register, read_registerpair
    from hardware.suboperations.rom import read_all_rom, read_all_rom_ports
    from hardware.suboperations.stack import read_all_stack, read_from_stack, \
        read_stack_pointer, write_to_stack
    from hardware.suboperations.wpm import flip_wpm_counter, read_wpm_counter
    #  pylint: enable=import-outside-toplevel

    # Operations to read the processor components
    # Some used internally,

    # i4004 Processor characteristics
    MAX_4_BITS = 15             # Maximum value 4 bits can hold

    MEMORY_SIZE_RAM = 4096      # Number of 4-bit words in RAM
    MEMORY_SIZE_ROM = 4096      # Number of 4-bit words in ROM
    MEMORY_SIZE_PRAM = 4096     # Number of 4-bit words in PRAM
    PAGE_SIZE = 256             # Number of 4-bit words in a memory page
    STACK_SIZE = 3              # Number of 12-bit registers in the stack
    NO_REGISTERS = 16           # Number of registers
    NO_ROM_PORTS = 16           # Number of ROM output ports
    NO_CHIPS_PER_BANK = 4       # Number of memory chips per Data RAM Bank
    RAM_BANK_SIZE = 256         # Size in 4-bit addresses of a Data RAM Bank
    RAM_CHIP_SIZE = 64          # Size in 4-bit addresses of a single RAM chip
    RAM_REGISTER_SIZE = 16      # Number of 4-bit registers in a RAM chip
    MSB = 8                     # Most significant bit of a 4 bit register
    NO_DRB = 8                  # Number of Data RAM Banks (0-7)
    NO_COMMAND_REGISTERS = 8    # Number of command registers
    NO_STATUS_REGISTERS = 4     # Number of Status registers per memory chip
    NO_STATUS_CHARACTERS = 4    # Number of Status chars per status register

    # Instruction table
    INSTRUCTIONS = opcodes.instructions.opcodes

    # Initialise processor

    def __init__(self):
        """Initialise an instance of the processor."""
        # Set up all the internals of the processor
        self.COMMAND_REGISTERS = []  # Command Register (Select Data RAM Bank)

        # Set up RAM
        self.RAM = []                                # RAM
        self.RAM_PORT = [[0 for _bank in range(4)]   # RAM Ports
                         for _chip in range(8)]
        # Set up ROM
        self.ROM = []                                # ROM
        self.ROM_PORT = [0 for _bank in range(self.NO_ROM_PORTS)]   # ROM ports

        self.PRAM = []               # Program RAM
        self.REGISTERS = []          # Registers (4-bit)
        self.STACK = []              # The stack - 3 x 12-bit registers

        self.COMMAND_REGISTER = 0

        # Set up RAM status characters
        self.STATUS_CHARACTERS = [[[[0 for _char in range(4)]
                                    for _reg in range(4)]
                                   for _chip in range(4)]
                                  for _bank in range(self.NO_DRB)]

        # Creation of processor simulated hardware
        # Pin 10 on the physical chip is the "test" pin
        # and can be read by the JCN instruction
        self.PIN_10_SIGNAL_TEST = 0
        self.write_pin10(0)

        # Initialise Internals
        self.set_accumulator(0)      # Initialise the accumulator
        self.ACBR = 0                # Accumulator Buffer Register
        self.STACK_POINTER = 2       # Stack Pointer
        self.PROGRAM_COUNTER = 0     # Program Counter - 12-bit value

        self.init_stack()
        self.init_command_registers()
        self.init_registers()
        self.init_pram()
        self.init_ram()
        self.init_rom()
        self.CURRENT_DRAM_BANK = 0   # Current Data RAM Bank
        self.CURRENT_RAM_BANK = 0    # Current Program RAM Bank
        self.reset_carry()           # Reset the carry bit
        self.init_wpm_counter()      # WPM Counter (Left/Right flip)

    #  END OF PROCESSOR DEFINITION
