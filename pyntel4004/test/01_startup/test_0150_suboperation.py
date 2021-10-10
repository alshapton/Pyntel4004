# Using pytest
# Test the suboperations of an instance of an i4004(processor)

import sys
import pickle

import pytest

sys.path.insert(1, '../src')

import hardware.suboperation  # noqa
from hardware.processor import processor  # noqa
from hardware.exceptions import IncompatibleChunkBit, InvalidBitValue, \
        InvalidChunkValue, InvalidEndOfPage, InvalidPin10Value, \
        InvalidRegister, InvalidRegisterPair,\
        NotABinaryNumber, ProgramCounterOutOfBounds, \
        ValueOutOfRangeForBits, ValueOutOfRangeForStack,\
        ValueTooLargeForAccumulator, \
        ValueTooLargeForRegister, ValueTooLargeForRegisterPair  # noqa
from hardware.suboperation import encode_command_register  # noqa

##############################################################################
#                      Set/Reset Carry Flag                                  #
##############################################################################


def test_suboperation_set_carry():
    """Tests for SET Carry Flag."""
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.CARRY = 1

    # Perform the operation under test:
    # setting carry
    processor.set_carry(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_carry() == chip_base.read_carry()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_reset_carry():
    """Tests for RESET Carry Flag."""
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.CARRY = 0

    # Perform the operation under test:
    # resetting carry
    processor.reset_carry(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_carry() == chip_base.read_carry()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                      Read Complement of Carry Flag                         #
##############################################################################
@pytest.mark.parametrize("carry", [0, 1])
def test_suboperation_read_complement_carry(carry):
    """Read Complement of Carry Flag."""
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_test.CARRY = carry
    complement_carry = 1 if carry == 0 else 0

    # Perform the operation under test:
    # N/A

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # Also ensure the carry flag is still correctly set
    assert chip_test.read_complement_carry() == complement_carry
    assert chip_test.read_carry() == chip_test.CARRY

    # Pickling each chip and comparing will show equality or not.
    # N/A

##############################################################################
#                      Insert Register                                       #
##############################################################################


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_suboperation_insert_register_scenario1(register):
    """Test Insert Registerr functionality."""
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.REGISTERS[register] = 5

    # Perform the operation under test:
    # insert a value of 5 into each register
    processor.insert_register(chip_test, register, 5)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_insert_register_scenario2():
    """Test Insert Register failure case #1."""
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value larger than the register can hold
    with pytest.raises(Exception) as e:
        assert processor.insert_register(chip_test, 3, 25)
    assert str(e.value) == "Register: 3,Value: 25"
    assert e.type == ValueTooLargeForRegister

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_register(3) == 0

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_insert_register_scenario3():
    """Test Insert Register failure case #2."""
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value into an invalid register
    with pytest.raises(Exception) as e:
        assert processor.insert_register(chip_test, 25, 3)
    assert str(e.value) == "Register: 25"
    assert e.type == InvalidRegister

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    # N/A - the operation will completely fail - the chip will be as it was
    # in the base state

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

##############################################################################
#                      Read Register                                         #
##############################################################################


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_suboperation_read_register_scenario1(register):
    """Test Read Register function."""
    chip_test = processor()

    # Perform the operation under test:
    # insert a value of 5 into each register
    chip_test.REGISTERS[register] = 5

    # Simulate conditions at end of operation in base chip
    # N/A

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_register(register) == 5


@pytest.mark.parametrize("register", [-1, 16])  # noqa
def test_suboperation_read_register_scenario2(register):
    """Test Read Register failure case #1."""
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to read from a non-existent register
    with pytest.raises(Exception) as e:
        assert processor.read_register(chip_test, register)
    assert str(e.value) == "Register:" + str(register)
    assert e.type == InvalidRegister

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                      Insert Register Pair                                  #
##############################################################################
@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])  # noqa
def test_suboperation_insert_registerpair_scenario1(registerpair):
    """Test Insert Register Pair function."""
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.REGISTERS[registerpair * 2] = 15
    chip_base.REGISTERS[(registerpair * 2) + 1] = 14

    # Insert a value of 254 into a registerpair
    processor.insert_registerpair(chip_test, registerpair, 254)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_insert_registerpair_scenario2():
    """Test Insert Register Pair failure case #1."""
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value larger than the register pair can hold
    with pytest.raises(Exception) as e:
        assert processor.insert_registerpair(chip_test, 3, 300)
    assert str(e.value) == "Register Pair: 3,Value: 300"
    assert e.type == ValueTooLargeForRegisterPair

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_register(3) == 0

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_insert_registerpair_scenario3():
    """Test Insert Register Pair failure case #2."""
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value into an invalid registerpair
    with pytest.raises(Exception) as e:
        assert processor.insert_registerpair(chip_test, 9, 3)
    assert str(e.value) == "Register Pair: 9"
    assert e.type == InvalidRegisterPair

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    # N/A - the operation will completely fail - the chip will be as it was
    # in the base state

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                      Read Register Pair                                    #
##############################################################################
def test_suboperation_read_registerpair():
    """Test Read Register Pair function."""
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_test.REGISTERS[6] = 15
    chip_test.REGISTERS[7] = 14

    # Perform the operation under test:
    # Read a value from register pair 3 (registers 6 and 7)
    assert chip_test.read_registerpair(3) == 254

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # N/A


