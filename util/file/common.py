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


def import_file(file_name, type):
    """Imports data from a JSON file

    Arguments:
    file_name - the name of the file to import
    type - the type of file to read
    """

    return types.imports[type](file_name)
