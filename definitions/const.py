import shutil
from os import path

dev = False

upload_limit = 8

external_drive = "E:"

if dev:
    base_dir = path.join(external_drive, "Test Movies")
else:
    base_dir = path.join(external_drive, "Plex Movies")

data_dir = path.join(base_dir, "data")

log_dir = path.join(data_dir, "logs")

nas_dir = "//DimitriNAS/Movies"

failure_file = path.abspath("./records/failures.txt")
series_file = path.abspath("./records/series.txt")

percent_pattern = ", (.*?) %"
eta_pattern = "ETA (.*?)\\)"

if dev:
    dev_flag = "[Dev Mode] "
else:
    dev_flag = ""

if shutil.disk_usage(external_drive).used > shutil.disk_usage(external_drive).free:
    compression_warning = "[WARNING] - Disk Usage Exceeds 50%"
else:
    compression_warning = ""
