#!/usr/bin/env python

from os import path
import shutil

from Classes.Movies import Movies
from Classes.Directories import Directories
import definitions.task_selector
import definitions.tasks

upload_limit = 6

Directories = Directories()


if __name__ == '__main__':
    print("MovieSorter execution started...")

    if not path.exists(Directories.base_dir):
        print("Please insert External HD and run again...")
        exit()

    while True:
        tasks.check_name()
        print()
        task_selector.selection_prompt()
