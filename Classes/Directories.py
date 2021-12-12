from os import path

from definitions import const


class _Directory:
    def __init__(self, name):
        self.name = name
        self.path = path.join(const.base_dir, name)

    def append(self, file_name):
        return path.join(self.path, file_name)


downloads = _Directory("Downloaded")
queued = _Directory("Queued")
ready = _Directory("Ready")
