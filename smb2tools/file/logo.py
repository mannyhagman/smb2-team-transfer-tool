"""A module for importing and exporting team logo files"""
import util
import json
import sys
import uuid


def save(data):
    """Exports the team logo to file

    Arguments:
    data - the dictionary to export
    """
    team_name = data['team_data'][2]

    del data['team_data']

    fname = util.file.common.get_file_name(team_name,
                                           util.file.types.FileTypes.LOGO)

    data['version'] = util.file.types.cur_ver

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()


def load(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    if util.file.common.is_file_compatible(data,
                                           util.file.types.FileTypes.TEAM):
        new_data = {'logo_data': [], 'logo_attrs': []}

        guid_map = {}

        for item in data['logo_data']:
            guid_map[item[0]] = uuid.uuid4().bytes
            new_data['logo_data'].append([guid_map[item[0]]] + item[1:])

        for data_piece in data['logo_attrs']:
            for item in data_piece:
                new_data['logo_attrs'].append([[guid_map[item[0]]] + item[1:]])

        new_data['version'] = 2

        return data
    else:
        raise exceptions.IncompatibleError
