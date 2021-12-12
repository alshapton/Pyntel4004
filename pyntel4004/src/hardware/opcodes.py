# flake8: noqa
# Ignore format and style issues
class instructions:
    """Complete set of opcodes for the i4004 processor."""
    opcodes = [
        {"opcode": 0, "mnemonic": "nop()", "exe": 10.8, "bits": [
            "0000", "0000"], "words": 1},
        {"opcode": 1, "mnemonic": "-", "words": 1},
        {"opcode": 2, "mnemonic": "-", "words": 1},
        {"opcode": 3, "mnemonic": "-", "words": 1},
        {"opcode": 4, "mnemonic": "-", "words": 1},
        {"opcode": 5, "mnemonic": "-", "words": 1},
        {"opcode": 6, "mnemonic": "-", "words": 1},
        {"opcode": 7, "mnemonic": "-", "words": 1},
        {"opcode": 8, "mnemonic": "-", "words": 1},
        {"opcode": 9, "mnemonic": "-", "words": 1},
        {"opcode": 10, "mnemonic": "-", "words": 1},
        {"opcode": 11, "mnemonic": "-", "words": 1},
        {"opcode": 12, "mnemonic": "-", "words": 1},
        {"opcode": 13, "mnemonic": "-", "words": 1},
        {"opcode": 14, "mnemonic": "-", "words": 1},
        {"opcode": 15, "mnemonic": "-", "words": 1},
        {"opcode": 16, "mnemonic": "jcn(0,address8)", "exe": 21.6, "bits": [
            "0001", "0000", "xxxx", "xxxx"], "words": 2},
        {"opcode": 17, "mnemonic": "jcn(1,address8)", "exe": 21.6, "bits": [
            "0001", "0001", "xxxx", "xxxx"], "words": 2},
        {"opcode": 18, "mnemonic": "jcn(2,address8)", "exe": 21.6, "bits": [
            "0001", "0010", "xxxx", "xxxx"], "words": 2},
        {"opcode": 19, "mnemonic": "jcn(3,address8)", "exe": 21.6, "bits": [
            "0001", "0011", "xxxx", "xxxx"], "words": 2},
        {"opcode": 20, "mnemonic": "jcn(4,address8)", "exe": 21.6, "bits": [
            "0001", "0100", "xxxx", "xxxx"], "words": 2},
        {"opcode": 21, "mnemonic": "jcn(5,address8)", "exe": 21.6, "bits": [
            "0001", "0101", "xxxx", "xxxx"], "words": 2},
        {"opcode": 22, "mnemonic": "jcn(6,address8)", "exe": 21.6, "bits": [
            "0001", "0110", "xxxx", "xxxx"], "words": 2},
        {"opcode": 23, "mnemonic": "jcn(7,address8)", "exe": 21.6, "bits": [
            "0001", "0111", "xxxx", "xxxx"], "words": 2},
        {"opcode": 24, "mnemonic": "jcn(8,address8)", "exe": 21.6, "bits": [
            "0001", "1000", "xxxx", "xxxx"], "words": 2},
        {"opcode": 25, "mnemonic": "jcn(9,address8)", "exe": 21.6, "bits": [
            "0001", "1001", "xxxx", "xxxx"], "words": 2},
        {"opcode": 26, "mnemonic": "jcn(10,address8)", "exe": 21.6, "bits": [
            "0001", "1010", "xxxx", "xxxx"], "words": 2},
        {"opcode": 27, "mnemonic": "jcn(11,address8)", "exe": 21.6, "bits": [
            "0001", "1011", "xxxx", "xxxx"], "words": 2},
        {"opcode": 28, "mnemonic": "jcn(12,address8)", "exe": 21.6, "bits": [
            "0001", "1100", "xxxx", "xxxx"], "words": 2},
        {"opcode": 29, "mnemonic": "jcn(13,address8)", "exe": 21.6, "bits": [
            "0001", "1101", "xxxx", "xxxx"], "words": 2},
        {"opcode": 30, "mnemonic": "jcn(14,address8)", "exe": 21.6, "bits": [
            "0001", "1110", "xxxx", "xxxx"], "words": 2},
        {"opcode": 31, "mnemonic": "jcn(15,address8)", "exe": 21.6, "bits": [
            "0001", "1111", "xxxx", "xxxx"], "words": 2},
        {"opcode": 32, "mnemonic": "fim(0p,data8)", "exe": 21.6, "bits": [
            "0010", "0000", "xxxx", "xxxx"], "words": 2},
        {"opcode": 33, "mnemonic": "src(0)", "exe": 21.6, "bits": [
            "0010", "0001"], "words": 1},
        {"opcode": 34, "mnemonic": "fim(1p,data8)", "exe": 21.6, "bits": [
            "0010", "0010", "xxxx", "xxxx"], "words": 2},
        {"opcode": 35, "mnemonic": "src(1)", "exe": 21.6, "bits": [
            "0010", "0011"], "words": 1},
        {"opcode": 36, "mnemonic": "fim(2p,data8)", "exe": 21.6, "bits": [
            "0010", "0100", "xxxx", "xxxx"], "words": 2},
        {"opcode": 37, "mnemonic": "src(2)", "exe": 21.6, "bits": [
            "0010", "0101"], "words": 1},
        {"opcode": 38, "mnemonic": "fim(3p,data8)", "exe": 21.6, "bits": [
            "0010", "0110", "xxxx", "xxxx"], "words": 2},
        {"opcode": 39, "mnemonic": "src(3)", "exe": 21.6, "bits": [
            "0010", "0111"], "words": 1},
        {"opcode": 40, "mnemonic": "fim(4p,data8)", "exe": 21.6, "bits": [
            "0010", "1000", "xxxx", "xxxx"], "words": 2},
        {"opcode": 41, "mnemonic": "src(4)", "exe": 21.6, "bits": [
            "0010", "1001"], "words": 1},
        {"opcode": 42, "mnemonic": "fim(5p,data8)", "exe": 21.6, "bits": [
            "0010", "1010", "xxxx", "xxxx"], "words": 2},
        {"opcode": 43, "mnemonic": "src(5)", "exe": 21.6, "bits": [
            "0010", "1011"], "words": 1},
        {"opcode": 44, "mnemonic": "fim(6p,data8)", "exe": 21.6, "bits": [
            "0010", "1100", "xxxx", "xxxx"], "words": 2},
        {"opcode": 45, "mnemonic": "src(6)", "exe": 21.6, "bits": [
            "0010", "1101"], "words": 1},
        {"opcode": 46, "mnemonic": "fim(7p,data8)", "exe": 21.6, "bits": [
            "0010", "1110", "xxxx", "xxxx"], "words": 2},
        {"opcode": 47, "mnemonic": "src(7)", "exe": 21.6, "bits": [
            "0010", "1111"], "words": 1},
        {"opcode": 48, "mnemonic": "fin(0)", "exe": 21.6, "bits": [
            "0011", "0000"], "words": 1},
        {"opcode": 49, "mnemonic": "jin(0)", "exe": 10.8, "bits": [
            "0011", "0001"], "words": 1},
        {"opcode": 50, "mnemonic": "fin(1)", "exe": 21.6, "bits": [
            "0011", "0010"], "words": 1},
        {"opcode": 51, "mnemonic": "jin(1)", "exe": 10.8, "bits": [
            "0011", "0011"], "words": 1},
        {"opcode": 52, "mnemonic": "fin(2)", "exe": 21.6, "bits": [
            "0011", "0100"], "words": 1},
        {"opcode": 53, "mnemonic": "jin(2)", "exe": 10.8, "bits": [
            "0011", "0101"], "words": 1},
        {"opcode": 54, "mnemonic": "fin(3)", "exe": 21.6, "bits": [
            "0011", "0110"], "words": 1},
        {"opcode": 55, "mnemonic": "jin(3)", "exe": 10.8, "bits": [
            "0011", "0111"], "words": 1},
        {"opcode": 56, "mnemonic": "fin(4)", "exe": 21.6, "bits": [
            "0011", "1000"], "words": 1},
        {"opcode": 57, "mnemonic": "jin(4)", "exe": 10.8, "bits": [
            "0011", "1001"], "words": 1},
        {"opcode": 58, "mnemonic": "fin(5)", "exe": 21.6, "bits": [
            "0011", "1010"], "words": 1},
        {"opcode": 59, "mnemonic": "jin(5)", "exe": 10.8, "bits": [
            "0011", "1011"], "words": 1},
        {"opcode": 60, "mnemonic": "fin(6)", "exe": 21.6, "bits": [
            "0011", "1100"], "words": 1},
        {"opcode": 61, "mnemonic": "jin(6)", "exe": 10.8, "bits": [
            "0011", "1101"], "words": 1},
        {"opcode": 62, "mnemonic": "fin(7)", "exe": 21.6, "bits": [
            "0011", "1110"], "words": 1},
        {"opcode": 63, "mnemonic": "jin(7)", "exe": 10.8, "bits": [
            "0011", "1111"], "words": 1},
        {"opcode": 64, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0000"], "words": 2},
        {"opcode": 65, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0001"], "words": 2},
        {"opcode": 66, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0010"], "words": 2},
        {"opcode": 67, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0011"], "words": 2},
        {"opcode": 68, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0100"], "words": 2},
        {"opcode": 69, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0101"], "words": 2},
        {"opcode": 70, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0110"], "words": 2},
        {"opcode": 71, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "0111"], "words": 2},
        {"opcode": 72, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1000"], "words": 2},
        {"opcode": 73, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1001"], "words": 2},
        {"opcode": 74, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1010"], "words": 2},
        {"opcode": 75, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1011"], "words": 2},
        {"opcode": 76, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1100"], "words": 2},
        {"opcode": 77, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1101"], "words": 2},
        {"opcode": 78, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1110"], "words": 2},
        {"opcode": 79, "mnemonic": "jun(address12)", "exe": 21.6, "bits": [
            "0100", "1111"], "words": 2},
        {"opcode": 80, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0000"], "words": 2},
        {"opcode": 81, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0001"], "words": 2},
        {"opcode": 82, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0010"], "words": 2},
        {"opcode": 83, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0011"], "words": 2},
        {"opcode": 84, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0100"], "words": 2},
        {"opcode": 85, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0101"], "words": 2},
        {"opcode": 86, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0110"], "words": 2},
        {"opcode": 87, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "0111"], "words": 2},
        {"opcode": 88, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1000"], "words": 2},
        {"opcode": 89, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1001"], "words": 2},
        {"opcode": 90, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1010"], "words": 2},
        {"opcode": 91, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1011"], "words": 2},
        {"opcode": 92, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1100"], "words": 2},
        {"opcode": 93, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1101"], "words": 2},
        {"opcode": 94, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1110"], "words": 2},
        {"opcode": 95, "mnemonic": "jms(address12)", "exe": 21.6, "bits": [
            "0101", "1111"], "words": 2},
        {"opcode": 96, "mnemonic": "inc(0)", "exe": 10.8, "bits": [
            "0110", "0000"], "words": 1},
        {"opcode": 97, "mnemonic": "inc(1)", "exe": 10.8, "bits": [
            "0110", "0001"], "words": 1},
        {"opcode": 98, "mnemonic": "inc(2)", "exe": 10.8, "bits": [
            "0110", "0010"], "words": 1},
        {"opcode": 99, "mnemonic": "inc(3)", "exe": 10.8, "bits": [
            "0110", "0011"], "words": 1},
        {"opcode": 100, "mnemonic": "inc(4)", "exe": 10.8, "bits": [
            "0110", "0100"], "words": 1},
        {"opcode": 101, "mnemonic": "inc(5)", "exe": 10.8, "bits": [
            "0110", "0101"], "words": 1},
        {"opcode": 102, "mnemonic": "inc(6)", "exe": 10.8, "bits": [
            "0110", "0110"], "words": 1},
        {"opcode": 103, "mnemonic": "inc(7)", "exe": 10.8, "bits": [
            "0110", "0111"], "words": 1},
        {"opcode": 104, "mnemonic": "inc(8)", "exe": 10.8, "bits": [
            "0110", "1000"], "words": 1},
        {"opcode": 105, "mnemonic": "inc(9)", "exe": 10.8, "bits": [
            "0110", "1001"], "words": 1},
        {"opcode": 106, "mnemonic": "inc(10)", "exe": 10.8, "bits": [
            "0110", "1010"], "words": 1},
        {"opcode": 107, "mnemonic": "inc(11)", "exe": 10.8, "bits": [
            "0110", "1011"], "words": 1},
        {"opcode": 108, "mnemonic": "inc(12)", "exe": 10.8, "bits": [
            "0110", "1100"], "words": 1},
        {"opcode": 109, "mnemonic": "inc(13)", "exe": 10.8, "bits": [
            "0110", "1101"], "words": 1},
        {"opcode": 110, "mnemonic": "inc(14)", "exe": 10.8, "bits": [
            "0110", "1110"], "words": 1},
        {"opcode": 111, "mnemonic": "inc(15)", "exe": 10.8, "bits": [
            "0110", "1111"], "words": 1},
        {"opcode": 112, "mnemonic": "isz(0,address8)", "exe": 10.8, "bits": [
            "0111", "0000"], "words": 2},
        {"opcode": 113, "mnemonic": "isz(1,address8)", "exe": 10.8, "bits": [
            "0111", "0001"], "words": 2},
        {"opcode": 114, "mnemonic": "isz(2,address8)", "exe": 10.8, "bits": [
            "0111", "0010"], "words": 2},
        {"opcode": 115, "mnemonic": "isz(3,address8)", "exe": 10.8, "bits": [
            "0111", "0011"], "words": 2},
        {"opcode": 116, "mnemonic": "isz(4,address8)", "exe": 10.8, "bits": [
            "0111", "0100"], "words": 2},
        {"opcode": 117, "mnemonic": "isz(5,address8)", "exe": 10.8, "bits": [
            "0111", "0101"], "words": 2},
        {"opcode": 118, "mnemonic": "isz(6,address8)", "exe": 10.8, "bits": [
            "0111", "0110"], "words": 2},
        {"opcode": 119, "mnemonic": "isz(7,address8)", "exe": 10.8, "bits": [
            "0111", "0111"], "words": 2},
        {"opcode": 120, "mnemonic": "isz(8,address8)", "exe": 10.8, "bits": [
            "0111", "1000"], "words": 2},
        {"opcode": 121, "mnemonic": "isz(9,address8)", "exe": 10.8, "bits": [
            "0111", "1001"], "words": 2},
        {"opcode": 122, "mnemonic": "isz(10,address8)", "exe": 10.8, "bits": [
            "0111", "1010"], "words": 2},
        {"opcode": 123, "mnemonic": "isz(11,address8)", "exe": 10.8, "bits": [
            "0111", "1011"], "words": 2},
        {"opcode": 124, "mnemonic": "isz(12,address8)", "exe": 10.8, "bits": [
            "0111", "1100"], "words": 2},
        {"opcode": 125, "mnemonic": "isz(13,address8)", "exe": 10.8, "bits": [
            "0111", "1101"], "words": 2},
        {"opcode": 126, "mnemonic": "isz(14,address8)", "exe": 10.8, "bits": [
            "0111", "1110"], "words": 2},
        {"opcode": 127, "mnemonic": "isz(15,address8)", "exe": 10.8, "bits": [
            "0111", "1111"], "words": 2},
        {"opcode": 128, "mnemonic": "add(0)", "exe": 10.8, "bits": [
            "1000", "0000"], "words": 1},
        {"opcode": 129, "mnemonic": "add(1)", "exe": 10.8, "bits": [
            "1000", "0001"], "words": 1},
        {"opcode": 130, "mnemonic": "add(2)", "exe": 10.8, "bits": [
            "1000", "0010"], "words": 1},
        {"opcode": 131, "mnemonic": "add(3)", "exe": 10.8, "bits": [
            "1000", "0011"], "words": 1},
        {"opcode": 132, "mnemonic": "add(4)", "exe": 10.8, "bits": [
            "1000", "0100"], "words": 1},
        {"opcode": 133, "mnemonic": "add(5)", "exe": 10.8, "bits": [
            "1000", "0101"], "words": 1},
        {"opcode": 134, "mnemonic": "add(6)", "exe": 10.8, "bits": [
            "1000", "0110"], "words": 1},
        {"opcode": 135, "mnemonic": "add(7)", "exe": 10.8, "bits": [
            "1000", "0111"], "words": 1},
        {"opcode": 136, "mnemonic": "add(8)", "exe": 10.8, "bits": [
            "1000", "1000"], "words": 1},
        {"opcode": 137, "mnemonic": "add(9)", "exe": 10.8, "bits": [
            "1000", "1001"], "words": 1},
        {"opcode": 138, "mnemonic": "add(10)", "exe": 10.8, "bits": [
            "1000", "1010"], "words": 1},
        {"opcode": 139, "mnemonic": "add(11)", "exe": 10.8, "bits": [
            "1000", "1011"], "words": 1},
        {"opcode": 140, "mnemonic": "add(12)", "exe": 10.8, "bits": [
            "1000", "1100"], "words": 1},
        {"opcode": 141, "mnemonic": "add(13)", "exe": 10.8, "bits": [
            "1000", "1101"], "words": 1},
        {"opcode": 142, "mnemonic": "add(14)", "exe": 10.8, "bits": [
            "1000", "1110"], "words": 1},
        {"opcode": 143, "mnemonic": "add(15)", "exe": 10.8, "bits": [
            "1000", "1111"], "words": 1},
        {"opcode": 144, "mnemonic": "sub(0)", "exe": 10.8, "bits": [
            "1001", "0000"], "words": 1},
        {"opcode": 145, "mnemonic": "sub(1)", "exe": 10.8, "bits": [
            "1001", "0001"], "words": 1},
        {"opcode": 146, "mnemonic": "sub(2)", "exe": 10.8, "bits": [
            "1001", "0010"], "words": 1},
        {"opcode": 147, "mnemonic": "sub(3)", "exe": 10.8, "bits": [
            "1001", "0011"], "words": 1},
        {"opcode": 148, "mnemonic": "sub(4)", "exe": 10.8, "bits": [
            "1001", "0100"], "words": 1},
        {"opcode": 149, "mnemonic": "sub(5)", "exe": 10.8, "bits": [
            "1001", "0101"], "words": 1},
        {"opcode": 150, "mnemonic": "sub(6)", "exe": 10.8, "bits": [
            "1001", "0110"], "words": 1},
        {"opcode": 151, "mnemonic": "sub(7)", "exe": 10.8, "bits": [
            "1001", "0111"], "words": 1},
        {"opcode": 152, "mnemonic": "sub(8)", "exe": 10.8, "bits": [
            "1001", "1000"], "words": 1},
        {"opcode": 153, "mnemonic": "sub(9)", "exe": 10.8, "bits": [
            "1001", "1001"], "words": 1},
        {"opcode": 154, "mnemonic": "sub(10)", "exe": 10.8, "bits": [
            "1001", "1010"], "words": 1},
        {"opcode": 155, "mnemonic": "sub(11)", "exe": 10.8, "bits": [
            "1001", "1011"], "words": 1},
        {"opcode": 156, "mnemonic": "sub(12)", "exe": 10.8, "bits": [
            "1001", "1100"], "words": 1},
        {"opcode": 157, "mnemonic": "sub(13)", "exe": 10.8, "bits": [
            "1001", "1101"], "words": 1},
        {"opcode": 158, "mnemonic": "sub(14)", "exe": 10.8, "bits": [
            "1001", "1110"], "words": 1},
        {"opcode": 159, "mnemonic": "sub(15)", "exe": 10.8, "bits": [
            "1001", "1111"], "words": 1},
        {"opcode": 160, "mnemonic": "ld (0)", "exe": 10.8, "bits": [
            "1010", "0000"], "words": 1},
        {"opcode": 161, "mnemonic": "ld (1)", "exe": 10.8, "bits": [
            "1010", "0001"], "words": 1},
        {"opcode": 162, "mnemonic": "ld (2)", "exe": 10.8, "bits": [
            "1010", "0010"], "words": 1},
        {"opcode": 163, "mnemonic": "ld (3)", "exe": 10.8, "bits": [
            "1010", "0011"], "words": 1},
        {"opcode": 164, "mnemonic": "ld (4)", "exe": 10.8, "bits": [
            "1010", "0100"], "words": 1},
        {"opcode": 165, "mnemonic": "ld (5)", "exe": 10.8, "bits": [
            "1010", "0101"], "words": 1},
        {"opcode": 166, "mnemonic": "ld (6)", "exe": 10.8, "bits": [
            "1010", "0110"], "words": 1},
        {"opcode": 167, "mnemonic": "ld (7)", "exe": 10.8, "bits": [
            "1010", "0111"], "words": 1},
        {"opcode": 168, "mnemonic": "ld (8)", "exe": 10.8, "bits": [
            "1010", "1000"], "words": 1},
        {"opcode": 169, "mnemonic": "ld (9)", "exe": 10.8, "bits": [
            "1010", "1001"], "words": 1},
        {"opcode": 170, "mnemonic": "ld (10)", "exe": 10.8, "bits": [
            "1010", "1010"], "words": 1},
        {"opcode": 171, "mnemonic": "ld (11)", "exe": 10.8, "bits": [
            "1010", "1011"], "words": 1},
        {"opcode": 172, "mnemonic": "ld (12)", "exe": 10.8, "bits": [
            "1010", "1100"], "words": 1},
        {"opcode": 173, "mnemonic": "ld (13)", "exe": 10.8, "bits": [
            "1010", "1101"], "words": 1},
        {"opcode": 174, "mnemonic": "ld (14)", "exe": 10.8, "bits": [
            "1010", "1110"], "words": 1},
        {"opcode": 175, "mnemonic": "ld (15)", "exe": 10.8, "bits": [
            "1010", "1111"], "words": 1},
        {"opcode": 176, "mnemonic": "xch(0)", "exe": 10.8, "bits": [
            "1011", "0000"], "words": 1},
        {"opcode": 177, "mnemonic": "xch(1)", "exe": 10.8, "bits": [
            "1011", "0001"], "words": 1},
        {"opcode": 178, "mnemonic": "xch(2)", "exe": 10.8, "bits": [
            "1011", "0010"], "words": 1},
        {"opcode": 179, "mnemonic": "xch(3)", "exe": 10.8, "bits": [
            "1011", "0011"], "words": 1},
        {"opcode": 180, "mnemonic": "xch(4)", "exe": 10.8, "bits": [
            "1011", "0100"], "words": 1},
        {"opcode": 181, "mnemonic": "xch(5)", "exe": 10.8, "bits": [
            "1011", "0101"], "words": 1},
        {"opcode": 182, "mnemonic": "xch(6)", "exe": 10.8, "bits": [
            "1011", "0110"], "words": 1},
        {"opcode": 183, "mnemonic": "xch(7)", "exe": 10.8, "bits": [
            "1011", "0111"], "words": 1},
        {"opcode": 184, "mnemonic": "xch(8)", "exe": 10.8, "bits": [
            "1011", "1000"], "words": 1},
        {"opcode": 185, "mnemonic": "xch(9)", "exe": 10.8, "bits": [
            "1011", "1001"], "words": 1},
        {"opcode": 186, "mnemonic": "xch(10)", "exe": 10.8, "bits": [
            "1011", "1010"], "words": 1},
        {"opcode": 187, "mnemonic": "xch(11)", "exe": 10.8, "bits": [
            "1011", "1011"], "words": 1},
        {"opcode": 188, "mnemonic": "xch(12)", "exe": 10.8, "bits": [
            "1011", "1100"], "words": 1},
        {"opcode": 189, "mnemonic": "xch(13)", "exe": 10.8, "bits": [
            "1011", "1101"], "words": 1},
        {"opcode": 190, "mnemonic": "xch(14)", "exe": 10.8, "bits": [
            "1011", "1110"], "words": 1},
        {"opcode": 191, "mnemonic": "xch(15)", "exe": 10.8, "bits": [
            "1011", "1111"], "words": 1},
        {"opcode": 192, "mnemonic": "bbl(0)", "exe": 10.8, "bits": [
            "1100", "0000"], "words": 1},
        {"opcode": 193, "mnemonic": "bbl(1)", "exe": 10.8, "bits": [
            "1100", "0001"], "words": 1},
        {"opcode": 194, "mnemonic": "bbl(2)", "exe": 10.8, "bits": [
            "1100", "0010"], "words": 1},
        {"opcode": 195, "mnemonic": "bbl(3)", "exe": 10.8, "bits": [
            "1100", "0011"], "words": 1},
        {"opcode": 196, "mnemonic": "bbl(4)", "exe": 10.8, "bits": [
            "1100", "0100"], "words": 1},
        {"opcode": 197, "mnemonic": "bbl(5)", "exe": 10.8, "bits": [
            "1100", "0101"], "words": 1},
        {"opcode": 198, "mnemonic": "bbl(6)", "exe": 10.8, "bits": [
            "1100", "0110"], "words": 1},
        {"opcode": 199, "mnemonic": "bbl(7)", "exe": 10.8, "bits": [
            "1100", "0111"], "words": 1},
        {"opcode": 200, "mnemonic": "bbl(8)", "exe": 10.8, "bits": [
            "1100", "1000"], "words": 1},
        {"opcode": 201, "mnemonic": "bbl(9)", "exe": 10.8, "bits": [
            "1100", "1001"], "words": 1},
        {"opcode": 202, "mnemonic": "bbl(10)", "exe": 10.8, "bits": [
            "1100", "1010"], "words": 1},
        {"opcode": 203, "mnemonic": "bbl(11)", "exe": 10.8, "bits": [
            "1100", "1011"], "words": 1},
        {"opcode": 204, "mnemonic": "bbl(12)", "exe": 10.8, "bits": [
            "1100", "1100"], "words": 1},
        {"opcode": 205, "mnemonic": "bbl(13)", "exe": 10.8, "bits": [
            "1100", "1101"], "words": 1},
        {"opcode": 206, "mnemonic": "bbl(14)", "exe": 10.8, "bits": [
            "1100", "1110"], "words": 1},
        {"opcode": 207, "mnemonic": "bbl(15)", "exe": 10.8, "bits": [
            "1100", "1111"], "words": 1},
        {"opcode": 208, "mnemonic": "ldm(0)", "exe": 10.8, "bits": [
            "1101", "0000"], "words": 1},
        {"opcode": 209, "mnemonic": "ldm(1)", "exe": 10.8, "bits": [
            "1101", "0001"], "words": 1},
        {"opcode": 210, "mnemonic": "ldm(2)", "exe": 10.8, "bits": [
            "1101", "0010"], "words": 1},
        {"opcode": 211, "mnemonic": "ldm(3)", "exe": 10.8, "bits": [
            "1101", "0011"], "words": 1},
        {"opcode": 212, "mnemonic": "ldm(4)", "exe": 10.8, "bits": [
            "1101", "0100"], "words": 1},
        {"opcode": 213, "mnemonic": "ldm(5)", "exe": 10.8, "bits": [
            "1101", "0101"], "words": 1},
        {"opcode": 214, "mnemonic": "ldm(6)", "exe": 10.8, "bits": [
            "1101", "0110"], "words": 1},
        {"opcode": 215, "mnemonic": "ldm(7)", "exe": 10.8, "bits": [
            "1101", "0111"], "words": 1},
        {"opcode": 216, "mnemonic": "ldm(8)", "exe": 10.8, "bits": [
            "1101", "1000"], "words": 1},
        {"opcode": 217, "mnemonic": "ldm(9)", "exe": 10.8, "bits": [
            "1101", "1001"], "words": 1},
        {"opcode": 218, "mnemonic": "ldm(10)", "exe": 10.8, "bits": [
            "1101", "1010"], "words": 1},
        {"opcode": 219, "mnemonic": "ldm(11)", "exe": 10.8, "bits": [
            "1101", "1011"], "words": 1},
        {"opcode": 220, "mnemonic": "ldm(12)", "exe": 10.8, "bits": [
            "1101", "1100"], "words": 1},
        {"opcode": 221, "mnemonic": "ldm(13)", "exe": 10.8, "bits": [
            "1101", "1101"], "words": 1},
        {"opcode": 222, "mnemonic": "ldm(14)", "exe": 10.8, "bits": [
            "1101", "1110"], "words": 1},
        {"opcode": 223, "mnemonic": "ldm(15)", "exe": 10.8, "bits": [
            "1101", "1111"], "words": 1},
        {"opcode": 224, "mnemonic": "wrm()", "exe": 10.8, "bits": [
            "1110", "0000"], "words": 1},
        {"opcode": 225, "mnemonic": "wmp()", "exe": 10.8, "bits": [
            "1110", "0001"], "words": 1},
        {"opcode": 226, "mnemonic": "wrr()", "exe": 10.8, "bits": [
            "1110", "0010"], "words": 1},
        {"opcode": 227, "mnemonic": "wpm()", "exe": 10.8, "bits": [
            "1110", "0011"], "words": 1},
        {"opcode": 228, "mnemonic": "wr0()", "exe": 10.8, "bits": [
            "1110", "0100"], "words": 1},
        {"opcode": 229, "mnemonic": "wr1()", "exe": 10.8, "bits": [
            "1110", "0101"], "words": 1},
        {"opcode": 230, "mnemonic": "wr2()", "exe": 10.8, "bits": [
            "1110", "0110"], "words": 1},
        {"opcode": 231, "mnemonic": "wr3()", "exe": 10.8, "bits": [
            "1110", "0111"], "words": 1},
        {"opcode": 232, "mnemonic": "sbm()", "exe": 10.8, "bits": [
            "1110", "0110"], "words": 1},
        {"opcode": 233, "mnemonic": "rdm()", "exe": 10.8, "bits": [
            "1110", "1001"], "words": 1},
        {"opcode": 234, "mnemonic": "rdr()", "exe": 10.8, "bits": [
            "1110", "1010"], "words": 1},
        {"opcode": 235, "mnemonic": "adm()", "exe": 10.8, "bits": [
            "1110", "1000"], "words": 1},
        {"opcode": 236, "mnemonic": "rd0()", "exe": 10.8, "bits": [
            "1110", "1100"], "words": 1},
        {"opcode": 237, "mnemonic": "rd1()", "exe": 10.8, "bits": [
            "1110", "1101"], "words": 1},
        {"opcode": 238, "mnemonic": "rd2()", "exe": 10.8, "bits": [
            "1110", "1110"], "words": 1},
        {"opcode": 239, "mnemonic": "rd3()", "exe": 10.8, "bits": [
            "1110", "1111"], "words": 1},
        {"opcode": 240, "mnemonic": "clb()", "exe": 10.8, "bits": [
            "1111", "0000"], "words": 1},
        {"opcode": 241, "mnemonic": "clc()", "exe": 10.8, "bits": [
            "1111", "0001"], "words": 1},
        {"opcode": 242, "mnemonic": "iac()", "exe": 10.8, "bits": [
            "1111", "0010"], "words": 1},
        {"opcode": 243, "mnemonic": "cmc()", "exe": 10.8, "bits": [
            "1111", "0011"], "words": 1},
        {"opcode": 244, "mnemonic": "cma()", "exe": 10.8, "bits": [
            "1111", "0100"], "words": 1},
        {"opcode": 245, "mnemonic": "ral()", "exe": 10.8, "bits": [
            "1111", "0101"], "words": 1},
        {"opcode": 246, "mnemonic": "rar()", "exe": 10.8, "bits": [
            "1111", "0110"], "words": 1},
        {"opcode": 247, "mnemonic": "tcc()", "exe": 10.8, "bits": [
            "1111", "0111"], "words": 1},
        {"opcode": 248, "mnemonic": "dac()", "exe": 10.8, "bits": [
            "1111", "1000"], "words": 1},
        {"opcode": 249, "mnemonic": "tcs()", "exe": 10.8, "bits": [
            "1111", "1001"], "words": 1},
        {"opcode": 250, "mnemonic": "stc()", "exe": 10.8, "bits": [
            "1111", "1010"], "words": 1},
        {"opcode": 251, "mnemonic": "daa()", "exe": 10.8, "bits": [
            "1111", "1011"], "words": 1},
        {"opcode": 252, "mnemonic": "kbp()", "exe": 10.8, "bits": [
            "1111", "1100"], "words": 1},
        {"opcode": 253, "mnemonic": "dcl()", "exe": 10.8, "bits": [
            "1111", "1101"], "words": 1},
        {"opcode": 254, "mnemonic": "-", "words": 1},
        {"opcode": 255, "mnemonic": "-", "words": 1},
        {"opcode": 256, "mnemonic": "end", "exe": 0,
         "bits": ["1111", "1111"], "words": 0}
    ]
