from os import path


class Directories:
    def __init__(self):
        self.base_dir = "E:/Plex Movies"
        self.download_dir = self.prepend_base_dir("Downloaded")
        self.compression_dir = self.prepend_base_dir("Ready for Compression")
        self.upload_dir = self.prepend_base_dir("Ready for Upload")

    def prepend_base_dir(self, input_dir):
        return path.join(self.base_dir, input_dir)
