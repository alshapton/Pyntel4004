
###########################################################################
#                                                                         #
#            .-.                                                          #
#           (._.)        ,--.      .-.      .-.        ,--.               #
#            .-.        /   |    /    \   /    \      /   |               #
#            | |       / .' |   |  .-. ; |  .-. ;    / .' |               #
#            | |     / /  | |   | |  | | | |  | |   / / | |               #
#            | |    / /   | |   | |  | | | |  | |  / /  | |               #
#            | |   /  `--'  |-. | |  | | | |  | | /  `--' |-.             #
#            | |    `-----| |-' | '  | | | '  | | `-----| |-'             #
#            | |          | |   '  `-' / '  `-' /       | |               #
#           (___)        (___)   `.__,'   `.__,'       (___)              #
#                                                                         #
#     _           _                   _   _                        _      #
#    (_)_ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __    ___  ___| |_    #
#    | | '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \  / __|/ _ \ __|   #
#    | | | | \__ \ |_| |  | |_| | (__| |_| | (_) | | | | \__ \  __/ |_    #
#    |_|_| |_|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_| |___/\___|\__|   #
#                                                                         #
###########################################################################

from hardware.instructions.accumulator import clb, clc, cma, cmc, iac, \
     daa, dac, kbp, ral, rar, stc, tcc, tcs  # noqa
from hardware.instructions.idx import inc, fin  # noqa
from hardware.instructions.idxacc import add, ld, sub, xch  # noqa
from hardware.instructions.immediate import fim, ldm  # noqa
from hardware.instructions.memory_select import dcl, src  # noqa
from hardware.instructions.nop import nop  # noqa
from hardware.instructions.subroutine import bbl, jms  # noqa
from hardware.instructions.io_ram import rdm, rd0, rd1, rd2, rd3 \
     rdr, wrm, wr0, wr1, wr2, wr3, wmp, wrr, adm, sbm, wpm  # noqa

#
# Abbreviations used in the descriptions of each instruction's actions:
#
#        (    )	    the content of
#        -->	    is transferred to
#        ACC	    Accumulator (4-bit)
#        CY	        Carry/link Flip-Flop
#        ACBR	    Accumulator Buffer Register (4-bit)
#        RRRR	    Index register address
#        RPn	    Index register pair address
#        PL	        Low order program counter Field (4-bit)
#        PM	        Middle order program counter Field (4-bit)
#        PH	        High order program counter Field (4-bit)
#        ai	        Order i content of the accumulator
#        CMi	    Order i content of the command register
#        M	        RAM main character location
#        MSi	    RAM status character i
#        DB (T)	    Data bus content at time T
#        Stack	    The 3 registers in the address register
#                   other than the program counter
#
# Additional Abbreviations:
#        ~           Inverse (1's complement)
#        .           logical OR
#
