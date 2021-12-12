from os import scandir

from Classes import Directories
from Classes.Movie import Movie


class _Movies:
    def __init__(self, directory):
        self.directory = directory
        self.movies = []

        for movie in scandir(directory.path):
            self.movies.append(Movie(movie))

    def print(self):
        print(f"{self.directory.name} [{self.num_movies()} movies | {self.num_gb()} GB]")
        for movie in self.movies:
            movie.print()

    def num_gb(self):
        total_gb = 0

        for movie in self.movies:
            total_gb += movie.size

        return total_gb

    def num_movies(self):
        return len(self.movies)


downloaded = _Movies(directory=Directories.downloads)
queued = _Movies(directory=Directories.queued)
ready = _Movies(directory=Directories.ready)
