"""A module for importing and exporting team data files"""
import json
from .. import exceptions


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

    fname = util.file.common.get_file_name(team_name,
                                           util.file.types.FileTypes.TEAM)

    data['version'] = util.file.types.cur_ver

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()

    return fname


def load(file):
    """Imports the team data from file

    Returns the data imported from file.

    Arguments:
    file - the file to load data from
    """
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    if util.file.common.is_file_compatible(data,
                                           util.file.types.FileTypes.TEAM):
        if(util.file.common.get_data_version(data) == 1):
            return _process_data_ver1(data)

        return data
    else:
        raise exceptions.IncompatibleError
