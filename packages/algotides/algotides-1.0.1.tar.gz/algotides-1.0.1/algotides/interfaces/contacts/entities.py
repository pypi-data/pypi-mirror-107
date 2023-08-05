# Python
from pathlib import Path
from sys import stderr


# Tides
from algotides import constants as constants


class Contact:
    """
    Object that represents a single contact in the contact list.
    """
    def __init__(self, pic_name: str, name: str, info: str):
        self.pic_name = pic_name
        self.name = name
        self.info = info

    def release(self):
        """
        Method to destroy profile picture on disk.
        """
        if self.pic_name:
            try:
                Path.joinpath(constants.path_thumbnails, self.pic_name).unlink()
            except FileNotFoundError as e:
                if __debug__:
                    print(type(e), str(e), file=stderr)
                print(f"Could not delete profile picture for {self.name}", file=stderr)
