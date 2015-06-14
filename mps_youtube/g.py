""" Module for holding globals that are needed throught mps-youtube. """

import os
import sys
import collections

from .playlist import Playlist
from .paths import get_config_dir


transcoder_path = "auto"
delete_orig = True
encoders = []
muxapp = False
meta = {}
detectable_size = True
command_line = False
debug_mode = False
preload_disabled = False
ytpls = []
mpv_version = 0, 0, 0
mpv_usesock = False
mprisctl = None
browse_mode = "normal"
preloading = []
# expiry = 5 * 60 * 60  # 5 hours
no_clear_screen = False
helptext = []
max_retries = 3
max_cached_streams = 1500
url_memo = collections.OrderedDict()
username_query_cache = collections.OrderedDict()
model = Playlist(name="model")
last_search_query = {}
current_page = 0
result_count = 0
more_pages = None
rprompt = None
active = Playlist(name="active")
text = {}
userpl = {}
ytpl = {}
pafs = collections.OrderedDict()
streams = collections.OrderedDict()
pafy_pls = {}  #
last_opened = message = content = ""
suffix = "3" # Python 3
CFFILE = os.path.join(get_config_dir(), "config")
TCFILE = os.path.join(get_config_dir(), "transcode")
OLD_PLFILE = os.path.join(get_config_dir(), "playlist" + suffix)
PLFILE = os.path.join(get_config_dir(), "playlist_v2")
CACHEFILE = os.path.join(get_config_dir(), "cache_py_" + sys.version[0:5])
READLINE_FILE = None
playerargs_defaults = {
    "mpv": {
        "msglevel": {"<0.4": "--msglevel=all=no:statusline=status",
                     ">=0.4": "--msg-level=all=no:statusline=status"},
        "title": "--title",
        "fs": "--fs",
        "novid": "--no-video",
        "ignidx": "--demuxer-lavf-o=fflags=+ignidx",
        "geo": "--geometry"},
    "mplayer": {
        "title": "-title",
        "fs": "-fs",
        "novid": "-novideo",
        # "ignidx": "-lavfdopts o=fflags=+ignidx".split()
        "ignidx": "",
        "geo": "-geometry"}
    }
argument_commands = []
