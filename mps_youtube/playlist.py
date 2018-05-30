class Playlist:

    """ Representation of a playist, has list of songs. """

    def __init__(self, name=None, songs=None):
        """ class members. """
        self.name = name
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
        mins, secs = divmod(duration, 60)
        hours, mins = divmod(mins, 60)
        duration = '{H:02}:{M:02}:{S:02}'.format(H=hours, M=mins, S=secs)
        return duration


class Video:

    """ Class to represent a YouTube video. """
    description = ""
    def __init__(self, ytid, title, length):
        """ class members. """
        self.ytid = ytid
        self.title = title
        self.length = int(length)
