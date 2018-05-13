import util
import sys


def _get_team_files():
    """Collects and allows the user to choose which team files to combine"""
    team_files = util.file.common.get_team_files_list([util.file.types.
                                                       FileTypes.TEAM])

    files_combine = []

    done = False

    page = 1
    while not done:
        file, page = util.file.common.select_file(team_files, page,
                                                  mchoice=True)
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


def create_team_pack():
    teams = _get_team_files()
    team_data_list = []
    guids = set()
    print('Choose teams to include in the team pack.')
    for team in teams:
        data = util.file.common.import_file(team,
                                            util.file.types.FileTypes.TEAM)
        guid = data['team_data'][0]
        if (guid in guids):
            print('File ' + team + ' appears to already be included.')
        else:
            team_data_list.append(data)
    print(str(len(team_data_list)) + ' teams have been included in the pack.')
    print('Choose a name for the file.')
    name = input('--> ').strip()
    team_data_list.append({'name': name})
    util.file.common.export_file(team_data_list,
                                 util.file.types.FileTypes.TEAMPACK)


def split_team_pack():
    files = util.file.common.get_team_files_list([util.file.types.
                                                  FileTypes.TEAMPACK])

    file_choice, page = util.file.common.select_file(files, 1)

    data = util.file.common.import_file(file_choice,
                                        util.file.types.FileTypes.TEAMPACK)

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
        file, page = util.file.common.select_file(names, page, True, True)

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
            util.file.common.export_file(item, util.file.types.FileTypes.TEAM)
