#!/usr/bin/python

""" setup.py for mps-youtube.

https://np1.github.com/mps-youtube

python setup.py sdist bdist_wheel
"""

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

setup(
    name="mps-youtube",
    version="0.2.3",
    description="Terminal based YouTube player and downloader",
    keywords=["video", "music", "audio", "youtube", "stream", "download"],
    author="np1",
    author_email="np1nagev@gmail.com",
    url="http://github.com/np1/mps-youtube",
    download_url="https://github.com/np1/mps-youtube/tarball/master",
    packages=['mps_youtube'],
    entry_points=dict(console_scripts=['mpsyt = mps_youtube:main.main']),
    install_requires=['pafy >= 0.3.72'],
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
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
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    long_description=open("README.rst").read()
)
