"""
This file will contain all constants needed throughout the rest of this project.
"""

# Python
from pathlib import Path


# Paths
# Single constants
path_app_data = Path.home().joinpath(".algo-tides/")
_filename_contacts_jpickle = Path("./contacts.jpickle")
_filename_settings_jpickle = Path("./settings.jpickle")
_folder_thumbnails = Path("./thumbnails/")

# Composite constants
path_contacts_jpickle = path_app_data.joinpath(_filename_contacts_jpickle)
path_settings_jpickle = path_app_data.joinpath(_filename_settings_jpickle)
path_thumbnails = path_app_data.joinpath(_folder_thumbnails)
