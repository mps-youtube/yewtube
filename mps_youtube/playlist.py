import time


class Playlist(object):

    """ Representation of a playist, has list of songs. """

    def __init__(self, name=None, songs=None):
        """ class members. """
        self.name = name
        self.creation = time.time()
        self.songs = songs or []

    def __len__(self):
        """ Return number of tracks. """
        return len(self.songs)

    def __getitem__(self, sliced):
        return self.songs[sliced]

    def __setitem__(self, position, item):
        self.songs[position] = item

    def __iter__(self):
        for i in self.songs:
            yield i

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
