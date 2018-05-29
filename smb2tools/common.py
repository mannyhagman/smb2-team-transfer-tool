"""A module to organise writing and reading files used by the tool"""
from . import types
import os
import sys
import math
import util


def is_file_compatible(data, type):
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
    if version == types.cur_ver or version in types.compat[type]:
        return True
    else:
        return False


def get_data_version(data):
    try:
        return data['version']
    except KeyError:
        return 1


def get_file_name(file, type):
    """Gets an unused file name to save the file to.

    It'll try name.ext, but if it's already in use,
    it'll try name_0.ext, then name_1.ext, and so on,
    until it finds an unused one.

    Arguments:
    file - the name to try and save to
    type - the type of file to save, determines extension
    """

    if (os.path.isfile(file + types.extensions[type])):
        print(file + types.extensions[type] + ' already exists...')
        number = 0
        exists = True
        while exists:
            if (os.path.isfile(file + '_' + str(number) +
                               types.extensions[type])):
                number += 1
            else:
                fname = file + '_' + str(number) + types.extensions[type]
                exists = False
    else:
        fname = file + types.extensions[type]

    print('Saving file as ' + fname)
    return fname


def get_team_files_list(types):
    """Collects and allows the user to choose which team files to combine

    Arguments:
    types - a list of enums to use to find extensions
    """

    if(types):
        exts = [util.file.types.extensions[t] for t in types]
    else:
        print('No extensions were requested!')
        print('This is a bug! Please report it.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

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
        print('No valid files were found.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

    return files


def select_file(files, page=1, mchoice=False, all=False):
    """Allow the user to select a team from a list

    files - the list of files to be chosen from
    page - which page should be shown initially
    mchoice - Enables the d - done option.
              Meant for if the user is able to select
              multiple choices and decide when they're done.
    all - Whether the user should be presented with a select all option.
    """

    print('')

    cur_page = page

    allowable_options = {'1', '2', '3', '4', '5', '6', '7', '8',
                         '9', '0', 'b'}
    max_pages = math.ceil(len(files)/10)
    if (cur_page > max_pages):
        cur_page = max_pages
    select = False

    if (mchoice):
        allowable_options.add('d')
    if (all):
        allowable_options.add('a')

    while not select:
        print('')
        print('Page ' + str(cur_page) + ' of files')
        print('Choose an option.')
        max_range = 10
        if(cur_page == max_pages):
            max_range = len(files) % 10
            if (max_range == 0):
                max_range = 10
        for i in range(0, max_range):
            print(str(i) + '. ' + files[10*(cur_page-1) + i])
        if (cur_page > 1):
            allowable_options.add('p')
            print('p. Previous page')
        else:
            allowable_options.discard('p')
        if (cur_page < max_pages):
            allowable_options.add('n')
            print('n. Next page')
        else:
            allowable_options.discard('n')
        if (all):
            print('a. Export all')
        if (mchoice):
            print('d. Done')
        print('b. Go back')
        choice = input('--> ').strip()
        if (choice in allowable_options):
            if (choice == 'n'):
                cur_page += 1
            elif (choice == 'p'):
                cur_page -= 1
            elif (choice == 'd'):
                return (None, cur_page)
            elif (choice == 'b'):
                raise util.GoBackException
            elif (choice == 'a'):
                return (True, cur_page)
            else:
                return (files[10*(cur_page-1) + int(choice)], cur_page)
        else:
            print('That is not a valid option. Please try again.')


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
