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


def export_logo():
    """The main function that controls exporting logos"""

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        print('Type the name of the team whose logo you wish to export.')
        team_guid = util.db._get_team_guid(c)
        data = _fetch_data(c, team_guid)
        conn.close()
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt from None

    util.file.common.export_file(data, util.file.types.FileTypes.LOGO)

    print('Saving file as ' + fname)
