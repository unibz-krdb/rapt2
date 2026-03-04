def flatten(lst):
    """
    Recursively flatten a nested list into a single-level list.

    :param lst: a potentially nested list.
    :return: a flat list containing all leaf elements.
    """
    return sum(([l] if not isinstance(l, list) else flatten(l) for l in lst), [])
