import os
import pickle


from . import g, c, streams
from .util import dbg


# Updated every time incompatible changes are made to cache format,
# So old cache can be dropped
CACHE_VERSION = 1

def load():
    """ Import cache file. """
    if os.path.isfile(g.CACHEFILE):

        try:

            with open(g.CACHEFILE, "rb") as cf:
                cached = pickle.load(cf)

            # Note: will be none for yewtube 0.2.5 or earlier
            version = cached.get('version')

            if 'streams' in cached:
                if version and version >= 1:
                    g.streams = cached['streams']
                    g.username_query_cache = cached['userdata']
            else:
                g.streams = cached

            if 'pafy' in cached:
                pass
                #pafy.load_cache(cached['pafy'])

            dbg(c.g + "%s cached streams imported%s", str(len(g.streams)), c.w)

        except (EOFError, IOError):
            dbg(c.r + "Cache file failed to open" + c.w)

        streams.prune()


def save():
    """ Save stream cache. """
    caches = dict(
        version=CACHE_VERSION,
        streams=g.streams,
        userdata=g.username_query_cache
        #,pafy=pafy.dump_cache()
    )

    with open(g.CACHEFILE, "wb") as cf:
        pickle.dump(caches, cf, protocol=2)

    dbg(c.p + "saved cache file: " + g.CACHEFILE + c.w)
