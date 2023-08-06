"""
This file will contain all exceptions used in the rest of this project.
"""

# Python
from pathlib import Path


class TBadEncoding(Exception):
    """
    Used when de-serializing some jsonpickle file that does not correspond to the expected object.
    """
    def __init__(self, path: Path, expected: type, actual: type):
        super().__init__(f"{path} serialized file was not the object type it was supposed to be:\n"
                         f"Expected type:\t\t{expected}\n"
                         f"De-serialized type:\t{actual}")
