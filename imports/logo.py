import sys
import sqlite3
import util


def _get_logo_file():
    """Collects and allows the user to choose which team logo to import"""
    team_files = util.file.common.get_team_files_list([util.file.types.
                                                       FileTypes.LOGO])

    file, page = util.file.common.select_file(team_files, 1)

    return file


def _clear_existing_data(c, guid):
    c.execute('DELETE FROM t_team_logos WHERE teamGUID = ?', (guid,))


def _write_data_to_db(c, data):
    """Writes the data read from file into the DB"""

    # t_team_logos
    logo_data = data['logo_data']
    c.executemany('INSERT INTO t_team_logos VALUES '
                  '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', logo_data)

    # t_team_logo_attributes
    logo_attrs = data['logo_attrs']
    for guid in logo_attrs:
        c.executemany('INSERT INTO t_team_logo_attributes VALUES '
                      '(?, ?, ?, ?, ?, ?, ?)', guid)


def import_logo(save):

    # Back up original save data
    util.save.backup_data(save)

    logo_file = _get_logo_file()

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        print('Type the name of the team you wish to import the logo to.')
        team_guid = util.db._get_team_guid(c)
        _clear_existing_data(c, team_guid)
        data = util.file.common.import_file(logo_file,
                                            util.file.types.FileTypes.LOGO)

        for item in data['logo_data']:
            print(item[0])
            item[1] = team_guid

        try:
            _write_data_to_db(c, data)
        except KeyError:
            print('There is a problem with your logo file.')
            print('Try redownloading or recreating your file.')
            print('If the problem persists, let the developer know.')
            print('Press Enter to exit.')
            sys.exit(0)
        except sqlite3.IntegrityError:
            print('There has been a problem with the database.')
            print('This is a bug! Please report it.')
            print('Press Enter to exit.')
            input('')
            sys.exit(0)
        conn.commit()
        conn.close()
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt from None

    util.save.save_data(save)
