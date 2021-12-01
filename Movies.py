from os import scandir

from Movie import Movie


class Movies:
    def __init__(self, directory):
        self.movies = []

        for movie in scandir(directory):
            self.movies.append(Movie(movie))

    def print(self):
        for movie in self.movies:
            movie.print()

    def get_movies(self):
        return self.movies
