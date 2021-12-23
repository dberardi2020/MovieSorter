import shutil
import subprocess
import sys
import time
from os import path

from InquirerPy import inquirer

from Classes import Directories
from Classes.Logger import Logger
from definitions import const, helpers, statistics

upload_limit = 6


def check_name():
    check = Directories.downloads.contains("title.mkv")
    if check and not check.is_locked():
        Directories.downloads.print()
        name = inquirer.text(message="Please rename title.mkv in Downloaded: ").execute()
        check.rename(name)


def get_external_info():
    total, used, free = shutil.disk_usage(const.external_drive)

    print("Total: %d GB" % (total // (2 ** 30)))
    print("Free: %d GB" % (free // (2 ** 30)))
    print("Used: %d GB" % (used // (2 ** 30)))


def get_dir_info():
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
    print("Compressing movies in Ready for Compression...")
    queued = Directories.queued.get_movies()
    total_tasks = len(queued)
    current_task = 0
    master_start_time = time.time()
    logger = Logger()
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
        output_log = f"Compressed {movie.name} from {movie.size} GB to {compressed_movie_size} " \
                     f"GB in {helpers.run_time(start_time)}"
        log_cache.append(output_log)

    print()
    logger.log_and_print(f"Completed {total_tasks} compression(s) in {helpers.run_time(master_start_time)}")
    for log in log_cache:
        logger.log_and_print(log)
    print()


def upload_to_nas():
    print("Uploading movies in Ready for Upload...")
    num_uploads = Directories.ready.get_movies_cnt()
    uploads_left = Directories.ready.get_movies_cnt()
    size_total = Directories.ready.get_size()
    start_time = time.time()

    for movie in Directories.ready.get_movies():
        print(f"{uploads_left} movie(s) left to upload - [{size_total} GB]")
        uploads_left = uploads_left - 1

        if movie.is_locked():
            continue

        movie.upload_to_nas()
        size_total = size_total - movie.size

    print(f"Uploaded {num_uploads} movies in {helpers.run_time(start_time)}")


def dev_func():
    statistics.add_stat(14, 555555)
    statistics.read_stat()
    sys.exit()


def mark_failure():
    check_name()
    last_rip = Directories.downloads.get_movies()[0]
    last_rip_name = last_rip.remove_extension()
    confirmed = inquirer.confirm(message=f"Are you sure you want to mark {last_rip_name} as a failure?",
                                 raise_keyboard_interrupt=False).execute()
    if confirmed:
        file = open(const.failure_file, 'r+')
        if last_rip_name not in file.read():
            file.write("\n" + last_rip_name)
            file.close()
            last_rip.delete()
        else:
            print("This entry is already marked as a failure")


def mark_series():
    series = inquirer.text(message="What is the name of the series?: ", raise_keyboard_interrupt=False).execute()
    file = open(const.series_file, 'r+')
    if series not in file.read():
        file.write("\n" + series)
        file.close()
    else:
        print("This entry is already marked as a series")