@pytest.mark.parametrize("registerpair", [-1, 8])  # noqa
def test_suboperation_read_registerpair_scenario2(registerpair):
    """Test Read Register Pair failure case #1."""
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to read from a non-existent register pair
    with pytest.raises(Exception) as e:
        assert processor.read_registerpair(chip_test, registerpair)
    assert str(e.value) == "Register Pair: " + str(registerpair)
    assert e.type == InvalidRegisterPair

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

##############################################################################
#                      Increment Program Counter                             #
##############################################################################


@pytest.mark.parametrize("words", [0, 1, 2])  # noqa
def test_suboperation_increment_pc_scenario1(words):
    """Test increment PC scenario 1."""
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.PROGRAM_COUNTER = chip_test.MEMORY_SIZE_RAM - 10 + words

    # Simulate conditions at end of operation in base chip
    chip_test.PROGRAM_COUNTER = chip_test.MEMORY_SIZE_RAM - 10

    # Increment the Program Counter by 0, then 1, then 2 words
    processor.increment_pc(chip_test, words)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_increment_pc_scenario2():
    """Test Increment PC scenario 2 (failure case)."""
    chip_base = processor()
    chip_test = processor()

    chip_test.PROGRAM_COUNTER = chip_test.MEMORY_SIZE_RAM - 1
    chip_base.PROGRAM_COUNTER = chip_test.PROGRAM_COUNTER

    # Perform the operation under test:
    # attempting to increment the Program Counter beyond the end of memory
    with pytest.raises(Exception) as e:
        assert processor.increment_pc(chip_test, 2)
    assert str(e.value) == "Program counter attempted to be set to 4097"
    assert e.type == ProgramCounterOutOfBounds

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()


##############################################################################
#                      Increment Program Counter by Page                     #
##############################################################################
@pytest.mark.parametrize("pc", [45, 2045])  # noqa
def test_suboperation_increment_pc_counter_by_page_scenario1(pc):
    """Test Increment PC by page function."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    chip_test.PROGRAM_COUNTER = pc
    chip_base.PROGRAM_COUNTER = pc + chip_base.PAGE_SIZE - 1

    # Increment the Program Counter by 1 page
    chip_test.PROGRAM_COUNTER = processor.inc_pc_by_page(chip_test, pc)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("pc", [3841, 4090])  # noqa
def test_suboperation_increment_pc_counter_by_page_scenario2(pc):
    """Test Increment PC by page failure."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    chip_test.PROGRAM_COUNTER = pc + chip_base.PAGE_SIZE
    chip_base.PROGRAM_COUNTER = pc + chip_base.PAGE_SIZE

    # attempting to increment the Program Counter beyond the end of memory
    with pytest.raises(Exception) as e:
        assert processor.inc_pc_by_page(chip_test, pc)
    assert str(e.value) == "Program counter attempted to be set to " + str(pc + chip_base.PAGE_SIZE)  # noqa
    assert e.type == ProgramCounterOutOfBounds

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Is Program Counter at the end of a Page                     #
##############################################################################
def test_suboperation_is_at_end_of_page_scenario1():
    """Test to see if the PC is at the end of the page."""
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A

    # Check for end of page (5 different page values)
    assert processor.is_end_of_page(chip_test, 0, 1) is False
    assert processor.is_end_of_page(chip_test, 0, 2) is False

    assert processor.is_end_of_page(chip_test, 2209, 1) is False
    assert processor.is_end_of_page(chip_test, 2209, 2) is False

    assert processor.is_end_of_page(chip_test, 254, 1) is False
    assert processor.is_end_of_page(chip_test, 254, 2) is False

    assert processor.is_end_of_page(chip_test, 255, 1) is True
    assert processor.is_end_of_page(chip_test, 255, 2) is False

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # N/A

    # Pickling each chip and comparing will show equality or not.
    # N/A


