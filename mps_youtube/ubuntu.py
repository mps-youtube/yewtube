"""
ubuntu.py - install ubuntu desktop file, needed for mpris.

https://github.com/np1/mps-youtube
"""

import os
import subprocess

desktop_file_contents = """\
[Desktop Entry]
Name=mps-youtube
GenericName=Music Player
Keywords=Audio;Song;Podcast;Playlist;youtube.com;
Exec=mpsyt %U
Terminal=true
Icon=terminal
Type=Application
Categories=AudioVideo;Audio;Player;
StartupNotify=true"""


def install_desktop_file(configdir, local_app_dir):
    """ Install desktop file if it hasn't already been done. """
    if not os.path.exists(local_app_dir):
        os.makedirs(local_app_dir)

    fname = "/tmp/mps-youtube.desktop"

    with open(fname, "w") as dtf:
        dtf.write(desktop_file_contents)

    cmd = ["desktop-file-install", "--dir={}".format(local_app_dir), fname]
    subprocess.call(cmd)
    os.unlink(fname)
