from os import path

dev = False

if dev:
    dev_flag = "[Dev Mode]"
else:
    dev_flag = ""

upload_limit = 8

external_drive = "E:"

if dev:
    base_dir = path.join(external_drive, "Test Movies")
else:
    base_dir = path.join(external_drive, "Plex Movies")

data_dir = path.join(base_dir, "data")
stats_pickle = path.join(data_dir, "stats.pkl")

log_dir = path.join(data_dir, "logs")

nas_dir = "//DimitriNAS/Movies"

stats_file = path.join(data_dir, "stats.json")

failure_file = path.abspath("./records/failures.txt")
series_file = path.abspath("./records/series.txt")
