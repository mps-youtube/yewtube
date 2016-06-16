import os
import pickle

from . import g, c
from .util import dbg
from .playlist import Playlist


def add(song):
    """ Add song to history. """
    if not g.userhist.get('history'):
        g.userhist['history'] = Playlist('history')

    g.userhist['history'].songs.append(song)

    save()


def load():
    """ Open history. Called once on script invocation. """
    try:

        with open(g.HISTFILE, "rb") as hlf:
            g.userhist = pickle.load(hlf)

    except IOError:
        # no playlist found, create a blank one
        if not os.path.isfile(g.HISTFILE):
            g.userhist = {}
            save()


def save():
    """ Save history.  Called each time history is updated. """
    with open(g.HISTFILE, "wb") as hlf:
        pickle.dump(g.userhist, hlf, protocol=2)

    dbg(c.r + "History saved\n---" + c.w)
