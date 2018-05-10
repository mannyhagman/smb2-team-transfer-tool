"""A module to organise writing and reading files used by the tool"""
from . import types


def export_file(data, type):
    """Exports the file to a shareable format

    Arguments:
    data - the dictionary to be exported
    type - the type of file to write
    """

    # The exports dict holds a callable, which we then call
    types.exports[type](data)
