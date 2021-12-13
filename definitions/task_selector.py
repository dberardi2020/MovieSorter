import types

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from definitions import tasks

task_list = types.SimpleNamespace()

task_list.run_dev = "Run Dev Function"
task_list.sort_all = "Sort All"
task_list.sort_downloads = "Sort Downloads"
task_list.sort_compression = "Sort Compression"
task_list.check_name = "Check Missing Title"
task_list.drive_info = "Get External HD Info"
task_list.dir_info = "Get Directory Info"
task_list.compress_upload = "Compress and Upload"
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

        case task_list.check_name:
            tasks.check_name()

        case task_list.drive_info:
            tasks.get_external_info()

        case task_list.dir_info:
            tasks.get_dir_info()

        case task_list.compress_upload:
            tasks.sort()
            tasks.run_compression()
            tasks.upload_to_nas()

        case task_list.run_compression:
            tasks.sort()
            tasks.run_compression()
            tasks.clean_compression_queue()

        case task_list.upload:
            tasks.sort()
            tasks.upload_to_nas()

        case task_list.run_dev:
            tasks.dev_func()

        case _:
            exit()
