import qcc.config


def qprint(*args, **kwargs):
    """ The lower the priority, the likelier a print is to take place.
        The default priority is 2, and the verbosity is typically 2; if
        priority is set to 1, then something _will_ print.
    """
    if 'priority' in kwargs:
        priority = kwargs.pop('priority')
    else:
        priority = qcc.config.max_verbosity

    if priority <= qcc.config.current_verbosity:
        print(*args, **kwargs)

