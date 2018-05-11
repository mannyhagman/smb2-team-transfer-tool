"""A module for importing and exporting team data files"""
import util
import os
import json


def export_team_pack(data):
    """Exports the team pack data to file

    Arguments:
    data - the list of team pack data to export, with a dictionary
           containing a name at the end
    """
    pack_name = data[-1]['name']
    del data[-1]

    if (os.path.isfile(pack_name + '.teampack')):
        number = 0
        exists = True
        while exists:
            if (os.path.isfile(pack_name + '_' + str(number) + '.teampack')):
                pass
                number += 1
            else:
                fname = pack_name + '_' + str(number) + '.teampack'
                exists = False
    else:
        fname = pack_name + '.teampack'

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()


def import_team_pack(file):
    with open(file) as team_pack_file:
        data = json.loads(team_pack_file.read(), cls=util.json.BytesDecoder)

    return data
