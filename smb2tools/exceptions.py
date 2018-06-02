class Error(Exception):
    pass


class MenuExit(Exception):
    pass


class NoSavesError(Exception):
    pass


class TooManySavesError(Exception):
    pass


class NoExtensionsError(Exception):
    pass


class NoFilesFound(Exception):
    pass


class IncompatibleError(Exception):
    pass
