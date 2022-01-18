import shutil
from os import path, remove, rename
from pathlib import Path

from Classes import Directories
from definitions import helpers, const


class Movie:
    def __init__(self, movie):
        self.name = movie.name
        self.path = movie.path
        self.dir = Path(self.path).parent
        self.size = helpers.convert_to_gb(path.getsize(self.path))

    def print(self):
        print(f"  -  {self.name}: {self.size.__str__()} GB")

    def rename(self, name):
        rename(self.path, path.join(self.dir, name + self.get_extension()))

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
        movie_check = Directories.ready.contains(self.name.replace("mkv", "mp4"))
        if movie_check and not movie_check.is_locked():
            return True

        return False

    def creation_time(self):
        return path.getctime(self.path)

    def remove_extension(self):
        return path.splitext(self.name)[0]

    def get_extension(self):
        return path.splitext(self.name)[1]

    def move_to_compression(self):
        self._move(Directories.queued.path)

    def move_to_upload(self):
        self._move(Directories.ready.path)

    def upload_to_nas(self):
        self._move(const.nas_dir)

    def delete(self):
        if path.exists(self.path) and not self.is_locked():
            remove(self.path)
            print("Deleted", self.path)

    def _move(self, dest_dir):
        source = self.path
        dest = path.join(dest_dir, self.name)

        if not self.is_locked():
            print(f"Moving {self.name} [{self.size} GB] from {self.dir} to {dest_dir}", end="\r")
            shutil.move(source, dest)
            print(f"Finished Moving {self.name} [{self.size} GB] from {self.dir} to {dest_dir}")
