import sqlite3
import zlib
import os
import json
import uuid
import sys
import math
import shutil
import util
import exports
import imports

def main():

    print("Ferrea's SMB2 Team Transfer Tool 0.1 beta")

    save_file = util.save.load_data()

    success = False
    while not success:
        print('Do you wish to import or export data?')
        print('1. Import')
        print('2. Export')
        decision = input('--> ')
        if (decision.strip() == '1'):
            success = True
            try:
                imports.team.import_team(save_file)
                util.save.save_data(save_file)
            except sqlite3.IntegrityError:
                print('There has been a problem with the database.')
                print('Are you trying to add a team that already exists?')
                print('Press Enter to exit.')
                input('')
                sys.exit(0)
        elif (decision.strip() == '2'):
            success = True
            exports.team.export_team()
        else:
            print('You did not type 1 or 2. Please try again.')

    os.remove('database.sqlite')

    print('Done! Press enter to exit.')
    input('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('')
        print('Quitting!')
        os.remove('database.sqlite')
        print('Press Enter to close.')
        input('')
        sys.exit(0)
