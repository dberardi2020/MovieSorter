from os import path, scandir

from Classes.Movie import Movie
from definitions import const


class _Directory:
    def __init__(self, name):
        self.name = name
        self.path = path.join(const.base_dir, name)

    def append(self, file_name):
        return path.join(self.path, file_name)

    def get_movies(self):
        movies = []
        for movie in scandir(self.path):
            movies.append(Movie(movie))
        movies.sort(key=lambda x: x.creation_time(), reverse=True)
        return movies

    def get_size(self):
        size = 0
        for movie in self.get_movies():
            size += movie.size
        return size

    def get_movies_cnt(self):
        cnt = 0
        for _ in self.get_movies():
            cnt += 1
        return cnt

    def print(self):
        print(f"{self.name} [{self.get_movies_cnt()} movies | {self.get_size()} GB]")
        for movie in self.get_movies():
            movie.print()

    def contains(self, name):
        for self_movie in self.get_movies():
            if self_movie.name == name:
                return self_movie

        return False


downloads = _Directory("Downloaded")
queued = _Directory("Queued")
ready = _Directory("Ready")
