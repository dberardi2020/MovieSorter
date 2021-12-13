#!/usr/bin/env python
import sys
from os import path

from definitions import task_selector, const

upload_limit = 6

if __name__ == '__main__':
    print("MovieSorter execution started...")

    if not path.exists(const.base_dir):
        print("Please insert External HD and run again...")
        sys.exit()

    while True:
        print()
        task_selector.selection_prompt()
