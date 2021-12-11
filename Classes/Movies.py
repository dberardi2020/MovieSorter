from os import scandir

from Classes.Movie import Movie


class Movies:
    def __init__(self, directory):
        self.directory = directory
        self.size = 0
        self.movies = []

        for movie in scandir(directory):
            movie = Movie(movie)
            self.movies.append(Movie(movie))
            self.size += movie.size

    def print(self):
        print(f"{self.directory} [{self.length()} movies | {self.size} GB]")
        for movie in self.movies:
            movie.print()

    def get_movies(self):
        return self.movies

    def length(self):
        return len(self.movies)
