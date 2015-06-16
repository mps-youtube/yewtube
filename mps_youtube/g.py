""" Module for holding globals that are needed throught mps-youtube. """

import os
import sys
import collections

from . import c
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

text = {
    "exitmsg": ("**0mps-youtube - **1http://github.com/np1/mps-youtube**0"
                "\nReleased under the GPLv3 license\n"
                "(c) 2014, 2015 np1 and contributors**2\n"""),
    "_exitmsg": (c.r, c.b, c.w),

    # Error / Warning messages

    'no playlists': "*No saved playlists found!*",
    'no playlists_': (c.r, c.w),
    'pl bad name': '*&&* is not valid a valid name. Ensure it starts with'
                   ' a letter or _',
    'pl bad name_': (c.r, c.w),
    'pl not found': 'Playlist *&&* unknown. Saved playlists are shown '
                    'above',
    'pl not found_': (c.r, c.w),
    'pl not found advise ls': 'Playlist "*&&*" not found. Use *ls* to '
                              'list',
    'pl not found advise ls_': (c.y, c.w, c.g, c.w),
    'pl empty': 'Playlist is empty!',
    'advise add': 'Use *add N* to add a track',
    'advise add_': (c.g, c.w),
    'advise search': 'Search for items and then use *add* to add them',
    'advise search_': (c.g, c.w),
    'no data': 'Error fetching data. Possible network issue.'
               '\n*&&*',
    'no data_': (c.r, c.w),
    'use dot': 'Start your query with a *.* to perform a search',
    'use dot_': (c.g, c.w),
    'cant get track': 'Problem playing last item: *&&*',
    'cant get track_': (c.r, c.w),
    'track unresolved': 'Sorry, this track is not available',
    'no player': '*&&* was not found on this system',
    'no player_': (c.y, c.w),
    'no pl match for rename': '*Couldn\'t find matching playlist to '
                              'rename*',
    'no pl match for rename_': (c.r, c.w),
    'invalid range': "*Invalid item / range entered!*",
    'invalid range_': (c.r, c.w),
    '-audio': "*Warning* - the filetype you selected (m4v) has no audio!",
    '-audio_': (c.y, c.w),
    'no mix': 'No mix is available for the selected video',
    'mix only videos': 'Mixes are only available for videos',
    'invalid item': '*Invalid item entered!*',

    # Info messages..

    'select mux': ("Select [*&&*] to mux audio or [*Enter*] to download "
                   "without audio\nThis feature is experimental!"),
    'select mux_': (c.y, c.w, c.y, c.w),
    'pl renamed': 'Playlist *&&* renamed to *&&*',
    'pl renamed_': (c.y, c.w, c.y, c.w),
    'pl saved': 'Playlist saved as *&&*.  Use *ls* to list playlists',
    'pl saved_': (c.y, c.w, c.g, c.w),
    'pl loaded': 'Loaded playlist *&&* as current playlist',
    'pl loaded_': (c.y, c.w),
    'pl viewed': 'Showing playlist *&&*',
    'pl viewed_': (c.y, c.w),
    'pl help': 'Enter *open <name or ID>* to load a playlist',
    'pl help_': (c.g, c.w),
    'added to pl': '*&&* tracks added (*&&* total [*&&*]). Use *vp* to '
                   'view',
    'added to pl_': (c.y, c.w, c.y, c.w, c.y, c.w, c.g, c.w),
    'added to saved pl': '*&&* tracks added to *&&* (*&&* total [*&&*])',
    'added to saved pl_': (c.y, c.w, c.y, c.w, c.y, c.w, c.y, c.w),
    'song move': 'Moved *&&* to position *&&*',
    'song move_': (c.y, c.w, c.y, c.w),
    'song sw': ("Switched item *&&* with *&&*"),
    'song sw_': (c.y, c.w, c.y, c.w),
    'current pl': "This is the current playlist. Use *save <name>* to save"
                  " it",
    'current pl_': (c.g, c.w),
    'help topic': ("  Enter *help <topic>* for specific help:"),
    'help topic_': (c.y, c.w),
    'songs rm': '*&&* tracks removed &&',
    'songs rm_': (c.y, c.w)}
