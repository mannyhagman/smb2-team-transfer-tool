import sys
import os
import exports
import imports
import traceback
import smb2tools as tools


def main():

    print("Ferrea's SMB2 Team Transfer Tool v0.3 beta")

    try:
        save_file = tools.save.load()
    except tools.exceptions.NoSavesError:
        print('No save data found.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
    except tools.exceptions.TooManySavesError:
        print('Multiple save files! Quitting to avoid problems.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

    print('Found save data file.')

    success = False
    while not success:
        print('What do you want to do?')
        print('1. Import a team or team pack')
        print('2. Export a team')
        print('3. Create a team pack')
        print('4. Split a team pack')
        print('5. Import a logo')
        print('6. Export a logo')
        print('b. Quit')
        decision = input('--> ')
        try:
            if (decision.strip() == '1'):
                imports.team(save_file)
                success = True
            elif (decision.strip() == '2'):
                exports.team()
                success = True
            elif (decision.strip() == '3'):
                exports.create_pack()
                success = True
            elif (decision.strip() == '4'):
                exports.split_pack()
                success = True
            elif (decision.strip() == '5'):
                imports.logo(save_file)
                success = True
            elif (decision.strip() == '6'):
                exports.logo()
                success = True
            elif (decision.strip() == 'b'):
                raise KeyboardInterrupt
            else:
                print('That is not a valid option. Please try again.')
        except tools.exceptions.MenuExit:
            pass

    os.remove('database.sqlite')

    print('Done! Press Enter to exit.')
    input('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('')
        print('Quitting!')
        tools.db.common.teardown()
        os.remove('database.sqlite')
        print('Press Enter to close.')
        input('')
    except Exception:
        traceback.print_exc()
        print('This should be reported as a bug.')
        print('Press Enter to exit.')
        tools.db.common.teardown()
        os.remove('database.sqlite')
        input('')
