import os
import sys
import zlib

def load_data():
    save_files = []

    for root, dirs, files in os.walk(os.path.expanduser('~\AppData\local\Metalhead\Super Mega Baseball 2')):
        for name in files:
            if (name == 'savedata.sav'):
                save_files.append((root, name))

    #This is for easier Linux testing for me
    save_files = [('.', 'savedata.sav')]

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

    try:
        with open(in_fname, 'rb') as in_data:
            in_file = in_data.read()
        print('Found save data file.')
    except FileNotFoundError:
        print('No save data found.')
        print('Press Enter to exit.')
        input('')

    decomp_in_file = zlib.decompress(in_file)
    f = open('database.sqlite', 'wb')
    f.write(decomp_in_file)
    f.close()

    return save_files
