import os
import shutil
import subprocess
import sys
import time
from os import path

from InquirerPy import inquirer

from Classes import Directories
from definitions import const
from definitions import helpers

upload_limit = 6


# TODO: fix error if file is busy.  May require refactor
def check_name():
    check_path = Directories.downloads.append("title.mkv")
    if path.exists(check_path):
        Directories.downloads.print()
        name = inquirer.text(message="Please rename title.mkv in Downloaded: ").execute()
        new_path = Directories.downloads.append(name + ".mkv")
        os.rename(check_path, new_path)


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
    print()
    get_dir_info()


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


def clean_compression_queue():
    print("Cleaning movies in Ready for Compression...")

    # TODO: this needs to check the movie being written, not read
    for movie in Directories.queued.get_movies():
        if movie.is_compressed() and not movie.is_locked():
            movie.delete()


def run_compression():
    print("Compressing movies in Ready for Compression...")
    queued = Directories.queued.get_movies()
    master_start_time = time.time()
    logs = []
    for movie in queued:
        output_path = Directories.ready.append(movie.name).replace(".mkv", ".mp4")
        handbrake_command = [r"HandBrakeCLI.exe", "-i", f"{movie.path}", "-o",
                             f"{output_path}", "-e", "x264", "-q", "20", "-B", "160"]
        start_time = time.time()
        process = subprocess.Popen(handbrake_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True)

        # TODO: figure out how to dump logs to file
        test_file = open(path.join(const.log_dir, "ExampleLog.txt"), 'w')
        for line in process.stdout:
            if line.startswith("Encoding:"):
                # test_file.write(line + "\n")
                print(line, file=open(path.join(const.log_dir, "ExampleLog.txt"), 'w'))

        compressed_movie_size = helpers.convert_to_gb(path.getsize(output_path))
        output_log = f"Compressed {movie.name} from {movie.size} GB to {compressed_movie_size} " \
                     f"GB in {helpers.run_time(start_time)}"
        logs.append(output_log)

    print("Completed", len(queued), "compression(s) in", helpers.run_time(master_start_time))
    for log in logs:
        print(log)


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
    pass
    sys.exit()
