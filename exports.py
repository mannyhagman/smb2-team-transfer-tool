import sys
import sqlite3
import smb2tools as tools
import util


def team():
    """The main function that controls exporting teams"""

    print('Type the name of the team you wish to export.')
    team_guid = util._get_team_guid(c)
    data = tools.db.exports.team(team_guid)

    tools.file.common.save(data, tools.file.FileTypes.TEAM)


def _get_team_files():
    """Collects and allows the user to choose which team files to combine"""
    try:
        team_files = tools.file.common.get_file_list([tools.file.
                                                      FileTypes.TEAM])
    except tools.exceptions.NoFilesFound:
        print('No valid files were found.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

    files_combine = []

    done = False

    page = 1
    while not done:
        file, page = util.select_file(team_files, page, mchoice=True)
        if file is None:
            done = True
        else:
            files_combine.append(file)
            team_files.remove(file)
        if(len(team_files) == 0):
            print('There are no more team files to choose!')
            done = True

    if(len(files_combine) == 0):
        print('You did not choose any teams to pack!')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

    return files_combine


def create_pack():
    teams = _get_team_files()
    team_data_list = []
    names = set()
    print('Choose teams to include in the team pack.')
    for team in teams:
        try:
            data = tools.file.common.load(team,
                                                 tools.file.FileTypes.TEAM)
        except tools.exceptions.IncompatibleError as e:
            print('One of the files is not compatible with the current tool.')
            print('It contains the team ' + e.team + '.')
            print('Press Enter to exit.')
            input('')
            sys.exit(0)
        data['version'] = 2
        name = data['team_data'][2]
        if (name in names):
            print('A team with name ' + team +
                  ' appears to already be included. Skipping.')
        else:
            team_data_list.append(data)
            names.add(name)
    print(str(len(team_data_list)) + ' teams have been included in the pack.')
    print('Choose a name for the file.')
    name = input('--> ').strip()
    team_data_list.append({'name': name})
    tools.file.common.save(team_data_list,
                                  tools.file.FileTypes.TEAMPACK)


def split_pack():
    files = tools.file.common.get_file_list([tools.file.
                                             FileTypes.TEAMPACK])

    file_choice, page = util.select_file(files, 1)

    data = tools.file.common.load(file_choice,
                                         tools.file.FileTypes.TEAMPACK)

    names = []
    # Get all of the team names out of the file
    if data:
        for item in data:
            names.append(item['team_data'][2])
    else:
        print('There is no data in this .teampack file.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)

    done = False
    page = 1
    files_export = []
    while not done:
        file, page = util.select_file(names, page, True, True)

        if file is None:
            done = True
        elif file is True:
            files_export.extend(data)
            done = True
        else:
            ind = names.index(file)
            del names[ind]
            files_export.append(data[ind])
            del data[ind]

        if(len(names) == 0):
            print('There are no more team files to choose!')
            done = True

    if len(files_export) == 0:
        print('You did not choose any files.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
    else:
        for item in files_export:
            tools.file.common.save(item,
                                          tools.file.FileTypes.TEAM)


def logo():
    """The main function that controls exporting logos"""

    print('Type the name of the team whose logo you wish to export.')
    team_guid = util._get_team_guid(c)
    data = tools.db.exports.logo(team_guid)

    fname = tools.file.common.save(data,
                                   tools.file.FileTypes.LOGO)

    print('Saving file as ' + fname)
