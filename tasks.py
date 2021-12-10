import os
import shutil
from Movies import Movies
from Directories import Directories
from os import path
import subprocess
import time
from InquirerPy import inquirer


upload_limit = 6

Directories = Directories()


def check_name():
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


def sort_downloaded():
    check_name()
    print("Sorting movies in Downloaded...")
    downloaded = Movies(Directories.download_dir)

    for movie in downloaded.get_movies():
        if movie.is_locked():
            continue

        if movie.size < upload_limit:
            movie.move_to_upload()
        else:
            movie.move_to_compression()


def clean_compression_queue():
    print("Sorting movies in Ready for Compression...")
    queued = Movies(Directories.compression_dir)
    done = Movies(Directories.upload_dir)

    for movie in queued.get_movies():
        for done_movie in done.get_movies():
            if movie.name_raw == done_movie.name_raw:
                if not done_movie.is_locked():
                    movie.delete()


def run_compression():
    print("Compressing movies in Ready for Compression...")
    queued = Movies(Directories.compression_dir)
    master_start_time = time.time()
    for movie in queued.get_movies():
        output_path = path.join(Directories.upload_dir, movie.name).replace(".mkv", ".mp4")
        handbrake_command = [r"HandBrakeCLI.exe", "-i", f"{movie.path}", "-o",
                             f"{output_path}", "-e", "x264", "-q", "20", "-B", "160"]
        start_time = time.time()
        subprocess.run(handbrake_command, shell=True)
        run_time = (time.time() - start_time) / 60
        print("Finished converting", movie.name, "in", run_time, "minutes")

    run_time = (time.time() - master_start_time) / 60
    print("Completed", queued.length(), "conversion(s) in", run_time, "minutes")


def upload_to_nas():
    print("Uploading movies in Ready for Upload")
    uploads = Movies(Directories.upload_dir)
    num_uploads = uploads.length()

    for movie in uploads.get_movies():
        print(f"{num_uploads} movies left to upload")
        num_uploads = num_uploads - 1

        if movie.is_locked():
            continue

        movie.upload_to_nas()
