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
        print('Type the name of the team whose logo you wish to export.')
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


def export_logo():
    """The main function that controls exporting logos"""

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        team_guid = _get_team_guid(c)
        data = _fetch_data(c, team_guid)
        conn.close()
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt from None

    util.file.common.export_file(data, util.file.types.FileTypes.LOGO)

    return True
