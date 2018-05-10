"""Exports a team to a .team file"""
import util
import sqlite3


def _fetch_data(c, team_guid):
    """Fetches the data needed from the database"""

    data = {}

    # t_teams
    c.execute('SELECT * FROM t_teams WHERE GUID = ?', (team_guid,))
    team_data = c.fetchone()
    data['team_data'] = team_data

    # t_baseball_players
    c.execute('SELECT * FROM t_baseball_players WHERE teamGUID = ?',
              (team_guid,))
    player_guids = []
    player_data = c.fetchall()
    for item in player_data:
        player_guids.append(item[0])

    data['player_data'] = player_data

    # t_baseball_player_local_ids
    player_ids = []
    for guid in player_guids:
        c.execute('SELECT * FROM t_baseball_player_local_ids WHERE GUID = ?',
                  (guid,))
        new_id = c.fetchone()
        player_ids.append((new_id[0], guid))
    data['player_ids'] = player_ids

    # t_baseball_player_attributes
    player_attr_data_all = []
    for id_ in player_ids:
        c.execute('SELECT * FROM t_baseball_player_attributes WHERE '
                  'baseballPlayerLocalID = ?', (id_[0],))
        player_attr_data = c.fetchall()
        player_attr_data_all.append(player_attr_data)
    data['player_attr_data'] = player_attr_data_all

    # t_lineups
    c.execute('SELECT * FROM t_lineups WHERE teamGUID = ?', (team_guid,))
    lineup_data = c.fetchone()
    lineup_guid = lineup_data[0]
    data['lineup_data'] = lineup_data

    # t_batting_orders
    c.execute('SELECT * FROM t_batting_orders WHERE lineupGUID = ?',
              (lineup_guid,))
    order_data = c.fetchall()
    data['order_data'] = order_data

    # t_pitching_rotations
    c.execute('SELECT * FROM t_pitching_rotations WHERE lineupGUID = ?',
              (lineup_guid,))
    rotation_data = c.fetchall()
    data['rotation_data'] = rotation_data

    # t_defensive_positions
    c.execute('SELECT * FROM t_defensive_positions WHERE lineupGUID = ?',
              (lineup_guid,))
    dpos_data = c.fetchall()
    data['dpos_data'] = dpos_data

    # t_team_local_ids
    c.execute('SELECT * FROM t_team_local_ids WHERE GUID = ?', (team_guid,))
    team_id_data = c.fetchone()
    data['team_id_data'] = team_id_data

    # t_team_attributes
    c.execute('SELECT * FROM t_team_attributes WHERE teamLocalID = ?',
              (team_id_data[0],))
    team_attr_data = c.fetchall()
    data['team_attr_data'] = team_attr_data

    # t_team_logos
    c.execute('SELECT * FROM t_team_logos WHERE teamGUID = ?', (team_guid,))
    logo_data = c.fetchall()
    logo_guids = []
    for item in logo_data:
        logo_guids.append(item[0])
    data['logo_data'] = logo_data

    # t_team_logo_attributes
    logo_attrs_all = []
    for guid in logo_guids:
        c.execute('SELECT * FROM t_team_logo_attributes WHERE '
                  'teamLogoGUID = ?', (guid,))
        logo_attrs = c.fetchall()
        logo_attrs_all.append(logo_attrs)
    data['logo_attrs'] = logo_attrs_all

    return data


def _get_team_guid(c):
    """User chooses a team, GUID is returned for use in the DB"""
    while True:
        print('Type the name of the team you wish to export.')
        team_name = input('--> ')
        c.execute('SELECT * FROM t_teams WHERE teamName = ? COLLATE NOCASE',
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


def export_team():
    """The main function that controls exporting teams"""

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        team_guid = _get_team_guid(c)
        data = _fetch_data(c, team_guid)
        conn.close()
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt from None

    util.file.common.export_file(data, util.file.types.FileTypes.TEAM)
