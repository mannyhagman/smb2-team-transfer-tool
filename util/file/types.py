"""A module that holds information about file types"""
from enum import Enum
from . import team
from . import teampack
from . import logo


class FileTypes(Enum):
    TEAM = 0
    TEAMPACK = 1
    LOGO = 2
    CSV = 3


exports = {FileTypes.TEAM: team.export_team,
           FileTypes.TEAMPACK: teampack.export_team_pack,
           FileTypes.LOGO: logo.export_logo}

imports = {FileTypes.TEAM: team.import_team,
           FileTypes.TEAMPACK: teampack.import_team_pack,
           FileTypes.LOGO: logo.import_logo}

extensions = {FileTypes.TEAM: '.team',
              FileTypes.TEAMPACK: '.teampack',
              FileTypes.LOGO: '.logo',
              FileTypes.CSV: '.csv'}

cur_ver = 2

compat = {FileTypes.TEAM: [1],
          FileTypes.TEAMPACK: [1],
          FileTypes.LOGO: [1]}
