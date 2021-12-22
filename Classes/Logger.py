from datetime import datetime
from os import path

from definitions import const


class Logger:
    def __init__(self):
        log_file_name = path.join(const.log_dir, f"compression_log_{datetime.now().strftime('%m-%d-%Y_%H%M%S')}.txt")
        extended_log_file_name = path.join(
            const.log_dir, f"extended_compression_log_{datetime.now().strftime('%m-%d-%Y_%H%M%S')}.txt")

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
