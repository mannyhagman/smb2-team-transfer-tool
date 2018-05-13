import util
import sys
import sqlite3


def _get_team_file():
    """Collects and allows the user to choose which team file to import"""
    team_files = util.file.common.get_team_files_list([util.file.types.
                                                       FileTypes.TEAM,
                                                       util.file.types.
                                                       FileTypes.TEAMPACK])

    file, page = util.file.common.select_file(team_files, 1)

    return file


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

    if (team_file[-5:] == '.team'):
        file_type = util.file.types.FileTypes.TEAM
    elif (team_file[-9:] == '.teampack'):
        file_type = util.file.types.FileTypes.TEAMPACK

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        data = util.file.common.import_file(team_file, file_type)
        try:
            if (file_type == util.file.types.FileTypes.TEAM):
                team_name = data['team_data'][2]
                try:
                    _write_data_to_db(c, data)
                except sqlite3.IntegrityError:
                    print('There has been a problem with the database.')
                    print('Does a team with that name (' + team_name + ') already exist?')
                    print('Press Enter to exit.')
                    input('')
                    sys.exit(0)
            elif (file_type == util.file.types.FileTypes.TEAMPACK):
                for item in data:
                    team_name = item['team_data'][2]
                    try:
                         _write_data_to_db(c, item)
                    except sqlite3.IntegrityError:
                        print('There has been a problem with the database.')
                        print('Does a team with that name (' + team_name + ') already exist?')
                        print('Skipping team and continuing.')
        except KeyError:
            print('There is a problem with your ' +
                  util.file.types.extensions[file_type] + ' file.')
            print('Try redownloading or recreating your file.')
            print('If the problem persists, let the developer know.')
            print('Press Enter to exit.')
            sys.exit(0)
        conn.commit()
        conn.close()
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt from None

    util.save.save_data(save)
