import time
import threading
from urllib.request import urlopen
from . import extractor
from . import g, c, screen, config, util


def prune():
    """Keep cache size in check."""
    while len(g.metadata_cache) > g.max_cached_streams:
        g.metadata_cache.popitem(last=False)

    while len(g.streams) > g.max_cached_streams:
        g.streams.popitem(last=False)

    # prune time expired items

    now = time.time()
    old_metadata = [
        k
        for k in g.metadata_cache
        if g.metadata_cache[k] is not None and g.metadata_cache[k].expiry < now
    ]

    if len(old_metadata):
        util.dbg(c.r + "%s old extractor items pruned%s", len(old_metadata), c.w)

    for old_entry in old_metadata:
        g.metadata_cache.pop(old_entry, 0)

    oldstreams = [
        k
        for k in g.streams
        if g.streams[k]["expiry"] is None or g.streams[k]["expiry"] < now
    ]

    if len(oldstreams):
        util.dbg(c.r + "%s old stream items pruned%s", len(oldstreams), c.w)

    for oldstream in oldstreams:
        g.streams.pop(oldstream, 0)

    util.dbg(
        c.b + "metadata: %s, streams: %s%s",
        len(g.metadata_cache),
        len(g.streams),
        c.w,
    )


def get(vid, force=False, callback=None, threeD=False):
    """Get all streams as a dict.  callback function passed to get_extractor."""
    now = time.time()
    ytid = vid.ytid
    have_stream = g.streams.get(ytid) and (
        g.streams[ytid]["expiry"] > now
        if g.streams[ytid]["expiry"] is not None
        else False
    )
    prfx = "preload: " if not callback else ""

    if not force and have_stream:
        ss = str(int(g.streams[ytid]["expiry"] - now) // 60)
        util.dbg(
            "%s%sGot streams from cache (%s mins left)%s", c.g, prfx, ss, c.w
        )
        return g.streams.get(ytid)["meta"]

    # p = None#util.get_metadata(vid, force=force, callback=callback)
    # ps = p.allstreams if threeD else [x for x in p.allstreams if not x.threed]
    ps = extractor.get_video_streams(ytid)

    streams = []
    for s in ps:
        # Determine stream type (audio, video, or both)
        vcodec = s.get("vcodec", "none")
        acodec = s.get("acodec", "none")
        
        if vcodec == "none" and acodec != "none":
            mtype = "audio"
        elif vcodec != "none" and acodec != "none":
            mtype = "video" # Mixed
        elif vcodec != "none" and acodec == "none":
            mtype = "video" # Video only
        else:
            mtype = "?"

        streams.append({
            "url": s["url"],
            "ext": s["ext"],
            "quality": s.get("resolution") or f"{s.get('width')}x{s.get('height')}",
            "rawbitrate": s.get("tbr") or s.get("abr") or -1,
            "mtype": mtype,
            "size": int(
                s.get("filesize")
                if s.get("filesize") is not None
                else s.get("filesize_approx", -1)
            ),
        })

    # Find expiry in URL if possible
    expiry = now + 3600 # Default fallback
    try:
        if "manifest" in streams[0]["url"]:
            expiry = float(streams[0]["url"].split("/expire/")[1].split("/")[0])
        elif "expire=" in streams[0]["url"]:
            temp = streams[0]["url"].split("expire=")[1]
            expiry = float(temp[: temp.find("&")])
    except (IndexError, ValueError):
        pass

    g.streams[ytid] = dict(expiry=expiry, meta=streams)
    prune()
    return streams


def select(slist, q=0, audio=False, m4a_ok=True, maxres=None):
    """Select a stream from stream list."""
    maxres = maxres or config.MAX_RES.get
    slist = slist["meta"] if isinstance(slist, dict) else slist

    def okres(x):
        """Return True if resolution is within user specified maxres."""
        try:
            res = x["quality"].split("x")
            height = int(res[1] if len(res) > 1 else res[0].strip("p"))
            return height <= maxres
        except (ValueError, IndexError, AttributeError):
            return True

    def getq(x):
        """Return height aspect of resolution, eg 640x480 => 480."""
        try:
            res = x["quality"].split("x")
            return int(res[1] if len(res) > 1 else res[0].strip("p"))
        except (ValueError, IndexError, AttributeError):
            return 0

    def getbitrate(x):
        """Return the bitrate of a stream."""
        return x["rawbitrate"]

    if audio:
        streams = [x for x in slist if x["mtype"] == "audio"]
        if not m4a_ok:
            streams = [x for x in streams if not x["ext"] == "m4a"]
        if not config.AUDIO_FORMAT.get == "auto":
            if m4a_ok and config.AUDIO_FORMAT.get == "m4a":
                streams = [x for x in streams if x["ext"] == "m4a"]
            if config.AUDIO_FORMAT.get == "webm":
                streams = [x for x in streams if x["ext"] == "webm"]
            if not streams:
                streams = [x for x in slist if x["mtype"] == "audio"]
        streams = sorted(streams, key=getbitrate, reverse=True)
    else:
        streams = [x for x in slist if x["mtype"] == "video" and okres(x)]
        if not config.VIDEO_FORMAT.get == "auto":
            if config.VIDEO_FORMAT.get == "mp4":
                streams = [x for x in streams if x["ext"] == "mp4"]
            if config.VIDEO_FORMAT.get == "webm":
                streams = [x for x in streams if x["ext"] == "webm"]
            if config.VIDEO_FORMAT.get == "3gp":
                streams = [x for x in streams if x["ext"] == "3gp"]
            if not streams:
                streams = [
                    x for x in slist if x["mtype"] == "video" and okres(x)
                ]
        streams = sorted(streams, key=getq, reverse=True)

    util.dbg("select stream, q: %s, audio: %s, len: %s", q, audio, len(streams))

    try:
        ret = streams[q]

    except IndexError:
        ret = streams[0] if q and len(streams) else None

    return ret


def get_size(ytid, url, preloading=False):
    """Get size of stream, try stream cache first."""
    # try cached value
    stream = [x for x in g.streams[ytid]["meta"] if x["url"] == url][0]
    size = stream["size"]
    prefix = "preload: " if preloading else ""

    if not size == -1:
        util.dbg("%s%susing cached size: %s%s", c.g, prefix, size, c.w)

    else:
        screen.writestatus("Getting content length", mute=preloading)
        stream["size"] = _get_content_length(url, preloading=preloading)
        util.dbg(
            "%s%s - content-length: %s%s", c.y, prefix, stream["size"], c.w
        )

    return stream["size"]


def _get_content_length(url, preloading=False):
    """Return content length of a url using HEAD request."""
    prefix = "preload: " if preloading else ""
    util.dbg(c.y + prefix + "getting content-length header" + c.w)
    try:
        from urllib.request import Request
        req = Request(url, method="HEAD")
        with urlopen(req, timeout=10) as response:
            return int(response.headers.get("content-length", -1))
    except Exception as e:
        util.dbg("%sfailed to get content-length: %s", prefix, e)
        return -1


def preload(song, delay=2, override=False):
    """Get streams."""
    args = (song, delay, override)
    t = threading.Thread(target=_preload, args=args)
    t.daemon = True
    t.start()


def _preload(song, delay, override):
    """Get streams (runs in separate thread)."""
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

        get_size(ytid, stream["url"], preloading=True)

    except Exception as e:
        util.dbg("Preload failed for %s: %s", ytid, e)
        # Never call input() in a background thread!

    finally:
        g.preloading.remove(song.ytid)
