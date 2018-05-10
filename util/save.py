import os
import zlib

def _get_save_location():
    """Get the OS-dependent save location"""
    save_name = 'savedata.sav'
    if os.name == 'nt':
        save_files = []

        for root, dirs, files in os.walk(os.path.expanduser('~\AppData\local\Metalhead\Super Mega Baseball 2')):
            for name in files:
                if (name == save_name):
                    save_files.append((root, name))

        return save_files

    elif os.name == 'posix':
        files = os.listdir()
        if 'savedata.sav' in files:
            return [('.', 'savedata.sav')]

def _extract_save_file(save_files):
    """Error checks and decompresses the save file."""

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

    save_files = _get_save_location()

    _extract_save_file(save_files)

    return save_files

def save_data(save_file):

    with open('database.sqlite', 'rb') as new_data:
        new_save = new_data.read()
    zlib_save = zlib.compress(new_save)
    f = open(os.path.join(save_file[0], 'savedata_new.sav'), 'wb')
    f.write(zlib_save)
    f.close()
    os.replace(os.path.join(save_file[0], 'savedata_new.sav'), os.path.join(save_file[0], save_file[1]))
