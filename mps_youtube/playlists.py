import os
import sys
import pickle

from . import g, c, screen, util
from .playlist import Playlist, Video


def save():
    """ Save playlists.  Called each time a playlist is saved or deleted. """
    with open(g.PLFILE, "wb") as plf:
        pickle.dump(g.userpl, plf, protocol=2)

    util.dbg(c.r + "Playlist saved\n---" + c.w)


def load():
    """ Open playlists. Called once on script invocation. """
    _convert_playlist_to_v2()
    try:

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

    except IOError:
        # no playlist found, create a blank one
        if not os.path.isfile(g.PLFILE):
            g.userpl = {}
            save()

    except AttributeError:
        # playlist is from a time when this module was __main__
        # https://github.com/np1/mps-youtube/issues/214
        import __main__
        __main__.Playlist = Playlist
        __main__.Video = Video

        from . import main
        main.Playlist = Playlist
        main.Video = Video

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

        save()
        screen.msgexit("Updated playlist file. Please restart mpsyt", 1)

    except EOFError:
        screen.msgexit("Error opening playlists from %s" % g.PLFILE, 1)

    # remove any cached urls from playlist file, these are now
    # stored in a separate cache file

    do_save = False

    for k, v in g.userpl.items():

        for song in v.songs:

            if hasattr(song, "urls"):
                util.dbg("remove %s: %s", k, song.urls)
                del song.urls
                do_save = True

    if do_save:
        save()


def _convert_playlist_to_v2():
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
    save()
