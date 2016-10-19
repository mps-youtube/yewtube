import math
import random

import pafy

from .. import g, c, screen, streams, content, util
from ..playlist import Video
from . import command, PL


def paginatesongs(func, page=0, splash=True, dumps=False,
        length=None, msg=None, failmsg=None, loadmsg=None):
    """
    A utility function for handling lists of songs, so that
    the pagination and the dump command will work properly.

    :param func: Either a function taking a start and end index,
        or a slicable object. Either way, it should produce an iterable
        of :class:`mps_youtube.playlist.Video` objects.
    :param page: The page number to display
    :param splash: Whether or not to display a splash screen while
        loading.
    :param dumps: Used by :func:`dump` command to load all songs, instead
        of only those that fit on a page
    :param length: The total number of songs. It it is not provided,
        ``len(func)`` will be used instead.
    :param msg: Message to display after loading successfully
    :param failmsg: Message to display on failure (if no songs are
        returned by func
    :param loadmsg: Message to display while loading
    :type page: int
    :type splash: bool
    :type dumps: bool
    :type length: int
    :type msg: str
    :type failmsg: str
    :type loadmsg: str
    """
    g.content = content.SongList(func, length=length, msg=msg,
            failmsg=failmsg, loadmsg=loadmsg)


@command(r'pl\s+%s' % PL)
def plist(parturl):
    """ Retrieve YouTube playlist. """

    if parturl in g.pafy_pls:
        ytpl, plitems = g.pafy_pls[parturl]
    else:
        util.dbg("%sFetching playlist using pafy%s", c.y, c.w)
        ytpl = pafy.get_playlist2(parturl)
        plitems = util.IterSlicer(ytpl)
        g.pafy_pls[parturl] = (ytpl, plitems)

    def pl_seg(s, e):
        return [Video(i.videoid, i.title, i.length) for i in plitems[s:e]]

    msg = "Showing YouTube playlist %s" % (c.y + ytpl.title + c.w)
    loadmsg = "Retrieving YouTube playlist"
    paginatesongs(pl_seg, length=len(ytpl), msg=msg, loadmsg=loadmsg)


@command(r'(rm|add)\s*(-?\d[-,\d\s]{,250})')
def songlist_rm_add(action, songrange):
    """ Remove or add tracks. works directly on user input. """
    selection = util.parse_multi(songrange)

    if action == "add":
        duplicate_songs = []
        for songnum in selection:
            if g.model[songnum - 1] in g.active:
                duplicate_songs.append(str(songnum))
            g.active.songs.append(g.model[songnum - 1])

        d = g.active.duration
        g.message = util.F('added to pl') % (len(selection), len(g.active), d)
        if duplicate_songs:
            duplicate_songs = ', '.join(sorted(duplicate_songs))
            g.message += '\n'
            g.message += util.F('duplicate tracks') % duplicate_songs

    elif action == "rm":
        selection = sorted(set(selection), reverse=True)
        removed = str(tuple(reversed(selection))).replace(",", "")

        for x in selection:
            g.model.songs.pop(x - 1)

        g.message = util.F('songs rm') % (len(selection), removed)

    g.content = content.generate_songlist_display()


@command(r'(mv|sw)\s*(\d{1,4})\s*[\s,]\s*(\d{1,4})')
def songlist_mv_sw(action, a, b):
    """ Move a song or swap two songs. """
    i, j = int(a) - 1, int(b) - 1

    if action == "mv":
        g.model.songs.insert(j, g.model.songs.pop(i))
        g.message = util.F('song move') % (g.model[j].title, b)

    elif action == "sw":
        g.model[i], g.model[j] = g.model[j], g.model[i]
        g.message = util.F('song sw') % (min(a, b), max(a, b))

    g.content = content.generate_songlist_display()


@command(r'(n|p)\s*(\d{1,2})?')
def nextprev(np, page=None):
    """ Get next / previous search results. """
    good = False
    if isinstance(g.content, content.PaginatedContent):
        page_count = g.content.numPages()

        if np == "n":
            if g.content.current_page + 1 < page_count:
                g.content.current_page += 1
                good = True

        elif np == "p":
            if page and int(page) in range(1,20):
                g.content.current_page = int(page)-1
                good = True

            elif g.content.current_page > 0:
                g.content.current_page -= 1
                good = True
    else:
        g.content = content.generate_songlist_display()

    if good:
        g.content.getPage(page=g.content.current_page)
    else:
        norp = "next" if np == "n" else "previous"
        g.message = "No %s items to display" % norp

    return good


@command(r'shuffle')
def shuffle_fn():
    """ Shuffle displayed items. """
    random.shuffle(g.model.songs)
    g.message = c.y + "Items shuffled" + c.w
    g.content = content.generate_songlist_display()


@command(r'reverse')
def reverse_songs():
    """ Reverse order of displayed items. """
    g.model.songs = g.model.songs[::-1]
    g.message = c.y + "Reversed displayed songs" + c.w
    g.content = content.generate_songlist_display()


@command(r'reverse\s*(\d{1,4})\s*-\s*(\d{1,4})\s*')
def reverse_songs_range(lower, upper):
    """ Reverse the songs within a specified range. """
    lower, upper = int(lower), int(upper)
    if lower > upper: lower, upper = upper, lower
    
    g.model.songs[lower-1:upper] = reversed(g.model.songs[lower-1:upper])
    g.message = c.y + "Reversed range: " + str(lower) + "-" + str(upper) + c.w
    g.content = content.generate_songlist_display()
    

@command(r'reverse all')
def reverse_playlist():
    """ Reverse order of entire loaded playlist. """
    # Prevent crash if no last query
    if g.last_search_query == (None, None) or \
            'func' not in g.last_search_query[1]:
        g.content = content.Logo()
        g.message = "No playlist loaded"
        return

    songs_list_or_func = g.last_search_query[1]['func']
    if callable(songs_list_or_func):
        songs = reversed(songs_list_or_func(0,None))
    else:
        songs = reversed(songs_list_or_func)

    paginatesongs(list(songs))
    g.message = c.y + "Reversed entire playlist" + c.w
    g.content = content.generate_songlist_display()
