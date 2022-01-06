import re
import time

from Classes import Directories
from Classes import Movie


def convert_to_gb(size_in_bytes):
    return round(size_in_bytes * (10 ** -9))


def format_time(seconds):
    return time.strftime("%Hh%Mm%Ss", time.gmtime(seconds))


def run_time(start_time):
    return time.time() - start_time


def get_all_movie() -> [Movie]:
    movies_array = [Directories.queued.get_movies(), Directories.ready.get_movies(), Directories.downloads.get_movies()]
    return [item for sublist in movies_array for item in sublist]


def process_compression_output(movie_name, current_task, total_tasks, line, target, logger):
    percent_pattern = ", (.*?) %"
    eta_pattern = "ETA (.*?)\\)"

    if not line.startswith("Encoding:"):
        return False

    if line == "":
        return False

    logger.log(line)

    percent = re.search(percent_pattern, line)
    eta = re.search(eta_pattern, line)

    if not percent or not eta:
        return False

    percent = int(float(percent.group(1)))
    eta = eta.group(1)

    if percent == target:
        spacing = "  "
        if target == 0:
            spacing = "   "
        elif target == 100:
            spacing = " "

        log = f"Encoding {movie_name}: task {current_task} of {total_tasks}, {percent}%{spacing}complete, ETA {eta}"
        logger.log(log)
        logger.log_and_print(log)
        return True
