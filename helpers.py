import time


def convert_to_gb(size_in_bytes):
    return round(size_in_bytes * (10 ** -9))


def run_time(start_time):
    seconds = time.time() - start_time
    return time.strftime("%H:%M:%S", time.gmtime(seconds))
