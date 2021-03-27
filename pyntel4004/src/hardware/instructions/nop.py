

#####################################################
#  _ _  _    ___   ___  _  _                        #
# (_) || |  / _ \ / _ \| || |                       #
#  _| || |_| | | | | | | || |_   _ __   ___  _ __   # 
# | |__   _| | | | | | |__   _| | '_ \ / _ \| '_ \  #
# | |  | | | |_| | |_| |  | |   | | | | (_) | |_) | #
# |_|  |_|  \___/ \___/   |_|   |_| |_|\___/| .__/  #
#                                           | |     #
#                                           |_|     #
#                                                   #
#####################################################

def nop(self):
    """
    Name:           No Operation
    Function:       No operation performed.
    Syntax:         NOP
    Assembled:      0000 0000
    Symbolic:       Not applicable
    Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
    Side-effects:   Not Applicable
    """

    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + 1
    return self.PROGRAM_COUNTER
