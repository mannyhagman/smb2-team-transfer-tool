"""A module for importing and exporting team data files"""
import util
import json
import sys


def _process_data_ver1(data):
    data['player_option_data'] = []
    data['player_colour_data'] = []

    for player in data['player_attr_data']:
        data['player_option_data'].append([])
        data['player_colour_data'].append([])

        for item in player:
            if (item[1] is None):
                print('Colours')
                print(item)
                data['player_colour_data'][-1].append([x for x in item
                                                       if x is not None])
            else:
                print('Options')
                print(item)
                data['player_option_data'][-1].append([x for x in item
                                                       if x is not None])

    del data['player_attr_data']

    return data


def export_team(data):
    """Exports the team data to file

    Arguments:
    data - the dictionary to export
    """
    team_name = data['team_data'][2]

    fname = util.file.common.get_file_name(team_name,
                                           util.file.types.FileTypes.TEAM)

    data['version'] = util.file.types.cur_ver

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()


def import_team(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    if util.file.common.is_file_compatible(data,
                                           util.file.types.FileTypes.TEAM):
        if(data['version'] == 1):
            return _process_data_ver1(data)

        return data
    else:
        print('This data is incompatible with the current version of '
              'the tool.')
        print('You may have to convert it to the new format or recreate it.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
