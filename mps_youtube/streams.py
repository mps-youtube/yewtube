import time

from . import g, c
from .util import dbg, get_pafy
from .config import Config


def prune():
    """ Keep cache size in check. """
    while len(g.pafs) > g.max_cached_streams:
        g.pafs.popitem(last=False)

    while len(g.streams) > g.max_cached_streams:
        g.streams.popitem(last=False)

    # prune time expired items

    now = time.time()
    oldpafs = [k for k in g.pafs if g.pafs[k].expiry < now]

    if len(oldpafs):
        dbg(c.r + "%s old pafy items pruned%s", len(oldpafs), c.w)

    for oldpaf in oldpafs:
        g.pafs.pop(oldpaf, 0)

    oldstreams = [k for k in g.streams if g.streams[k]['expiry'] < now]

    if len(oldstreams):
        dbg(c.r + "%s old stream items pruned%s", len(oldstreams), c.w)

    for oldstream in oldstreams:
        g.streams.pop(oldstream, 0)

    dbg(c.b + "paf: %s, streams: %s%s", len(g.pafs), len(g.streams), c.w)


def get(vid, force=False, callback=None, threeD=False):
    """ Get all streams as a dict.  callback function passed to get_pafy. """
    now = time.time()
    ytid = vid.ytid
    have_stream = g.streams.get(ytid) and g.streams[ytid]['expiry'] > now
    prfx = "preload: " if not callback else ""

    if not force and have_stream:
        ss = str(int(g.streams[ytid]['expiry'] - now) // 60)
        dbg("%s%sGot streams from cache (%s mins left)%s", c.g, prfx, ss, c.w)
        return g.streams.get(ytid)['meta']

    p = get_pafy(vid, force=force, callback=callback)
    ps = p.allstreams if threeD else [x for x in p.allstreams if not x.threed]

    try:
        # test urls are valid
        [x.url for x in ps]

    except TypeError:
        # refetch if problem
        dbg("%s****Type Error in get_streams. Retrying%s", c.r, c.w)
        p = get_pafy(vid, force=True, callback=callback)
        ps = p.allstreams if threeD else [x for x in p.allstreams
                                          if not x.threed]

    streams = []

    for s in ps:
        try:
            rawbitrate = s.rawbitrate
        except AttributeError:
            # Deal with bug in pafy before 88fda70 or 0.7.x
            rawbitrate = None

        x = dict(url=s.url,
                 ext=s.extension,
                 quality=s.quality,
                 rawbitrate=rawbitrate,
                 mtype=s.mediatype,
                 size=-1)
        streams.append(x)

    g.streams[ytid] = dict(expiry=p.expiry, meta=streams)
    prune()
    return streams


def select(slist, q=0, audio=False, m4a_ok=True, maxres=None):
    """ Select a stream from stream list. """
    maxres = maxres or Config.MAX_RES.get
    slist = slist['meta'] if isinstance(slist, dict) else slist
    au_streams = [x for x in slist if x['mtype'] == "audio"]

    def okres(x):
        """ Return True if resolution is within user specified maxres. """
        return int(x['quality'].split("x")[1]) <= maxres

    def getq(x):
        """ Return height aspect of resolution, eg 640x480 => 480. """
        return int(x['quality'].split("x")[1])

    def getbitrate(x):
        """Return the bitrate of a stream."""
        return x['rawbitrate']

    vo_streams = [x for x in slist if x['mtype'] == "normal" and okres(x)]
    vo_streams = sorted(vo_streams, key=getq, reverse=True)

    if not m4a_ok:
        au_streams = [x for x in au_streams if not x['ext'] == "m4a"]

    au_streams = sorted(au_streams, key=getbitrate, reverse=True)

    streams = au_streams if audio else vo_streams
    dbg("select stream, q: %s, audio: %s, len: %s", q, audio, len(streams))

    try:
        ret = streams[q]

    except IndexError:
        ret = streams[0] if q and len(streams) else None

    return ret
