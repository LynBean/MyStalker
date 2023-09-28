
import urllib3

from .__main__ import main

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = '3.1.0'
