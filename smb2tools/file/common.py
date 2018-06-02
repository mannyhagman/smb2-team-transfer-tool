"""A module to organise writing and reading files used by the tool"""
import os
from smb2tools import file, exceptions


def is_compatible(data, type):
    """Determines if a file is compatible with the tool.

    Returns a boolean.

    Arguments:
    data - the data to check the version of
    type - the type of file that data is
    """

    try:
        version = data['version']
    except KeyError:
        version = 1
    if version == file.cur_ver or version in file.compat[type]:
        return True
    else:
        return False


def get_version(data):
    """Gets the version of the file structure.

    Returns the version tag of the data, else returns 1.

    Arguments:
    data - the data to get the version of
    """
    try:
        return data['version']
    except KeyError:
        return 1


def get_file_name(fname, type):
    """Gets an unused file name to save the file to.

    It'll try name.ext, but if it's already in use,
    it'll try name_0.ext, then name_1.ext, and so on,
    until it finds an unused one.

    Arguments:
    fname - the name to try and save to
    type - the type of file to save, determines extension
    """

    if (os.path.isfile(fname + file.extensions[type])):
        number = 0
        exists = True
        while exists:
            if (os.path.isfile(fname + '_' + str(number) +
                               file.extensions[type])):
                number += 1
            else:
                fname = fname + '_' + str(number) + file.extensions[type]
                exists = False
    else:
        fname = fname + file.extensions[type]

    return fname


def get_file_list(types):
    """Collects and allows the user to choose which team files to combine

    Arguments:
    types - a list of enums to use to find extensions
    """

    if(types):
        exts = [file.extensions[t] for t in types]
    else:
        raise exceptions.NoExtensionsError

    exts = tuple(exts)

    files = []
    for root, dirs, files_ in os.walk('.'):
        for filename in files_:
            if(filename.endswith(exts)):
                reldir = os.path.relpath(root, '.')
                relfile = os.path.join(reldir, filename)
                if relfile[:2] == './' or relfile[:2] == '.\\':
                    relfile = relfile[2:]
                files.append(relfile)

    files = sorted(files)
    if(len(files) == 0):
        raise exceptions.NoFilesFound

    return files


def save(data, type):
    """Exports the file to a shareable format

    Returns the name of the file that was saved to

    Arguments:
    data - the dictionary to be exported
    type - the type of file to write
    """

    # The exports dict holds a callable, which we then call
    return file.exports[type](data)


def load(file_name, type):
    """Imports data from a JSON file

    Returns the data loaded from file.

    Arguments:
    file_name - the name of the file to import
    type - the type of file to read
    """

    return file.imports[type](file_name)
