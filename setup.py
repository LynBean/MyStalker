import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 10):
    sys.exit('Sorry, Python < 3.10 is not supported')

with open("README.md", "r") as README :
    LongDescription = README.read()

setup(
    name = "MYScraper",
    version = "2.1.1",
    description = "Scrap user Identity by spamming requests to a government website",
    author = "Asuna",
    author_email = "2003victoryy@1utar.my",
    url = "https://github.com/victoryy2003/Malaysian-Identity-Scraper",
    license = "GPL-3.0",
    packages = find_packages (exclude = ["test"]),
    zip_safe = False,
    python_requires = ">=3.10.0",
    install_requires = [
        "pywin32",
        "DateTime",
        "requests",
        "urllib3",
        "bs4",
        "lxml"
        ],
    entry_points = {
        "console_scripts": ["MYScraper = src.__main__:main"],
    },
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description = LongDescription,
    long_description_content_type = "text/markdown",
)