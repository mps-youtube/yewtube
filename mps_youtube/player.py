import abc
import os
import sys
import random
import tempfile
import subprocess
import logging
import json
import re
import socket
import math
import time
import shlex
from urllib.error import HTTPError, URLError

from . import g, screen, c, streams, history, content, paths, config, util

class Player(metaclass=abc.ABCMeta):

    """This class should declare some abstract methods that all players
    must implement. Right now, only help method is used without any changes in all
    players. A default design, with declarations of abstract methods that are essential
    for all types of players must be written, instead of play_range and _playback_progress
    , which are currently only used as an example of the design logic."""

    def _help(self, short=True):
        """ Default help(uses mplayer's keys as help.). Should be implemented specifically
        for other players and its implementation should be on the equivalent subclass(and
        of course define _help as abstractmethod here), if every player uses its own keys. """

        mswin = os.name == "nt"
        not_utf8_environment = mswin or "UTF-8" not in sys.stdout.encoding


        # pylint: disable=W1402

        volume = "[{0}9{1}] volume [{0}0{1}]      [{0}CTRL-C{1}] return"
        seek = "[{0}\u2190{1}] seek [{0}\u2192{1}]"
        pause = "[{0}\u2193{1}] SEEK [{0}\u2191{1}]       [{0}space{1}] pause"

        if not_utf8_environment:
            seek = "[{0}<-{1}] seek [{0}->{1}]"
            pause = "[{0}DN{1}] SEEK [{0}UP{1}]       [{0}space{1}] pause"

        single = "[{0}q{1}] next"
        next_prev = "[{0}>{1}] next/prev [{0}<{1}]"
        # ret = "[{0}q{1}] %s" % ("return" if short else "next track")
        ret = single if short and config.AUTOPLAY.get else ""
        ret = next_prev if not short else ret
        fmt = "    %-20s       %-20s"
        lines = fmt % (seek, volume) + "\n" + fmt % (pause, ret)
        return lines.format(c.g, c.w)

    def _check_player(player_type):
        """
        Useful function to create the proper subclass instance when needed.
        Perhaps it could be in a different factory-like file, loaded here as
        a first functional attempt.
        """
        if "mpv" in player_type:
            from .players.mpv import Mpv
            return Mpv()
        elif "mplayer" in player_type:
            from .players.mplayer import Mplayer
            return Mplayer()
        elif "vlc" in player_type:
            from .players.vlc import Vlc
            return Vlc()
        else:
            from .players.other_players import OtherPlayers
            return OtherPlayers()

    @abc.abstractmethod
    def play_range(self, songlist, shuffle=False, repeat=False, override=False):
        """ Plays a range of songs included in songlist []. Shuffle, repeat and override
        values are set as False from default. Exits cleanly on keyboard interrupt.
        See mplayer class for an example of a detailed implementation of this method. """
        raise NotImplementedError('You must define play_range to use this base class')

    @abc.abstractmethod
    def _playback_progress(self, idx, allsongs, repeat=False):
        """ Generate string to show selected tracks, indicate current track. """
        raise NotImplementedError('You must define _playback_progress to use this base class')
