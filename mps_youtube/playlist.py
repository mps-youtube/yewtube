import time
import pickle
import os
import sys

from . import g
from .util import dbg


class Playlist(object):

    """ Representation of a playist, has list of songs. """

    def __init__(self, name=None, songs=None):
        """ class members. """
        self.name = name
        self.creation = time.time()
        self.songs = songs or []

    @property
    def is_empty(self):
        """ Return True / False if songs are populated or not. """
        return not self.songs

    @property
    def size(self):
        """ Return number of tracks. """
        return len(self.songs)

    @property
    def duration(self):
        """ Sum duration of the playlist. """
        duration = sum(s.length for s in self.songs)
        duration = time.strftime('%H:%M:%S', time.gmtime(int(duration)))
        return duration


class Video(object):

    """ Class to represent a YouTube video. """

    def __init__(self, ytid, title, length):
        """ class members. """
        self.ytid = ytid
        self.title = title
        self.length = int(length)


def save_to_file():
    """ Save playlists.  Called each time a playlist is saved or deleted. """
    with open(g.PLFILE, "wb") as plf:
        pickle.dump(g.userpl, plf, protocol=2)

    dbg(c.r + "Playlist saved\n---" + c.w)


def open_from_file():
    """ Open playlists. Called once on script invocation. """
    try:

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

    except IOError:
        # no playlist found, create a blank one
        if not os.path.isfile(g.PLFILE):
            g.userpl = {}
            save_to_file()

    except AttributeError:
        # playlist is from a time when this module was __main__
        # https://github.com/np1/mps-youtube/issues/214
        import __main__
        __main__.Playlist = Playlist
        __main__.Video = Video

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

        save_to_file()
        xprint("Updated playlist file. Please restart mpsyt")
        sys.exit()

    except EOFError:
        xprint("Error opening playlists from %s" % g.PLFILE)
        sys.exit()

    # remove any cached urls from playlist file, these are now
    # stored in a separate cache file

    save = False

    for k, v in g.userpl.items():

        for song in v.songs:

            if hasattr(song, "urls"):
                dbg("remove %s: %s", k, song.urls)
                del song.urls
                save = True

    if save:
        save_to_file()


def convert_playlist_to_v2():
    """ Convert previous playlist file to v2 playlist. """
    # skip if previously done
    if os.path.isfile(g.PLFILE):
        return

    # skip if no playlist files exist
    elif not os.path.isfile(g.OLD_PLFILE):
        return

    try:
        with open(g.OLD_PLFILE, "rb") as plf:
            old_playlists = pickle.load(plf)

    except IOError:
        sys.exit("Couldn't open old playlist file")

    # rename old playlist file
    backup = g.OLD_PLFILE + "_v1_backup"

    if os.path.isfile(backup):
        sys.exit("Error, backup exists but new playlist exists not!")

    os.rename(g.OLD_PLFILE, backup)

    # do the conversion
    for plname, plitem in old_playlists.items():

        songs = []

        for video in plitem.songs:
            v = Video(video['link'], video['title'], video['duration'])
            songs.append(v)

        g.userpl[plname] = Playlist(plname, songs)

    # save as v2
    save_to_file()
