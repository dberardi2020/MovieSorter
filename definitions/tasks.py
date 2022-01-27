import shutil
import subprocess
import sys
import time
from os import path

from InquirerPy import inquirer
from InquirerPy.base import Choice

from Classes import Directories, ANSI, Statistics
from Classes.Logger import Logger
from Classes.Movie import Movie
from definitions import const, helpers

upload_limit = 6


def check_name():
    check = Directories.downloads.contains("title.mkv")
    if check and not check.is_locked():
        Directories.downloads.print()
        name = inquirer.text(message="Please rename title.mkv in Downloaded: ",
                             raise_keyboard_interrupt=False).execute()
        if name:
            check.rename(name)


def change_name():
    check_name()

    # Give selection prompt
    selected: Movie = inquirer.select(
        message="Which movie would you like to rename?",
        choices=[Choice(movie, name=movie.name) for movie in helpers.get_all_movie()] +
                [Choice(value=None, name="Exit")],
        show_cursor=False,
        raise_keyboard_interrupt=False
    ).execute()

    if not selected:
        return

    name = inquirer.text(message=f"Please provide the new name for {selected.name}: ",
                         raise_keyboard_interrupt=False, default=selected.remove_extension()).execute()

    if not name:
        return

    confirmed = inquirer.confirm(
        message=f"Are you sure you want to rename {selected.name} to {name}{selected.get_extension()}?",
        raise_keyboard_interrupt=False).execute()

    if confirmed:
        selected.rename(name)


def get_external_info():
    total, used, free = shutil.disk_usage(const.external_drive)

    print("Total: %d GB" % (total // (2 ** 30)))
    print("Free: %d GB" % (free // (2 ** 30)))
    print("Used: %d GB" % (used // (2 ** 30)))


def get_dir_info():
    get_external_info()
    print()
    Directories.downloads.print()
    Directories.queued.print()
    Directories.ready.print()


def sort():
    sort_downloaded()
    clean_compression_queue()


def sort_downloaded():
    check_name()
    print("Sorting movies in Downloaded...")

    for movie in Directories.downloads.get_movies():
        if movie.is_locked():
            continue

        if movie.size < const.upload_limit:
            movie.move_to_upload()
        else:
            movie.move_to_compression()
    print()


def clean_compression_queue():
    print("Cleaning movies in Ready for Compression...")

    for movie in Directories.queued.get_movies():
        if movie.is_compressed():
            movie.delete()
    print()


def run_compression():
    logger = Logger()
    eta = Statistics.compression.estimate(Directories.queued.get_size())

    logger.log_and_print(f"Compressing movies in Ready for Compression... [ETA: {eta}]")
    queued = Directories.queued.get_movies()
    total_tasks = len(queued)
    current_task = 0
    master_start_time = time.time()
    log_cache = []
    for movie in queued:
        target = 0
        current_task += 1
        output_path = Directories.ready.append(movie.name).replace(".mkv", ".mp4")
        handbrake_command = [r"HandBrakeCLI.exe", "-i", f"{movie.path}", "-o",
                             f"{output_path}", "-e", "x264", "-q", "20", "-B", "160"]
        start_time = time.time()
        process = subprocess.Popen(handbrake_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True)

        for line in process.stdout:
            if helpers.process_compression_output(movie.name, current_task, total_tasks, line, target, logger):
                target += 10

        compressed_movie_size = helpers.convert_to_gb(path.getsize(output_path))
        run_time = helpers.run_time(start_time)
        Statistics.compression.add_stat(movie.size, run_time)
        output_log = f"Compressed {movie.name} from {movie.size} GB to {compressed_movie_size} " \
                     f"GB in {helpers.format_time(run_time)}"
        log_cache.append(output_log)

    print()
    logger.log_and_print(
        f"Completed {total_tasks} compression(s) in {helpers.format_time(helpers.run_time(master_start_time))}... "
        f"[ETA: {eta}]")
    for log in log_cache:
        logger.log_and_print(log)
    print()


def upload_to_nas():
    num_uploads = Directories.ready.get_movies_cnt()
    uploads_left = Directories.ready.get_movies_cnt()
    size_total = Directories.ready.get_size()

    eta = Statistics.upload.estimate(size_total)
    print(f"Uploading movies in Ready for Upload... [ETA: {eta}]\n")

    start_time = time.time()

    for idx, movie in enumerate(Directories.ready.get_movies()):
        print(
            f"{ANSI.up_char(idx + 1)}{uploads_left} movie(s) left to upload - [{size_total} GB]{ANSI.clr_char()}{ANSI.down_char(idx)}")
        uploads_left = uploads_left - 1

        if movie.is_locked():
            continue

        movie.upload_to_nas()
        Statistics.upload.add_stat(movie.size, helpers.run_time(start_time))
        size_total = size_total - movie.size

    print(
        f"{ANSI.up_char(num_uploads + 1)}{uploads_left} movie(s) left to upload - [{size_total} GB]{ANSI.clr_char()}{ANSI.down_char(num_uploads)}")
    print(f"\nUploaded {num_uploads} movies in {helpers.format_time(helpers.run_time(start_time))}\n")


def dev_func():
    Statistics.compression.print_stat()
    print()
    Statistics.upload.print_stat()
    sys.exit()


def mark_failure():
    check_name()
    if Directories.downloads.get_movies_cnt() > 0:
        last_rip = Directories.downloads.get_movies()[0]
        last_rip_name = last_rip.remove_extension()
        confirmed = inquirer.confirm(message=f"Are you sure you want to mark {last_rip_name} as a failure?",
                                     raise_keyboard_interrupt=False).execute()
        if confirmed:
            if helpers.write_failure(last_rip_name):
                last_rip.delete()
        else:
            custom = inquirer.text(message="What is the name of the failure?: ",
                                   raise_keyboard_interrupt=False).execute()
            if custom:
                helpers.write_failure(custom)
    else:
        custom = inquirer.text(message="What is the name of the failure?: ", raise_keyboard_interrupt=False).execute()
        if custom:
            helpers.write_failure(custom)


def mark_series():
    series = inquirer.text(message="What is the name of the series?: ", raise_keyboard_interrupt=False).execute()
    if series:
        helpers.write_series(series)
