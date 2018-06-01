def _get_team_file():
    """Collects and allows the user to choose which team file to import"""
    team_files = util.file.common.get_team_files_list([util.file.types.
                                                       FileTypes.TEAM,
                                                       util.file.types.
                                                       FileTypes.TEAMPACK])

    file, page = util.file.common.select_file(team_files, 1)

    return file


def import_team(save):

    # Back up original save data
    util.save.backup_data(save)
    print('Backup of savedata made to savedata_backup.sav')

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
                    print('Does a team with that name (' + team_name +
                          ') already exist?')
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
                        print('Does a team with that name (' + team_name +
                              ') already exist?')
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

def _get_logo_file():
    """Collects and allows the user to choose which team logo to import"""
    team_files = util.file.common.get_team_files_list([util.file.types.
                                                       FileTypes.LOGO])

    file, page = util.file.common.select_file(team_files, 1)

    return file

def import_logo(save):

    # Back up original save data
    util.save.backup_data(save)
    print('Backup of savedata made to savedata_backup.sav')

    logo_file = _get_logo_file()

    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        print('Type the name of the team you wish to import the logo to.')
        team_guid = util.db._get_team_guid(c)
        _clear_existing_data(c, team_guid)
        try:
            data = util.file.common.import_file(logo_file,
                                                util.file.types.FileTypes.LOGO)
        except IncompatibleException:
        print('This data is incompatible with the current version of '
              'the tool.')
        print('You may have to convert it to the new format or recreate it.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

        for item in data['logo_data']:
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