def test_suboperation_is_at_end_of_page_scenario2():
    """Test failure scenarios for "is PC at end of page" function."""
    chip_test = processor()
    chip_base = processor()
    pc = -1
    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    chip_test.PROGRAM_COUNTER = pc + chip_base.PAGE_SIZE
    chip_base.PROGRAM_COUNTER = pc + chip_base.PAGE_SIZE

    # attempting to increment the Program Counter beyond the end of memory -
    # use negative numbers, zeros etc to try and "trip up" the function
    try:
        processor.is_end_of_page(chip_test, -1, -222)
        processor.is_end_of_page(chip_test, 0, 0)
        processor.is_end_of_page(chip_test, -22222, 30000)
        processor.is_end_of_page(chip_test, 4096, 0)
        processor.is_end_of_page(chip_test, 4096, -1)

    except pytest.raises(Exception) as e:
        assert False, (e.type == InvalidEndOfPage)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check for Accumulator Overflow                              #
##############################################################################
@pytest.mark.parametrize("values", [[16, 2, 1], [15, 15, 0], [0, 0, 0], [99, 85, 1]])  # noqa
def test_suboperation_check_for_overflow(values):
    """Test check for overflow function."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.ACCUMULATOR = values[1]
    chip_base.CARRY = values[2]

    chip_test.ACCUMULATOR = values[0]
    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # Check for overflow

    acc, carry = processor.check_overflow(chip_test)
    assert acc == values[1]
    assert carry == values[2]

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check "set accumulator"                                     #
##############################################################################
@pytest.mark.parametrize("value", [-1, 0, 14, 15])  # noqa
def test_suboperation_set_accumulator_scenario1(value):
    """Test set accumulator."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.ACCUMULATOR = value

    chip_test.set_accumulator(value)
    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # N/A

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", [16, 20, 257])
def test_suboperation_set_accumulator_scenario2(value):
    """Test set accumulator function failure."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to set the accumulator to an invalid value
    with pytest.raises(Exception) as e:
        assert processor.set_accumulator(chip_test, value)
    assert str(e.value) == ' Value: ' + str(value)
    assert e.type == ValueTooLargeForAccumulator

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Increment Register                                    #
##############################################################################
@pytest.mark.parametrize("value", [0, 3, 9, 14])  # noqa
def test_suboperation_test_inc_register_scenario1(value):
    """Test increment register scenario 1."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip (use R4)
    chip_test.REGISTERS[4] = value
    chip_base.REGISTERS[4] = value + 1

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    chip_test.increment_register(4)
    assert processor.read_register(chip_test, 4) == value + 1

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_test_inc_register_scenario2():
    """Test increment register scenario 2."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A    # Simulate conditions at end of operation in base chip (use R4)
    chip_test.REGISTERS[4] = 15
    chip_base.REGISTERS[4] = 0

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # This is a rollover - i.e. 15 incremented becomes 0

    processor.increment_register(chip_test, 4)
    assert processor.read_register(chip_test, 4) == 0

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", [16, 20, 257])
def test_suboperation_test_increment_register_scenario3(value):
    """Test increment register failure."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use an invalid register
    with pytest.raises(Exception) as e:
        assert processor.increment_register(chip_test, value)
    assert str(e.value) == 'Register: ' + str(value)
    assert e.type == InvalidRegister

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check set PIN_10_SIGNAL_TEST                                #
##############################################################################
@pytest.mark.parametrize("value", [0, 1])  # noqa
def test_suboperation_test_write_pin10_scenario1(value):
    """Test reading of PIN 10."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.PIN_10_SIGNAL_TEST = value

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    chip_test.write_pin10(value)
    assert chip_test.read_pin10() == value

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", [-1, 2, 23, 98, -3])
def test_suboperation_test_write_pin_10_scenario2(value):
    """Test PIN 10 failure."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use an invalid PIN10 value
    with pytest.raises(Exception) as e:
        assert processor.write_pin10(chip_test, value)
    assert str(e.value) == 'PIN 10 attempted to be set to ' + str(value)
    assert e.type == InvalidPin10Value

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Flip WPM Counter                                      #
##############################################################################
@pytest.mark.parametrize("value", ['LEFT', 'RIGHT'])  # noqa
def test_suboperation_test_flip_wpm_counter_scenario1(value):
    """Test WPM counter flip function."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.WPM_COUNTER = value
    chip_test.WPM_COUNTER = value

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # flip the WPM counter 4 times, such that it returns to the original value
    for _i in range(4):
        chip_test.flip_wpm_counter()
    assert chip_test.read_wpm_counter() == value

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Binary to decimal                                     #
##############################################################################
@pytest.mark.parametrize("value", [['0000', '0'], ['0010', '2'],
                                   ['1111', '15'], ['1010', '10'],
                                   ['1100', '12'], ['11111111', '255'],
                                   ['00001111', '15'],
                                   ['100011111010', '2298'],
                                   ['010101111011', '1403'],
                                   ['11001100', '204'],
                                   ['111111111111', '4095']])  # noqa
def test_suboperation_test_binary_decimal_scenario1(value):
    """Test binary to decimal function #1."""
    chip_test = processor()
    chip_base = processor()

    # Call the binary_to_decimal method - the rest of the chip should
    # stay unchanged
    assert str(processor.binary_to_decimal(value[0])) == value[1]

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", ['-1', 'not a binary', '',
                                   'IOIOIOIOI', ' Intel4004'])
