import os
import sys
import math


def _get_team_files():
    """Collects and allows the user to choose which team files to combine"""
    # Search for team files
    # TODO some of this probably should be moved into its own file
    team_files = []
    for root, dirs, files in os.walk('.'):
        for fileName in files:
            if(fileName[-5:] == '.team'):
                relDir = os.path.relpath(root, '.')
                relFile = os.path.join(relDir, fileName)
                if relFile[:2] == './' or relFile[:2] == '.\\':
                    relFile = relFile[2:]
                team_files.append(relFile)

    team_files = sorted(team_files)
    if(len(team_files) == 0):
        print('No team files were found.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
    # List pages of the team files
    files_combine = []
    cur_page = 1
    while True:
        allowable_options = ['1', '2', '3', '4', '5', '6', '7', '8',
                             '9', '0', 'n', 'p', 'd']
        max_pages = math.ceil(len(team_files)/10)
        items_on_last_page = len(team_files) % 10
        if (items_on_last_page == 0):
            items_on_last_page = 10
        if (cur_page == max_pages):
            print('Page ' + str(cur_page) + ' of team files')
            print('Choose an option.')
            for i in range(0, items_on_last_page):
                print(str(i) + '. ' + team_files[10*(cur_page-1) + i])
            if (cur_page > 1):
                print('p. Previous page')
            print('d. Done')
            choice = input('--> ').strip().lower()
            if (choice in allowable_options):
                if (choice == 'n'):
                    print('You are already on the last page.')
                elif (choice == 'p'):
                    if (cur_page == 1):
                        print('You are already on the first page.')
                    else:
                        cur_page -= 1
                elif (choice == 'd'):
                    return files_combine
                else:
                    item = team_files[10*(cur_page-1) + int(choice)]
                    files_combine.append(item)
                    team_files.remove(item)
            else:
                print('That is not a valid option. Please try again.')
        else:
            print('Page ' + str(cur_page) + ' of team files')
            print('Choose an option.')
            for i in range(0, 10):
                print(str(i) + '. ' + team_files[10*(cur_page-1) + i])
            if (cur_page > 1):
                print('p. Previous page')
            if (cur_page < max_pages):
                print('n. Next page')
            print('d. Done')
            choice = input('--> ').strip()
            if (choice in allowable_options):
                if (choice == 'n'):
                    cur_page += 1
                elif (choice == 'p'):
                    if (cur_page == 1):
                        print('You are already on the first page.')
                    else:
                        cur_page -= 1
                elif (choice == 'd'):
                    return files_combine
                else:
                    item = team_files[10*(cur_page-1) + int(choice)]
                    files_combine.append(item)
                    team_files.remove(item)
            else:
                print('That is not a valid option. Please try again.')

        print('')


def create_team_pack():
    pass
