try:
    import pylast
    has_pylast = True
except ImportError:
    has_pylast = False

from .. import g, util, config
from . import command


@command(r'lastfm_connect')
def init_network(verbose=True):
    """ Initialize the global pylast network variable """
    if not has_pylast :
        if verbose:
            pylast_url = 'https://github.com/pylast/pylast'
            g.message = '"pylast" module not found\n see %s' % (pylast_url)
        return

    # TODO: Add option to read lastfm config from file or env variable
    key = config.LASTFM_API_KEY.get
    secret = config.LASTFM_API_SECRET.get
    password = config.LASTFM_PASSWORD.get # already hashed
    username = config.LASTFM_USERNAME.get

    if not (key and secret and password and username):
        if verbose:
            util.xprint("Not all Last.fm credentials were set.")
        return

    try:
        g.lastfm_network = pylast.LastFMNetwork(api_key=key, api_secret=secret,
                                                username=username,
                                                password_hash=password)
        if verbose:
            g.message = "Last.fm authentication successful!"
    except (pylast.WSError, pylast.MalformedResponseError, pylast.NetworkError):
        if verbose:
            g.message = "Last.fm connection error: %s" % (str(e))