def test_suboperation_test_binary_decimal_scenario2(value):
    """Test binary to decimal function failure #2."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use an invalid binary number
    with pytest.raises(Exception) as e:
        assert processor.binary_to_decimal(value)
    if value != '':
        assert str(e.value) == '"' + value + '"'
    else:
        assert str(e.value) == '"<empty>"'

    assert e.type == NotABinaryNumber

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Decimal to Binary                                     #
##############################################################################
@pytest.mark.parametrize("value", [[0, 4, '0000'], [1, 4, '0001'],
                                   [14, 4, '1110'], [15, 4, '1111'],
                                   [8, 4, '1000'], [16, 8, '00010000'],
                                   [17, 8, '00010001'], [9, 8, '00001001'],
                                   [255, 8, '11111111'], [0, 8, '00000000'],
                                   [4095, 12, '111111111111'],
                                   [4094, 12, '111111111110'],
                                   [0, 12, '000000000000'],
                                   [2439, 12, '100110000111'],
                                   [1002, 12, '001111101010']
                                   ])  # noqa
def test_suboperation_test_decimal_to_binaryscenario1(value):
    """Test decimal to binary function."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # Attempt to convert decimal to binary (chip status should not change)
    assert processor.decimal_to_binary(value[1], value[0]) == value[2]

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", [[-1, 4], [-1, 8], [-1, 12],
                                   [16, 4], [17, 4], [256, 4],
                                   [256, 8], [257, 8],
                                   [4096, 12], [2322442, 12]])
