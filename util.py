import math
import smb2tools as tools
import smb2tools.db.common as common


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
                raise tools.exceptions.MenuExit
            elif (choice == 'a'):
                return (True, cur_page)
            else:
                return (files[10*(cur_page-1) + int(choice)], cur_page)
        else:
            print('That is not a valid option. Please try again.')


def _get_team_guid():
    """User chooses a team, GUID is returned for use in the DB"""

    c = common.cur

    while True:
        team_name = input('--> ')
        c.execute('SELECT * FROM t_teams WHERE teamType = 1 AND '
                  ' teamName = ? COLLATE NOCASE',
                  (team_name,))
        team_choices = c.fetchall()
        if len(team_choices) == 0:
            print('No teams exist with the name ' +
                  team_name +
                  '. Please try again.')
        else:
            break
    for item in team_choices[:]:
        if item[1] is not None:
            team_choices.remove(item)

    if len(team_choices) > 1:
        while True:
            print('There are multiple teams with that name, '
                  'please choose one.')
            print('Note the highest-numbered teams '
                  'are the most recently created.')
            count = 0
            for item in team_choices:
                count += 1
                print(str(count) + '. ' + item[2])
            try:
                choice = int(input('--> '))
            except ValueError:
                print('That was not a valid number. Please try again.')
            if (choice < 1 or choice > count):
                print('That was not a valid choice. Please try again.')
            else:
                return team_choices[choice-1][0]
    else:
        print('Found a team! Using found team.')
        return team_choices[0][0]
