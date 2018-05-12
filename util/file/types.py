"""A module that holds information about file types"""
from enum import Enum
from . import team
from . import teampack


class FileTypes(Enum):
    TEAM = 0
    TEAMPACK = 1


exports = {FileTypes.TEAM: team.export_team,
           FileTypes.TEAMPACK: teampack.export_team_pack}

imports = {FileTypes.TEAM: team.import_team}

extensions = {FileTypes.TEAM: '.team',
              FileTypes.TEAMPACK: '.teampack'}
