from smb2tools import db


def team(data):
    """Writes the data read from file into the DB"""

    c = db.common.cur

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

    # t_baseball_player_colors
    player_colour_data = data['player_colour_data']
    for player in player_colour_data:
        for item in player:
            c.execute('INSERT INTO t_baseball_player_colors VALUES'
                      '(?, ?, ?, ?)',
                      [player_ids_dict[item[0]]] + item[1:])

    # t_baseball_player_options
    player_colour_data = data['player_option_data']
    for player in player_colour_data:
        for item in player:
            c.execute('INSERT INTO t_baseball_player_options VALUES'
                      '(?, ?, ?, ?)',
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


def logo(data, guid):
    """Writes the data read from file into the DB"""

    c = db.common.cur

    c.execute('DELETE FROM t_team_logos WHERE teamGUID = ?', (guid,))

    # t_team_logos
    logo_data = data['logo_data']
    c.executemany('INSERT INTO t_team_logos VALUES '
                  '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', logo_data)

    # t_team_logo_attributes
    logo_attrs = data['logo_attrs']
    for guid in logo_attrs:
        c.executemany('INSERT INTO t_team_logo_attributes VALUES '
                      '(?, ?, ?, ?, ?, ?, ?)', guid)
