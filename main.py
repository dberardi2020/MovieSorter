#!/usr/bin/env python
import sys
from os import path

import colorama

from definitions import task_selector, const

if __name__ == '__main__':
    colorama.init()
    print(f"MovieSorter execution started... {const.dev_flag}{const.compression_warning}\n")

    if not path.exists(const.external_drive):
        print("Please insert External HD and run again...")
        sys.exit()

    task_selector.selection_prompt()
