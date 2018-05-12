import os
import sys
import util
import exports
import imports


def _export(save_file):
    success = False
    while not success:
        print('What do you wish to export?')
        print('1. Team')
        print('2. Create team pack')
        print('b. Go back')
        decision = input('--> ')
        if (decision.strip() == '1'):
            success = exports.team.export_team()
            return True
        elif (decision.strip() == '2'):
            try:
                success = exports.pack.create_team_pack()
                return True
            except util.QuitException:
                pass
        elif (decision.strip() == 'b'):
            return False
        else:
            print('You did not choose a valid option. Please try again.')


def _import(save_file):
    success = False
    while not success:
        print('What do you wish to import?')
        print('1. Team or team pack')
        print('b. Go back')
        decision = input('--> ')
        if (decision.strip() == '1'):
            try:
                imports.team.import_team(save_file)
                return True
            except util.QuitException:
                pass
        elif (decision.strip() == 'b'):
            return False
        else:
            print('You did not choose a valid option. Please try again.')


def main():

    print("Ferrea's SMB2 Team Transfer Tool v0.3 beta")

    save_file = util.save.load_data()

    success = False
    while not success:
        print('Do you wish to import or export data?')
        print('1. Import')
        print('2. Export')
        print('b. Quit')
        decision = input('--> ')
        if (decision.strip() == '1'):
            success = _import(save_file)
        elif (decision.strip() == '2'):
            success = _export(save_file)
        elif (decision.strip() == 'b'):
            raise KeyboardInterrupt
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
