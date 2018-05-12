"""A module for importing and exporting team data files"""
import util
import json


def export_team(data):
    """Exports the team data to file

    Arguments:
    data - the dictionary to export
    """
    team_name = data['team_data'][2]

    fname = util.file.common.get_file_name(team_name,
                                           util.file.types.FileTypes.TEAM)

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()


def import_team(file):
    with open(file) as team_file:
        data = json.loads(team_file.read(), cls=util.json.BytesDecoder)

    return data
