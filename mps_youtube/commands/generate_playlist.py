from os import path
import pafy
from random import choice
import string

from .. import content, g, playlists, screen, util
from ..playlist import Playlist
from . import command, search, album_search


@command(r'mkp\s*(.{1,100})')
def generate_playlist(sourcefile):
    """Generate a playlist from video titles in sourcefile"""
    expanded_sourcefile = path.expanduser(sourcefile)
    if not check_sourcefile(expanded_sourcefile):
        g.message = util.F('mkp empty') % expanded_sourcefile
    else:
        queries = read_sourcefile(expanded_sourcefile)
        g.message = util.F('mkp parsed') % (len(queries), sourcefile)
        if len(queries) > 0:
            create_playlist(queries)
            g.message = util.F('pl help')
            g.content = content.playlists_display()


def read_sourcefile(filename):
    """Read each line as a query from filename"""
    with open(filename) as srcfl:
        queries = list()
        for item in srcfl.readlines():
            clean_item = str(item).strip()
            if not clean_item:
                continue
            queries.append(clean_item)
        return queries


def check_sourcefile(filename):
    """Check if filename exists and has a non-zero size"""
    return path.isfile(filename) and path.getsize(filename) > 0


def create_playlist(queries):
    """Add a new playlist

    Create playlist with a random name, get the first
    match for each title in queries and append it to the playlist
    """
    plname = random_plname()
    if not g.userpl.get(plname):
        g.userpl[plname] = Playlist(plname)
    for query in queries:
        g.message = util.F('mkp finding') % query
        screen.update()
        qresult = find_best_match(query)
        if qresult:
            g.userpl[plname].songs.append(qresult)
    if len(g.userpl[plname]) > 0:
        playlists.save()


def find_best_match(query):
    """Find the best(first)"""
    # This assumes that the first match is the best one
    qs = search.generate_search_qs(query)
    wdata = pafy.call_gdata('search', qs)
    results = search.get_tracks_from_json(wdata)
    if results:
        res, score = album_search._best_song_match(
            results, query, 0.1, 1.0, 0.0)
        return res


def random_plname():
    """Generates a random alphanumeric string of 6 characters"""
    n_chars = 6
    return ''.join(choice(string.ascii_lowercase + string.digits)
                   for _ in range(n_chars))
