import os
import shutil
import subprocess
import time
from os import path

from InquirerPy import inquirer

from Classes.Directories import Directories
from Classes.Movies import Movies
from definitions import helpers

upload_limit = 6

Directories = Directories()


# TODO: fix error if file is busy.  May require refactor
def check_name():
    Movies(Directories.download_dir).print()
    check_path = path.join(Directories.download_dir, "title.mkv")
    if path.exists(check_path):
        name = inquirer.text(message="Please rename title.mkv in Downloaded: ").execute()
        new_path = path.join(Directories.download_dir, name + ".mkv")
        os.rename(check_path, new_path)


def get_external_info():
    total, used, free = shutil.disk_usage(Directories.external_drive_letter)

    print("Total: %d GB" % (total // (2 ** 30)))
    print("Free: %d GB" % (free // (2 ** 30)))
    print("Used: %d GB" % (used // (2 ** 30)))


def get_dir_info():
    Movies(Directories.download_dir).print()
    Movies(Directories.compression_dir).print()
    Movies(Directories.upload_dir).print()


# def get_dir_info():
#     Movies.downloaded.print()
#     Movies.queued.print()
#     Movies.ready.print()


def sort():
    sort_downloaded()
    clean_compression_queue()
    get_dir_info()


def sort_downloaded():
    check_name()
    print("Sorting movies in Downloaded...")
    downloaded = Movies(Directories.download_dir)

    for movie in downloaded.movies:
        if movie.is_locked():
            continue

        if movie.num_gb < upload_limit:
            movie.move_to_upload()
        else:
            movie.move_to_compression()


def clean_compression_queue():
    print("Cleaning movies in Ready for Compression...")
    queued = Movies(Directories.compression_dir)
    done = Movies(Directories.upload_dir)

    for movie in queued.movies:
        for done_movie in done.movies:
            if movie.name_raw == done_movie.name_raw:
                if not done_movie.is_locked():
                    movie.delete()


def run_compression():
    print("Compressing movies in Ready for Compression...")
    queued = Movies(Directories.compression_dir)
    master_start_time = time.time()
    logs = []
    for movie in queued.movies:
        output_path = path.join(Directories.upload_dir, movie.name).replace(".mkv", ".mp4")
        handbrake_command = [r"HandBrakeCLI.exe", "-i", f"{movie.path}", "-o",
                             f"{output_path}", "-e", "x264", "-q", "20", "-B", "160"]
        start_time = time.time()
        process = subprocess.Popen(handbrake_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True)

        for line in process.stdout:
            if line.startswith("Encoding:"):
                print(line)

        compressed_movie_size = helpers.convert_to_gb(path.getsize(output_path))
        output_log = f"Compressed {movie.name} from {movie.num_gb} GB to {compressed_movie_size} " \
                     f"GB in {run_time(start_time)}"
        logs.append(output_log)

    print("Completed", queued.length(), "compression(s) in", run_time(master_start_time))
    for log in logs:
        print(log)


def upload_to_nas():
    print("Uploading movies in Ready for Upload...")
    uploads = Movies(Directories.upload_dir)
    num_uploads = uploads.length()
    uploads_cnt = num_uploads
    size_total = uploads.num_gb
    start_time = time.time()

    for movie in uploads.movies:
        size_total = size_total - movie.num_gb
        print(f"{uploads_cnt} movie(s) left to upload - [{size_total} GB]")
        uploads_cnt = uploads_cnt - 1

        if movie.is_locked():
            continue

        movie.upload_to_nas()

    print(f"Uploaded {num_uploads} movies in {run_time(start_time)}")


# Helper Functions
def run_time(start_time):
    seconds = time.time() - start_time
    return time.strftime("%H:%M:%S", time.gmtime(seconds))
