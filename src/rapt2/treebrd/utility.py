from typing import Any


def flatten(lst: list[Any]) -> list[Any]:
    """
    Recursively flatten a nested list into a single-level list.

    :param lst: a potentially nested list.
    :return: a flat list containing all leaf elements.
    """
    result: list[Any] = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
