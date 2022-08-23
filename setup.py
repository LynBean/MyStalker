#!/usr/bin/env python3

import re
import os
import sys
from setuptools import setup


if sys.version_info < (3, 5):
    sys.exit('MyStalker requires Python >= 3.5.')

with open('README.md', 'r', encoding = 'UTF-8') as README :
    LongDescription = README.read()

def get_version():
    SRC = os.path.abspath(os.path.dirname(__file__))
    PATH = os.path.join(SRC, 'mystalker/__init__.py')

    with open(PATH, encoding = 'UTF-8') as f:
        for line in f:
            m = re.match("__version__ = '(.*)'", line)
            if m:
                return m.group(1)
    raise SystemExit('Could not find version string.')


setup(
    name = 'MyStalker',
    version = get_version(),
    description = "Get your friend's NRIC number with this program.",
    author = 'Asuna',
    author_email = '2003victoryy@1utar.my',
    url = 'https://github.com/LynBean/MyStalker',
    license = 'GPL-3.0',
    packages = ['mystalker'],
    zip_safe = False,
    python_requires = '>=3.5',
    install_requires = [
        'argparse',
        'bs4',
        'colorama',
        'lxml',
        'pandas',
        'platformdirs',
        'requests',
        'tabulate',
        'urllib3',
        ],
    entry_points = {
        'console_scripts': [
            'mystalker = mystalker.__main__: main'
            ],
    },
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords = (
        ['malaysia', 'malaysia-nric', 'malaysia-stalker', 'sapsnkra.moe.gov.my']
    ),
    long_description = LongDescription,
    long_description_content_type = 'text/markdown',
)
