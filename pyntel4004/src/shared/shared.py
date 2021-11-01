def get_opcodeinfo(self, ls: str, mnemonic: str):
    """
    Given a mnemonic, retrieve information about the mnemonic from
    the opcode table

    Parameters
    ----------
    chip : processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    ls: str, mandatory
        's' or 'S' indicating whether the mnemonic contains the full mnemonic
        or not - e.g.    nop   as a mnemonic would be found if ls = 'S' or 's'
                         nop() as a mnemonic would be found if ls != 'S' or 's'

    mnemonic: str, mandatory
        The mnemonic to locate

    Returns
    -------
    opcodeinfo
        The information about the mnemonic required in JSON form,
        or

           {"opcode": -1, "mnemonic": "N/A"}

        if the mnemonic is not found.

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    if ls.upper() == 'S':
        try:
            opcodeinfo = next((item for item in self.INSTRUCTIONS
                               if str(item["mnemonic"][:3]) == mnemonic),
                              {"opcode": -1, "mnemonic": "N/A"})
        except:  # noqa
            opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
        return opcodeinfo
    try:
        opcodeinfo = next((item for item in self.INSTRUCTIONS
                           if str(item["mnemonic"]) == mnemonic),
                          {"opcode": -1, "mnemonic": "N/A"})
    except:  # noqa
        opcodeinfo = {"opcode": -1, "mnemonic": "N/A"}
    return opcodeinfo
