"""A module for importing and exporting team data files"""
import json
from smb2tools import file, exceptions
from smb2tools import json as json_tools


def save(data):
    """Exports the team pack data to file

    Arguments:
    data - the list of team pack data to export, with a dictionary
           containing a name at the end
    """
    pack_name = data[-1]['name']
    del data[-1]

    fname = file.common.get_file_name(pack_name,
                                      file.FileTypes.TEAMPACK)

    for item in data:
        if not file.common.is_file_compatible(item,
                                              file.FileTypes.TEAM):
            raise exceptions.IncompatibleError

    data = {'version': file.cur_ver, 'data': data}

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=json_tools.BytesEncoder))
    f.close()

    return fname


def load(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=json_tools.BytesDecoder)

    if file.common.is_file_compatible(data,
                                      file.FileTypes.TEAMPACK):

        data_new = []

        for item in data['data']:
            if (file.common.get_data_version(item) == 1):
                data_new.append(file.team._process_data_ver1(item))
            else:
                data_new.append(item)

        return data_new

    else:
        raise exceptions.IncompatibleError
