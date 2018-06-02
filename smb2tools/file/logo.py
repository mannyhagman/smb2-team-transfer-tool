"""A module for importing and exporting team logo files"""
import json
import uuid
from smb2tools import exceptions, file
from smb2tools import json as json_tools


def save(data):
    """Exports the team logo to file

    Arguments:
    data - the dictionary to export
    """
    team_name = data['team_data'][2]

    del data['team_data']

    fname = file.common.get_file_name(team_name,
                                      file.FileTypes.LOGO)

    data['version'] = file.cur_ver

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=json_tools.BytesEncoder))
    f.close()

    return fname


def load(fname):
    with open(fname) as team_file:
        data = json.loads(team_file.read(), cls=json_tools.BytesDecoder)

    if file.common.is_compatible(data,
                                      file.FileTypes.TEAM):
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
