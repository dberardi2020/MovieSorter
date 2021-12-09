from os import path, remove
import errno
import shutil
from pathlib import Path
from Directories import Directories


Directories = Directories()


def convert_to_gb(size_in_bytes):
    return round(size_in_bytes * (10 ** -9))


class Movie:
    def __init__(self, movie):
        self.name = movie.name
        self.path = movie.path
        self.size = convert_to_gb(path.getsize(self.path))

    def print(self):
        print(self.name + ":", self.size.__str__(), "GB")

    def is_locked(self):
        path_obj = Path(self.path)

        if not path_obj.exists():
            raise FileNotFoundError

        try:
            path_obj.rename(path_obj)
        except PermissionError:
            print(self.path, "is currently locked...")
            return True
        else:
            return False

    def is_compressed(self):
        return path.exists(path.join(Directories.upload_dir, self.name))

    def move_to_compression(self):
        self._move(Directories.compression_dir)

    def move_to_upload(self):
        self._move(Directories.upload_dir)

    def upload_to_nas(self):
        self._move(Directories.nas_dir)

    def delete(self):
        if path.exists(self.path):
            print("Deleting", self.path)
            remove(self.path)
            print("Deleted", self.path)

    def _move(self, dest_dir):
        source_dir = self.path
        dest_dir = path.join(dest_dir, self.name)

        if not self.is_locked():
            print("Moving", self.name, "from", source_dir, "to", dest_dir)
            shutil.move(source_dir, dest_dir)
            print("Finished Moving", self.name, "from", source_dir, "to", dest_dir)
