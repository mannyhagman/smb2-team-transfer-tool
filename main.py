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

    print("Ferrea's SMB2 Team Transfer Tool v0.3 beta")

    save_file = util.save.load_data()

    success = False
    while not success:
        print('Do you wish to import or export data?')
        print('1. Import')
        print('2. Export')
        print('3. Create team pack')
        decision = input('--> ')
        if (decision.strip() == '1'):
            success = True
            imports.team.import_team(save_file)
            util.save.save_data(save_file)
        elif (decision.strip() == '2'):
            success = True
            exports.team.export_team()
        elif (decision.strip() == '3'):
            success = True
            exports.pack.create_team_pack()
        else:
            print('You did not choose a valid option. Please try again.')

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