def test_suboperation_test_decimal_to_binary_scenario2(value):
    """Test decimal to binary function failure #2."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use binary number larger than the bits will allow
    with pytest.raises(Exception) as e:
        assert processor.decimal_to_binary(value[0], value[1])
        assert str(e.value) == 'Value: ' + str(value[0]) + \
                               'Bits: ' + str(value[1])
        assert e.type == ValueOutOfRangeForBits

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", [-1, 0, 1, 2, 3, 5, 6, 7, 9,
                                   10, 11, 13, 14, 15, 16, 17])
def test_suboperation_test_decimal_to_binary_scenario3(value):
    """Test decimal to binary function failure #3."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use a bit value which is illegal
    with pytest.raises(Exception) as e:
        assert processor.decimal_to_binary(value[0], 3)
        assert str(e.value) == 'Bits: ' + str(value[1])
        assert e.type == InvalidBitValue

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check One's Complement                                      #
##############################################################################
@pytest.mark.parametrize("value", [[2, '1101', 4], [3, '1100', 4],
                                   [0, '1111', 4], [2, '11111101', 8],
                                   [3, '11111100', 8], [2, '111111111101', 12],
                                   [3, '111111111100', 12],
                                   [0, '111111111111', 12]
                                   ])  # noqa
def test_suboperation_test_ones_complement_scenario1(value):
    """Test ones_complement scenario 1."""
    # Simulate conditions at end of operation in base chip

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # Attempt to convert decimal to binary (chip status should not change)
    assert processor.ones_complement(value[0], value[2]) == value[1]


@pytest.mark.parametrize("value", [[-1, 4], [-1, 8], [-1, 12],
                                   [16, 4], [17, 4], [256, 4],
                                   [256, 8], [257, 8],
                                   [4096, 12], [2322442, 12]])
def test_suboperation_test_ones_complement_scenario2(value):
    """Test ones_complement scenario 2."""
    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use binary number larger than the bits will allow
    with pytest.raises(Exception) as e:
        assert processor.ones_complement(value[0], value[1])
        assert str(e.value) == 'Value: ' + str(value[0]) + \
                               'Bits: ' + str(value[1])
        assert e.type == ValueOutOfRangeForBits


@pytest.mark.parametrize("bits", [-1, 0, 1, 3, 5, 7, 9, 11, 13, 232])
def test_suboperation_test_ones_complement_scenario3(bits):
    """Test ones_complement scenario 2."""
    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use binary number larger than the bits will allow
    with pytest.raises(Exception) as e:
        assert processor.ones_complement(2, bits)
        assert str(e.value) == 'Value: ' + str(2) + \
                               'Bits: ' + str(bits)
        assert e.type == InvalidBitValue


