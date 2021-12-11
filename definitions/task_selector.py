from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import types

import definitions.tasks

task_list = types.SimpleNamespace()

task_list.sort_all = "Sort All"
task_list.sort_downloads = "Sort Downloads"
task_list.sort_compression = "Sort Compression"
task_list.drive_info = "Get External HD info"
task_list.dir_info = "Get Directory Info"
task_list.run_compression = "Run Compression"
task_list.upload = "Upload to NAS"


def selection_prompt():
    choices = []

    for task in task_list.__dict__:
        choices.append(task_list.__getattribute__(task))

    choices.append(Choice(value=None, name="Exit"))

    action = inquirer.select(
        message="Select an action:",
        choices=choices,
        default=task_list.sort_all
    ).execute()

    match action:
        case task_list.sort_all:
            tasks.sort()

        case task_list.sort_downloads:
            tasks.sort_downloaded()

        case task_list.sort_compression:
            tasks.clean_compression_queue()

        case task_list.drive_info:
            tasks.get_external_info()

        case task_list.dir_info:
            tasks.get_dir_info()

        case task_list.run_compression:
            tasks.sort_downloaded()
            tasks.clean_compression_queue()
            tasks.run_compression()
            tasks.clean_compression_queue()

        case task_list.upload:
            tasks.sort()
            tasks.upload_to_nas()

        case _:
            exit()



