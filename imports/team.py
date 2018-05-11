import util
import sys
import sqlite3
import math
import os


def _get_team_file():
    """Collects and allows the user to choose which team file to import"""
    # Search for team files
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
    cur_page = 1
    while True:
        allowable_options = ['1', '2', '3', '4', '5', '6', '7', '8',
                             '9', '0', 'n', 'p']
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
            choice = input('--> ').strip().lower()
            if (choice in allowable_options):
                if (choice == 'n'):
                    print('You are already on the last page.')
                elif (choice == 'p'):
                    if (cur_page == 1):
                        print('You are already on the first page.')
                    else:
                        cur_page -= 1
                else:
                    return team_files[10*(cur_page-1) + int(choice)]
                    break
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
            choice = input('--> ').strip()
            if (choice in allowable_options):
                if (choice == 'n'):
                    cur_page += 1
                elif (choice == 'p'):
                    if (cur_page == 1):
                        print('You are already on the first page.')
                    else:
                        cur_page -= 1
                else:
                    return team_files[10*(cur_page-1) + int(choice)]
                    break
            else:
                print('That is not a valid option. Please try again.')

        print('')


def _write_data_to_db(c, data):
    """Writes the data read from file into the DB"""

    # t_teams
    team_data = data['team_data']
    c.execute('INSERT INTO t_teams VALUES (?, ?, ?, ?, ?, ?, ?, ?)', team_data)

    # t_baseball_players
    player_data = data['player_data']
    c.executemany('INSERT INTO t_baseball_players VALUES '
                  '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', player_data)

    # t_baseball_player_local_ids
    space = False
    number = 3000
    while not space:
        c.execute('SELECT MAX(localID) FROM t_baseball_player_local_ids '
                  'WHERE localID < ?', (number,))
        max_val = c.fetchone()[0]
        if max_val < 2500:
            next_val = 2500
            space = True
        elif (max_val < (number-22)):
            next_val = max_val + 1
            space = True
        else:
            number += 10
    player_ids_dict = {}
    player_ids = data['player_ids']
    player_ids_new = []
    for id in player_ids:
        # Do mapping from old ID to new ID
        player_ids_dict[id[0]] = next_val
        player_ids_new.append((next_val, id[1]))
        next_val += 1

    c.executemany('INSERT INTO t_baseball_player_local_ids VALUES (?, ?)',
                  player_ids_new)

    # t_baseball_player_attributes
    player_attr_data = data['player_attr_data']
    for player in player_attr_data:
        for item in player:
            c.execute('INSERT INTO t_baseball_player_attributes VALUES'
                      '(?, ?, ?, ?, ?, ?, ?)',
                      [player_ids_dict[item[0]]] + item[1:])

    # t_lineups
    lineup_data = data['lineup_data']
    c.execute('INSERT INTO t_lineups VALUES (?, ?, ?)', lineup_data)

    # t_batting_orders
    order_data = data['order_data']
    c.executemany('INSERT INTO t_batting_orders VALUES (?, ?, ?)', order_data)

    # t_pitching_rotations
    rotation_data = data['rotation_data']
    c.executemany('INSERT INTO t_pitching_rotations VALUES (?, ?, ?)',
                  rotation_data)

    # t_defensive_positions
    dpos_data = data['dpos_data']
    c.executemany('INSERT INTO t_defensive_positions VALUES (?, ?, ?)',
                  dpos_data)

    # t_team_local_ids
    c.execute('SELECT MAX(localID) FROM t_team_local_ids')
    next_team_val = int(c.fetchone()[0]) + 1

    team_id_data = data['team_id_data']

    c.execute('INSERT INTO t_team_local_ids VALUES (?, ?)',
              (next_team_val, team_id_data[1]))

    # t_team_attributes
    team_attr_data = data['team_attr_data']
    for team_attr in team_attr_data:
        c.execute('INSERT INTO t_team_attributes VALUES (?, ?, ?, ?, ?, ?, ?)',
                  [next_team_val] + team_attr[1:])

    # t_team_logos
    logo_data = data['logo_data']
    c.executemany('INSERT INTO t_team_logos VALUES '
                  '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', logo_data)

    # t_team_logo_attributes
    logo_attrs = data['logo_attrs']
    for guid in logo_attrs:
        c.executemany('INSERT INTO t_team_logo_attributes VALUES '
                      '(?, ?, ?, ?, ?, ?, ?)', guid)


def import_team(save):

    # Back up original save data
    util.save.backup_data(save)

    team_file = _get_team_file()

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        data = util.file.common.import_file(team_file,
                                            util.file.types.FileTypes.TEAM)
        _write_data_to_db(c, data)
        conn.commit()
        conn.close()
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt from None
    except sqlite3.IntegrityError:
        print('There has been a problem with the database.')
        print('Are you trying to add a team that already exists?')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
