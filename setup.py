#!/usr/bin/python3

""" setup.py for yewtube.

https://github.com/iamtalhaasghar/yewtube

python setup.py sdist bdist_wheel
"""

import os
import sys

if sys.version_info < (3, 6):
    sys.exit("yewtube requires minimum python 3.6")

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.readlines()

__version__ = "2.8.2"

options = dict(
    name="yewtube",
    version=__version__,
    description="A Terminal based YouTube player and downloader. No Youtube API key required. Forked from mps-youtube",
    keywords=["video", "music", "audio", "youtube", "stream", "download"],
    author="talha_programmer",
    author_email="talhaasghar.contact@simplelogin.fr",
    url="https://github.com/iamtalhaasghar/yewtube",
    download_url="https://github.com/iamtalhaasghar/yewtube/releases",
    packages=['mps_youtube', 'mps_youtube.commands', 'mps_youtube.listview', 'mps_youtube.players'],
    entry_points={'console_scripts': ['yt = mps_youtube:main.main']},
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        "mpris": [
            "dbus-python>=1.2.18",
            "PyGObject>=3.42.0",
        ],
        "docs": [
            "mkdocs-gen-files>=0.3.4",
            "mkdocs-literate-nav>=0.4.1",
            "mkdocs-macros-plugin>=0.6.4",
            "mkdocs-material>=8.2.1",
            "mkdocstrings-python-legacy>=0.2.2",
            "mkdocstrings>=0.18.0",
        ],
    },
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Multimedia :: Video",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS 9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: Microsoft :: Windows :: Windows Vista",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    options={
        "py2exe": {
            "excludes": ("readline, win32api, win32con, dbus, gi,"
                         " urllib.unquote_plus, urllib.urlencode,"
                         " PyQt4, gtk"),
            "bundle_files": 1
        }
    },
    package_data={"": ["LICENSE", "README.md", "CHANGELOG.md"]},
    long_description_content_type='text/markdown',
    long_description=long_description
)

if sys.platform.startswith('linux'):
    # Install desktop file. Required for mpris on Ubuntu
    options['data_files'] = [('share/applications/', ['yewtube.desktop'])]

if os.name == "nt":
    try:
        import py2exe

        # Only setting these when py2exe imports successfully prevents warnings
        # in easy_install
        options['console'] = ['yt']
        options['zipfile'] = None
    except ImportError:
        pass

setup(**options)
