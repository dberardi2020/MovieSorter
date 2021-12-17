from os import path

dev = True

upload_limit = 8

external_drive = "E:"

if dev:
    base_dir = path.join(external_drive, "Test Movies")
else:
    base_dir = path.join(external_drive, "Plex Movies")

data_dir = path.join(base_dir, "data")
log_dir = path.join(data_dir, "logs")

nas_dir = "//DimitriNAS/Movies"

stats_file = path.join(data_dir, "stats.json")
