import util
import sys


def _get_team_files():
    """Collects and allows the user to choose which team files to combine"""
    team_files = util.file.common.get_team_files_list(True, False)

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

    return True
