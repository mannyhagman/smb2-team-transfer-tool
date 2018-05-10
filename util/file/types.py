"""A module that holds information about file types"""
from enum import Enum
from . import team


class FileTypes(Enum):
    TEAM = 0


exports = {FileTypes.TEAM: team.export_team}

imports = {FileTypes.TEAM: team.import_team}
