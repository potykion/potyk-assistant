def split_strip(str_, sep=","):
    """
    >>> split_strip("a, b")
    ['a', 'b']
    """
    return [item.strip() for item in str_.split(sep)]
