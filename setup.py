#!/usr/bin/env python3

import re
import os
import sys
from typing import List
from setuptools import setup


if sys.version_info.major < 3 or sys.version_info.minor < 10:
    sys.exit("Requiring Python >= 3.10")

with open("README.md", "r", encoding = "UTF-8") as README :
    LongDescription = README.read()

def get_version():
    SRC = os.path.abspath(os.path.dirname(__file__))
    PATH = os.path.join(SRC, "mystalker/__init__.py")

    with open(PATH, encoding = "UTF-8") as f:
        for line in f:
            m = re.match("__version__ = '(.*)'", line)
            if m:
                return m.group(1)

    raise SystemExit("Could not find version string.")

dependencies: List[str] = [
    "argparse",
    "bs4",
    "lxml",
    "pandas",
    "requests",
    "urllib3",
]

if os.name == "nt":
    dependencies.append("windows-curses")


setup(
    name = "mystalker",
    version = get_version(),
    description = "Get your friend's NRIC number with this program.",
    author = "LynBean",
    author_email = "kim.is.fighting@gmail.com",
    url = "https://github.com/LynBean/MyStalker",
    license = "GPL-3.0",
    packages = ["mystalker"],
    zip_safe = False,
    python_requires = ">=3.5",
    install_requires = dependencies,
    entry_points = {
        "console_scripts": [
            "mystalker = mystalker.__main__: main"
        ],
    },
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords = (
        [
            "malaysia",
            "malaysia-nric",
            "malaysia-stalker",
            "sapsnkra.moe.gov.my"
        ]
    ),
    long_description = LongDescription,
    long_description_content_type = "text/markdown",
)
