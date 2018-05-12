"""A module for importing and exporting team data files"""
import util
import json


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

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=util.json.BytesEncoder))
    f.close()