##############################################################################
#                Check Insert RAM Status Character                           #
##############################################################################
@pytest.mark.parametrize("rambank", [0, 1, 2, 3])
@pytest.mark.parametrize("chip", [0, 1, 2, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
@pytest.mark.parametrize("value", [[12, 0], [12, 1], [12, 2], [12, 3]])  # noqa
def test_suboperation_test_insert_ram_status_scenario1(
            rambank, chip, register, value):
    """Test insert RAM status character."""
    chip_test = processor()
    chip_base = processor()

    # Simulate conditions at end of operation in base chip

    #
    #    Hi 2 bits of address are 1 of 4 data RAM chips
    #    Nxt 2 bits of address are 1 of 4 registers in the above chip
    #    Lo 4 bits are not relevant
    #
    #    e.g.   11110000b =240
    #
    #            Chip 3, Register 3
    #

    chip_base.set_accumulator(value[0])
    chip_base.CURRENT_RAM_BANK = rambank
    address = encode_command_register(chip, register, 0,
                                      'DATA_RAM_STATUS_CHAR')
    chip_base.COMMAND_REGISTER = address
    chip_base.STATUS_CHARACTERS[rambank][chip][register][value[1]] = value[0]

    chip_test.set_accumulator(value[0])
    chip_test.CURRENT_RAM_BANK = rambank
    chip_test.COMMAND_REGISTER = address

    # Attempt to write to the RAM status character

    processor.write_ram_status(chip_test, value[1])

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    #
    assert chip_test.STATUS_CHARACTERS[rambank][chip][register]
    [value[1]] == value[0]

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Write to Stack                                        #
##############################################################################
@pytest.mark.parametrize("value", [-1, -100, -4096, 4096, 4098])  # noqa
def test_suboperation_test_write_to_stackscenario1(value):
    """Test Write to Stack scenario 1."""
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use binary number larger than the bits will allow
    with pytest.raises(Exception) as e:
        assert processor.write_to_stack(chip_test, value)
        assert str(e.value) == 'Value: ' + str(value)
        assert e.type == ValueOutOfRangeForStack


def test_suboperation_test_write_to_stack_scenario2():
    """Test Write to Stack scenario 2."""
    chip_test = processor()
    chip_base = processor()

    # Scenario 2.0

    # Check that stack pointer is initialized and no content on the stack

    assert chip_test.STACK_POINTER == 2
    assert chip_test.STACK[2] == 0
    assert chip_test.STACK[1] == 0
    assert chip_test.STACK[0] == 0

    # Scenario 2.1

    # Attempt to write to an empty stack

    # Simulate conditions at end of operation in base chip
    chip_base.STACK_POINTER = 1
    chip_base.STACK[2] = 14

    processor.write_to_stack(chip_test, 14)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    #
    assert chip_test.STACK_POINTER == 1
    assert chip_test.STACK[2] == 14

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

    # Scenario 2.2

    # Attempt to write to a stack with one position full

    # Simulate conditions at end of operation in base chip
    chip_base.STACK_POINTER = 0
    chip_base.STACK[2] = 14
    chip_base.STACK[1] = 22

    processor.write_to_stack(chip_test, 22)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    #
    assert chip_test.STACK_POINTER == 0
    assert chip_test.STACK[2] == 14
    assert chip_test.STACK[1] == 22

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

    # Scenario 2.2

    # Attempt to write to a stack with two positions full

    # Simulate conditions at end of operation in base chip
    chip_base.STACK_POINTER = 2
    chip_base.STACK[2] = 14
    chip_base.STACK[1] = 22
    chip_base.STACK[0] = 33

    processor.write_to_stack(chip_test, 33)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    assert chip_test.STACK_POINTER == 2
    assert chip_test.STACK[2] == 14
    assert chip_test.STACK[1] == 22
    assert chip_test.STACK[0] == 33

    # Scenario 2.3

    # Attempt to write to a full stack
    # This will result in a pointer wrap-around and a value lost

    # Simulate conditions at end of operation in base chip
    chip_base.STACK_POINTER = 1
    chip_base.STACK[2] = 44
    chip_base.STACK[1] = 22
    chip_base.STACK[0] = 33

    processor.write_to_stack(chip_test, 44)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    #
    assert chip_test.STACK_POINTER == 1
    assert chip_test.STACK[2] == 44
    assert chip_test.STACK[1] == 22
    assert chip_test.STACK[0] == 33

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Read from Stack                                       #
##############################################################################
def test_suboperation_test_read_from_stack_scenarios():
    """Test Read from Stack."""
    chip_test = processor()
    chip_base = processor()

    # Initialize the stack for further testing

    processor.write_to_stack(chip_test, 11)
    processor.write_to_stack(chip_test, 22)
    processor.write_to_stack(chip_test, 33)

    processor.write_to_stack(chip_base, 11)
    processor.write_to_stack(chip_base, 22)
    processor.write_to_stack(chip_base, 33)

    # Assert that the stack is in a position that is known
    assert chip_test.STACK_POINTER == 2
    assert chip_test.STACK[2] == 11
    assert chip_test.STACK[1] == 22
    assert chip_test.STACK[0] == 33

    # Scenario (a)

    processor.read_from_stack(chip_base)
    assert processor.read_from_stack(chip_test) == 33
    assert chip_test.STACK_POINTER == 0

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

    # Scenario (b)
    processor.read_from_stack(chip_base)
    assert processor.read_from_stack(chip_test) == 22
    assert chip_test.STACK_POINTER == 1

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

    # Scenario (c)
    processor.read_from_stack(chip_base)
    assert processor.read_from_stack(chip_test) == 11
    assert chip_test.STACK_POINTER == 2

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)

    # Scenario (d) (Wrap-around)
    processor.read_from_stack(chip_base)
    assert processor.read_from_stack(chip_test) == 33
    assert chip_test.STACK_POINTER == 0

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


##############################################################################
#                Check Convert Decimal to n Bit Slices                       #
##############################################################################
@pytest.mark.parametrize("value", [[8, 4, 200, 'd', 12, 8],
                                   [8, 4, 255, 'd', 15, 15],
                                   [8, 4, 200, 'b', '1100', '1000'],
                                   [8, 4, 255, 'b', '1111', '1111'],
                                   [8, 4, 14, 'd', 0, 14],
                                   [8, 4, 14, 'b', '0000', '1110']
                                   ])  # noqa
def test_suboperation_convert_decimal_to_n_bit_slices_scenario1(value):
    """Test convert decimal to n bit slices #1."""
    chip_test = processor()
    chip_base = processor()

    # Attempt to convert decimal to binary or decimal chunks
    # (chip status should not change)
    chunks = processor.convert_decimal_to_n_bit_slices(value[0],
                value[1], value[2], value[3])  # noqa
    assert chunks == [value[4], value[5]]

    # Simulate conditions at end of operation in base chip
    # N/A

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("value", [[12, 4, 200, 'd', 0, 12, 8],
                                   [12, 4, 255, 'd', 0, 15, 15],
                                   [12, 4, 200, 'b', '0000', '1100', '1000'],
                                   [12, 4, 255, 'b', '0000', '1111', '1111'],
                                   [12, 4, 14, 'd', 0, 0, 14],
                                   [12, 4, 14, 'b', '0000', '0000', '1110'],
                                   [12, 4, 4095, 'b', '1111', '1111', '1111'],
                                   [12, 4, 4095, 'd', 15, 15, 15],
                                   [12, 4, 2003, 'b', '0111', '1101', '0011'],
                                   [12, 4, 2003, 'd', 7, 13, 3],
                                   ])  # noqa
def test_suboperation_convert_decimal_to_n_bit_slices_scenario2(value):
    """Test convert decimal to n bit slices #2."""
    chip_test = processor()
    chip_base = processor()

    # Attempt to convert decimal to binary or decimal chunks
    # (chip status should not change)
    chunks = processor.convert_decimal_to_n_bit_slices(value[0],
                value[1], value[2], value[3])  # noqa
    assert chunks == [value[4], value[5], value[6]]

    # Simulate conditions at end of operation in base chip
    # N/A

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_suboperation_convert_decimal_to_n_bit_slices_scenario3():
    """Test convert decimal to n bit slices #3."""
    # Simulate conditions at end of operation in base chip
    # N/A

    # Simulate conditions at end of operation in base chip
    # N/A - chip should have not had any changes as the operations will fail

    # attempting to use an invalid bit value (1)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(3, 1, 12, 'd')  # noqa
        assert str(e.value) == 'Bits: 3'
        assert e.type == InvalidBitValue

    # attempting to use an invalid bit value (2)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(0, 1, 12, 'd')  # noqa
        assert str(e.value) == 'Bits: 0'
        assert e.type == InvalidBitValue

    # attempting to use an invalid chunk value (1)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(12, 1, 12, 'd')  # noqa
        assert str(e.value) == 'Chunk: 1'
        assert e.type == InvalidChunkValue


def test_suboperation_convert_decimal_to_n_bit_slices_scenario4():
    """Test convert decimal to n bit slices #4."""
    # attempting to use an invalid bit value (2)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(12, 0, 12, 'd')  # noqa
        assert str(e.value) == 'Chunk: 0'
        assert e.type == InvalidChunkValue

    # attempting to use an incompatible bit/chunk combination (1)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(12, 8, 12, 'd')  # noqa
        assert str(e.value) == 'Bits: 12 Chunk: 8'
        assert e.type == IncompatibleChunkBit

    # attempting to use an incompatible bit/chunk combination (2)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(4, 8, 12, 'd')  # noqa
        assert str(e.value) == 'Bits: 4 Chunk: 8'
        assert e.type == IncompatibleChunkBit

    # attempting to use an out of range value (1)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(12, 4, -1, 'd')  # noqa
        assert str(e.value) == 'Value: -1 Bits: 12'
        assert e.type == ValueOutOfRangeForBits

    # attempting to use an out of range value (2)
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(8, 8, 257, 'd')  # noqa
        assert str(e.value) == 'Value: 12 Bits: 8'
        assert e.type == ValueOutOfRangeForBits

    # attempting to use a large value
    with pytest.raises(Exception) as e:
        assert processor.convert_decimal_to_n_bit_slices(8, 8, 8192, 'd')  # noqa
        assert str(e.value) == 'Value: 8192 Bits: 8'
        assert e.type == ValueOutOfRangeForBits
