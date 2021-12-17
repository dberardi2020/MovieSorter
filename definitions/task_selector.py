import types

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from definitions import tasks

task_list = types.SimpleNamespace()

task_list.run_dev = "Run Dev Function"
task_list.compress_upload = "Compress and Upload"
task_list.run_compression = "Run Compression"
task_list.upload = "Upload to NAS"
task_list.dir_info = "Get Directory Info"
task_list.drive_info = "Get External HD Info"
task_list.check_name = "Check Missing Title"


def selection_prompt():
    choices = []

    for task in task_list.__dict__:
        choices.append(task_list.__getattribute__(task))

    choices.append(Choice(value=None, name="Exit"))

    action = inquirer.select(
        message="Select an action:",
        choices=choices,
        default=task_list.dir_info
    ).execute()

    match action:
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
