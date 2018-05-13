"""A module for importing and exporting team logo files"""
import util
import json
import sys


def export_logo(data):
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


def import_logo(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    if util.file.common.is_file_compatible(data,
                                           util.file.types.FileTypes.TEAM):
        return data
    else:
        print('This data is incompatible with the current version of '
              'the tool.')
        print('You may have to convert it to the new format or recreate it.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
