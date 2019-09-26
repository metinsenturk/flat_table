from ._norm import mapper
from ._norm import normalize
from ._version import version


__doc__ = """
A tool to flat dataframes in rowwise and columnwise.
====================================================

It is an extension to pd.io.json.json_normalize() function, where
it expands json_normalize functions abilities in a few ways.

    - Dicts expand into columns, as in json_normalize().
    - Columns expand even if there are nulls.
    - Lists expand into rows.
"""
