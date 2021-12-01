#!/usr/bin/env python

from os import path
from Movies import Movies
from Directories import Directories


upload_limit = 6

Directories = Directories()


def sort_downloaded():
    print("Sorting movies in Downloaded...")
    downloaded = Movies(Directories.download_dir)

    for movie in downloaded.get_movies():
        if movie.is_locked():
            continue

        if movie.size < upload_limit:
            movie.move_to_upload()
        else:
            movie.move_to_compression()


def sort_compression_queue():
    print("Sorting movies in Ready for Compression...")
    queued = Movies(Directories.compression_dir)
    done = Movies(Directories.upload_dir)

    for movie in queued.get_movies():
        for done_movie in done.get_movies():
            if movie.name == done_movie.name:
                if not done_movie.is_locked():
                    movie.delete()


if __name__ == '__main__':
    print("MovieSorter execution started...")
    sort_downloaded()
    sort_compression_queue()
