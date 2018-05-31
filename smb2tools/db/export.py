def team(c, team_guid):
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

    # t_baseball_player_options AND t_baseball_player_colors
    player_option_data = []
    player_colour_data = []
    for id_ in player_ids:
        c.execute('SELECT * FROM t_baseball_player_options WHERE '
                  'baseballPlayerLocalID = ?', (id_[0],))
        player_options = c.fetchall()
        c.execute('SELECT * FROM t_baseball_player_colors WHERE '
                  'baseballPlayerLocalID = ?', (id_[0],))
        player_colours = c.fetchall()
        player_option_data.append(player_options)
        player_colour_data.append(player_colours)
    data['player_colour_data'] = player_colour_data
    data['player_option_data'] = player_option_data

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

def _fetch_data(c, team_guid):
    """Fetches the data needed from the database"""

    data = {}

    # t_teams
    c.execute('SELECT * FROM t_teams WHERE GUID = ?', (team_guid,))
    team_data = c.fetchone()
    data['team_data'] = team_data

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
