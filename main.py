#!/usr/bin/env python
import sys
from os import path

from definitions import task_selector, const

if __name__ == '__main__':
    dev_flag = ""
    if const.dev:
        dev_flag = "[Dev Mode]"

    print(f"MovieSorter execution started... {dev_flag} \n")

    if not path.exists(const.external_drive):
        print("Please insert External HD and run again...")
        sys.exit()

    task_selector.selection_prompt()
