from os import path


# TODO: Refactor to include Directory class
class Directories:
    def __init__(self):
        self.external_drive_letter = "E:"
        self.base_dir = path.join(self.external_drive_letter, "Plex Movies")
        self.download_dir = self.prepend_base_dir("Downloaded")
        self.compression_dir = self.prepend_base_dir("Queued")
        self.upload_dir = self.prepend_base_dir("Ready")
        self.nas_dir = "//DimitriNAS/Movies"

    def prepend_base_dir(self, input_dir):
        return path.join(self.base_dir, input_dir)
