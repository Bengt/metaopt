"""
Utilities for algorithm implementations.

"""


def default_mutation_stength(param):
    """
    Returns the default mutation strength for a parameter.

    Based on http://www.iue.tuwien.ac.at/phd/heitzinger/node27.html.
    """
    return (param.upper_bound - param.lower_bound) / 10