"""A module for importing and exporting team data files"""
import util
import os
import json


def export_team(data):
    """Exports the team data to file

    Arguments:
    data - the dictionary to export
    """
    team_name = data['team_data'][2]

    if (os.path.isfile(team_name + '.team')):
        number = 0
        exists = True
        while exists:
            if (os.path.isfile(team_name + '_' + str(number) + '.team')):
                pass
                number += 1
            else:
                fname = team_name + '_' + str(number) + '.team'
                exists = False
    else:
        fname = team_name + '.team'

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()


def import_team(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    return data
