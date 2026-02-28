from .base import ListViewItem
from .. import util as u


class ListSongtitle(ListViewItem):
    """Describes a user"""

    # pylint: disable=unused-argument
    _checked = False
    _certainty = 1.0

    def __init__(self, data, certainty=1.0):
        self._checked = True
        self._certainty = certainty
        super(ListSongtitle, self).__init__(data)

    def artist(self, l=10):
        """Get artist"""
        return u.uea_pad(l, self.data[0])

    def title(self, l=10):
        """Get title"""
        return u.uea_pad(l, self.data[1])

    def checked(self, l=10):
        """String from for checked"""
        return "  X  " if self._checked else "     "

    def certainty(self):
        """Float"""
        return self._certainty

    def is_checked(self):
        """Returns true if checked"""
        return self._checked

    def toggle(self):
        """Toggle checked status"""
        self._checked = not self._checked

    def ret(self):
        """Used in the ListView play function"""
        return "%s - %s" % (self.artist().strip(), self.title().strip())

    @staticmethod
    def return_field():
        """Determines which function will be called on selected items"""
        return "ret"
