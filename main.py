#!/usr/bin/env python

from definitions import task_selector

upload_limit = 6


if __name__ == '__main__':
    print("MovieSorter execution started...")

    # if not path.exists(Directories.base_dir):
    #     print("Please insert External HD and run again...")
    #     exit()
    #
    while True:
        print()
        task_selector.selection_prompt()
