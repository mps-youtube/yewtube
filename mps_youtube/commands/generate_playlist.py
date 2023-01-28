"""
    Playlist Generation
"""
from os import path
from random import choice
import string

from .. import content, g, playlists, screen, util, listview
from ..playlist import Playlist
from . import command, search, album_search


@command(r'mkp\s*(.{1,100})', 'mkp')
def generate_playlist(sourcefile):
    """Generate a playlist from video titles in sourcefile"""

    # Hooks into this, check if the argument --description is present
    if "--description" in sourcefile or "-d" in sourcefile:
        description_generator(sourcefile)
        return

    expanded_sourcefile = path.expanduser(sourcefile)
    if not check_sourcefile(expanded_sourcefile):
        g.message = util.F('mkp empty') % expanded_sourcefile
    else:
        queries = read_sourcefile(expanded_sourcefile)
        g.message = util.F('mkp parsed') % (len(queries), sourcefile)
        if queries:
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


def create_playlist(queries, title=''):
    """Add a new playlist

    Create playlist with a random name, get the first
    match for each title in queries and append it to the playlist
    """
    plname = title.replace(" ", "-") or random_plname()
    if not g.userpl.get(plname):
        g.userpl[plname] = Playlist(plname)
    for query in queries:
        g.message = util.F('mkp finding') % query
        screen.update()
        qresult = find_best_match(query)
        if qresult:
            g.userpl[plname].songs.append(qresult)
    if g.userpl[plname]:
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
    return None


def random_plname():
    """Generates a random alphanumeric string of 6 characters"""
    n_chars = 6
    return ''.join(choice(string.ascii_lowercase + string.digits)
                   for _ in range(n_chars))


def description_generator(text):
    """ Fetches a videos description and parses it for
        <artist> - <track> combinations
    """
    if not isinstance(g.model, Playlist):
        g.message = util.F("mkp desc unknown")
        return

    # Use only the first result, for now
    num = text.replace("--description", "")
    num = num.replace("-d", "")
    num = util.number_string_to_list(num)[0]

    query = {}
    query['id'] = g.model[num].ytid
    query['part'] = 'snippet'
    query['maxResults'] = '1'
    data = pafy.call_gdata('videos', query)['items'][0]['snippet']
    title = "mkp %s" % data['title']
    data = util.fetch_songs(data['description'], data['title'])

    columns = [
        {"name": "idx", "size": 3, "heading": "Num"},
        {"name": "artist", "size": 30, "heading": "Artist"},
        {"name": "title", "size": "remaining", "heading": "Title"},
    ]

    def run_m(idx):
        """ Create playlist based on the
            results selected
        """
        create_playlist(idx, title)

    if data:
        data = [listview.ListSongtitle(x) for x in data]
        g.content = listview.ListView(columns, data, run_m)
        g.message = util.F("mkp desc which data")
    else:
        g.message = util.F("mkp no valid")

    return
