from os import scandir

from Classes.Movie import Movie


class Movies:
    def __init__(self, directory):
        self.directory = directory
        self.num_gb = 0
        self.movies = []

        for movie in scandir(directory):
            movie = Movie(movie)
            self.movies.append(Movie(movie))
            self.num_gb += movie.size

    def print(self):
        print(f"{self.directory} [{self.length()} movies | {self.num_gb} GB]")
        for movie in self.movies:
            movie.print()

    def length(self):
        return len(self.movies)
