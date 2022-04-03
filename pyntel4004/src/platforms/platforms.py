def get_current_platform() -> str:
    """
    Get the current platform

    Parameters
    ----------
    N/A

    Returns
    -------
    str:
        The current platform

    Raises
    ------
    N/A

    Notes
    -----
    platforms could be one of:
        "micropython"
        "cpython"

    """

    import sys
    # Detect current platform
    return sys.implementation.name.lower()


def get_current_datetime() -> str:
    """
    Get the current date/time depending on platform

    Parameters
    ----------
    N/A

    Returns
    -------
    str:
        The current date/time in text format

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """

    # Detect Micropython
    if get_current_platform() == 'micropython':
        import time
        rawtime = time.localtime()
        weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        day = str(rawtime[2])
        if int(day) < 10:
            day = ' ' + day
        hour = str(rawtime[3])
        if int(hour) < 10:
            hour = '0' + hour
        mins = str(rawtime[4])
        if int(mins) < 10:
            mins = '0' + mins
        secs = str(rawtime[5])
        if int(secs) < 10:
            secs = '0' + secs
        errortime = weekday[int(rawtime[6])] + ' ' + \
            month[int(rawtime[1]) - 1] + ' ' +  \
            day + ' ' + \
            hour + ':' + \
            mins + ':' + \
            secs + ' ' + \
            str(rawtime[0])
    else:
        # Other versions of Python
        from time import asctime
        errortime = asctime()

    return errortime
