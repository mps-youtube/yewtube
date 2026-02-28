"""Module for holding globals that are needed throught mps-youtube."""

import collections
import os
import sys

from . import c, paths
from .playlist import Playlist

volume = None
transcoder_path = "auto"
delete_orig = True
encoders = []
muxapp = False
meta = {}
artist = ""  # Mostly used for scrobbling purposes
album = ""  # Mostly used for scrobbling purposes
scrobble = False
scrobble_queue = []
lastfm_network = None
detectable_size = True
command_line = False
debug_mode = False
preload_disabled = False
ytpls = []
mpv_version = 0, 0, 0
mpv_options = None
mpv_usesock = False
mplayer_version = 0
mprisctl = None
browse_mode = "normal"
preloading = []
# expiry = 5 * 60 * 60  # 5 hours
no_clear_screen = False
no_textart = False
max_retries = 3
max_cached_streams = 1500
username_query_cache = collections.OrderedDict()
model = Playlist(name="model")
last_search_query = (None, None)
current_page = 0
result_count = 0
rprompt = None
active = Playlist(name="active")
userpl = {}
userhist = {}
metadata_cache = collections.OrderedDict()
streams = collections.OrderedDict()
playlist_cache = {}  #
selected_playlist_id = ""
last_opened = message = content = ""
suffix = "3"  # Python 3
OLD_CFFILE = os.path.join(paths.get_config_dir(), "config")
CFFILE = os.path.join(paths.get_config_dir(), "config.json")
TCFILE = os.path.join(paths.get_config_dir(), "transcode")
OLD_PLFILE = os.path.join(paths.get_config_dir(), "playlist" + suffix)
PLFILE = os.path.join(paths.get_config_dir(), "playlist_v2")
PLFOLDER = os.path.join(paths.get_config_dir(), "playlists")
OLDHISTFILE = os.path.join(paths.get_config_dir(), "play_history")
HISTFILE = os.path.join(paths.get_config_dir(), "play_history.m3u")
CACHEFILE = os.path.join(paths.get_config_dir(), "cache_py_" + sys.version[0:5])
READLINE_FILE = None
PLAYER_OBJ = None
categories = {
    "film": 1,
    "autos": 2,
    "music": 10,
    "sports": 17,
    "travel": 19,
    "gaming": 20,
    "blogging": 21,
    "news": 25,
}
playerargs_defaults = {
    "mpv": {
        "msglevel": {
            "<0.4": "--msglevel=all=no:statusline=status",
            ">=0.4": "--msg-level=all=no,statusline=status",
        },
        "title": "--force-media-title",
        "fs": "--fs",
        "novid": "--no-video",
        "ignidx": "--demuxer-lavf-o=fflags=+ignidx",
        "geo": "--geometry",
    },
    "mplayer": {
        "title": "-title",
        "fs": "-fs",
        "novid": "-novideo",
        # "ignidx": "-lavfdopts o=fflags=+ignidx".split()
        "ignidx": "",
        "geo": "-geometry",
    },
    "vlc": {"title": "--meta-title"},
}
argument_commands = []
commands = []

from .i18n import text
