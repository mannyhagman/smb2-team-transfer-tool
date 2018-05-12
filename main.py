import os
import sys
import util
import exports
import imports


def main():

    print("Ferrea's SMB2 Team Transfer Tool v0.3 beta")

    save_file = util.save.load_data()

    success = False
    while not success:
        print('What do you want to do?')
        print('1. Import a team or team pack')
        print('2. Export a team')
        print('3. Create a team pack')
        print('4. Split a team pack')
        print('b. Quit')
        decision = input('--> ')
        try:
            if (decision.strip() == '1'):
                imports.team.import_team(save_file)
                success = True
            elif (decision.strip() == '2'):
                exports.team.export_team()
                success = True
            elif (decision.strip() == '3'):
                exports.pack.create_team_pack()
                success = True
            elif (decision.strip() == '4'):
                exports.pack.split_team_pack()
                success = True
            elif (decision.strip() == 'b'):
                raise KeyboardInterrupt
            else:
                print('You did not choose a valid option. Please try again.')
        except util.QuitException:
            pass

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
