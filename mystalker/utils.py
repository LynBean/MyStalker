
import os
from enum import Enum
from pathlib import Path

from .constants import APP_AUTHOR
from .constants import APP_NAME


class WhichOS(Enum):
    Windows = "Windows"
    Linux = "Linux"

def get_os() -> WhichOS:
    """Returns the current operating system.
    For saved file directory purposes.
    """
    if os.name == "nt":
        return WhichOS.Windows
    if os.name == "posix":
        return WhichOS.Linux
    return None

def get_data_dir() -> Path:
    """Returns the directory where the data is stored.
    """
    if get_os() == WhichOS.Windows:
        return Path().home().joinpath("Documents", APP_AUTHOR, APP_NAME).resolve()
    if get_os() == WhichOS.Linux:
        return Path().home().joinpath(".local", "share", APP_AUTHOR, APP_NAME).resolve()
    return Path().home().joinpath(APP_AUTHOR, APP_NAME).resolve()

# Initialize the data directory
DATA_DIR = get_data_dir()
DATA_DIR.mkdir(parents = True, exist_ok = True)
