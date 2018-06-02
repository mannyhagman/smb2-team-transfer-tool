"""A module for importing and exporting team data files"""
import util
import json
import sys


def save(data):
    """Exports the team pack data to file

    Arguments:
    data - the list of team pack data to export, with a dictionary
           containing a name at the end
    """
    pack_name = data[-1]['name']
    del data[-1]

    fname = util.file.common.get_file_name(pack_name,
                                           util.file.types.FileTypes.TEAMPACK)

    for item in data:
        if not util.file.common.is_file_compatible(item,
                                                   util.file.types.
                                                   FileTypes.TEAM):
            raise IncompatibleException

    data = {'version': util.file.types.cur_ver, 'data': data}

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()

    return fname


def load(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    if util.file.common.is_file_compatible(data,
                                           util.file.types.FileTypes.TEAMPACK):

        data_new = []

        for item in data['data']:
            if (util.file.common.get_data_version(item) == 1):
                data_new.append(util.file.team._process_data_ver1(item))
            else:
                data_new.append(item)

        return data_new

    else:
        raise IncompatibleException
