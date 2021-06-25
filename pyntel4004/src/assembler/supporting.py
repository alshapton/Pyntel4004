def add_label(_L, label: str):
    """
    Add a label to the label table (if it does not exist already).

    Parameters
    ----------
    _L : list, mandatory
        A list of the existing labels
    label: str, mandatory
        A candidate new label

    Returns
    -------
    -1          if the label already existed and was not added
    _L : list
                the list of labels with the new label appended

    Raises
    ------
    N/A

    Notes
    ------
    N/A

    """
    try:
        label_exists = next((item for item in _L
                            if str(item["label"]) == label), None)
    except:  # noqa
        pass
    if not label_exists:
        _L.append({'label': label, 'address': -1})
    else:
        return -1
    return _L
