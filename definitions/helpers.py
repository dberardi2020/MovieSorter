import re
import time

from Classes import Directories
from Classes import Movie
from definitions import const


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
    if not line.startswith("Encoding:"):
        return False

    if line == "":
        return False

    logger.log(line)

    percent = re.search(const.percent_pattern, line)
    eta = re.search(const.eta_pattern, line)

    if not percent or not eta:
        return False

    try:
        percent = int(float(percent.group(1)))
        eta = eta.group(1)
    except ValueError:
        return False

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
