import types

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from definitions import tasks

task_list = types.SimpleNamespace()

task_list.run_dev = "Run Dev Function"
task_list.upload = "Upload to NAS"
task_list.run_compression = "Run Compression"
task_list.compress_upload = "Compress and Upload"
task_list.dir_info = "Get Directory Info"
task_list.rename = "Rename Title"
task_list.mark_failure = "Mark Failure"
task_list.mark_series = "Mark Series"


def selection_prompt():
    choices = [task_list.__getattribute__(item) for item in task_list.__dict__]
    choices.append(Choice(value=None, name="Exit"))

    action = inquirer.select(
        message="Select an action:",
        choices=choices,
        default=task_list.dir_info,
        show_cursor=False,
        raise_keyboard_interrupt=False
    ).execute()

    if action == task_list.rename:
        tasks.change_name()
    elif action == task_list.dir_info:
        tasks.get_dir_info()
    elif action == task_list.compress_upload:
        tasks.sort()
        tasks.upload_to_nas()
        tasks.run_compression()
        tasks.clean_compression_queue()
        tasks.upload_to_nas()
    elif action == task_list.run_compression:
        tasks.sort()
        tasks.run_compression()
        tasks.clean_compression_queue()
    elif action == task_list.upload:
        tasks.sort()
        tasks.upload_to_nas()
    elif action == task_list.mark_failure:
        tasks.mark_failure()
    elif action == task_list.mark_series:
        tasks.mark_series()
    elif action == task_list.run_dev:
        tasks.dev_func()
    else:
        exit()
