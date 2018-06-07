

class StatechartLoaderError(Exception):
    pass


class StatechartAlreadyInitialized(StatechartLoaderError):
    pass


class StatechartNotExist(StatechartLoaderError):
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path


class InvalidStatechartXML(StatechartLoaderError):
    pass
