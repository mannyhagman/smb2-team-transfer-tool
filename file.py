import math
from smb2tools import exceptions


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
                raise exceptions.MenuExit
            elif (choice == 'a'):
                return (True, cur_page)
            else:
                return (files[10*(cur_page-1) + int(choice)], cur_page)
        else:
            print('That is not a valid option. Please try again.')
