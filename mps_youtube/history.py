import os
import pickle

from . import g, c
from .util import dbg
from .playlist import Playlist
from .playlists import read_m3u


def add(song):
    """ Add song to history. """
    if not g.userhist.get('history'):
        g.userhist['history'] = Playlist('history')

    g.userhist['history'].songs.append(song)

    save()


def load():
    """ Open history. Called once on script invocation. """
    _convert_to_m3u()
    try:
        g.userhist['history'] = read_m3u(g.HISTFILE)

    except FileNotFoundError:
        # no playlist found, create a blank one
        if not os.path.isfile(g.HISTFILE):
            g.userhist = {}
            save()


def save():
    """ Save history.  Called each time history is updated. """
    with open(g.HISTFILE, 'w') as hf:
        hf.write('#EXTM3U\n\n')
        if 'history' in g.userhist:
            for song in g.userhist['history'].songs:
                hf.write('#EXTINF:%d,%s\n' % (song.length, song.title))
                hf.write('https://www.youtube.com/watch?v=%s\n' % song.ytid)

    dbg(c.r + "History saved\n---" + c.w)

def _convert_to_m3u():
    """ Converts the play_history file to the m3u format. """
    # Skip if m3u file already exists
    if os.path.isfile(g.HISTFILE):
        return

    elif not os.path.isfile(g.OLDHISTFILE):
        return

    with open(g.OLDHISTFILE, "rb") as hf:
        g.userhist = pickle.load(hf)

    save()
