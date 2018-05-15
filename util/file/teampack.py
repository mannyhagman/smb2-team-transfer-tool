"""A module for importing and exporting team data files"""
import util
import json
import sys


def export_team_pack(data):
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
            print('One of the files is not compatible with the current tool.')
            print('It contains the team ' + item['team_data'][2] + '.')
            print('Press Enter to exit.')
            input('')
            sys.exit(0)

    data = {'version': util.file.types.cur_ver, 'data': data}

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()


def import_team_pack(file):
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
        print('This data is incompatible with the current version of '
              'the tool.')
        print('You may have to convert it to the new format or recreate it.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
