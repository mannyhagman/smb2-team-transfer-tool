"""Utility module to work with save data."""

import os
import zlib
import sys
import shutil


def _get_save_location():
    """Get the OS-dependent save location"""
    save_name = 'savedata.sav'
    save_dir = '~\AppData\local\Metalhead\Super Mega Baseball 2'
    if os.name == 'nt':
        save_files = []

        for root, dirs, files in os.walk(os.path.expanduser(save_dir)):
            for name in files:
                if (name == save_name):
                    save_files.append((root, name))

        return save_files

    elif os.name == 'posix':
        files = os.listdir()
        if 'savedata.sav' in files:
            return [('.', 'savedata.sav')]


def _extract_save_file(save_files):
    """Does basic error checking and decompresses the save file."""

    if len(save_files) > 1:
        print('Multiple save files! Quitting to avoid problems.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
    elif (len(save_files) == 0):
        print('No save data found.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

    in_fname = os.path.join(save_files[0][0], save_files[0][1])

    with open(in_fname, 'rb') as in_data:
        in_file = in_data.read()
    print('Found save data file.')

    decomp_in_file = zlib.decompress(in_file)
    f = open('database.sqlite', 'wb')
    f.write(decomp_in_file)
    f.close()


def load_data():
    """Loads the save data and returns the save location.

    Returns a tuple with directory and save name.
    """

    save_files = _get_save_location()

    _extract_save_file(save_files)

    return save_files[0]


def save_data(save_file):
    """Saves the modified database

    Creates a copy then moves it when written

    Arguments:
    save_file - A tuple with directory and save name
    """

    with open('database.sqlite', 'rb') as new_data:
        new_save = new_data.read()
    zlib_save = zlib.compress(new_save)
    f = open(os.path.join(save_file[0], 'savedata_new.sav'), 'wb')
    f.write(zlib_save)
    f.close()
    os.replace(os.path.join(save_file[0], 'savedata_new.sav'),
               os.path.join(save_file[0], save_file[1]))


def backup_data(save_file):
    """Backs up the original save data

    Copies savedata.sav to savedata_backup.sav

    Arguments:
    save_file - A tuple with directory and save name
    """
    shutil.copy2(os.path.join(save_file[0], save_file[1]),
                 os.path.join(save_file[0], 'savedata_backup.sav'))
    print('Backup of savedata made to savedata_backup.sav')