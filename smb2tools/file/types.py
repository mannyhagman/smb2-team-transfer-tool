"""A module that holds information about file types"""
from enum import Enum
from smb2tools.file import team, pack, logo


class FileTypes(Enum):
    TEAM = 0
    TEAMPACK = 1
    LOGO = 2
    CSV = 3


exports = {FileTypes.TEAM: team.save,
           FileTypes.TEAMPACK: pack.save,
           FileTypes.LOGO: logo.save}

imports = {FileTypes.TEAM: team.load,
           FileTypes.TEAMPACK: pack.load,
           FileTypes.LOGO: logo.load}

extensions = {FileTypes.TEAM: '.team',
              FileTypes.TEAMPACK: '.teampack',
              FileTypes.LOGO: '.logo',
              FileTypes.CSV: '.csv'}

cur_ver = 2

compat = {FileTypes.TEAM: [1],
          FileTypes.TEAMPACK: [1],
          FileTypes.LOGO: [1]}
