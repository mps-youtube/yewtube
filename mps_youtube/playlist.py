import time


class Playlist(object):

    """ Representation of a playist, has list of songs. """

    def __init__(self, name=None, songs=None):
        """ class members. """
        self.name = name
        self.creation = time.time()
        self.songs = songs or []

    @property
    def is_empty(self):
        """ Return True / False if songs are populated or not. """
        return not self.songs

    @property
    def size(self):
        """ Return number of tracks. """
        return len(self.songs)

    @property
    def duration(self):
        """ Sum duration of the playlist. """
        duration = sum(s.length for s in self.songs)
        duration = time.strftime('%H:%M:%S', time.gmtime(int(duration)))
        return duration


class Video(object):

    """ Class to represent a YouTube video. """

    def __init__(self, ytid, title, length):
        """ class members. """
        self.ytid = ytid
        self.title = title
        self.length = int(length)
