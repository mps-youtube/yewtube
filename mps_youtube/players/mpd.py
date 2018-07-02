from ..player import BasePlayer
from .. import config

try:
    import mpd as pympd
    HAS_PY_MPD = True
except ImportError:
    HAS_PY_MPD = False


class mpd(BasePlayer):
    def init_status(self):
        if not HAS_PY_MPD:
            return dict(valid=False, message="python-mpd2 not found. Install with pip install python-mpd2")

        self.mpdclient = pympd.MPDClient()

        try:
            self.connect()
        except Exception as e:
            return dict(valid=False, message=str(e))

        return dict(valid=True, message="player set to mpd", value=self.player)

    def connect(self):
        conf = dict([tuple(conf.split('=', 3)) for conf in config.PLAYERARGS.get.strip().split(' ') if conf])
        self.mpdclient.connect(conf.get('address', 'localhost'), int(conf.get('port', 6600)))

    def _launch_player(self):
        try:
            self.add_song()
        except pympd.base.ConnectionError:
            self.connect()

    def add_song(self):
        songid = self.mpdclient.addid(self.stream['url'],
                                      len(self.mpdclient.playlist()))
        meta = self.generate_metadata()
        self.mpdclient.addtagid(songid, 'title', meta['title'])
        self.mpdclient.addtagid(songid, 'artist', meta['artists'][0])
        self.mpdclient.addtagid(songid, 'album', meta['album'])
        self.mpdclient.addtagid(songid, 'title', meta['title'])
        self.mpdclient.play()
        self.next()

    def _help(self, short=True):
        pass
