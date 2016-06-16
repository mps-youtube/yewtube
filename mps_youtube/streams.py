import time
import threading
from urllib.request import urlopen

from . import g, c, screen, config, util


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
        util.dbg(c.r + "%s old pafy items pruned%s", len(oldpafs), c.w)

    for oldpaf in oldpafs:
        g.pafs.pop(oldpaf, 0)

    oldstreams = [k for k in g.streams if g.streams[k]['expiry'] < now]

    if len(oldstreams):
        util.dbg(c.r + "%s old stream items pruned%s", len(oldstreams), c.w)

    for oldstream in oldstreams:
        g.streams.pop(oldstream, 0)

    util.dbg(c.b + "paf: %s, streams: %s%s", len(g.pafs), len(g.streams), c.w)


def get(vid, force=False, callback=None, threeD=False):
    """ Get all streams as a dict.  callback function passed to get_pafy. """
    now = time.time()
    ytid = vid.ytid
    have_stream = g.streams.get(ytid) and g.streams[ytid]['expiry'] > now
    prfx = "preload: " if not callback else ""

    if not force and have_stream:
        ss = str(int(g.streams[ytid]['expiry'] - now) // 60)
        util.dbg("%s%sGot streams from cache (%s mins left)%s",
                c.g, prfx, ss, c.w)
        return g.streams.get(ytid)['meta']

    p = util.get_pafy(vid, force=force, callback=callback)
    ps = p.allstreams if threeD else [x for x in p.allstreams if not x.threed]

    try:
        # test urls are valid
        [x.url for x in ps]

    except TypeError:
        # refetch if problem
        util.dbg("%s****Type Error in get_streams. Retrying%s", c.r, c.w)
        p = util.get_pafy(vid, force=True, callback=callback)
        ps = p.allstreams if threeD else [x for x in p.allstreams
                                          if not x.threed]

    streams = [{"url": s.url,
                "ext": s.extension,
                "quality": s.quality,
                "rawbitrate": s.rawbitrate,
                "mtype": s.mediatype,
                "size": -1} for s in ps]

    g.streams[ytid] = dict(expiry=p.expiry, meta=streams)
    prune()
    return streams


def select(slist, q=0, audio=False, m4a_ok=True, maxres=None):
    """ Select a stream from stream list. """
    maxres = maxres or config.MAX_RES.get
    slist = slist['meta'] if isinstance(slist, dict) else slist

    def okres(x):
        """ Return True if resolution is within user specified maxres. """
        return int(x['quality'].split("x")[1]) <= maxres

    def getq(x):
        """ Return height aspect of resolution, eg 640x480 => 480. """
        return int(x['quality'].split("x")[1])

    def getbitrate(x):
        """Return the bitrate of a stream."""
        return x['rawbitrate']

    if audio:
        streams = [x for x in slist if x['mtype'] == "audio"]
        if not m4a_ok:
            streams = [x for x in streams if not x['ext'] == "m4a"]
        if not config.AUDIO_FORMAT.get == "auto":
            if m4a_ok and config.AUDIO_FORMAT.get == "m4a":
                streams = [x for x in streams if x['ext'] == "m4a"]
            if config.AUDIO_FORMAT.get == "webm":
                streams = [x for x in streams if x['ext'] == "webm"]
            if not streams:
                streams = [x for x in slist if x['mtype'] == "audio"]
        streams = sorted(streams, key=getbitrate, reverse=True)
    else:
        streams = [x for x in slist if x['mtype'] == "normal" and okres(x)]
        streams = sorted(streams, key=getq, reverse=True)

    util.dbg("select stream, q: %s, audio: %s, len: %s", q, audio, len(streams))

    try:
        ret = streams[q]

    except IndexError:
        ret = streams[0] if q and len(streams) else None

    return ret


def get_size(ytid, url, preloading=False):
    """ Get size of stream, try stream cache first. """
    # try cached value
    stream = [x for x in g.streams[ytid]['meta'] if x['url'] == url][0]
    size = stream['size']
    prefix = "preload: " if preloading else ""

    if not size == -1:
        util.dbg("%s%susing cached size: %s%s", c.g, prefix, size, c.w)

    else:
        screen.writestatus("Getting content length", mute=preloading)
        stream['size'] = _get_content_length(url, preloading=preloading)
        util.dbg("%s%s - content-length: %s%s", c.y, prefix, stream['size'], c.w)

    return stream['size']


def _get_content_length(url, preloading=False):
    """ Return content length of a url. """
    prefix = "preload: " if preloading else ""
    util.dbg(c.y + prefix + "getting content-length header" + c.w)
    response = urlopen(url)
    headers = response.headers
    cl = headers['content-length']
    return int(cl)


def preload(song, delay=2, override=False):
    """  Get streams. """
    args = (song, delay, override)
    t = threading.Thread(target=_preload, args=args)
    t.daemon = True
    t.start()


def _preload(song, delay, override):
    """  Get streams (runs in separate thread). """
    if g.preload_disabled:
        return

    ytid = song.ytid
    g.preloading.append(ytid)
    time.sleep(delay)
    video = config.SHOW_VIDEO.get
    video = True if override in ("fullscreen", "window", "forcevid") else video
    video = False if override == "audio" else video

    try:
        m4a = "mplayer" not in config.PLAYER.get
        streamlist = get(song)
        stream = select(streamlist, audio=not video, m4a_ok=m4a)

        if not stream and not video:
            # preload video stream, no audio available
            stream = select(streamlist, audio=False)

        get_size(ytid, stream['url'], preloading=True)

    except (ValueError, AttributeError, IOError) as e:
        util.dbg(e)  # Fail silently on preload

    finally:
        g.preloading.remove(song.ytid)
