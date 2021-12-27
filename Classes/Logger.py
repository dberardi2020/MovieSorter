from datetime import datetime
from os import path, mkdir

from definitions import const


class Logger:
    def __init__(self):
        log_folder = path.join(const.log_dir, datetime.now().strftime('%m-%d-%Y @ %Hh%Mm%Ss'))
        mkdir(log_folder)
        log_file_name = path.join(log_folder, "compression_log.txt")
        extended_log_file_name = path.join(log_folder, "extended_compression_log.txt")

        self.log_file = open(log_file_name, 'w')
        self.extended_log_file = open(extended_log_file_name, 'w')

    def log(self, line):
        self.extended_log_file.write(line + "\n")

    def log_and_print(self, line):
        self.log_file.write(line + "\n")
        print(line)

    def close(self):
        self.log_file.close()
        self.extended_log_file.close()
