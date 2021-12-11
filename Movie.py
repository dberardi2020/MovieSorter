from os import path, remove
from pathlib import Path
from Directories import Directories
import errno
import shutil
import helpers


Directories = Directories()


class Movie:
    def __init__(self, movie):
        self.name = movie.name
        self.name_raw = Path(movie.name).with_suffix('')
        self.path = movie.path
        self.size = helpers.convert_to_gb(path.getsize(self.path))

    def print(self):
        print(f"  -  {self.name}: {self.size.__str__()} GB")

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
            remove(self.path)
            print("Deleted", self.path)

    def _move(self, dest_dir):
        source_dir = self.path
        dest_dir = path.join(dest_dir, self.name)

        if not self.is_locked():
            # print("Moving", self.name, "from", source_dir, "to", dest_dir)
            print(f"Moving {self.name} ({self.size}) from {source_dir} to {dest_dir}")
            shutil.move(source_dir, dest_dir)
            print(f"Finished Moving {self.name} ({self.size}) from {source_dir} to {dest_dir}")
