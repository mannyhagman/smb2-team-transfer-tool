"""A module for importing and exporting team data files"""
import json
from smb2tools import exceptions, file
from smb2tools import json as json_tools


def _process_data_ver1(data):
    """Convert version 1 team data to current version."""
    data['player_option_data'] = []
    data['player_colour_data'] = []

    for player in data['player_attr_data']:
        data['player_option_data'].append([])
        data['player_colour_data'].append([])

        for item in player:
            if (item[1] is None):
                data['player_colour_data'][-1].append([x for x in item
                                                       if x is not None])
            else:
                data['player_option_data'][-1].append([x for x in item
                                                       if x is not None])

    del data['player_attr_data']

    return data


def save(data):
    """Exports the team data to file

    Returns the name of the file that was created.

    Arguments:
    data - the dictionary to export
    """
    team_name = data['team_data'][2]

    fname = file.common.get_file_name(team_name,
                                      file.FileTypes.TEAM)

    data['version'] = file.cur_ver

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=json_tools.BytesEncoder))
    f.close()

    return fname


def load(fname):
    """Imports the team data from file

    Returns the data imported from file.

    Arguments:
    fname - the file to load data from
    """
    with open(fname) as team_file:
        data = json.loads(team_file.read(), cls=json_tools.BytesDecoder)

    if file.common.is_compatible(data,
                                      file.FileTypes.TEAM):
        if(file.common.get_version(data) == 1):
            return _process_data_ver1(data)

        return data
    else:
        raise exceptions.IncompatibleError
